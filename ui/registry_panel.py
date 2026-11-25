import difflib
import tkinter as tk
from tkinter import ttk
import pandas as pd
from utils import debug_error
from ui.state import app_bus, PROBLEM_STATE_CHANGED


def _bind_icedig_context_menu(ui, widget, field_name):
    """Bind right-click ICEDIG status menu to a registration Entry widget."""
    from ui.context_menu import ContextMenuManager
    import config
    def _build_menu(event):
        current_val = ui.reg_vars.get(field_name, tk.StringVar()).get().strip().lower()
        items = []
        # Submenu items — one per ICEDIG code
        submenu_items = []
        for code, label in config.ICEDIG_CODE_LABELS.items():
            _code = code  # closure capture
            submenu_items.append({
                "label": label,
                "command": lambda c=_code: _apply_icedig_code(ui, field_name, c),
                "state": "normal" if current_val != _code else "disabled",
            })
        items.append({
            "label": "Set ICEDIG status",
            "submenu": submenu_items,
            "state": "normal",
        })
        if current_val in config.ALL_UNKNOWN_TOKENS or current_val:
            items.append({"separator": True})
            items.append({
                "label": "Clear Field Value",
                "command": lambda: _apply_icedig_code(ui, field_name, ""),
                "state": "normal",
            })
        return items
    widget._icedig_menu_builder = _build_menu
    ContextMenuManager.bind(widget, _build_menu)

def _bind_icedig_shortcuts(ui, widget, field_name):
    """Bind shorthand expansion (?m, ?i, ?u, ?w) and Ctrl+Shift hotkeys to a registration Entry widget."""
    shorthands = {
        "?m": "unknown:missing",
        "?missing": "unknown:missing",
        "?i": "unknown:indecipherable",
        "?illegible": "unknown:indecipherable",
        "?u": "unknown:undigitized",
        "?undigitized": "unknown:undigitized",
        "?w": "withheld",
        "?withheld": "withheld",
        "??": "unknown",
        "?unk": "unknown",
    }

    def _check_shorthand(event=None):
        var = ui.reg_vars.get(field_name)
        val = var.get().strip().lower() if var else ""
        if not val and hasattr(widget, "get"):
            try:
                val = widget.get().strip().lower()
            except Exception:
                pass
        if val in shorthands:
            _apply_icedig_code(ui, field_name, shorthands[val])

    widget.bind("<KeyRelease>", _check_shorthand, add="+")
    widget.bind("<FocusOut>", _check_shorthand, add="+")
    widget._check_shorthand = _check_shorthand

    widget.bind("<Control-Shift-M>", lambda e: (_apply_icedig_code(ui, field_name, "unknown:missing"), "break")[1])
    widget.bind("<Control-Shift-m>", lambda e: (_apply_icedig_code(ui, field_name, "unknown:missing"), "break")[1])
    widget.bind("<Control-Shift-I>", lambda e: (_apply_icedig_code(ui, field_name, "unknown:indecipherable"), "break")[1])
    widget.bind("<Control-Shift-i>", lambda e: (_apply_icedig_code(ui, field_name, "unknown:indecipherable"), "break")[1])
    widget.bind("<Control-Shift-U>", lambda e: (_apply_icedig_code(ui, field_name, "unknown:undigitized"), "break")[1])
    widget.bind("<Control-Shift-u>", lambda e: (_apply_icedig_code(ui, field_name, "unknown:undigitized"), "break")[1])
    widget.bind("<Control-Shift-W>", lambda e: (_apply_icedig_code(ui, field_name, "withheld"), "break")[1])
    widget.bind("<Control-Shift-w>", lambda e: (_apply_icedig_code(ui, field_name, "withheld"), "break")[1])
    widget.bind("<Control-Shift-BackSpace>", lambda e: (_apply_icedig_code(ui, field_name, ""), "break")[1])

def _apply_icedig_code(ui, field_name, code):
    """Write a canonical ICEDIG code (or empty string) into a registration field, clear its mapped problem flag, and commit."""
    import config
    var = ui.reg_vars.get(field_name)
    if var is None:
        return
    var.set(code)

    # Setting a precision ICEDIG code resolves that field's missing-field problem flag
    cleared_cols = []
    warned_conflict = False
    if code and code.lower() in config.ICEDIG_UNKNOWN_CODES:
        for p_col, mapped_field in getattr(ui, "problem_to_field", {}).items():
            if mapped_field == field_name and p_col in getattr(ui, "problem_vars", {}):
                try:
                    if ui.problem_vars[p_col].get():
                        ui.problem_vars[p_col].set(False)
                        cleared_cols.append(p_col)
                except Exception:
                    pass
        # Gentle reminder if historical books have a conflicting value for this field
        if code.lower() == "unknown:missing":
            sugg = getattr(ui, "current_object_suggestions", None) or {}
            if sugg.get(field_name) and hasattr(ui, "show_toast"):
                warned_conflict = True
                ui.show_toast(
                    f"Heads up: historical ledgers have a value for {field_name} — press Ctrl+H to compare.",
                    "warning",
                    duration_ms=4500,
                )

    _prev_sup = getattr(ui, "_suppress_auto_clear_toasts", 0)
    _prev_sup = _prev_sup if isinstance(_prev_sup, int) else 0
    ui._suppress_auto_clear_toasts = _prev_sup + 1
    try:
        ui.commit_current_object()
    finally:
        ui._suppress_auto_clear_toasts = _prev_sup

    if cleared_cols and not warned_conflict and hasattr(ui, "notify_auto_cleared_flags"):
        ui.notify_auto_cleared_flags(cleared_cols, source="ICEDIG")
    # Refresh the field background and per-field ICEDIG trigger immediately
    from ui.registry_panel import RegistryPanel
    RegistryPanel.refresh_field_background(ui, field_name)


def _open_field_icedig_menu(ui, field_name, anchor_widget):
    """Open a clean, config-driven ICEDIG status menu scoped strictly to one Registration field."""
    import config
    current_val = ui.reg_vars.get(field_name, tk.StringVar()).get().strip().lower()
    menu = tk.Menu(ui.root, tearoff=0)
    menu.add_command(label=f"ICEDIG status — {field_name}", state="disabled")
    menu.add_separator()
    for item in config.ICEDIG_CODES:
        code = item["code"]
        desc = item["description"]
        shortcut = item.get("shortcut", "")
        is_active = (current_val == code.lower())
        prefix = "✓ " if is_active else "   "
        label = f"{prefix}{code}  ({desc})"
        menu.add_command(
            label=label,
            accelerator=shortcut,
            command=lambda f=field_name, c=code: _apply_icedig_code(ui, f, c),
        )
    if current_val:
        menu.add_separator()
        menu.add_command(
            label="Clear field value",
            accelerator="Ctrl+Shift+Backspace",
            command=lambda f=field_name: _apply_icedig_code(ui, f, ""),
        )
    try:
        x = anchor_widget.winfo_rootx()
        y = anchor_widget.winfo_rooty() + anchor_widget.winfo_height()
        menu.tk_popup(x, y)
    finally:
        menu.grab_release()


class RegistryPanel:
    """Manager and builder for the Specimen Registration cards and fields form."""

    @staticmethod
    def build_sections(ui):
        """Construct the Registration form cards, fields, problems tab, and location wiring."""
        from config import sc
        import config

        ui._rebuild_focus_registration_menu()

        # Initialize problem vars first so they are available for inline problem checkboxes
        ui.problem_vars.clear()
        ui.problem_checkbuttons = []
        for field in ui.app.config["ui_sections"]["problems"]:
            name = field["name"]
            var = tk.BooleanVar()
            ui.problem_vars[name] = var
            var.trace_add("write", lambda *_, n=name: (
                ui.update_problems_default_view(),
                app_bus.publish(PROBLEM_STATE_CHANGED, {"field": n, "value": ui.problem_vars.get(n, tk.BooleanVar()).get()})
            ))

        if not hasattr(ui, "images_missing_var"):
            ui.images_missing_var = tk.StringVar()

        # -------- REG --------
        if hasattr(ui, "reg_notebook") and ui.reg_notebook.winfo_exists():
            for tab in ui.reg_notebook.tabs():
                ui.reg_notebook.forget(tab)

        ui.reg_vars.clear()
        ui.reg_entries.clear()
        ui.reg_row_frames.clear()
        ui.reg_entry_list = []
        ui.unval_btns = {}
        ui.unval_comment_frames = {}
        ui.unval_comment_vars = {}
        ui.icedig_field_btns = {}
        ui._registry_theme_widgets = {
            "canvases": [],
            "card_frames": [],
            "header_frames": [],
            "header_lbls": [],
            "badge_lbls": [],
            "body_frames": [],
            "row_frames": [],
            "field_lbls": [],
            "spec_bars": [],
            "spec_cbs": [],
            "spec_subtitles": [],
            "tag_rows": [],
            "tag_pills": [],
            "hint_lbls": [],
            "comment_boxes": [],
        }

        ui.no_problems_msg_label = ttk.Label(
            ui.reg_data_frame,
            text="No active problems for this specimen. Focus Mode is hiding clean fields.",
            foreground="#2b8a3e",
            font=("Segoe UI", sc(10), "italic"),
            anchor="center"
        )

        def _exit_focus_mode_from_empty():
            if hasattr(ui, "focus_mode_var"):
                ui.focus_mode_var.set(False)
            RegistryPanel.update_reg_fields_visibility(ui, skip_snap=True)

        ui.focus_show_all_btn = tk.Button(
            ui.reg_data_frame,
            text="Show All Fields",
            font=("Inter", sc(9), "bold"),
            bg="#eaf5ec",
            fg="#1b5e20",
            activebackground="#d4ecd9",
            relief="flat",
            highlightbackground="#3a7d44",
            highlightthickness=1,
            padx=sc(12),
            pady=sc(4),
            cursor="hand2",
            command=_exit_focus_mode_from_empty,
        )

        # Build reverse map for inline problem checkboxes
        field_to_problem = {v: k for k, v in ui.problem_to_field.items()}
        ui.prob_border_bars.clear()
        ui.prob_label_widgets.clear()

        # Build single Specimen Audit tab with cards
        all_fields = [f["name"] for f in ui.app.config["ui_sections"]["registration"]]
        ui._reg_tabs = {}

        # Define cards with themes, header icons and ordered fields
        card_defs = [
            {
                "id": "taxonomy",
                "title": "Taxonomy & Scientific Name",
                "icon": "🧬",
                "fields": ["Genus", "Species", "Author", "Family", "Higher Classification"]
            },
            {
                "id": "collection",
                "title": "Collection & Specimen Metadata",
                "icon": "📦",
                "fields": ["Collector", "Innsammling Nr.", "Collection Date", "Collection Place", "Variant", "(N) Plant Part", "Plant Part", "Box Label", "Conservation Status", "Online photo 1", "Online photo 2", "Online photo 3", "UID"]
            },
            {
                "id": "notes",
                "title": "Audit Notes & Descriptions",
                "icon": "📝",
                "fields": ["Comment", "Observation", "ProblemDescription"]
            }
        ]

        # Safeguard: Append any other registration fields in config not explicitly assigned to any card
        assigned_fields = set()
        for c in card_defs:
            assigned_fields.update(c["fields"])
        unassigned_fields = [f for f in all_fields if f not in assigned_fields]
        if unassigned_fields:
            card_defs[1]["fields"].extend(unassigned_fields)

        ui.card_defs_ordered = [c["id"] for c in card_defs]
        ui.card_frames = {}

        is_dark = getattr(ui, "dark_mode_active", False)
        canvas_bg = "#181c19" if is_dark else "#fbfaf8"
        card_bg = "#212622" if is_dark else "#ffffff"
        header_bg = "#262c28" if is_dark else "#f5f5f5"
        border_color = "#333a35" if is_dark else "#e2e2e2"
        fg_color = "#e8ebe9" if is_dark else "#2c302e"

        # Create a single tab container for Specimen Audit
        tab_container = ttk.Frame(ui.reg_notebook)

        # Scrollable canvas inside the tab container
        tab_canvas = tk.Canvas(tab_container, highlightthickness=0, bg=canvas_bg)
        ui._registry_theme_widgets["canvases"].append(tab_canvas)
        tab_scroll = ttk.Scrollbar(tab_container, orient="vertical", command=tab_canvas.yview)
        tab_frame = ttk.Frame(tab_canvas, style="RightPane.TFrame")

        tab_frame.bind(
            "<Configure>",
            lambda e, tc=tab_canvas: tc.configure(scrollregion=tc.bbox("all"))
        )
        tab_win_id = tab_canvas.create_window((0, 0), window=tab_frame, anchor="nw")
        tab_canvas.configure(yscrollcommand=tab_scroll.set)
        tab_canvas.bind(
            "<Configure>",
            lambda e, tc=tab_canvas, twid=tab_win_id: tc.itemconfig(twid, width=e.width) if getattr(tc, "_last_width", None) != e.width and not setattr(tc, "_last_width", e.width) else None
        )

        def _make_mousewheel_scroller(canvas):
            return lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        mw_scroller = _make_mousewheel_scroller(tab_canvas)
        tab_canvas.bind("<MouseWheel>", mw_scroller)
        tab_frame.bind("<MouseWheel>", mw_scroller)

        tab_canvas.pack(side="left", fill="both", expand=True)
        tab_scroll.pack(side="right", fill="y")

        ui._reg_tabs["General Data"] = {
            "container": tab_container,
            "canvas": tab_canvas,
            "frame": tab_frame,
            "fields": all_fields
        }

        ui.reg_notebook.add(tab_container, text="General Data")

        # Create O(1) lookup dictionary for registration config
        reg_config_dict = {f["name"]: f for f in ui.app.config.get("ui_sections", {}).get("registration", [])}

        # Generate collapsible accordion card layout inside the tab frame
        for c in card_defs:
            card_id = c["id"]
            card_title = c["title"]
            icon = c["icon"]
            fields_to_render = c["fields"]

            # Card frame (outer container with 1px border)
            card_frame = tk.Frame(tab_frame, bg=card_bg, highlightthickness=1, highlightbackground=border_color, bd=0)
            card_frame.pack(fill="x", padx=sc(10), pady=sc(6))
            ui._registry_theme_widgets["card_frames"].append(card_frame)

            # Header panel (interactive accordion trigger)
            header_frame = tk.Frame(card_frame, bg=header_bg, padx=sc(8), pady=sc(6), cursor="hand2")
            header_frame.pack(fill="x")
            ui._registry_theme_widgets["header_frames"].append(header_frame)

            toggle_lbl = tk.Label(
                header_frame, text="▼",
                font=("Inter", sc(9), "bold"),
                bg=header_bg, fg=fg_color, cursor="hand2"
            )
            toggle_lbl.pack(side="left", padx=(sc(2), sc(4)))

            icon_lbl = tk.Label(header_frame, text=icon, font=("Segoe UI Symbol", sc(11)), bg=header_bg, fg=fg_color, cursor="hand2")
            icon_lbl.pack(side="left", padx=(0, sc(6)))

            title_lbl = tk.Label(header_frame, text=card_title, font=("Inter", sc(10), "bold"), bg=header_bg, fg=fg_color, cursor="hand2")
            title_lbl.pack(side="left")
            ui._registry_theme_widgets["header_lbls"].extend([toggle_lbl, icon_lbl, title_lbl])

            # Problem count badge inside card header
            badge_lbl = tk.Label(
                header_frame, text="",
                font=("JetBrains Mono", sc(8), "bold"),
                bg=header_bg, fg="#c93a40"
            )
            badge_lbl.pack(side="left", padx=(sc(8), 0))
            ui._registry_theme_widgets["badge_lbls"].append(badge_lbl)

            if card_id == "taxonomy":
                prefs = config.load_prefs()
                show_gbif = prefs.get("enable_gbif", False)

                ui.gbif_btn = tk.Label(header_frame, text="🔍 Check GBIF", font=("Inter", sc(8), "bold"), bg="#2b8a3e", fg="#ffffff", cursor="hand2", padx=sc(6), pady=sc(2))
                if show_gbif:
                    ui.gbif_btn.pack(side="right", padx=sc(6))
                ui.gbif_btn.bind("<Button-1>", lambda e: ui.check_gbif_action())
                ui.gbif_btn.bind("<Enter>", lambda e, w=ui.gbif_btn: w.config(bg="#3bc954"))
                ui.gbif_btn.bind("<Leave>", lambda e, w=ui.gbif_btn: w.config(bg="#2b8a3e"))

            # Card content area
            body_frame = tk.Frame(card_frame, bg=card_bg, padx=sc(10), pady=sc(8))
            body_frame.pack(fill="x")
            body_frame.columnconfigure(0, weight=1)
            ui._registry_theme_widgets["body_frames"].append(body_frame)

            def _make_toggle_handler(b_frame, t_lbl, tc):
                def _handler(event=None):
                    if b_frame.winfo_manager():
                        b_frame.pack_forget()
                        t_lbl.config(text="▶")
                    else:
                        b_frame.pack(fill="x")
                        t_lbl.config(text="▼")
                    tc.configure(scrollregion=tc.bbox("all"))
                return _handler

            toggle_cmd = _make_toggle_handler(body_frame, toggle_lbl, tab_canvas)
            for w in (header_frame, toggle_lbl, icon_lbl, title_lbl):
                w.bind("<Button-1>", toggle_cmd)

            ui.card_frames[card_id] = {
                "frame": card_frame,
                "body": body_frame,
                "toggle_lbl": toggle_lbl,
                "badge_lbl": badge_lbl,
                "fields": fields_to_render
            }

            current_row = 0
            for fname in fields_to_render:
                field = reg_config_dict.get(fname)
                if not field:
                    continue

                name = field["name"]
                ftype = field.get("type", "text")
                var = tk.StringVar()
                ui.reg_vars[name] = var

                # Single individual field row
                frame = tk.Frame(body_frame, bg=card_bg)
                ui.reg_row_frames[name] = frame

                # Col 0: border bar + optional problem checkbox
                col0_frame = tk.Frame(frame, bg=card_bg)
                col0_frame.grid(row=0, column=0, sticky="nsw", padx=(2, 2))
                ui._registry_theme_widgets["row_frames"].extend([frame, col0_frame])

                prob_col = field_to_problem.get(name)
                if prob_col:
                    prob_var = ui.problem_vars[prob_col]

                    border_bar = tk.Frame(col0_frame, width=3, bd=0, highlightthickness=0)
                    border_bar.pack(side="left", fill="y", padx=(0, 2))
                    ui.prob_border_bars[name] = border_bar

                    cb = ttk.Checkbutton(
                        col0_frame, text="", variable=prob_var, cursor="hand2",
                        command=lambda n=name, pc=prob_col: (
                            ui._update_problem_row_style(n, ui.problem_vars[pc].get()),
                            ui.commit_current_object()
                        )
                    )
                    cb.pack(side="left")
                    cb.tutorial_id = f"inline_prob_{prob_col}"
                    if not hasattr(ui, "inline_problem_checkbuttons") or ui.inline_problem_checkbuttons is None:
                        ui.inline_problem_checkbuttons = {}
                    ui.inline_problem_checkbuttons[prob_col] = cb
                    ui.add_tooltip(cb, f"Flag as having a problem ({prob_col.replace('_', ' ')}). Tab + Space to toggle.")

                    prob_var.trace_add(
                        "write",
                        lambda *_, n=name, pc=prob_col: ui.root.after_idle(
                            lambda: ui._update_problem_row_style(n, ui.problem_vars[pc].get())
                        )
                    )
                else:
                    bar_spacer = tk.Frame(col0_frame, width=3, bd=0, highlightthickness=0, bg=card_bg)
                    bar_spacer.pack(side="left", fill="y", padx=(0, 2))
                    spacer_lbl = tk.Frame(col0_frame, width=16, bg=card_bg)
                    spacer_lbl.pack(side="left")
                    ui._registry_theme_widgets["row_frames"].extend([bar_spacer, spacer_lbl])

                # Col 1: Label with bold clean typography + helpful inline field tooltips
                _display_names = {
                    "Observation": "Observation (Legacy)",
                    "ProblemDescription": "Problem Note (Legacy)",
                    "Problem Description": "Problem Note (Legacy)",
                }
                lbl_text = _display_names.get(name, name)
                is_legacy_lbl = name in _display_names
                lbl_fg = ("#9399b2" if is_dark else "#757d77") if is_legacy_lbl else fg_color
                lbl = tk.Label(frame, text=lbl_text, width=18 if is_legacy_lbl else 15, anchor="w", font=("Inter", sc(9 if is_legacy_lbl else 10), "bold"), bg=card_bg, fg=lbl_fg)
                lbl.grid(row=0, column=1, sticky="w", padx=(0, 6))
                ui._registry_theme_widgets["field_lbls"].append((lbl, is_legacy_lbl))
                _field_tips = {
                    "Genus": "First word of the scientific name. Type what is printed on the box — outdated or synonym names can be updated later with 🔍 Check GBIF.",
                    "Species": "Second word of the scientific name. Type what is printed on the box — outdated or synonym names can be updated later with 🔍 Check GBIF.",
                    "Author": "Scientist who originally named the plant (e.g. L.) — NOT the person who collected it (use Collector for that).",
                    "Comment": "General notes, physical condition remarks, or messages for the next curator — synced with Mobile Companion.",
                    "Observation": "Legacy note from an older record — still saved safely. You can optionally combine legacy notes into Comment anytime from TOOLS ▾.",
                    "ProblemDescription": "Legacy problem note from an older record — still saved safely. You can optionally combine legacy notes into Comment anytime from TOOLS ▾.",
                }
                if name in _field_tips and hasattr(ui, "add_tooltip"):
                    ui.add_tooltip(lbl, _field_tips[name])
                if prob_col:
                    ui.prob_label_widgets[name] = lbl

                # Col 2: input widget based on type
                if ftype == "choice":
                    choices = field.get("choices", [])
                    if "" not in choices:
                        choices = [""] + choices
                    widget = ttk.Combobox(frame, textvariable=var, values=choices, cursor="hand2")
                    widget.bind("<<ComboboxSelected>>", lambda e: ui.commit_current_object())
                elif ftype == "checkbox":
                    widget = ttk.Checkbutton(
                        frame, cursor="hand2",
                        text="",
                        variable=var,
                        onvalue="True",
                        offvalue="False",
                        command=lambda n=name, v=var: ui._on_checkbox_change(n, v)
                    )
                elif ftype == "multiline" or name in ("Conservation Status", "Observation", "Comment", "ProblemDescription", "Problem Description"):
                    if name == "Comment":
                        from ui.widgets import FlowWrapFrame
                        comment_box = tk.Frame(frame, bg=card_bg)
                        ui._registry_theme_widgets["comment_boxes"].append(comment_box)
                        # Synced "Needs Specialist" escalation bar + strictly non-ICEDIG physical/specialist quick tags
                        spec_var = ui.problem_vars.get("Other_problem")
                        if spec_var is None:
                            spec_var = tk.BooleanVar(value=False)
                            ui.problem_vars["Other_problem"] = spec_var

                        spec_bg = "#222c34" if is_dark else "#eef2f5"
                        spec_fg = "#a5bfd1" if is_dark else "#355566"
                        spec_border = "#3a4f5e" if is_dark else "#c6d4de"

                        spec_bar = tk.Frame(
                            comment_box, bg=spec_bg,
                            highlightthickness=1, highlightbackground=spec_border,
                            padx=sc(6), pady=sc(3)
                        )
                        spec_bar.pack(fill="x", side="top", pady=(0, sc(3)))
                        ui._registry_theme_widgets["spec_bars"].append(spec_bar)

                        hint_lbl = tk.Label(
                            comment_box,
                            text="Add a short note for the specialist — for blank or unreadable label fields, use the field's ICEDIG menu (⋯).",
                            font=("Inter", sc(8), "italic"),
                            bg=card_bg,
                            fg="#d9a036" if is_dark else "#9a6700",
                            anchor="w",
                            wraplength=sc(320),
                            justify="left"
                        )
                        ui._specialist_comment_hint_lbl = hint_lbl
                        ui._registry_theme_widgets["hint_lbls"].append(hint_lbl)

                        widget = tk.Text(
                            comment_box, height=3,
                            relief="flat", bd=0,
                            highlightthickness=1, highlightbackground=border_color,
                            highlightcolor="#3a7d44" if not is_dark else "#a6e3a1",
                            insertbackground="#2c302e" if not is_dark else "#e8ebe9",
                            bg="#ffffff" if not is_dark else "#212622",
                            fg="#2c302e" if not is_dark else "#e8ebe9",
                            font=("Inter", sc(10)),
                            undo=True, maxundo=-1, autoseparators=True
                        )

                        def _sync_specialist_hint(focus_if_empty=False, _w=widget, _v=spec_var, _h=hint_lbl):
                            try:
                                flagged = bool(_v.get())
                                txt = _w.get("1.0", "end-1c").strip()
                                if flagged and not txt:
                                    if _h.winfo_manager() != "pack":
                                        _h.pack(fill="x", side="top", pady=(0, sc(3)), before=_w)
                                    if focus_if_empty:
                                        _w.focus_set()
                                else:
                                    if _h.winfo_manager() == "pack":
                                        _h.pack_forget()
                            except Exception:
                                pass

                        ui._sync_specialist_comment_hint = _sync_specialist_hint

                        def _on_spec_toggle(_sync=_sync_specialist_hint):
                            RegistryPanel.update_reg_fields_visibility(ui, skip_snap=True)
                            ui.commit_current_object()
                            _sync(focus_if_empty=True)

                        spec_cb = tk.Checkbutton(
                            spec_bar,
                            text="Needs Specialist",
                            variable=spec_var,
                            font=("Inter", sc(9), "bold"),
                            bg=spec_bg, fg=spec_fg,
                            activebackground=spec_bg, activeforeground=spec_fg,
                            selectcolor="#1d2d35" if is_dark else "#ffffff",
                            relief="flat", bd=0, highlightthickness=0,
                            cursor="hand2",
                            command=_on_spec_toggle
                        )
                        spec_cb.pack(side="left")
                        ui.comment_specialist_cb = spec_cb
                        ui._registry_theme_widgets["spec_cbs"].append(spec_cb)
                        if hasattr(ui, "add_tooltip"):
                            ui.add_tooltip(
                                spec_cb,
                                "Escalate physical damage, mold/pest, mixed specimens, or archival deadlocks to a specialist (triggers NOTE / REV+NOTE; stays out of the default trainee queue)."
                            )

                        # Responsive wrapping quick-tag pills driven by config.SPECIALIST_QUICK_TAGS
                        tag_row = FlowWrapFrame(comment_box, bg=card_bg, hgap=sc(4), vgap=sc(3))
                        tag_row.pack(fill="x", side="top", pady=(0, sc(2)))
                        ui._registry_theme_widgets["tag_rows"].append(tag_row)

                        def _append_specialist_tag(tag_text, _w=widget, _v=spec_var, _sync=_sync_specialist_hint):
                            try:
                                existing = _w.get("1.0", "end-1c").strip()
                                if tag_text.lower() not in existing.lower():
                                    sep = "; " if existing else ""
                                    _w.delete("1.0", "end")
                                    _w.insert("1.0", f"{existing}{sep}{tag_text}")
                                _v.set(True)
                                RegistryPanel.update_reg_fields_visibility(ui, skip_snap=True)
                                ui.commit_current_object()
                                _sync(focus_if_empty=False)
                            except Exception:
                                pass

                        quick_tags = getattr(config, "SPECIALIST_QUICK_TAGS", []) or []
                        for _tag in quick_tags:
                            _lbl = _tag.get("label", "") if isinstance(_tag, dict) else str(_tag)
                            _val = _tag.get("text", _lbl.lstrip("+ ").strip()) if isinstance(_tag, dict) else str(_tag)
                            if not _lbl:
                                continue
                            _pill = tk.Button(
                                tag_row, text=_lbl,
                                font=("Inter", sc(8)),
                                bg=spec_bg, fg=spec_fg,
                                activebackground=spec_border, activeforeground=spec_fg,
                                relief="flat", bd=0,
                                highlightthickness=1, highlightbackground=spec_border,
                                padx=sc(5), pady=sc(1), cursor="hand2",
                                command=lambda t=_val: _append_specialist_tag(t)
                            )
                            tag_row.add_item(_pill)
                            ui._registry_theme_widgets["tag_pills"].append(_pill)

                        widget.pack(fill="x", expand=True)

                        def bind_text_events(w, _sync=_sync_specialist_hint):
                            w.bind("<KeyRelease>", lambda e: (ui._on_text_change(e), _sync(False)))
                            w.bind("<FocusOut>", lambda e: (ui.commit_current_object(), _sync(False)), add="+")

                        bind_text_events(widget)
                        try:
                            spec_var.trace_add("write", lambda *_: _sync_specialist_hint(False))
                        except Exception:
                            pass
                        comment_box_widget = comment_box
                    else:
                        comment_box_widget = None
                        widget = tk.Text(
                            frame, height=3,
                            relief="flat", bd=0,
                            highlightthickness=1, highlightbackground=border_color,
                            highlightcolor="#3a7d44" if not is_dark else "#a6e3a1",
                            insertbackground="#2c302e" if not is_dark else "#e8ebe9",
                            bg="#ffffff" if not is_dark else "#212622",
                            fg="#2c302e" if not is_dark else "#e8ebe9",
                            font=("Inter", sc(10)),
                            undo=True, maxundo=-1, autoseparators=True
                        )

                        def bind_text_events(w):
                            w.bind("<KeyRelease>", ui._on_text_change)
                            w.bind("<FocusOut>", lambda e: ui.commit_current_object(), add="+")

                        bind_text_events(widget)
                else:
                    entry_container = tk.Frame(frame, bg=card_bg)
                    field_font = ("JetBrains Mono", sc(10)) if name in ("Collection Date", "Innsammling Nr.", "Year", "Month", "Day", "ObjectID") else ("Inter", sc(10))
                    widget = tk.Entry(
                        entry_container, textvariable=var,
                        relief="flat", bd=0,
                        highlightthickness=1, highlightbackground=border_color,
                        highlightcolor="#3a7d44" if not is_dark else "#a6e3a1",
                        insertbackground="#2c302e" if not is_dark else "#e8ebe9",
                        bg="#ffffff" if not is_dark else "#212622",
                        fg="#2c302e" if not is_dark else "#e8ebe9",
                        font=field_font
                    )
                    widget.pack(fill="x", expand=True, ipady=sc(3))

                    focus_line = tk.Frame(entry_container, height=sc(2), bg=card_bg)
                    focus_line.pack(fill="x", side="bottom")
                    ui._registry_theme_widgets["row_frames"].extend([entry_container, focus_line])

                    def make_focus_handlers(w, fl, ec, default_bg, field_key=name):
                        def on_focus_in(e):
                            dark = getattr(ui, "dark_mode_active", False)
                            fl.configure(bg="#a6e3a1" if dark else "#3a7d44")
                            ui._last_focused_reg_field = field_key

                        def on_focus_out(e):
                            dark = getattr(ui, "dark_mode_active", False)
                            fl.configure(bg="#212622" if dark else "#ffffff")

                        w.bind("<FocusIn>", on_focus_in, add="+")
                        w.bind("<FocusOut>", on_focus_out, add="+")

                    make_focus_handlers(widget, focus_line, entry_container, card_bg)

                    widget.bind("<KeyRelease>", lambda e, n=name, w=widget: RegistryPanel.on_autocomplete_key(ui, e, n, w), add="+")
                    widget.bind("<KeyRelease>", lambda e: ui.root.after(500, lambda: RegistryPanel.validate_fields(ui)), add="+")
                    widget.bind("<FocusOut>", lambda e, n=name, w=widget: RegistryPanel.run_fuzzy_match(ui, n, w), add="+")
                    widget.bind("<FocusOut>", lambda e: ui.commit_current_object(), add="+")

                    if field.get("readonly"):
                        widget.configure(state="disabled")

                if ftype not in ("multiline", "checkbox", "choice") and not field.get("readonly"):
                    _bind_icedig_context_menu(ui, widget, name)
                    _bind_icedig_shortcuts(ui, widget, name)

                ui.reg_entries[name] = widget
                ui.reg_entry_list.append(widget)

                if ftype == "multiline" or name in ("Conservation Status", "Observation", "Comment", "ProblemDescription", "Problem Description"):
                    if name == "Comment" and locals().get("comment_box_widget") is not None:
                        comment_box_widget.grid(row=0, column=2, sticky="ew", pady=sc(2))
                    else:
                        widget.grid(row=0, column=2, sticky="ew", pady=sc(2))
                elif ftype in ("choice", "checkbox"):
                    widget.grid(row=0, column=2, sticky="ew")
                else:
                    entry_container.grid(row=0, column=2, sticky="ew")

                # Quiet per-field ICEDIG status trigger (⋯) in Column 3 for editable text fields
                if ftype not in ("multiline", "checkbox", "choice") and not field.get("readonly"):
                    icedig_btn = tk.Button(
                        frame, text="⋯",
                        font=("JetBrains Mono", sc(9), "bold"),
                        bg=card_bg, fg="#8b948d",
                        activebackground="#2a322c" if is_dark else "#e9ece5",
                        activeforeground=fg_color,
                        relief="flat", bd=0, highlightthickness=0,
                        cursor="hand2", padx=sc(6), pady=sc(1),
                    )
                    icedig_btn.configure(command=lambda n=name, b=icedig_btn: _open_field_icedig_menu(ui, n, b))
                    icedig_btn.grid(row=0, column=3, padx=(sc(3), sc(1)), sticky="e")
                    ui.icedig_field_btns[name] = icedig_btn
                    if name == "Collection Date":
                        icedig_btn.tutorial_id = "icedig_field_btn"
                    elif name == "Collector":
                        icedig_btn.tutorial_id = "icedig_collector_btn"
                    if hasattr(ui, "add_tooltip"):
                        ui.add_tooltip(
                            icedig_btn,
                            f"Set ICEDIG code for {name} (unknown:missing, unknown:indecipherable, unknown:undigitized, withheld). Shortcuts: Ctrl+Shift+M / I / U / W."
                        )

                widget.bind("<Shift-Up>", ui._reg_nav_up)
                widget.bind("<Shift-Down>", ui._reg_nav_down)
                widget.bind("<Control-Up>", ui._reg_nav_up)
                widget.bind("<Control-Down>", ui._reg_nav_down)
                if ftype != "multiline":
                    widget.bind("<Return>", ui._reg_nav_down)

                frame.columnconfigure(0, minsize=sc(28), weight=0)
                frame.columnconfigure(1, minsize=sc(120), weight=0)
                frame.columnconfigure(2, weight=1)
                frame.columnconfigure(3, weight=0)

                frame.grid(row=current_row, column=0, sticky="ew", pady=4)
                current_row += 1

        # -------- PROBLEMS TAB --------
        tab_container = ttk.Frame(ui.reg_notebook)
        tab_canvas = tk.Canvas(tab_container, highlightthickness=0)
        tab_scroll = ttk.Scrollbar(tab_container, orient="vertical", command=tab_canvas.yview)
        tab_frame = ttk.Frame(tab_canvas)

        tab_frame.bind(
            "<Configure>",
            lambda e, tc=tab_canvas: tc.configure(scrollregion=tc.bbox("all"))
        )
        tab_win_id = tab_canvas.create_window((0, 0), window=tab_frame, anchor="nw")
        tab_canvas.configure(yscrollcommand=tab_scroll.set)
        tab_canvas.bind(
            "<Configure>",
            lambda e, tc=tab_canvas, twid=tab_win_id: tc.itemconfig(twid, width=e.width) if getattr(tc, "_last_width", None) != e.width and not setattr(tc, "_last_width", e.width) else None
        )

        tab_canvas.pack(side="left", fill="both", expand=True)
        tab_scroll.pack(side="right", fill="y")

        ui.reg_notebook.add(tab_container, text="Problems")
        ui._reg_tabs["Problems"] = {
            "container": tab_container,
            "canvas": tab_canvas,
            "frame": tab_frame,
            "fields": []
        }

        edit_frame = ttk.Frame(tab_frame, padding=12)
        edit_frame.pack(fill="x")

        def _humanize_problem_label(col_name: str) -> str:
            import re
            clean = re.sub(r"[_ ]?[Pp]roblem$", "", str(col_name or "")).replace("_", " ").strip()
            clean = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", clean)
            if not clean or clean.lower() == "other":
                return "Needs Specialist"
            return f"{clean} Issue"

        ui.problem_checkbuttons = []
        ui.problem_checkbutton_map = {}
        data_problem_fields = []
        specialist_problem_field = None
        for field in ui.app.config["ui_sections"]["problems"]:
            if field["name"] == "Other_problem":
                specialist_problem_field = field
            else:
                data_problem_fields.append(field)

        for i, field in enumerate(data_problem_fields):
            name = field["name"]
            var = ui.problem_vars.get(name)
            if not var:
                var = tk.BooleanVar()
                ui.problem_vars[name] = var

            cb = ttk.Checkbutton(
                edit_frame, cursor="hand2",
                text=_humanize_problem_label(name),
                variable=var,
                command=lambda: (
                    RegistryPanel.update_reg_fields_visibility(ui, skip_snap=True),
                    ui.commit_current_object()
                )
            )
            row = i // 2
            col = i % 2
            cb.grid(row=row, column=col, sticky="w", padx=10, pady=6)
            ui.problem_checkbuttons.append(cb)
            ui.problem_checkbutton_map[name] = cb

        edit_frame.columnconfigure(0, weight=1)
        edit_frame.columnconfigure(1, weight=1)

        # Visually distinct Tier-2 Specialist Escalation strip (separated from desk data errors)
        if specialist_problem_field is not None:
            name = specialist_problem_field["name"]
            var = ui.problem_vars.get(name)
            if not var:
                var = tk.BooleanVar()
                ui.problem_vars[name] = var

            is_dark_tab = getattr(ui, "dark_mode_active", False)
            spec_bg = "#222c34" if is_dark_tab else "#eef2f5"
            spec_fg = "#a5bfd1" if is_dark_tab else "#355566"
            spec_border = "#3a4f5e" if is_dark_tab else "#c6d4de"

            spec_strip = tk.Frame(
                tab_frame, bg=spec_bg,
                highlightthickness=1, highlightbackground=spec_border,
                padx=sc(10), pady=sc(8)
            )
            spec_strip.pack(fill="x", padx=sc(12), pady=(sc(4), sc(2)))
            ui._registry_theme_widgets["spec_bars"].append(spec_strip)

            cb = tk.Checkbutton(
                spec_strip, cursor="hand2",
                text="Needs Specialist",
                variable=var,
                font=("Inter", sc(9), "bold"),
                bg=spec_bg, fg=spec_fg,
                activebackground=spec_bg, activeforeground=spec_fg,
                selectcolor="#1d2d35" if is_dark_tab else "#ffffff",
                relief="flat", bd=0, highlightthickness=0,
                command=lambda: (
                    RegistryPanel.update_reg_fields_visibility(ui, skip_snap=True),
                    ui.commit_current_object()
                )
            )
            cb.pack(anchor="w")
            cb.tutorial_id = "other_problem_checkbox"
            ui._registry_theme_widgets["spec_cbs"].append(cb)
            spec_sub_lbl = tk.Label(
                spec_strip,
                text="Physical / archival escalation (NOTE / REV+NOTE) for broken specimens, mold/pest, or deadlocks — synced with Comment and excluded from the default trainee queue.",
                font=("Inter", sc(8)),
                bg=spec_bg, fg=spec_fg,
                wraplength=sc(340), justify="left", anchor="w"
            )
            spec_sub_lbl.pack(anchor="w", padx=(sc(22), 0), pady=(sc(2), 0))
            ui._registry_theme_widgets["spec_subtitles"].append(spec_sub_lbl)
            ui.problem_checkbuttons.append(cb)
            ui.problem_checkbutton_map[name] = cb

        ttk.Separator(tab_frame, orient="horizontal").pack(fill="x", pady=10)

        ui.problem_frame = ttk.Frame(tab_frame, padding=12)
        ui.problem_frame.pack(fill="both", expand=True)
        ui.problem_frame.tutorial_id = "problem_flags_frame"

        # -------- LOCATION --------
        for w in ui.location_frame.winfo_children():
            w.destroy()
        if hasattr(ui, 'loc_frame_horizontal'):
            for w in ui.loc_frame_horizontal.winfo_children():
                w.destroy()

        ui.location_vars.clear()
        ui.location_entries = []

        for field in ui.app.config["ui_sections"]["location"]:
            name = field["name"]
            var = tk.StringVar()
            ui.location_vars[name] = var

        ui._build_vertical_location_ui()
        if hasattr(ui, 'loc_frame_horizontal'):
            ui._build_horizontal_location_ui()

        # -------- PROBLEMS --------
        ui.update_problems_default_view()

    @staticmethod
    def update_reg_fields_visibility(ui, skip_snap=False):
        """Update field and card visibility based on Focus Mode and active problems."""
        if not ui.object_loaded:
            return

        focus_active = ui.focus_mode_var.get()
        focus_fallback = ui.focus_fallback_var.get()

        oid = ui.app.current_object_id
        if oid and not ui.loading_object:
            ui.commit_current_object(skip_heavy=True)

        active_problem_fields = set()
        for prob_col, mapped_field in ui.problem_to_field.items():
            if ui.problem_vars.get(prob_col) and ui.problem_vars[prob_col].get():
                active_problem_fields.add(mapped_field)

        if hasattr(ui, "loc_container") and hasattr(ui, "prob_container"):
            show_loc = not (focus_active and not ui.focus_visibility_vars.get("Location", tk.BooleanVar(value=True)).get())
            show_prob = not (focus_active and not ui.focus_visibility_vars.get("Problems", tk.BooleanVar(value=True)).get())

            ui.loc_container.pack_forget()

            loc_in_center = hasattr(ui, 'location_in_center_var') and ui.location_in_center_var.get()

            if show_loc and not loc_in_center:
                if str(ui.left_bottom_container) not in ui.left_panes.panes():
                    ui.left_panes.add(ui.left_bottom_container, weight=0)
                ui.loc_container.pack(side="top", fill="x")
            else:
                if str(ui.left_bottom_container) in ui.left_panes.panes():
                    ui.left_panes.forget(ui.left_bottom_container)

            if show_prob:
                try:
                    ui.reg_notebook.add(ui._reg_tabs["Problems"]["container"])
                except Exception:
                    pass
            else:
                try:
                    ui.reg_notebook.hide(ui._reg_tabs["Problems"]["container"])
                except Exception:
                    pass

        visible_count = 0
        legacy_note_fields = ("Observation", "ProblemDescription", "Problem Description")

        def _has_legacy_note_text(field_name: str) -> bool:
            w = getattr(ui, "reg_entries", {}).get(field_name)
            if isinstance(w, tk.Text):
                try:
                    return bool(w.get("1.0", "end-1c").strip())
                except Exception:
                    pass
            var = getattr(ui, "reg_vars", {}).get(field_name)
            if var is not None:
                try:
                    return bool(str(var.get() or "").strip())
                except Exception:
                    pass
            df_reg = getattr(getattr(ui, "app", None), "df_reg", None)
            if df_reg is not None and oid is not None and field_name in df_reg.columns:
                for key in (oid, str(oid), int(oid) if str(oid).isdigit() else None):
                    if key is not None and key in df_reg.index:
                        val = str(df_reg.loc[key, field_name] or "").strip()
                        return bool(val and val.lower() not in ("nan", "none", "<na>"))
            return False

        for field in ui.app.config["ui_sections"]["registration"]:
            name = field["name"]
            frame = ui.reg_row_frames.get(name)
            if not frame:
                continue

            is_visible = True
            # Non-Destructive Legacy Reveal: hide Observation / ProblemDescription unless this specimen has text in them
            if name in legacy_note_fields and not _has_legacy_note_text(name):
                is_visible = False

            if is_visible and focus_active:
                field_toggle = ui.focus_visibility_vars.get(name, tk.BooleanVar(value=True)).get()
                has_problem = (name in active_problem_fields)
                if focus_fallback and has_problem:
                    is_visible = True
                else:
                    is_visible = field_toggle

            if is_visible:
                if frame.winfo_manager() != "grid":
                    frame.grid()
                visible_count += 1
            else:
                if frame.winfo_manager() == "grid":
                    frame.grid_remove()

        if hasattr(ui, "unknown_fields_container"):
            frame = ui.unknown_fields_container
            is_visible = not focus_active

            if is_visible:
                if frame.winfo_manager() != "grid":
                    frame.grid()
                visible_count += 1
            else:
                if frame.winfo_manager() == "grid":
                    frame.grid_remove()

        if hasattr(ui, "no_problems_msg_label"):
            if focus_active and visible_count <= 0:
                ui.no_problems_msg_label.config(text="No active problems for this specimen. Focus Mode is hiding clean fields.")
                if ui.no_problems_msg_label.winfo_manager() != "grid":
                    ui.no_problems_msg_label.grid(row=0, column=0, pady=(15, 6), sticky="ew")
                if hasattr(ui, "focus_show_all_btn") and ui.focus_show_all_btn.winfo_manager() != "grid":
                    ui.focus_show_all_btn.grid(row=1, column=0, pady=(0, 12))
            else:
                if ui.no_problems_msg_label.winfo_manager() == "grid":
                    ui.no_problems_msg_label.grid_remove()
                if hasattr(ui, "focus_show_all_btn") and ui.focus_show_all_btn.winfo_manager() == "grid":
                    ui.focus_show_all_btn.grid_remove()

        if hasattr(ui, "card_frames") and hasattr(ui, "card_defs_ordered"):
            for card_id in ui.card_defs_ordered:
                info = ui.card_frames[card_id]
                card_frame = info["frame"]
                fields = info["fields"]
                any_visible = False
                for f in fields:
                    row_frame = ui.reg_row_frames.get(f)
                    if row_frame and row_frame.winfo_manager() == "grid":
                        any_visible = True
                        break
                if any_visible:
                    if card_frame.winfo_manager() != "pack":
                        card_frame.pack(fill="x", padx=10, pady=8)
                else:
                    if card_frame.winfo_manager() == "pack":
                        card_frame.pack_forget()

        if not skip_snap and ui.snap_lock_var.get():
            ui.snap_to_place(shrink=focus_active)

    @staticmethod
    def refresh_field_background(ui, field_name):
        """Update individual field widget background color based on validation and problem state."""
        import config
        widget = ui.reg_entries.get(field_name)
        if not widget:
            return

        is_dark = getattr(ui, "dark_mode_active", ui.app.config.get("theme", "dark") == "dark")
        norm_bg = "#212622" if is_dark else "#ffffff"
        warn_bg = "#3b2e15" if is_dark else "#fef9e7"
        err_bg = "#3b1c1e" if is_dark else "#ffdad6"
        unknown_bg = "#3b2e15" if is_dark else "#fef9e7"
        suggest_bg = "#1e293b" if is_dark else "#e9f0f5"

        is_active_problem = False
        prob_col = None
        for p_col, f_name in ui.problem_to_field.items():
            if f_name == field_name:
                prob_col = p_col
                break
        if prob_col and ui.problem_vars.get(prob_col) and ui.problem_vars[prob_col].get():
            is_active_problem = True

        genus = ui.reg_vars.get("Genus", tk.StringVar()).get().strip()
        species = ui.reg_vars.get("Species", tk.StringVar()).get().strip()
        building = ui.reg_vars.get("Building", tk.StringVar()).get().strip()
        loc_prob = ui.problem_vars.get("Loc_Problem", tk.BooleanVar()).get()

        color = norm_bg

        if is_active_problem:
            hl_color_name = "Default (Red)"
            has_custom_pref = False
            try:
                advanced_prefs = config.load_prefs().get("advanced", {})
                if advanced_prefs.get("enable_problem_highlights", True):
                    pref_val = advanced_prefs.get("problem_highlight_color")
                    if pref_val and pref_val != "Default (Red)":
                        hl_color_name = pref_val
                        has_custom_pref = True
            except Exception:
                pass

            if has_custom_pref:
                if "Yellow" in hl_color_name:
                    tint = "#3b2e15" if is_dark else "#fef9e7"
                elif "Orange" in hl_color_name:
                    tint = "#3b2615" if is_dark else "#fef0e6"
                elif "Blue" in hl_color_name:
                    tint = "#1e293b" if is_dark else "#e9f0f5"
                else:
                    tint = "#3b1c1e" if is_dark else "#ffdad6"
            else:
                prob_cat = ui.problem_categories.get(prob_col, "notes") if hasattr(ui, "problem_categories") else "notes"
                prob_imp = ui.problem_importances.get(prob_col, "medium") if hasattr(ui, "problem_importances") else "medium"
                if prob_imp == "low":
                    tint = "#1e293b" if is_dark else "#f2f5f1"
                elif prob_cat == "taxonomy":
                    tint = "#3b1c1e" if is_dark else "#ffdad6"
                elif prob_cat == "collection":
                    tint = "#3b2e15" if is_dark else "#fef9e7"
                elif prob_cat == "physical":
                    tint = "#4e342e" if is_dark else "#efebe9"
                elif prob_cat == "media":
                    tint = "#203a5f" if is_dark else "#e3f2fd"
                else:
                    tint = "#5c1e1e" if is_dark else "#ffdad6"
            color = tint
        elif field_name == "Species" and genus and not species:
            color = warn_bg
        elif field_name == "Building" and not building and not loc_prob:
            color = err_bg
        else:
            raw_val = ui.reg_vars.get(field_name, tk.StringVar()).get()
            if isinstance(raw_val, pd.Series):
                raw_val = raw_val.iloc[0]
            raw_val = str(raw_val)

            if ui.is_unknown(raw_val):
                color = unknown_bg
            elif getattr(ui, "show_all_history_var", None) and ui.show_all_history_var.get():
                if ui.current_object_suggestions and field_name in ui.collect_historical_suggestions(ui.app.current_object_id):
                    color = suggest_bg
            else:
                color = norm_bg

        try:
            if isinstance(widget, (tk.Text, tk.Entry)):
                widget.config(background=color)
            elif isinstance(widget, ttk.Combobox):
                if color == warn_bg:
                    widget.configure(style="Warning.TCombobox")
                elif color == err_bg:
                    widget.configure(style="Error.TCombobox")
                elif is_active_problem:
                    widget.configure(style="Problem.TCombobox")
                else:
                    widget.configure(style="TCombobox")
            elif isinstance(widget, ttk.Entry):
                if color == warn_bg:
                    widget.configure(style="Warning.TEntry")
                elif color == err_bg:
                    widget.configure(style="Error.TEntry")
                elif is_active_problem:
                    widget.configure(style="Problem.TEntry")
                else:
                    widget.configure(style="TEntry")
        except Exception as e:
            debug_error("Suppressed Error in _refresh_field_background", str(e))

        # Sync per-field ICEDIG trigger button highlight
        icedig_btn = getattr(ui, "icedig_field_btns", {}).get(field_name)
        if icedig_btn is not None:
            try:
                if icedig_btn.winfo_exists():
                    val_str = str(ui.reg_vars.get(field_name, tk.StringVar()).get() or "").strip().lower()
                    is_icedig = val_str in config.ICEDIG_UNKNOWN_CODES
                    card_bg = "#212622" if is_dark else "#ffffff"
                    if is_icedig:
                        icedig_btn.configure(
                            bg="#3b2e15" if is_dark else "#fef3c7",
                            fg="#fcd34d" if is_dark else "#92400e",
                            activebackground="#4d3b1a" if is_dark else "#fde68a",
                            activeforeground="#fcd34d" if is_dark else "#78350f",
                        )
                    else:
                        icedig_btn.configure(
                            bg=card_bg,
                            fg="#8b948d",
                            activebackground="#2a322c" if is_dark else "#e9ece5",
                            activeforeground="#e8ebe9" if is_dark else "#2c302e",
                        )
            except Exception:
                pass

    @staticmethod
    def apply_theme(ui, is_dark: bool):
        """Live-update custom tk widgets inside Registration & Problems tabs when toggling Light/Dark mode."""
        canvas_bg = "#181c19" if is_dark else "#fbfaf8"
        card_bg = "#212622" if is_dark else "#ffffff"
        header_bg = "#262c28" if is_dark else "#f5f5f5"
        border_color = "#333a35" if is_dark else "#e2e2e2"
        fg_color = "#e8ebe9" if is_dark else "#2c302e"
        legacy_fg = "#9399b2" if is_dark else "#757d77"
        spec_bg = "#222c34" if is_dark else "#eef2f5"
        spec_fg = "#a5bfd1" if is_dark else "#355566"
        spec_border = "#3a4f5e" if is_dark else "#c6d4de"
        spec_sel = "#1d2d35" if is_dark else "#ffffff"
        hint_fg = "#d9a036" if is_dark else "#9a6700"

        tw = getattr(ui, "_registry_theme_widgets", None) or {}
        for w in tw.get("canvases", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=canvas_bg)
            except Exception:
                pass
        for w in tw.get("card_frames", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=card_bg, highlightbackground=border_color)
            except Exception:
                pass
        for w in tw.get("header_frames", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=header_bg)
            except Exception:
                pass
        for w in tw.get("header_lbls", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=header_bg, fg=fg_color)
            except Exception:
                pass
        for w in tw.get("badge_lbls", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=header_bg)
            except Exception:
                pass
        for w in tw.get("body_frames", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=card_bg)
            except Exception:
                pass
        for w in tw.get("row_frames", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=card_bg)
            except Exception:
                pass
        for item in tw.get("field_lbls", []):
            try:
                w, is_legacy = item
                if w.winfo_exists():
                    w.configure(bg=card_bg, fg=legacy_fg if is_legacy else fg_color)
            except Exception:
                pass
        for w in tw.get("comment_boxes", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=card_bg)
            except Exception:
                pass
        for w in tw.get("spec_bars", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=spec_bg, highlightbackground=spec_border)
            except Exception:
                pass
        for w in tw.get("spec_cbs", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=spec_bg, fg=spec_fg, activebackground=spec_bg, activeforeground=spec_fg, selectcolor=spec_sel)
            except Exception:
                pass
        for w in tw.get("spec_subtitles", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=spec_bg, fg=spec_fg)
            except Exception:
                pass
        for w in tw.get("tag_rows", []):
            try:
                if w.winfo_exists():
                    if hasattr(w, "set_bg"):
                        w.set_bg(card_bg)
                    else:
                        w.configure(bg=card_bg)
            except Exception:
                pass
        for w in tw.get("tag_pills", []):
            try:
                if w.winfo_exists():
                    w.configure(
                        bg=spec_bg, fg=spec_fg,
                        activebackground=spec_border, activeforeground=spec_fg,
                        highlightbackground=spec_border,
                    )
            except Exception:
                pass
        for w in tw.get("hint_lbls", []):
            try:
                if w.winfo_exists():
                    w.configure(bg=card_bg, fg=hint_fg)
            except Exception:
                pass

        for fname in list(getattr(ui, "icedig_field_btns", {}).keys()):
            RegistryPanel.refresh_field_background(ui, fname)
        for fname, bar in list(getattr(ui, "prob_border_bars", {}).items()):
            try:
                if bar and bar.winfo_exists():
                    prob_col = getattr(ui, "field_to_problem", {}).get(fname)
                    is_flagged = bool(ui.problem_vars.get(prob_col).get()) if prob_col and prob_col in getattr(ui, "problem_vars", {}) else False
                    if not is_flagged:
                        bar.configure(bg=card_bg)
            except Exception:
                pass

    @staticmethod
    def validate_fields(ui, event=None):
        if ui._is_navigating or ui.loading_object:
            return

        for f_name in ui.reg_entries.keys():
            RegistryPanel.refresh_field_background(ui, f_name)

    @staticmethod
    def run_fuzzy_match(ui, field_name, widget):
        if field_name not in ["Genus", "Species"]:
            return

        val = ui.reg_vars[field_name].get().strip()
        if not val or len(val) < 3:
            if hasattr(widget, "fuzzy_label"):
                widget.fuzzy_label.destroy()
                delattr(widget, "fuzzy_label")
            return

        history = ui.current_object_suggestions.get(field_name, [])
        if not history:
            return

        matches = difflib.get_close_matches(val, history, n=1, cutoff=0.7)

        if matches and matches[0].lower() != val.lower():
            suggestion = matches[0]
            if hasattr(widget, "fuzzy_label"):
                widget.fuzzy_label.destroy()

            lbl = ttk.Label(widget.master, text=f"Did you mean '{suggestion}'?", foreground="#4dabf7", font=("Segoe UI", sc(8), "underline"), cursor="hand2")
            lbl.grid(row=1, column=1, sticky="w")

            def apply_suggestion(e, s=suggestion, w=widget, n=field_name):
                ui.reg_vars[n].set(s)
                ui.commit_current_object()
                w.fuzzy_label.destroy()
                delattr(w, "fuzzy_label")
                RegistryPanel.validate_fields(ui)

            lbl.bind("<Button-1>", apply_suggestion)
            widget.fuzzy_label = lbl
        else:
            if hasattr(widget, "fuzzy_label"):
                widget.fuzzy_label.destroy()
                delattr(widget, "fuzzy_label")

    @staticmethod
    def clear_all_fuzzy_labels(ui):
        """Destroy any 'Did you mean' suggestion labels on all registration entry widgets."""
        for widget in ui.reg_entries.values():
            if hasattr(widget, "fuzzy_label"):
                try:
                    widget.fuzzy_label.destroy()
                except Exception:
                    pass
                delattr(widget, "fuzzy_label")

    @staticmethod
    def on_autocomplete_key(ui, event, name, widget):
        if event.keysym in ("Up", "Down", "Left", "Right", "Return", "Escape", "Tab", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R"):
            return
        typed = widget.get().strip().lower()
        all_vals = ui.current_object_suggestions.get(name, [])
        if not all_vals:
            return
        if not typed:
            filtered = all_vals
        else:
            filtered = [v for v in all_vals if typed in str(v).lower()]
        if isinstance(widget, ttk.Combobox):
            widget.configure(values=filtered)

    @staticmethod
    def merge_legacy_notes_into_comment(ui, interactive: bool = True) -> int:
        """
        One-time opt-in, non-destructive cleanup that combines legacy Observation and
        ProblemDescription notes into the unified Comment field without overwriting
        any existing Comment text.
        """
        from tkinter import messagebox
        import pandas as pd

        app = getattr(ui, "app", None)
        df_reg = getattr(app, "df_reg", None)
        if df_reg is None or df_reg.empty:
            return 0

        if hasattr(ui, "commit_current_object") and getattr(app, "current_object_id", None):
            try:
                ui.commit_current_object(skip_heavy=True)
            except Exception:
                pass

        legacy_cols = [c for c in ("Observation", "ProblemDescription", "Problem Description") if c in df_reg.columns]
        if not legacy_cols:
            if interactive and hasattr(ui, "show_toast"):
                ui.show_toast("All notes are already in Comment — no legacy notes found.", "info")
            return 0

        def _clean_text(v) -> str:
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return ""
            s = str(v).strip()
            return "" if s.lower() in ("nan", "none", "<na>") else s

        # Identify rows with non-empty legacy notes
        candidate_indices = []
        for idx in df_reg.index:
            has_any = any(_clean_text(df_reg.loc[idx, c]) for c in legacy_cols)
            if has_any:
                candidate_indices.append(idx)

        if not candidate_indices:
            if interactive and hasattr(ui, "show_toast"):
                ui.show_toast("All notes are already in Comment — no legacy notes found.", "info")
            return 0

        if interactive:
            count = len(candidate_indices)
            noun = "specimen" if count == 1 else "specimens"
            proceed = messagebox.askyesno(
                "Combine Legacy Notes into Comment",
                f"Found {count} {noun} with notes in older fields (Observation / Problem Note).\n\n"
                "Would you like to combine those notes into the main Comment box?\n\n"
                "• Completely safe & non-destructive: existing Comments are never overwritten — older notes are added neatly underneath.\n"
                "• Nothing is written to disk until you press Ctrl+S (and Arbor saves a safety backup first).\n"
                "• You can also click No to keep them as-is; Arbor automatically shows legacy boxes whenever an object has text in them.",
                parent=getattr(ui, "root", None),
            )
            if not proceed:
                return 0

        if "Comment" not in df_reg.columns:
            df_reg["Comment"] = ""

        label_map = {
            "Observation": "Legacy Observation",
            "ProblemDescription": "Legacy Problem Note",
            "Problem Description": "Legacy Problem Note",
        }

        updated = 0
        lock = getattr(app, "df_lock", None)
        def _apply_merge():
            nonlocal updated
            for idx in candidate_indices:
                existing = _clean_text(df_reg.loc[idx, "Comment"])
                parts = [existing] if existing else []
                for col in legacy_cols:
                    val = _clean_text(df_reg.loc[idx, col])
                    if not val:
                        continue
                    # Avoid duplicating if already merged previously
                    if val in existing:
                        df_reg.loc[idx, col] = ""
                        continue
                    prefix = label_map.get(col, col)
                    parts.append(f"[{prefix}]: {val}" if existing or len(parts) > 0 else val)
                    df_reg.loc[idx, col] = ""
                merged = "\n".join(p for p in parts if p)
                df_reg.loc[idx, "Comment"] = merged
                updated += 1
            app.dirty = True
            if hasattr(app, "_mutation_seq"):
                app._mutation_seq += 1

        if lock is not None:
            with lock:
                _apply_merge()
        else:
            _apply_merge()

        if hasattr(ui, "_invalidate_row_cache"):
            try:
                ui._invalidate_row_cache()
            except Exception:
                pass
        if hasattr(ui, "update_dirty_ui"):
            try:
                ui.update_dirty_ui()
            except Exception:
                pass
        curr_oid = getattr(app, "current_object_id", None)
        if curr_oid and hasattr(ui, "load_object"):
            try:
                ui.load_object(curr_oid)
            except Exception:
                pass
        if interactive and hasattr(ui, "show_toast"):
            ui.show_toast(
                f"✓ Safely combined legacy notes into Comment for {updated} specimen(s) — press Ctrl+S to save.",
                "success",
                duration_ms=4000,
            )
        return updated
