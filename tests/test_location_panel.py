import pytest
import tkinter as tk
from ui.location_panel import LocationPanel, create_location_panel


@pytest.fixture
def tk_root():
    try:
        root = tk.Tk()
        root.withdraw()
        yield root
        root.destroy()
    except Exception as e:
        pytest.skip(f"Tkinter display not available: {e}")


def test_location_panel_init_vertical(tk_root):
    panel = create_location_panel(tk_root, mode="vertical")
    assert isinstance(panel, LocationPanel)
    assert panel.mode == "vertical"
    data = panel.get_data()
    assert "Stored as" in data
    assert "Building" in data
    assert "Floor" in data
    assert "Cabinet" in data
    assert "Shelf" in data
    assert "Extra" in data
    assert "Loaned out" in data


def test_location_panel_init_horizontal_modes(tk_root):
    panel_1row = create_location_panel(tk_root, mode="horizontal_1row")
    assert panel_1row.mode == "horizontal_1row"
    
    panel_2row = create_location_panel(tk_root, mode="horizontal_2row")
    assert panel_2row.mode == "horizontal_2row"


def test_set_layout_mode_switch(tk_root):
    panel = create_location_panel(tk_root, mode="vertical")
    assert panel.mode == "vertical"
    
    panel.set_layout_mode("horizontal_1row")
    assert panel.mode == "horizontal_1row"
    
    panel.set_layout_mode("horizontal_2row")
    assert panel.mode == "horizontal_2row"


def test_set_dark_mode(tk_root):
    panel = create_location_panel(tk_root, dark_mode=False)
    assert panel.dark_mode is False
    
    panel.set_dark_mode(True)
    assert panel.dark_mode is True


def test_data_get_set(tk_root):
    panel = create_location_panel(tk_root)
    sample = {
        "Stored as": "Mounted on wooden platform",
        "Building": "Lid's hus",
        "Floor": "2",
        "Cabinet": "C-12",
        "Shelf": "3B",
        "Extra": "Lower shelf",
        "Loaned out": "True"
    }
    panel.set_data(sample)
    data = panel.get_data()
    assert data["Stored as"] == "Mounted on wooden platform"
    assert data["Building"] == "Lid's hus"
    assert data["Floor"] == "2"
    assert data["Cabinet"] == "C-12"
    assert data["Shelf"] == "3B"
    assert data["Extra"] == "Lower shelf"
    assert data["Loaned out"] == "True"


def test_callbacks_fire(tk_root):
    events = []
    
    callbacks = {
        "on_field_change": lambda f, v: events.append(("field_change", f, v)),
        "on_commit": lambda d: events.append(("commit", d)),
        "on_preset_applied": lambda p, d: events.append(("preset_applied", p)),
        "on_preset_saved": lambda p, d: events.append(("preset_saved", p)),
        "on_loan_toggle": lambda active: events.append(("loan_toggle", active)),
    }
    
    panel = create_location_panel(tk_root, live_callbacks=callbacks)
    
    # Trigger field change
    panel.location_vars["Building"].set("Økern")
    assert any(e[0] == "field_change" and e[1] == "Building" and e[2] == "Økern" for e in events)
    
    # Trigger preset apply
    panel.apply_active_preset()
    assert any(e[0] == "preset_applied" for e in events)
    assert any(e[0] == "commit" for e in events)


# ============================================================================
# Merged from test_location_center_toggle.py
# ============================================================================

import os
import sys
import tkinter as tk
from unittest.mock import MagicMock
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import config
from ui.unified_settings import UnifiedSettingsWindow
from ui.location_panel import LocationPanel, create_location_panel


@pytest.fixture
def loc_toggle_tk_root():
    try:
        root = tk.Tk()
        root.withdraw()
        yield root
        root.destroy()
    except Exception as e:
        pytest.skip(f"Tkinter display not available: {e}")


def test_unified_settings_location_center_live_callback(loc_toggle_tk_root):
    events = {}

    def _callback(val):
        events["location_center"] = val

    win = UnifiedSettingsWindow(
        loc_toggle_tk_root,
        initial_tab="layout",
        live_callbacks={"location_center": _callback}
    )
    win.var_location_center.set(True)
    win._notify_live("location_center", True)

    assert events.get("location_center") is True
    win.win.destroy()


def test_unified_settings_push_location_center_to_app(loc_toggle_tk_root):
    mock_app = MagicMock()
    mock_app.show_list_var = tk.BooleanVar(value=True)
    mock_app.show_search_var = tk.BooleanVar(value=True)
    mock_app.show_reg_var = tk.BooleanVar(value=True)
    mock_app.show_images_var = tk.BooleanVar(value=True)
    mock_app.location_in_center_var = tk.BooleanVar(value=False)
    mock_app.draft_location_in_center_var = tk.BooleanVar(value=False)
    mock_app.show_image_tools_var = tk.BooleanVar(value=True)
    mock_app.show_bulk_edit_var = tk.BooleanVar(value=True)
    mock_app.image_stack_var = tk.BooleanVar(value=False)
    mock_app.toolbar_vars = {}

    win = UnifiedSettingsWindow(loc_toggle_tk_root, app_ref=mock_app, initial_tab="layout")
    win.var_location_center.set(True)
    win._push_layout_to_app()

    assert mock_app.location_in_center_var.get() is True
    assert mock_app.draft_location_in_center_var.get() is True
    win.win.destroy()


def test_unified_settings_save_location_in_center(loc_toggle_tk_root, tmp_path, monkeypatch):
    test_prefs_file = str(tmp_path / "user_prefs.json")
    monkeypatch.setattr(config, "_PREFS_PATH", test_prefs_file)
    monkeypatch.setattr(config, "_prefs_cache", None)

    win = UnifiedSettingsWindow(loc_toggle_tk_root, initial_tab="layout")
    win.var_location_center.set(True)
    win.save_settings()

    loaded = config.load_prefs()
    assert loaded.get("location_in_center") is True
    win.win.destroy()


def test_location_panel_integration_modes(loc_toggle_tk_root):
    loc_vars = {
        "Stored as": tk.StringVar(value=""),
        "Building": tk.StringVar(value=""),
        "Floor": tk.StringVar(value=""),
        "Cabinet": tk.StringVar(value=""),
        "Shelf": tk.StringVar(value=""),
        "Extra": tk.StringVar(value=""),
        "Loaned out": tk.StringVar(value="False"),
    }

    vert_panel = create_location_panel(loc_toggle_tk_root, mode="vertical", location_vars=loc_vars)
    assert isinstance(vert_panel, LocationPanel)
    assert vert_panel.mode == "vertical"

    horiz_panel = create_location_panel(loc_toggle_tk_root, mode="horizontal_1row", location_vars=loc_vars)
    assert isinstance(horiz_panel, LocationPanel)
    assert horiz_panel.mode == "horizontal_1row"

    # Test dark mode propagation
    vert_panel.set_dark_mode(True)
    assert vert_panel.dark_mode is True
    horiz_panel.set_dark_mode(True)
    assert horiz_panel.dark_mode is True


def test_hide_images_docks_location_at_bottom_and_collapses_middle_frame(loc_toggle_tk_root):
    """Hiding images collapses middle_frame from panes and docks Location at the bottom of root."""
    from tkinter import ttk
    from ui.main_window import ObjectProgramUI

    class _DummyUI:
        _sync_middle_panes = ObjectProgramUI._sync_middle_panes
        toggle_location_panel = ObjectProgramUI.toggle_location_panel

    ui = _DummyUI()
    ui.root = loc_toggle_tk_root
    ui.dark_mode_active = False
    ui.show_images_var = tk.BooleanVar(value=True)
    ui.location_in_center_var = tk.BooleanVar(value=True)
    ui.focus_mode_var = tk.BooleanVar(value=False)
    ui.focus_visibility_vars = {}
    ui.refresh_image_view = lambda: None

    ui.panes = ttk.Panedwindow(loc_toggle_tk_root, orient="horizontal")
    ui.panes.pack(fill="both", expand=True)

    ui.left_frame = ttk.Frame(ui.panes)
    ui.middle_frame = ttk.Frame(ui.panes)
    ui.reg_outer = ttk.Frame(ui.panes)
    ui.panes.add(ui.left_frame, weight=1)
    ui.panes.add(ui.middle_frame, weight=1)
    ui.panes.add(ui.reg_outer, weight=1)

    ui.object_context_bar = tk.Frame(loc_toggle_tk_root)
    ui.middle_panes = ttk.Panedwindow(ui.middle_frame, orient="vertical")
    ui.middle_panes.pack(fill="both", expand=True)
    ui.image_panel = tk.Frame(ui.middle_panes)
    ui.image_panel.image_mode = None
    ui.right_frame = ui.image_panel
    ui._middle_loc_slot = tk.Frame(ui.middle_panes)
    ui.loc_frame_horizontal = tk.Frame(loc_toggle_tk_root)

    # 1. Images visible + Location in center -> middle_frame in panes, loc inside _middle_loc_slot
    ui._sync_middle_panes()
    assert str(ui.middle_frame) in ui.panes.panes()
    assert str(ui.image_panel) == ui.middle_panes.panes()[0]
    assert str(ui._middle_loc_slot) in ui.middle_panes.panes()
    assert ui.loc_frame_horizontal.pack_info()["in"] == ui._middle_loc_slot

    # 2. Hide images (F8) + Location in center -> middle_frame collapsed, Location docked at bottom of root
    ui.show_images_var.set(False)
    ui._sync_middle_panes()
    assert str(ui.middle_frame) not in ui.panes.panes()
    assert ui.loc_frame_horizontal.pack_info()["in"] == loc_toggle_tk_root
    assert ui.loc_frame_horizontal.pack_info()["side"] == "bottom"
    assert ui.object_context_bar.pack_info()["in"] == loc_toggle_tk_root
    assert ui.object_context_bar.pack_info()["side"] == "top"

    # 3. Turn images back on -> middle_frame restored, image_panel at index 0, loc back in middle_panes
    ui.show_images_var.set(True)
    ui._sync_middle_panes()
    assert str(ui.middle_frame) in ui.panes.panes()
    assert str(ui.image_panel) == ui.middle_panes.panes()[0]
    assert ui.loc_frame_horizontal.pack_info()["in"] == ui._middle_loc_slot
    assert ui.object_context_bar.pack_info()["in"] == ui.middle_frame

    # 4. Offline mode keeps middle_frame open with image_panel (Summary Hub) above Location
    ui.image_panel.image_mode = "offline"
    ui.location_in_center_var.set(True)
    ui.show_images_var.set(True)
    ui._sync_middle_panes()
    assert str(ui.middle_frame) in ui.panes.panes()
    assert ui.middle_panes.panes()[0] == str(ui.image_panel)
    assert ui.middle_panes.panes()[1] == str(ui._middle_loc_slot)
    assert ui.loc_frame_horizontal.pack_info()["in"] == ui._middle_loc_slot

    # 5. Hide images (F8) + Location on Left -> middle_frame collapsed AND loc_frame_horizontal unpacked
    ui.location_in_center_var.set(False)
    ui.show_images_var.set(False)
    ui._sync_middle_panes()
    assert str(ui.middle_frame) not in ui.panes.panes()
    assert ui.loc_frame_horizontal.winfo_manager() == ""


def test_real_main_window_storage_location_always_below_images():
    """Regression: on fresh startup and across online/folder/missing/offline modes,
    Storage Location must sit strictly below the image pane, and F8 must dock it
    below panes and above the status bar without overlapping other panels."""
    import config
    from models import AppState
    from ui.main_window import ObjectProgramUI

    root = tk.Tk()
    try:
        root.geometry("1280x800+50+50")
        app = AppState()
        app.config = next(iter(config.DATABASE_CONFIGS.values()))
        ui = ObjectProgramUI(root, app)
        ui.apply_config()
        root.update_idletasks()
        root.update()

        # 1. Default startup (no image mode yet): image_panel at index 0, Location below it
        assert ui.location_in_center_var.get() is True
        assert ui.middle_panes.panes()[0] == str(ui.right_frame)
        assert ui.middle_panes.panes()[1] == str(ui._middle_loc_slot)
        assert ui.right_frame.winfo_rooty() < ui.loc_frame_horizontal.winfo_rooty()

        # 2. Online, Folder, and Offline modes all keep Location strictly below image_panel
        for mode in ("online", "folder", "offline"):
            ui.image_panel.image_mode = mode
            ui._sync_middle_panes()
            root.update_idletasks()
            root.update()
            assert str(ui.middle_frame) in ui.panes.panes(), f"middle_frame collapsed in {mode} mode"
            assert ui.middle_panes.panes()[0] == str(ui.right_frame), f"image_panel not on top in {mode} mode"
            assert ui.middle_panes.panes()[1] == str(ui._middle_loc_slot), f"location not below images in {mode} mode"
            assert ui.right_frame.winfo_rooty() < ui.loc_frame_horizontal.winfo_rooty(), f"y-order inverted in {mode} mode"

        # 3. Pressing F8 with Location in default bottom position hides images and docks Location
        #    cleanly below panes and above the status bar with non-collapsed height
        ui.show_images_var.set(False)
        ui._sync_middle_panes()
        root.update_idletasks()
        root.update()
        assert str(ui.middle_frame) not in ui.panes.panes()
        assert ui.loc_frame_horizontal.winfo_ismapped() == 1
        assert ui.loc_frame_horizontal.winfo_height() > 20
        panes_bottom = ui.panes.winfo_rooty() + ui.panes.winfo_height()
        loc_top = ui.loc_frame_horizontal.winfo_rooty()
        status_top = ui._status_bar_frame.winfo_rooty()
        assert panes_bottom <= loc_top + 2, f"Location ({loc_top}) overlaps panes bottom ({panes_bottom})"
        assert loc_top < status_top, f"Location ({loc_top}) should sit above status bar ({status_top})"

        # 4. Pressing F8 with Location in Left column hides the entire middle column and unpacks horizontal Location
        ui.location_in_center_var.set(False)
        ui.toggle_location_panel()
        root.update_idletasks()
        assert str(ui.middle_frame) not in ui.panes.panes()
        assert ui.loc_frame_horizontal.winfo_manager() == ""
    finally:
        try:
            root.destroy()
        except Exception:
            pass


def test_summary_hub_dark_mode_and_empty_source_actions(loc_toggle_tk_root):
    """No-images Specimen Summary Hub renders Dark Mode tokens, humanized flags, and folder/online/hide CTAs."""
    import pandas as pd
    from ui.image_panel import ImagePanel

    mock_app = MagicMock()
    mock_app.df_reg = pd.DataFrame(
        [{"Genus": "Betula", "Species": "pendula", "Collector": "Linné"}],
        index=["101"],
    )
    mock_app.df_obs = pd.DataFrame(
        [{"Reviewed": False, "Box_Label_Problem": True, "Collection_Date_Problem": True}],
        index=["101"],
    )
    mock_app.config = {
        "ui_sections": {
            "problems": [
                {"name": "Box_Label_Problem"},
                {"name": "Collection_Date_Problem"},
            ]
        }
    }

    panel = ImagePanel(loc_toggle_tk_root, app=mock_app, dark_mode=True)
    panel.image_mode = None
    panel.render_specimen_summary_hub("101")
    loc_toggle_tk_root.update_idletasks()

    texts = []
    bgs = []

    def _walk(w):
        for c in w.winfo_children():
            try:
                t = c.cget("text")
                if t:
                    texts.append(t)
            except Exception:
                pass
            try:
                bgs.append(c.cget("bg"))
            except Exception:
                pass
            _walk(c)

    _walk(panel.image_container)
    assert "Select Image Folder…" in texts
    assert "Use Online Photos" in texts
    assert "Hide Photo Pane (F8)" in texts
    assert "• Box Label Issue" in texts
    assert "• Collection Date Issue" in texts
    assert "#222723" in bgs
    assert "#ffffff" not in bgs
    panel.destroy()
