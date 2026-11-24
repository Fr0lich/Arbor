import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox
import config
from config import sc


def _render_markdown_to_text(txt_widget, md_text, is_dark=False):
    """
    Parses markdown text and inserts it into a Tkinter Text widget with rich tags.
    Returns a list of detected chapter bookmarks: [(title, mark_id), ...]
    """
    fg_text = "#e8ebe9" if is_dark else "#2c302e"
    fg_h1 = "#81c784" if is_dark else "#1b5e20"
    fg_h2 = "#a5d6a7" if is_dark else "#2e7d32"
    fg_h3 = "#c8e6c9" if is_dark else "#388e3c"
    fg_code = "#ff7b72" if is_dark else "#b33939"
    bg_code = "#2d333b" if is_dark else "#ebeff2"
    bg_block = "#1e242c" if is_dark else "#f3f5f4"
    fg_dim = "#8b949e" if is_dark else "#7f8c8d"
    bg_callout = "#1e3a24" if is_dark else "#eef6ef"
    fg_callout = "#b0f3a9" if is_dark else "#1e4620"
    fg_link = "#64b5f6" if is_dark else "#2e7d32"

    # Define Tags
    txt_widget.tag_configure("h1", font=("Segoe UI", sc(14), "bold"), foreground=fg_h1, spacing1=sc(8), spacing3=sc(6))
    txt_widget.tag_configure("h2", font=("Segoe UI", sc(11), "bold"), foreground=fg_h2, spacing1=sc(12), spacing3=sc(4))
    txt_widget.tag_configure("h3", font=("Segoe UI", sc(10), "bold"), foreground=fg_h3, spacing1=sc(8), spacing3=sc(2))
    txt_widget.tag_configure("body", font=("Segoe UI", sc(9.5)), foreground=fg_text, spacing1=sc(1), spacing3=sc(1))
    txt_widget.tag_configure("bold", font=("Segoe UI", sc(9.5), "bold"), foreground=fg_text)
    txt_widget.tag_configure("italic", font=("Segoe UI", sc(9.5), "italic"), foreground=fg_text)
    txt_widget.tag_configure("bullet", font=("Segoe UI", sc(9.5)), foreground=fg_text, lmargin1=sc(16), lmargin2=sc(28))
    txt_widget.tag_configure("callout", font=("Segoe UI", sc(9.5)), foreground=fg_callout, background=bg_callout, lmargin1=sc(14), lmargin2=sc(14), rmargin=sc(14), spacing1=sc(3), spacing3=sc(3))
    txt_widget.tag_configure("code_inline", font=("Consolas", sc(9), "bold"), foreground=fg_code, background=bg_code)
    txt_widget.tag_configure("code_block", font=("Consolas", sc(8.5)), foreground=fg_text, background=bg_block, lmargin1=sc(12), lmargin2=sc(12))
    txt_widget.tag_configure("table", font=("Consolas", sc(8.5)), foreground=fg_text)
    txt_widget.tag_configure("table_hdr", font=("Consolas", sc(8.5), "bold"), foreground=fg_h2, background=bg_block)
    txt_widget.tag_configure("hr", font=("Segoe UI", sc(3)), foreground=fg_dim)

    in_code_block = False
    in_table = False
    bookmarks = []
    anchor_map = {}

    def _slugify(title_str):
        slug = re.sub(r'[^a-z0-9\s-]', '', title_str.lower()).strip()
        return re.sub(r'\s+', '-', slug)

    def _scroll_to_top(mark_or_idx):
        try:
            txt_widget.update_idletasks()
            txt_widget.yview(mark_or_idx)
        except Exception:
            try:
                txt_widget.see(mark_or_idx)
            except Exception:
                pass

    def _jump_to_anchor(slug):
        mark = anchor_map.get(slug)
        if not mark:
            for k, m in anchor_map.items():
                if slug in k or k in slug:
                    mark = m
                    break
        if mark:
            _scroll_to_top(mark)

    def insert_inline(line_text, base_tag=None):
        parts = re.split(r'(\[[^\]]+\]\(#[^)]+\)|`[^`]+`|\*\*[^*]+\*\*)', line_text)
        for part in parts:
            if not part:
                continue
            if part.startswith('[') and '](#' in part and part.endswith(')'):
                m = re.match(r'^\[([^\]]+)\]\(#([^)]+)\)$', part)
                if m:
                    lbl_txt, anchor_slug = m.group(1), m.group(2)
                    link_tag = f"link_{anchor_slug}_{len(txt_widget.tag_names())}"
                    txt_widget.tag_configure(link_tag, font=("Segoe UI", sc(9.5), "underline"), foreground=fg_link)
                    txt_widget.tag_bind(link_tag, "<Button-1>", lambda e, s=anchor_slug: _jump_to_anchor(s))
                    txt_widget.tag_bind(link_tag, "<Enter>", lambda e: txt_widget.config(cursor="hand2"))
                    txt_widget.tag_bind(link_tag, "<Leave>", lambda e: txt_widget.config(cursor=""))
                    tags = (link_tag, base_tag) if base_tag else (link_tag,)
                    txt_widget.insert("end", lbl_txt, tags)
                    continue
            if part.startswith('`') and part.endswith('`') and len(part) >= 2:
                txt_widget.insert("end", part[1:-1], "code_inline")
            elif part.startswith('**') and part.endswith('**') and len(part) >= 4:
                txt_widget.insert("end", part[2:-2], ("bold", base_tag) if base_tag else "bold")
            else:
                if base_tag:
                    txt_widget.insert("end", part, base_tag)
                else:
                    txt_widget.insert("end", part, "body")

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        # Handle code fences
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            txt_widget.insert("end", raw_line + "\n", "code_block")
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            txt_widget.insert("end", " " * 80 + "\n", "hr")
            continue

        # Headers and Bookmark registration
        if line.startswith("# "):
            in_table = False
            title = line[2:].strip()
            mark_id = f"bm_{len(bookmarks)}"
            txt_widget.mark_set(mark_id, txt_widget.index("end-1c"))
            txt_widget.mark_gravity(mark_id, "left")
            bookmarks.append((title, mark_id))
            anchor_map[_slugify(title)] = mark_id
            txt_widget.insert("end", title + "\n", "h1")
        elif line.startswith("## "):
            in_table = False
            title = line[3:].strip()
            mark_id = f"bm_{len(bookmarks)}"
            txt_widget.mark_set(mark_id, txt_widget.index("end-1c"))
            txt_widget.mark_gravity(mark_id, "left")
            bookmarks.append((title, mark_id))
            anchor_map[_slugify(title)] = mark_id
            txt_widget.insert("end", title + "\n", "h2")
        elif line.startswith("### "):
            in_table = False
            txt_widget.insert("end", line[4:].strip() + "\n", "h3")
        elif line.startswith("> "):
            in_table = False
            insert_inline("  " + line[2:].strip(), base_tag="callout")
            txt_widget.insert("end", "\n", "callout")
        elif line.startswith("|") and line.endswith("|"):
            # Skip markdown alignment separator lines like | :--- | :--- |
            if re.match(r'^\|[\s:\-|]+\|$', line):
                continue
            tag = "table_hdr" if not in_table else "table"
            in_table = True
            clean_row = "  " + " │ ".join(c.strip() for c in line.strip("|").split("|"))
            txt_widget.insert("end", clean_row + "\n", tag)
        elif re.match(r'^\d+\.\s+', line):
            in_table = False
            insert_inline(line, base_tag="bullet")
            txt_widget.insert("end", "\n")
        elif line.startswith("* ") or line.startswith("- "):
            in_table = False
            txt_widget.insert("end", "• ", "bullet")
            insert_inline(line[2:], base_tag="bullet")
            txt_widget.insert("end", "\n")
        elif line.startswith("  * ") or line.startswith("  - "):
            in_table = False
            txt_widget.insert("end", "    - ", "bullet")
            insert_inline(line[4:], base_tag="bullet")
            txt_widget.insert("end", "\n")
        elif line.strip() == "":
            in_table = False
            txt_widget.insert("end", "\n")
        else:
            in_table = False
            insert_inline(raw_line)
            txt_widget.insert("end", "\n")

    return bookmarks


def _load_guide_markdown(filename, fallback_title):
    """Locate and read a markdown guide file with PyInstaller + repo fallbacks."""
    import utils

    candidate_paths = []
    try:
        candidate_paths.append(utils.get_resource_path(filename))
    except Exception:
        pass

    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        candidate_paths.append(os.path.join(base_dir, filename))
        if filename == "USER_GUIDE.md":
            candidate_paths.append(os.path.join(base_dir, "documentation", "curator", "CURATOR_USER_GUIDE.md"))
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate_paths.append(os.path.join(repo_root, filename))
        if filename == "USER_GUIDE.md":
            candidate_paths.append(os.path.join(repo_root, "documentation", "curator", "CURATOR_USER_GUIDE.md"))

    for p in candidate_paths:
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"# {fallback_title}\n\nCould not read guide file: {e}"

    return f"# {fallback_title}\n\n`{filename}` could not be found at standard resource paths."


def show_main_help(root_or_ui, initial_tab="desktop", initial_chapter=None):
    """
    Display the unified Arbor Guide Reader (Desktop Work Manual + Mobile Vault Guide)
    with a clickable left-hand chapter sidebar, Find-in-Guide (Ctrl+F), and quick links.
    Works from StartupDialog, MobileHostApp, normal desktop sessions, and Practice Mode.
    """
    import utils

    root = getattr(root_or_ui, "root", root_or_ui)
    is_dark = getattr(root_or_ui, "dark_mode_active", False)
    has_main_ui = hasattr(root_or_ui, "app") and hasattr(root_or_ui, "start_tutorial_flow")

    win = tk.Toplevel(root)
    win.title("Arbor System User Guide — Desktop & Mobile Manuals")
    w_width = sc(960)
    w_height = sc(760)
    utils.center_and_fit_toplevel(win, w_width, w_height)
    win.bind("<Escape>", lambda e: win.destroy())

    # Arbor AI_UI_GUIDE.md Design Tokens
    bg_outer = "#181c19" if is_dark else "#fbfaf8"
    bg_sidebar = "#1c211d" if is_dark else "#f2f5f1"
    bg_surface = "#212622" if is_dark else "#ffffff"
    fg_text = "#e8ebe9" if is_dark else "#2c302e"
    fg_muted = "#a2aba5" if is_dark else "#757d77"
    border_col = "#2c302e" if is_dark else "#c4c7c7"
    accent_col = "#389e63" if is_dark else "#3a7d44"
    accent_soft = "#1e3a24" if is_dark else "#eaf5ec"
    accent_fg = "#b0f3a9" if is_dark else "#1b5e20"

    win.configure(background=bg_outer)

    # ── Top Header Bar ───────────────────────────────────────────────────────
    hdr_frame = tk.Frame(win, bg=bg_outer, padx=sc(18), pady=sc(12))
    hdr_frame.pack(fill="x")

    title_col = tk.Frame(hdr_frame, bg=bg_outer)
    title_col.pack(side="left")

    tk.Label(
        title_col,
        text="Arbor Guide",
        font=("Lora", sc(15), "bold"),
        fg=fg_text,
        bg=bg_outer,
        anchor="w",
    ).pack(anchor="w")

    tk.Label(
        title_col,
        text="Plain-language manuals for desk curation & vault hallway auditing",
        font=("Inter", sc(8.5)),
        fg=fg_muted,
        bg=bg_outer,
        anchor="w",
    ).pack(anchor="w")

    # Right header quick actions
    hdr_actions = tk.Frame(hdr_frame, bg=bg_outer)
    hdr_actions.pack(side="right")

    if has_main_ui:
        def _launch_tour_from_reader():
            win.destroy()
            root_or_ui.start_tutorial_flow("review")

        tk.Button(
            hdr_actions,
            text="🎓 3-Min Practice Tour",
            font=("Inter", sc(8.5), "bold"),
            bg=accent_soft,
            fg=accent_fg,
            activebackground=accent_col,
            activeforeground="#ffffff",
            relief="flat",
            highlightbackground=accent_col,
            highlightthickness=1,
            padx=sc(10),
            pady=sc(4),
            cursor="hand2",
            command=_launch_tour_from_reader,
        ).pack(side="left", padx=(0, sc(8)))

    tk.Button(
        hdr_actions,
        text="⌨️ Shortcuts (F1)",
        font=("Inter", sc(8.5), "bold"),
        bg=bg_surface,
        fg=fg_text,
        relief="flat",
        highlightbackground=border_col,
        highlightthickness=1,
        padx=sc(10),
        pady=sc(4),
        cursor="hand2",
        command=lambda: show_shortcuts(root_or_ui),
    ).pack(side="left")

    # ── Segmented Tab Bar (Desktop Manual | Mobile Vault Guide) ──────────────
    tab_bar = tk.Frame(win, bg=bg_outer, padx=sc(18), pady=sc(4))
    tab_bar.pack(fill="x")

    tab_btns = {}
    active_tab = [initial_tab if initial_tab in ("desktop", "mobile") else "desktop"]

    # Find-in-Guide inline on right side of tab bar
    find_box = tk.Frame(tab_bar, bg=bg_outer)
    find_box.pack(side="right")

    tk.Label(
        find_box, text="Find:", font=("Inter", sc(8.5), "bold"),
        fg=fg_muted, bg=bg_outer
    ).pack(side="left", padx=(0, sc(4)))
    find_var = tk.StringVar()
    find_entry = ttk.Entry(find_box, textvariable=find_var, width=22)
    find_entry.pack(side="left", padx=(0, sc(4)))
    match_lbl = tk.Label(find_box, text="", font=("Inter", sc(8)), fg=fg_muted, bg=bg_outer)
    match_lbl.pack(side="left", padx=(sc(4), 0))

    tk.Frame(win, bg=border_col, height=1).pack(fill="x", pady=(sc(6), 0))

    # ── Footer (packed side="bottom" first so split body fills remaining area) ──
    footer = tk.Frame(win, bg=bg_outer, padx=sc(18), pady=sc(9))
    footer.pack(fill="x", side="bottom")
    tk.Frame(win, bg=border_col, height=1).pack(fill="x", side="bottom")

    tk.Label(
        footer,
        text="Tip: Press Ctrl+F to search inside this guide, or click any chapter on the left. Press Escape to close.",
        font=("Inter", sc(8.5), "italic"),
        fg=fg_muted,
        bg=bg_outer,
    ).pack(side="left")

    ttk.Button(footer, text="Close", command=win.destroy, cursor="hand2").pack(side="right")

    # ── 2-Column Split Body (Left Chapter Sidebar + Right Reading Card) ──────
    sidebar_outer = tk.Frame(win, bg=bg_sidebar, width=sc(235))
    sidebar_outer.pack(side="left", fill="y")
    sidebar_outer.pack_propagate(False)

    tk.Label(
        sidebar_outer,
        text="CHAPTERS",
        font=("JetBrains Mono", sc(8), "bold"),
        fg=fg_muted,
        bg=bg_sidebar,
        padx=sc(14),
        pady=sc(10),
        anchor="w",
    ).pack(fill="x")

    sb_canvas = tk.Canvas(sidebar_outer, bg=bg_sidebar, highlightthickness=0, bd=0)
    sb_list_frame = tk.Frame(sb_canvas, bg=bg_sidebar)
    sb_canvas_win = sb_canvas.create_window((0, 0), window=sb_list_frame, anchor="nw")
    sb_canvas.pack(fill="both", expand=True, padx=(sc(6), sc(6)), pady=(0, sc(8)))

    sb_list_frame.bind("<Configure>", lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all")))
    sb_canvas.bind("<Configure>", lambda e: sb_canvas.itemconfig(sb_canvas_win, width=e.width))

    tk.Frame(win, bg=border_col, width=1).pack(side="left", fill="y")

    content_frame = tk.Frame(win, bg=bg_surface, padx=sc(16), pady=sc(10))
    content_frame.pack(side="left", fill="both", expand=True)

    sb = ttk.Scrollbar(content_frame, orient="vertical")
    txt = tk.Text(
        content_frame,
        wrap="word",
        font=("Inter", sc(9.5)),
        relief="flat",
        bg=bg_surface,
        fg=fg_text,
        padx=sc(14),
        pady=sc(10),
        yscrollcommand=sb.set,
        highlightthickness=0,
        spacing2=sc(2),
        state="normal",
    )
    sb.config(command=txt.yview)
    sb.pack(side="right", fill="y")
    txt.pack(side="left", fill="both", expand=True)

    _search_matches = []
    _search_idx = [0]
    _chapter_buttons = []

    def _run_find(*_):
        txt.tag_remove("search_hit", "1.0", "end")
        _search_matches.clear()
        _search_idx[0] = 0
        q = find_var.get().strip()
        if not q:
            match_lbl.config(text="")
            return
        pos = "1.0"
        while True:
            idx = txt.search(q, pos, stopindex="end", nocase=True)
            if not idx:
                break
            end_idx = f"{idx}+{len(q)}c"
            txt.tag_add("search_hit", idx, end_idx)
            _search_matches.append(idx)
            pos = end_idx
        if _search_matches:
            txt.see(_search_matches[0])
            match_lbl.config(text=f"1/{len(_search_matches)}")
        else:
            match_lbl.config(text="0")

    def _find_next(*_):
        if not _search_matches:
            _run_find()
            return
        _search_idx[0] = (_search_idx[0] + 1) % len(_search_matches)
        txt.see(_search_matches[_search_idx[0]])
        match_lbl.config(text=f"{_search_idx[0] + 1}/{len(_search_matches)}")

    find_var.trace_add("write", _run_find)
    find_entry.bind("<Return>", _find_next)
    ttk.Button(find_box, text="Next", command=_find_next, width=5).pack(side="left", padx=(sc(4), 0))
    win.bind("<Control-f>", lambda e: (find_entry.focus_set(), find_entry.select_range(0, "end"), "break")[2])

    def _scroll_reader_to_top(mark_or_idx):
        try:
            txt.update_idletasks()
            txt.yview(mark_or_idx)
        except Exception:
            try:
                txt.see(mark_or_idx)
            except Exception:
                pass

    def _select_chapter_btn(active_btn):
        for b in _chapter_buttons:
            if b is active_btn:
                b.config(bg=accent_soft, fg=accent_fg, font=("Inter", sc(8.5), "bold"))
            else:
                b.config(bg=bg_sidebar, fg=fg_text, font=("Inter", sc(8.5)))

    def _load_tab(tab_key, jump_slug=None):
        active_tab[0] = tab_key
        for k, btn in tab_btns.items():
            if k == tab_key:
                btn.config(bg=accent_col, fg="#ffffff")
            else:
                btn.config(bg=bg_surface, fg=fg_text)

        if tab_key == "mobile":
            content = _load_guide_markdown("MOBILE_COMPANION_USER_GUIDE.md", "Arbor Mobile Vault Guide")
        else:
            content = _load_guide_markdown("USER_GUIDE.md", "Arbor Desktop Work Manual")

        txt.config(state="normal")
        txt.delete("1.0", "end")
        bookmarks = _render_markdown_to_text(txt, content, is_dark=is_dark)
        txt.tag_configure("search_hit", background="#f9e2af" if is_dark else "#fde68a", foreground="#181c19")
        txt.config(state="disabled")

        # Rebuild clickable chapter sidebar
        for child in sb_list_frame.winfo_children():
            child.destroy()
        _chapter_buttons.clear()

        target_btn = None
        target_mark = None
        for idx_bm, (bm_title, bm_mark) in enumerate(bookmarks):
            short_title = bm_title.replace("Chapter ", "").strip()
            if len(short_title) > 30:
                short_title = short_title[:28].rstrip() + "…"

            btn = tk.Button(
                sb_list_frame,
                text=short_title,
                font=("Inter", sc(8.5)),
                bg=bg_sidebar,
                fg=fg_text,
                activebackground=accent_soft,
                activeforeground=accent_fg,
                relief="flat",
                bd=0,
                anchor="w",
                justify="left",
                padx=sc(8),
                pady=sc(5),
                cursor="hand2",
            )
            btn.configure(command=lambda m=bm_mark, b=btn: (_scroll_reader_to_top(m), _select_chapter_btn(b)))
            btn.pack(fill="x", pady=sc(1))
            _chapter_buttons.append(btn)

            if jump_slug:
                norm_bm = re.sub(r"[^a-z0-9]+", "-", bm_title.lower()).strip("-")
                if jump_slug.lower() in norm_bm:
                    target_btn = btn
                    target_mark = bm_mark

        if target_mark and target_btn:
            _scroll_reader_to_top(target_mark)
            _select_chapter_btn(target_btn)
        elif _chapter_buttons:
            _scroll_reader_to_top("1.0")
            _select_chapter_btn(_chapter_buttons[0])

        if find_var.get().strip():
            _run_find()

    for tab_key, tab_label in [("desktop", "📖 Desktop Work Manual"), ("mobile", "📱 Mobile Vault Guide")]:
        tb = tk.Button(
            tab_bar,
            text=tab_label,
            font=("Inter", sc(9), "bold"),
            bg=bg_surface,
            fg=fg_text,
            relief="flat",
            highlightbackground=border_col,
            highlightthickness=1,
            padx=sc(12),
            pady=sc(5),
            cursor="hand2",
            command=lambda k=tab_key: _load_tab(k),
        )
        tb.pack(side="left", padx=(0, sc(6)))
        tab_btns[tab_key] = tb

    _load_tab(active_tab[0], jump_slug=initial_chapter)


def show_quick_help(ui=None):
    """Display the Keyboard Shortcuts HUD or an overview of essential shortcuts."""
    if ui is not None and hasattr(ui, "root"):
        show_shortcuts(ui)
    else:
        messagebox.showinfo(
            "Quick Start",
            "Arbor Essential Shortcuts:\n\n"
            "• F1: Open Keyboard Shortcuts HUD (Cheat Sheet)\n"
            "• Ctrl+K / Ctrl+Shift+P: Open Universal Command Palette\n"
            "• Ctrl+S: Save active session directly to Excel\n"
            "• Ctrl+Enter: Mark specimen as reviewed & advance\n"
            "• Space: Toggle focused problem checkbox\n"
            "• Down / Up Arrow: Navigate between specimens"
        )


def show_about(ui=None):
    """Display the About Arbor dialog with application details, dynamic version, and environment info."""
    import platform
    import utils

    root = getattr(ui, "root", None) if ui else None
    win = tk.Toplevel(root) if root else tk.Toplevel()
    win.title("About Arbor")
    win.resizable(False, False)
    if root:
        win.transient(root)
    utils.center_and_fit_toplevel(win, sc(520), sc(420))

    is_dark = getattr(ui, "dark_mode_active", False) if ui else False
    bg_color = "#181c19" if is_dark else "#f8faf9"
    card_bg = "#212623" if is_dark else "#ffffff"
    fg_title = "#e8ebe9" if is_dark else "#2c302e"
    fg_text = "#c6cac7" if is_dark else "#444748"
    fg_sub = "#a2aba5" if is_dark else "#636d65"
    border_col = "#2c302e" if is_dark else "#e0e4e1"
    accent_col = "#389e63" if is_dark else "#2d7a4c"

    win.configure(background=bg_color)
    win.bind("<Escape>", lambda e: win.destroy())

    container = tk.Frame(win, bg=bg_color, padx=sc(20), pady=sc(16))
    container.pack(fill="both", expand=True)

    tk.Label(
        container,
        text="ARBOR",
        font=("Segoe UI", sc(16), "bold"),
        fg=accent_col,
        bg=bg_color
    ).pack(anchor="w")

    tk.Label(
        container,
        text="Herbarium & Museum Collection Curation System",
        font=("Segoe UI", sc(9.5), "bold"),
        fg=fg_title,
        bg=bg_color
    ).pack(anchor="w", pady=(0, sc(10)))

    card = tk.Frame(container, bg=card_bg, highlightbackground=border_col, highlightthickness=1, padx=sc(14), pady=sc(12))
    card.pack(fill="x", pady=(0, sc(12)))

    db_name = "None loaded"
    rec_count = 0
    if ui and getattr(ui, "app", None):
        if getattr(ui.app, "current_excel_path", None):
            db_name = os.path.basename(ui.app.current_excel_path)
        if getattr(ui.app, "df_reg", None) is not None:
            rec_count = len(ui.app.df_reg)

    app_ver = getattr(config, "APP_VERSION", "2.1.0")
    tk_ver = getattr(tk, "TkVersion", "unknown")

    info_rows = [
        ("Version", f"{app_ver} (Production Tkinter)"),
        ("Tkinter Runtime", f"{tk_ver}"),
        ("Python Runtime", f"{platform.python_version()} ({platform.system()} {platform.machine()})"),
        ("Active Database", f"{db_name} ({rec_count} records)" if rec_count else db_name),
        ("Storage Formats", "Excel (.xlsx), SQLite (.db), CSV"),
        ("Mission", "100% Offline-First Museum Collection Curation"),
    ]

    for label, val in info_rows:
        row_frame = tk.Frame(card, bg=card_bg)
        row_frame.pack(fill="x", pady=sc(2))
        tk.Label(row_frame, text=label, font=("Segoe UI", sc(8.5), "bold"), fg=fg_sub, bg=card_bg, width=17, anchor="w").pack(side="left")
        tk.Label(row_frame, text=val, font=("Segoe UI", sc(8.5)), fg=fg_text, bg=card_bg, anchor="w").pack(side="left", fill="x", expand=True)

    tk.Label(
        container,
        text="Arbor is a 100% offline-first museum curation and botanical label verification system.\n"
             "Designed for rapid physical inspection, box auditing, and Excel workbook synchronization.",
        font=("Segoe UI", sc(8)),
        fg=fg_sub,
        bg=bg_color,
        justify="left"
    ).pack(anchor="w", pady=(0, sc(12)))

    btn_frame = tk.Frame(container, bg=bg_color)
    btn_frame.pack(fill="x")
    ttk.Button(btn_frame, text="Close", command=win.destroy, style="Tool.TButton", width=10).pack(side="right")


def open_help_window(ui, initial_tab="tutorials"):
    """
    Display the Unified Arbor Help Center (matching UnifiedSettingsWindow layout).
    Available in normal desktop sessions, demo mode, and sandbox mode.
    """
    from ui.unified_help import open_unified_help

    parent = getattr(ui, "root", ui)
    hub = open_unified_help(parent, app_ref=ui, initial_tab=initial_tab)
    try:
        ui.help_win = hub.win
    except Exception:
        pass
    return hub


def show_shortcuts(ui):
    """
    Create a searchable HUD dialog displaying all keyboard shortcuts with visual keycaps,
    dual-depth trainee descriptions, and Excel translation impacts.
    Works from Main Window, StartupDialog, and MobileHostApp.
    """
    import utils

    root = getattr(ui, "root", ui)
    win = tk.Toplevel(root)
    win.title("Keyboard Shortcuts & Desk Guide HUD")
    utils.center_and_fit_toplevel(win, sc(880), sc(700))

    is_dark = getattr(ui, "dark_mode_active", False)
    bg_color = "#181c19" if is_dark else "#fbfaf8"
    fg_title = "#e8ebe9" if is_dark else "#2c302e"
    fg_label = "#a6adc8" if is_dark else "#757d77"
    fg_nomatch = "#c93a40"
    fg_cat = "#3a7d44"
    bg_key = "#111412" if is_dark else "#f2f5f1"
    fg_key = "#e8ebe9" if is_dark else "#2c302e"
    key_border = "#2c302e" if is_dark else "#dadada"
    fg_desc = "#c6cac7" if is_dark else "#2c302e"
    fg_excel = "#81c784" if is_dark else "#2e7d32"
    fg_footer = "#757d77"
    border_color = "#2c302e" if is_dark else "#dadada"
    btn_primary_bg = "#3a7d44" if is_dark else "#2c302e"
    btn_primary_hover = "#4b9e57" if is_dark else "#3d4240"

    win.configure(background=bg_color)
    win.transient(root)
    win.bind("<Escape>", lambda e: win.destroy())

    title_frame = tk.Frame(win, bg=bg_color)
    title_frame.pack(fill="x", padx=sc(24), pady=(sc(16), sc(8)))

    tk.Label(
        title_frame,
        text="KEYBOARD SHORTCUTS & DESK GUIDE",
        font=("Segoe UI", sc(13), "bold"),
        fg=fg_title,
        bg=bg_color
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Ergonomic keybindings for mouse-free curation, missing label codes (?m, ?i), and Excel mappings.",
        font=("Segoe UI", sc(9)),
        fg=fg_label,
        bg=bg_color
    ).pack(anchor="w", pady=(sc(2), 0))

    search_frame = tk.Frame(win, bg=bg_color, padx=sc(24))
    search_frame.pack(fill="x", pady=(0, sc(12)))

    search_card = tk.Frame(search_frame, bg=bg_key, bd=1, relief="solid", highlightbackground=border_color, highlightthickness=1, padx=sc(10), pady=sc(6))
    search_card.pack(fill="x")

    tk.Label(
        search_card,
        text="🔍",
        font=("Segoe UI", sc(9.5)),
        fg=fg_label,
        bg=bg_key
    ).pack(side="left", padx=(0, sc(6)))

    search_var = tk.StringVar()
    search_ent = tk.Entry(
        search_card, textvariable=search_var,
        font=("Segoe UI", sc(9.5)),
        bg=bg_key, fg=fg_key,
        insertbackground=fg_key,
        bd=0, highlightthickness=0
    )
    search_ent.pack(side="left", fill="x", expand=True)
    search_ent.focus_set()

    content_outer = tk.Frame(win, bg=bg_color)
    content_outer.pack(fill="both", expand=True, padx=sc(24), pady=(0, sc(10)))

    canvas = tk.Canvas(content_outer, bg=bg_color, highlightthickness=0)
    scrollbar = ttk.Scrollbar(content_outer, orient="vertical", command=canvas.yview)
    scroll_content = tk.Frame(canvas, bg=bg_color)

    scroll_content.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    window_id = canvas.create_window((0, 0), window=scroll_content, anchor="nw")
    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(window_id, width=e.width) if getattr(canvas, "_last_width", None) != e.width and not setattr(canvas, "_last_width", e.width) else None
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    try:
        from ui.scroll_helper import bind_mousewheel
        bind_mousewheel(canvas, scroll_content)
    except Exception:
        pass

    # Dynamically pull from canonical registry in ui/keybindings.py
    try:
        from ui.keybindings import get_canonical_shortcuts
        raw_shortcuts = get_canonical_shortcuts()
    except Exception:
        raw_shortcuts = [
            ("PRIMARY WORK KEYS", "[ CTRL ] + [ ENTER ] or [ CTRL ] + [ R ]", "Mark Reviewed & Advance", "Signs off record, advances to next (sets Reviewed = TRUE in Excel)"),
            ("PRIMARY WORK KEYS", "[ SPACE ]", "Toggle Problem Checkbox", "Flags or clears problem on active field (sets problem flag TRUE / FALSE in Excel)"),
            ("PRIMARY WORK KEYS", "[ CTRL ] + [ S ]", "Save Active Workbook to Excel", "Writes all updates safely to Excel"),
            ("SEARCHING & RECORD NAVIGATION", "[ CTRL ] + [ K ]", "Command Palette & Omni-Search", "Instant keyboard switcher to run any command or jump to #ObjectID"),
            ("SEARCHING & RECORD NAVIGATION", "[ CTRL ] + [ F ]", "Search Bar Focus", "Focuses directory search box to filter by ID, genus, or species"),
            ("SEARCHING & RECORD NAVIGATION", "[ CTRL ] + [ G ]", "Filter Menu", "Filters by Reviewed status, specific problem flags, or photos"),
            ("SPECIMEN PHOTOS & VIEW CONTROLS", "[ CTRL ] + [ 0 ]", "Reset Zoom", "Fits entire specimen sheet back into visible frame"),
            ("ASSISTANCE & WORKSPACE", "[ F1 ]", "Help Center & Shortcuts HUD", "Opens central assistance hub and keyboard cheat sheet"),
        ]

    def draw_shortcuts(filter_text=""):
        for w in scroll_content.winfo_children():
            w.destroy()

        categories = {}
        filter_lower = filter_text.lower()

        for item in raw_shortcuts:
            cat = item[0]
            keys = item[1]
            desc = item[2]
            excel_eff = item[3] if len(item) > 3 else ""

            if filter_lower:
                match = (
                    filter_lower in cat.lower() or
                    filter_lower in keys.lower() or
                    filter_lower in desc.lower() or
                    filter_lower in excel_eff.lower()
                )
                if not match:
                    continue

            categories.setdefault(cat, []).append((keys, desc, excel_eff))

        if not categories:
            tk.Label(
                scroll_content,
                text="No shortcuts matched your search.",
                font=("Segoe UI", sc(11), "italic"),
                fg=fg_nomatch,
                bg=bg_color
            ).pack(pady=sc(20))
            return

        for cat, items in categories.items():
            cat_frame = tk.Frame(scroll_content, bg=bg_color)
            cat_frame.pack(fill="x", pady=(sc(12), sc(4)), anchor="w")

            tk.Label(
                cat_frame,
                text=cat,
                font=("JetBrains Mono", sc(10), "bold"),
                fg=fg_cat,
                bg=bg_color
            ).pack(side="left")

            tk.Frame(cat_frame, bg=border_color, height=1).pack(side="left", fill="x", expand=True, padx=(sc(10), 0))

            grid_frame = tk.Frame(scroll_content, bg=bg_color)
            grid_frame.pack(fill="x", padx=sc(4), pady=sc(2), anchor="w")
            grid_frame.columnconfigure(0, minsize=sc(260))
            grid_frame.columnconfigure(1, weight=1)

            for r, (keys, desc, excel_eff) in enumerate(items):
                key_container = tk.Frame(
                    grid_frame, bg=bg_key,
                    bd=1, relief="solid",
                    highlightbackground=key_border,
                    highlightthickness=1,
                    padx=sc(8), pady=sc(3)
                )
                key_container.grid(row=r, column=0, sticky="w", pady=sc(4), padx=(0, sc(12)))

                tk.Label(
                    key_container,
                    text=keys,
                    font=("JetBrains Mono", sc(9.5), "bold"),
                    fg=fg_key,
                    bg=bg_key
                ).pack()

                desc_frame = tk.Frame(grid_frame, bg=bg_color)
                desc_frame.grid(row=r, column=1, sticky="w", pady=sc(3))

                tk.Label(
                    desc_frame,
                    text=desc,
                    font=("Segoe UI", sc(9.5), "bold"),
                    fg=fg_desc,
                    bg=bg_color,
                    wraplength=sc(540),
                    justify="left"
                ).pack(anchor="w")

                if excel_eff:
                    tk.Label(
                        desc_frame,
                        text=f"Excel impact: {excel_eff}",
                        font=("Segoe UI", sc(8.5), "italic"),
                        fg=fg_excel,
                        bg=bg_color,
                        wraplength=sc(540),
                        justify="left"
                    ).pack(anchor="w", pady=(sc(1), 0))

    draw_shortcuts()
    search_var.trace_add("write", lambda *args: draw_shortcuts(search_var.get()))

    footer = tk.Frame(win, bg=bg_color)
    footer.pack(fill="x", side="bottom", pady=sc(10), padx=sc(24))

    tk.Label(
        footer,
        text="Press Escape to close this window.",
        font=("Segoe UI", sc(9), "italic"),
        fg=fg_footer,
        bg=bg_color
    ).pack(side="left")

    btn_box = tk.Frame(footer, bg=bg_color)
    btn_box.pack(side="right")

    manual_btn = tk.Button(
        btn_box,
        text="📖 READ USER MANUAL",
        command=lambda: (win.destroy(), show_main_help(ui)),
        font=("Segoe UI", sc(9), "bold"),
        bg="#e0e4e1" if not is_dark else "#2c302e",
        fg=fg_title,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=sc(12),
        pady=sc(5)
    )
    manual_btn.pack(side="left", padx=(0, sc(8)))

    close_btn = tk.Button(
        btn_box,
        text="CLOSE",
        command=win.destroy,
        font=("Segoe UI", sc(9.5), "bold"),
        bg=btn_primary_bg,
        fg="#ffffff",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=sc(16),
        pady=sc(5)
    )
    close_btn.pack(side="left")
    close_btn.bind("<Enter>", lambda e: close_btn.config(bg=btn_primary_hover))
    close_btn.bind("<Leave>", lambda e: close_btn.config(bg=btn_primary_bg))
