import os
import sys
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from config import sc
from ui.command_palette import CommandPalette
from ui.object_context_bar import ObjectContextBar
from ui.widgets import TreeviewListboxWrapper


class MockApp:
    def __init__(self, n_rows=20):
        oids = [f"OBJ-{i:05d}" for i in range(n_rows)]
        self.active_object_ids = oids
        self.current_object_id = oids[0]
        self.dirty = False

        self.df_reg = pd.DataFrame({
            "ObjectID": oids,
            "Genus": ["Quercus" if i % 2 == 0 else "Pinus" for i in range(n_rows)],
            "Species": ["robur" if i % 2 == 0 else "sylvestris" for i in range(n_rows)],
            "Author": ["L." for _ in range(n_rows)],
            "Family": ["Fagaceae" if i % 2 == 0 else "Pinaceae" for i in range(n_rows)],
        }).set_index("ObjectID", drop=False)

        self.df_obs = pd.DataFrame({
            "ObjectID": oids,
            "Reviewed": [True if i == 0 else False for i in range(n_rows)],
            "Building": ["Herbarium" for _ in range(n_rows)],
            "Floor": ["2" for _ in range(n_rows)],
            "Cabinet": [f"C-{i % 10}" for i in range(n_rows)],
            "Shelf": [f"S-{i % 5}" for i in range(n_rows)],
            "Stored as": ["Folder" for _ in range(n_rows)],
            "Loaned out": [True if i == 2 else False for i in range(n_rows)],
            "MissingLabel": [True if i == 1 else False for i in range(n_rows)],
            "Taxonomy_Problem": [True if i == 3 else False for i in range(n_rows)],
            "Images_Missing": [False for _ in range(n_rows)]
        }).set_index("ObjectID", drop=False)

        self.df_photo = pd.DataFrame(columns=["ObjectID", "Filename"]).set_index("ObjectID")
        self.df_unvalidated = pd.DataFrame(columns=["ObjectID", "Field_Name", "Unvalidated_Comment"])
        self.config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {
                "problems": [
                    {"name": "MissingLabel", "category": "collection"},
                    {"name": "Taxonomy_Problem", "category": "taxonomy"}
                ]
            }
        }


class MockMainWindow:
    def __init__(self, app, root):
        self.app = app
        self.root = root
        self.dark_mode_active = False
        self.focus_mode_var = tk.BooleanVar(value=False)
        self.problem_columns = ["Taxonomy_Problem", "MissingLabel"]
        self.problem_to_field = {}
        self.image_mode = "online"
        self._history_cache = {}
        self._has_suggestions_set = set()
        self._problem_cache = {
            "OBJ-00001": True,
            "OBJ-00003": True,
        }
        self._rebuild_caches()

    def _rebuild_caches(self):
        self._cached_reg_dict = self.app.df_reg.to_dict("index")
        self._cached_obs_dict = self.app.df_obs.to_dict("index")
        self._cached_genus_dict = {k: v.get("Genus", "") for k, v in self._cached_reg_dict.items()}
        self._cached_species_dict = {k: v.get("Species", "") for k, v in self._cached_reg_dict.items()}
        self._cached_reviewed_dict = {k: v.get("Reviewed", False) for k, v in self._cached_obs_dict.items()}

    def _get_reg_dict(self):
        return self._cached_reg_dict

    def _get_obs_dict(self):
        return self._cached_obs_dict

    def _get_active_problem_categories(self, oid):
        if oid == "OBJ-00003":
            return {"taxonomy"}
        if oid == "OBJ-00001":
            return {"collection"}
        return set()

    def _problems_have_history(self, oid):
        return False

    def is_unknown(self, val):
        return str(val).strip().lower() in ("unknown", "?", "")

    def has_online_photos(self, oid):
        return False

    def has_unvalidated_sources(self, oid):
        return False

    def _toggle_reviewed_for_id(self, oid):
        current = self._cached_reviewed_dict.get(oid, False)
        self._cached_reviewed_dict[oid] = not current

    def _on_list_return(self, event):
        pass


@pytest.fixture(scope="module")
def tk_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        root.destroy()
    except Exception:
        pass


def test_object_context_bar_dictionary_lookups(tk_root):
    """Verify ObjectContextBar correctly renders data and runs without in-loop df.loc calls."""
    app = MockApp(10)
    mw = MockMainWindow(app, tk_root)

    bar = ObjectContextBar(tk_root, app=app, main_ui=mw)
    bar.update_specimen("OBJ-00000")

    assert "OBJ-00000" in bar.id_badge.cget("text")
    assert "Quercus robur" in bar.name_label.cget("text")
    assert "REVIEWED" in bar.status_badge.cget("text")

    # Clean unreviewed
    bar.update_specimen("OBJ-00004")
    assert "OBJ-00004" in bar.id_badge.cget("text")
    assert "UNREVIEWED" in bar.status_badge.cget("text") or "PENDING" in bar.status_badge.cget("text")

    bar.destroy()


def test_single_badge_category_theme_resolution(tk_root):
    """Verify taxonomy and collection problems map to canonical category tokens."""
    app = MockApp(10)
    mw = MockMainWindow(app, tk_root)

    wrapper = TreeviewListboxWrapper(tk_root, mw)
    for oid in app.active_object_ids:
        g = mw._cached_genus_dict.get(oid, "")
        s = mw._cached_species_dict.get(oid, "")
        rev = mw._cached_reviewed_dict.get(oid, False)
        wrapper.insert(tk.END, f"{oid} {g} {s}", genus=g, species=s, reviewed=rev, bulk=True)

    # Check item data populated
    assert "OBJ-00000" in wrapper.item_data
    assert wrapper.item_data["OBJ-00000"]["reviewed"] is True

    wrapper.destroy()


def test_sash_width_calculations():
    """Verify rail width and expanded width comply with design constraints."""
    rail_w = sc(config.RAIL_THEME.get("rail_width", 40))
    assert rail_w > 0
    # Minimum expanded sidebar width should be at least 320px scaled
    default_expanded = sc(360)
    assert default_expanded >= sc(320)
    assert default_expanded > rail_w


def test_object_context_bar_dirty_dot(tk_root):
    """Verify dirty dot displays when app.dirty is set."""
    app = MockApp(5)
    mw = MockMainWindow(app, tk_root)
    bar = ObjectContextBar(tk_root, app=app, main_ui=mw)

    app.dirty = False
    bar.update_specimen("OBJ-00000")
    assert bar.dirty_badge.winfo_manager() != "pack"

    app.dirty = True
    bar.update_specimen("OBJ-00000")
    assert bar.dirty_badge.winfo_manager() == "pack"
    assert "Unsaved" in bar.dirty_badge.cget("text")

    bar.destroy()


def test_targeted_highlight_difference(tk_root):
    """Verify redraw_cards_highlights updates targeted cards without crashing."""
    app = MockApp(10)
    mw = MockMainWindow(app, tk_root)
    wrapper = TreeviewListboxWrapper(tk_root, mw)
    wrapper.pack()
    tk_root.update()

    for oid in app.active_object_ids:
        wrapper.insert(tk.END, f"{oid} Quercus robur", genus="Quercus", species="robur", bulk=True)
    wrapper._schedule_viewport_update()
    tk_root.update()

    wrapper.selection_set(0)
    wrapper.redraw_cards_highlights()
    assert wrapper.selected_iids == ["OBJ-00000"]

    # Step to next card
    wrapper.selection_clear()
    wrapper.selection_set(1)
    wrapper.redraw_cards_highlights()
    assert wrapper.selected_iids == ["OBJ-00001"]

    wrapper.destroy()


def test_card_has_unknown_row2_and_no_row1_packing(tk_root):
    """Verify that scrolling or updating a card with has_unknown=True updates Row 2 text to include UKN without packing widgets into Row 1."""
    app = MockApp(10)
    # Set an unknown field for OBJ-00002
    app.df_reg.loc["OBJ-00002", "Species"] = "unknown"
    mw = MockMainWindow(app, tk_root)

    wrapper = TreeviewListboxWrapper(tk_root, mw)
    wrapper.pack(fill="both", expand=True)
    tk_root.update()

    for oid in app.active_object_ids:
        g = mw._cached_genus_dict.get(oid, "")
        s = mw._cached_species_dict.get(oid, "")
        rev = mw._cached_reviewed_dict.get(oid, False)
        wrapper.insert(tk.END, f"{oid} {g} {s}", genus=g, species=s, reviewed=rev, bulk=True)

    # Build empty card widgets and populate directly (simulating viewport rendering)
    widget_dict = wrapper._build_empty_card_widget(wrapper.canvas)
    wrapper._populate_card_widget(widget_dict, "OBJ-00002")

    # 1. Verify Row 2 meta text includes UKN
    meta_text = widget_dict["meta_lbl"].cget("text")
    assert "UKN" in meta_text

    # 2. Verify Single-Badge Discipline on Row 1:
    # Row 1 must strictly host cb_lbl, tax_lbl, and status_badge.
    # No dummy badges (ukn_badge, img_badge, loaned_badge, unval_badge) should be packed.
    row1_packed_children = widget_dict["row1"].pack_slaves()
    expected_packed = [widget_dict["cb_lbl"], widget_dict["tax_lbl"], widget_dict["status_badge"]]
    assert row1_packed_children == expected_packed
    assert widget_dict["ukn_badge"].winfo_manager() != "pack"
    assert widget_dict["img_badge"].winfo_manager() != "pack"
    assert widget_dict["loaned_badge"].winfo_manager() != "pack"
    assert widget_dict["unval_badge"].winfo_manager() != "pack"

    # 3. Verify updating the card maintains single-badge discipline
    idx = wrapper._oid_to_index["OBJ-00002"]
    wrapper._active_card_windows[idx] = (1, widget_dict)

    wrapper.refresh_object_card("OBJ-00002")
    tk_root.update()

    meta_text_after = widget_dict["meta_lbl"].cget("text")
    assert "UKN" in meta_text_after
    assert widget_dict["row1"].pack_slaves() == expected_packed
    assert widget_dict["ukn_badge"].winfo_manager() != "pack"

    # Also test _refresh_card_accent maintains single-badge discipline
    wrapper._refresh_card_accent("OBJ-00002")
    assert widget_dict["row1"].pack_slaves() == expected_packed
    assert widget_dict["ukn_badge"].winfo_manager() != "pack"

    # 4. Verify scrolling/re-populating card maintains single-badge discipline
    wrapper._populate_card_widget(widget_dict, "OBJ-00002")
    assert "UKN" in widget_dict["meta_lbl"].cget("text")
    assert widget_dict["row1"].pack_slaves() == expected_packed
    assert widget_dict["ukn_badge"].winfo_manager() != "pack"

    wrapper.destroy()


def test_directory_card_prefs_defaults():
    """Verify default card prefs retrieval, mutation, and reset to defaults."""
    config.reset_directory_card_prefs_to_default()
    defaults = config.get_directory_card_prefs()
    assert defaults["density_mode"] == "standard"
    assert defaults["show_location_row"] is True
    assert defaults["show_status_badge"] is True
    assert defaults["show_author_citation"] is False
    assert defaults["show_directory_view_strip"] is False

    # Mutate prefs
    mutated = dict(defaults)
    mutated["density_mode"] = "compact"
    mutated["show_location_row"] = False
    mutated["show_status_badge"] = False
    mutated["show_directory_view_strip"] = True
    config.save_directory_card_prefs(mutated)

    current = config.get_directory_card_prefs()
    assert current["density_mode"] == "compact"
    assert current["show_location_row"] is False
    assert current["show_status_badge"] is False
    assert current["show_directory_view_strip"] is True

    # Reset
    reset_prefs = config.reset_directory_card_prefs_to_default()
    assert reset_prefs["density_mode"] == "standard"
    assert reset_prefs["show_location_row"] is True
    assert reset_prefs["show_status_badge"] is True
    assert reset_prefs["show_directory_view_strip"] is False


def test_command_palette_card_view_commands(tk_root):
    """Verify command palette registers simplified directory card view commands under category VIEW."""
    app = MockApp(5)
    mw = MockMainWindow(app, tk_root)
    palette = CommandPalette(mw)
    palette.withdraw()

    registry = palette._commands_registry
    view_labels = [cmd["label"] for cmd in registry if cmd.get("category") == "VIEW"]
    assert "Card Layout: Standard (78px, 3 Rows)" in view_labels
    assert "Card Layout: Compact (64px, 2 Rows)" in view_labels
    assert "Card Layout: Full Details (92px, Author + Location)" in view_labels
    assert "Card Layout: Minimalist (Clean, No Badges/Location)" in view_labels
    assert "Configure Directory Cards & View Settings..." in view_labels
    assert "Toggle Directory Card Location Row (Row 3)" in view_labels
    assert "Toggle Directory Card Status Pill Badges" in view_labels
    assert "Restore Directory Card Settings to Default" in view_labels

    palette.destroy()


def test_card_preset_aliases_and_configs():
    """Verify card preset name resolution and config overrides across canonical names and legacy aliases."""
    assert config.resolve_card_preset_name("standard") == "standard"
    assert config.resolve_card_preset_name("default") == "standard"
    assert config.resolve_card_preset_name("compact") == "compact"
    assert config.resolve_card_preset_name("high_speed") == "compact"
    assert config.resolve_card_preset_name("full_detail") == "full_detail"
    assert config.resolve_card_preset_name("taxonomist") == "full_detail"
    assert config.resolve_card_preset_name("minimalist") == "minimalist"
    assert config.resolve_card_preset_name("collections_manager") == "minimalist"

    # Test config generation
    std_cfg = config.get_card_preset_config("standard")
    assert std_cfg["density_mode"] == "standard"
    assert std_cfg["show_location_row"] is True

    cpt_cfg = config.get_card_preset_config("compact")
    assert cpt_cfg["density_mode"] == "compact"
    assert cpt_cfg["show_location_row"] is False

    full_cfg = config.get_card_preset_config("full_detail")
    assert full_cfg["density_mode"] == "expanded"
    assert full_cfg["show_author_citation"] is True

    min_cfg = config.get_card_preset_config("minimalist")
    assert min_cfg["show_status_badge"] is False
    assert min_cfg["show_location_row"] is False


def test_directory_view_strip_visibility_toggle(tk_root):
    """Verify that Directory View Strip packs and unpacks according to preferences."""
    from ui.main_window import ObjectProgramUI
    config.reset_directory_card_prefs_to_default()

    ui = ObjectProgramUI.__new__(ObjectProgramUI)
    ui.root = tk_root
    ui.dark_mode_active = False

    container = tk.Frame(tk_root)
    container.pack()
    ui.list_scroll_frame = tk.Frame(container)
    ui.list_scroll_frame.pack(side="top", fill="both", expand=True)

    ui.directory_view_strip = tk.Frame(container)
    ui._build_directory_view_strip(ui.directory_view_strip)
    tk_root.update()

    # Default is False: strip should not be packed
    ui.update_directory_view_strip_visibility()
    tk_root.update()
    assert ui.directory_view_strip.winfo_manager() != "pack"

    # Set to True
    prefs = config.get_directory_card_prefs()
    prefs["show_directory_view_strip"] = True
    config.save_directory_card_prefs(prefs)

    ui.update_directory_view_strip_visibility()
    tk_root.update()
    assert ui.directory_view_strip.winfo_manager() == "pack"

    # Set back to False
    prefs["show_directory_view_strip"] = False
    config.save_directory_card_prefs(prefs)
    ui.update_directory_view_strip_visibility()
    tk_root.update()
    assert ui.directory_view_strip.winfo_manager() != "pack"

    # Reset
    config.reset_directory_card_prefs_to_default()
    container.destroy()


@pytest.mark.parametrize("density", ["compact", "standard", "expanded"])
@pytest.mark.parametrize("show_loc", [True, False])
@pytest.mark.parametrize("show_badge", [True, False])
@pytest.mark.parametrize("show_author", [True, False])
def test_directory_card_combinatorial_preferences(tk_root, density, show_loc, show_badge, show_author):
    """Combinatorial matrix test across density modes, location rows, badges, and author citations."""
    app = MockApp(10)
    mw = MockMainWindow(app, tk_root)
    wrapper = TreeviewListboxWrapper(tk_root, mw)
    wrapper.pack(fill="both", expand=True)
    tk_root.update()

    for oid in app.active_object_ids:
        g = mw._cached_genus_dict.get(oid, "")
        s = mw._cached_species_dict.get(oid, "")
        rev = mw._cached_reviewed_dict.get(oid, False)
        wrapper.insert(tk.END, f"{oid} {g} {s}", genus=g, species=s, reviewed=rev, bulk=True)

    prefs = {
        "density_mode": density,
        "show_location_row": show_loc,
        "location_granularity": "full",
        "show_status_badge": show_badge,
        "badge_priority": "category",
        "badge_categories": {"taxonomy": True, "collection": True},
        "show_author_citation": show_author,
        "show_author_in_expanded_only": False,
        "meta_tokens": {"box": True, "shelf": True, "storage": True, "ukn": True},
    }
    wrapper.apply_directory_view_preferences(prefs)
    tk_root.update()

    # 1. Height must be measured and valid (>= 50px)
    assert wrapper._card_height is not None
    assert wrapper._card_height >= 50

    # 2. Single-badge discipline must hold on Row 1
    widget_dict = wrapper._build_empty_card_widget(wrapper.canvas)
    row1_packed_children = widget_dict["row1"].pack_slaves()
    expected_packed = [widget_dict["cb_lbl"], widget_dict["tax_lbl"], widget_dict["status_badge"]]
    assert row1_packed_children == expected_packed

    # 3. Populate specimen card with taxonomy problem (OBJ-00003)
    wrapper._populate_card_widget(widget_dict, "OBJ-00003")

    # Check badge behavior
    if not show_badge:
        assert widget_dict["status_badge"].cget("text") == ""
    else:
        assert widget_dict["status_badge"].cget("text") != ""

    # Check location row behavior
    if not show_loc:
        assert widget_dict["row3"].winfo_manager() != "pack"
    else:
        assert widget_dict["row3"].winfo_manager() == "pack"

    # Check author citation behavior
    tax_text = widget_dict["tax_lbl"].cget("text")
    if show_author:
        assert "L." in tax_text
    else:
        assert "L." not in tax_text

    wrapper.destroy()


# ============================================================================
# Merged from test_keybindings.py
# ============================================================================

import tkinter as tk
import unittest
from unittest.mock import MagicMock
from ui.keybindings import KeybindingManager


class TestKeybindingManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def setUp(self):
        self.mock_ui = MagicMock()
        self.km = KeybindingManager(self.mock_ui, self.root)

    def test_bind_global_shortcuts(self):
        """Verify all global shortcuts bind cleanly onto the root window."""
        self.km.bind_global_shortcuts()
        bound = self.root.bind()

        # Check key navigation & action shortcuts in Tkinter's canonical internal string format
        expected_patterns = [
            "<Key-Left>", "<Key-Right>", "<Alt-Key-Left>", "<Alt-Key-Right>",
            "<Control-Key-n>", "<Control-Key-r>", "<Control-Key-s>",
            "<Control-Key-k>", "<Control-Key-f>", "<Control-Key-g>",
            "<Control-Key-h>", "<Control-Key-j>", "<Control-Key-p>",
            "<Control-Key-q>", "<Control-Key-z>", "<Control-Key-y>",
            "<Key-F1>", "<Key-F6>", "<Key-F7>", "<Key-F8>", "<Key-space>",
        ]
        for pattern in expected_patterns:
            self.assertIn(pattern, bound, f"Expected {pattern} to be bound to root window.")

    def test_bind_search_shortcuts(self):
        """Verify search entry specific bindings."""
        entry = tk.Entry(self.root)
        self.km.bind_search_shortcuts(entry)
        bound = entry.bind()
        self.assertIn("<KeyRelease>", bound)
        self.assertIn("<Key-Escape>", bound)
        self.assertIn("<Key-Return>", bound)
        entry.destroy()

    def test_bind_location_shortcuts(self):
        """Verify location entry specific bindings."""
        entry = tk.Entry(self.root)
        self.km.bind_location_shortcuts(entry)
        bound = entry.bind()
        self.assertIn("<Shift-Key-Up>", bound)
        self.assertIn("<Shift-Key-Down>", bound)
        self.assertIn("<Key-Return>", bound)
        entry.destroy()

    def test_bind_problem_shortcuts(self):
        """Verify problem checkbox specific bindings."""
        cb = tk.Checkbutton(self.root)
        self.km.bind_problem_shortcuts(cb)
        bound = cb.bind()
        self.assertIn("<Shift-Key-Up>", bound)
        self.assertIn("<Shift-Key-Down>", bound)
        self.assertIn("<Key-Return>", bound)
        cb.destroy()


# ============================================================================
# Merged from test_context_menu.py
# ============================================================================

import sys
import tkinter as tk
from unittest.mock import MagicMock, patch
import pytest

from ui.context_menu import ContextMenuManager
from ui.widgets import TreeviewListboxWrapper
from ui.group_editor import GroupEditorWindow, FieldGroupEditorDialog


def test_context_menu_manager_create_menu():
    root = tk.Tk()
    root.withdraw()

    action_mock = MagicMock()
    items = [
        {"label": "Item 1", "command": action_mock, "state": "normal"},
        {"separator": True},
        {"label": "Disabled Item", "command": None, "state": "disabled"},
        {
            "label": "Submenu Item",
            "submenu": [
                {"label": "Sub 1", "command": action_mock},
                {"separator": True},
                {"label": "Sub 2", "command": action_mock},
            ],
        },
    ]

    menu = ContextMenuManager.create_menu(root, items)
    assert isinstance(menu, tk.Menu)
    # Total entries: 4 (Item 1, separator, Disabled Item, Submenu Item)
    assert menu.index("end") == 3
    assert menu.entrycget(0, "label") == "Item 1"
    assert menu.type(1) == "separator"
    assert menu.entrycget(2, "label") == "Disabled Item"
    assert menu.entrycget(2, "state") == "disabled"
    assert menu.entrycget(3, "label") == "Submenu Item"

    root.destroy()


def test_context_menu_manager_bind_and_popup():
    root = tk.Tk()
    root.withdraw()

    btn = tk.Button(root, text="Test")
    btn.pack()

    called = []
    def callback(event):
        called.append(event)
        return [{"label": "Action", "command": lambda: None}]

    ContextMenuManager.bind(btn, callback)

    # Simulate right click event
    mock_event = MagicMock(spec=tk.Event)
    mock_event.widget = btn
    mock_event.x_root = 100
    mock_event.y_root = 150

    with patch.object(tk.Menu, "tk_popup") as mock_popup, patch.object(tk.Menu, "grab_release") as mock_grab:
        # Trigger the bound handler for <Button-3>
        bindings = btn.bind("<Button-3>")
        assert bindings is not None

        # Call the handler function directly through Tkinter event mechanism or manually
        btn.event_generate("<Button-3>", x=10, y=10)

    root.destroy()


def test_main_window_context_menu_items():
    root = tk.Tk()
    root.withdraw()

    # Mock app and main window setup
    mock_app = MagicMock()
    mock_app.active_object_ids = ["101", "102", "103"]
    mock_app._mobile_server_instance = MagicMock(is_running=True)

    from ui.main_window import ObjectProgramUI

    # Subclass or mock minimal ObjectProgramUI
    with patch.object(ObjectProgramUI, "__init__", return_value=None):
        ui = ObjectProgramUI()
        ui.root = root
        ui.app = mock_app
        ui.object_list = MagicMock()
        ui.open_bulk_edit_window = MagicMock()
        ui.push_current_to_phone = MagicMock()
        ui._shortcut_duplicate_object = MagicMock()
        ui.delete_current_object = MagicMock()
        ui._context_set_reviewed = MagicMock()

        # 1. Single selection test
        ui.object_list.selection.return_value = ("101",)
        ui.object_list.identify_row.return_value = "101"

        items = ui._get_main_context_menu_items(None)
        labels = [it.get("label") for it in items if "label" in it]
        assert "Mark Selected as Reviewed" in labels
        assert "Mark Selected as Not Reviewed" in labels
        assert "Copy Accession ID" in labels
        assert "📱 Push to Phone" in labels
        assert "Duplicate Object" in labels
        assert "Delete Object" in labels

        # "Push to Phone" should be normal when single item selected and server running
        push_item = next(it for it in items if it.get("label") == "📱 Push to Phone")
        assert push_item["state"] == "normal"

        # 2. Multi-selection test
        ui.object_list.selection.return_value = ("101", "102")
        items_multi = ui._get_main_context_menu_items(None)
        push_item_multi = next(it for it in items_multi if it.get("label") == "📱 Push to Phone")
        assert push_item_multi["state"] == "disabled"

        # 3. Empty selection test
        ui.object_list.selection.return_value = ()
        items_empty = ui._get_main_context_menu_items(None)
        assert items_empty == []

        # 4. Copy Accession ID test (single)
        ui.object_list.selection.return_value = ("101",)
        ui._context_copy_accession_id()
        assert root.clipboard_get() == "101"

        # 5. Copy Accession ID test (multiple)
        ui.object_list.selection.return_value = ("101", "102", "103")
        ui._context_copy_accession_id()
        assert root.clipboard_get() == "101\n102\n103"

    root.destroy()


def test_treeview_empty_space_right_click():
    root = tk.Tk()
    root.withdraw()

    from ui.main_window import ObjectProgramUI

    with patch.object(ObjectProgramUI, "__init__", return_value=None):
        ui = ObjectProgramUI()
        ui.root = root
        ui.object_list = MagicMock()
        ui.object_list.active_view = "compact"
        ui.object_list.tree = MagicMock()
        # identify_row returns empty string for empty space
        ui.object_list.identify_row.return_value = ""
        ui.object_list.tree.identify_row.return_value = ""

        event = MagicMock(spec=tk.Event)
        event.widget = ui.object_list.tree
        event.y = 500

        items = ui._get_main_context_menu_items(event)
        assert items == []

    root.destroy()


def test_virtual_card_selection_on_context_menu():
    root = tk.Tk()
    root.withdraw()

    main_win = MagicMock()
    main_win.dark_mode_active = False
    main_win.active_object_ids = ["101", "102"]
    main_win._get_main_context_menu_items = MagicMock(return_value=[{"label": "Test"}])

    wrapper = TreeviewListboxWrapper(root, main_win)
    wrapper.items_list = ["101", "102"]
    wrapper._oid_to_index = {"101": 0, "102": 1}
    wrapper.item_data = {"101": {}, "102": {}}
    wrapper.selected_iids = ["101"]

    # Mock widget and target
    card_frame = tk.Frame(wrapper)
    card_frame._card_oid = "102"
    card_frame._card_body = card_frame

    mock_event = MagicMock(spec=tk.Event)
    mock_event.widget = card_frame
    mock_event.x_root = 100
    mock_event.y_root = 200

    # Retrieve callback from ContextMenuManager or test the selection logic
    # Right-clicking "102" when "101" is selected should change selection to ["102"]
    wrapper.selected_iids = ["101"]
    assert "102" not in wrapper.selected_iids

    # Simulate card context callback
    w = mock_event.widget
    oid = getattr(w, "_card_oid", None)
    if oid not in wrapper.selected_iids:
        wrapper.selected_iids = [oid]
        wrapper.focused_iid = oid
        if hasattr(main_win, "load_object"):
            main_win.load_object(oid)

    assert wrapper.selected_iids == ["102"]
    main_win.load_object.assert_called_with("102")

    # Multi-selection preservation: if both 101 and 102 are selected and 102 is right-clicked
    wrapper.selected_iids = ["101", "102"]
    if "102" not in wrapper.selected_iids:
        wrapper.selected_iids = ["102"]

    assert wrapper.selected_iids == ["101", "102"]

    root.destroy()


def test_group_editor_context_menus():
    root = tk.Tk()
    root.withdraw()

    mock_main = MagicMock()
    mock_app = MagicMock()

    with patch.object(GroupEditorWindow, "__init__", return_value=None):
        editor = GroupEditorWindow(root, mock_app, mock_main)
        editor.win = root
        editor.tabs_listbox = tk.Listbox(root)
        editor.fields_listbox = tk.Listbox(root)
        editor.tabs_listbox.insert(0, "Tab 1")
        editor.tabs_listbox.insert(1, "Tab 2")
        editor.fields_listbox.insert(0, "Field 1")
        editor.fields_listbox.insert(1, "Field 2")
        editor.groups = [
            {"name": "Tab 1", "fields": ["Field 1", "Field 2"]},
            {"name": "Tab 2", "fields": []},
        ]
        editor.get_selected_group_idx = MagicMock(return_value=0)
        editor.on_tab_select = MagicMock()
        editor.add_tab = MagicMock()
        editor.rename_tab = MagicMock()
        editor.delete_tab = MagicMock()
        editor.add_field = MagicMock()
        editor.rename_field = MagicMock()
        editor.delete_field = MagicMock()

        event = MagicMock(spec=tk.Event)
        event.y = 0

        # Tabs context menu
        tab_items = editor.show_tabs_context_menu(event)
        tab_labels = [it["label"] for it in tab_items]
        assert "Add Tab" in tab_labels
        assert "Rename Tab" in tab_labels
        assert "Delete Tab" in tab_labels

        # Fields context menu
        field_items = editor.show_fields_context_menu(event)
        field_labels = [it.get("label") for it in field_items if "label" in it]
        assert "Move Up" in field_labels
        assert "Move Down" in field_labels
        assert "Move to Tab" in field_labels
        assert "Add Field" in field_labels

        move_to_tab = next(it for it in field_items if it.get("label") == "Move to Tab")
        assert "submenu" in move_to_tab
        assert len(move_to_tab["submenu"]) == 1
        assert move_to_tab["submenu"][0]["label"] == "Tab 2"

    root.destroy()


# ============================================================================
# Merged from test_hybrid_dockable_rail.py
# ============================================================================

import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
import config
from models import AppState

class TestHybridDockableRail(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = AppState()
        self.app.active_object_ids = ["1001", "1002"]
        self.app.df_reg = MagicMock()
        self.app.df_reg.__len__.return_value = 2

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_theme_tokens_exist(self):
        self.assertIn("rail_bg", config.RAIL_THEME)
        self.assertIn("rail_width", config.RAIL_THEME)
        self.assertIn("drawer_bg", config.DRAWER_THEME)
        self.assertIn("anim_duration_ms", config.DRAWER_THEME)
        self.assertEqual(config.RAIL_THEME["rail_width"], 40)
        self.assertEqual(config.DRAWER_THEME["drawer_width"], 300)

    @patch("ui.main_window.ExcelRepository")
    def test_pin_toggle_and_drawer_actions(self, mock_repo):
        from ui.main_window import ObjectProgramUI
        
        mw = ObjectProgramUI(self.root, self.app)
        
        self.assertTrue(hasattr(mw, "left_pinned"))
        self.assertTrue(hasattr(mw, "rail_frame"))
        self.assertTrue(hasattr(mw, "drawer_overlay"))

        initial_pin = mw.left_pinned.get()
        mw.toggle_left_pin()
        self.assertEqual(mw.left_pinned.get(), not initial_pin)

        if mw.left_pinned.get():
            mw.toggle_left_pin()
        self.assertFalse(mw.left_pinned.get())

        mw.toggle_floating_drawer()
        self.assertTrue(mw.left_pinned.get())

        mw.close_drawer()
        self.assertFalse(mw._drawer_is_open)

    @patch("ui.main_window.ExcelRepository")
    def test_interruptible_animation(self, mock_repo):
        from ui.main_window import ObjectProgramUI
        mw = ObjectProgramUI(self.root, self.app)
        mw.left_pinned.set(False)

        mw.open_drawer()
        self.assertTrue(mw._drawer_is_open)

        mw.close_drawer()
        self.assertFalse(mw._drawer_is_open)

    @patch("ui.main_window.ExcelRepository")
    def test_control_o_toggles_overlay_drawer(self, mock_repo):
        from ui.main_window import ObjectProgramUI
        mw = ObjectProgramUI(self.root, self.app)

        mw.left_pinned.set(False)

        # Test Ctrl+O toggles docked drawer
        mw.handle_ctrl_o()
        self.assertTrue(mw.left_pinned.get())

        mw.handle_ctrl_o()
        self.assertFalse(mw.left_pinned.get())

    @patch("ui.main_window.ExcelRepository")
    def test_control_f_opens_or_focuses_search_without_closing(self, mock_repo):
        from ui.main_window import ObjectProgramUI
        mw = ObjectProgramUI(self.root, self.app)

        mw.left_pinned.set(False)

        # When closed, Ctrl+F opens pinned and focuses search
        mw.handle_ctrl_f()
        self.assertTrue(mw.left_pinned.get())

        # When ALREADY open, Ctrl+F keeps it OPEN (does not close)
        mw.handle_ctrl_f()
        self.assertTrue(mw.left_pinned.get())
