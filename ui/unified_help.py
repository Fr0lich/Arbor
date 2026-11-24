"""
ui/unified_help.py - Unified Help Center for Arbor

Formatted identically to UnifiedSettingsWindow (vertical sidebar navigation,
card-based scrollable content area, clean header and footer). Lets trainees
read about each interactive tutorial, quick guide, manual, and keyboard shortcut
before starting or opening it. Persists Learning Path completion progress in
user_prefs.json via sandbox_manager.
"""

import tkinter as tk
from tkinter import ttk
import config
from config import sc
from ui.scroll_helper import bind_mousewheel
from ui.tutorials.sandbox_manager import (
    get_completed_tutorials,
    reset_completed_tutorials,
)


class UnifiedHelpWindow:
    """
    Unified Help Center dialog matching UnifiedSettingsWindow's design system:
    - Vertical left sidebar with active green accent
    - Scrollable card-based content area
    - Read-before-starting cards for all 5 Suggested Learning Path tutorials
    - Quick Guides (30s), User Manuals, Keyboard Shortcuts, and About & Updates
    """

    _active_instance = None

    COLORS = {
        "surface": "#fbfaf8",
        "surface_container_low": "#f2f5f1",
        "surface_container_highest": "#e9ece5",
        "card_bg": "#ffffff",
        "on_surface": "#2c302e",
        "on_surface_variant": "#5f6862",
        "outline": "#757d77",
        "outline_variant": "#c4c7c7",
        "primary": "#2c302e",
        "on_primary": "#ffffff",
        "secondary": "#3a7d44",
        "secondary_light": "#eaf5ec",
        "secondary_dark": "#1b5e20",
        "sidebar_bg": "#f3f3f3",
        "sidebar_active": "#ffffff",
        "badge_neutral_bg": "#eef1ee",
        "badge_neutral_fg": "#444c47",
        "badge_phone_bg": "#e6f0f6",
        "badge_phone_fg": "#1e4b66",
        "keycap_bg": "#eef2ee",
        "keycap_border": "#b5c2b7",
    }

    LEARNING_PATH_IDS = ("review", "mobile", "discrepancy", "triage", "database")

    def __init__(self, parent, app_ref=None, initial_tab="tutorials"):
        # Reuse existing open Help Center if already open
        prev = UnifiedHelpWindow._active_instance
        if prev is not None and getattr(prev, "win", None) is not None:
            try:
                if prev.win.winfo_exists():
                    prev.show_tab(initial_tab if initial_tab in prev.tabs else "tutorials")
                    prev.win.lift()
                    prev.win.focus_force()
                    self.win = prev.win
                    self.tabs = prev.tabs
                    return
            except Exception:
                pass

        self.parent = parent
        self.app = app_ref

        self.FONT_HEADLINE = ("Lora", sc(14), "bold")
        self.FONT_SUBTITLE = ("Inter", sc(9))
        self.FONT_TAB = ("Inter", sc(10), "bold")
        self.FONT_CARD_TITLE = ("Inter", sc(10.5), "bold")
        self.FONT_LABEL = ("Inter", sc(9.5), "bold")
        self.FONT_BODY = ("Inter", sc(9.5))
        self.FONT_SMALL = ("Inter", sc(8.5))
        self.FONT_MONO = ("JetBrains Mono", sc(8.5), "bold")

        self.win = tk.Toplevel(parent)
        self.win.title("Arbor Help Center")
        self.win.resizable(True, True)
        self.win.transient(parent)

        import utils
        utils.center_and_fit_toplevel(self.win, sc(840), sc(620))

        self.win.bind("<Escape>", lambda e: self.win.destroy())
        self.win.bind("<Destroy>", self._on_destroy)
        UnifiedHelpWindow._active_instance = self

        self.main_container = tk.Frame(self.win, bg=self.COLORS["surface"])
        self.main_container.pack(fill="both", expand=True)

        # 1. Header
        self._build_header()

        # 2. Body (Sidebar + Content)
        self.body_frame = tk.Frame(self.main_container, bg=self.COLORS["surface"])
        self.body_frame.pack(fill="both", expand=True)

        self.sidebar_frame = tk.Frame(self.body_frame, bg=self.COLORS["sidebar_bg"], width=sc(195))
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        tk.Frame(self.sidebar_frame, bg=self.COLORS["outline_variant"], width=1).pack(side="right", fill="y")

        self.content_frame = tk.Frame(self.body_frame, bg=self.COLORS["surface"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # 3. Footer
        self._build_footer()

        self.tabs = {}
        self.tab_buttons = {}
        self.active_tab = None

        self._build_sidebar_nav()
        self._build_all_tabs()

        self.show_tab(initial_tab if initial_tab in self.tabs else "tutorials")

    def _on_destroy(self, event):
        if event.widget is self.win and UnifiedHelpWindow._active_instance is self:
            UnifiedHelpWindow._active_instance = None

    # ------------------------------------------------------------------
    # Header & Footer (mirrors UnifiedSettingsWindow)
    # ------------------------------------------------------------------

    def _build_header(self):
        header = tk.Frame(self.main_container, bg=self.COLORS["surface_container_low"], height=sc(54))
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Frame(header, bg=self.COLORS["outline_variant"], height=1).pack(fill="x", side="bottom")

        left = tk.Frame(header, bg=self.COLORS["surface_container_low"])
        left.pack(side="left", fill="y", padx=sc(16))

        tk.Label(
            left, text="Arbor Help Center", font=self.FONT_HEADLINE,
            fg=self.COLORS["primary"], bg=self.COLORS["surface_container_low"],
        ).pack(side="top", pady=(sc(6), 0), anchor="w")

        tk.Label(
            left, text="Read about each interactive tutorial before starting, or browse quick guides, manuals, and shortcuts",
            font=self.FONT_SUBTITLE, fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["surface_container_low"],
        ).pack(side="top", anchor="w")

    def _build_footer(self):
        footer = tk.Frame(self.main_container, bg=self.COLORS["surface_container_low"], height=sc(50))
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Frame(footer, bg=self.COLORS["outline_variant"], height=1).pack(fill="x", side="top")

        left = tk.Frame(footer, bg=self.COLORS["surface_container_low"])
        left.pack(side="left", fill="y", padx=sc(16))
        self.progress_footer_lbl = tk.Label(
            left, text="", font=self.FONT_MONO,
            fg=self.COLORS["secondary_dark"], bg=self.COLORS["surface_container_low"],
        )
        self.progress_footer_lbl.pack(side="left", pady=sc(12))
        self._refresh_progress_footer()

        right = tk.Frame(footer, bg=self.COLORS["surface_container_low"])
        right.pack(side="right", fill="y", padx=sc(16))
        tk.Button(
            right, text="Close", font=self.FONT_LABEL,
            fg=self.COLORS["on_surface"], bg=self.COLORS["card_bg"], bd=1,
            relief="solid", padx=sc(16), pady=sc(4), cursor="hand2",
            command=self.win.destroy,
        ).pack(side="right", pady=sc(9))

    def _refresh_progress_footer(self):
        done = get_completed_tutorials()
        count = sum(1 for tid in self.LEARNING_PATH_IDS if tid in done)
        if hasattr(self, "progress_footer_lbl") and self.progress_footer_lbl.winfo_exists():
            self.progress_footer_lbl.config(
                text=f"LEARNING PATH: {count} OF {len(self.LEARNING_PATH_IDS)} COMPLETED"
            )

    # ------------------------------------------------------------------
    # Sidebar Navigation
    # ------------------------------------------------------------------

    def _build_sidebar_nav(self):
        nav_items = [
            ("tutorials", "Interactive Tutorials"),
            ("quick_guides", "Quick Guides (30s)"),
            ("manuals", "User Manuals"),
            ("shortcuts", "Keyboard Shortcuts"),
            ("about", "About & Updates"),
        ]
        nav_wrap = tk.Frame(self.sidebar_frame, bg=self.COLORS["sidebar_bg"], pady=sc(10))
        nav_wrap.pack(fill="both", expand=True)

        for tab_id, label in nav_items:
            row = tk.Frame(nav_wrap, bg=self.COLORS["sidebar_bg"])
            row.pack(fill="x", pady=sc(2))

            accent = tk.Frame(row, bg=self.COLORS["sidebar_bg"], width=sc(4))
            accent.pack(side="left", fill="y")

            btn = tk.Button(
                row,
                text=label,
                font=self.FONT_TAB,
                fg=self.COLORS["on_surface"],
                bg=self.COLORS["sidebar_bg"],
                activebackground=self.COLORS["surface_container_highest"],
                activeforeground=self.COLORS["primary"],
                relief="flat",
                bd=0,
                anchor="w",
                padx=sc(14),
                pady=sc(10),
                cursor="hand2",
                command=lambda tid=tab_id: self.show_tab(tid),
            )
            btn.pack(side="left", fill="x", expand=True)
            self.tab_buttons[tab_id] = (row, accent, btn)

    def show_tab(self, tab_id):
        if tab_id not in self.tabs:
            return
        self.active_tab = tab_id
        for tid, frame in self.tabs.items():
            if tid == tab_id:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

        for tid, (row, accent, btn) in self.tab_buttons.items():
            if tid == tab_id:
                row.config(bg=self.COLORS["sidebar_active"])
                accent.config(bg=self.COLORS["secondary"])
                btn.config(bg=self.COLORS["sidebar_active"], fg=self.COLORS["secondary_dark"])
            else:
                row.config(bg=self.COLORS["sidebar_bg"])
                accent.config(bg=self.COLORS["sidebar_bg"])
                btn.config(bg=self.COLORS["sidebar_bg"], fg=self.COLORS["on_surface"])

    # ------------------------------------------------------------------
    # Scrollable Tab Container & Card Helpers
    # ------------------------------------------------------------------

    def _create_scrollable_tab(self, tab_id):
        outer = tk.Frame(self.content_frame, bg=self.COLORS["surface"])
        canvas = tk.Canvas(outer, bg=self.COLORS["surface"], highlightthickness=0, bd=0)
        sb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=sb.set)

        inner = tk.Frame(canvas, bg=self.COLORS["surface"], padx=sc(20), pady=sc(16))
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        bind_mousewheel(canvas, inner)

        self.tabs[tab_id] = outer
        return inner

    def _add_section_intro(self, parent, title, subtitle):
        tk.Label(
            parent, text=title, font=("Lora", sc(13), "bold"),
            fg=self.COLORS["primary"], bg=self.COLORS["surface"], anchor="w",
        ).pack(fill="x")
        tk.Label(
            parent, text=subtitle, font=self.FONT_SUBTITLE,
            fg=self.COLORS["on_surface_variant"], bg=self.COLORS["surface"],
            anchor="w", justify="left", wraplength=sc(560),
        ).pack(fill="x", pady=(sc(2), sc(12)))

    def _make_card(self, parent):
        card = tk.Frame(
            parent,
            bg=self.COLORS["card_bg"],
            highlightbackground=self.COLORS["outline_variant"],
            highlightthickness=1,
            padx=sc(14),
            pady=sc(12),
        )
        card.pack(fill="x", pady=(0, sc(10)))
        return card

    def _add_pill(self, parent, text, bg, fg):
        tk.Label(
            parent, text=f" {text} ", font=self.FONT_MONO,
            bg=bg, fg=fg, padx=sc(4), pady=sc(1),
        ).pack(side="left", padx=(0, sc(6)))

    def _launch_and_close(self, fn):
        try:
            self.win.destroy()
        except Exception:
            pass
        if callable(fn):
            fn()

    # ------------------------------------------------------------------
    # Build All 5 Tabs
    # ------------------------------------------------------------------

    def _build_all_tabs(self):
        self._build_tutorials_tab()
        self._build_quick_guides_tab()
        self._build_manuals_tab()
        self._build_shortcuts_tab()
        self._build_about_tab()

    def _build_tutorials_tab(self):
        # Clear previous content if refreshing after Reset Tutorial Progress
        if "tutorials" in self.tabs:
            try:
                self.tabs["tutorials"].destroy()
            except Exception:
                pass
        inner = self._create_scrollable_tab("tutorials")
        self._add_section_intro(
            inner,
            "Interactive Tutorials — Suggested Learning Path",
            "Read what each walkthrough covers before you begin. Practice Mode tutorials run on safe sample data and never touch your real museum files. Your progress is saved automatically between sessions.",
        )

        done = get_completed_tutorials()

        def _start_flow(key):
            if self.app and hasattr(self.app, "start_tutorial_flow"):
                self._launch_and_close(lambda: self.app.start_tutorial_flow(key))

        def _start_mobile():
            from ui.tutorials import start_armed_shelf_guide
            if self.app:
                self._launch_and_close(lambda: start_armed_shelf_guide(self.app))

        tutorials = [
            (
                "review",
                "Step 1",
                "3-Minute Quick Tour",
                "~3 min",
                "Practice Mode",
                True,
                (
                    "Start here if you are new to Arbor Desktop.\n"
                    "• Inspect Object #110 and #198 using real specimen photos\n"
                    "• Fill in a missing Collection Date and mark an object Reviewed (green [REV])\n"
                    "• Compare conflicting older records in Problem Resolution, flag physical damage, and see amber [REV+ERR]"
                ),
                lambda: _start_flow("review"),
            ),
            (
                "mobile",
                "Step 2 · Recommended Next",
                "Mobile Companion Hallway Guide",
                "~2 min",
                "Uses Your Phone",
                False,
                (
                    "Walk the collection aisles with your phone without carrying a laptop.\n"
                    "• Pair your phone with a QR code (works offline in concrete basement vaults)\n"
                    "• Record Physical Locations for whole shelves in 1 tap (Set Shelf + 5-sec Undo)\n"
                    "• Check older plant names (Old names), flag issues right on Details, mark Reviewed, and save on Desktop"
                ),
                _start_mobile,
            ),
            (
                "triage",
                "Step 3",
                "Office Triage (REV+ERR)",
                "~2 min",
                "Practice Mode",
                True,
                (
                    "The desk follow-up right after a hallway shift — sort through amber [REV+ERR] objects.\n"
                    "• Filter the Specimen Directory to Hallway Follow-Up (Ctrl+G)\n"
                    "• Step through the Problem Queue, clear false alarms in 1 click, and leave physical damage flagged for a specialist"
                ),
                lambda: _start_flow("triage"),
            ),
            (
                "discrepancy",
                "Step 4",
                "Historical Ledger Comparison",
                "~3 min",
                "Practice Mode",
                True,
                (
                    "Use this at your desk when older museum catalog books disagree across multiple fields.\n"
                    "• Open Problem Resolution (Ctrl+H) and browse disagreeing fields in the sidebar\n"
                    "• Compare two conflicting catalog books carefully and apply confirmed values\n"
                    "• Learn why desk edits leave 'Reviewed' unchecked until physical inspection"
                ),
                lambda: _start_flow("discrepancy"),
            ),
            (
                "database",
                "Step 5 · Optional",
                "Collections & New Specimens",
                "~2 min",
                "Practice Mode",
                True,
                (
                    "Optional — skip if you only work on an existing museum collection file.\n"
                    "• See how to create a new collection Excel file from scratch\n"
                    "• Practice adding a new specimen record (Ctrl+N) and filling in its details and storage location"
                ),
                lambda: _start_flow("database"),
            ),
        ]

        for tid, step_tag, title, duration, mode_lbl, is_sandbox, desc, launch_fn in tutorials:
            card = self._make_card(inner)
            is_done = tid in done

            top = tk.Frame(card, bg=self.COLORS["card_bg"])
            top.pack(fill="x")

            if is_done:
                self._add_pill(top, "✓ COMPLETED", self.COLORS["secondary_light"], self.COLORS["secondary_dark"])
            else:
                self._add_pill(top, step_tag.upper(), self.COLORS["badge_neutral_bg"], self.COLORS["badge_neutral_fg"])

            self._add_pill(top, duration, self.COLORS["badge_neutral_bg"], self.COLORS["badge_neutral_fg"])
            if is_sandbox:
                self._add_pill(top, mode_lbl, self.COLORS["secondary_light"], self.COLORS["secondary_dark"])
            else:
                self._add_pill(top, mode_lbl, self.COLORS["badge_phone_bg"], self.COLORS["badge_phone_fg"])

            tk.Label(
                card, text=title, font=self.FONT_CARD_TITLE,
                fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
            ).pack(fill="x", pady=(sc(6), sc(3)))

            tk.Label(
                card, text=desc, font=self.FONT_BODY,
                fg=self.COLORS["on_surface_variant"], bg=self.COLORS["card_bg"],
                anchor="w", justify="left", wraplength=sc(540),
            ).pack(fill="x", pady=(0, sc(10)))

            btn_row = tk.Frame(card, bg=self.COLORS["card_bg"])
            btn_row.pack(fill="x")
            btn_text = "▶ Replay Tutorial" if is_done else "▶ Start Tutorial"
            tk.Button(
                btn_row,
                text=btn_text,
                font=self.FONT_LABEL,
                bg=self.COLORS["secondary"] if not is_done else self.COLORS["surface_container_low"],
                fg=self.COLORS["on_primary"] if not is_done else self.COLORS["on_surface"],
                activebackground="#4c9a58" if not is_done else self.COLORS["surface_container_highest"],
                activeforeground=self.COLORS["on_primary"] if not is_done else self.COLORS["primary"],
                relief="flat" if not is_done else "solid",
                bd=0 if not is_done else 1,
                padx=sc(14),
                pady=sc(5),
                cursor="hand2",
                command=launch_fn,
            ).pack(side="left")

    def _build_quick_guides_tab(self):
        inner = self._create_scrollable_tab("quick_guides")
        self._add_section_intro(
            inner,
            "Quick Guides (20–30 Seconds)",
            "Short, in-place reminders that run right over your open workspace without entering Practice Mode.",
        )

        def _run_quick(fn_name):
            from ui import tutorials as tut_mod
            fn = getattr(tut_mod, fn_name, None)
            if fn and self.app:
                self._launch_and_close(lambda: fn(self.app))

        guides = [
            (
                "Hallway Follow-Up (REV+ERR) — 30 sec",
                "A 2-step reminder on filtering to amber [REV+ERR] objects with Ctrl+G and stepping through the Problem Queue.",
                lambda: _run_quick("start_hallway_followup_guide"),
            ),
            (
                "Image Zoom, Pan & Rotate — 20 sec",
                "Learn how to zoom with the mousewheel, switch front/back thumbnails, rotate sideways labels (Alt+R), and pop out scans.",
                lambda: _run_quick("start_image_controls_guide"),
            ),
        ]

        for title, desc, fn in guides:
            card = self._make_card(inner)
            tk.Label(
                card, text=title, font=self.FONT_CARD_TITLE,
                fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
            ).pack(fill="x")
            tk.Label(
                card, text=desc, font=self.FONT_BODY,
                fg=self.COLORS["on_surface_variant"], bg=self.COLORS["card_bg"],
                anchor="w", justify="left", wraplength=sc(540),
            ).pack(fill="x", pady=(sc(4), sc(10)))
            tk.Button(
                card, text="▶ Start Quick Guide", font=self.FONT_LABEL,
                bg=self.COLORS["secondary"], fg=self.COLORS["on_primary"],
                relief="flat", bd=0, padx=sc(12), pady=sc(5), cursor="hand2",
                command=fn,
            ).pack(anchor="w")

        # Reference card: How to Open Arbor
        ref_card = self._make_card(inner)
        tk.Label(
            ref_card, text="How to Open Arbor (Startup Files Reference)", font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
        ).pack(fill="x")
        tk.Label(
            ref_card,
            text=(
                "When you double-click Arbor's .exe file, Project Setup asks for up to three things:\n"
                "1. Collection File (REQUIRED): Your museum's main .xlsx Excel file (or pick it from Recent Projects).\n"
                "2. Specimen Photos (RECOMMENDED): Pick a Local Folder of photos, Online, or leave Offline for later.\n"
                "3. Historical Books (OPTIONAL): Older digitized catalog spreadsheets to compare against — leave blank if none.\n"
                "Then click LAUNCH SYSTEM (or Mobile Companion to use your phone)."
            ),
            font=self.FONT_BODY,
            fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["card_bg"],
            anchor="w",
            justify="left",
            wraplength=sc(540),
        ).pack(fill="x", pady=(sc(5), 0))

    def _build_manuals_tab(self):
        inner = self._create_scrollable_tab("manuals")
        self._add_section_intro(
            inner,
            "User Manuals & Troubleshooting",
            "Full searchable guides when you need step-by-step instructions or run into an unexpected problem.",
        )

        from ui.help_dialogs import show_main_help
        host = self.app or self.parent

        manuals = [
            (
                "Desktop Work Manual",
                "Complete trainee handbook covering searching, inspecting photos, reviewing objects, comparing older catalog books, and saving safely.",
                "Open Desktop Manual",
                lambda: self._launch_and_close(lambda: show_main_help(host, initial_tab="desktop")),
            ),
            (
                "Mobile Vault Guide",
                "Step-by-step phone pairing, 1-tap Set Shelf location saving with 5-sec Undo, checking Old Names, and offline basement vault syncing.",
                "Open Mobile Guide",
                lambda: self._launch_and_close(lambda: show_main_help(host, initial_tab="mobile")),
            ),
            (
                "\"Don't Panic!\" Troubleshooting",
                "Quick fixes if you accidentally edited a field, photos aren't loading, Excel says a file is in use, or you need to restore a backup.",
                "Open Troubleshooting",
                lambda: self._launch_and_close(lambda: show_main_help(host, initial_tab="desktop", initial_chapter="dont-panic")),
            ),
        ]

        for title, desc, btn_lbl, fn in manuals:
            card = self._make_card(inner)
            tk.Label(
                card, text=title, font=self.FONT_CARD_TITLE,
                fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
            ).pack(fill="x")
            tk.Label(
                card, text=desc, font=self.FONT_BODY,
                fg=self.COLORS["on_surface_variant"], bg=self.COLORS["card_bg"],
                anchor="w", justify="left", wraplength=sc(540),
            ).pack(fill="x", pady=(sc(4), sc(10)))
            tk.Button(
                card, text=btn_lbl, font=self.FONT_LABEL,
                bg=self.COLORS["surface_container_low"], fg=self.COLORS["on_surface"],
                relief="solid", bd=1, padx=sc(12), pady=sc(5), cursor="hand2",
                command=fn,
            ).pack(anchor="w")

    def _build_shortcuts_tab(self):
        inner = self._create_scrollable_tab("shortcuts")
        self._add_section_intro(
            inner,
            "Keyboard Shortcuts & Quick Codes",
            "Keep your hands on the keyboard while inspecting physical specimens.",
        )

        groups = [
            ("Everyday Curation", [
                ("Ctrl + F", "Focus Search Bar (Specimen Directory)"),
                ("Ctrl + K", "Open Command Palette (search any tool or filter)"),
                ("Ctrl + Enter", "Mark current specimen as Reviewed"),
                ("Ctrl + H", "Open Problem Resolution / Historical Sources"),
                ("Ctrl + G", "Open Filter dialog (e.g. Hallway Follow-Up REV+ERR)"),
                ("Ctrl + L", "Jump straight to Storage Location"),
                ("Ctrl + S", "Save Workbook to disk"),
                ("Ctrl + Z / Y", "Undo / Redo edit"),
            ]),
            ("Photos & Navigation", [
                ("← / →", "Previous / Next specimen"),
                ("Alt + R", "Rotate specimen photo 90°"),
                ("Ctrl + 0", "Reset photo zoom"),
                ("F1", "Open Arbor Help Center"),
            ]),
            ("Missing-Data Quick Codes (ICEDIG)", [
                ("Ctrl + Shift + M", "Insert ?m — Missing on label"),
                ("Ctrl + Shift + I", "Insert ?i — Cannot read / damaged ink"),
                ("Ctrl + Shift + U", "Insert ?u — Skipped for now"),
                ("Ctrl + Shift + W", "Insert ?w — Confidential / protected location"),
            ]),
        ]

        for group_title, rows in groups:
            card = self._make_card(inner)
            tk.Label(
                card, text=group_title, font=self.FONT_CARD_TITLE,
                fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
            ).pack(fill="x", pady=(0, sc(6)))

            for keys, desc in rows:
                r = tk.Frame(card, bg=self.COLORS["card_bg"])
                r.pack(fill="x", pady=sc(2))
                tk.Label(
                    r, text=f" {keys} ", font=self.FONT_MONO,
                    bg=self.COLORS["keycap_bg"], fg=self.COLORS["primary"],
                    highlightbackground=self.COLORS["keycap_border"], highlightthickness=1,
                    width=18, anchor="center", pady=sc(2),
                ).pack(side="left", padx=(0, sc(12)))
                tk.Label(
                    r, text=desc, font=self.FONT_BODY,
                    fg=self.COLORS["on_surface"], bg=self.COLORS["card_bg"], anchor="w",
                ).pack(side="left", fill="x", expand=True)

        # Button to pop out the full Printable Desk Cheat Sheet
        from ui.help_dialogs import show_shortcuts
        host = self.app or self.parent
        tk.Button(
            inner, text="Open Full Shortcuts & Desk Cheat Sheet", font=self.FONT_LABEL,
            bg=self.COLORS["secondary"], fg=self.COLORS["on_primary"],
            relief="flat", bd=0, padx=sc(14), pady=sc(6), cursor="hand2",
            command=lambda: self._launch_and_close(lambda: show_shortcuts(host)),
        ).pack(anchor="w", pady=(sc(4), sc(8)))

    def _build_about_tab(self):
        inner = self._create_scrollable_tab("about")
        self._add_section_intro(
            inner,
            "About Arbor & Updates",
            "Version information, software updates, and tutorial progress controls.",
        )

        # About & Updates card
        card = self._make_card(inner)
        ver = getattr(config, "APP_VERSION", "")
        title_txt = f"Arbor Desktop{' — v' + str(ver) if ver else ''}"
        tk.Label(
            card, text=title_txt, font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
        ).pack(fill="x")
        tk.Label(
            card,
            text="Offline-first museum collection curation suite for reviewing physical specimens, comparing historical catalog books, and auditing shelves with Mobile Companion.",
            font=self.FONT_BODY, fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["card_bg"], anchor="w", justify="left", wraplength=sc(540),
        ).pack(fill="x", pady=(sc(4), sc(10)))

        btn_row = tk.Frame(card, bg=self.COLORS["card_bg"])
        btn_row.pack(fill="x")
        if self.app and hasattr(self.app, "check_for_updates_action"):
            tk.Button(
                btn_row, text="Check for Updates...", font=self.FONT_LABEL,
                bg=self.COLORS["surface_container_low"], fg=self.COLORS["on_surface"],
                relief="solid", bd=1, padx=sc(12), pady=sc(5), cursor="hand2",
                command=lambda: self._launch_and_close(self.app.check_for_updates_action),
            ).pack(side="left", padx=(0, sc(8)))
        if self.app and hasattr(self.app, "show_about"):
            tk.Button(
                btn_row, text="About Arbor", font=self.FONT_LABEL,
                bg=self.COLORS["surface_container_low"], fg=self.COLORS["on_surface"],
                relief="solid", bd=1, padx=sc(12), pady=sc(5), cursor="hand2",
                command=lambda: self._launch_and_close(self.app.show_about),
            ).pack(side="left")

        # Tutorial Progress Reset card
        prog_card = self._make_card(inner)
        tk.Label(
            prog_card, text="Tutorial Progress (Saved Between Sessions)", font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"], bg=self.COLORS["card_bg"], anchor="w",
        ).pack(fill="x")
        tk.Label(
            prog_card,
            text="Arbor remembers which Learning Path tutorials you have finished in your user preferences. Reset checkmarks here when handing this computer to a new trainee.",
            font=self.FONT_BODY, fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["card_bg"], anchor="w", justify="left", wraplength=sc(540),
        ).pack(fill="x", pady=(sc(4), sc(10)))

        def _do_reset():
            reset_completed_tutorials()
            self._build_tutorials_tab()
            self._refresh_progress_footer()
            if self.app and hasattr(self.app, "show_toast"):
                try:
                    self.app.show_toast("Tutorial progress reset.", "info")
                except Exception:
                    pass

        tk.Button(
            prog_card, text="Reset Tutorial Checkmarks", font=self.FONT_LABEL,
            bg=self.COLORS["surface_container_low"], fg=self.COLORS["on_surface"],
            relief="solid", bd=1, padx=sc(12), pady=sc(5), cursor="hand2",
            command=_do_reset,
        ).pack(anchor="w")


def open_unified_help(parent, app_ref=None, initial_tab="tutorials"):
    """Open (or focus) the Unified Help Center window."""
    return UnifiedHelpWindow(parent, app_ref=app_ref, initial_tab=initial_tab)
