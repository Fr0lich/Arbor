"""
ui/old_names_dialog.py

Read-only 1-tap "Old Names & Synonyms" lookup popover for Desktop Arbor.
Displays past museum names (Log & historical ledgers), offline classical/APG
family aliases, and ranked GBIF synonyms (Basionym & Homotypic first) without
blocking the Tkinter main thread.
"""

import tkinter as tk
from tkinter import ttk
from config import sc


class OldNamesDialog:
    """Lightweight, read-only popup displaying known older names for the active specimen."""

    def __init__(self, main_ui):
        self.ui = main_ui
        self.app = getattr(main_ui, "app", None)
        self.root = getattr(main_ui, "root", None)
        self._data = None
        self._show_more = False

        oid = getattr(self.app, "current_object_id", None) if self.app else None
        if not oid:
            if hasattr(main_ui, "show_toast"):
                main_ui.show_toast("Select a specimen first to view older names.", "info")
            return

        self.oid = str(oid)
        self.genus, self.species, self.family = self._read_active_taxon()

        is_dark = bool(getattr(main_ui, "dark_mode_active", False))
        self.bg = "#1e2220" if is_dark else "#fbfaf8"
        self.surface = "#262b28" if is_dark else "#ffffff"
        self.tonal = "#2d3330" if is_dark else "#f2f5f1"
        self.border = "#3c443f" if is_dark else "#dce2dd"
        self.fg = "#e8ebe9" if is_dark else "#1f2421"
        self.muted = "#9aa59e" if is_dark else "#5a655e"
        self.accent = "#52b765" if is_dark else "#2d5a3c"

        self.win = tk.Toplevel(self.root)
        self.win.title(f"Old Names & Synonyms — #{self.oid}")
        self.win.configure(bg=self.bg)
        self.win.transient(self.root)
        self.win.resizable(True, True)
        self.win.minsize(sc(420), sc(360))
        self.win.bind("<Escape>", lambda e: self.win.destroy())

        self._build_ui()

        import utils
        utils.center_and_fit_toplevel(self.win, sc(500), sc(480))
        self._load_async()

    def _read_active_taxon(self):
        reg_vars = getattr(self.ui, "reg_vars", None) or {}
        g = str(reg_vars["Genus"].get()).strip() if "Genus" in reg_vars else ""
        s = str(reg_vars["Species"].get()).strip() if "Species" in reg_vars else ""
        f = str(reg_vars["Family"].get()).strip() if "Family" in reg_vars else ""
        if not g and self.app and getattr(self.app, "df_reg", None) is not None and self.oid in self.app.df_reg.index:
            try:
                row = self.app.df_reg.loc[self.oid]
                g = str(row.get("Genus", "") or "").strip()
                s = str(row.get("Species", "") or "").strip()
                f = str(row.get("Family", "") or "").strip()
            except Exception:
                pass
        return g, s, f

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.win, bg=self.surface, padx=sc(14), pady=sc(10))
        hdr.pack(fill="x", side="top")
        tk.Frame(self.win, bg=self.border, height=1).pack(fill="x", side="top")

        tk.Label(
            hdr, text="OLD NAMES & SYNONYMS (READ-ONLY)",
            font=("JetBrains Mono", sc(8), "bold"), bg=self.surface, fg=self.muted,
        ).pack(anchor="w")

        sci_name = f"{self.genus} {self.species}".strip() or f"Specimen #{self.oid}"
        fam_suffix = f"  ({self.family})" if self.family else ""
        tk.Label(
            hdr, text=sci_name + fam_suffix,
            font=("Lora", sc(12), "italic"), bg=self.surface, fg=self.fg,
        ).pack(anchor="w", pady=(sc(2), 0))

        # Bottom fallback filter / GBIF check + Close bar (packed before body)
        footer = tk.Frame(self.win, bg=self.tonal, padx=sc(14), pady=sc(10))
        footer.pack(fill="x", side="bottom")
        tk.Frame(self.win, bg=self.border, height=1).pack(fill="x", side="bottom")

        filter_row = tk.Frame(footer, bg=self.tonal)
        filter_row.pack(fill="x", pady=(0, sc(6)))

        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._on_filter_change())
        self.filter_entry = tk.Entry(
            filter_row, textvariable=self.filter_var,
            font=("Inter", sc(9)), bg=self.surface, fg=self.fg,
            insertbackground=self.fg, relief="solid", bd=1,
        )
        self.filter_entry.pack(side="left", fill="x", expand=True, ipady=sc(3))

        self.check_btn = tk.Button(
            filter_row, text="Check in GBIF", font=("Inter", sc(9), "bold"),
            bg=self.accent, fg="#ffffff", relief="flat", padx=sc(10), pady=sc(3),
            cursor="hand2", command=self._check_label_gbif,
        )
        self.check_btn.pack(side="left", padx=(sc(6), 0))

        self.verdict_lbl = tk.Label(
            footer, text="", font=("Inter", sc(9)), bg=self.tonal, fg=self.fg,
            wraplength=sc(450), justify="left", anchor="w",
        )

        btn_row = tk.Frame(footer, bg=self.tonal)
        btn_row.pack(fill="x", pady=(sc(4), 0))
        tk.Label(
            btn_row,
            text="If the physical label matches an old name above, keep the modern name.",
            font=("Inter", sc(8)), bg=self.tonal, fg=self.muted,
        ).pack(side="left")
        tk.Button(
            btn_row, text="Close", font=("Inter", sc(9), "bold"),
            bg=self.surface, fg=self.fg, relief="solid", bd=1,
            padx=sc(12), pady=sc(3), cursor="hand2", command=self.win.destroy,
        ).pack(side="right")

        # Scrollable content area
        body_wrap = tk.Frame(self.win, bg=self.bg)
        body_wrap.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(body_wrap, bg=self.bg, highlightthickness=0)
        sb = ttk.Scrollbar(body_wrap, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=self.bg, padx=sc(14), pady=sc(10))
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._win_id, width=e.width))
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        tk.Label(
            self.inner, text="Loading known old names…",
            font=("Inter", sc(9)), bg=self.bg, fg=self.muted,
        ).pack(anchor="w", pady=sc(12))

    def _load_async(self):
        from backend import gbif as gbif_mod
        from backend.task_queue import app_worker

        wb_path = getattr(self.app, "excel_path", None) if self.app else None
        local_history = gbif_mod.collect_local_old_names(self.app, self.oid)

        def _worker():
            cache_path = gbif_mod.get_synonym_cache_path(wb_path)
            syn = gbif_mod.get_synonyms(self.genus, self.species, family=self.family, cache_path=cache_path)
            syn["local_history"] = local_history
            return syn

        def _on_done(res):
            if not self.win.winfo_exists():
                return
            self._data = res
            self._render_list()

        def _on_err(_err):
            if not self.win.winfo_exists():
                return
            self._data = {
                "local_history": local_history,
                "old_families": gbif_mod.get_old_family_names(self.family),
                "primary_synonyms": [],
                "other_synonyms": [],
                "offline": True,
            }
            self._render_list()

        app_worker.run_in_background(_worker, _on_done, error_callback=_on_err)

    def _on_filter_change(self):
        self.verdict_lbl.pack_forget()
        if self._data is not None:
            self._render_list()

    def _render_list(self):
        for w in self.inner.winfo_children():
            w.destroy()
        if not self._data:
            return

        q = self.filter_var.get().strip().lower()
        match_q = lambda txt: (not q) or (q in str(txt or "").lower())

        local_hist = [x for x in self._data.get("local_history", []) if match_q(f"{x.get('name')} {x.get('source')}")]
        old_fams = [x for x in self._data.get("old_families", []) if match_q(f"{x.get('name')} {x.get('note')}")]
        primary = [x for x in self._data.get("primary_synonyms", []) if match_q(f"{x.get('name')} {x.get('author')}")]
        others = [x for x in self._data.get("other_synonyms", []) if match_q(f"{x.get('name')} {x.get('author')}")]

        def _section(title):
            tk.Label(
                self.inner, text=title.upper(),
                font=("JetBrains Mono", sc(8), "bold"), bg=self.bg, fg=self.muted,
            ).pack(anchor="w", pady=(sc(8), sc(3)))

        def _row(left_txt, right_txt="", italic=True):
            card = tk.Frame(self.inner, bg=self.surface, highlightbackground=self.border, highlightthickness=1, padx=sc(8), pady=sc(5))
            card.pack(fill="x", pady=sc(2))
            font_style = ("Lora", sc(9.5), "italic") if italic else ("Inter", sc(9.5), "bold")
            tk.Label(card, text=left_txt, font=font_style, bg=self.surface, fg=self.fg, anchor="w").pack(side="left")
            if right_txt:
                tk.Label(card, text=right_txt, font=("Inter", sc(8)), bg=self.surface, fg=self.muted, anchor="e").pack(side="right")

        if local_hist:
            _section("Past Names in This Museum")
            for item in local_hist:
                _row(item["name"], item.get("source", ""))

        if old_fams:
            _section("Old Family Names")
            for item in old_fams:
                _row(item["name"], item.get("note", ""), italic=False)

        if primary:
            _section("Most Likely Old Names (Basionym & Homotypic)")
            for item in primary:
                label = f"{item['name']} {item['author']}".strip() if item.get("author") else item["name"]
                _row(label, item.get("kind", "Synonym"))

        if others:
            if q or self._show_more or not primary:
                _section(f"Other Known Synonyms ({len(others)})")
                for item in others:
                    label = f"{item['name']} {item['author']}".strip() if item.get("author") else item["name"]
                    _row(label, item.get("kind", ""))
            else:
                tk.Button(
                    self.inner, text=f"Show {len(others)} more synonyms ▾",
                    font=("Inter", sc(9), "bold"), bg=self.tonal, fg=self.fg,
                    relief="solid", bd=1, pady=sc(4), cursor="hand2",
                    command=lambda: (setattr(self, "_show_more", True), self._render_list()),
                ).pack(fill="x", pady=(sc(8), sc(2)))

        if self._data.get("offline"):
            tk.Label(
                self.inner,
                text="Offline — showing local history & old family names only. Connect to internet for full GBIF synonyms.",
                font=("Inter", sc(8.5)), bg=self.tonal, fg="#b45309",
                wraplength=sc(440), justify="left", padx=sc(8), pady=sc(6),
            ).pack(fill="x", pady=(sc(8), 0))
        elif not (local_hist or old_fams or primary or others):
            msg = f'No loaded old names match "{q}". Click "Check in GBIF" below to compare directly.' if q else "No older synonyms recorded for this name."
            tk.Label(
                self.inner, text=msg,
                font=("Inter", sc(9)), bg=self.bg, fg=self.muted,
                wraplength=sc(440), justify="left",
            ).pack(anchor="w", pady=sc(10))

    def _check_label_gbif(self):
        label = self.filter_var.get().strip()
        if not label:
            self.verdict_lbl.config(text="Type a name from the physical label above first.", fg=self.muted)
            self.verdict_lbl.pack(fill="x", pady=(0, sc(4)))
            return

        self.check_btn.config(state="disabled", text="Checking…")
        from backend import gbif as gbif_mod
        from backend.task_queue import app_worker

        def _worker():
            return gbif_mod.compare_label_name(label, self.genus, self.species, reg_family=self.family)

        def _on_done(res):
            if not self.win.winfo_exists():
                return
            self.check_btn.config(state="normal", text="Check in GBIF")
            v = res.get("verdict")
            if v == "synonym_match":
                self.verdict_lbl.config(text=f"✓ {res.get('message', '')}", fg=self.accent)
            elif v == "different_species":
                self.verdict_lbl.config(text=f"⚠ {res.get('message', '')}", fg="#b45309")
            else:
                self.verdict_lbl.config(text=f"? {res.get('message', '')}", fg=self.muted)
            self.verdict_lbl.pack(fill="x", pady=(0, sc(4)))

        def _on_err(_err):
            if not self.win.winfo_exists():
                return
            self.check_btn.config(state="normal", text="Check in GBIF")
            self.verdict_lbl.config(text="Offline or unreachable — leave a note in Comment if unsure.", fg=self.muted)
            self.verdict_lbl.pack(fill="x", pady=(0, sc(4)))

        app_worker.run_in_background(_worker, _on_done, error_callback=_on_err)
