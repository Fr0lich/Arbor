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
def tk_root():
    try:
        root = tk.Tk()
        root.withdraw()
        yield root
        root.destroy()
    except Exception as e:
        pytest.skip(f"Tkinter display not available: {e}")


def test_unified_settings_location_center_live_callback(tk_root):
    events = {}

    def _callback(val):
        events["location_center"] = val

    win = UnifiedSettingsWindow(
        tk_root,
        initial_tab="layout",
        live_callbacks={"location_center": _callback}
    )
    win.var_location_center.set(True)
    win._notify_live("location_center", True)

    assert events.get("location_center") is True
    win.win.destroy()


def test_unified_settings_push_layout_to_app(tk_root):
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

    win = UnifiedSettingsWindow(tk_root, app_ref=mock_app, initial_tab="layout")
    win.var_location_center.set(True)
    win._push_layout_to_app()

    assert mock_app.location_in_center_var.get() is True
    assert mock_app.draft_location_in_center_var.get() is True
    win.win.destroy()


def test_unified_settings_save_location_in_center(tk_root, tmp_path, monkeypatch):
    test_prefs_file = str(tmp_path / "user_prefs.json")
    monkeypatch.setattr(config, "_PREFS_PATH", test_prefs_file)
    monkeypatch.setattr(config, "_prefs_cache", None)

    win = UnifiedSettingsWindow(tk_root, initial_tab="layout")
    win.var_location_center.set(True)
    win.save_settings()

    loaded = config.load_prefs()
    assert loaded.get("location_in_center") is True
    win.win.destroy()


def test_location_panel_integration_modes(tk_root):
    loc_vars = {
        "Stored as": tk.StringVar(value=""),
        "Building": tk.StringVar(value=""),
        "Floor": tk.StringVar(value=""),
        "Cabinet": tk.StringVar(value=""),
        "Shelf": tk.StringVar(value=""),
        "Extra": tk.StringVar(value=""),
        "Loaned out": tk.StringVar(value="False"),
    }

    vert_panel = create_location_panel(tk_root, mode="vertical", location_vars=loc_vars)
    assert isinstance(vert_panel, LocationPanel)
    assert vert_panel.mode == "vertical"

    horiz_panel = create_location_panel(tk_root, mode="horizontal_1row", location_vars=loc_vars)
    assert isinstance(horiz_panel, LocationPanel)
    assert horiz_panel.mode == "horizontal_1row"

    # Test dark mode propagation
    vert_panel.set_dark_mode(True)
    assert vert_panel.dark_mode is True
    horiz_panel.set_dark_mode(True)
    assert horiz_panel.dark_mode is True


def test_hide_images_docks_location_at_bottom_and_collapses_middle_frame(tk_root):
    """Hiding images collapses middle_frame from panes and docks Location at the bottom of root."""
    from tkinter import ttk
    from ui.main_window import ObjectProgramUI

    class _DummyUI:
        _sync_middle_panes = ObjectProgramUI._sync_middle_panes
        toggle_location_panel = ObjectProgramUI.toggle_location_panel

    ui = _DummyUI()
    ui.root = tk_root
    ui.dark_mode_active = False
    ui.show_images_var = tk.BooleanVar(value=True)
    ui.location_in_center_var = tk.BooleanVar(value=True)
    ui.focus_mode_var = tk.BooleanVar(value=False)
    ui.focus_visibility_vars = {}
    ui.refresh_image_view = lambda: None

    ui.panes = ttk.Panedwindow(tk_root, orient="horizontal")
    ui.panes.pack(fill="both", expand=True)

    ui.left_frame = ttk.Frame(ui.panes)
    ui.middle_frame = ttk.Frame(ui.panes)
    ui.reg_outer = ttk.Frame(ui.panes)
    ui.panes.add(ui.left_frame, weight=1)
    ui.panes.add(ui.middle_frame, weight=1)
    ui.panes.add(ui.reg_outer, weight=1)

    ui.object_context_bar = tk.Frame(tk_root)
    ui.middle_panes = ttk.Panedwindow(ui.middle_frame, orient="vertical")
    ui.middle_panes.pack(fill="both", expand=True)
    ui.image_panel = tk.Frame(ui.middle_panes)
    ui.image_panel.image_mode = None
    ui.right_frame = ui.image_panel
    ui._middle_loc_slot = tk.Frame(ui.middle_panes)
    ui.loc_frame_horizontal = tk.Frame(tk_root)

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
    assert ui.loc_frame_horizontal.pack_info()["in"] == tk_root
    assert ui.loc_frame_horizontal.pack_info()["side"] == "bottom"
    assert ui.object_context_bar.pack_info()["in"] == tk_root
    assert ui.object_context_bar.pack_info()["side"] == "top"

    # 3. Turn images back on -> middle_frame restored, image_panel at index 0, loc back in middle_panes
    ui.show_images_var.set(True)
    ui._sync_middle_panes()
    assert str(ui.middle_frame) in ui.panes.panes()
    assert str(ui.image_panel) == ui.middle_panes.panes()[0]
    assert ui.loc_frame_horizontal.pack_info()["in"] == ui._middle_loc_slot
    assert ui.object_context_bar.pack_info()["in"] == ui.middle_frame

    # 4. Hide images + Location on Left -> middle_frame collapsed AND loc_frame_horizontal unpacked
    ui.location_in_center_var.set(False)
    ui.show_images_var.set(False)
    ui._sync_middle_panes()
    assert str(ui.middle_frame) not in ui.panes.panes()
    assert ui.loc_frame_horizontal.winfo_manager() == ""


def test_summary_hub_dark_mode_and_empty_source_actions(tk_root):
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

    panel = ImagePanel(tk_root, app=mock_app, dark_mode=True)
    panel.image_mode = None
    panel.render_specimen_summary_hub("101")
    tk_root.update_idletasks()

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
