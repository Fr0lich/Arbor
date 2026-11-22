"""
ui/tutorials/tutorial_runner.py

Action-driven interactive tutorial engine for Arbor.
Provides event-gated step progression, glowing target element highlights,
and persistent skip/exit controls.
"""

import tkinter as tk
from tkinter import ttk
from config import sc
from .sandbox_manager import SandboxManager


class ActionStep:
    def __init__(self, step_id, title, instruction, target_id=None,
                 action_hint=None, on_enter=None, validator=None, keycaps=None, details=None):
        self.step_id = step_id
        self.title = title
        self.instruction = instruction
        self.target_id = target_id
        self.action_hint = action_hint
        self.on_enter = on_enter
        self.validator = validator
        self.keycaps = list(keycaps) if keycaps else []
        self.details = details


class TutorialHighlight:
    """Animated glowing border frame around a target widget."""
    def __init__(self, parent, target_widget):
        self.target_widget = target_widget
        self.win = tk.Toplevel(parent)
        if parent:
            try:
                self.win.transient(parent)
            except Exception:
                pass
        self.win.overrideredirect(True)

        try:
            self.win.attributes("-transparentcolor", "black")
        except Exception:
            pass
        self.win.config(bg="black")

        self.canvas = tk.Canvas(self.win, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.rect = self.canvas.create_rectangle(0, 0, 10, 10, outline="#3a7d44", width=4)

        self._anim_idx = 0
        self._last_geom = None
        self.win.deiconify()
        self.win.lift()
        self.update_position()
        self.animate()

    def update_position(self):
        try:
            if not self.target_widget or not self.target_widget.winfo_exists() or not self.target_widget.winfo_viewable():
                if self.win.winfo_exists():
                    self.win.withdraw()
                self._last_geom = None
                return

            x = self.target_widget.winfo_rootx()
            y = self.target_widget.winfo_rooty()
            w = self.target_widget.winfo_width()
            h = self.target_widget.winfo_height()

            geom_key = (x, y, w, h)
            if geom_key == self._last_geom:
                return
            self._last_geom = geom_key

            pad = 4
            if self.win.winfo_exists():
                self.win.deiconify()
                self.win.geometry(f"{w + pad*2}x{h + pad*2}{x - pad:+d}{y - pad:+d}")
                self.canvas.coords(self.rect, pad, pad, w + pad, h + pad)
        except Exception:
            try:
                if self.win.winfo_exists():
                    self.win.withdraw()
            except Exception:
                pass

    def animate(self):
        if not self.win.winfo_exists():
            return
        colors = ["#3a7d44", "#52b765", "#85e89d", "#52b765"]
        try:
            self.canvas.itemconfig(self.rect, outline=colors[self._anim_idx])
        except Exception:
            pass
        self._anim_idx = (self._anim_idx + 1) % len(colors)
        self.update_position()
        try:
            self.win.after(250, self.animate)
        except Exception:
            pass

    def destroy(self):
        if self.win.winfo_exists():
            try:
                self.win.destroy()
            except Exception:
                pass


class TutorialRunner:
    """Drives step progression and UI synchronization for an action-driven tutorial."""
    _active_instance = None

    def __init__(self, ui, steps, tutorial_name="Interactive Tutorial", on_complete=None,
                 use_sandbox=True, badge_text=None):
        # Single-runner guard: close any previous active tutorial HUD so two never overlap.
        # If switching from a sandbox tour to a non-sandbox Quick Guide, exit sandbox cleanly.
        prev = TutorialRunner._active_instance
        if prev is not None and prev is not self:
            try:
                if prev.use_sandbox and not use_sandbox:
                    prev.exit_tutorial()
                else:
                    prev._cleanup()
            except Exception:
                pass

        self.ui = ui
        self.steps = steps
        self.tutorial_name = tutorial_name
        self.on_complete = on_complete
        self.use_sandbox = use_sandbox
        self.badge_text = badge_text or ("🛡️ PRACTICE SANDBOX" if use_sandbox else "⚡ QUICK GUIDE")
        self.current_idx = 0

        self.hud_win = None
        self.highlight = None
        self._poll_job = None
        self._details_expanded = False
        self.root = ui.root if hasattr(ui, "root") else ui

        TutorialRunner._active_instance = self
        if self.use_sandbox:
            SandboxManager()._active_runner = self

        self._build_hud()
        self.show_step()

    def _build_hud(self):
        self.hud_win = tk.Toplevel(self.root)
        self.hud_win.title(f"Arbor Tutorial - {self.tutorial_name}")
        self.hud_win.attributes("-topmost", True)
        self.hud_win.resizable(False, False)
        self.hud_win.config(bg="#181c19")
        self.hud_win.protocol("WM_DELETE_WINDOW", self.exit_tutorial)
        self.hud_win.bind("<Escape>", lambda e: self.exit_tutorial())

        # Main HUD container
        frame = tk.Frame(self.hud_win, bg="#181c19", padx=sc(16), pady=sc(14), highlightbackground="#3a7d44", highlightthickness=1)
        frame.pack(fill="both", expand=True)

        # Header Row: Badge & Progress
        hdr_row = tk.Frame(frame, bg="#181c19")
        hdr_row.pack(fill="x", pady=(0, sc(6)))

        self.badge_lbl = tk.Label(
            hdr_row,
            text=self.badge_text,
            font=("JetBrains Mono", sc(8), "bold"),
            bg="#1e3a24",
            fg="#85e89d",
            padx=sc(6),
            pady=sc(2)
        )
        self.badge_lbl.pack(side="left")

        self.step_counter_lbl = tk.Label(
            hdr_row,
            text=f"STEP 1 OF {len(self.steps)}",
            font=("JetBrains Mono", sc(8), "bold"),
            bg="#181c19",
            fg="#a2aba5"
        )
        self.step_counter_lbl.pack(side="right")

        # Progress bar track
        self.progress_track = tk.Frame(frame, bg="#2c302e", height=sc(4))
        self.progress_track.pack(fill="x", pady=(0, sc(10)))
        self.progress_track.pack_propagate(False)
        self.progress_fill = tk.Frame(self.progress_track, bg="#3a7d44", height=sc(4), width=1)
        self.progress_fill.place(x=0, y=0, relheight=1.0, relwidth=1.0 / max(1, len(self.steps)))

        # Step Title
        self.title_lbl = tk.Label(
            frame,
            text="",
            font=("Inter", sc(12), "bold"),
            bg="#181c19",
            fg="#ffffff",
            anchor="w",
            justify="left"
        )
        self.title_lbl.pack(fill="x", pady=(0, sc(6)))

        # Instruction Text
        self.instruction_lbl = tk.Label(
            frame,
            text="",
            font=("Inter", sc(10)),
            bg="#181c19",
            fg="#e8ebe9",
            anchor="w",
            justify="left",
            wraplength=sc(380)
        )
        self.instruction_lbl.pack(fill="x", pady=(0, sc(8)))

        # Collapsible "💡 More Details & Excel Impact" Drawer (keeps default step crisp)
        self.details_toggle_btn = tk.Button(
            frame,
            text="▸ 💡 More Details & Excel Impact",
            font=("Inter", sc(8.5), "bold"),
            bg="#181c19",
            fg="#85e89d",
            activebackground="#212622",
            activeforeground="#b0f3a9",
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            command=self._toggle_details,
        )
        self.details_frame = tk.Frame(
            frame,
            bg="#1f2521",
            highlightbackground="#3a7d44",
            highlightthickness=1,
            padx=sc(10),
            pady=sc(8),
        )
        self.details_lbl = tk.Label(
            self.details_frame,
            text="",
            font=("Inter", sc(9)),
            bg="#1f2521",
            fg="#d4dcd6",
            anchor="w",
            justify="left",
            wraplength=sc(360),
        )
        self.details_lbl.pack(fill="x")

        # Floating visual keycaps row (shown on steps with keyboard shortcuts)
        self.keycaps_frame = tk.Frame(frame, bg="#181c19")
        self.keycaps_frame.pack(fill="x", pady=(0, sc(10)))

        # Action hint bar
        self.hint_frame = tk.Frame(frame, bg="#212622", padx=sc(10), pady=sc(7), highlightbackground="#2e4a33", highlightthickness=1)
        self.hint_frame.pack(fill="x", pady=(0, sc(14)))

        self.hint_lbl = tk.Label(
            self.hint_frame,
            text="",
            font=("Inter", sc(9), "italic"),
            bg="#212622",
            fg="#85e89d",
            anchor="w",
            justify="left"
        )
        self.hint_lbl.pack(fill="x")

        # Footer Button Bar
        btn_bar = tk.Frame(frame, bg="#181c19")
        btn_bar.pack(fill="x")

        self.exit_btn = tk.Button(
            btn_bar,
            text="Exit Tutorial",
            font=("Inter", sc(9)),
            bg="#212622",
            fg="#ff8a80",
            relief="flat",
            cursor="hand2",
            padx=sc(8),
            pady=sc(4),
            command=self.exit_tutorial
        )
        self.exit_btn.pack(side="left")

        self.next_btn = tk.Button(
            btn_bar,
            text="Skip Step →",
            font=("Inter", sc(9), "bold"),
            bg="#3a7d44",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=sc(12),
            pady=sc(4),
            command=self.next_step
        )
        self.next_btn.pack(side="right", padx=(sc(6), 0))

        self.prev_btn = tk.Button(
            btn_bar,
            text="← Back",
            font=("Inter", sc(9)),
            bg="#212622",
            fg="#e8ebe9",
            relief="flat",
            cursor="hand2",
            padx=sc(8),
            pady=sc(4),
            command=self.prev_step
        )
        self.prev_btn.pack(side="right")

        # Position HUD in top-right corner of parent or screen
        self._position_hud()

    def _toggle_details(self):
        self._details_expanded = not self._details_expanded
        if self._details_expanded:
            self.details_toggle_btn.config(text="▾ 💡 Hide Details")
            self.details_frame.pack(fill="x", pady=(sc(2), sc(10)), after=self.details_toggle_btn)
        else:
            self.details_toggle_btn.config(text="▸ 💡 More Details & Excel Impact")
            self.details_frame.pack_forget()

    def _position_hud(self, target_widget=None):
        """Position HUD on the same monitor as self.root, auto-dodging target_widget."""
        try:
            self.hud_win.update_idletasks()
            w = self.hud_win.winfo_reqwidth()
            h = self.hud_win.winfo_reqheight()

            parent_root = self.ui.root if hasattr(self.ui, "root") else self.root
            if parent_root and parent_root.winfo_exists():
                parent_root.update_idletasks()
                rx = parent_root.winfo_rootx()
                ry = parent_root.winfo_rooty()
                rw = parent_root.winfo_width()
                rh = parent_root.winfo_height()
                if rw > 100 and rh > 100:
                    dock_left = False
                    if target_widget is not None:
                        try:
                            if target_widget.winfo_exists() and target_widget.winfo_viewable():
                                tx_center = target_widget.winfo_rootx() + (target_widget.winfo_width() // 2)
                                if tx_center > (rx + rw // 2):
                                    dock_left = True
                        except Exception:
                            pass

                    if dock_left:
                        x = rx + sc(24)
                    else:
                        x = max(rx + sc(12), rx + rw - w - sc(24))
                    y = max(ry + sc(40), ry + sc(56))
                    self.hud_win.geometry(f"{x:+d}{y:+d}")
                    return

            sw = self.hud_win.winfo_screenwidth()
            x = max(10, sw - w - sc(24))
            y = sc(56)
            self.hud_win.geometry(f"{x:+d}{y:+d}")
        except Exception:
            pass

    def show_step(self):
        self._cleanup_highlight()
        if self._poll_job:
            try:
                self.root.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None

        if self.current_idx >= len(self.steps):
            self.finish_tutorial()
            return

        step = self.steps[self.current_idx]
        self.step_counter_lbl.config(text=f"STEP {self.current_idx + 1} OF {len(self.steps)}")
        self.title_lbl.config(text=step.title)
        self.instruction_lbl.config(text=step.instruction)

        # Collapsible details drawer (reset to collapsed on step change for calm scanning)
        self._details_expanded = False
        self.details_frame.pack_forget()
        if getattr(step, "details", None):
            self.details_lbl.config(text=step.details)
            self.details_toggle_btn.config(text="▸ 💡 More Details & Excel Impact")
            self.details_toggle_btn.pack(fill="x", pady=(0, sc(8)), after=self.instruction_lbl)
        else:
            self.details_toggle_btn.pack_forget()

        # Render visual keycaps if defined on this step
        if hasattr(self, "keycaps_frame") and self.keycaps_frame.winfo_exists():
            for child in self.keycaps_frame.winfo_children():
                child.destroy()
            if getattr(step, "keycaps", None):
                self.keycaps_frame.pack(fill="x", pady=(0, sc(10)), before=self.hint_frame)
                tk.Label(
                    self.keycaps_frame,
                    text="SHORTCUT:",
                    font=("JetBrains Mono", sc(8), "bold"),
                    bg="#181c19",
                    fg="#848f87",
                ).pack(side="left", padx=(0, sc(6)))
                for idx_k, key_text in enumerate(step.keycaps):
                    if idx_k > 0:
                        tk.Label(
                            self.keycaps_frame,
                            text="+",
                            font=("JetBrains Mono", sc(9), "bold"),
                            bg="#181c19",
                            fg="#848f87",
                        ).pack(side="left", padx=sc(3))
                    cap = tk.Frame(
                        self.keycaps_frame,
                        bg="#263128",
                        highlightbackground="#52b765",
                        highlightthickness=1,
                        padx=sc(8),
                        pady=sc(2),
                    )
                    cap.pack(side="left")
                    tk.Label(
                        cap,
                        text=key_text,
                        font=("JetBrains Mono", sc(9), "bold"),
                        bg="#263128",
                        fg="#b0f3a9",
                    ).pack()
            else:
                self.keycaps_frame.pack_forget()

        if step.action_hint:
            self.hint_frame.pack(fill="x", pady=(0, sc(14)))
            self.hint_lbl.config(text=f"Action: {step.action_hint}")
        else:
            self.hint_frame.pack_forget()

        self.prev_btn.config(state="normal" if self.current_idx > 0 else "disabled")
        is_last = (self.current_idx == len(self.steps) - 1)
        if is_last:
            self.next_btn.config(text="Finish ✓")
        elif step.validator:
            self.next_btn.config(text="Skip Step →")
        else:
            self.next_btn.config(text="Next →")
        if hasattr(self, "progress_fill") and self.progress_fill.winfo_exists():
            frac = min(1.0, (self.current_idx + 1) / max(1, len(self.steps)))
            self.progress_fill.place(x=0, y=0, relheight=1.0, relwidth=frac)

        # Trigger on_enter callback if specified
        if step.on_enter:
            try:
                step.on_enter(self.ui)
            except Exception:
                pass

        # Highlight target widget & auto-dodge HUD away from it
        target_widget = self._find_target(step.target_id)
        self._position_hud(target_widget=target_widget)
        if target_widget:
            try:
                self.highlight = TutorialHighlight(self.root, target_widget)
            except Exception:
                self.highlight = None

        # Start validator polling if a validator condition is provided
        if step.validator:
            self._poll_validator(step.validator)

    def _poll_validator(self, validator_fn):
        if not self.hud_win or not self.hud_win.winfo_exists():
            return
        try:
            if validator_fn(self.ui):
                self.next_step()
                return
        except Exception:
            pass
        self._poll_job = self.root.after(300, lambda: self._poll_validator(validator_fn))

    def _find_target(self, target_id):
        if not target_id:
            return None
        if isinstance(target_id, tk.Widget):
            return target_id
        # Support precise registration field targeting: "reg_field:<FieldName>"
        if isinstance(target_id, str) and target_id.startswith("reg_field:"):
            field_name = target_id.split(":", 1)[1]
            reg_entries = getattr(self.ui, "reg_entries", None) or {}
            w = reg_entries.get(field_name)
            if isinstance(w, tk.Widget):
                return w
            # Fallback to the editor frame if field isn't mounted yet
            return self._find_target("object_editor_frame")
        if hasattr(self.ui, target_id):
            attr = getattr(self.ui, target_id)
            if isinstance(attr, tk.Widget):
                return attr
        # Search widget tree by tutorial_id
        return self._search_by_tutorial_id(self.root, target_id)

    def _search_by_tutorial_id(self, root, target_id):
        try:
            if not root or not root.winfo_exists():
                return None
            if getattr(root, "tutorial_id", None) == target_id:
                return root
            for child in root.winfo_children():
                res = self._search_by_tutorial_id(child, target_id)
                if res:
                    return res
        except Exception:
            pass
        return None

    def _cleanup_highlight(self):
        if self.highlight:
            try:
                self.highlight.destroy()
            except Exception:
                pass
            self.highlight = None

    def next_step(self):
        self.current_idx += 1
        self.show_step()

    def prev_step(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.show_step()

    def finish_tutorial(self):
        self._cleanup()
        if self.use_sandbox:
            SandboxManager().exit_sandbox(self.ui)
        if hasattr(self.ui, "show_toast"):
            try:
                self.ui.show_toast(f"✓ Completed: {self.tutorial_name}", "success")
            except Exception:
                pass
        if self.on_complete:
            try:
                self.on_complete()
            except Exception:
                pass

    def exit_tutorial(self):
        self._cleanup()
        if self.use_sandbox:
            SandboxManager().exit_sandbox(self.ui)

    def _cleanup(self):
        if TutorialRunner._active_instance is self:
            TutorialRunner._active_instance = None
        if self.use_sandbox and SandboxManager()._active_runner is self:
            SandboxManager()._active_runner = None
        self._cleanup_highlight()
        if self._poll_job:
            try:
                self.root.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        if self.hud_win:
            try:
                self.hud_win.destroy()
            except Exception:
                pass
            self.hud_win = None
