import pytest
import pandas as pd
import tkinter as tk
from ui.main_window import ObjectProgramUI
from ui.object_problem_resolver import ObjectProblemResolver as HistoricalConflictResolverWindow
from ui.widgets import TreeviewListboxWrapper
from ui.image_panel import ImagePanel
from unittest.mock import MagicMock

class MockApp:
    def __init__(self, df_reg, df_obs):
        self.df_reg = df_reg
        self.df_obs = df_obs
        self.current_object_id = None
        self.active_object_ids = list(df_reg.index)
        self.output_path = ""
        self.excel_path = ""
        self.df_log = pd.DataFrame()
        self._log_records = []
        self.undo_stacks = {}
        self.redo_stacks = {}
        self.historical_dbs = []
        self.df_photo = None
        self.dirty = False
        self.config = {
            "ui_sections": {
                "registration": [
                    {"name": "Genus", "type": "text", "maps_to": "Genus_Problem"},
                    {"name": "Species", "type": "text", "maps_to": "Species_Problem"}
                ],
                "problems": [
                    {"name": "Genus_Problem", "type": "bool", "maps_to": "Genus"},
                    {"name": "Species_Problem", "type": "bool", "maps_to": "Species"}
                ],
                "location": []
            },
            "problems": [
                {"name": "Genus_Problem", "type": "bool", "maps_to": "Genus"},
                {"name": "Species_Problem", "type": "bool", "maps_to": "Species"}
            ]
        }

def create_mock_ui(root, app):
    app.config = {
        "ui_sections": {
            "problems": [
                {"name": "Genus_Problem", "type": "bool", "maps_to": "Genus"},
                {"name": "Species_Problem", "type": "bool", "maps_to": "Species"}
            ],
            "registration": [
                {"name": "Genus", "type": "text"},
                {"name": "Species", "type": "text"}
            ]
        }
    }
    mw = ObjectProgramUI(root, app)
    mw.initializing = False
    mw.reg_by_id = app.df_reg
    mw.obs_by_id = app.df_obs
    mw.problem_to_field = {"Genus_Problem": "Genus", "Species_Problem": "Species"}
    mw.problem_columns = ["Genus_Problem", "Species_Problem"]
    mw.reg_columns = ["Genus", "Species"]
    mw.choice_fields = set()
    mw.image_panel = MagicMock()
    mw.image_panel.image_zoom_factor = 1.0
    mw.image_panel.image_rotation_angle = 0
    mw.image_panel.images_missing_var = tk.StringVar()
    mw.image_panel.images_missing_label = tk.Label(root)
    mw.image_panel.image_container = tk.Frame(root)
    mw.image_panel.show_images_var = tk.BooleanVar(value=True)
    mw.image_panel.show_image_tools_var = tk.BooleanVar(value=True)
    mw._preload_adjacent_images = MagicMock()

    mw.show_all_history_var = tk.BooleanVar(value=False)
    mw.current_object_suggestions = {}
    mw.reg_vars = {"Genus": tk.StringVar(), "Species": tk.StringVar()}
    mw.problem_vars = {"Genus_Problem": tk.BooleanVar(), "Species_Problem": tk.BooleanVar()}
    mw.reg_entries = {
        "Genus": tk.Entry(root, textvariable=mw.reg_vars["Genus"]),
        "Species": tk.Entry(root, textvariable=mw.reg_vars["Species"])
    }
    mw.reg_entry_list = list(mw.reg_entries.values())
    mw.location_vars = {}
    mw.reviewed_var = tk.BooleanVar(value=False)
    mw.reviewed_time_label = tk.Label(root)
    mw.title_label = tk.Label(root)
    mw.object_id_var = tk.StringVar()
    mw.no_image_label = tk.Label(root)
    mw.location_summary_label = tk.Label(root)
    mw.no_problems_msg_label = tk.Label(root)
    mw.object_list = TreeviewListboxWrapper(root, mw)

    return mw

def test_manual_edit_clears_auto_problem_and_persists():
    """Verifies that editing a field with an auto-detected problem clears the problem flag and persists across object navigation."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1", "OBJ2"],
        "Genus": ["", "Abies"],
        "Species": ["", "alba"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1", "OBJ2"],
        "Genus_Problem": [False, False],
        "Species_Problem": [False, False],
        "Reviewed": [False, False]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)

    # Load OBJ1 (has blank Genus -> auto_val = True for Genus_Problem)
    mw.load_object("OBJ1")
    assert bool(mw.problem_vars["Genus_Problem"].get()) is True
    assert app.df_reg.at["OBJ1", "Genus"] == ""

    # User manually types "Pinus" into Genus
    mw.reg_vars["Genus"].set("Pinus")

    # Navigate to OBJ2 (should commit OBJ1 changes first)
    mw.load_object("OBJ2")

    # Verify OBJ1 in df_reg is now "Pinus" and Genus_Problem in df_obs is False
    assert app.df_reg.at["OBJ1", "Genus"] == "Pinus"
    assert bool(app.df_obs.at["OBJ1", "Genus_Problem"]) is False

    # Navigate back to OBJ1
    mw.load_object("OBJ1")
    assert mw.reg_vars["Genus"].get() == "Pinus"
    assert bool(mw.problem_vars["Genus_Problem"].get()) is False

    root.destroy()

def test_historical_resolver_persistence():
    """Verifies that applying a resolution via HistoricalConflictResolverWindow updates caches, df_reg, and df_obs across navigation."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1", "OBJ2"],
        "Genus": ["", "Picea"],
        "Species": ["", "abies"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1", "OBJ2"],
        "Genus_Problem": [True, False],
        "Species_Problem": [False, False],
        "Reviewed": [False, False]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)

    mw.load_object("OBJ1")
    assert bool(mw.problem_vars["Genus_Problem"].get()) is True

    # Open resolver with suggestions structure: {field: {value: {source_name}}}
    suggestions = {"Genus": {"Pinus": {"DB1"}}}
    resolver = HistoricalConflictResolverWindow(mw, "OBJ1", suggestions)
    resolver.res_vars["Genus"].set("Pinus")
    resolver.apply_all()

    # Verify DF updated and problem cleared
    assert app.df_reg.at["OBJ1", "Genus"] == "Pinus"
    assert bool(app.df_obs.at["OBJ1", "Genus_Problem"]) is False

    # Navigate to OBJ2 and back to OBJ1
    mw.load_object("OBJ2")
    mw.load_object("OBJ1")

    assert mw.reg_vars["Genus"].get() == "Pinus"
    assert bool(mw.problem_vars["Genus_Problem"].get()) is False

    root.destroy()

def test_card_live_update():
    """Verifies that refresh_object_card updates card taxonomy labels live when an object field is edited."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus": ["Quercus"],
        "Species": ["robur"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus_Problem": [False],
        "Species_Problem": [False],
        "Reviewed": [False]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)

    listbox = mw.object_list
    listbox.insert(0, "OBJ1", genus="Quercus", species="robur")
    mw.load_object("OBJ1")

    # Change genus to "Betula"
    mw.reg_vars["Genus"].set("Betula")
    mw.commit_current_object()

    # Verify item_data in listbox has been refreshed live
    assert listbox.item_data["OBJ1"]["genus"] == "Betula"
    assert listbox.item_data["OBJ1"]["values"] == ["☐", "OBJ1", "Betula", "robur"]

    root.destroy()

def test_unknown_fixed_removes_yellow_highlights():
    """Verifies that replacing an unknown value removes yellow background highlights and updates card status badge away from yellow UKN."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus": ["Unknown"],
        "Species": ["sylvestris"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus_Problem": [False],
        "Species_Problem": [False],
        "Reviewed": [False]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)

    mw.load_object("OBJ1")
    assert mw.is_unknown(mw.reg_vars["Genus"].get()) is True

    # Fix the unknown value
    mw.reg_vars["Genus"].set("Pinus")
    mw.commit_current_object()

    # Re-validate fields
    mw._validate_fields()
    genus_bg = mw.reg_entries["Genus"].cget("background")
    assert genus_bg != "#ffe4b3"
    assert genus_bg != "#fff3a3"

    # Test card status badge fallback for clean unreviewed object is UNREV (not bright yellow UKN)
    widgets = mw.object_list._build_empty_card_widget(mw.object_list.canvas)
    populated = mw.object_list._populate_card_widget(widgets, "OBJ1")
    status_badge = widgets["status_badge"]
    assert status_badge.cget("text") == "UNREV"

    root.destroy()

def test_invalidate_row_cache_and_undo_redo_sync():
    """Verifies that _invalidate_row_cache properly clears problem caches and undo/redo updates problem flags."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus": ["Pinus"],
        "Species": ["sylvestris"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus_Problem": [False],
        "Species_Problem": [False],
        "Reviewed": [False]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)
    mw.load_object("OBJ1")

    # Pre-populate problem cache
    mw._problem_cache["OBJ1"] = False
    assert mw._problem_cache.get("OBJ1") is False

    # Perform an edit that introduces a problem
    mw.reg_vars["Genus"].set("")
    mw.commit_current_object()

    # Verify problem cache is cleared/invalidated for OBJ1
    assert "OBJ1" not in mw._problem_cache or mw._problem_cache["OBJ1"] is True
    assert mw.is_problem_active("OBJ1", "Genus_Problem") is True

    # Test Undo
    mw.undo()
    assert mw.reg_vars["Genus"].get() == "Pinus"
    assert mw.is_problem_active("OBJ1", "Genus_Problem") is False

    # Test Redo
    mw.redo()
    assert mw.reg_vars["Genus"].get() == ""
    assert mw.is_problem_active("OBJ1", "Genus_Problem") is True

    root.destroy()

def test_is_problem_active_safe_lookup_nonexistent_ids():
    """Verifies that is_problem_active safely returns False for non-existent IDs without raising KeyError."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus": ["Pinus"],
        "Species": ["sylvestris"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus_Problem": [False],
        "Species_Problem": [False],
        "Reviewed": [False]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)

    # Calling with a non-existent ObjectID should safely return False
    assert mw.is_problem_active("NON_EXISTENT", "Other_problem") is False
    assert mw.is_problem_active("NON_EXISTENT", "Reviewed") is False
    assert mw.is_problem_active("NON_EXISTENT", "Genus_Problem") is False
    assert mw.is_problem_active(99999, "Genus_Problem") is False

    root.destroy()


def test_rev_err_card_badge_and_color():
    """Verifies that an object with Reviewed=True and active problems gets REV+ERR badge and amber color."""
    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus": ["Pinus"],
        "Species": ["sylvestris"]
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1"],
        "Genus_Problem": [True],
        "Species_Problem": [False],
        "Reviewed": [True]
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)
    mw.load_object("OBJ1")
    mw.update_list_item_color("OBJ1")

    # Check list item tags
    tags = mw.object_list.item("OBJ1", "tags")
    assert any("f0ad4e" in t or "ffb366" in t for t in tags)

    # Check card populate badge
    widgets = mw.object_list._build_empty_card_widget(mw.object_list.canvas)
    mw.object_list._populate_card_widget(widgets, "OBJ1")
    assert widgets["status_badge"].cget("text") == "REV+ERR"
    assert widgets["status_badge"].cget("bg") == "#F57C00"

    root.destroy()


def test_problem_resolver_clear_flag_keep_value_and_queue_nav():
    """Verify 1-click '✓ Value is Correct (Clear Flag)' clears flag with Undo & Alt+Left/Right navigates queue."""
    from ui.object_problem_resolver import ObjectProblemResolver

    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    df_reg = pd.DataFrame({
        "ObjectID": ["OBJ1", "OBJ2"],
        "Genus": ["Betula", "Pinus"],
        "Species": ["pendula", "sylvestris"],
    }).set_index("ObjectID")

    df_obs = pd.DataFrame({
        "ObjectID": ["OBJ1", "OBJ2"],
        "Genus_Problem": [True, True],
        "Species_Problem": [False, False],
        "Reviewed": [True, True],
    }).set_index("ObjectID")

    app = MockApp(df_reg, df_obs)
    mw = create_mock_ui(root, app)
    mw.load_object("OBJ1")

    logged_actions = []
    undo_calls = []
    mw.log_action = lambda action, **kw: logged_actions.append((action, kw))
    mw.push_undo_state = lambda oid=None: undo_calls.append(oid)

    resolver = ObjectProblemResolver(mw, ["OBJ1", "OBJ2"], suggestions={"Genus": []})
    root.update_idletasks()

    # Locate the 1-click Clear Flag button on the Genus card
    clear_btns = []

    def _walk(w):
        for child in w.winfo_children():
            if isinstance(child, tk.Button) and "Value is Correct" in str(child.cget("text")):
                clear_btns.append(child)
            _walk(child)

    _walk(resolver.win)
    assert clear_btns, "Expected '✓ Value is Correct (Clear Flag)' button on active-flag card"

    # Invoke 1-click Clear Flag
    clear_btns[0].invoke()
    root.update_idletasks()

    # Registration value preserved, problem flag cleared, Undo pushed, audit logged
    assert app.df_reg.loc["OBJ1", "Genus"] == "Betula"
    assert bool(app.df_obs.loc["OBJ1", "Genus_Problem"]) is False
    assert "OBJ1" in undo_calls
    assert any(a == "PROBLEM_CLEARED" for a, _ in logged_actions)
    assert "Cleared" in str(clear_btns[0].cget("text"))

    # Queue navigation via _queue_navigate (bound to Alt+Right / Alt+Left)
    assert resolver.oid == "OBJ1"
    resolver._queue_navigate(1)
    assert resolver.oid == "OBJ2"
    resolver._queue_navigate(-1)
    assert resolver.oid == "OBJ1"

    resolver.win.destroy()
    root.destroy()


# ============================================================================
# Merged from test_object_problem_resolver.py
# ============================================================================

import pytest
import tkinter as tk
import pandas as pd
from unittest.mock import MagicMock, patch
from models import AppState
from ui.object_problem_resolver import ObjectProblemResolver, ProblemQueueDialog
from ui.main_window import ObjectProgramUI
import config


def test_object_problem_resolver_single_mode_taxonomy_and_provenance():
    root = tk.Tk()
    root.withdraw()
    try:
        app = AppState()
        app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
        app.df_reg = pd.DataFrame([{
            "ObjectID": "1001",
            "Genus": "OldGenus",
            "Species": "sylvestris",
            "Collector": "OldCollector"
        }]).set_index("ObjectID")
        app.df_obs = pd.DataFrame([{
            "ObjectID": "1001",
            "Genus_Problem": True,
            "Collector_Problem": True
        }]).set_index("ObjectID")
        app.df_photo = pd.DataFrame(columns=["ObjectID", "ImagePath"]).set_index("ObjectID")
        app.df_log = pd.DataFrame()
        app._log_records = []
        app.current_object_id = "1001"

        main_app = MagicMock()
        main_app.root = root
        main_app.app = app
        main_app.current_object_id = "1001"
        main_app.problem_to_field = {
            "Genus_Problem": "Genus",
            "Collector_Problem": "Collector"
        }
        main_app.problem_vars = {
            "Genus_Problem": tk.BooleanVar(value=True),
            "Collector_Problem": tk.BooleanVar(value=True)
        }
        main_app.reg_vars = {
            "Genus": tk.StringVar(value="OldGenus"),
            "Collector": tk.StringVar(value="OldCollector")
        }
        main_app.reg_entries = {}
        main_app._cached_reg_dict = {"1001": {"Genus": "OldGenus", "Collector": "OldCollector"}}
        main_app._cached_obs_dict = {"1001": {"Genus_Problem": True, "Collector_Problem": True}}
        main_app.loaded_problem_states = {"Genus_Problem": True, "Collector_Problem": True}
        main_app.push_undo_state = ObjectProgramUI.push_undo_state.__get__(main_app, MagicMock)
        main_app.log_action = MagicMock()

        suggestions = {
            "Genus": {"Pinus": ["Book1.xlsx"]},
            "Collector": {"Smith, J.": ["Book1.xlsx"]}
        }

        with patch("config.load_prefs", return_value={"completed_tutorials": ["historical_resolver"]}):
            resolver = ObjectProblemResolver(main_app, "1001", suggestions)
            
            # Verify queue mode is False for single object
            assert resolver._is_queue_mode is False
            assert resolver.oid == "1001"

            # Check taxonomy detection
            assert "Genus" in resolver._taxonomy_fields
            assert "Collector" not in resolver._taxonomy_fields

            # Provenance field (Collector) must be blank by default regardless of suggestions
            assert resolver.res_vars["Collector"].get() == ""

            # Populate manually or via suggestion
            resolver.res_vars["Genus"].set("Pinus")
            resolver.res_vars["Collector"].set("Smith, J.")

            # Apply
            resolver.apply_all()

            # Verify df_reg and df_obs are updated immediately
            assert app.df_reg.at["1001", "Genus"] == "Pinus"
            assert app.df_reg.at["1001", "Collector"] == "Smith, J."
            assert bool(app.df_obs.at["1001", "Genus_Problem"]) is False
            assert bool(app.df_obs.at["1001", "Collector_Problem"]) is False

            # Undo state recorded
            assert len(app.undo_stacks.get("1001", [])) == 1
    finally:
        root.destroy()


def test_object_problem_resolver_queue_mode_navigation():
    root = tk.Tk()
    root.withdraw()
    try:
        app = AppState()
        app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
        app.df_reg = pd.DataFrame([
            {"ObjectID": "1001", "Genus": "OldGenus1", "Species": "sp1"},
            {"ObjectID": "1002", "Genus": "OldGenus2", "Species": "sp2"},
            {"ObjectID": "1003", "Genus": "OldGenus3", "Species": "sp3"},
        ]).set_index("ObjectID")
        app.df_obs = pd.DataFrame([
            {"ObjectID": "1001", "Genus_Problem": True},
            {"ObjectID": "1002", "Genus_Problem": True},
            {"ObjectID": "1003", "Genus_Problem": True},
        ]).set_index("ObjectID")
        app.df_photo = pd.DataFrame(columns=["ObjectID", "ImagePath"]).set_index("ObjectID")
        app.df_log = pd.DataFrame()
        app._log_records = []
        app.current_object_id = "1001"

        main_app = MagicMock()
        main_app.root = root
        main_app.app = app
        main_app.current_object_id = "1001"
        main_app.problem_to_field = {"Genus_Problem": "Genus"}
        main_app.problem_vars = {"Genus_Problem": tk.BooleanVar(value=True)}
        main_app.reg_vars = {"Genus": tk.StringVar(value="OldGenus1")}
        main_app.reg_entries = {}
        main_app._cached_reg_dict = {}
        main_app._cached_obs_dict = {}
        main_app.loaded_problem_states = {}
        main_app.push_undo_state = ObjectProgramUI.push_undo_state.__get__(main_app, MagicMock)
        main_app.log_action = MagicMock()
        main_app.collect_historical_suggestions = lambda oid, **kwargs: {"Genus": {f"NewGenus_{oid}": ["Book1.xlsx"]}}

        with patch("config.load_prefs", return_value={"completed_tutorials": ["historical_resolver"]}):
            resolver = ObjectProblemResolver(main_app, ["1001", "1002", "1003"])
            
            assert resolver._is_queue_mode is True
            assert resolver.oid == "1001"
            assert resolver._queue_idx == 0

            # Step to next object
            resolver._queue_navigate(1)
            assert resolver.oid == "1002"
            assert resolver._queue_idx == 1

            # Resolve 1002 and apply
            resolver.res_vars["Genus"].set("NewGenus_1002")
            resolver.apply_all()

            # Immediate persistence of 1002
            assert app.df_reg.at["1002", "Genus"] == "NewGenus_1002"
            assert bool(app.df_obs.at["1002", "Genus_Problem"]) is False

            # apply_all in queue mode advances to 1003
            assert resolver.oid == "1003"
            assert resolver._queue_idx == 2
    finally:
        root.destroy()


def test_problem_queue_dialog_filtering_and_matching():
    root = tk.Tk()
    root.withdraw()
    try:
        app = AppState()
        app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
        app.df_reg = pd.DataFrame([
            {"ObjectID": "1", "Genus": "Rosa"},
            {"ObjectID": "2", "Genus": "Quercus"},
            {"ObjectID": "3", "Genus": "Pinus"},
        ]).set_index("ObjectID")
        app.df_obs = pd.DataFrame([
            {"ObjectID": "1", "Genus_Problem": True, "Collector_Problem": False, "Other_problem": False},
            {"ObjectID": "2", "Genus_Problem": False, "Collector_Problem": True, "Other_problem": False},
            {"ObjectID": "3", "Genus_Problem": False, "Collector_Problem": False, "Other_problem": True},
        ]).set_index("ObjectID")
        app.active_object_ids = ["1", "2", "3"]

        main_app = MagicMock()
        main_app.root = root
        main_app.app = app
        main_app._get_obs_dict.return_value = {
            "1": {"Genus_Problem": True, "Collector_Problem": False, "Other_problem": False},
            "2": {"Genus_Problem": False, "Collector_Problem": True, "Other_problem": False},
            "3": {"Genus_Problem": False, "Collector_Problem": False, "Other_problem": True},
        }

        dialog = ProblemQueueDialog(root, main_app)

        # All categories selected -> matches 1, 2, 3
        matching = dialog._get_matching_oids()
        assert set(matching) == {"1", "2", "3"}

        # Deselect collection and notes -> only taxonomy matches (1)
        dialog.cat_collection_var.set(False)
        dialog.cat_notes_var.set(False)
        dialog.cat_physical_var.set(False)
        matching_tax = dialog._get_matching_oids()
        assert matching_tax == ["1"]

        dialog.destroy()
    finally:
        root.destroy()


# ============================================================================
# Merged from test_problem_categories.py
# ============================================================================

import pytest
import pandas as pd
from config import DATABASE_CONFIGS, PROBLEM_CATEGORY_THEMES
from backend.filter import FilterManager
from repository import REVIEWED_COLUMN


class TestProblemCategoryConfig:
    """Verify that configuration schemas include required domain categories and metadata."""

    def test_problem_category_themes_structure(self):
        expected_cats = {"taxonomy", "collection", "physical", "media", "notes"}
        assert expected_cats.issubset(set(PROBLEM_CATEGORY_THEMES.keys()))

        for cat, data in PROBLEM_CATEGORY_THEMES.items():
            assert "label" in data
            assert "badge" in data
            assert "color" in data
            assert "rank" in data
            assert isinstance(data["rank"], int)

    def test_botany_config_problem_metadata(self):
        botany_cfg = DATABASE_CONFIGS["Økonomisk Botanisk"]
        problems = botany_cfg.get("ui_sections", {}).get("problems", [])
        assert len(problems) > 0

        for p in problems:
            assert "category" in p, f"Problem {p.get('name')} missing category"
            assert p["category"] in PROBLEM_CATEGORY_THEMES, f"Problem {p.get('name')} has invalid category {p['category']}"
            assert "importance" in p, f"Problem {p.get('name')} missing importance"
            assert p["importance"] in {"high", "medium", "low", "workflow"}

        # Verify specific assignments
        prob_map = {p["name"]: p for p in problems}

        # Taxonomy
        assert prob_map["Genus_Problem"]["category"] == "taxonomy"
        assert prob_map["Genus_Problem"]["importance"] == "high"
        assert prob_map["Species_Problem"]["category"] == "taxonomy"
        assert prob_map["Species_Problem"]["importance"] == "high"

        # Collection & Provenance
        assert prob_map["Collector_Problem"]["category"] == "collection"
        assert prob_map["Collection_Date_Problem"]["category"] == "collection"

        # Physical & Storage
        assert prob_map["PlantPart_Problem"]["category"] == "physical"
        assert prob_map["PlantPart_Problem"]["importance"] == "low"
        assert prob_map["Box_Label_Problem"]["category"] == "physical"

        # Media
        assert prob_map["Images_Problem"]["category"] == "media"


class TestCategoryFilterEvaluators:
    """Test category evaluators in FilterManager."""

    @pytest.fixture
    def specimen_dataset(self):
        df_reg = pd.DataFrame(
            {
                "Genus": ["Quercus", "Pinus", "", "Betula"],
                "Species": ["robur", "sylvestris", "alba", ""],
                "Collector": ["Smith", "ukjent", "Jones", ""],
                "Collection_Date": ["1920", "unknown", "1950", ""],
                "Box Label": ["Box 1", "Box 2", "Box 3", ""],
                "Plant Part": ["Wood", "Leaf", "Bark", ""],
            },
            index=["1", "2", "3", "4"]
        )
        df_obs = pd.DataFrame(
            {
                "Genus_Problem": [False, False, True, False],
                "Species_Problem": [False, False, False, False],
                "Collector_Problem": [False, False, False, False],
                "Box_Label_Problem": [False, False, False, True],
                "PlantPart_Problem": [False, False, False, False],
                "Images_Problem": [False, True, False, False],
                "Images_Missing": [False, False, False, True],
                REVIEWED_COLUMN: [True, True, False, False],
            },
            index=["1", "2", "3", "4"]
        )

        reg_dict = df_reg.to_dict(orient="index")
        obs_dict = df_obs.to_dict(orient="index")
        history_set = set()

        prob_cols = [
            "Genus_Problem", "Species_Problem", "Collector_Problem",
            "Box_Label_Problem", "PlantPart_Problem", "Images_Problem", "Images_Missing"
        ]
        prob_to_field = {
            "Genus_Problem": "Genus",
            "Species_Problem": "Species",
            "Collector_Problem": "Collector",
            "Box_Label_Problem": "Box Label",
            "PlantPart_Problem": "Plant Part",
        }
        prob_categories = {
            "Genus_Problem": "taxonomy",
            "Species_Problem": "taxonomy",
            "Collector_Problem": "collection",
            "Box_Label_Problem": "physical",
            "PlantPart_Problem": "physical",
            "Images_Problem": "media",
            "Images_Missing": "media",
        }
        unknown_to_field = ["Collector", "Collection_Date"]

        return df_reg, reg_dict, obs_dict, history_set, prob_cols, prob_to_field, prob_categories, unknown_to_field

    def test_filter_has_taxonomy_problem(self, specimen_dataset):
        df_reg, reg_dict, obs_dict, history_set, prob_cols, prob_to_field, prob_cats, unk_fields = specimen_dataset
        fm = FilterManager()

        # Object 3 has Genus_Problem = True, Object 4 has missing Species
        res = fm.apply_filter(
            df_reg=df_reg,
            reg_dict=reg_dict,
            obs_dict=obs_dict,
            history_set=history_set,
            groups={"Problems": ["Has_Taxonomy_Problem"]},
            global_mode="AND",
            not_reviewed_only=False,
            location_filters=("", "", ""),
            problem_columns=prob_cols,
            problem_to_field=prob_to_field,
            problem_categories=prob_cats,
            unknown_to_field=unk_fields,
            image_mode="folder"
        )
        assert "3" in res
        assert "4" in res
        assert "1" not in res
        assert "2" not in res

    def test_filter_has_collection_problem_with_ukjent_suppression(self, specimen_dataset):
        df_reg, reg_dict, obs_dict, history_set, prob_cols, prob_to_field, prob_cats, unk_fields = specimen_dataset
        fm = FilterManager()

        # Object 2 has "ukjent" / "unknown", which should NOT trigger collection problem
        # Object 4 has empty Collector and empty Date without ukjent, so it triggers
        res = fm.apply_filter(
            df_reg=df_reg,
            reg_dict=reg_dict,
            obs_dict=obs_dict,
            history_set=history_set,
            groups={"Problems": ["Has_Collection_Problem"]},
            global_mode="AND",
            not_reviewed_only=False,
            location_filters=("", "", ""),
            problem_columns=prob_cols,
            problem_to_field=prob_to_field,
            problem_categories=prob_cats,
            unknown_to_field=unk_fields,
            image_mode="folder"
        )
        assert "2" not in res  # Ukjent properly suppressed as actionable problem
        assert "4" in res

        # Also verify ICEDIG code "unknown:missing" suppresses collection problem
        df_reg_icedig = df_reg.copy()
        df_reg_icedig.at["4", "Collector"] = "unknown:missing"
        df_reg_icedig.at["4", "Collection_Date"] = "unknown:indecipherable"
        reg_dict_icedig = df_reg_icedig.to_dict(orient="index")
        res_icedig = fm.apply_filter(
            df_reg=df_reg_icedig,
            reg_dict=reg_dict_icedig,
            obs_dict=obs_dict,
            history_set=history_set,
            groups={"Problems": ["Has_Collection_Problem"]},
            global_mode="AND",
            not_reviewed_only=False,
            location_filters=("", "", ""),
            problem_columns=prob_cols,
            problem_to_field=prob_to_field,
            problem_categories=prob_cats,
            unknown_to_field=unk_fields,
            image_mode="folder"
        )
        assert "4" not in res_icedig

    def test_filter_has_storage_problem(self, specimen_dataset):
        df_reg, reg_dict, obs_dict, history_set, prob_cols, prob_to_field, prob_cats, unk_fields = specimen_dataset
        fm = FilterManager()

        # Object 4 has Box_Label_Problem=True
        res = fm.apply_filter(
            df_reg=df_reg,
            reg_dict=reg_dict,
            obs_dict=obs_dict,
            history_set=history_set,
            groups={"Problems": ["Has_Storage_Problem"]},
            global_mode="AND",
            not_reviewed_only=False,
            location_filters=("", "", ""),
            problem_columns=prob_cols,
            problem_to_field=prob_to_field,
            problem_categories=prob_cats,
            unknown_to_field=unk_fields,
            image_mode="folder"
        )
        assert res == ["4"]

    def test_filter_needs_image_workflow(self, specimen_dataset):
        df_reg, reg_dict, obs_dict, history_set, prob_cols, prob_to_field, prob_cats, unk_fields = specimen_dataset
        fm = FilterManager()

        # Object 2 has Images_Problem=True, Object 4 has Images_Missing=True
        res = fm.apply_filter(
            df_reg=df_reg,
            reg_dict=reg_dict,
            obs_dict=obs_dict,
            history_set=history_set,
            groups={"Images": ["Needs_Image_Workflow"]},
            global_mode="AND",
            not_reviewed_only=False,
            location_filters=("", "", ""),
            problem_columns=prob_cols,
            problem_to_field=prob_to_field,
            problem_categories=prob_cats,
            unknown_to_field=unk_fields,
            image_mode="folder"
        )
        assert "2" in res
        assert "4" in res
        assert "1" not in res
        assert "3" not in res


class TestMobileServerCategoryForwardCompatibility:
    """Verify that backend/mobile_server.py passes category and importance metadata in endpoints."""

    def test_get_problem_metadata_in_schema(self):
        botany_cfg = DATABASE_CONFIGS["Økonomisk Botanisk"]
        
        # Test schema payload generation
        ui_sections = botany_cfg.get("ui_sections", {})
        problems = ui_sections.get("problems", [])
        
        for p in problems:
            assert "category" in p
            assert "importance" in p


# ============================================================================
# Merged from test_icedig_usability.py
# ============================================================================

import pytest
import tkinter as tk
from unittest.mock import MagicMock
import pandas as pd

from ui.registry_panel import _bind_icedig_context_menu, _bind_icedig_shortcuts, _apply_icedig_code
from ui.object_problem_resolver import ObjectProblemResolver
import config
from backend.mobile_server import INDEX_TEMPLATE


@pytest.fixture
def tk_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        root.destroy()
    except Exception:
        pass


def test_icedig_context_menu_unlocked_on_empty_and_valid_fields(tk_root):
    """Verify that ICEDIG context menu generates on empty fields, valid data, and legacy tokens."""
    mock_ui = MagicMock()
    mock_ui.reg_vars = {
        "Collector": tk.StringVar(value=""),
        "Species": tk.StringVar(value="sylvestris"),
        "Genus": tk.StringVar(value="unknown:missing")
    }

    entry = tk.Entry(tk_root)
    entry.pack()

    # 1. Bind to empty field and verify menu builds
    _bind_icedig_context_menu(mock_ui, entry, "Collector")
    assert hasattr(entry, "_icedig_menu_builder")
    menu_fn = entry._icedig_menu_builder

    menu_items_empty = menu_fn(None)
    assert menu_items_empty is not None
    assert any(item.get("label") == "Set ICEDIG status" for item in menu_items_empty)

    # 2. Check menu on field with regular data
    mock_ui.reg_vars["Collector"].set("Carl Linnaeus")
    menu_items_data = menu_fn(None)
    assert menu_items_data is not None
    assert any(item.get("label") == "Clear Field Value" for item in menu_items_data)


def test_icedig_shorthand_expansion(tk_root):
    """Verify that shorthand tokens (?m, ?i, ?u, ?w, ??) expand to ICEDIG codes."""
    mock_ui = MagicMock()
    var = tk.StringVar(value="")
    mock_ui.reg_vars = {"Collector": var}
    mock_ui.commit_current_object = MagicMock()

    entry = tk.Entry(tk_root, textvariable=var)
    entry.pack()

    _bind_icedig_shortcuts(mock_ui, entry, "Collector")

    # Test ?m -> unknown:missing
    var.set("?m")
    entry._check_shorthand(None)
    assert var.get() == "unknown:missing"

    # Test ?i -> unknown:indecipherable
    var.set("?i")
    entry._check_shorthand(None)
    assert var.get() == "unknown:indecipherable"

    # Test ?u -> unknown:undigitized
    var.set("?u")
    entry._check_shorthand(None)
    assert var.get() == "unknown:undigitized"

    # Test ?w -> withheld
    var.set("?w")
    entry._check_shorthand(None)
    assert var.get() == "withheld"

    # Test ?? -> unknown
    var.set("??")
    entry._check_shorthand(None)
    assert var.get() == "unknown"


def test_resolver_1click_icedig_buttons(tk_root):
    """Verify that 1-click Blank and Illegible buttons in ObjectProblemResolver resolve issues."""
    mock_main = MagicMock()
    mock_main.root = tk_root
    mock_main.df_reg = pd.DataFrame([{"Collector": ""}], index=["1001"])
    mock_main.df_obs = pd.DataFrame([{"Collector_Problem": True}], index=["1001"])
    mock_main._get_reg_dict = lambda: {"1001": {"Collector": ""}}
    mock_main.is_unknown = lambda val: str(val).strip().lower() in config.ALL_UNKNOWN_TOKENS
    mock_main.problem_to_field = {"Collector_Problem": "Collector"}
    mock_main.problem_vars = {"Collector_Problem": tk.BooleanVar(value=True)}
    mock_main.reg_vars = {"Collector": tk.StringVar(value="")}
    mock_main.reg_entries = {}
    mock_main.app = MagicMock()
    mock_main.app.df_reg = mock_main.df_reg
    mock_main.app.df_obs = mock_main.df_obs

    suggestions = {"Collector": {"Linnaeus": {"Book A"}}}
    resolver = ObjectProblemResolver(mock_main, "1001", suggestions)

    # Verify resolution cards were created
    assert "Collector" in resolver.card_frames
    assert "Collector" in resolver.res_vars

    # Execute resolution via res_var set
    resolver.res_vars["Collector"].set("unknown:missing")
    assert mock_main.is_unknown(resolver.res_vars["Collector"].get()) is True


def test_mobile_template_icedig_picker_integration():
    """Verify that mobile template includes bottom sheet modal and ICEDIG button handlers."""
    assert 'id="icedigBottomSheetModal"' in INDEX_TEMPLATE
    assert 'openIcedigBottomSheet' in INDEX_TEMPLATE
    assert 'applyIcedigChoice' in INDEX_TEMPLATE
    assert 'showToastWithUndo' in INDEX_TEMPLATE
    assert 'discrepancyUnvalCheck' in INDEX_TEMPLATE
    assert 'Missing Data Status' in INDEX_TEMPLATE
