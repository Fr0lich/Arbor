import tkinter as tk
from ui.state import app_bus, DATABASE_UPDATED
from ui.mobile_panel import MobilePanel


class MobileDialog:
    """In-app mobile companion dialog (modal Toplevel).

    Embeds MobilePanel for all shared UI/server logic; this class only
    handles what is unique to the in-app context:
      - Modal Toplevel lifecycle (transient, grab_set, centering)
      - Pre-session desktop commit (prevent in-flight edits being lost)
      - MobileServer reuse across re-opens
      - Post-session desktop UI refresh (load_object, update_dirty_ui, etc.)
      - Exposing the server instance on parent_ui for reuse
    """

    def __init__(self, parent_ui, root, app_state):
        self.parent_ui = parent_ui
        self.root = root
        self.app_state = app_state
        self.port = 5055

        # Build modal window (DPI-safe sizing + multi-monitor centering)
        from tkinter import ttk
        from config import sc
        import utils

        self.win = tk.Toplevel(root)
        self.win.title("Arbor Mobile Companion - Vault Auditing & Offline Sync")
        self.win.minsize(sc(420), sc(460))
        self.win.resizable(True, True)
        self.win.transient(root)

        # Only lock if simultaneous edit is not enabled and no interactive tutorial HUD is active
        _tutorial_active = False
        try:
            from ui.tutorials.tutorial_runner import TutorialRunner
            _inst = getattr(TutorialRunner, "_active_instance", None)
            _hud = getattr(_inst, "hud_win", None) if _inst is not None else None
            if _hud is not None and _hud.winfo_exists():
                _tutorial_active = True
        except Exception:
            pass
        if (hasattr(self.parent_ui, "simultaneous_edit_var") and self.parent_ui.simultaneous_edit_var.get()) or _tutorial_active:
            pass
        else:
            self.win.grab_set()

        # Commit any active desktop typing before locking
        if hasattr(self.parent_ui, "commit_current_object"):
            try:
                self.parent_ui.commit_current_object()
            except Exception:
                pass

        # Scrollable host container so 13-inch 125%–150% DPI laptops never clip bottom controls
        is_dark = getattr(self.parent_ui, "dark_mode_active", getattr(self.parent_ui, "dark_mode", False))
        host_bg = "#1e211f" if is_dark else "#f7f5f0"
        self.win.configure(bg=host_bg)

        scroll_outer = tk.Frame(self.win, bg=host_bg)
        scroll_outer.pack(fill="both", expand=True)
        self._scroll_canvas = tk.Canvas(scroll_outer, bg=host_bg, highlightthickness=0, bd=0)
        vsb = ttk.Scrollbar(scroll_outer, orient="vertical", command=self._scroll_canvas.yview)
        self._panel_host = tk.Frame(self._scroll_canvas, bg=host_bg)
        win_id = self._scroll_canvas.create_window((0, 0), window=self._panel_host, anchor="nw")
        self._scroll_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._scroll_canvas.pack(side="left", fill="both", expand=True)

        self._panel_host.bind(
            "<Configure>",
            lambda e: self._scroll_canvas.configure(scrollregion=self._scroll_canvas.bbox("all"))
            if self._scroll_canvas.winfo_exists() else None,
        )
        self._scroll_canvas.bind(
            "<Configure>",
            lambda e: self._scroll_canvas.itemconfig(win_id, width=e.width)
            if self._scroll_canvas.winfo_exists() else None,
        )
        try:
            from ui.scroll_helper import bind_mousewheel
            bind_mousewheel(self._scroll_canvas, self._panel_host)
        except Exception:
            pass

        # Build panel — reuse an existing server if one is already running
        self.server = getattr(self.parent_ui, '_mobile_server_instance', None)
        self.tunnel = None
        self.port = 5055
        self.qr_image_ref = None
        self.local_url_with_token = ""
        self.public_url_with_token = ""
        self.current_qr_mode = "public"
        self.panel = MobilePanel(
            parent=self._panel_host,
            app_state=self.app_state,
            root_tk=self.root,
            port=self.port,
            on_end_session=self._end_session,
            on_edit=self._on_mobile_edit,
            reuse_server=self.server,
            parent_ui=self.parent_ui,
        )

        # Store server reference on parent UI and app state if already running
        if self.panel.server is not None:
            self.parent_ui._mobile_server_instance = self.panel.server
            self.app_state._mobile_server_instance = self.panel.server

        utils.center_and_fit_toplevel(self.win, sc(540), sc(700))
        self.win.protocol("WM_DELETE_WINDOW", self._end_session)
        self.win.bind("<Escape>", lambda e: self._end_session())

    # ------------------------------------------------------------------
    # Session end
    # ------------------------------------------------------------------

    def _end_session(self):
        """Stop panel, refresh desktop UI, close window."""
        self.panel.stop()

        # Reload the currently displayed object to pick up mobile edits
        if hasattr(self.parent_ui, "load_object") and self.app_state.current_object_id:
            try:
                self.parent_ui.load_object(self.app_state.current_object_id)
            except Exception:
                pass

        app_bus.publish(DATABASE_UPDATED)

        if hasattr(self.parent_ui, "_update_push_to_phone_state"):
            self.parent_ui.root.after(100, self.parent_ui._update_push_to_phone_state)

        # Check for unsaved in-memory changes from mobile session
        if getattr(self.app_state, "dirty", False):
            import config
            prefs = config.load_prefs() if hasattr(config, "load_prefs") else {}
            auto_save = getattr(self.panel, "auto_save_var", None)
            is_auto_save = auto_save.get() if auto_save else prefs.get("mobile_autosave_on_stop", False)

            has_valid_path = bool(
                hasattr(self.parent_ui, "app")
                and getattr(self.parent_ui.app, "output_path", None)
            )

            if is_auto_save and has_valid_path:
                if hasattr(self.parent_ui, "save_session"):
                    self.parent_ui.save_session("MOBILE_SESSION_END")
                elif hasattr(self.parent_ui, "save_database"):
                    self.parent_ui.save_database()
            else:
                from tkinter import messagebox
                try:
                    save_now = messagebox.askyesno(
                        title="Arbor Mobile Companion",
                        message=(
                            "Mobile session ended with unsaved changes in memory.\n\n"
                            "Save the workbook to disk now?"
                        ),
                        parent=self.win,
                    )
                except Exception:
                    save_now = False

                if save_now:
                    if hasattr(self.parent_ui, "save_session"):
                        self.parent_ui.save_session("MOBILE_SESSION_END")
                    elif hasattr(self.parent_ui, "save_database"):
                        self.parent_ui.save_database()

        self.win.destroy()

        # Notify desktop curator & offer Post-Shift Batch Follow-Up Popup
        try:
            df_obs = getattr(self.app_state, "df_obs", None)
            rev_err_count = 0
            session_ids = set(getattr(self.app_state, "last_mobile_session_reviewed_ids", None) or set())
            if not session_ids and self.server and getattr(self.server, "session_reviewed_ids", None):
                session_ids = set(self.server.session_reviewed_ids)
                try:
                    self.app_state.last_mobile_session_reviewed_ids = set(session_ids)
                except Exception:
                    pass

            session_reviewed_count = 0
            session_flagged_count = 0
            session_specialist_count = 0
            if df_obs is not None and not df_obs.empty and "Reviewed" in df_obs.columns:
                rev_mask = df_obs["Reviewed"].fillna(False).astype(bool)
                prob_cols = [c for c in df_obs.columns if c.endswith("_Problem") and c != "Other_problem"]
                prob_mask = df_obs[prob_cols].fillna(False).astype(bool).any(axis=1) if prob_cols else (rev_mask & False)
                spec_mask = df_obs["Other_problem"].fillna(False).astype(bool) if "Other_problem" in df_obs.columns else (rev_mask & False)
                rev_err_count = int((rev_mask & prob_mask).sum())

                if session_ids:
                    idx_strs = df_obs.index.astype(str)
                    in_sess = idx_strs.isin(session_ids) & rev_mask
                    session_reviewed_count = int(in_sess.sum())
                    session_flagged_count = int((in_sess & prob_mask).sum())
                    session_specialist_count = int((in_sess & (~prob_mask) & spec_mask).sum())

            import config
            prefs = config.load_prefs() if hasattr(config, "load_prefs") else {}
            if prefs.get("suppress_mobile_stop_followup_popup", False):
                if rev_err_count > 0 and hasattr(self.parent_ui, "show_toast"):
                    self.parent_ui.show_toast(
                        f"Mobile sync complete · {rev_err_count} specimen(s) ready for Hallway Follow-Up (REV+ERR)",
                        "info",
                    )
            else:
                self._show_post_mobile_followup_popup(
                    rev_err_count,
                    session_reviewed_count=session_reviewed_count,
                    session_flagged_count=session_flagged_count,
                    session_specialist_count=session_specialist_count,
                )
        except Exception:
            pass

    def _show_post_mobile_followup_popup(
        self,
        rev_err_count: int,
        session_reviewed_count: int = 0,
        session_flagged_count: int = 0,
        session_specialist_count: int = 0,
    ):
        """Show a calm post-session wrap-up popup confirming mobile edits are synced in Arbor,
        offering 1-click access to the session's reviewed objects & Batch Problem Solver,
        and reminding the user to save (Ctrl+S)."""
        import config
        import utils
        from config import sc

        parent_root = getattr(self.parent_ui, "root", self.root)
        if not parent_root or not parent_root.winfo_exists():
            return

        pop = tk.Toplevel(parent_root)
        pop.title("Mobile Session Complete — Synced to Arbor")
        pop.transient(parent_root)
        pop.resizable(True, True)
        pop.minsize(sc(480), sc(420))
        self.parent_ui._post_mobile_followup_win = pop

        dark = getattr(self.parent_ui, "dark_mode_active", getattr(self.parent_ui, "dark_mode", False))
        bg = "#1e211f" if dark else "#f7f5f0"
        card_bg = "#252926" if dark else "#ffffff"
        fg = "#eef1ef" if dark else "#2c302e"
        muted = "#a2aba5" if dark else "#5e6560"
        border = "#3a403c" if dark else "#d8ddd6"
        accent = "#3a7d44"
        pop.configure(bg=bg)

        outer = tk.Frame(pop, bg=bg, padx=sc(22), pady=sc(18))
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="📱 MOBILE SESSION COMPLETE",
            font=("JetBrains Mono", sc(8.5), "bold"),
            bg="#1e3a24" if dark else "#eaf5ec",
            fg="#85e89d" if dark else "#1b5e20",
            padx=sc(8),
            pady=sc(3),
        ).pack(anchor="w", pady=(0, sc(10)))

        title_lbl = tk.Label(
            outer,
            text="All Your Phone Work Is Now in Arbor!",
            font=("Lora", sc(13), "bold"),
            bg=bg, fg=fg, anchor="w", justify="left", wraplength=sc(490),
        )
        title_lbl.pack(fill="x", pady=(0, sc(6)))

        if session_reviewed_count > 0:
            clean_cnt = max(0, session_reviewed_count - session_flagged_count - session_specialist_count)
            parts = [f"{clean_cnt} clean"]
            if session_flagged_count > 0:
                parts.append(f"{session_flagged_count} flagged")
            if session_specialist_count > 0:
                parts.append(f"{session_specialist_count} Needs Specialist")
            session_line = (
                f"You marked {session_reviewed_count} object{'s' if session_reviewed_count != 1 else ''} as reviewed "
                f"during this mobile session ({', '.join(parts)})."
            )
        else:
            flagged_note = (
                f" ({rev_err_count} reviewed object{'s' if rev_err_count != 1 else ''} currently have open flags you can review whenever you're ready.)"
                if rev_err_count > 0
                else ""
            )
            session_line = (
                "Every location, edit, and flag you recorded on Mobile Companion is already synced into your open Arbor workspace."
                f"{flagged_note}"
            )
        session_lbl = tk.Label(
            outer, text=session_line, font=("Inter", sc(9.5)),
            bg=bg, fg=muted, anchor="w", justify="left", wraplength=sc(490),
        )
        session_lbl.pack(fill="x", pady=(0, sc(8)))

        save_reminder_lbl = tk.Label(
            outer,
            text="IMPORTANT: Remember to save your Excel file (Ctrl+S) so your changes are written safely to disk.",
            font=("Inter", sc(9.5), "bold"),
            bg=bg, fg=fg, anchor="w", justify="left", wraplength=sc(490),
        )
        save_reminder_lbl.pack(fill="x", pady=(0, sc(12)))

        # Next-steps exploration card
        tip_card = tk.Frame(
            outer, bg=card_bg, highlightbackground=border, highlightthickness=1,
            padx=sc(12), pady=sc(9),
        )
        tip_card.pack(fill="x", pady=(0, sc(12)))
        tip_lbl = tk.Label(
            tip_card,
            text=(
                "Where to explore next:\n"
                "• Use Filter (Ctrl+G) to find objects with specific qualities — flagged issues, Needs Specialist, ICEDIG codes, or shelf locations\n"
                "• Open Help (HELP in the top bar) anytime to browse optional & advanced tutorials"
            ),
            font=("Inter", sc(9)), bg=card_bg, fg=fg, anchor="w", justify="left", wraplength=sc(460),
        )
        tip_lbl.pack(fill="x")

        def _on_outer_resize(event):
            avail = max(sc(280), event.width - sc(48))
            for lbl in (title_lbl, session_lbl, save_reminder_lbl):
                lbl.configure(wraplength=avail)
            tip_lbl.configure(wraplength=max(sc(250), avail - sc(28)))

        outer.bind("<Configure>", _on_outer_resize)

        dont_show_var = tk.BooleanVar(value=False)

        def _persist_opt():
            if dont_show_var.get():
                try:
                    p = config.load_prefs() or {}
                    p["suppress_mobile_stop_followup_popup"] = True
                    config.save_prefs(p)
                except Exception:
                    pass

        def _close():
            _persist_opt()
            if pop.winfo_exists():
                pop.destroy()

        def _save_now():
            _persist_opt()
            if pop.winfo_exists():
                pop.destroy()
            for fn_name in ("save_excel", "save_changes", "save_file"):
                fn = getattr(self.parent_ui, fn_name, None)
                if callable(fn):
                    fn()
                    break

        def _open_filter():
            _persist_opt()
            if pop.winfo_exists():
                pop.destroy()
            for fn_name in ("open_filter_dialog", "show_filter_dialog"):
                fn = getattr(self.parent_ui, fn_name, None)
                if callable(fn):
                    fn()
                    break

        def _open_help():
            _persist_opt()
            if pop.winfo_exists():
                pop.destroy()
            for fn_name in ("open_help_window", "show_main_help"):
                fn = getattr(self.parent_ui, fn_name, None)
                if callable(fn):
                    fn()
                    break

        def _view_session_reviewed():
            _persist_opt()
            if pop.winfo_exists():
                pop.destroy()
            fn = getattr(self.parent_ui, "apply_reviewed_batch_filter", None)
            if callable(fn):
                fn("mobile_session")

        def _send_session_to_solver():
            _persist_opt()
            if pop.winfo_exists():
                pop.destroy()
            fn = getattr(self.parent_ui, "send_reviewed_batch_to_problem_queue", None)
            if callable(fn):
                fn("mobile_session")

        tk.Checkbutton(
            outer,
            text="Don't show this popup again when stopping Mobile Companion",
            variable=dont_show_var,
            font=("Inter", sc(9)),
            bg=bg, fg=muted, activebackground=bg, activeforeground=fg,
            selectcolor=card_bg, cursor="hand2",
        ).pack(anchor="w", pady=(0, sc(12)))

        btn_row = tk.Frame(outer, bg=bg)
        btn_row.pack(fill="x")

        tk.Button(
            btn_row,
            text="💾 Save File Now (Ctrl+S)",
            font=("Inter", sc(9.5), "bold"),
            bg=accent, fg="#ffffff", activebackground="#2f6638", activeforeground="#ffffff",
            relief="flat", padx=sc(12), pady=sc(7), cursor="hand2", command=_save_now,
        ).pack(fill="x", pady=(0, sc(6)))

        if session_reviewed_count > 0:
            sess_row = tk.Frame(btn_row, bg=bg)
            sess_row.pack(fill="x", pady=(0, sc(6)))
            tk.Button(
                sess_row,
                text=f"✅ View {session_reviewed_count} Reviewed",
                font=("Inter", sc(9), "bold"), bg=card_bg, fg=fg,
                relief="flat", highlightbackground=border, highlightthickness=1,
                padx=sc(10), pady=sc(6), cursor="hand2", command=_view_session_reviewed,
            ).pack(side="left", expand=True, fill="x", padx=(0, sc(6)))

            solver_label = (
                f"🔧 Batch Problem Solver ({session_flagged_count} flagged)"
                if session_flagged_count > 0
                else "🔧 Send to Batch Problem Solver"
            )
            tk.Button(
                sess_row,
                text=solver_label,
                font=("Inter", sc(9), "bold"),
                bg="#fef3c7" if (not dark and session_flagged_count > 0) else card_bg,
                fg="#92400e" if (not dark and session_flagged_count > 0) else fg,
                relief="flat", highlightbackground=border, highlightthickness=1,
                padx=sc(10), pady=sc(6), cursor="hand2", command=_send_session_to_solver,
            ).pack(side="left", expand=True, fill="x")

        sec_row = tk.Frame(btn_row, bg=bg)
        sec_row.pack(fill="x")
        tk.Button(
            sec_row,
            text="🔍 Filter (Ctrl+G)",
            font=("Inter", sc(9)), bg=card_bg, fg=fg,
            relief="flat", highlightbackground=border, highlightthickness=1,
            padx=sc(10), pady=sc(6), cursor="hand2", command=_open_filter,
        ).pack(side="left", expand=True, fill="x", padx=(0, sc(6)))

        tk.Button(
            sec_row,
            text="❓ Help & Tutorials",
            font=("Inter", sc(9)), bg=card_bg, fg=fg,
            relief="flat", highlightbackground=border, highlightthickness=1,
            padx=sc(10), pady=sc(6), cursor="hand2", command=_open_help,
        ).pack(side="left", expand=True, fill="x", padx=(0, sc(6)))

        tk.Button(
            sec_row,
            text="Close",
            font=("Inter", sc(9)), bg=card_bg, fg=fg,
            relief="flat", highlightbackground=border, highlightthickness=1,
            padx=sc(14), pady=sc(6), cursor="hand2", command=_close,
        ).pack(side="right")

        pop.protocol("WM_DELETE_WINDOW", _close)
        pop.bind("<Escape>", lambda e: _close())
        pop.update_idletasks()
        init_w = max(sc(560), pop.winfo_reqwidth() + sc(24))
        init_h = max(sc(520 if session_reviewed_count > 0 else 460), pop.winfo_reqheight() + sc(24))
        utils.center_and_fit_toplevel(pop, init_w, init_h)

    # ------------------------------------------------------------------
    # Edit callback — notify desktop UI of each incoming mobile edit
    # ------------------------------------------------------------------

    def _on_mobile_edit(self, oid, summary):
        # <<MobileEdit>> is already fired by MobileServer.update_object() directly on root_tk.
        # Do NOT fire it a second time here — that would cause double load_object(), double
        # refresh_list(), and double autosave in the main window handler.
        # This method is retained as a documented hook for future dialog-specific reactions.
        pass
