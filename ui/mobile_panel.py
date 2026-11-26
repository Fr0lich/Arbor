import os
import queue
import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime
import qrcode
from PIL import ImageTk
import config
from config import sc

from backend.mobile_server import MobileServer, get_local_ip, is_waitress_available
from backend.tunnel import (
    PinggyTunnel,
    CloudflareTunnel,
    get_all_local_ips,
    run_connection_diagnostics,
    format_diagnostic_report,
)


from enum import Enum


class MobileConnectionState(Enum):
    STOPPED = "stopped"
    LOCAL_READY = "local_ready"
    TUNNEL_CONNECTING = "tunnel_connecting"
    TUNNEL_READY = "tunnel_ready"
    ERROR = "error"


class MobilePanel:
    """Shared mobile companion panel.

    Renders the full mobile-session UI — QR code, status pill, URL/PIN,
    tunnel status, lock notice, and activity feed.  Both MobileHostApp
    (standalone window) and MobileDialog (in-app Toplevel) embed this
    panel and supply context-specific callbacks for session lifecycle
    actions that differ between the two entry points.

    Parameters
    ----------
    parent : tk widget
        Frame or window to pack the panel into.
    app_state : AppState
        Shared application state (df_reg, excel_path, …).
    root_tk : tk.Tk
        The root Tk window used for after() scheduling.
    port : int
        Port the MobileServer listens on (default 5055).
    on_end_session : callable, optional
        Called when the user clicks "🔴 End Mobile Session".
        The wrapper is responsible for any saving / cleanup beyond
        stopping the tunnel (which the panel always does first).
    on_edit : callable(oid, summary), optional
        Extra hook fired on every incoming mobile edit — used by the
        in-app dialog to notify the main desktop UI.
    reuse_server : MobileServer or None
        Pass a live MobileServer instance to reuse across re-opens
        (in-app dialog mode).  If None a fresh server is started.
    """

    def __init__(
        self,
        parent,
        app_state,
        root_tk,
        port=5055,
        on_end_session=None,
        on_edit=None,
        reuse_server=None,
        parent_ui=None,
        on_server_started=None,
    ):
        self.parent = parent
        self.app_state = app_state
        self.root = root_tk
        self.port = port
        self.on_end_session = on_end_session
        self.on_edit = on_edit
        self.parent_ui = parent_ui
        self.on_server_started = on_server_started

        self.server = reuse_server
        self.tunnel = None
        self._destroyed = False
        self._ui_queue = queue.Queue()
        self.connection_state = MobileConnectionState.STOPPED
        self.qr_image_ref = None
        self.local_url_with_token = ""
        self.public_url_with_token = ""
        self.current_qr_mode = "public"  # public tunnel is the default
        self.ui_version_choice = tk.StringVar(value="v2")
        prefs = config.load_prefs() if hasattr(config, "load_prefs") else {}
        self.auto_save_var = tk.BooleanVar(value=bool(prefs.get("mobile_autosave_on_stop", False)))
        self.require_pin_var = tk.BooleanVar(value=bool(prefs.get("require_mobile_pin", True)))
        raw_tut_mode = prefs.get("mobile_phone_tutorial_mode")
        if raw_tut_mode in ("ask", "trainee", "helper", "off"):
            init_tut_mode = raw_tut_mode
        else:
            init_tut_mode = "off" if (prefs.get("mobile_show_walkthrough", True) is False) else "ask"
        self.phone_tutorial_mode_var = tk.StringVar(value=init_tut_mode)
        self.show_walkthrough_var = tk.BooleanVar(value=(init_tut_mode != "off"))

        self._build_ui()
        self._schedule_ui_drain()

    def _post_ui(self, fn):
        """Thread-safe dispatch of a UI callback onto the Tk main thread."""
        if not self._destroyed:
            self._ui_queue.put(fn)

    def _schedule_ui_drain(self):
        if self._destroyed:
            return
        try:
            while True:
                fn = self._ui_queue.get_nowait()
                try:
                    fn()
                except Exception:
                    pass
        except queue.Empty:
            pass
        if not self._destroyed:
            try:
                self.root.after(80, self._schedule_ui_drain)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        is_dark = getattr(self.parent_ui, "dark_mode_active", getattr(self.parent_ui, "dark_mode", False))
        self._bg_main = "#1e211f" if is_dark else "#ffffff"
        self._fg_title = "#85e89d" if is_dark else "#1b4332"

        main = tk.Frame(self.parent, bg=self._bg_main, padx=20, pady=16)
        main.pack(fill="both", expand=True)
        self._main = main
        main.bind("<Destroy>", lambda e: setattr(self, "_destroyed", True) if e.widget is main else None)

        # ── Header ────────────────────────────────────────────────────
        hdr = tk.Frame(main, bg=self._bg_main)
        hdr.pack(fill="x", pady=(0, 10))

        hdr_top = tk.Frame(hdr, bg=self._bg_main)
        hdr_top.pack(fill="x")

        import utils as _mob_utils
        _mob_icon = _mob_utils.load_app_icon_image(sc(22), master=hdr_top)
        mob_title_lbl = tk.Label(
            hdr_top,
            text=" Arbor Mobile Companion" if _mob_icon else "📱 Arbor Mobile Companion",
            image=_mob_icon if _mob_icon else "",
            compound="left" if _mob_icon else "none",
            font=("Lora", sc(15), "bold"),
            bg=self._bg_main,
            fg=self._fg_title,
        )
        if _mob_icon:
            mob_title_lbl._icon_ref = _mob_icon
        mob_title_lbl.pack(side="left", anchor="w")

        def _open_armed_guide():
            from ui.tutorials import start_armed_shelf_guide
            start_armed_shelf_guide(self.parent_ui or self.root)

        def _open_mobile_manual():
            from ui.help_dialogs import show_main_help
            show_main_help(self.parent_ui or self.root, initial_tab="mobile")

        tk.Button(
            hdr_top,
            text="📖 Mobile Guide",
            font=("Segoe UI", sc(8), "bold"),
            bg="#f2f5f1",
            fg="#2c302e",
            activebackground="#e2e8e3",
            activeforeground="#2c302e",
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=2,
            command=_open_mobile_manual,
        ).pack(side="right", anchor="e", padx=(4, 0))

        tk.Button(
            hdr_top,
            text="[?] Armed Shelf (45s)",
            font=("Segoe UI", sc(8), "bold"),
            bg="#eaf5ec",
            fg="#1b5e20",
            activebackground="#d4ecd9",
            activeforeground="#1b5e20",
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=2,
            command=_open_armed_guide,
        ).pack(side="right", anchor="e")

        tk.Label(
            hdr,
            text="Scan the QR code to inspect & edit records on your phone.",
            bg="#ffffff",
            fg="#5a655e",
            font=("Segoe UI", sc(9)),
        ).pack(anchor="w")

        # DB info line (filled in after server start when we know the path)
        self._db_info_lbl = tk.Label(
            hdr, text="", bg="#ffffff", fg="#5a655e", font=("Segoe UI", sc(8), "italic")
        )
        self._db_info_lbl.pack(anchor="w")

        # ── Setup Screen ──────────────────────────────────────────────
        self.setup_frame = tk.Frame(main, bg="#ffffff")
        self.setup_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Setup Status Pill
        setup_status_bar = tk.Frame(
            self.setup_frame, bg="#e8f5e9", bd=1, relief="solid", padx=10, pady=6)
        setup_status_bar.pack(fill="x", pady=(0, 10))

        setup_status_dot = tk.Label(
            setup_status_bar, text="●", fg="#2e7d32", bg="#e8f5e9", font=("Segoe UI", sc(12))
        )
        setup_status_dot.pack(side="left", padx=(0, 6))

        setup_status_lbl = tk.Label(
            setup_status_bar,
            text="⚙️ Setup — Configure Mobile Connection",
            bg="#e8f5e9",
            fg="#1b4332",
            font=("Segoe UI", sc(9), "bold"),
        )
        setup_status_lbl.pack(side="left")

        # Setup Card
        setup_card = tk.Frame(self.setup_frame, bg="#fbfbf9", bd=1,
                              relief="solid", padx=12, pady=12)
        setup_card.pack(fill="x", pady=(0, 10))

        # Network Mode Section
        tk.Label(
            setup_card,
            text="Network Mode:",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            setup_card,
            text="Choose how you want to connect to your mobile device.",
            font=("Segoe UI", sc(8)),
            bg="#fbfbf9",
            fg="#5a655e",
        ).pack(anchor="w", pady=(0, 2))
        self.net_hint_lbl = tk.Label(
            setup_card,
            text="• Public (Internet): Recommended for University / Eduroam Wi-Fi (bypasses AP firewall isolation)\n• LAN only: For private home Wi-Fi or offline portable routers",
            font=("Segoe UI", sc(7), "italic"),
            bg="#fbfbf9",
            fg="#2d6a4f",
            justify="left",
        )
        self.net_hint_lbl.pack(anchor="w", pady=(0, 6))

        self.network_choice = tk.StringVar(value="public")

        network_btn_frame = tk.Frame(setup_card, bg="#ffffff")
        network_btn_frame.pack(fill="x", pady=(0, 15))

        self.btn_net_public = tk.Button(
            network_btn_frame,
            text="🌐 Public (Internet)",
            font=("Segoe UI", sc(9), "bold"),
            bg="#1b4332",
            fg="white",
            relief="flat",
            padx=4,
            pady=4,
            command=lambda: self._switch_setup_mode("public"),
            cursor="hand2",
        )
        self.btn_net_public.pack(side="left", expand=True, fill="x", padx=(0, 1))

        self.btn_net_local = tk.Button(
            network_btn_frame,
            text="📶 LAN only",
            font=("Segoe UI", sc(9)),
            bg="#e0e3df",
            fg="#333",
            relief="flat",
            padx=4,
            pady=4,
            command=lambda: self._switch_setup_mode("local"),
            cursor="hand2",
        )
        self.btn_net_local.pack(side="right", expand=True, fill="x", padx=(1, 0))

        # Collapsible Advanced Options (Tunnel Provider & Classic V1) for a calm default setup card
        self._adv_expanded = False
        self.btn_adv_toggle = tk.Button(
            setup_card,
            text="▸ Advanced Connection & Version Options",
            font=("Segoe UI", sc(8), "bold"),
            bg="#fbfbf9",
            fg="#5a655e",
            activebackground="#ecefed",
            activeforeground="#1b4332",
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            command=self._toggle_advanced_setup,
        )
        self.btn_adv_toggle.pack(fill="x", pady=(10, 0))

        self.advanced_setup_frame = tk.Frame(setup_card, bg="#fbfbf9")

        # Tunnel Provider Section (inside advanced_setup_frame)
        self.provider_frame = tk.Frame(self.advanced_setup_frame, bg="#fbfbf9")
        self.provider_frame.pack(fill="x", pady=(6, 0))

        tk.Label(
            self.provider_frame,
            text="Tunnel Provider:",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            self.provider_frame,
            text="Cloudflare is recommended to bypass firewalls.",
            font=("Segoe UI", sc(8)),
            bg="#fbfbf9",
            fg="#5a655e",
        ).pack(anchor="w", pady=(0, 6))

        self.provider_choice = tk.StringVar(value="cloudflare")

        provider_btn_frame = tk.Frame(self.provider_frame, bg="#ffffff")
        provider_btn_frame.pack(fill="x", pady=(0, 4))

        self.btn_prov_cf = tk.Button(
            provider_btn_frame,
            text="☁️ Cloudflare",
            font=("Segoe UI", sc(9), "bold"),
            bg="#1b4332",
            fg="white",
            relief="flat",
            padx=4,
            pady=4,
            command=lambda: self._switch_provider("cloudflare"),
            cursor="hand2",
        )
        self.btn_prov_cf.pack(side="left", expand=True, fill="x", padx=(0, 1))

        self.btn_prov_pinggy = tk.Button(
            provider_btn_frame,
            text="🏓 Pinggy / SSH",
            font=("Segoe UI", sc(9)),
            bg="#e0e3df",
            fg="#333",
            relief="flat",
            padx=4,
            pady=4,
            command=lambda: self._switch_provider("pinggy"),
            cursor="hand2",
        )
        self.btn_prov_pinggy.pack(side="right", expand=True, fill="x", padx=(1, 0))

        # Interface Version Section (inside advanced_setup_frame)
        self.version_frame = tk.Frame(self.advanced_setup_frame, bg="#fbfbf9")
        self.version_frame.pack(fill="x", pady=(10, 0))

        tk.Label(
            self.version_frame,
            text="Interface Version:",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            self.version_frame,
            text="V2 Tabbed optimizes physical location and discrepancy resolution.",
            font=("Segoe UI", sc(8)),
            bg="#fbfbf9",
            fg="#5a655e",
        ).pack(anchor="w", pady=(0, 6))

        version_btn_frame = tk.Frame(self.version_frame, bg="#ffffff")
        version_btn_frame.pack(fill="x", pady=(0, 4))

        self.btn_ver_v2 = tk.Button(
            version_btn_frame,
            text="📑 V2 Tabbed (New)",
            font=("Segoe UI", sc(9), "bold"),
            bg="#1b4332",
            fg="white",
            relief="flat",
            padx=4,
            pady=4,
            command=lambda: self._switch_ui_version("v2"),
            cursor="hand2",
        )
        self.btn_ver_v2.pack(side="left", expand=True, fill="x", padx=(0, 1))

        self.btn_ver_v1 = tk.Button(
            version_btn_frame,
            text="📄 V1 Classic",
            font=("Segoe UI", sc(9)),
            bg="#e0e3df",
            fg="#333",
            relief="flat",
            padx=4,
            pady=4,
            command=lambda: self._switch_ui_version("v1"),
            cursor="hand2",
        )
        self.btn_ver_v1.pack(side="right", expand=True, fill="x", padx=(1, 0))

        # Experimental HTTP Server Engine Selector (inside advanced_setup_frame)
        self.server_engine_choice = tk.StringVar(value="flask")
        eng_frame = tk.Frame(self.advanced_setup_frame, bg="#fbfbf9")
        eng_frame.pack(fill="x", pady=(10, 0))
        tk.Label(
            eng_frame,
            text="HTTP Server Engine (Experimental):",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 2))
        waitress_ok = is_waitress_available()
        eng_hint = (
            "Flask is the tested default. Waitress is an experimental WSGI alternative (32 threads)."
            if waitress_ok
            else "Flask is the tested default. Waitress is not installed here (will fall back safely to Flask)."
        )
        tk.Label(
            eng_frame,
            text=eng_hint,
            font=("Segoe UI", sc(7.5)),
            bg="#fbfbf9",
            fg="#5a655e",
            wraplength=sc(430),
            justify="left",
        ).pack(anchor="w", pady=(0, 4))
        eng_btn_row = tk.Frame(eng_frame, bg="#ffffff")
        eng_btn_row.pack(fill="x", pady=(0, 2))

        def _set_engine(eng):
            self.server_engine_choice.set(eng)
            if eng == "flask":
                self.btn_eng_flask.config(bg="#1b4332", fg="white", font=("Segoe UI", sc(8.5), "bold"))
                self.btn_eng_waitress.config(bg="#e0e3df", fg="#333", font=("Segoe UI", sc(8.5)))
            else:
                self.btn_eng_waitress.config(bg="#1b4332", fg="white", font=("Segoe UI", sc(8.5), "bold"))
                self.btn_eng_flask.config(bg="#e0e3df", fg="#333", font=("Segoe UI", sc(8.5)))

        self.btn_eng_flask = tk.Button(
            eng_btn_row,
            text="Flask (Default)",
            font=("Segoe UI", sc(8.5), "bold"),
            bg="#1b4332",
            fg="white",
            relief="flat",
            padx=4,
            pady=3,
            command=lambda: _set_engine("flask"),
            cursor="hand2",
        )
        self.btn_eng_flask.pack(side="left", expand=True, fill="x", padx=(0, 1))
        self.btn_eng_waitress = tk.Button(
            eng_btn_row,
            text="Waitress (Experimental)",
            font=("Segoe UI", sc(8.5)),
            bg="#e0e3df",
            fg="#333",
            relief="flat",
            padx=4,
            pady=3,
            command=lambda: _set_engine("waitress"),
            cursor="hand2",
        )
        self.btn_eng_waitress.pack(side="right", expand=True, fill="x", padx=(1, 0))

        # Local Network Adapter Picker (LAN / Tailscale / Phone Hotspot / USB)
        adapter_frame = tk.Frame(self.advanced_setup_frame, bg="#fbfbf9")
        adapter_frame.pack(fill="x", pady=(10, 0))
        tk.Label(
            adapter_frame,
            text="Local Network Adapter (LAN / Tailscale / Hotspot):",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 2))
        self._ip_options = [("Auto", "Auto (Recommended)")] + [
            (ip, f"{lbl} — {ip}") for ip, lbl in get_all_local_ips()
        ]
        self.local_adapter_var = tk.StringVar(value=self._ip_options[0][1])
        ttk.Combobox(
            adapter_frame,
            textvariable=self.local_adapter_var,
            values=[disp for _, disp in self._ip_options],
            state="readonly",
            width=36,
            cursor="hand2",
        ).pack(anchor="w", fill="x", pady=(0, 2))

        # Optional Named Cloudflare Tunnel (Permanent Museum URL)
        named_cf_frame = tk.Frame(self.advanced_setup_frame, bg="#fbfbf9")
        named_cf_frame.pack(fill="x", pady=(10, 0))
        tk.Label(
            named_cf_frame,
            text="Named Cloudflare Tunnel (Optional — Permanent URL):",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 2))
        tk.Label(
            named_cf_frame,
            text="Leave blank to use automatic Quick Tunnels. Fill in both fields only if IT set up a permanent Cloudflare Tunnel.",
            font=("Segoe UI", sc(7.5)),
            bg="#fbfbf9",
            fg="#5a655e",
            wraplength=sc(430),
            justify="left",
        ).pack(anchor="w", pady=(0, 4))

        _prefs_cf = config.load_prefs() if hasattr(config, "load_prefs") else {}
        self.cf_named_token_var = tk.StringVar(value=str(_prefs_cf.get("mobile_cf_tunnel_token", "") or ""))
        self.cf_named_url_var = tk.StringVar(value=str(_prefs_cf.get("mobile_cf_custom_url", "") or ""))

        cf_tok_row = tk.Frame(named_cf_frame, bg="#fbfbf9")
        cf_tok_row.pack(fill="x", pady=1)
        tk.Label(cf_tok_row, text="Token:", font=("Segoe UI", sc(8)), bg="#fbfbf9", fg="#2c302e", width=8, anchor="w").pack(side="left")
        ttk.Entry(cf_tok_row, textvariable=self.cf_named_token_var, show="•", font=("Consolas", sc(8))).pack(side="left", fill="x", expand=True)

        cf_url_row = tk.Frame(named_cf_frame, bg="#fbfbf9")
        cf_url_row.pack(fill="x", pady=1)
        tk.Label(cf_url_row, text="URL:", font=("Segoe UI", sc(8)), bg="#fbfbf9", fg="#2c302e", width=8, anchor="w").pack(side="left")
        ttk.Entry(cf_url_row, textvariable=self.cf_named_url_var, font=("Consolas", sc(8))).pack(side="left", fill="x", expand=True)

        # Auto-save setting row
        self.autosave_row = tk.Frame(setup_card, bg="#fbfbf9")
        self.autosave_row.pack(fill="x", pady=(12, 0))

        tk.Label(
            self.autosave_row,
            text="On Session End:",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 2))

        autosave_pill_frame = tk.Frame(self.autosave_row, bg="#fbfbf9")
        autosave_pill_frame.pack(fill="x", pady=(0, 2))

        self.btn_autosave_toggle = tk.Button(
            autosave_pill_frame,
            font=("Segoe UI", sc(8), "bold"),
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._toggle_auto_save,
        )
        self.btn_autosave_toggle.pack(side="left")

        self.lbl_autosave_tip = tk.Label(
            self.autosave_row,
            font=("Segoe UI", sc(7), "italic"),
            bg="#fbfbf9",
            fg="#5a655e",
            anchor="w",
        )
        self.lbl_autosave_tip.pack(fill="x")

        # PIN security toggle row
        self.pin_toggle_row = tk.Frame(setup_card, bg="#fbfbf9")
        self.pin_toggle_row.pack(fill="x", pady=(10, 0))

        tk.Label(
            self.pin_toggle_row,
            text="Phone Login PIN:",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 2))

        pin_pill_frame = tk.Frame(self.pin_toggle_row, bg="#fbfbf9")
        pin_pill_frame.pack(fill="x", pady=(0, 2))

        self.btn_pin_toggle = tk.Button(
            pin_pill_frame,
            font=("Segoe UI", sc(8), "bold"),
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._toggle_pin_required,
        )
        self.btn_pin_toggle.pack(side="left")

        self.lbl_pin_tip = tk.Label(
            self.pin_toggle_row,
            font=("Segoe UI", sc(7), "italic"),
            bg="#fbfbf9",
            fg="#5a655e",
            anchor="w",
            justify="left",
            wraplength=420,
        )
        self.lbl_pin_tip.pack(fill="x")

        # Phone tutorial mode selector (compact dropdown so launcher stays clean and unintimidating)
        self.walkthrough_row = tk.Frame(setup_card, bg="#fbfbf9")
        self.walkthrough_row.pack(fill="x", pady=(10, 0))
        _tut_hdr = tk.Frame(self.walkthrough_row, bg="#fbfbf9")
        _tut_hdr.pack(fill="x")
        tk.Label(
            _tut_hdr,
            text="Phone tutorial:",
            font=("Inter", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
            anchor="w",
        ).pack(side="left", padx=(0, sc(8)))

        self._phone_tutorial_options = [
            ("ask", "Ask on the phone (recommended)"),
            ("trainee", "Trainee (completed desktop tutorial)"),
            ("helper", "Helper (helping out for a day)"),
            ("off", "Off"),
        ]
        self._phone_tutorial_val_to_lbl = dict(self._phone_tutorial_options)
        self._phone_tutorial_lbl_to_val = {lbl: val for val, lbl in self._phone_tutorial_options}
        self._phone_tutorial_display_var = tk.StringVar(
            value=self._phone_tutorial_val_to_lbl.get(
                self.phone_tutorial_mode_var.get(),
                self._phone_tutorial_options[0][1],
            )
        )

        def _on_tut_combo_selected(_event=None):
            lbl = self._phone_tutorial_display_var.get()
            mode_val = self._phone_tutorial_lbl_to_val.get(lbl, "ask")
            self.phone_tutorial_mode_var.set(mode_val)
            self._on_phone_tutorial_mode_changed()

        self.phone_tutorial_combo = ttk.Combobox(
            _tut_hdr,
            textvariable=self._phone_tutorial_display_var,
            values=[lbl for _, lbl in self._phone_tutorial_options],
            state="readonly",
            font=("Inter", sc(8.5)),
            cursor="hand2",
        )
        self.phone_tutorial_combo.pack(side="left", fill="x", expand=True)
        self.phone_tutorial_combo.bind("<<ComboboxSelected>>", _on_tut_combo_selected)

        tk.Label(
            self.walkthrough_row,
            text="Anyone can also start or change the tutorial later from the phone's Settings.",
            font=("Segoe UI", sc(7.5), "italic"),
            bg="#fbfbf9",
            fg="#5a655e",
            anchor="w",
            justify="left",
            wraplength=420,
        ).pack(fill="x", pady=(3, 0))

        self.start_btn = tk.Button(
            self.setup_frame,
            text="▶ Start Mobile Session",
            font=("Inter", sc(10), "bold"),
            bg="#3a7d44",
            fg="#ffffff",
            activebackground="#2d6336",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            pady=8,
            command=self._on_start_btn_clicked,
            cursor="hand2",
        )
        self.start_btn.pack(fill="x", pady=(10, 0))
        self.start_btn.tutorial_id = "mobile_start_btn"

        # ── Active Frame (Hidden initially) ───────────────────────────
        self.active_frame = tk.Frame(main, bg="#ffffff")
        # Do not pack active_frame yet

        # ── Status pill ───────────────────────────────────────────────
        self.status_bar = tk.Frame(
            self.active_frame, bg="#e8f5e9", bd=1, relief="solid", padx=10, pady=6)
        self.status_bar.pack(fill="x", pady=(0, 10))

        self.status_dot = tk.Label(
            self.status_bar, text="●", fg="#2e7d32", bg="#e8f5e9", font=("Segoe UI", sc(12))
        )
        self.status_dot.pack(side="left", padx=(0, 6))

        self.status_lbl = tk.Label(
            self.status_bar,
            text="🟢 Local Server Ready — Connecting public tunnel...",
            bg="#e8f5e9",
            fg="#1b4332",
            font=("Segoe UI", sc(9), "bold"),
        )
        self.status_lbl.pack(side="left")

        self.client_badge = tk.Label(
            self.status_bar, text="📱 Offline", bg="#e8f5e9", fg="#5a655e", font=("Segoe UI", sc(9))
        )
        self.client_badge.pack(side="right", padx=(0, 6))

        # ── QR + connection info ──────────────────────────────────────
        mid = tk.Frame(self.active_frame, bg="#fbfbf9", bd=1,
                       relief="solid", padx=12, pady=12)
        mid.pack(fill="x", pady=(0, 10))

        # QR box
        qr_box = tk.Frame(mid, bg="#ffffff", bd=1,
                          relief="solid", padx=6, pady=6)
        qr_box.pack(side="left", padx=(0, 14))

        self.qr_label = tk.Label(qr_box, bg="#ffffff")
        self.qr_label.pack()

        mode_btn_frame = tk.Frame(qr_box, bg="#ffffff")
        mode_btn_frame.pack(fill="x", pady=(4, 0))

        self.btn_qr_public = tk.Button(
            mode_btn_frame,
            text="🌐 Public (Internet)",
            font=("Segoe UI", sc(7), "bold"),
            bg="#1b4332",
            fg="white",
            relief="flat",
            padx=4,
            pady=1,
            command=lambda: self.switch_qr("public"),
            cursor="hand2",
        )
        self.btn_qr_public.pack(side="left", expand=True, fill="x", padx=1)

        self.btn_qr_local = tk.Button(
            mode_btn_frame,
            text="📶 LAN only",
            font=("Segoe UI", sc(7)),
            bg="#e0e3df",
            fg="#333",
            relief="flat",
            padx=4,
            pady=1,
            command=lambda: self.switch_qr("local"),
            cursor="hand2",
        )
        self.btn_qr_local.pack(side="right", expand=True, fill="x", padx=1)

        # Connection info
        info = tk.Frame(mid, bg="#fbfbf9")
        info.pack(side="left", fill="both", expand=True)

        tk.Label(
            info,
            text="1. Scan QR with phone camera",
            font=("Segoe UI", sc(9), "bold"),
            bg="#fbfbf9",
            fg="#1b4332",
        ).pack(anchor="w", pady=(0, 2))

        self.local_ip_lbl = tk.Label(
            info,
            text=f"📶 Local Wi-Fi IP: {get_local_ip()}",
            font=("Segoe UI", sc(9), "bold"),
            bg="#e8f5e9",
            fg="#1b4332",
            padx=4,
            pady=2,
            anchor="w",
        )
        self.local_ip_lbl.pack(anchor="w", fill="x", pady=(2, 4))

        tk.Label(
            info,
            text="Or open this link on your phone:",
            font=("Segoe UI", sc(8)),
            bg="#fbfbf9",
            fg="#5a655e",
        ).pack(anchor="w")

        url_frame = tk.Frame(info, bg="#fbfbf9")
        url_frame.pack(fill="x", pady=(2, 4))

        self.url_var = tk.StringVar(value="Initializing...")
        self.url_entry = ttk.Entry(
            url_frame, textvariable=self.url_var, font=("Consolas", sc(8)), state="readonly"
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_copy_url = tk.Button(
            url_frame,
            text="📋 Copy",
            font=("Segoe UI", sc(8)),
            bg="#e0e3df",
            fg="#1b4332",
            relief="flat",
            padx=6,
            pady=1,
            command=self._copy_pairing_url,
            cursor="hand2",
        )
        self.btn_copy_url.pack(side="right")

        pin_row = tk.Frame(info, bg="#fbfbf9")
        pin_row.pack(fill="x", pady=2)
        tk.Label(
            pin_row, text="PIN: ", font=("Segoe UI", sc(9), "bold"), bg="#fbfbf9", fg="#1b4332"
        ).pack(side="left")
        self.pin_var = tk.StringVar(value="----")
        self.pin_badge = tk.Label(
            pin_row,
            textvariable=self.pin_var,
            font=("Consolas", sc(11), "bold"),
            bg="#1b4332",
            fg="#ffffff",
            padx=8,
            pady=1,
        )
        self.pin_badge.pack(side="left")

        self.btn_active_pin_toggle = tk.Button(
            pin_row,
            font=("Segoe UI", sc(7), "bold"),
            relief="flat",
            padx=6,
            pady=1,
            cursor="hand2",
            command=self._toggle_pin_required,
        )
        self.btn_active_pin_toggle.pack(side="right")

        self.lbl_active_pin_warning = tk.Label(
            info,
            text="",
            font=("Segoe UI", sc(7), "bold"),
            bg="#fbfbf9",
            fg="#b45309",
            anchor="w",
            justify="left",
            wraplength=260,
        )

        self.tunnel_lbl = tk.Label(
            info,
            text="Tunnel: Establishing...",
            font=("Segoe UI", sc(8), "italic"),
            bg="#fbfbf9",
            fg="#d97706",
        )
        self.tunnel_lbl.pack(anchor="w", pady=(4, 0))

        # Active Connection Recovery & Diagnostics Toolbar
        diag_row = tk.Frame(info, bg="#fbfbf9")
        diag_row.pack(fill="x", pady=(6, 0))

        self.btn_reconnect_tunnel = tk.Button(
            diag_row,
            text="🔄 Reconnect",
            font=("Segoe UI", sc(7.5), "bold"),
            bg="#e0e3df",
            fg="#1b4332",
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            command=self._reconnect_tunnel,
        )
        self.btn_reconnect_tunnel.pack(side="left", padx=(0, 3))

        self.btn_switch_provider = tk.Button(
            diag_row,
            text="⇄ Switch Provider",
            font=("Segoe UI", sc(7.5), "bold"),
            bg="#e0e3df",
            fg="#1b4332",
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            command=self._switch_active_provider,
        )
        self.btn_switch_provider.pack(side="left", padx=(0, 3))

        self.btn_test_connection = tk.Button(
            diag_row,
            text="🩺 Test Connection",
            font=("Segoe UI", sc(7.5), "bold"),
            bg="#e8f5e9",
            fg="#1b5e20",
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            command=self._open_diagnostics_dialog,
        )
        self.btn_test_connection.pack(side="left")

        # Active Version Toggle
        active_ver_row = tk.Frame(info, bg="#fbfbf9")
        active_ver_row.pack(fill="x", pady=(4, 0))
        tk.Label(
            active_ver_row, text="UI Version: ", font=("Segoe UI", sc(8), "bold"), bg="#fbfbf9", fg="#1b4332"
        ).pack(side="left")
        
        self.btn_active_ver_v2 = tk.Button(
            active_ver_row,
            text="V2 Tabbed",
            font=("Segoe UI", sc(7), "bold"),
            bg="#1b4332",
            fg="white",
            relief="flat",
            padx=4,
            pady=1,
            command=lambda: self._switch_ui_version("v2"),
            cursor="hand2",
        )
        self.btn_active_ver_v2.pack(side="left", padx=(2, 1))

        self.btn_active_ver_v1 = tk.Button(
            active_ver_row,
            text="V1 Classic",
            font=("Segoe UI", sc(7)),
            bg="#e0e3df",
            fg="#333",
            relief="flat",
            padx=4,
            pady=1,
            command=lambda: self._switch_ui_version("v1"),
            cursor="hand2",
        )
        self.btn_active_ver_v1.pack(side="left", padx=1)

        # Link to main window's simultaneous edit toggle if it exists
        _p_ui = self.parent_ui or getattr(getattr(self.parent, "master", None), "parent_ui", None)
        if _p_ui is not None and hasattr(_p_ui, "simultaneous_edit_var"):
            simul_cb = ttk.Checkbutton(
                info,
                text="Enable simultaneous edit",
                variable=_p_ui.simultaneous_edit_var,
                command=_p_ui.toggle_simultaneous_edit,
                cursor="hand2"
            )
            simul_cb.pack(anchor="w", pady=(8, 0))

        # ── Session notice ────────────────────────────────────────────
        notice = tk.Frame(self.active_frame, bg="#fffbeb",
                          bd=1, relief="solid", padx=10, pady=6)
        notice.pack(fill="x", pady=(0, 10))
        self.notice_frame = notice

        self.notice_lbl = tk.Label(
            notice,
            text="",
            bg="#fffbeb",
            fg="#92400e",
            font=("Segoe UI", sc(8)),
            justify="left",
        )
        self.notice_lbl.pack(side="left", fill="x", expand=True)

        self.btn_active_autosave_toggle = tk.Button(
            notice,
            font=("Segoe UI", sc(8), "bold"),
            relief="flat",
            padx=6,
            pady=2,
            cursor="hand2",
            command=self._toggle_auto_save,
        )
        self.btn_active_autosave_toggle.pack(side="right", padx=(6, 0))

        # ── Activity feed ─────────────────────────────────────────────
        feed_frame = tk.LabelFrame(
            self.active_frame,
            text="Recent Mobile Activity",
            bg="#ffffff",
            font=("Segoe UI", sc(9), "bold"),
            fg="#1b4332",
            padx=8,
            pady=6,
        )
        feed_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.feed_list = tk.Listbox(
            feed_frame,
            bg="#fbfbf9",
            font=("Segoe UI", sc(9)),
            bd=0,
            highlightthickness=1,
            selectmode="none",
        )
        self.feed_list.pack(fill="both", expand=True, side="left")

        feed_scroll = ttk.Scrollbar(
            feed_frame, orient="vertical", command=self.feed_list.yview)
        feed_scroll.pack(side="right", fill="y")
        self.feed_list.config(yscrollcommand=feed_scroll.set)

        self.feed_list.insert(
            tk.END, "Session initialized. Ready for mobile connections.")

        # ── Bottom buttons ────────────────────────────────────────────
        bottom = tk.Frame(self.active_frame, bg=self._bg_main)
        bottom.pack(fill="x")

        self._save_now_btn = tk.Button(
            bottom,
            text="💾 Save Workbook Now",
            font=("Inter", sc(9), "bold"),
            bg="#eaf5ec",
            fg="#1b5e20",
            activebackground="#d4ecd9",
            relief="flat",
            highlightbackground="#3a7d44",
            highlightthickness=1,
            pady=6,
            command=self._save_workbook_now,
            cursor="hand2",
        )
        self._save_now_btn.pack(fill="x", pady=(0, 6))

        self._end_btn = tk.Button(
            bottom,
            text="End Mobile Session",
            font=("Inter", sc(9), "bold"),
            bg="#fdf2f2",
            fg="#ba1a1a",
            activebackground="#f9dcdc",
            activeforeground="#93000a",
            relief="flat",
            highlightbackground="#ba1a1a",
            highlightthickness=1,
            pady=6,
            command=self._on_end_btn,
            cursor="hand2",
        )
        self._end_btn.pack(fill="x")

        self._update_autosave_ui()
        self._update_pin_ui()

    def _save_workbook_now(self):
        """Save the active Excel workbook immediately without stopping the mobile session."""
        if self.parent_ui and hasattr(self.parent_ui, "save_session"):
            try:
                self.parent_ui.save_session("MOBILE_MANUAL_SAVE")
                self.log("💾 Workbook save requested from Mobile Companion.")
                return
            except Exception:
                pass
        if self.parent_ui and hasattr(self.parent_ui, "save_database"):
            try:
                self.parent_ui.save_database()
                self.log("💾 Workbook saved from Mobile Companion.")
            except Exception:
                pass

    def _on_phone_tutorial_mode_changed(self):
        mode = self.phone_tutorial_mode_var.get()
        if mode not in ("ask", "trainee", "helper", "off"):
            mode = "ask"
            self.phone_tutorial_mode_var.set(mode)
        self.show_walkthrough_var.set(mode != "off")
        try:
            prefs = config.load_prefs() or {}
            prefs["mobile_phone_tutorial_mode"] = mode
            prefs["mobile_show_walkthrough"] = (mode != "off")
            config.save_prefs(prefs)
        except Exception:
            pass
        if self.server and hasattr(self.server, "update_phone_tutorial_mode"):
            try:
                self.server.update_phone_tutorial_mode(mode)
            except Exception:
                pass

    def _on_walkthrough_toggle(self):
        enabled = bool(self.show_walkthrough_var.get())
        self.phone_tutorial_mode_var.set("ask" if enabled else "off")
        self._on_phone_tutorial_mode_changed()

    def _toggle_pin_required(self):
        new_val = not self.require_pin_var.get()
        self.require_pin_var.set(new_val)
        try:
            prefs = config.load_prefs() or {}
            prefs["require_mobile_pin"] = new_val
            config.save_prefs(prefs)
        except Exception:
            pass
        if self.server and hasattr(self.server, "update_pin_requirement"):
            try:
                self.server.update_pin_requirement(new_val)
            except Exception:
                pass
        self._update_pin_ui()

    def _toggle_advanced_setup(self):
        self._adv_expanded = not self._adv_expanded
        if self._adv_expanded:
            self.btn_adv_toggle.config(text="▾ Advanced Connection & Version Options")
            self.advanced_setup_frame.pack(fill="x", after=self.btn_adv_toggle)
        else:
            self.btn_adv_toggle.config(text="▸ Advanced Connection & Version Options")
            self.advanced_setup_frame.pack_forget()

    def _update_pin_ui(self):
        is_req = self.require_pin_var.get()
        is_public = getattr(self, "current_qr_mode", "public") == "public"
        if hasattr(self, "network_choice"):
            try:
                is_public = (self.network_choice.get() == "public")
            except Exception:
                pass

        if is_req:
            txt = "🔒 Require 4-Digit PIN: ON"
            short_txt = "PIN: ON"
            bg, fg = "#1b4332", "#ffffff"
            tip = "Phones entering the URL manually must enter the 4-digit PIN (QR scan still pairs in 1 tap)."
            tip_fg = "#5a655e"
            if self.server and hasattr(self.server, "pin"):
                self.pin_var.set(self.server.pin)
            if hasattr(self, "pin_badge") and self.pin_badge.winfo_exists():
                self.pin_badge.config(bg="#1b4332", fg="#ffffff")
            if hasattr(self, "lbl_active_pin_warning") and self.lbl_active_pin_warning.winfo_exists():
                self.lbl_active_pin_warning.pack_forget()
        else:
            txt = "🔓 Require 4-Digit PIN: OFF"
            short_txt = "PIN: OFF"
            bg, fg = "#e0e3df", "#333333"
            self.pin_var.set("OFF (Open)")
            if hasattr(self, "pin_badge") and self.pin_badge.winfo_exists():
                self.pin_badge.config(bg="#e0e3df", fg="#555555")
            if is_public:
                tip = "⚠ Public tunnel is active without a PIN — anyone with the link can edit. Recommended only on private Local Wi-Fi."
                tip_fg = "#b45309"
                if hasattr(self, "lbl_active_pin_warning") and self.lbl_active_pin_warning.winfo_exists():
                    self.lbl_active_pin_warning.config(text="⚠ Public tunnel open without PIN (use Local Wi-Fi)")
                    self.lbl_active_pin_warning.pack(anchor="w", pady=(2, 0))
            else:
                tip = "Open local Wi-Fi access — phones on your private vault router connect without typing a PIN."
                tip_fg = "#2d6a4f"
                if hasattr(self, "lbl_active_pin_warning") and self.lbl_active_pin_warning.winfo_exists():
                    self.lbl_active_pin_warning.pack_forget()

        if hasattr(self, "btn_pin_toggle") and self.btn_pin_toggle.winfo_exists():
            self.btn_pin_toggle.config(text=txt, bg=bg, fg=fg)
        if hasattr(self, "lbl_pin_tip") and self.lbl_pin_tip.winfo_exists():
            self.lbl_pin_tip.config(text=tip, fg=tip_fg)
        if hasattr(self, "btn_active_pin_toggle") and self.btn_active_pin_toggle.winfo_exists():
            self.btn_active_pin_toggle.config(text=short_txt, bg=bg, fg=fg)

    def _toggle_auto_save(self):
        new_val = not self.auto_save_var.get()
        self.auto_save_var.set(new_val)
        self._update_autosave_ui()
        try:
            prefs = config.load_prefs() or {}
            prefs["mobile_autosave_on_stop"] = new_val
            config.save_prefs(prefs)
        except Exception:
            pass

    def _update_autosave_ui(self):
        is_on = self.auto_save_var.get()
        if is_on:
            txt = "💾 Auto-save on stop: ON"
            tip = "Edits will automatically save to disk when server stops."
            bg = "#1b4332"
            fg = "#ffffff"
            notice_text = (
                "📱 Mobile session active. In-memory edits from your phone will be\n"
                "automatically saved to disk when you stop the server."
            )
        else:
            txt = "⏸️ Auto-save on stop: OFF (Prompt)"
            tip = "Arbor will ask whether to save when server stops."
            bg = "#e0e3df"
            fg = "#2c302e"
            notice_text = (
                "📱 Mobile session active. All edits are synced into memory.\n"
                "When you stop the server, Arbor will ask if you want to save to disk."
            )

        if hasattr(self, "btn_autosave_toggle") and self.btn_autosave_toggle:
            self.btn_autosave_toggle.config(text=txt, bg=bg, fg=fg)
        if hasattr(self, "lbl_autosave_tip") and self.lbl_autosave_tip:
            self.lbl_autosave_tip.config(text=tip)
        if hasattr(self, "btn_active_autosave_toggle") and self.btn_active_autosave_toggle:
            self.btn_active_autosave_toggle.config(text=txt, bg=bg, fg=fg)
        if hasattr(self, "notice_lbl") and self.notice_lbl:
            self.notice_lbl.config(text=notice_text)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def _on_start_btn_clicked(self):
        self.setup_frame.pack_forget()
        self.active_frame.pack(fill="both", expand=True)
        self._start_services()

    def start(self):
        """Dummy method to not break existing caller assumptions.
        Server now actually starts upon user interacting with UI.
        """
        pass

    def _get_selected_local_ip(self):
        """Return the user-selected local adapter IP, or auto-detected get_local_ip()."""
        if hasattr(self, "local_adapter_var") and hasattr(self, "_ip_options"):
            chosen = self.local_adapter_var.get()
            for ip, disp in self._ip_options:
                if disp == chosen and ip != "Auto":
                    return ip
        return get_local_ip()

    def _start_services(self):
        """Start (or reuse) MobileServer and conditionally launch tunnel."""
        # Start or reuse MobileServer — always verify it is actually running & healthy
        selected_engine = (
            self.server_engine_choice.get()
            if hasattr(self, "server_engine_choice")
            else "flask"
        )
        server_ok = True
        if self.server is None:
            self.server = MobileServer(
                self.app_state,
                root_tk=self.root,
                port=self.port,
                on_edit_callback=self._on_mobile_edit,
                server_engine=selected_engine,
            )
            server_ok = bool(self.server.start())
        else:
            self.server.app_state = self.app_state
            self.server.root_tk = self.root
            self.server.on_edit_callback = self._on_mobile_edit
            healthy = False
            if getattr(self.server, "is_running", False):
                if hasattr(self.server, "check_local_health"):
                    healthy, _ = self.server.check_local_health(timeout=1.0)
                else:
                    healthy = True
            if not healthy:
                server_ok = bool(self.server.start())
            elif hasattr(self.server, "_add_firewall_rule") and not getattr(self.server, "_firewall_rule_active", False):
                self.server._add_firewall_rule()

        if not server_ok:
            err_msg = getattr(self.server, "last_error", None) or "Local server did not respond on startup."
            self.connection_state = MobileConnectionState.ERROR
            self.status_dot.config(fg="#ba1a1a")
            self.status_lbl.config(text="🔴 Local Server Failed to Start", fg="#ba1a1a")
            self.tunnel_lbl.config(text=f"Error: {err_msg}", fg="#ba1a1a")
            self.url_var.set("Local server unavailable")
            self.log(f"🔴 Local server failed to start: {err_msg}")
            return

        self.server.on_client_connect_callback = self._on_client_connect
        self.server.on_presence_callback = self._on_client_presence
        self.app_state._mobile_server_instance = self.server
        if self.parent_ui is not None:
            self.parent_ui._mobile_server_instance = self.server
        if callable(self.on_server_started):
            try:
                self.on_server_started(self.server)
            except Exception:
                pass
        self._on_client_connect(len(self.server.clients))

        # Populate PIN and local URL (kept as LAN fallback)
        if hasattr(self.server, "update_pin_requirement"):
            self.server.update_pin_requirement(self.require_pin_var.get())
        if hasattr(self.server, "update_phone_tutorial_mode"):
            self.server.update_phone_tutorial_mode(self.phone_tutorial_mode_var.get())
        elif hasattr(self.server, "update_walkthrough_setting"):
            self.server.update_walkthrough_setting(self.show_walkthrough_var.get())
        self.pin_var.set(self.server.pin)
        self._update_pin_ui()
        local_ip = self._get_selected_local_ip()
        if hasattr(self, "local_ip_lbl") and self.local_ip_lbl:
            try:
                self.local_ip_lbl.config(text=f"📶 Local Wi-Fi IP: {local_ip}")
            except Exception:
                pass
        ver = self.ui_version_choice.get()
        v_path = "/v2" if ver == "v2" else "/"
        self.local_url_with_token = (
            f"http://{local_ip}:{self.server.port}{v_path}?token={self.server.session_token}"
        )

        # Update DB info label
        try:
            db_name = os.path.basename(self.app_state.excel_path or "")
            record_count = len(
                self.app_state.df_reg) if self.app_state.df_reg is not None else 0
            self._db_info_lbl.config(
                text=f"DB: {db_name}  ({record_count} records)")
        except Exception:
            pass

        choice = self.network_choice.get()
        if choice == "public":
            self.log(f"Local LAN ready: http://{local_ip}:{self.server.port}")
            provider = getattr(self, 'provider_choice', tk.StringVar(value='cloudflare')).get()
            self._launch_tunnel(provider)
        else:
            # Local only mode
            self.connection_state = MobileConnectionState.LOCAL_READY
            self.tunnel_lbl.config(
                text="Tunnel: Disabled (LAN Only)", fg="#5a655e")
            self.status_lbl.config(text="🟢 Local Server Ready", fg="#1b4332")
            self.status_dot.config(fg="#2e7d32")
            self.switch_qr("local")
            self.log(
                f"Server started in LAN-only mode: http://{local_ip}:{self.server.port}")

    def _launch_tunnel(self, provider="cloudflare"):
        """Stop any existing tunnel and launch a fresh public tunnel for the given provider."""
        if not self.server:
            return
        if self.tunnel:
            try:
                self.tunnel.stop()
            except Exception:
                pass
            self.tunnel = None

        self.public_url_with_token = ""
        self.connection_state = MobileConnectionState.TUNNEL_CONNECTING
        self.current_qr_mode = "public"
        if hasattr(self, "provider_choice"):
            self.provider_choice.set(provider)

        prov_label = "Cloudflare (HTTP/2)" if provider == "cloudflare" else "Pinggy / SSH"
        self.url_var.set(f"🔄 Connecting {prov_label}…")
        try:
            self.qr_image_ref = None
            self.qr_label.config(
                image="",
                text=f"⏳ Connecting {prov_label}…\n\nVerifying DNS & link.\n(Or click 'Local Wi-Fi' above)",
            )
            self.btn_qr_public.config(
                text="🌐 Public (Internet)",
                bg="#1b4332", fg="white", font=("Segoe UI", sc(7), "bold"),
            )
            self.btn_qr_local.config(
                bg="#e0e3df", fg="#333", font=("Segoe UI", sc(7)),
            )
            self.status_dot.config(fg="#d97706")
            self.status_lbl.config(text=f"🔄 Connecting {prov_label}…", fg="#d97706")
            self.tunnel_lbl.config(text=f"Tunnel: Starting {prov_label}…", fg="#d97706")
        except Exception:
            pass

        self.log(f"Establishing secure public tunnel via {prov_label}...")
        if provider == "cloudflare":
            cf_tok = self.cf_named_token_var.get().strip() if hasattr(self, "cf_named_token_var") else ""
            cf_url = self.cf_named_url_var.get().strip() if hasattr(self, "cf_named_url_var") else ""
            if cf_tok and not cf_url:
                self.log("⚠ Named Cloudflare Tunnel Token set without a Custom URL — using Quick Tunnel instead.")
                cf_tok = ""
            elif cf_tok and cf_url:
                try:
                    _p = config.load_prefs() or {}
                    _p["mobile_cf_tunnel_token"] = cf_tok
                    _p["mobile_cf_custom_url"] = cf_url
                    config.save_prefs(_p)
                except Exception:
                    pass
            self.tunnel = CloudflareTunnel(
                self.server.port,
                tunnel_token=cf_tok or None,
                custom_public_url=cf_url or None,
            )
        else:
            self.tunnel = PinggyTunnel(self.server.port)
        self.tunnel.start(self._on_tunnel_ready, self._on_tunnel_status)

    def _reconnect_tunnel(self):
        """Restart the active public tunnel to obtain a fresh, verified URL."""
        if not self.server:
            return
        provider = getattr(self, "provider_choice", tk.StringVar(value="cloudflare")).get()
        self.network_choice.set("public")
        self.log("🔄 Reconnecting public tunnel…")
        self._launch_tunnel(provider)

    def _switch_active_provider(self):
        """Toggle between Cloudflare and Pinggy/SSH on the fly without ending the session."""
        if not self.server:
            return
        curr = getattr(self, "provider_choice", tk.StringVar(value="cloudflare")).get()
        nxt = "pinggy" if curr == "cloudflare" else "cloudflare"
        self.network_choice.set("public")
        self.log(f"⇄ Switching tunnel provider to {nxt.title()}…")
        self._launch_tunnel(nxt)

    def _open_diagnostics_dialog(self):
        """Open a built-in 5-step Connection Diagnostics & Troubleshooting dialog."""
        if not self._is_alive():
            return
        import utils

        dlg = tk.Toplevel(self.root)
        dlg.title("Arbor Mobile Companion — Connection Diagnostics")
        dlg.transient(self.root)
        dlg.resizable(True, True)
        dlg.minsize(sc(560), sc(500))
        dlg.configure(bg="#f7f5f0")

        outer = tk.Frame(dlg, bg="#f7f5f0", padx=sc(16), pady=sc(14))
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="🩺 Mobile Connection Diagnostics",
            font=("Lora", sc(13), "bold"),
            bg="#f7f5f0",
            fg="#1b4332",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            outer,
            text="Tests your local Arbor server, Wi-Fi interface, outbound internet, tunnel process, and public URL end-to-end.",
            font=("Inter", sc(9)),
            bg="#f7f5f0",
            fg="#5a655e",
            anchor="w",
            justify="left",
            wraplength=sc(540),
        ).pack(fill="x", pady=(sc(2), sc(10)))

        # Results card
        res_card = tk.Frame(
            outer, bg="#ffffff", highlightbackground="#c4c7c7", highlightthickness=1,
            padx=sc(12), pady=sc(10),
        )
        res_card.pack(fill="x", pady=(0, sc(10)))

        # Tunnel logs card
        log_card = tk.Frame(
            outer, bg="#ffffff", highlightbackground="#c4c7c7", highlightthickness=1,
            padx=sc(10), pady=sc(8),
        )
        log_card.pack(fill="both", expand=True, pady=(0, sc(10)))
        tk.Label(
            log_card, text="Recent Tunnel Output", font=("Inter", sc(9), "bold"),
            bg="#ffffff", fg="#1b4332", anchor="w",
        ).pack(fill="x", pady=(0, sc(4)))
        log_text = tk.Text(
            log_card, height=6, font=("Consolas", sc(8)),
            bg="#f2f5f1", fg="#2c302e", bd=0, wrap="word",
        )
        log_text.pack(fill="both", expand=True)
        log_text.config(state="disabled")

        # Future-proof campus firewall playbook
        guide_card = tk.Frame(
            outer, bg="#fffbeb", highlightbackground="#d97706", highlightthickness=1,
            padx=sc(10), pady=sc(8),
        )
        guide_card.pack(fill="x", pady=(0, sc(10)))
        tk.Label(
            guide_card,
            text=(
                "Can't reach the site on campus / corporate Wi-Fi?\n"
                "• Click '⇄ Switch Provider' to swap between Cloudflare (HTTP/2) and Pinggy / SSH if one is filtered.\n"
                "• Click '🔄 Reconnect' to generate a fresh link if your phone/PC cached a DNS error.\n"
                "• Firewall-proof fallback: Turn on your phone's Mobile Hotspot, connect your laptop to it, and use '📶 Local Wi-Fi' (LAN) mode — works even if campus IT blocks all tunnels."
            ),
            font=("Inter", sc(8.5)),
            bg="#fffbeb",
            fg="#78350f",
            anchor="w",
            justify="left",
            wraplength=sc(540),
        ).pack(fill="x")

        latest_report = [""]

        def _render_results(results):
            if not dlg.winfo_exists():
                return
            for w in res_card.winfo_children():
                w.destroy()
            icons = {"pass": ("✅", "#1b5e20"), "warn": ("⚠️", "#b45309"), "fail": ("❌", "#ba1a1a")}
            for item in results:
                ico, col = icons.get(item["status"], ("•", "#2c302e"))
                row = tk.Frame(res_card, bg="#ffffff")
                row.pack(fill="x", pady=sc(2))
                tk.Label(
                    row, text=f"{ico} {item['step']}:", font=("Inter", sc(9), "bold"),
                    bg="#ffffff", fg=col, anchor="w",
                ).pack(anchor="w")
                tk.Label(
                    row, text=item["detail"], font=("Consolas", sc(8)),
                    bg="#ffffff", fg="#2c302e", anchor="w", justify="left", wraplength=sc(520),
                ).pack(anchor="w", padx=(sc(18), 0))
                if item.get("advice"):
                    tk.Label(
                        row, text=f"→ {item['advice']}", font=("Inter", sc(8.5), "italic"),
                        bg="#ffffff", fg="#5a655e", anchor="w", justify="left", wraplength=sc(520),
                    ).pack(anchor="w", padx=(sc(18), 0))

            logs = list(getattr(self.tunnel, "recent_logs", [])) if self.tunnel else []
            log_text.config(state="normal")
            log_text.delete("1.0", tk.END)
            log_text.insert("1.0", "\n".join(logs[-20:]) if logs else "(No tunnel log output captured yet.)")
            log_text.config(state="disabled")

            latest_report[0] = format_diagnostic_report(
                results, server=self.server, tunnel=self.tunnel, local_ip=get_local_ip()
            )

        def _run_checks():
            if not dlg.winfo_exists():
                return
            for w in res_card.winfo_children():
                w.destroy()
            tk.Label(
                res_card, text="⏳ Running 5-step connection checks…",
                font=("Inter", sc(9), "italic"), bg="#ffffff", fg="#5a655e",
            ).pack(anchor="w")

            sel_ip = self._get_selected_local_ip()

            def _worker(_ip=sel_ip):
                res = run_connection_diagnostics(
                    server=self.server, tunnel=self.tunnel, local_ip=_ip
                )
                self._post_ui(lambda: dlg.winfo_exists() and _render_results(res))

            threading.Thread(target=_worker, daemon=True).start()

        def _copy_report():
            if latest_report[0]:
                try:
                    dlg.clipboard_clear()
                    dlg.clipboard_append(latest_report[0])
                    btn_copy.config(text="✓ Copied (Redacted)!")
                    dlg.after(2000, lambda: dlg.winfo_exists() and btn_copy.config(text="📋 Copy Diagnostic Report"))
                except Exception:
                    pass

        # Footer action buttons
        btn_bar = tk.Frame(outer, bg="#f7f5f0")
        btn_bar.pack(fill="x")

        tk.Button(
            btn_bar, text="🔄 Re-run Checks", font=("Inter", sc(8.5), "bold"),
            bg="#1b4332", fg="#ffffff", relief="flat", padx=sc(10), pady=sc(4),
            cursor="hand2", command=_run_checks,
        ).pack(side="left", padx=(0, sc(6)))

        btn_copy = tk.Button(
            btn_bar, text="📋 Copy Diagnostic Report", font=("Inter", sc(8.5)),
            bg="#ffffff", fg="#1b4332", bd=1, relief="solid", padx=sc(10), pady=sc(4),
            cursor="hand2", command=_copy_report,
        )
        btn_copy.pack(side="left", padx=(0, sc(6)))

        tk.Button(
            btn_bar, text="⇄ Switch Provider", font=("Inter", sc(8.5)),
            bg="#ffffff", fg="#2c302e", bd=1, relief="solid", padx=sc(8), pady=sc(4),
            cursor="hand2", command=lambda: (self._switch_active_provider(), dlg.after(1500, _run_checks)),
        ).pack(side="left", padx=(0, sc(6)))

        tk.Button(
            btn_bar, text="Close", font=("Inter", sc(8.5)),
            bg="#ffffff", fg="#2c302e", bd=1, relief="solid", padx=sc(12), pady=sc(4),
            cursor="hand2", command=dlg.destroy,
        ).pack(side="right")

        dlg.bind("<Escape>", lambda e: dlg.destroy())
        utils.center_and_fit_toplevel(dlg, sc(620), sc(600))
        _run_checks()

    def _is_alive(self):
        """Check if widget hierarchy is still valid and not destroyed."""
        try:
            return (
                hasattr(self, "_main")
                and self._main is not None
                and bool(self._main.winfo_exists())
                and hasattr(self, "client_badge")
                and self.client_badge is not None
                and bool(self.client_badge.winfo_exists())
            )
        except Exception:
            return False


    def stop(self):
        """Stop the tunnel (does not save data — wrapper handles that)."""
        if self.server:
            try:
                self.server.broadcast_event('session_ended', {})
            except Exception:
                pass
            if getattr(self.server, 'on_client_connect_callback', None) == self._on_client_connect:
                self.server.on_client_connect_callback = None
            if getattr(self.server, 'on_presence_callback', None) == self._on_client_presence:
                self.server.on_presence_callback = None
            if getattr(self.server, 'on_edit_callback', None) == self._on_mobile_edit:
                self.server.on_edit_callback = None

        if self.tunnel:
            self.tunnel.stop()
            self.tunnel = None
        self.connection_state = MobileConnectionState.STOPPED

    def _copy_pairing_url(self):
        url = self.url_var.get().strip()
        if url and self.connection_state in (
            MobileConnectionState.LOCAL_READY,
            MobileConnectionState.TUNNEL_READY,
        ):
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                self.btn_copy_url.config(text="✓ Copied!", bg="#e8f5e9")
                self.root.after(2000, lambda: self._is_alive() and self.btn_copy_url.config(text="📋 Copy", bg="#e0e3df"))
            except Exception:
                pass

    def _on_client_presence(self, oid):
        def _update():
            if not self._is_alive():
                return
            self.log(f"📱 Phone inspecting Specimen #{oid}")
        self._post_ui(_update)

    def log(self, message: str):
        """Append a timestamped line to the activity feed."""
        def _append():
            if not self._is_alive():
                return
            try:
                ts = datetime.now().strftime("%H:%M:%S")
                self.feed_list.insert(tk.END, f"[{ts}] {message}")
                self.feed_list.see(tk.END)
            except Exception:
                pass
        self._post_ui(_append)

    # ------------------------------------------------------------------
    # Internal callbacks
    # ------------------------------------------------------------------

    def _render_qr(self, url_to_encode):
        """Generate and display a QR code for the given URL."""
        if not self._is_alive():
            return
        try:
            qr = qrcode.QRCode(box_size=4, border=4)
            qr.add_data(url_to_encode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            self.qr_image_ref = ImageTk.PhotoImage(img)
            self.qr_label.config(image=self.qr_image_ref, text="")
        except Exception:
            try:
                self.qr_label.config(text=f"Scan URL:\n{url_to_encode[:25]}...")
            except Exception:
                pass

    def _switch_setup_mode(self, mode):
        if not self._is_alive():
            return
        self.network_choice.set(mode)
        try:
            if mode == "local":
                self.btn_net_local.config(
                    bg="#1b4332", fg="white", font=("Segoe UI", sc(9), "bold"))
                self.btn_net_public.config(
                    bg="#e0e3df", fg="#333", font=("Segoe UI", sc(9)))
                self.provider_frame.pack_forget()
            else:
                self.btn_net_public.config(
                    bg="#1b4332", fg="white", font=("Segoe UI", sc(9), "bold"))
                self.btn_net_local.config(
                    bg="#e0e3df", fg="#333", font=("Segoe UI", sc(9)))
                self.provider_frame.pack(fill="x")
            self._update_pin_ui()
        except Exception:
            pass

    def _switch_provider(self, mode):
        if not self._is_alive():
            return
        self.provider_choice.set(mode)
        try:
            if mode == "cloudflare":
                self.btn_prov_cf.config(
                    bg="#1b4332", fg="white", font=("Segoe UI", sc(9), "bold"))
                self.btn_prov_pinggy.config(
                    bg="#e0e3df", fg="#333", font=("Segoe UI", sc(9)))
            else:
                self.btn_prov_pinggy.config(
                    bg="#1b4332", fg="white", font=("Segoe UI", sc(9), "bold"))
                self.btn_prov_cf.config(
                    bg="#e0e3df", fg="#333", font=("Segoe UI", sc(9)))
        except Exception:
            pass

    def _switch_ui_version(self, version):
        if not self._is_alive():
            return
        self.ui_version_choice.set(version)
        try:
            # Update Setup buttons if present
            if hasattr(self, 'btn_ver_v2') and hasattr(self, 'btn_ver_v1'):
                if version == "v2":
                    self.btn_ver_v2.config(
                        bg="#1b4332", fg="white", font=("Segoe UI", sc(9), "bold"))
                    self.btn_ver_v1.config(
                        bg="#e0e3df", fg="#333", font=("Segoe UI", sc(9)))
                else:
                    self.btn_ver_v1.config(
                        bg="#1b4332", fg="white", font=("Segoe UI", sc(9), "bold"))
                    self.btn_ver_v2.config(
                        bg="#e0e3df", fg="#333", font=("Segoe UI", sc(9)))

            # Update Active screen buttons if present
            if hasattr(self, 'btn_active_ver_v2') and hasattr(self, 'btn_active_ver_v1'):
                if version == "v2":
                    self.btn_active_ver_v2.config(
                        bg="#1b4332", fg="white", font=("Segoe UI", sc(7), "bold"))
                    self.btn_active_ver_v1.config(
                        bg="#e0e3df", fg="#333", font=("Segoe UI", sc(7)))
                else:
                    self.btn_active_ver_v1.config(
                        bg="#1b4332", fg="white", font=("Segoe UI", sc(7), "bold"))
                    self.btn_active_ver_v2.config(
                        bg="#e0e3df", fg="#333", font=("Segoe UI", sc(7)))

            if self.server:
                local_ip = self._get_selected_local_ip()
                v_path = "/v2" if version == "v2" else "/"
                self.local_url_with_token = (
                    f"http://{local_ip}:{self.server.port}{v_path}?token={self.server.session_token}"
                )
                if self.tunnel and getattr(self.tunnel, 'public_url', None):
                    clean_url = self.tunnel.public_url.rstrip("/")
                    self.public_url_with_token = f"{clean_url}{v_path}?token={self.server.session_token}"

                self.switch_qr(self.current_qr_mode)
                self.log(f"Switched mobile interface to {version.upper()} ({'V2 Tabbed' if version == 'v2' else 'V1 Classic'})")
        except Exception:
            pass

    def switch_qr(self, mode):
        """Toggle the QR code between local and public URL."""
        if not self._is_alive():
            return
        self.current_qr_mode = mode
        try:
            if mode == "local":
                self.btn_qr_local.config(
                    bg="#1b4332", fg="white", font=("Segoe UI", sc(7), "bold"))
                self.btn_qr_public.config(
                    bg="#e0e3df", fg="#333", font=("Segoe UI", sc(7)))
                self.url_var.set(self.local_url_with_token)
                self._render_qr(self.local_url_with_token)
            else:
                self.btn_qr_public.config(
                    bg="#1b4332", fg="white", font=("Segoe UI", sc(7), "bold"))
                self.btn_qr_local.config(
                    bg="#e0e3df", fg="#333", font=("Segoe UI", sc(7)))
                url = self.public_url_with_token or self.local_url_with_token
                self.url_var.set(url)
                self._render_qr(url)
        except Exception:
            pass

    def _on_tunnel_status(self, status):
        def _update():
            if not self._is_alive():
                return
            try:
                if status.startswith("🔄"):
                    self.connection_state = MobileConnectionState.TUNNEL_CONNECTING
                    self.status_lbl.config(text=status, fg="#d97706")
                    self.status_dot.config(fg="#d97706")
                    self.tunnel_lbl.config(text=f"Tunnel: {status.lstrip('🔄 ').strip()}", fg="#d97706")
                elif status.startswith("🔴") or status.startswith("🟡"):
                    self.connection_state = MobileConnectionState.ERROR
                    self.public_url_with_token = ""
                    color = "#ba1a1a" if status.startswith("🔴") else "#d95c14"
                    self.status_lbl.config(text=status, fg=color)
                    self.status_dot.config(fg=color)
                    self.tunnel_lbl.config(text="Tunnel: Disconnected — click Reconnect or Test Connection", fg=color)
                    self.btn_qr_public.config(text="🌐 Public (Internet)")
                else:
                    self.status_lbl.config(text=status, fg="#5a655e")
                self.feed_list.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
                self.feed_list.see(tk.END)
            except Exception:
                pass
        self._post_ui(_update)

    def _on_tunnel_ready(self, url):
        def _update():
            if not self._is_alive():
                return
            try:
                self.connection_state = MobileConnectionState.TUNNEL_READY
                ver = self.ui_version_choice.get()
                v_path = "/v2" if ver == "v2" else "/"
                clean_url = url.rstrip("/")
                self.public_url_with_token = f"{clean_url}{v_path}?token={self.server.session_token}"
                self.status_dot.config(fg="#2e7d32")
                self.status_lbl.config(
                    text="🟢 Public Tunnel Live & Secure", fg="#1b4332")
                self.tunnel_lbl.config(
                    text=f"Public: {url}", fg="#2e7d32", font=("Segoe UI", sc(8)))
                self.btn_qr_public.config(text="🌐 Public (Internet) ✓")
                # Always switch to the public QR as soon as the tunnel is ready
                self.switch_qr("public")
                self.feed_list.insert(
                    tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Public tunnel ready: {url}")
                self.feed_list.see(tk.END)
            except Exception:
                pass
        self._post_ui(_update)

    def _on_client_connect(self, active_count):
        def _update():
            if not self._is_alive():
                return
            try:
                if active_count > 0:
                    self.client_badge.config(
                        text=f"📱 Phone Connected ({active_count} Online)",
                        fg="#2e7d32",
                        font=("Segoe UI", sc(9), "bold"),
                    )
                else:
                    self.client_badge.config(
                        text="📱 Offline", fg="#5a655e", font=("Segoe UI", sc(9))
                    )
            except Exception:
                pass
        self._post_ui(_update)

    def _on_mobile_edit(self, oid, summary):
        # Log to feed
        self.log(summary)
        # Notify the wrapper (e.g. desktop UI sync)
        if self.on_edit:
            try:
                self.on_edit(oid, summary)
            except Exception:
                pass

    def _on_end_btn(self):
        """Stop tunnel, then hand off to the wrapper's on_end_session."""
        self.stop()
        if self.on_end_session:
            try:
                self.on_end_session()
            except Exception:
                pass
