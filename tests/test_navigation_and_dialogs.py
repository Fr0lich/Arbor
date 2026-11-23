"""Unit tests for High-DPI NavigationBar geometry and Modal mousewheel scroll consistency."""

import tkinter as tk
from unittest.mock import MagicMock
import pytest
import config
from ui.navigation_bar import NavigationBar
from ui.create_collection_dialog import CreateCollectionDialog
from ui.dialogs import StartupDialog


def test_navigation_bar_high_dpi_geometry_scaling():
    """Verify NavigationBar geometry scales dynamically with sc() under UI_SCALE = 1.0 and 1.5."""
    orig_scale = config.UI_SCALE
    root = tk.Tk()
    root.withdraw()

    try:
        # 1. Test at UI_SCALE = 1.0
        config.UI_SCALE = 1.0
        app1 = MagicMock()
        app1.toolbar_buttons = {}
        app1.toolbar_vars = {}
        app1.add_tooltip = lambda widget, text: None
        parent_frame1 = tk.Frame(root)
        parent_frame1.pack()

        NavigationBar.build_nav_ui(app1, parent_frame1)

        # Verify scaled geometry at 1.0
        nav_bar_height_1 = int(app1.nav_bar.cget("height"))
        assert nav_bar_height_1 == 48

        title_padx_1 = int(app1.nav_title_lbl.cget("padx"))
        assert title_padx_1 == 16

        # Verify progress bar length at 1.0
        progress_len_1 = int(app1.image_scan_progress.cget("length"))
        assert progress_len_1 == 140

        # Verify data_status is created for backward compatibility but NOT packed
        assert hasattr(app1, "data_status")
        assert app1.data_status.winfo_manager() == ""

        # 2. Test at UI_SCALE = 1.5
        config.UI_SCALE = 1.5
        app2 = MagicMock()
        app2.toolbar_buttons = {}
        app2.toolbar_vars = {}
        app2.add_tooltip = lambda widget, text: None
        parent_frame2 = tk.Frame(root)
        parent_frame2.pack()

        NavigationBar.build_nav_ui(app2, parent_frame2)

        # Verify scaled geometry at 1.5: 48 -> 72, 16 -> 24, 140 -> 210
        nav_bar_height_2 = int(app2.nav_bar.cget("height"))
        assert nav_bar_height_2 == 72

        title_padx_2 = int(app2.nav_title_lbl.cget("padx"))
        assert title_padx_2 == 24

        progress_len_2 = int(app2.image_scan_progress.cget("length"))
        assert progress_len_2 == 210

    finally:
        config.UI_SCALE = orig_scale
        root.destroy()


def test_create_collection_dialog_canvas_scroll_binding():
    """Verify CreateCollectionDialog canvas receives ScrollTag_<id> and does not hijack root bind_all."""
    root = tk.Tk()
    root.withdraw()

    try:
        dialog = CreateCollectionDialog(root)

        assert hasattr(dialog, "canvas")
        assert hasattr(dialog, "scrollable_frame")

        tag = f"ScrollTag_{id(dialog.canvas)}"

        # Check tag in canvas bindtags
        assert tag in dialog.canvas.bindtags()

        # Check tag in scrollable_frame bindtags
        assert tag in dialog.scrollable_frame.bindtags()

        # Canvas itself has mousewheel and linux buttons bound
        canvas_bindings = dialog.canvas.bind()
        assert "<MouseWheel>" in canvas_bindings
        assert "<Button-4>" in canvas_bindings
        assert "<Button-5>" in canvas_bindings

        # Global root has no destructive mousewheel hijacking
        assert "<MouseWheel>" not in root.bind()

        dialog.win.destroy()
    finally:
        root.destroy()


def test_startup_dialog_scroll_binding_and_scaling():
    """Verify StartupDialog canvas mousewheel binding and coordinate scaling."""
    root = tk.Tk()
    root.withdraw()

    try:
        mock_app = MagicMock()
        startup = StartupDialog(root, mock_app)

        assert hasattr(startup, "canvas")
        assert hasattr(startup, "_outer")

        tag = f"ScrollTag_{id(startup.canvas)}"

        # Verify tag in canvas and inner frame bindtags
        assert tag in startup.canvas.bindtags()
        assert tag in startup._outer.bindtags()

        # Verify canvas bindings
        canvas_bindings = startup.canvas.bind()
        assert "<MouseWheel>" in canvas_bindings
        assert "<Button-4>" in canvas_bindings
        assert "<Button-5>" in canvas_bindings

        # Global root has no destructive mousewheel hijacking
        assert "<MouseWheel>" not in root.bind()

        startup.win.destroy()
    finally:
        root.destroy()


def test_bind_mousewheel_tag_routing():
    """Verify non-destructive mousewheel tag routing from scroll_helper."""
    from ui.scroll_helper import bind_mousewheel
    root = tk.Tk()
    root.withdraw()
    try:
        canvas = tk.Canvas(root, height=200, width=200)
        canvas.pack()

        frame = tk.Frame(canvas)
        label = tk.Label(frame, text="Inside scroll frame")
        label.pack()

        bind_mousewheel(canvas, frame)

        tag = f"ScrollTag_{id(canvas)}"
        assert tag in frame.bindtags()
        assert tag in label.bindtags()
        assert "<MouseWheel>" not in root.bind()
    finally:
        root.destroy()


def test_show_about_fetches_dynamic_version():
    """Verify show_about dynamically reads config.APP_VERSION and TkVersion."""
    import config
    from ui import help_dialogs

    root = tk.Tk()
    root.withdraw()
    try:
        mock_ui = MagicMock()
        mock_ui.root = root
        mock_ui.dark_mode_active = False
        mock_ui.app = None

        help_dialogs.show_about(mock_ui)
        about_win = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)][0]
        assert about_win.title() == "About Arbor"

        # Inspect labels inside about window to ensure dynamic config.APP_VERSION is shown
        found_version = False
        for child in about_win.winfo_children():
            for sub in getattr(child, "winfo_children", lambda: [])():
                for row in getattr(sub, "winfo_children", lambda: [])():
                    for lbl in getattr(row, "winfo_children", lambda: [])():
                        if isinstance(lbl, tk.Label) and config.APP_VERSION in lbl.cget("text"):
                            found_version = True
        assert found_version, f"Expected {config.APP_VERSION} to be displayed in About dialog"
        about_win.destroy()
    finally:
        root.destroy()


def test_show_shortcuts_data_contains_canonical_keys():
    """Verify show_shortcuts data registry contains Space, Ctrl+S, Ctrl+Enter, keycaps, and Excel impacts."""
    from ui.keybindings import get_canonical_shortcuts, KeybindingManager

    shortcuts = get_canonical_shortcuts()
    assert len(shortcuts) >= 10
    assert KeybindingManager.get_shortcuts_registry() == shortcuts

    # Must contain Space, Ctrl+S, Ctrl+Enter with visual keycaps
    keys_upper = " ".join(item[1] for item in shortcuts).upper()
    assert "[ SPACE ]" in keys_upper
    assert "[ CTRL ] + [ S ]" in keys_upper
    assert "[ CTRL ] + [ ENTER ]" in keys_upper

    # Must contain dual-depth Excel translation bridge impacts
    excel_text = " ".join(item[3] for item in shortcuts if len(item) > 3)
    assert "Reviewed" in excel_text and "Excel" in excel_text
    assert ".xlsx" in excel_text

    # Zero barcode references in shortcuts registry
    full_text = " ".join(" ".join(item) for item in shortcuts)
    assert "barcode" not in full_text.lower()


def test_show_main_help_locates_and_parses_user_guide():
    """Verify show_main_help loads USER_GUIDE.md and provides chapter bookmarks."""
    from ui import help_dialogs

    root = tk.Tk()
    root.withdraw()
    try:
        mock_ui = MagicMock()
        mock_ui.root = root
        mock_ui.dark_mode_active = False

        help_dialogs.show_main_help(mock_ui)
        help_win = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)][0]
        assert "Arbor System User Guide" in help_win.title()

        # Locate text widget
        txt_widget = None
        for child in help_win.winfo_children():
            for sub in getattr(child, "winfo_children", lambda: [])():
                if isinstance(sub, tk.Text):
                    txt_widget = sub
        assert txt_widget is not None
        text_content = txt_widget.get("1.0", "end")
        assert "Welcome to Arbor" in text_content or "Trainee Work Manual" in text_content
        assert "barcode" not in text_content.lower()

        help_win.destroy()
    finally:
        root.destroy()


def test_setting_info_texts_dual_depth_and_lexicon():
    """Verify SETTING_INFO_TEXTS in ui/unified_settings.py has dual-depth learning and no banned terms."""
    from ui.unified_settings import SETTING_INFO_TEXTS

    assert len(SETTING_INFO_TEXTS) >= 10

    banned_terms = ["schema", "rest api", "daemon", "relational join", "serialization", "barcode"]

    for key, text in SETTING_INFO_TEXTS.items():
        lower_text = text.lower()
        for banned in banned_terms:
            assert banned not in lower_text, f"Banned term '{banned}' found in setting '{key}' tooltip"

    # Critical settings must mention Excel/safety impacts
    assert "excel" in SETTING_INFO_TEXTS["focus_fallback"].lower()
    assert "excel" in SETTING_INFO_TEXTS["auto_advance_history"].lower()
    assert "excel" in SETTING_INFO_TEXTS["mobile_autosave_on_stop"].lower()
    assert ".xlsx" in SETTING_INFO_TEXTS["mobile_autosave_on_stop"].lower()


def test_unified_help_reader_and_shortcuts_work_outside_main_ui(tk_root):
    """Verify Help Guide Reader (Desktop/Mobile tabs) and Shortcuts HUD work from StartupDialog/bare Tk root."""
    from ui.help_dialogs import show_main_help, show_shortcuts

    show_main_help(tk_root, initial_tab="desktop", initial_chapter="dont-panic")
    show_main_help(tk_root, initial_tab="mobile")
    show_shortcuts(tk_root)


def test_mobile_guide_zero_barcodes_and_bundled_in_spec():
    """Verify MOBILE_COMPANION_USER_GUIDE.md has zero barcode terms and is bundled in main.spec."""
    import os
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(repo_root, "MOBILE_COMPANION_USER_GUIDE.md"), "r", encoding="utf-8") as f:
        mobile_guide = f.read()
    assert "barcode" not in mobile_guide.lower(), "Zero-barcode rule violated in MOBILE_COMPANION_USER_GUIDE.md"
    assert "Armed Target Shelf" in mobile_guide

    with open(os.path.join(repo_root, "main.spec"), "r", encoding="utf-8") as f:
        spec_text = f.read()
    assert "MOBILE_COMPANION_USER_GUIDE.md" in spec_text
    assert "USER_GUIDE.md" in spec_text


def test_startup_setup_help_dialog_opens_cleanly(tk_root):
    """Regression: StartupDialog._show_setup_help_msg must open without AttributeError (C_MUTED)."""
    from ui.dialogs import StartupDialog

    dlg = StartupDialog.__new__(StartupDialog)
    dlg.win = tk_root
    dlg.load_demo_project = lambda: None
    dlg._show_setup_help_msg()
    tk_root.update_idletasks()
    children = [w for w in tk_root.winfo_children() if isinstance(w, tk.Toplevel)]
    assert any("Setup Guide" in w.title() for w in children)
    for w in children:
        w.destroy()


def test_guide_reader_chapter_click_scrolls_to_top(tk_root):
    """Regression: Clicking a sidebar chapter in Desktop/Mobile Guide must align it to top via yview."""
    from ui.help_dialogs import show_main_help

    for tab in ("desktop", "mobile"):
        show_main_help(tk_root, initial_tab=tab)
        tk_root.update_idletasks()
        tops = [w for w in tk_root.winfo_children() if isinstance(w, tk.Toplevel)]
        reader = tops[-1]

        # Find the Text widget and sidebar buttons
        txt_widgets = []
        buttons = []

        def _walk(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Text):
                    txt_widgets.append(child)
                elif isinstance(child, tk.Button):
                    buttons.append(child)
                _walk(child)

        _walk(reader)
        assert txt_widgets, "Guide reader Text widget not found"
        txt = txt_widgets[0]
        # Pick a chapter button from the middle of the sidebar (skip header/tab/action buttons)
        chapter_btns = [b for b in buttons if b.cget("anchor") == "w"]
        assert len(chapter_btns) >= 3, f"Expected >= 3 chapter buttons in {tab} guide"
        chapter_btns[2].invoke()
        tk_root.update_idletasks()
        # yview()[0] should have scrolled past the very top of the document
        assert txt.yview()[0] > 0.0, f"Clicking sidebar chapter in {tab} guide did not scroll pane"
        reader.destroy()


def test_mobile_dialog_scrollable_and_dpi_safe(tk_root, monkeypatch):
    """Verify MobileDialog wraps MobilePanel in a scrollable canvas with compact DPI-safe minsize."""
    from ui.mobile_dialog import MobileDialog
    from models import AppState

    class _DummyParentUI:
        dark_mode_active = True
        simultaneous_edit_var = tk.BooleanVar(value=True)
        root = tk_root

    monkeypatch.setattr("ui.mobile_dialog.MobilePanel", lambda **kw: type("P", (), {"server": None, "stop": lambda s: None})())
    dlg = MobileDialog(_DummyParentUI(), tk_root, AppState())
    tk_root.update_idletasks()
    assert hasattr(dlg, "_scroll_canvas")
    assert dlg.win.cget("bg") == "#1e211f"
    min_w, min_h = dlg.win.minsize()
    assert min_h <= 550, f"Expected compact laptop-safe minsize height, got {min_h}"
    dlg.win.destroy()


def test_multimonitor_negative_coordinates_positioning(tk_root, monkeypatch):
    """Verify helper, ToastManager, and center_and_fit_toplevel preserve negative secondary-monitor coordinates."""
    import utils
    from ui.toast import ToastManager

    # 1. Signed Tk geometry formatter never produces "+-" syntax
    assert utils.format_tk_geometry(-1200, -150, 500, 400) == "500x400-1200-150"
    assert utils.format_tk_geometry(-45, 80) == "-45+80"

    # 2. center_and_fit_toplevel centers over a master placed on a left/upper secondary monitor
    monkeypatch.setattr(tk_root, "winfo_viewable", lambda: True)
    monkeypatch.setattr(tk_root, "winfo_width", lambda: 1400)
    monkeypatch.setattr(tk_root, "winfo_height", lambda: 900)
    monkeypatch.setattr(tk_root, "winfo_rootx", lambda: -1600)
    monkeypatch.setattr(tk_root, "winfo_rooty", lambda: -100)

    child = tk.Toplevel(tk_root)
    recorded_geoms = []
    orig_geom = child.geometry

    def _capture_geom(g=None):
        if g is not None:
            recorded_geoms.append(g)
        return orig_geom(g) if g is not None else orig_geom()

    monkeypatch.setattr(child, "geometry", _capture_geom)
    utils.center_and_fit_toplevel(child, 500, 400)
    assert recorded_geoms, "Expected geometry to be applied"
    assert "+-" not in recorded_geoms[-1]
    assert "-1150" in recorded_geoms[-1]  # -1600 + (1400 - 500)//2 = -1150
    child.destroy()

    # 3. ToastManager renders cleanly with signed negative coordinates without raising TclError
    ToastManager.show(tk_root, "Saved on secondary monitor", toast_type="success", duration_ms=5000)
    assert ToastManager._active_toast is not None and ToastManager._active_toast.winfo_exists()
    ToastManager.dismiss()





