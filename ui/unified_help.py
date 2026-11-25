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

    LEARNING_PATH_IDS = ("review", "mobile")

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
                text=f"CORE INTRO: {count} OF {len(self.LEARNING_PATH_IDS)} COMPLETED"
            )

    # ------------------------------------------------------------------
    # Sidebar Navigation
    # ------------------------------------------------------------------

    def _build_sidebar_nav(self):
        nav_items = [
            ("tutorials", "Interactive Tutorials"),
            ("reference", "Badges & Reference"),
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
    # Build All 6 Tabs
    # ------------------------------------------------------------------

    def _build_all_tabs(self):
        self._build_tutorials_tab()
        self._build_reference_tab()
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
            "Getting Started with Arbor — 2-Part Core Introduction",
            "Start at your desk in safe Practice Mode (Part 1), then bring the exact same workflow into the collection on your phone (Part 2). Progress is saved automatically between sessions.",
        )

        done = get_completed_tutorials()

        def _start_flow(key):
            if self.app and hasattr(self.app, "start_tutorial_flow"):
                self._launch_and_close(lambda: self.app.start_tutorial_flow(key))

        def _start_mobile():
            from ui.tutorials import start_armed_shelf_guide
            if self.app:
                self._launch_and_close(lambda: start_armed_shelf_guide(self.app))

        def _start_triage_sandbox():
            from ui.tutorials import start_triage_tutorial
            if self.app:
                self._launch_and_close(lambda: start_triage_tutorial(self.app, use_sandbox=True))

        core_tutorials = [
            (
                "review",
                "Part 1 · At Your Desk",
                "Desktop Basics",
                "~3–4 min",
                "Practice Mode",
                True,
                (
                    "Start here if you are new to Arbor — learn all 3 core paths on real photos (#110 & #198):\n"
                    "• Check Registration Data, fill missing details, and resolve older catalog books in Problem Resolution\n"
                    "• Mark confirmed-blank fields using per-field ⋯ canonical ICEDIG codes (unknown:missing, etc.)\n"
                    "• Escalate physical damage with Needs Specialist ([REV+NOTE]) and learn when to click Mark Reviewed"
                ),
                lambda: _start_flow("review"),
                None,
            ),
            (
                "mobile",
                "Part 2 · In the Collection",
                "Mobile Companion",
                "~2 min",
                "Live · Uses Your Phone",
                False,
                (
                    "Translate the exact same ideas onto your phone for walking the collection aisles:\n"
                    "• Launch Phone Connector, scan the QR code, and set your shelf once (Set Shelf + 5-sec ↩ Undo)\n"
                    "• Use inline checkboxes on Data, tap any field value for ICEDIG codes, swipe to Problems & 📜 Old names, and flag Needs Specialist ([REV+NOTE])"
                ),
                _start_mobile,
                None,
            ),
        ]

        def _render_tutorial_card(tid, step_tag, title, duration, mode_lbl, is_sandbox, desc, launch_fn, secondary_action=None):
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

            if secondary_action:
                sec_lbl, sec_fn = secondary_action
                tk.Button(
                    btn_row,
                    text=sec_lbl,
                    font=self.FONT_SMALL,
                    bg=self.COLORS["surface_container_low"],
                    fg=self.COLORS["on_surface"],
                    relief="solid",
                    bd=1,
                    padx=sc(10),
                    pady=sc(5),
                    cursor="hand2",
                    command=sec_fn,
                ).pack(side="left", padx=(sc(8), 0))

        for spec in core_tutorials:
            _render_tutorial_card(*spec)

        # Clearly separated Optional & Advanced Tutorials section
        tk.Frame(inner, bg=self.COLORS["outline_variant"], height=1).pack(fill="x", pady=(sc(8), sc(14)))
        self._add_section_intro(
            inner,
            "Optional & Advanced Tutorials",
            "Independent guides you can try anytime once you are comfortable with the 2-part introduction.",
        )
        _render_tutorial_card(
            "triage",
            "Optional · Advanced",
            "Batch Problem Queue (One-by-One Desk Review)",
            "~2–3 min",
            "Live Workspace",
            False,
            (
                "An optional desk tool for stepping through every object with a flagged problem one by one:\n"
                "• Filter with Ctrl+G (Hallway Follow-Up or Archival Gaps) — clean [REV] and [REV+NOTE] stay out automatically\n"
                "• Step through Problem Resolution in Queue Mode, clear false alarms in 1 click, compare older books, and save (Ctrl+S)"
            ),
            lambda: _start_flow("triage"),
            ("🛡️ Practice with Sample Data", _start_triage_sandbox),
        )
        _render_tutorial_card(
            "database",
            "Optional · Admin",
            "Collections & New Specimens",
            "~2 min",
            "Practice Mode",
            True,
            (
                "Skip if you only work on an existing museum collection file.\n"
                "• See how to create a new collection Excel file from scratch\n"
                "• Practice adding a new specimen record (Ctrl+N) and setting its Storage Location (Ctrl+L)"
            ),
            lambda: _start_flow("database"),
        )

    def _build_reference_tab(self):
        inner = self._create_scrollable_tab("reference")
        self._add_section_intro(
            inner,
            "Badges, Icons & Quick Reference",
            "Every status badge, card chip, missing-data code, and everyday rule used across Arbor Desktop and Mobile Companion.",
        )

        # 1. Status Badges (Single-Badge Priority)
        badge_card = self._make_card(inner)
        tk.Label(
            badge_card,
            text="1. Status Badges (One Priority Badge Per Card)",
            font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
            anchor="w",
        ).pack(fill="x", pady=(0, sc(2)))
        tk.Label(
            badge_card,
            text="Arbor shows at most one status badge per specimen so you immediately see the most important action. Badges marked (Desktop) appear on unreviewed cards at your desk; Mobile Companion uses the reviewed, specialist, and conflict badges.",
            font=self.FONT_SMALL,
            fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["card_bg"],
            anchor="w",
            justify="left",
            wraplength=sc(540),
        ).pack(fill="x", pady=(0, sc(8)))

        badge_rows = [
            ("REV+ERR", "#F57C00", "#ffffff", "Reviewed with Actionable Error — Physically checked, but a data/label mismatch is flagged. Queued safely for desk follow-up (Ctrl+G → Hallway Follow-Up)."),
            ("REV+NOTE", "#e3f2ef", "#1b5e55", "Reviewed — Needs Specialist — Physically checked; ONLY Needs Specialist is ticked (damage, mold, pest, or expert question). Kept out of the default trainee queue."),
            ("REV", "#f2f9f3", "#3a7d44", "Reviewed & Verified — Physically checked and matches what is on file, with no open flags. All done!"),
            ("TAX", "#fdf2f2", "#c93a40", "Plant Name Issue (Desktop) — Unreviewed card with a Genus, Species, Author, or Family flag. Check the label or 📜 Old names."),
            ("PROV", "#fef9e7", "#b45309", "Origin / Collector Issue (Desktop) — Unreviewed card with a Collector, Collection Date, or Collection Place flag."),
            ("BOX", "#f7f5f4", "#757d77", "Box / Housing Issue (Desktop) — Unreviewed card with a Box Label mismatch (Box_Label_Problem)."),
            ("IMG", "#f0f8ff", "#4a7b9d", "Photo Issue (Desktop) — Unreviewed card with a missing, blurry, or mismatched photo (Images_Problem)."),
            ("ERR+HIS", "#e9f0f5", "#4a7b9d", "Error + Older Books (Desktop) — Unreviewed card with an actionable flag AND older catalog books loaded. Press Ctrl+H to compare."),
            ("CFCT", "#e9f0f5", "#4a7b9d", "Catalog Book Conflict — Older digitized catalog books disagree with the current record. Open Problem Resolution (Ctrl+H / Phone Problems tab)."),
            ("ERR", "#fdf2f2", "#c93a40", "General Actionable Error (Desktop) — Unreviewed card with another actionable problem flag."),
            ("NOTE", "#eceef6", "#434a6b", "Pending — Needs Specialist — Unreviewed card with ONLY Needs Specialist checked (never triggered by a plain Comment)."),
            ("UNREV", "#f2f5f1", "#757d77", "Unreviewed — Not checked yet. Inspect the specimen, verify the details, and click Mark Reviewed."),
        ]

        for label, bg, fg, desc in badge_rows:
            row = tk.Frame(badge_card, bg=self.COLORS["card_bg"])
            row.pack(fill="x", pady=sc(2))
            pill_wrap = tk.Frame(row, bg=self.COLORS["card_bg"], width=sc(92))
            pill_wrap.pack(side="left", anchor="n")
            pill_wrap.pack_propagate(False)
            tk.Label(
                pill_wrap,
                text=f" {label} ",
                font=self.FONT_MONO,
                bg=bg,
                fg=fg,
                padx=sc(4),
                pady=sc(1),
            ).pack(side="left")
            tk.Label(
                row,
                text=desc,
                font=self.FONT_BODY,
                fg=self.COLORS["on_surface"],
                bg=self.COLORS["card_bg"],
                anchor="w",
                justify="left",
                wraplength=sc(445),
            ).pack(side="left", fill="x", expand=True)

        # 2. Card Chips & Visual Markers
        chip_card = self._make_card(inner)
        tk.Label(
            chip_card,
            text="2. Card Chips & Visual Markers",
            font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
            anchor="w",
        ).pack(fill="x", pady=(0, sc(6)))

        chip_rows = [
            ("LOAN / ↗ Loaned", "#fef3c7", "#92400e", "Specimen is currently loaned out (toggle in Storage Location on Desktop, or the Location tab on Phone)."),
            ("UKN", "#eef1ee", "#444c47", "At least one field contains a confirmed ICEDIG missing-data code (unknown:* or withheld)."),
            ("UNVAL", "#eef1ee", "#444c47", "Has a draft note in Unvalidated_source (e.g. uncertain handwriting saved without altering the main field)."),
            ("NO PHOTO", "#eef1ee", "#444c47", "No photo is linked yet (or Images_Problem is flagged). ONLINE means photos load from an online link."),
            ("● Unsaved", "#fef3c7", "#92400e", "Amber dot in the top bar: you have edits not yet written to Excel. Press Ctrl+S to save."),
            ("Yellow Box", "#fef9c3", "#854d0e", "A Registration field glows yellow while its problem checkbox is ticked. Untick the box once you are confident it is fixed."),
        ]
        for label, bg, fg, desc in chip_rows:
            row = tk.Frame(chip_card, bg=self.COLORS["card_bg"])
            row.pack(fill="x", pady=sc(2))
            pill_wrap = tk.Frame(row, bg=self.COLORS["card_bg"], width=sc(112))
            pill_wrap.pack(side="left", anchor="n")
            pill_wrap.pack_propagate(False)
            tk.Label(
                pill_wrap,
                text=f" {label} ",
                font=self.FONT_MONO,
                bg=bg,
                fg=fg,
                padx=sc(4),
                pady=sc(1),
            ).pack(side="left")
            tk.Label(
                row,
                text=desc,
                font=self.FONT_BODY,
                fg=self.COLORS["on_surface"],
                bg=self.COLORS["card_bg"],
                anchor="w",
                justify="left",
                wraplength=sc(425),
            ).pack(side="left", fill="x", expand=True)

        # 3. The 3-Way Problem Rule
        rule_card = self._make_card(inner)
        tk.Label(
            rule_card,
            text="3. The 3-Way Problem Rule (Which Option to Pick)",
            font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
            anchor="w",
        ).pack(fill="x", pady=(0, sc(6)))

        rules = [
            ("1. Confirmed Blank or Illegible → ICEDIG Code", "Click the ⋯ button on the field (Desktop) or tap the field value (Phone) to insert unknown:missing or unknown:indecipherable. Do NOT flag a problem when the label genuinely lacks that detail."),
            ("2. Data or Label Mismatch → Tick the Field's Problem Box", "Use when the physical object disagrees with what is on file (e.g. label says Africa, file says China) or older catalog books conflict. Resolve in Problem Resolution (Ctrl+H / Phone Problems tab) or leave flagged ([REV+ERR]) for desk follow-up."),
            ("3. Damage, Pests, or Expert Question → Needs Specialist + Comment", "Use for torn/moldy boxes, mixed specimens, or taxonomic doubts needing a curator. Shows calm [REV+NOTE] or [NOTE] and stays out of the everyday trainee Problem Queue."),
        ]
        for heading, body_txt in rules:
            tk.Label(
                rule_card,
                text=heading,
                font=self.FONT_LABEL,
                fg=self.COLORS["secondary_dark"],
                bg=self.COLORS["card_bg"],
                anchor="w",
            ).pack(fill="x", pady=(sc(3), sc(1)))
            tk.Label(
                rule_card,
                text=body_txt,
                font=self.FONT_BODY,
                fg=self.COLORS["on_surface_variant"],
                bg=self.COLORS["card_bg"],
                anchor="w",
                justify="left",
                wraplength=sc(540),
            ).pack(fill="x", pady=(0, sc(4)))

        # 4. ICEDIG Missing-Data Codes
        icedig_card = self._make_card(inner)
        tk.Label(
            icedig_card,
            text="4. Standard Missing-Data Codes (ICEDIG)",
            font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
            anchor="w",
        ).pack(fill="x", pady=(0, sc(4)))
        tk.Label(
            icedig_card,
            text="Insert via the ⋯ button on any field, the ICEDIG ▾ menu in Problem Resolution, or by typing the short code:",
            font=self.FONT_SMALL,
            fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["card_bg"],
            anchor="w",
            justify="left",
            wraplength=sc(540),
        ).pack(fill="x", pady=(0, sc(6)))

        icedig_rows = [
            ("unknown:missing", "?m", "Confirmed absent on the physical label (e.g. no date was ever written). Never use if older catalog books have a value — check Problem Resolution first!"),
            ("unknown:indecipherable", "?i", "Faded ink, torn paper, water damage, or handwriting that cannot be read."),
            ("unknown:undigitized", "?u", "Present on the specimen, but skipped during an earlier digitization pass."),
            ("withheld", "?w", "Intentionally hidden for conservation or legal reasons (e.g. exact GPS of an endangered species)."),
        ]
        for code, short, desc in icedig_rows:
            row = tk.Frame(icedig_card, bg=self.COLORS["card_bg"])
            row.pack(fill="x", pady=sc(2))
            tk.Label(
                row,
                text=f" {code} ({short}) ",
                font=self.FONT_MONO,
                bg=self.COLORS["keycap_bg"],
                fg=self.COLORS["primary"],
                highlightbackground=self.COLORS["keycap_border"],
                highlightthickness=1,
                padx=sc(4),
                pady=sc(1),
            ).pack(side="left", anchor="n", padx=(0, sc(8)))
            tk.Label(
                row,
                text=desc,
                font=self.FONT_BODY,
                fg=self.COLORS["on_surface"],
                bg=self.COLORS["card_bg"],
                anchor="w",
                justify="left",
                wraplength=sc(350),
            ).pack(side="left", fill="x", expand=True)

        # 5. Everyday Conventions & Tips
        conv_card = self._make_card(inner)
        tk.Label(
            conv_card,
            text="5. Everyday Conventions & Field Rules",
            font=self.FONT_CARD_TITLE,
            fg=self.COLORS["primary"],
            bg=self.COLORS["card_bg"],
            anchor="w",
        ).pack(fill="x", pady=(0, sc(6)))

        conventions = (
            "• Date format (DD.MM.YYYY): Use 00 for unknown parts — e.g. 15.07.1965, 00.06.1912, or 00.00.1954 (or just 1954).\n"
            "• Author vs. Collector: Author is the scientist who named the species (e.g. L.); Collector is the person who gathered the plant in the field.\n"
            "• Physical-Inspection Rule: Only click Mark Reviewed after checking the real specimen (or its full label scan). Flagging an issue and still clicking Mark Reviewed is encouraged — it saves your verification as [REV+ERR] or [REV+NOTE] so nobody checks the box twice.\n"
            "• Old Plant & Family Names: Unfamiliar names on old boxes (like Compositae for Asteraceae) are often valid older synonyms. Check 📜 Old names before flagging a name mismatch.\n"
            "• Desktop ↔ Mobile Companion: Phone tabs are Data · Location · Problems (Problems works just like Desktop's Ctrl+H Problem Resolution). Always close Microsoft Excel before saving with Ctrl+S."
        )
        tk.Label(
            conv_card,
            text=conventions,
            font=self.FONT_BODY,
            fg=self.COLORS["on_surface_variant"],
            bg=self.COLORS["card_bg"],
            anchor="w",
            justify="left",
            wraplength=sc(540),
        ).pack(fill="x")

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
