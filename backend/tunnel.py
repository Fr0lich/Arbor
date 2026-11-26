import subprocess
import threading
import queue
import re
import socket
import logging
import sys
import time

import os
import urllib.request
import urllib.error
import ssl
import platform
import stat
import tarfile
import shutil
from collections import deque


def ensure_ssh_key():
    """Ensure an SSH key exists in ~/.ssh, generating one automatically if missing.

    Reverse tunnel services (Serveo, Pinggy, etc.) require an SSH client key pair
    for cryptographic session negotiation.
    """
    try:
        ssh_dir = os.path.expanduser('~/.ssh')
        os.makedirs(ssh_dir, exist_ok=True)
        key_path = os.path.join(ssh_dir, 'id_ed25519')
        rsa_path = os.path.join(ssh_dir, 'id_rsa')
        if not os.path.exists(key_path) and not os.path.exists(rsa_path):
            flags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith('win') else 0
            subprocess.run(
                ['ssh-keygen', '-t', 'ed25519', '-N', '', '-f', key_path, '-q'],
                capture_output=True,
                creationflags=flags,
                timeout=5
            )
        return key_path if os.path.exists(key_path) else rsa_path
    except Exception as e:
        logging.warning(f"Could not auto-generate SSH key: {e}")
        return None


_ANSI_ESCAPE_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')


from enum import Enum


class TunnelState(Enum):
    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RETRYING = "retrying"
    STOPPED = "stopped"


class ResilientSSHTunnel:
    """Resilient SSH reverse tunnel.

    Primary provider: Serveo (serveo.net, port 22), which delivers public HTTPS
    URLs in ~1.5s without registration, accounts, or auth requirements.
    Fallback providers (Pinggy, Localhost.run) are tried if Serveo is unreachable.
    """

    def __init__(self, port, preferred_provider=None):
        self.port = port
        self.preferred_provider = preferred_provider
        self.public_url = None
        self.process = None
        self.thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.state = TunnelState.IDLE
        self.recent_logs = deque(maxlen=50)
        self.last_error = None
        self.active_protocol = "ssh"
        self.edge_registered = False

    def start(self, url_callback, status_callback=None):
        with self._lock:
            if self.state in (TunnelState.CONNECTING, TunnelState.CONNECTED, TunnelState.RETRYING):
                return
            self._stop_event.clear()
            self.state = TunnelState.CONNECTING
            self.thread = threading.Thread(
                target=self._run,
                args=(url_callback, status_callback),
                daemon=True
            )
            self.thread.start()

    def _run(self, url_callback, status_callback):
        ensure_ssh_key()

        # Multi-provider configurations in priority order:
        # (host, port, remote_forward, pattern)
        providers = [
            (
                'serveo.net',
                '22',
                f'80:127.0.0.1:{self.port}',
                re.compile(r'(https://[a-zA-Z0-9.-]+\.(?:serveousercontent\.com|serveo\.net))')
            ),
            (
                'a.pinggy.io',
                '443',
                f'0:127.0.0.1:{self.port}',
                re.compile(r'(https://[a-zA-Z0-9.-]+?\.(?:free\.pinggy\.net|run\.pinggy-free\.link|a\.pinggy\.link|free\.pinggy\.link|pinggy\.link|pinggy\.net))')
            ),
            (
                'nokey@localhost.run',
                '22',
                f'80:127.0.0.1:{self.port}',
                re.compile(r'(https://[a-zA-Z0-9-]+\.lhr\.(?:life|rocks))')
            )
        ]

        if self.preferred_provider == 'pinggy':
            providers.insert(0, providers.pop(1))
        elif self.preferred_provider == 'localhost.run':
            providers.insert(0, providers.pop(2))

        flags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith('win') else 0
        known_hosts_null = 'NUL' if sys.platform.startswith('win') else '/dev/null'

        attempt = 0
        backoff = 2

        try:
            while not self._stop_event.is_set():
                provider_idx = attempt % len(providers)
                target_host, target_port, forward_rule, url_pattern = providers[provider_idx]

                if status_callback and attempt > 0:
                    status_callback(f"🔄 Connecting via {target_host.split('@')[-1]}...")

                cmd = [
                    'ssh',
                    '-T',
                    '-p', target_port,
                    '-o', 'StrictHostKeyChecking=no',
                    '-o', f'UserKnownHostsFile={known_hosts_null}',
                    '-o', 'LogLevel=ERROR',
                    '-o', 'ServerAliveInterval=15',
                    '-o', 'ServerAliveCountMax=3',
                    '-o', 'ConnectTimeout=10',
                    '-R', forward_rule,
                    target_host
                ]

                try:
                    self.process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        bufsize=1,
                        creationflags=flags
                    )

                    connected = False
                    url_deadline = time.time() + 12  # 12s per provider attempt


                    q = queue.Queue()
                    def _reader():
                        while True:
                            l = self.process.stdout.readline()
                            if not l:
                                break
                            q.put(l)
                    t = threading.Thread(target=_reader, daemon=True)
                    t.start()

                    while not self._stop_event.is_set():
                        if self.process.poll() is not None and q.empty():
                            break

                        try:
                            line = q.get(timeout=0.1)
                        except queue.Empty:
                            if not connected and time.time() > url_deadline:
                                logging.warning(f"Tunnel {target_host}: no URL received within 12s")
                                if status_callback and attempt >= len(providers):
                                    status_callback("🟡 Tunnel timeout — trying next provider...")
                                try:
                                    self.process.terminate()
                                    self.process.wait(timeout=1.0)
                                except Exception:
                                    try:
                                        self.process.kill()
                                    except Exception:
                                        pass
                                break
                            continue

                        clean_line = _ANSI_ESCAPE_RE.sub('', line).strip()
                        if not clean_line:
                            continue
                        self.recent_logs.append(clean_line)

                        # Explicitly skip promo links
                        if "dashboard.pinggy.io" in clean_line or "admin.localhost.run" in clean_line or "admin.pinggy.io" in clean_line:
                            continue

                        match = url_pattern.search(clean_line)
                        if match and not connected:
                            url = match.group(1).rstrip('/')
                            self.public_url = url
                            connected = True
                            attempt = 0
                            backoff = 2
                            if url_callback:
                                url_callback(self.public_url)

                        if not connected and time.time() > url_deadline:
                            logging.warning(f"Tunnel {target_host}: no URL received within 12s")
                            if status_callback and attempt >= len(providers):
                                status_callback("🟡 Tunnel timeout — trying next provider...")
                            try:
                                self.process.terminate()
                                self.process.wait(timeout=1.0)
                            except Exception:
                                try:
                                    self.process.kill()
                                except Exception:
                                    pass
                            break

                    if self.process and not self._stop_event.is_set():
                        try:
                            self.process.wait(timeout=0.5)
                        except Exception:
                            pass

                    if self._stop_event.is_set():
                        break


                except Exception as e:
                    logging.error(f"Tunnel error with {target_host}: {e}")

                finally:
                    if self.process and self._stop_event.is_set():
                        try:
                            self.process.terminate()
                            self.process.wait(timeout=1.0)
                        except Exception:
                            try:
                                self.process.kill()
                            except Exception:
                                pass
                    self.public_url = None

                if self._stop_event.is_set():
                    break

                attempt += 1
                if attempt >= len(providers) * 2:
                    if status_callback:
                        status_callback("🟡 Tunnel disconnected (Local Wi-Fi still active)")
                    break

                self._stop_event.wait(timeout=backoff)
                backoff = min(backoff * 1.5, 15)

        finally:
            with self._lock:
                proc = self.process
                self.process = None
                self.state = TunnelState.STOPPED
            if proc:
                try:
                    proc.terminate()
                    proc.wait(timeout=1.0)
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass

    def stop(self):
        self._stop_event.set()
        with self._lock:
            proc = self.process
            self.process = None
            self.public_url = None
            self.state = TunnelState.STOPPED
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=1.0)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass


def ensure_cloudflared():
    """Ensure the cloudflared binary exists locally, checking drop-in/PATH locations before downloading."""
    is_windows = sys.platform.startswith('win')
    binary_name = 'cloudflared.exe' if is_windows else 'cloudflared'

    # 1. Check drop-in locations first (next to Arbor.exe / app root / system PATH)
    #    so offline or GitHub-blocked museum PCs can supply cloudflared locally.
    dropin_candidates = []
    if getattr(sys, 'frozen', False):
        dropin_candidates.append(os.path.join(os.path.dirname(sys.executable), binary_name))
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dropin_candidates.append(os.path.join(app_root, binary_name))
    which_cf = shutil.which(binary_name) or shutil.which('cloudflared')
    if which_cf:
        dropin_candidates.append(which_cf)

    for cand in dropin_candidates:
        if cand and os.path.isfile(cand):
            return cand

    cf_dir = os.path.expanduser('~/.cloudflared')
    os.makedirs(cf_dir, exist_ok=True)
    binary_path = os.path.join(cf_dir, binary_name)

    if not os.path.exists(binary_path):
        system = platform.system().lower()
        machine = platform.machine().lower()

        # Map architecture
        if machine in ['x86_64', 'amd64']:
            arch = 'amd64'
        elif machine in ['arm64', 'aarch64']:
            arch = 'arm64'
        elif machine in ['i386', 'x86']:
            arch = '386'
        elif machine in ['arm']:
            arch = 'arm'
        else:
            arch = 'amd64' # fallback

        # Map OS and build URL
        base_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/"
        if system == 'windows':
            url = f"{base_url}cloudflared-windows-{arch}.exe"
            is_tgz = False
        elif system == 'darwin':
            url = f"{base_url}cloudflared-darwin-{arch}.tgz" # macOS uses a tgz
            is_tgz = True
        else: # linux
            url = f"{base_url}cloudflared-linux-{arch}"
            is_tgz = False

        logging.info(f"Downloading cloudflared from {url}...")

        last_error = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

                def _open_url(request):
                    try:
                        return urllib.request.urlopen(request)
                    except (ssl.SSLCertVerificationError, urllib.error.URLError) as ssl_err:
                        if isinstance(ssl_err, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(ssl_err) or "certificate verify failed" in str(ssl_err).lower():
                            logging.warning(f"SSL certificate verification failed for cloudflared download. Retrying with unverified context...")
                            unverified_ctx = ssl._create_unverified_context()
                            return urllib.request.urlopen(request, context=unverified_ctx)
                        raise

                if is_tgz:
                    temp_tgz = os.path.join(cf_dir, "cloudflared.tgz")
                    with _open_url(req) as response, open(temp_tgz, 'wb') as f:
                        shutil.copyfileobj(response, f)

                    with tarfile.open(temp_tgz, 'r:gz') as tar:
                        tar.extract('cloudflared', path=cf_dir)

                    os.remove(temp_tgz)
                else:
                    with _open_url(req) as response, open(binary_path, 'wb') as f:
                        shutil.copyfileobj(response, f)

                last_error = None
                break  # Success
            except Exception as e:
                logging.warning(f"Download attempt {attempt + 1} failed: {e}")
                last_error = e
                time.sleep(1) # simple backoff

        if last_error:
            raise Exception(f"Failed to download cloudflared after 3 attempts: {last_error}")

        # Make executable
        if not is_windows:
            st = os.stat(binary_path)
            os.chmod(binary_path, st.st_mode | stat.S_IEXEC)

    return binary_path

def _check_doh_dns_ready(hostname: str, timeout: float = 2.5):
    """Query Cloudflare 1.1.1.1 DNS-over-HTTPS directly (by IP, bypassing OS Dnscache)
    to verify a newly-minted trycloudflare.com hostname has propagated without poisoning
    the local OS negative DNS cache.

    Returns True if resolved, False if NXDOMAIN/pending, or None if DoH is unreachable.
    """
    import json
    from urllib.parse import quote
    doh_url = f"https://1.1.1.1/dns-query?name={quote(hostname)}&type=A"
    req = urllib.request.Request(
        doh_url,
        headers={"Accept": "application/dns-json", "User-Agent": "ArborProbe/1.0"},
    )
    try:
        try:
            resp_ctx = urllib.request.urlopen(req, timeout=timeout)
        except (ssl.SSLCertVerificationError, urllib.error.URLError) as ssl_err:
            if isinstance(ssl_err, ssl.SSLCertVerificationError) or "certificate" in str(ssl_err).lower():
                resp_ctx = urllib.request.urlopen(req, timeout=timeout, context=ssl._create_unverified_context())
            else:
                raise
        with resp_ctx as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("Status") == 0 and data.get("Answer"):
                return True
            return False
    except Exception:
        return None


def probe_public_url(url: str, timeout: float = 3.5):
    """Actively probe <url>/api/ping to verify DNS propagation and end-to-end reachability.

    Returns (ok: bool, detail: str).
    """
    if not url:
        return False, "No public URL available yet"
    ping_url = url.rstrip("/") + "/api/ping"
    req = urllib.request.Request(ping_url, headers={"User-Agent": "ArborProbe/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return True, "Reachable (HTTP 200)"
            return False, f"Unexpected HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (530, 502, 503, 504):
            return False, f"HTTP {e.code} (tunnel edge not ready or local server unreachable)"
        return False, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        reason = str(e.reason)
        low = reason.lower()
        if "getaddrinfo" in low or "name or service not known" in low or "nodename" in low or "11001" in low:
            return False, f"DNS not resolved yet (NXDOMAIN): {reason}"
        if "certificate" in low or "ssl" in low:
            return False, f"TLS/SSL interception or certificate error: {reason}"
        if "timed out" in low or "timeout" in low:
            return False, f"Connection timed out ({timeout}s)"
        return False, f"Network error: {reason}"
    except socket.timeout:
        return False, f"Connection timed out ({timeout}s)"
    except Exception as e:
        return False, f"Probe error: {e}"


class CloudflareTunnel:
    """Cloudflare Quick Tunnels (trycloudflare.com) with HTTP/2 firewall bypass,
    two-stage readiness verification (edge registration + /api/ping probe),
    log capture, and automatic reconnect.
    """

    def __init__(
        self,
        port,
        protocols=("http2", "quic"),
        max_attempts=3,
        verify_ping=True,
        tunnel_token=None,
        custom_public_url=None,
    ):
        self.port = port
        self.protocols = tuple(protocols) if protocols else ("http2", "quic")
        self.max_attempts = max(1, int(max_attempts))
        self.verify_ping = bool(verify_ping)
        self.tunnel_token = (tunnel_token or "").strip() or None
        self.custom_public_url = (custom_public_url or "").strip().rstrip("/") or None
        self.public_url = None
        self.process = None
        self.thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.state = TunnelState.IDLE
        self.recent_logs = deque(maxlen=50)
        self.active_protocol = self.protocols[0]
        self.edge_registered = False
        self.last_error = None

    def start(self, url_callback, status_callback=None):
        with self._lock:
            if self.state in (TunnelState.CONNECTING, TunnelState.CONNECTED, TunnelState.RETRYING):
                return
            self._stop_event.clear()
            self.last_error = None
            self.edge_registered = False
            self.state = TunnelState.CONNECTING
            self.thread = threading.Thread(
                target=self._run,
                args=(url_callback, status_callback),
                daemon=True
            )
            self.thread.start()

    def _terminate_proc(self, proc):
        if not proc:
            return
        try:
            proc.terminate()
            proc.wait(timeout=1.0)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    def _run(self, url_callback, status_callback):
        try:
            binary_path = ensure_cloudflared()
            if not binary_path:
                self.last_error = "Failed to download cloudflared binary"
                if status_callback:
                    status_callback("🔴 Failed to download cloudflared")
                with self._lock:
                    self.state = TunnelState.STOPPED
                return
        except Exception as e:
            self.last_error = str(e)
            logging.error(f"Failed to ensure cloudflared: {e}")
            if status_callback:
                status_callback(f"🔴 Failed to download cloudflared: {e}")
            with self._lock:
                self.state = TunnelState.STOPPED
            return

        flags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith('win') else 0
        url_pattern = re.compile(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)')
        backoff = 2.0

        try:
            for attempt in range(self.max_attempts):
                if self._stop_event.is_set():
                    break

                protocol = self.protocols[attempt % len(self.protocols)]
                self.active_protocol = protocol
                self.edge_registered = False
                candidate_url = self.custom_public_url if self.tunnel_token else None
                verified = False

                if self.tunnel_token:
                    cmd = [
                        binary_path,
                        'tunnel',
                        '--no-autoupdate',
                        '--protocol', protocol,
                        'run',
                        '--token', self.tunnel_token,
                    ]
                else:
                    cmd = [
                        binary_path,
                        'tunnel',
                        '--no-autoupdate',
                        '--protocol', protocol,
                        '--url', f'http://127.0.0.1:{self.port}',
                    ]

                if status_callback:
                    if attempt == 0:
                        status_callback(f"🔄 Starting Cloudflare tunnel ({protocol.upper()})…")
                    else:
                        status_callback(
                            f"🔄 Reconnecting Cloudflare ({protocol.upper()}, attempt {attempt + 1}/{self.max_attempts})…"
                        )

                proc = None
                try:
                    proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        bufsize=1,
                        creationflags=flags
                    )
                    with self._lock:
                        self.process = proc

                    q = queue.Queue()

                    def _cf_reader(_p=proc, _q=q):
                        try:
                            while True:
                                l = _p.stderr.readline()
                                if not l:
                                    break
                                _q.put(l)
                        except Exception:
                            pass

                    t = threading.Thread(target=_cf_reader, daemon=True)
                    t.start()

                    # Stage 1: Wait for URL + edge registration (25s deadline)
                    handshake_deadline = time.time() + 25.0
                    dns_wait_deadline = None
                    ping_deadline = None
                    next_check_at = 0.0
                    doh_confirmed = False
                    doh_checked = False

                    while not self._stop_event.is_set():
                        if proc.poll() is not None and q.empty():
                            if verified:
                                self.last_error = f"cloudflared exited unexpectedly (code {proc.returncode})"
                                if status_callback and not self._stop_event.is_set():
                                    status_callback("🟡 Cloudflare tunnel dropped — reconnecting…")
                            else:
                                self.last_error = f"cloudflared exited before connecting (code {proc.returncode})"
                            break

                        try:
                            line = q.get(timeout=0.1)
                            clean_line = _ANSI_ESCAPE_RE.sub('', line).strip()
                            if clean_line:
                                self.recent_logs.append(clean_line)
                                if not candidate_url:
                                    match = url_pattern.search(clean_line)
                                    if match:
                                        candidate_url = match.group(1).rstrip('/')
                                        if status_callback:
                                            status_callback(f"🔄 Registering Cloudflare edge ({protocol.upper()})…")
                                if "registered tunnel connection" in clean_line.lower():
                                    self.edge_registered = True
                                    if dns_wait_deadline is None:
                                        dns_wait_deadline = time.time() + 14.0
                                        next_check_at = time.time() + 1.0
                                        if status_callback:
                                            status_callback("🔄 Waiting for Cloudflare DNS propagation…")
                        except queue.Empty:
                            pass

                        # Stage 2: Non-poisoning DoH DNS check -> /api/ping probe
                        if not verified and candidate_url and self.edge_registered:
                            if not self.verify_ping:
                                verified = True
                                with self._lock:
                                    self.public_url = candidate_url
                                    self.state = TunnelState.CONNECTED
                                if url_callback:
                                    url_callback(candidate_url)
                            elif not doh_checked and time.time() >= next_check_at:
                                from urllib.parse import urlparse
                                host = urlparse(candidate_url).hostname or ""
                                doh_res = _check_doh_dns_ready(host, timeout=2.5) if host else None
                                if doh_res is True:
                                    doh_confirmed = True
                                    doh_checked = True
                                    ping_deadline = time.time() + 12.0
                                    next_check_at = time.time() + 1.5
                                    if status_callback:
                                        status_callback("🔄 Verifying public URL reachability…")
                                elif doh_res is None or (dns_wait_deadline and time.time() > dns_wait_deadline):
                                    # DoH unreachable or timed out — wait a short grace period then probe directly
                                    doh_checked = True
                                    ping_deadline = time.time() + 12.0
                                    next_check_at = time.time() + 2.5
                                    if status_callback:
                                        status_callback("🔄 Verifying public URL reachability…")
                                else:
                                    next_check_at = time.time() + 1.2
                            elif doh_checked and time.time() >= next_check_at:
                                ok, detail = probe_public_url(candidate_url, timeout=3.5)
                                if ok:
                                    verified = True
                                    self.last_error = None
                                    with self._lock:
                                        self.public_url = candidate_url
                                        self.state = TunnelState.CONNECTED
                                    if url_callback:
                                        url_callback(candidate_url)
                                else:
                                    self.last_error = detail
                                    if ping_deadline and time.time() > ping_deadline:
                                        # If DoH confirmed DNS + edge is registered and only local OS DNS lags,
                                        # emit the URL rather than killing a live tunnel; phones on 4G/5G can reach it.
                                        if doh_confirmed and "nxdomain" in detail.lower():
                                            verified = True
                                            with self._lock:
                                                self.public_url = candidate_url
                                                self.state = TunnelState.CONNECTED
                                            if url_callback:
                                                url_callback(candidate_url)
                                        else:
                                            logging.warning(f"Cloudflare URL failed reachability probe: {detail}")
                                            break
                                    else:
                                        next_check_at = time.time() + 2.0

                        # Handshake timeout check
                        if not verified and not self.edge_registered and time.time() > handshake_deadline:
                            self.last_error = (
                                f"Timed out waiting for Cloudflare edge registration ({protocol.upper()})"
                            )
                            logging.warning(self.last_error)
                            break

                except Exception as e:
                    self.last_error = str(e)
                    logging.error(f"Cloudflare tunnel error ({protocol}): {e}")
                finally:
                    self._terminate_proc(proc)
                    with self._lock:
                        if self.process is proc:
                            self.process = None
                        self.public_url = None
                        if not self._stop_event.is_set():
                            self.state = TunnelState.RETRYING

                if self._stop_event.is_set():
                    break

                if attempt + 1 < self.max_attempts:
                    self._stop_event.wait(timeout=backoff)
                    backoff = min(backoff * 1.5, 8.0)

            if not self._stop_event.is_set() and status_callback:
                err_hint = f" ({self.last_error})" if self.last_error else ""
                status_callback(
                    f"🔴 Cloudflare unreachable{err_hint} — try Switch Provider or Test Connection"
                )
        finally:
            self.stop()

    def stop(self):
        self._stop_event.set()
        with self._lock:
            proc = self.process
            self.process = None
            self.public_url = None
            self.edge_registered = False
            self.state = TunnelState.STOPPED
        self._terminate_proc(proc)


def run_connection_diagnostics(server=None, tunnel=None, local_ip=None):
    """Run a 5-step end-to-end connectivity diagnostic for Arbor Mobile Companion.

    Returns a list of dicts:
        [{"step": str, "status": "pass"|"warn"|"fail", "detail": str, "advice": str}, ...]
    """
    results = []
    lip = local_ip or get_local_ip()

    # Step 1: Local Arbor Server (127.0.0.1)
    if server is None:
        results.append({
            "step": "1. Local Arbor Server",
            "status": "fail",
            "detail": "Mobile server is not started.",
            "advice": "Click 'Start Mobile Server' first.",
        })
    else:
        ok, detail = (
            server.check_local_health(timeout=1.5)
            if hasattr(server, "check_local_health")
            else probe_public_url(f"http://127.0.0.1:{server.port}", timeout=1.5)
        )
        results.append({
            "step": "1. Local Arbor Server",
            "status": "pass" if ok else "fail",
            "detail": detail,
            "advice": "" if ok else "Restart Mobile Companion or close any conflicting app using the port.",
        })

    # Step 2: LAN / Local Wi-Fi Interface
    if server is None:
        results.append({
            "step": "2. Local Wi-Fi (LAN)",
            "status": "warn",
            "detail": f"Detected IP: {lip} (server not running).",
            "advice": "",
        })
    else:
        lan_ok, lan_detail = probe_public_url(f"http://{lip}:{server.port}", timeout=2.0)
        results.append({
            "step": "2. Local Wi-Fi (LAN)",
            "status": "pass" if lan_ok else "warn",
            "detail": f"{lip}:{server.port} — {lan_detail}",
            "advice": (
                ""
                if lan_ok
                else "Windows Firewall or a Public network profile may be blocking LAN access. Set Wi-Fi to Private or allow Arbor in Windows Defender Firewall."
            ),
        })

    # Step 3: Outbound Internet (TCP/443)
    inet_ok = False
    inet_detail = ""
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=2.5):
            inet_ok = True
            inet_detail = "Outbound HTTPS (port 443) reachable"
    except Exception as e:
        inet_detail = f"Cannot reach 1.1.1.1:443 ({e})"
    results.append({
        "step": "3. Outbound Internet (HTTPS 443)",
        "status": "pass" if inet_ok else "fail",
        "detail": inet_detail,
        "advice": (
            ""
            if inet_ok
            else "Check Wi-Fi / captive portal login, or use Phone Hotspot + LAN-only mode."
        ),
    })

    # Step 4: Tunnel Process & Protocol
    if tunnel is None:
        results.append({
            "step": "4. Public Tunnel Process",
            "status": "warn",
            "detail": "No public tunnel active (LAN-only mode or stopped).",
            "advice": "Enable Public (Internet) mode if you need to connect across campus/Eduroam Wi-Fi.",
        })
    else:
        t_name = type(tunnel).__name__
        proto = getattr(tunnel, "active_protocol", "unknown")
        state_val = getattr(getattr(tunnel, "state", None), "value", "unknown")
        proc = getattr(tunnel, "process", None)
        alive = proc is not None and proc.poll() is None
        edge_ok = getattr(tunnel, "edge_registered", False)
        last_err = getattr(tunnel, "last_error", None)
        if alive and state_val == "connected":
            results.append({
                "step": "4. Public Tunnel Process",
                "status": "pass",
                "detail": f"{t_name} running ({proto}), state={state_val}, edge_registered={edge_ok}",
                "advice": "",
            })
        elif alive and state_val in ("connecting", "retrying"):
            results.append({
                "step": "4. Public Tunnel Process",
                "status": "warn",
                "detail": f"{t_name} still connecting ({proto}, state={state_val})" + (f" — {last_err}" if last_err else ""),
                "advice": "Wait a few seconds and re-run Test Connection, or click Switch Provider.",
            })
        else:
            results.append({
                "step": "4. Public Tunnel Process",
                "status": "fail",
                "detail": f"{t_name} not running ({proto}, state={state_val})" + (f" — {last_err}" if last_err else ""),
                "advice": "Click 'Reconnect' or 'Switch Provider' (Cloudflare ↔ Pinggy/SSH). If campus IT blocks all tunnels, use Phone Hotspot + LAN mode.",
            })

    # Step 5: Public URL End-to-End Probe
    pub_url = getattr(tunnel, "public_url", None) if tunnel is not None else None
    if not pub_url:
        results.append({
            "step": "5. Public URL Reachability",
            "status": "warn" if tunnel is None else "fail",
            "detail": "No active public URL to probe.",
            "advice": "" if tunnel is None else "Wait for tunnel connection, click Reconnect, or switch tunnel provider.",
        })
    else:
        pub_ok, pub_detail = probe_public_url(pub_url, timeout=4.0)
        advice = ""
        if not pub_ok:
            low = pub_detail.lower()
            if "nxdomain" in low or "dns" in low:
                advice = "Campus DNS may still be propagating or filtering trycloudflare.com. Click Reconnect for a fresh link or Switch Provider to Pinggy/SSH."
            elif "530" in low or "502" in low or "edge" in low:
                advice = "Tunnel edge dropped or local server stopped. Click Reconnect."
            elif "ssl" in low or "tls" in low:
                advice = "A corporate proxy may be intercepting HTTPS. Try Switch Provider or Phone Hotspot + LAN mode."
            else:
                advice = "Try Reconnect, Switch Provider, or Phone Hotspot + LAN mode."
        results.append({
            "step": "5. Public URL Reachability",
            "status": "pass" if pub_ok else "fail",
            "detail": f"{pub_url} — {pub_detail}",
            "advice": advice,
        })

    return results


def format_diagnostic_report(results, server=None, tunnel=None, local_ip=None) -> str:
    """Format a shareable, token/PIN-redacted diagnostic report for IT support or maintainers."""
    import config as _cfg
    lines = [
        "=== Arbor Mobile Companion Diagnostic Report ===",
        f"Arbor Version : {getattr(_cfg, 'APP_VERSION', 'unknown')}",
        f"OS / Platform : {platform.platform()}",
        f"Python        : {platform.python_version()}",
        f"Local IP      : {local_ip or get_local_ip()}",
        f"Server Port   : {getattr(server, 'port', 'N/A')} (running={getattr(server, 'is_running', False)})",
        f"Tunnel        : {type(tunnel).__name__ if tunnel else 'None'} (protocol={getattr(tunnel, 'active_protocol', 'N/A')}, state={getattr(getattr(tunnel, 'state', None), 'value', 'N/A')})",
        "",
        "--- Check Results ---",
    ]
    icons = {"pass": "[PASS]", "warn": "[WARN]", "fail": "[FAIL]"}
    for r in results:
        lines.append(f"{icons.get(r['status'], '[INFO]')} {r['step']}: {r['detail']}")
        if r.get("advice"):
            lines.append(f"       -> {r['advice']}")

    logs = list(getattr(tunnel, "recent_logs", [])) if tunnel is not None else []
    if logs:
        lines.append("")
        lines.append("--- Recent Tunnel Logs (last 15 lines) ---")
        lines.extend(logs[-15:])

    report = "\n".join(lines)

    # Redact any session token, PIN, or Named Cloudflare Tunnel token that could appear
    if server is not None:
        tok = getattr(server, "session_token", None)
        if tok and len(str(tok)) >= 6:
            report = report.replace(str(tok), "[REDACTED_TOKEN]")
        pin = getattr(server, "pin", None)
        if pin and len(str(pin)) >= 4:
            report = re.sub(rf"(?i)(pin\s*[:=]\s*){re.escape(str(pin))}", r"\1[REDACTED_PIN]", report)
    if tunnel is not None:
        cf_tok = getattr(tunnel, "tunnel_token", None)
        if cf_tok and len(str(cf_tok)) >= 6:
            report = report.replace(str(cf_tok), "[REDACTED_CF_TOKEN]")
    report = re.sub(r"([?&]token=)[^&\s]+", r"\1[REDACTED_TOKEN]", report)
    return report


def _classify_local_ip(ip: str) -> str:
    """Return a human-friendly label for a local IPv4 address (Tailscale, Hotspot/USB, or Wi-Fi/LAN)."""
    parts = ip.split(".")
    if len(parts) == 4:
        try:
            a, b = int(parts[0]), int(parts[1])
            # Tailscale CGNAT range: 100.64.0.0/10
            if a == 100 and 64 <= b <= 127:
                return "🛡️ Tailscale"
            # Common mobile hotspot / USB tethering subnets (Windows, iPhone, Android)
            if (a == 192 and b == 168 and int(parts[2]) in (42, 43, 137)) or (a == 172 and b == 20 and int(parts[2]) == 10):
                return "📱 Hotspot / USB"
        except ValueError:
            pass
    return "📶 Wi-Fi / LAN"


def get_all_local_ips():
    """Return a deduplicated list of (ip, label) tuples for all active non-loopback IPv4 interfaces."""
    seen = []
    primary = get_local_ip()
    if primary and primary != "127.0.0.1":
        seen.append(primary)
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if (
                ip
                and not ip.startswith("127.")
                and not ip.startswith("169.254.")
                and ip not in seen
            ):
                seen.append(ip)
    except Exception:
        pass
    if not seen:
        seen.append("127.0.0.1")
    return [(ip, _classify_local_ip(ip)) for ip in seen]


# Backwards-compatible aliases — callers import without changes
class LocalhostRunTunnel(ResilientSSHTunnel):
    def __init__(self, port):
        super().__init__(port, preferred_provider='localhost.run')

class PinggyTunnel(ResilientSSHTunnel):
    def __init__(self, port):
        super().__init__(port, preferred_provider='pinggy')


def get_local_ip():
    """Discover the most suitable local LAN / Wi-Fi IP address for the mobile companion."""
    # 1. Direct UDP gateway probe using public/local DNS targets
    for target in [('8.8.8.8', 80), ('1.1.1.1', 80), ('10.255.255.255', 1)]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            s.connect(target)
            ip = s.getsockname()[0]
            s.close()
            # Ignore loopback, VirtualBox host-only, and APIPA autoconfig addresses
            if ip and not ip.startswith('127.') and not ip.startswith('192.168.56.') and not ip.startswith('169.254.'):
                return ip
        except Exception:
            pass

    # 2. Enumerate host IP list prioritizing physical private LAN / Wi-Fi ranges
    try:
        host_ips = socket.gethostbyname_ex(socket.gethostname())[2]

        # Priority 2a: Standard home/office Wi-Fi (192.168.x.x excluding VirtualBox 192.168.56.x)
        for ip in host_ips:
            if ip.startswith('192.168.') and not ip.startswith('192.168.56.') and not ip.startswith('127.'):
                return ip

        # Priority 2b: Standard 10.x private LAN
        for ip in host_ips:
            if ip.startswith('10.') and not ip.startswith('127.'):
                return ip

        # Priority 2c: 172.16 - 172.31 private LAN (deprioritizing default Docker bridge 172.17.x.x)
        for ip in host_ips:
            if ip.startswith('172.') and not ip.startswith('172.17.') and not ip.startswith('127.'):
                return ip

        for ip in host_ips:
            if ip.startswith('172.') and not ip.startswith('127.'):
                return ip

        # Priority 2d: Any remaining 192.168.x.x (including host-only if nothing else)
        for ip in host_ips:
            if ip.startswith('192.168.') and not ip.startswith('127.'):
                return ip

        # Priority 2e: Any non-loopback, non-APIPA IP
        for ip in host_ips:
            if not ip.startswith('127.') and not ip.startswith('169.254.'):
                return ip
    except Exception:
        pass

    return '127.0.0.1'
