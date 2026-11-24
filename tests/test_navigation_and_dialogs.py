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
    assert "Set Shelf" in mobile_guide

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
    assert any("How to Open Arbor" in w.title() for w in children)
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

    # 1. Tk geometry formatter uses explicit '+' anchor ('+-') so negative X/Y stay on secondary monitors
    assert utils.format_tk_geometry(-1200, -150, 500, 400) == "500x400+-1200+-150"
    assert utils.format_tk_geometry(-45, 80) == "+-45+80"

    # Live Tk check: '+-500+100' keeps winfo_x at -500 (whereas '-500+100' teleports onto primary monitor)
    probe = tk.Toplevel(tk_root)
    probe.withdraw()
    probe.geometry(utils.format_tk_geometry(-500, 100, 200, 100))
    probe.update_idletasks()
    assert probe.winfo_x() == -500
    probe.destroy()

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
    assert "+-1150" in recorded_geoms[-1]  # -1600 + (1400 - 500)//2 = -1150
    child.destroy()

    # 3. ToastManager renders cleanly with signed negative coordinates without raising TclError
    ToastManager.show(tk_root, "Saved on secondary monitor", toast_type="success", duration_ms=5000)
    assert ToastManager._active_toast is not None and ToastManager._active_toast.winfo_exists()
    ToastManager.dismiss()


def test_legacy_note_reveal_and_safe_merge_into_comment(tk_root):
    """Verify Option A: blank Observation/ProblemDescription stay hidden, non-empty ones reveal, and merge is non-destructive."""
    import pandas as pd
    from models import AppState
    from ui.registry_panel import RegistryPanel

    app = AppState()
    app.config = {
        "ui_sections": {
            "registration": [
                {"name": "Comment", "type": "multiline"},
                {"name": "Observation", "type": "multiline"},
                {"name": "ProblemDescription", "type": "multiline"},
            ],
            "problems": [],
        }
    }
    app.df_reg = pd.DataFrame(
        [
            {"ObjectID": "1", "Comment": "Existing note", "Observation": "", "ProblemDescription": "Faded pencil"},
            {"ObjectID": "2", "Comment": "", "Observation": "Bent stem", "ProblemDescription": ""},
            {"ObjectID": "3", "Comment": "Clean", "Observation": "", "ProblemDescription": ""},
        ]
    ).set_index("ObjectID", drop=False)
    app.current_object_id = "1"

    class _DummyUI:
        def __init__(self, root, app_state):
            self.root = root
            self.app = app_state
            self.object_loaded = True
            self.loading_object = True
            self.focus_mode_var = tk.BooleanVar(value=False)
            self.focus_fallback_var = tk.BooleanVar(value=True)
            self.snap_lock_var = tk.BooleanVar(value=False)
            self.focus_visibility_vars = {}
            self.problem_to_field = {}
            self.problem_vars = {}
            self.reg_vars = {}
            self.reg_entries = {}
            self.reg_row_frames = {}
            self.card_frames = {}
            self.card_defs_ordered = []
            container = tk.Frame(root)
            container.pack()
            for r, name in enumerate(("Comment", "Observation", "ProblemDescription")):
                f = tk.Frame(container)
                f.grid(row=r, column=0)
                t = tk.Text(f, height=2)
                t.pack()
                self.reg_row_frames[name] = f
                self.reg_entries[name] = t

    ui = _DummyUI(tk_root, app)
    # Specimen 1: Comment + ProblemDescription non-empty, Observation empty
    ui.reg_entries["Comment"].insert("1.0", "Existing note")
    ui.reg_entries["ProblemDescription"].insert("1.0", "Faded pencil")
    RegistryPanel.update_reg_fields_visibility(ui)

    assert ui.reg_row_frames["Comment"].winfo_manager() == "grid"
    assert ui.reg_row_frames["ProblemDescription"].winfo_manager() == "grid"
    assert ui.reg_row_frames["Observation"].winfo_manager() == ""

    # Run non-destructive opt-in merge (interactive=False)
    merged_count = RegistryPanel.merge_legacy_notes_into_comment(ui, interactive=False)
    assert merged_count == 2
    assert app.dirty is True
    # Existing comment preserved, legacy note appended cleanly
    assert "Existing note" in app.df_reg.loc["1", "Comment"]
    assert "[Legacy Problem Note]: Faded pencil" in app.df_reg.loc["1", "Comment"]
    assert app.df_reg.loc["1", "ProblemDescription"] == ""
    # Row 2 (empty Comment) gets clean Observation text without redundant prefix
    assert app.df_reg.loc["2", "Comment"] == "Bent stem"
    assert app.df_reg.loc["2", "Observation"] == ""
    # Row 3 untouched
    assert app.df_reg.loc["3", "Comment"] == "Clean"
    # Second run is a no-op (idempotent)
    assert RegistryPanel.merge_legacy_notes_into_comment(ui, interactive=False) == 0


# ============================================================================
# Merged from test_collection_dialog.py
# ============================================================================

import os
import pytest
import tkinter as tk
from ui.create_collection_dialog import CreateCollectionDialog, create_standard_collection_file, SHEET_BLUEPRINT_INFO
from ui.dialogs import CreateCollectionDialog as ReexportedDialog
from repository import ExcelRepository
import config

def test_sheet_blueprint_info_completeness():
    assert "reg" in SHEET_BLUEPRINT_INFO
    assert "obs" in SHEET_BLUEPRINT_INFO
    assert "log" in SHEET_BLUEPRINT_INFO

    for key, info in SHEET_BLUEPRINT_INFO.items():
        assert "title" in info
        assert "badge" in info
        assert "summary" in info
        assert "chips" in info
        assert "new_curator_bullets" in info
        assert "curator_bullets" in info
        assert len(info["chips"]) > 0
        assert "🌱" in info["new_curator_bullets"]
        assert "🏛️" in info["curator_bullets"]

def test_reexported_dialog_is_identical():
    assert ReexportedDialog is CreateCollectionDialog

def test_create_standard_collection_file(tmp_path):
    target = str(tmp_path / "test_new_collection.xlsx")
    create_standard_collection_file(target)

    assert os.path.exists(target)

    cfg = config.DATABASE_CONFIGS.get("Økonomisk Botanisk")
    assert cfg is not None

    df_reg, df_obs, df_photo, df_log, df_unval = ExcelRepository.load_excel(target, cfg)

    # 1 sample specimen created
    assert len(df_reg) == 1
    assert len(df_obs) == 1
    assert "ObjectID" in df_reg.columns
    assert "Genus" in df_reg.columns
    assert "Species" in df_reg.columns
    assert "UID" in df_reg.columns
    assert df_reg.iloc[0]["Genus"] == "Welwitschia"
    assert df_reg.iloc[0]["Species"] == "mirabilis"

    # Observation verification
    assert "PlantPart_Problem" in df_obs.columns
    assert "Building" in df_obs.columns
    assert df_obs.iloc[0]["PlantPart_Problem"] == False

    # Log verification
    assert len(df_log) >= 1
    assert "Action" in df_log.columns
    assert df_log.iloc[0]["Action"] == "DATABASE_CREATED"

    # Unvalidated source exists
    assert isinstance(df_unval, type(df_reg))


# ============================================================================
# Merged from test_group_editor.py
# ============================================================================

import tkinter as tk
from ui.group_editor import FieldGroupEditorDialog

def test_field_group_editor_dialog_init():
    root = tk.Tk()
    root.withdraw()  # hide main window

    all_fields = ["Genus", "Species", "Collector", "CustomField"]
    current_groups = [
        {"name": "Taxonomy", "fields": ["Genus", "Species"]},
        {"name": "Collection", "fields": ["Collector"]}
    ]

    saved_groups = []
    def on_save(groups):
        saved_groups.append(groups)

    # Instantiate dialog
    dialog = FieldGroupEditorDialog(root, all_fields, current_groups, on_save)

    # 1. Verify Groups initialization
    # Miscellaneous tab should have been automatically added for "CustomField"
    assert len(dialog.groups) == 3
    assert dialog.groups[0]["name"] == "Taxonomy"
    assert dialog.groups[1]["name"] == "Collection"
    assert dialog.groups[2]["name"] == "Miscellaneous"
    assert dialog.groups[2]["fields"] == ["CustomField"]

    # 2. Verify Tab Listbox population
    assert dialog.tabs_listbox.size() == 3
    assert dialog.tabs_listbox.get(0) == "Taxonomy"
    assert dialog.tabs_listbox.get(1) == "Collection"
    assert dialog.tabs_listbox.get(2) == "Miscellaneous"

    # 3. Save Settings should trigger the callback
    dialog.save_settings()
    assert len(saved_groups) == 1
    assert saved_groups[0][0]["name"] == "Taxonomy"
    assert saved_groups[0][2]["name"] == "Miscellaneous"

    root.destroy()

def test_field_group_editor_dialog_move_field():
    root = tk.Tk()
    root.withdraw()

    all_fields = ["Genus", "Species"]
    current_groups = [
        {"name": "Taxonomy", "fields": ["Genus", "Species"]}
    ]

    dialog = FieldGroupEditorDialog(root, all_fields, current_groups, lambda g: None)

    # Select the Taxonomy tab
    dialog.tabs_listbox.selection_clear(0, tk.END)
    dialog.tabs_listbox.selection_set(0)
    dialog.on_tab_select(None)

    # Check fields in the listbox
    assert dialog.fields_listbox.size() == 2
    assert dialog.fields_listbox.get(0) == "Genus"
    assert dialog.fields_listbox.get(1) == "Species"

    # Select "Genus" (index 0) and move it down
    dialog.fields_listbox.selection_clear(0, tk.END)
    dialog.fields_listbox.selection_set(0)

    dialog.move_field_order(1)  # move down

    # Genus and Species should have swapped places
    assert dialog.groups[0]["fields"] == ["Species", "Genus"]

    root.destroy()


# ============================================================================
# Merged from test_add_objects.py
# ============================================================================

import pytest
import tkinter as tk
import pandas as pd
from ui.add_objects import AddObjectsWizard
from repository import REVIEWED_COLUMN

class DummyApp:
    def __init__(self):
        self.config_name = "Test DB"
        self.config = {
            "ui_sections": {
                "registration": [
                    {"name": "Genus", "type": "text"},
                    {"name": "Species", "type": "text"},
                    {"name": "Status", "type": "choice", "choices": ["Valid", "Draft"]}
                ],
                "location": [
                    {"name": "Building", "type": "text"},
                    {"name": "Floor", "type": "choice", "choices": ["1", "2"]},
                    {"name": "Is_Cabinet", "type": "checkbox"}
                ],
                "problems": [
                    {"name": "Images_Problem", "type": "bool"},
                    {"name": "Other_problem", "type": "bool"}
                ]
            }
        }
        self.df_reg = pd.DataFrame(
            {"Genus": ["Quercus"], "Species": ["robur"], "Status": ["Valid"]},
            index=["1"]
        )
        self.df_reg.index.name = "ObjectID"
        self.df_obs = pd.DataFrame(
            {
                "Building": ["Main"], "Floor": ["1"], "Is_Cabinet": ["True"],
                "Images_Missing": [False], "Images_Problem": [False], "Images_Wrong": [False],
                REVIEWED_COLUMN: [False], "ReviewedAt": [""], "Online_Images_Exist": [False],
                "Other_problem": [False]
            },
            index=["1"]
        )
        self.df_obs.index.name = "ObjectID"
        self.df_photo = pd.DataFrame()
        self.active_object_ids = ["1"]
        self.dirty = False

class DummyMainWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.refreshed = False
        self.invalidated_cache = False
        self.invalidated_search = False
        self.dirty_updated = False
        self.count_updated = False
        self.progress_updated = False
        self.logged_actions = []

    def _invalidate_row_cache(self):
        self.invalidated_cache = True

    def invalidate_search_index(self):
        self.invalidated_search = True

    def refresh_list(self):
        self.refreshed = True

    def update_dirty_ui(self):
        self.dirty_updated = True

    def update_object_count(self):
        self.count_updated = True

    def update_review_progress(self):
        self.progress_updated = True

    def log_action(self, action, fields, details):
        self.logged_actions.append((action, fields, details))

from unittest.mock import patch

@pytest.fixture
def tk_env():
    root = tk.Tk()
    root.withdraw()
    app = DummyApp()
    mw = DummyMainWindow(root, app)
    with patch("tkinter.messagebox.showinfo"), \
         patch("tkinter.messagebox.showwarning"), \
         patch("tkinter.messagebox.showerror"):
        yield root, app, mw
    try:
        root.destroy()
    except Exception:
        pass

def test_wizard_init_and_render_step1(tk_env):
    root, app, mw = tk_env
    wizard = AddObjectsWizard(root, app, mw)
    assert wizard.win is not None
    assert wizard.current_step == 0
    assert wizard.subtitle_lbl.cget("text") == "1. Object IDs"
    assert wizard.target_listbox is not None
    wizard.win.destroy()

def test_auto_id_generation(tk_env):
    root, app, mw = tk_env
    wizard = AddObjectsWizard(root, app, mw)
    wizard.auto_n_var.set(3)
    wizard._generate_auto_ids()
    
    # Existing max numeric ID was 1, so auto generates 2, 3, 4
    target_oids = wizard._get_target_oids()
    assert target_oids == ["2", "3", "4"]
    assert "2" in wizard.staged_data
    assert "3" in wizard.staged_data
    assert "4" in wizard.staged_data
    wizard.win.destroy()

def test_manual_id_addition_and_removal(tk_env):
    root, app, mw = tk_env
    wizard = AddObjectsWizard(root, app, mw)
    wizard.manual_ids_var.set("A10, B20, 1") # 1 already exists in df_reg
    wizard._add_manual_ids()
    
    target_oids = wizard._get_target_oids()
    assert "A10" in target_oids
    assert "B20" in target_oids
    assert "1" not in target_oids # Prevent duplicates with database
    
    # Select A10 and remove it
    wizard.target_listbox.selection_clear(0, tk.END)
    wizard.target_listbox.selection_set(0)
    wizard._remove_selected_id()
    assert "A10" not in wizard._get_target_oids()
    assert "A10" not in wizard.staged_data
    assert "B20" in wizard._get_target_oids()
    wizard.win.destroy()

def test_step_transitions_and_metadata_editing(tk_env):
    root, app, mw = tk_env
    wizard = AddObjectsWizard(root, app, mw)
    wizard.manual_ids_var.set("OBJ_X")
    wizard._add_manual_ids()
    
    # Advance to step 2
    wizard._on_next()
    assert wizard.current_step == 1
    assert wizard.subtitle_lbl.cget("text") == "2. Initial Metadata"
    assert "Genus" in wizard.field_vars
    
    wizard.field_vars["Genus"].set("Betula")
    wizard.field_vars["Building"].set("North Wing")
    
    # Advance to step 3
    wizard._on_next()
    assert wizard.current_step == 2
    assert wizard.subtitle_lbl.cget("text") == "3. Review & Create"
    assert wizard.staged_data["OBJ_X"]["Genus"] == "Betula"
    assert wizard.staged_data["OBJ_X"]["Building"] == "North Wing"
    
    # Go back to step 2
    wizard._on_back()
    assert wizard.current_step == 1
    wizard.win.destroy()

def test_create_objects_commit(tk_env):
    root, app, mw = tk_env
    wizard = AddObjectsWizard(root, app, mw)
    wizard.manual_ids_var.set("NEW_1, NEW_2")
    wizard._add_manual_ids()
    
    # Customize NEW_1
    wizard.staged_data["NEW_1"]["Genus"] = "Acer"
    wizard.staged_data["NEW_1"]["Building"] = "Herbarium"
    
    wizard._create_objects()
    
    # Verify DataFrames updated
    assert "NEW_1" in app.df_reg.index
    assert "NEW_2" in app.df_reg.index
    assert app.df_reg.loc["NEW_1", "Genus"] == "Acer"
    assert app.df_obs.loc["NEW_1", "Building"] == "Herbarium"
    assert bool(app.df_obs.loc["NEW_1", "Images_Missing"]) is True
    assert bool(app.df_obs.loc["NEW_1", REVIEWED_COLUMN]) is False
    
    assert "NEW_1" in app.active_object_ids
    assert "NEW_2" in app.active_object_ids
    assert app.dirty is True
    assert mw.refreshed is True
    assert mw.invalidated_cache is True


    assert len(mw.logged_actions) == 2


# ============================================================================
# Merged from test_recent_activity_dialog.py
# ============================================================================

import pytest
import tkinter as tk
import pandas as pd
from ui.recent_activity_dialog import RecentActivityDialog, open_recent_activity_dialog, COLORS_DARK


@pytest.fixture
def tk_root():
    try:
        root = tk.Tk()
        root.withdraw()
        yield root
        root.destroy()
    except Exception as e:
        pytest.skip(f"Tkinter display not available: {e}")


@pytest.fixture
def mock_data():
    mock_history = ["1001", "1002", "1003"]
    mock_df_log = pd.DataFrame([
        {
            "Timestamp": "2026-08-17T10:15:30.123",
            "Action": "EDIT",
            "ObjectID": "1001",
            "ChangedFields": "Genus",
            "ChangedValues": "Pinus  Abies",
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "",
            "LocationChangedValues": ""
        },
        {
            "Timestamp": "2026-08-17T10:45:00.000",
            "Action": "RESOLVE_HISTORICAL_CONFLICT",
            "ObjectID": "1002",
            "ChangedFields": "Species",
            "ChangedValues": "sylvestris  alba",
            "ProblemsChanged": "Species_Problem",
            "ProblemsChangedValues": "True  False",
            "LocationChanged": "",
            "LocationChangedValues": ""
        },
        {
            "Timestamp": "2026-08-17T11:00:00.000",
            "Action": "MOBILE_EDIT",
            "ObjectID": "1003",
            "ChangedFields": "Family",
            "ChangedValues": "Pinaceae  Betulaceae",
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "",
            "LocationChangedValues": ""
        }
    ])
    return mock_history, mock_df_log


def test_recent_activity_dialog_init(tk_root, mock_data):
    history, df_log = mock_data
    dialog = open_recent_activity_dialog(tk_root, history_stack=history, df_log=df_log, default_tab=0)
    assert isinstance(dialog, RecentActivityDialog)
    assert dialog.title() == "Recent Activity"
    assert dialog.active_tab_name == "visited"

    # Visited rows populated
    items = dialog.tree_v.get_children()
    assert len(items) == 3

    dialog.destroy()


def test_recent_activity_dialog_tab_switch(tk_root, mock_data):
    history, df_log = mock_data
    dialog = open_recent_activity_dialog(tk_root, history_stack=history, df_log=df_log, default_tab=1)
    assert dialog.active_tab_name == "edits"

    items = dialog.tree_e.get_children()
    assert len(items) == 3

    dialog.destroy()


def test_recent_activity_dark_mode(tk_root, mock_data):
    history, df_log = mock_data
    dialog = open_recent_activity_dialog(tk_root, history_stack=history, df_log=df_log, dark_mode=True)
    assert dialog.colors == COLORS_DARK
    dialog.destroy()


def test_visited_header_sorting(tk_root, mock_data):
    history, df_log = mock_data
    dialog = open_recent_activity_dialog(tk_root, history_stack=history, df_log=df_log, default_tab=0)

    # Initial sort for visited is desc by ObjectID (1003, 1002, 1001)
    items = dialog.tree_v.get_children()
    first_id = dialog.tree_v.item(items[0])["values"][0]
    assert str(first_id) == "1003"

    # Sort ascending by clicking ObjectID header
    dialog._sort_visited("ObjectID")
    items = dialog.tree_v.get_children()
    first_id = dialog.tree_v.item(items[0])["values"][0]
    assert str(first_id) == "1001"

    dialog.destroy()


def test_edits_header_sorting(tk_root, mock_data):
    history, df_log = mock_data
    dialog = open_recent_activity_dialog(tk_root, history_stack=history, df_log=df_log, default_tab=1)

    # Sort by Action column
    dialog._sort_edits("Action")
    items = dialog.tree_e.get_children()
    assert len(items) == 3
    act0 = dialog.tree_e.item(items[0])["values"][2]
    act1 = dialog.tree_e.item(items[1])["values"][2]
    act2 = dialog.tree_e.item(items[2])["values"][2]
    assert act0 <= act1 <= act2

    dialog.destroy()


def test_search_and_action_filtering(tk_root, mock_data):
    history, df_log = mock_data
    dialog = open_recent_activity_dialog(tk_root, history_stack=history, df_log=df_log, default_tab=1)

    # Test Search Query
    dialog.search_query.set("1002")
    items = dialog.tree_e.get_children()
    assert len(items) == 1
    assert str(dialog.tree_e.item(items[0])["values"][0]) == "1002"

    # Reset search query
    dialog.search_query.set("")
    items = dialog.tree_e.get_children()
    assert len(items) == 3

    # Test Action Filter Chip: Manual Edit
    dialog._set_action_filter("Manual Edit")
    items = dialog.tree_e.get_children()
    assert len(items) == 1
    assert dialog.tree_e.item(items[0])["values"][2] == "Manual Edit"

    # Test Action Filter Chip: Mobile Edit
    dialog._set_action_filter("Mobile Edit")
    items = dialog.tree_e.get_children()
    assert len(items) == 1
    assert dialog.tree_e.item(items[0])["values"][2] == "Mobile Edit"
    assert str(dialog.tree_e.item(items[0])["values"][0]) == "1003"

    dialog.destroy()


def test_callbacks_invocation(tk_root, mock_data):
    history, df_log = mock_data
    nav_events = []
    ref_events = []
    close_events = []

    callbacks = {
        "on_navigate": lambda oid: nav_events.append(oid),
        "on_refresh": lambda: ref_events.append(True),
        "on_close": lambda: close_events.append(True)
    }

    dialog = open_recent_activity_dialog(
        tk_root, history_stack=history, df_log=df_log,
        live_callbacks=callbacks, default_tab=0
    )

    # Refresh callback
    dialog._handle_refresh()
    assert len(ref_events) == 1

    # Select item & navigate callback
    items = dialog.tree_v.get_children()
    dialog.tree_v.selection_set(items[0])
    target_oid = str(dialog.tree_v.item(items[0])["values"][0])
    dialog._do_navigate()

    assert len(nav_events) == 1
    assert nav_events[0] == target_oid
    assert len(close_events) == 1


# ============================================================================
# Merged from test_status_bar.py
# ============================================================================

"""Tests for decoupled StatusBarPanel and layout settings dead widget purge.

Verifies:
1. StatusBarPanel initializes cleanly without creating sb_top, sb_buttons_frame,
   sb_settings_btn, or sb_help_btn frames, and maintains height ~26px.
2. update_status(total=50, reviewed=25, problems=5) correctly formats telemetry.
3. Theme switching (apply_light_theme and apply_dark_theme) does not raise
   AttributeError or TclError.
"""

import pytest
import tkinter as tk
from tkinter import ttk

from ui.status_bar import StatusBarPanel
from ui.layout_settings import LayoutSettingsMixin


class MockApp:
    """Mock Application state for testing."""
    def __init__(self):
        self.active_object_ids = ["OBJ-001", "OBJ-002"]
        self.df_reg = None
        self.df_obs = None


class MockUI(LayoutSettingsMixin):
    """Mock MainWindow implementing LayoutSettingsMixin with minimal Tkinter structure."""
    def __init__(self, root):
        self.root = root
        self.app = MockApp()
        self.dark_mode_active = False

        # Status bar containers
        statusbar_bg = "#1c1b1b"
        self._status_bar_frame = tk.Frame(self.root, bg=statusbar_bg, height=26)
        self._status_bar_frame.pack(side="bottom", fill="x")

        # Mock collections expected by LayoutSettingsMixin.apply_theme
        self.reg_entries = {}
        self.location_entries = {}
        self.problem_switches = {}
        self.review_card_buttons = {}
        self.toolbar_buttons = {}
        self.toolbar_vars = {}
        self.filter_buttons = {}

        # Mock treeview for tag_configure
        self.object_list = ttk.Treeview(self.root)
        self.object_list.pack()

        # Instantiate decoupled status bar panel
        self.status_bar_panel = StatusBarPanel(self._status_bar_frame, self)

    def _open_unified(self):
        pass

    def open_help_window(self):
        pass

    def show_statistics(self):
        pass

    def open_log_viewer_window(self):
        pass


@pytest.fixture
def status_bar_tk_env():
    """Create a hidden Tk root and MockUI instance for tests, destroying on teardown."""
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter display unavailable in test environment")

    root.withdraw()
    ui = MockUI(root)
    root.update_idletasks()

    yield root, ui

    try:
        root.destroy()
    except Exception:
        pass


def test_status_bar_initialization_and_dead_widget_purge(status_bar_tk_env):
    """Verify StatusBarPanel constructs cleanly at ~26px height without creating sb_top frames."""
    root, ui = status_bar_tk_env
    panel = ui.status_bar_panel

    # Ensure sb_top and obsolete button stubs are None properties (not Tk widgets)
    assert panel.sb_top is None
    assert panel.sb_buttons_frame is None
    assert panel.sb_settings_btn is None
    assert panel.sb_help_btn is None

    # Verify stubs can be set without raising AttributeError
    panel.sb_top = "test_ignore"
    assert panel.sb_top is None

    # Verify ui backward-compatibility stubs do not hold live dead widgets
    assert not hasattr(ui, "sb_top") or getattr(ui, "sb_top") is None
    assert not hasattr(ui, "sb_buttons_frame") or getattr(ui, "sb_buttons_frame") is None
    assert not hasattr(ui, "sb_settings_btn") or getattr(ui, "sb_settings_btn") is None
    assert not hasattr(ui, "sb_help_btn") or getattr(ui, "sb_help_btn") is None

    # Verify sb_bottom points to the live status bar frame
    assert panel.sb_bottom == ui._status_bar_frame
    assert ui.sb_bottom == ui._status_bar_frame

    # Verify height is ~26px (within standard font/DPI variance 18px-34px)
    req_h = ui._status_bar_frame.winfo_reqheight()
    assert 18 <= req_h <= 34, f"Expected height ~26px, got {req_h}px"

    # Verify children: no child is or contains an sb_top frame
    children = ui._status_bar_frame.winfo_children()
    for child in children:
        assert getattr(child, "name", "") != "sb_top"

    # Verify critical specimen telemetry widgets exist and are packed
    assert "object_count" in panel.labels
    assert "reviewed" in panel.labels
    assert "problems" in panel.labels
    assert "last_save" in panel.labels
    assert panel.filter_active_badge is not None
    assert panel.filter_active_badge.winfo_exists()


def test_status_bar_update_status_telemetry(status_bar_tk_env):
    """Verify update_status correctly formats OBJECT_COUNT, REVIEWED, and PROBLEMS."""
    root, ui = status_bar_tk_env
    panel = ui.status_bar_panel

    # Test exact requirement values: total=50, reviewed=25, problems=5
    panel.update_status(total=50, reviewed=25, problems=5)

    assert panel.labels["object_count"].cget("text") == "Specimens: 50"
    assert panel.labels["reviewed"].cget("text") == "Reviewed: 25"
    assert panel.labels["problems"].cget("text") == "Problems: 5"
    # When problems > 0, problems label foreground must highlight in red (#ff6b6b)
    assert panel.problems_lbl.cget("foreground") == "#ff6b6b"

    # Test with 0 problems and large count formatting
    panel.update_status(total=5000, reviewed="100%", problems=0, last_save="12:00:00")
    assert panel.labels["object_count"].cget("text") == "Specimens: 5,000"
    assert panel.labels["reviewed"].cget("text") == "Reviewed: 100%"
    assert panel.labels["problems"].cget("text") == "Problems: 0"
    assert panel.labels["last_save"].cget("text") == "Last Saved: 12:00:00"
    assert panel.problems_lbl.cget("foreground") == "#e2e2e2"


def test_status_bar_theme_switching_no_errors(status_bar_tk_env):
    """Verify theme switching (apply_light_theme and apply_dark_theme) executes cleanly."""
    root, ui = status_bar_tk_env

    # 1. Apply dark theme
    ui.apply_dark_theme()
    assert ui.dark_mode_active is True
    root.update_idletasks()

    # Verify status bar theming succeeded in dark mode (#141715)
    assert ui.sb_bottom.cget("background") == "#141715"

    # 2. Apply light theme
    ui.apply_light_theme()
    assert ui.dark_mode_active is False
    root.update_idletasks()

    # Verify status bar theming succeeded in light mode (#2c302e)
    assert ui.sb_bottom.cget("background") == "#2c302e"

    # 3. Toggle dark mode back and forth to ensure registration doesn't reference dead widgets
    ui.toggle_dark_mode()
    assert ui.dark_mode_active is True
    root.update_idletasks()
    assert ui.sb_bottom.cget("background") == "#141715"

    ui.toggle_dark_mode()
    assert ui.dark_mode_active is False
    root.update_idletasks()
    assert ui.sb_bottom.cget("background") == "#2c302e"


def test_in_app_user_manuals_stay_synced_with_ui():
    """CI/pytest guard: bundled in-app manuals must never drift back to retired UI labels."""
    import os

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    user_guide = open(os.path.join(root_dir, "USER_GUIDE.md"), encoding="utf-8").read()
    mobile_guide = open(os.path.join(root_dir, "MOBILE_COMPANION_USER_GUIDE.md"), encoding="utf-8").read()
    cheat_sheet = open(
        os.path.join(root_dir, "documentation", "curator", "KEYBOARD_SHORTCUTS_CHEAT_SHEET.md"),
        encoding="utf-8",
    ).read()

    retired_labels = (
        "Armed Target Shelf",
        "Stamp to This Shelf",
        "Stamp Target",
        "Details ↔ Location ↔ Problems",
        "HELP ▾",
        "Quick Tour (Cabinet 21)",
    )
    for doc_name, text in (
        ("USER_GUIDE.md", user_guide),
        ("MOBILE_COMPANION_USER_GUIDE.md", mobile_guide),
    ):
        for retired in retired_labels:
            assert retired not in text, f"Stale UI label '{retired}' found in {doc_name}"

    # Verify current core workflows are documented in the live bundled manuals
    for required in ("Set Shelf", "Old names", "Details ↔ Location ↔ History"):
        assert required in user_guide, f"Missing '{required}' in USER_GUIDE.md"
        assert required in mobile_guide, f"Missing '{required}' in MOBILE_COMPANION_USER_GUIDE.md"

    assert "OPEN HELP CENTER" in cheat_sheet


def test_unified_help_and_old_names_dialogs_smoke(tk_root):
    """Smoke test: UnifiedHelpWindow (all 5 tabs) & OldNamesDialog open, bind <Escape>, and close cleanly."""
    from unittest.mock import MagicMock, patch
    from ui.unified_help import UnifiedHelpWindow
    from ui.old_names_dialog import OldNamesDialog
    from backend import gbif as gbif_mod
    import pandas as pd

    mock_ui = MagicMock()
    mock_ui.root = tk_root
    mock_ui.dark_mode_active = False
    mock_ui.app = MagicMock()
    mock_ui.app.current_object_id = "110"
    mock_ui.app.excel_path = None
    mock_ui.app.df_log = pd.DataFrame()
    mock_ui.app.historical_dbs = []
    mock_ui.app.df_reg = pd.DataFrame(
        [{"ObjectID": "110", "Genus": "Ephedra", "Species": "major", "Family": "Asteraceae"}]
    ).set_index("ObjectID", drop=False)
    mock_ui.reg_vars = {
        "Genus": tk.StringVar(master=tk_root, value="Ephedra"),
        "Species": tk.StringVar(master=tk_root, value="major"),
        "Family": tk.StringVar(master=tk_root, value="Asteraceae"),
    }

    # 1. UnifiedHelpWindow opens cleanly, binds <Escape>, and renders all 5 tabs
    help_win = UnifiedHelpWindow(tk_root, mock_ui)
    try:
        assert help_win.win.winfo_exists()
        assert help_win.win.bind("<Escape>")
        for tab_key in ("tutorials", "guides", "manuals", "shortcuts", "about"):
            help_win.show_tab(tab_key)
            tk_root.update_idletasks()
    finally:
        if help_win.win.winfo_exists():
            help_win.win.destroy()

    # 2. OldNamesDialog opens cleanly, binds <Escape>, and renders offline family aliases
    with patch.object(gbif_mod, "get_synonyms", return_value={
        "registered_name": "Ephedra major",
        "registered_family": "Asteraceae",
        "old_families": [{"name": "Compositae", "note": "Classical name for Asteraceae"}],
        "primary_synonyms": [],
        "other_synonyms": [],
        "offline": True,
        "from_cache": False,
    }):
        old_dlg = OldNamesDialog(mock_ui)
        try:
            assert old_dlg.win.winfo_exists()
            assert old_dlg.win.bind("<Escape>")
            tk_root.update_idletasks()
        finally:
            if old_dlg.win.winfo_exists():
                old_dlg.win.destroy()
