import os
import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime
import qrcode
from PIL import ImageTk
import config
from config import sc

from backend.mobile_server import MobileServer, get_local_ip
from backend.tunnel import PinggyTunnel, CloudflareTunnel


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
        self.qr_image_ref = None
        self.local_url_with_token = ""
        self.public_url_with_token = ""
        self.current_qr_mode = "public"  # public tunnel is the default
        self.ui_version_choice = tk.StringVar(value="v2")
        prefs = config.load_prefs() if hasattr(config, "load_prefs") else {}
        self.auto_save_var = tk.BooleanVar(value=bool(prefs.get("mobile_autosave_on_stop", False)))
        self.require_pin_var = tk.BooleanVar(value=bool(prefs.get("require_mobile_pin", True)))
        self.show_walkthrough_var = tk.BooleanVar(value=bool(prefs.get("mobile_show_walkthrough", True)))

        self._build_ui()

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

        # ── Header ────────────────────────────────────────────────────
        hdr = tk.Frame(main, bg=self._bg_main)
        hdr.pack(fill="x", pady=(0, 10))

        hdr_top = tk.Frame(hdr, bg=self._bg_main)
        hdr_top.pack(fill="x")

        tk.Label(
            hdr_top,
            text="📱 Arbor Mobile Companion",
            font=("Lora", sc(15), "bold"),
            bg=self._bg_main,
            fg=self._fg_title,
        ).pack(side="left", anchor="w")

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

        # First-time phone tutorial toggle (ON by default)
        self.walkthrough_row = tk.Frame(setup_card, bg="#fbfbf9")
        self.walkthrough_row.pack(fill="x", pady=(10, 0))
        self.cb_mobile_walkthrough = tk.Checkbutton(
            self.walkthrough_row,
            text="Launch with mobile companion tutorial for first-time users",
            variable=self.show_walkthrough_var,
            command=self._on_walkthrough_toggle,
            font=("Inter", sc(9)),
            bg="#fbfbf9",
            fg="#1b4332",
            activebackground="#fbfbf9",
            activeforeground="#1b4332",
            selectcolor="#ffffff",
            anchor="w",
            cursor="hand2",
        )
        self.cb_mobile_walkthrough.pack(fill="x")

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

    def _on_walkthrough_toggle(self):
        enabled = bool(self.show_walkthrough_var.get())
        try:
            prefs = config.load_prefs() or {}
            prefs["mobile_show_walkthrough"] = enabled
            config.save_prefs(prefs)
        except Exception:
            pass
        if self.server and hasattr(self.server, "update_walkthrough_setting"):
            try:
                self.server.update_walkthrough_setting(enabled)
            except Exception:
                pass

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

    def _start_services(self):
        """Start (or reuse) MobileServer and conditionally launch tunnel."""
        # Start or reuse MobileServer
        if self.server is None:
            self.server = MobileServer(
                self.app_state,
                root_tk=self.root,
                port=self.port,
                on_edit_callback=self._on_mobile_edit,
            )
            self.server.start()
        else:
            self.server.app_state = self.app_state
            self.server.root_tk = self.root
            self.server.on_edit_callback = self._on_mobile_edit

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
        if hasattr(self.server, "update_walkthrough_setting"):
            self.server.update_walkthrough_setting(self.show_walkthrough_var.get())
        self.pin_var.set(self.server.pin)
        self._update_pin_ui()
        local_ip = get_local_ip()
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
            # Render LAN fallback QR immediately so user can scan right away while public tunnel warms up
            self.current_qr_mode = "public"
            self.url_var.set("🔄 Connecting public tunnel…")
            self._render_qr(self.local_url_with_token)
            self.status_lbl.config(text="🔄 Warming up public tunnel… (LAN QR active)", fg="#d97706")
            self.tunnel_lbl.config(text="Tunnel: Establishing secure public tunnel...", fg="#d97706")
            self.log(f"Local LAN ready: http://{local_ip}:{self.server.port}")
            self.log("Establishing secure public tunnel in background...")

            # Start tunnel in background based on provider choice
            if getattr(self, 'provider_choice', tk.StringVar(value='cloudflare')).get() == 'cloudflare':
                self.tunnel = CloudflareTunnel(self.server.port)
            else:
                self.tunnel = PinggyTunnel(self.server.port)

            self.tunnel.start(self._on_tunnel_ready, self._on_tunnel_status)
        else:
            # Local only mode
            self.tunnel_lbl.config(
                text="Tunnel: Disabled (LAN Only)", fg="#5a655e")
            self.status_lbl.config(text="🟢 Local Server Ready", fg="#1b4332")
            self.switch_qr("local")
            self.log(
                f"Server started in LAN-only mode: http://{local_ip}:{self.server.port}")

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

    def _copy_pairing_url(self):
        url = self.url_var.get().strip()
        if url and not url.startswith("🔄") and not url.startswith("Init"):
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
        try:
            if self._is_alive():
                self.root.after(0, _update)
        except Exception:
            pass

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
        try:
            if self._is_alive():
                self.root.after(0, _append)
        except Exception:
            pass

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
                local_ip = get_local_ip()
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
                self.status_lbl.config(text=status, fg="#d95c14")
                self.status_dot.config(fg="#d95c14")
                self.tunnel_lbl.config(text="Tunnel: Disconnected", fg="#d95c14")
                self.feed_list.insert(tk.END, status)
                self.feed_list.see(tk.END)
            except Exception:
                pass
        try:
            if self._is_alive():
                self.root.after(0, _update)
        except Exception:
            pass

    def _on_tunnel_ready(self, url):
        def _update():
            if not self._is_alive():
                return
            try:
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
        try:
            if self._is_alive():
                self.root.after(0, _update)
        except Exception:
            pass

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
        try:
            if self._is_alive():
                self.root.after(0, _update)
        except Exception:
            pass

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
