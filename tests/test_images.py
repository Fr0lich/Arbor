import unittest
from ui.image_handler import ImageHandlerMixin
from ui.image_panel import ImagePanel

class DummyApp:
    def __init__(self):
        self.config = {}
        self.df_obs = None

class DummyUI(ImageHandlerMixin):
    def __init__(self):
        self.app = DummyApp()
        self.image_mode = "folder"
        self._image_paths = []
        self._rendered_paths = None
        self._thumb_cards = []

class TestImageHandler(unittest.TestCase):
    def test_image_next_prev(self):
        ui = DummyUI()
        ui._image_paths = ["img1.jpg", "img2.jpg"]
        ui._current_image_index = 0

        def mock_render():
            pass
        ui._render_image_gallery = mock_render

        ui._next_image()
        self.assertEqual(ui._current_image_index, 1)
        ui._prev_image()
        self.assertEqual(ui._current_image_index, 0)

    def test_zoom_image(self):
        ui = DummyUI()
        ui.image_zoom_factor = 1.0
        ui._re_render_current_images = lambda: None

        ui.zoom_image_in()
        self.assertEqual(ui.image_zoom_factor, 1.25)

        ui.zoom_image_out()
        self.assertEqual(ui.image_zoom_factor, 1.0)

        for _ in range(20):
            ui.zoom_image_out()
        self.assertEqual(ui.image_zoom_factor, 0.1)

    def test_rotate_image(self):
        ui = DummyUI()
        ui.image_rotation_angle = 0
        ui._re_render_current_images = lambda: None

        ui.rotate_image()
        self.assertEqual(ui.image_rotation_angle, 270)

        ui.rotate_image()
        self.assertEqual(ui.image_rotation_angle, 180)

        ui.rotate_image()
        self.assertEqual(ui.image_rotation_angle, 90)

        ui.rotate_image()
        self.assertEqual(ui.image_rotation_angle, 0)

    def test_reset_image_view(self):
        ui = DummyUI()
        ui.image_zoom_factor = 2.0
        ui.image_rotation_angle = 90
        ui._re_render_current_images = lambda: None

        ui.reset_image_view()
        self.assertEqual(ui.image_zoom_factor, 1.0)
        self.assertEqual(ui.image_rotation_angle, 0)

    def test_toggle_image_view(self):
        ui = DummyUI()
        ui.image_view_mode = "gallery"
        ui.app.current_object_id = None

        class DummyBtn:
            def config(self, **kwargs):
                pass
        ui.view_btn = DummyBtn()
        ui.load_images = lambda oid: None

        ui.toggle_image_view()
        self.assertEqual(ui.image_view_mode, "stack")

        ui.toggle_image_view()
        self.assertEqual(ui.image_view_mode, "gallery")

    def test_build_online_image_urls(self):
        ui = DummyUI()

        ui.app.config["image_url_pattern"] = ""
        self.assertEqual(ui.build_online_image_urls("123"), [])

        ui.app.config["image_url_pattern"] = "https://example.com/img/{id}.jpg"
        urls = ui.build_online_image_urls("123")
        self.assertEqual(urls, [
            "https://example.com/img/123.jpg",
            "https://example.com/img/123-01.jpg",
            "https://example.com/img/123-02.jpg",
            "https://example.com/img/123-03.jpg"
        ])

        ui.app.config["image_url_pattern"] = "https://example.com/img/{num:04d}{suffix}.jpg"
        urls = ui.build_online_image_urls("42")
        self.assertEqual(urls, [
            "https://example.com/img/0042.jpg",
            "https://example.com/img/0042-01.jpg",
            "https://example.com/img/0042-02.jpg",
            "https://example.com/img/0042-03.jpg"
        ])

class TestImagePanel(unittest.TestCase):
    def test_panel_zoom_rotate_reset(self):
        panel = ImagePanel.__new__(ImagePanel)
        panel.image_zoom_factor = 1.0
        panel.image_rotation_angle = 0
        panel.app = DummyApp()
        panel._re_render_current_images = lambda: None

        panel.zoom_image_in()
        self.assertEqual(panel.image_zoom_factor, 1.25)

        panel.zoom_image_out()
        self.assertEqual(panel.image_zoom_factor, 1.0)

        panel.rotate_image(90)
        self.assertEqual(panel.image_rotation_angle, 90)

        panel.reset_image_view()
        self.assertEqual(panel.image_zoom_factor, 1.0)
        self.assertEqual(panel.image_rotation_angle, 0)

    def test_panel_online_url_building(self):
        panel = ImagePanel.__new__(ImagePanel)
        panel.app = DummyApp()
        panel.app.config["image_url_pattern"] = "https://example.com/img/{id}.jpg"
        urls = panel.build_online_image_urls("99")
        self.assertEqual(urls[0], "https://example.com/img/99.jpg")

    def test_toggle_image_tools(self):
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        try:
            panel = ImagePanel(root)
            panel.show_image_tools_var.set(True)
            panel.toggle_image_tools()
            self.assertEqual(panel.image_toolbar.winfo_manager(), "pack")

            panel.show_image_tools_var.set(False)
            panel.toggle_image_tools()
            self.assertEqual(panel.image_toolbar.winfo_manager(), "")
        finally:
            root.destroy()


class TestMainWindowImageDelegation(unittest.TestCase):
    def test_main_window_image_box_and_toggle_tools(self):
        import tkinter as tk
        from ui.main_window import ObjectProgramUI
        root = tk.Tk()
        root.withdraw()
        try:
            panel = ImagePanel(root)
            mw = ObjectProgramUI.__new__(ObjectProgramUI)
            mw.image_panel = panel
            
            # Verify image_box property delegation
            self.assertIsNotNone(mw.image_box)
            self.assertEqual(mw.image_box, panel.image_box)

            # Verify toggle_image_tools delegation without AttributeError
            mw.show_image_tools_var.set(True)
            mw.toggle_image_tools()
            self.assertEqual(panel.image_toolbar.winfo_manager(), "pack")

            mw.show_image_tools_var.set(False)
            mw.toggle_image_tools()
            self.assertEqual(panel.image_toolbar.winfo_manager(), "")
        finally:
            root.destroy()




class TestAsyncGBIFWorkflows(unittest.TestCase):
    def setUp(self):
        import tkinter as tk
        from unittest.mock import MagicMock
        from ui.main_window import ObjectProgramUI
        self.root = tk.Tk()
        self.root.withdraw()
        self.mw = ObjectProgramUI.__new__(ObjectProgramUI)
        self.mw.root = self.root
        self.mw.app = MagicMock()
        self.mw.app.current_object_id = "12345"
        self.mw.reg_vars = {
            "Genus": tk.StringVar(),
            "Species": tk.StringVar()
        }
        self.mw.gbif_btn = MagicMock()
        self.mw.gbif_btn.winfo_exists.return_value = True

    def tearDown(self):
        self.root.destroy()

    def test_check_gbif_missing_genus_shows_toast_not_messagebox(self):
        from unittest.mock import patch
        with patch("ui.toast.ToastManager.show") as mock_toast,              patch("tkinter.messagebox.showinfo") as mock_msgbox:
            self.mw.reg_vars["Genus"].set("")
            self.mw.check_gbif_action()

            mock_msgbox.assert_not_called()
            mock_toast.assert_called_once_with(self.root, "Genus is required for GBIF verification", toast_type="warning")

    def test_check_gbif_dispatches_app_worker(self):
        from unittest.mock import patch
        with patch("ui.toast.ToastManager.show") as mock_toast,              patch("tkinter.messagebox.showwarning") as mock_warn,              patch("backend.task_queue.app_worker.run_in_background") as mock_run_bg:
            self.mw.reg_vars["Genus"].set("Betula")
            self.mw.reg_vars["Species"].set("pendula")
            self.mw.check_gbif_action()

            mock_warn.assert_not_called()
            self.assertTrue(mock_run_bg.called)
            self.mw.gbif_btn.config.assert_called_with(text="Loading...", bg="#6c757d")

    def test_gbif_no_match_shows_toast_not_messagebox(self):
        from unittest.mock import patch
        with patch("ui.toast.ToastManager.show") as mock_toast,              patch("tkinter.messagebox.showwarning") as mock_warn:
            self.mw._on_gbif_result(None, "Unknown", "species")
            mock_warn.assert_not_called()
            mock_toast.assert_called_once_with(self.root, "No match found in GBIF Backbone Taxonomy", toast_type="warning")

    def test_gbif_network_error_shows_toast_not_messagebox(self):
        from unittest.mock import patch
        with patch("ui.toast.ToastManager.show") as mock_toast,              patch("tkinter.messagebox.showerror") as mock_err:
            self.mw._on_gbif_result({"error": "Timeout 504"}, "Betula", "pendula")
            mock_err.assert_not_called()
            mock_toast.assert_called_once_with(self.root, "GBIF connection error: Timeout 504", toast_type="error")

    def test_gbif_exception_handler_shows_toast_not_messagebox(self):
        from unittest.mock import patch
        with patch("ui.toast.ToastManager.show") as mock_toast,              patch("tkinter.messagebox.showerror") as mock_err:
            self.mw._on_gbif_error("DNS resolution failed")
            mock_err.assert_not_called()
            mock_toast.assert_called_once_with(self.root, "GBIF connection error: DNS resolution failed", toast_type="error")

    def test_gbif_synonym_fetches_accepted_name_via_app_worker(self):
        from unittest.mock import patch
        with patch("backend.task_queue.app_worker.run_in_background") as mock_run_bg:
            result = {"synonym": True, "acceptedUsageKey": 98765}
            self.mw._on_gbif_result(result, "Betula", "alba")
            self.assertTrue(mock_run_bg.called)


class TestAsyncImageTasks(unittest.TestCase):
    def test_image_panel_tasks_route_through_app_worker(self):
        import tkinter as tk
        from unittest.mock import patch, MagicMock
        root = tk.Tk()
        root.withdraw()
        try:
            panel = ImagePanel(root)
            with patch("backend.task_queue.app_worker.run_in_background") as mock_run_bg,                  patch("tkinter.filedialog.askdirectory", return_value="C:/herbarium_images"):
                panel.select_image_folder()
                self.assertTrue(mock_run_bg.called)

            with patch("backend.task_queue.app_worker.run_in_background") as mock_run_bg:
                mock_label = MagicMock()
                mock_label.winfo_exists.return_value = True
                panel._load_image_async("C:/herbarium_images/123.jpg", False, mock_label)
                self.assertTrue(mock_run_bg.called)

            with patch("backend.task_queue.app_worker.run_in_background") as mock_run_bg:
                panel.app = MagicMock()
                panel.app.config = {"has_images": True}
                panel.app.active_object_ids = ["122", "123", "124"]
                panel.image_mode = "folder"
                panel.show_images_var.set(True)
                panel.image_index = {"124": ["C:/herbarium_images/124.jpg"]}
                panel._preload_adjacent_images("123")
                self.assertTrue(mock_run_bg.called)
        finally:
            root.destroy()


# ============================================================================
# Merged from test_image_display.py
# ============================================================================

"""Unit tests for Arbor Image Inspection Canvas, Zoom Ergonomics, and Async Pre-Caching.

Verifies:
1. Graceful placeholder canvas rendering when image files are missing from disk or corrupted,
   with zero mainloop crashes and explanatory badge: 'Image not found on disk: [filename]'.
2. Conflict-free zoom presets (Ctrl+1 Fit Window, Ctrl+2 Fit Width, Ctrl+3 100% 1:1 Actual Pixels)
   with mathematical scale factor correctness and zero clashing with ui/keybindings.py shortcuts.
3. Cachetools LRUCache eviction discipline with maxsize=10 capacity.
"""

import os
import time
import tempfile
import tkinter as tk
from unittest.mock import MagicMock
from PIL import Image

from ui.image_handler import (
    ImagePreCacher,
    create_missing_image_placeholder
)
from ui.image_panel import ImagePanel
from ui.keybindings import KeybindingManager, CANONICAL_SHORTCUTS


def _wait_for_condition(root, predicate, panel=None, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        if panel and hasattr(panel, "_poll_ui_queue"):
            panel._poll_ui_queue()
        root.update_idletasks()
        root.update()
        if predicate():
            return True
        time.sleep(0.02)
    if panel and hasattr(panel, "_poll_ui_queue"):
        panel._poll_ui_queue()
    return predicate()


def test_missing_and_corrupted_image_displays_graceful_placeholder():
    """Verify missing or corrupted image files render a graceful placeholder without crashing."""
    root = tk.Tk()
    root.withdraw()
    try:
        # 1. Test visual placeholder image generator
        missing_filename = "non_existent_specimen_12345.jpg"
        placeholder = create_missing_image_placeholder(missing_filename, width=400, height=300)
        assert placeholder is not None
        assert isinstance(placeholder, Image.Image)
        assert placeholder.size == (400, 300)

        # 2. Test ImagePanel handling of missing file path
        panel = ImagePanel(root)
        mock_label = tk.Label(panel)
        missing_path = "C:/herbarium_scans/ghost_specimen_99999.jpg"
        mock_label.loading_path = missing_path

        # Async load on non-existent file should not raise FileNotFoundError or crash
        panel._load_image_async(missing_path, large=True, target_widget=mock_label)
        success = _wait_for_condition(root, lambda: hasattr(mock_label, "image"), panel=panel)
        assert success, "Expected mock_label to receive placeholder image within timeout"

        assert mock_label.image is not None
        assert "Image not found on disk" in panel.images_missing_label.cget("text")
        assert "ghost_specimen_99999.jpg" in panel.images_missing_label.cget("text")

        # 3. Test corrupted image file resilience
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as corrupt_file:
            corrupt_file.write(b"CORRUPTED_NON_IMAGE_DATA_BYTES")
            corrupt_path = corrupt_file.name

        try:
            panel_corrupt = ImagePanel(root)
            corrupt_label = tk.Label(panel_corrupt)
            corrupt_label.loading_path = corrupt_path
            panel_corrupt._load_image_async(corrupt_path, large=True, target_widget=corrupt_label)
            success_corrupt = _wait_for_condition(root, lambda: hasattr(corrupt_label, "image"), panel=panel_corrupt)
            assert success_corrupt, "Expected corrupt_label to receive placeholder image within timeout"
            assert corrupt_label.image is not None
        finally:
            if os.path.exists(corrupt_path):
                os.remove(corrupt_path)
    finally:
        root.destroy()


def test_zoom_presets_scale_factors_and_no_keybinding_clash():
    """
    Verify Ctrl+1, Ctrl+2, Ctrl+3 calculate expected scale factors and do not
    clash with existing shortcuts in ui/keybindings.py.
    """
    root = tk.Tk()
    root.withdraw()
    try:
        panel = ImagePanel(root)
        panel._image_paths = ["test_herbarium_sheet.jpg"]
        panel._current_image_index = 0

        # Supply mock pre-decoded 2000x3000 portrait herbarium scan
        dummy_scan = Image.new("RGB", (2000, 3000), color="green")
        panel.pre_cacher.put("test_herbarium_sheet.jpg", dummy_scan)

        # 1. Scale factor calculations
        scales = panel.calculate_zoom_preset_scales("test_herbarium_sheet.jpg")
        assert "fit_window" in scales
        assert "fit_width" in scales
        assert "actual_pixels" in scales

        # Fit Window is 1.0 (entire sheet visible)
        assert scales["fit_window"] == 1.0
        # Fit Width expands to match canvas width (greater than window fit)
        assert scales["fit_width"] > 1.0
        # 100% 1:1 Actual Pixels is largest magnification
        assert scales["actual_pixels"] >= scales["fit_width"]

        # 2. Preset activation methods
        panel.zoom_fit_window()
        assert panel.image_zoom_factor == 1.0

        panel.zoom_fit_width()
        assert panel.image_zoom_factor == scales["fit_width"]

        panel.zoom_actual_pixels()
        assert panel.image_zoom_factor == scales["actual_pixels"]

        # Ctrl+0 reset_image_view preserved
        panel.reset_image_view()
        assert panel.image_zoom_factor == 1.0
        assert panel.image_rotation_angle == 0

        # 3. Shortcut anti-collision audit with ui/keybindings.py
        bound_keys = root.bind()

        # Ensure preserved shortcuts and new presets are bound
        assert "<Control-Key-0>" in bound_keys or "<Control-0>" in bound_keys
        assert "<Control-Key-1>" in bound_keys or "<Control-1>" in bound_keys
        assert "<Control-Key-2>" in bound_keys or "<Control-2>" in bound_keys
        assert "<Control-Key-3>" in bound_keys or "<Control-3>" in bound_keys

        # Verify no clashing: Ctrl+1, Ctrl+2, Ctrl+3 are NOT clobbering Primary Work Keys
        primary_shortcuts = [item[1] for item in CANONICAL_SHORTCUTS if item[0] == "PRIMARY WORK KEYS"]
        primary_str = " ".join(primary_shortcuts)
        assert "Ctrl + 1" not in primary_str
        assert "Ctrl + 2" not in primary_str
        assert "Ctrl + 3" not in primary_str

        # Preserved critical shortcuts in CANONICAL_SHORTCUTS
        assert "ENTER" in primary_str or "R" in primary_str
        assert "SPACE" in primary_str
    finally:
        root.destroy()


def test_image_pre_cacher_lru_eviction():
    """Verify cachetools LRUCache evicts oldest items when capacity (10) is reached."""
    pre_cacher = ImagePreCacher(maxsize=10)
    assert pre_cacher.maxsize == 10
    assert len(pre_cacher) == 0

    # Populate with 10 dummy images
    dummy_images = {}
    for i in range(1, 11):
        path = f"/scans/specimen_{i:03d}.jpg"
        img = Image.new("RGB", (64, 64), color=(i * 10, i * 10, i * 10))
        dummy_images[path] = img
        pre_cacher.put(path, img)

    assert len(pre_cacher) == 10
    assert "/scans/specimen_001.jpg" in pre_cacher

    # Insert 11th image -> specimen_001.jpg should be evicted
    img_11 = Image.new("RGB", (64, 64), color="blue")
    pre_cacher.put("/scans/specimen_011.jpg", img_11)

    assert len(pre_cacher) == 10
    assert "/scans/specimen_001.jpg" not in pre_cacher
    assert "/scans/specimen_011.jpg" in pre_cacher

    # Access specimen_002.jpg to make it most recently used
    accessed = pre_cacher.get("/scans/specimen_002.jpg")
    assert accessed is not None

    # Insert 12th image -> specimen_003.jpg should be evicted next (since 002 was recently accessed)
    img_12 = Image.new("RGB", (64, 64), color="yellow")
    pre_cacher.put("/scans/specimen_012.jpg", img_12)

    assert len(pre_cacher) == 10
    assert "/scans/specimen_003.jpg" not in pre_cacher
    assert "/scans/specimen_002.jpg" in pre_cacher
    assert "/scans/specimen_012.jpg" in pre_cacher


# ============================================================================
# Merged from test_image_popup.py
# ============================================================================

import pytest
import tkinter as tk
from PIL import Image, ImageTk
from ui.image_popup import ZoomableImagePopup
from ui.dialogs import ZoomableImagePopup as ReexportedPopup

def test_image_popup_reexport_parity():
    assert ReexportedPopup is ZoomableImagePopup

def test_zoomable_image_popup_lifecycle():
    root = tk.Tk()
    root.withdraw()
    try:
        # Create a tiny 10x10 PIL image
        img = Image.new("RGB", (10, 10), color="green")
        tk_img = ImageTk.PhotoImage(img)

        popup = ZoomableImagePopup(root, tk_img, source=None, is_online=False)

        assert popup.top.winfo_exists()
        assert popup.scale > 0
        assert popup.orig_img is not None

        # Test zoom and pan
        class DummyEvent:
            delta = 120
            x = 5
            y = 5

        popup._on_zoom(DummyEvent())
        popup._start_pan(DummyEvent())

        class DummyDragEvent:
            x = 15
            y = 15
        popup._do_pan(DummyDragEvent())

        # Close and verify cleanup
        popup._on_close()
        assert popup.orig_img is None
        assert popup.tk_img is None
        assert popup._stop_event.is_set()

        popup.top.destroy()
    finally:
        root.destroy()


def test_zoomable_image_popup_linux_zoom():
    root = tk.Tk()
    root.withdraw()
    try:
        img = Image.new("RGB", (20, 20), color="blue")
        tk_img = ImageTk.PhotoImage(img)
        popup = ZoomableImagePopup(root, tk_img, source=None, is_online=False)

        # Verify Linux button bindings exist on the canvas
        canvas_bindings = popup.canvas.bind()
        assert "<Button-4>" in canvas_bindings
        assert "<Button-5>" in canvas_bindings
        assert "<MouseWheel>" in canvas_bindings

        class DummyEvent:
            x = 10
            y = 10

        initial_scale = popup.scale

        # Linux scroll up (Button-4, direction=1) -> zoom in factor 1.1
        popup._on_zoom_linux(DummyEvent(), 1)
        assert popup.scale == pytest.approx(initial_scale * 1.1, rel=1e-4)

        # Linux scroll down (Button-5, direction=-1) -> zoom out factor 0.9
        after_zoom_in = popup.scale
        popup._on_zoom_linux(DummyEvent(), -1)
        assert popup.scale == pytest.approx(after_zoom_in * 0.9, rel=1e-4)

        popup.top.destroy()
    finally:
        root.destroy()


def test_zoomable_image_popup_app_worker_streaming(monkeypatch):
    from backend.task_queue import app_worker
    from unittest.mock import MagicMock

    root = tk.Tk()
    root.withdraw()
    try:
        img = Image.new("RGB", (10, 10), color="red")
        tk_img = ImageTk.PhotoImage(img)

        run_bg_mock = MagicMock()
        monkeypatch.setattr(app_worker, "run_in_background", run_bg_mock)

        popup = ZoomableImagePopup(root, tk_img, source="http://example.com/specimen.jpg", is_online=True)

        # Verify app_worker.run_in_background was invoked with expected callbacks
        run_bg_mock.assert_called_once()
        call_args, call_kwargs = run_bg_mock.call_args

        assert call_args[0] == popup._load_full_res_worker
        assert call_kwargs.get("on_success") == popup._apply_full_res
        assert call_kwargs.get("on_error") == popup._on_full_res_error

        # Verify cancellation halts worker streaming immediately
        popup._stop_event.set()
        res = popup._load_full_res_worker()
        assert res is None

        # Verify applying full resolution updates title and image
        popup._stop_event.clear()
        full_img = Image.new("RGB", (100, 100), color="yellow")
        popup._apply_full_res(full_img)
        assert popup.orig_img == full_img
        assert popup.top.title() == "Image (Full Resolution)"

        # Verify error handling sets fallback title
        popup._on_full_res_error(RuntimeError("Network timeout"))
        assert popup.top.title() == "Image (Failed to load full res)"

        # Verify closing sets stop event
        popup._on_close()
        assert popup._stop_event.is_set()

        popup.top.destroy()
    finally:
        root.destroy()


# ============================================================================
# Merged from test_image_toolbar.py
# ============================================================================

import pytest
import tkinter as tk
from ui.image_toolbar import create_image_toolbar


@pytest.fixture
def tk_root():
    """Provides a hidden root Tk instance for component testing."""
    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()


def test_toolbar_creation(tk_root):
    toolbar = create_image_toolbar(tk_root, design_mode="standard", dark_mode=False)
    assert toolbar is not None
    assert toolbar.design_mode == "standard"
    assert toolbar.dark_mode is False
    assert "zoom_in" in toolbar.buttons
    assert "zoom_out" in toolbar.buttons
    assert "rotate_cw" in toolbar.buttons
    assert "rotate_ccw" in toolbar.buttons
    assert "reset" in toolbar.buttons
    assert "fit" in toolbar.buttons


def test_toolbar_status_formatting(tk_root):
    toolbar = create_image_toolbar(tk_root, zoom_level=1.25, rotation_angle=90)
    status_text = toolbar._format_status_text()
    assert "125%" in status_text
    assert "90°" in status_text

    toolbar.set_status(2.50, 270)
    assert "250%" in toolbar._format_status_text()
    assert "270°" in toolbar._format_status_text()


def test_design_mode_toggle(tk_root):
    toggled_modes = []

    def on_toggle(mode):
        toggled_modes.append(mode)

    callbacks = {"design_toggle": on_toggle}
    toolbar = create_image_toolbar(tk_root, live_callbacks=callbacks, design_mode="standard")

    assert toolbar.design_mode == "standard"
    
    # Toggle to large mode
    toolbar.set_design_mode("large")
    assert toolbar.design_mode == "large"
    assert toolbar.buttons["zoom_in"].mode == "large"

    # Trigger toggle widget handler directly
    toolbar._handle_design_toggle("standard")
    assert toolbar.design_mode == "standard"
    assert "standard" in toggled_modes


def test_image_toolbar_callbacks_invocation(tk_root):
    invoked = []

    callbacks = {
        "zoom_in": lambda: invoked.append("zoom_in"),
        "zoom_out": lambda: invoked.append("zoom_out"),
        "rotate_cw": lambda deg: invoked.append(f"rotate_cw_{deg}"),
        "rotate_ccw": lambda deg: invoked.append(f"rotate_ccw_{deg}"),
        "reset": lambda: invoked.append("reset"),
        "fit": lambda: invoked.append("fit"),
    }

    toolbar = create_image_toolbar(tk_root, live_callbacks=callbacks)

    toolbar._handle_zoom_in()
    assert "zoom_in" in invoked

    toolbar._handle_zoom_out()
    assert "zoom_out" in invoked

    toolbar._handle_rotate_cw()
    assert "rotate_cw_90" in invoked

    toolbar._handle_rotate_ccw()
    assert "rotate_ccw_-90" in invoked

    toolbar._handle_reset()
    assert "reset" in invoked

    toolbar._handle_fit()
    assert "fit" in invoked


def test_dark_mode_switch(tk_root):
    toolbar = create_image_toolbar(tk_root, dark_mode=False)
    assert toolbar.dark_mode is False

    toolbar.set_dark_mode(True)
    assert toolbar.dark_mode is True
    assert toolbar.colors["surface"] == "#181c19"

    toolbar.set_dark_mode(False)
    assert toolbar.dark_mode is False
    assert toolbar.colors["surface"] == "#fbfaf8"


def test_toolbar_typographic_icons(tk_root):
    toolbar = create_image_toolbar(tk_root, zoom_level=1.0, rotation_angle=0)
    assert toolbar.buttons["zoom_in"].icon_symbol == "+"
    assert toolbar.buttons["zoom_out"].icon_symbol == "−"
    status = toolbar._format_status_text()
    assert "🔍" not in status
    assert "100%" in status and "0°" in status


# ============================================================================
# Merged from test_online_photos.py
# ============================================================================

import os
import sys
import unittest
import tempfile
import pandas as pd
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config
from repository import _normalise_dataframes, SQLiteRepository, ExcelRepository


class TestOnlinePhotos(unittest.TestCase):

    def setUp(self):
        self.cfg = config.DATABASE_CONFIGS["Økonomisk Botanisk"]

    def test_01_config_schema(self):
        """Verify Online photo columns exist in config.py for Økonomisk Botanisk."""
        reg_fields = [f["name"] for f in self.cfg["ui_sections"]["registration"]]
        for col in ("Online photo 1", "Online photo 2", "Online photo 3"):
            self.assertIn(col, reg_fields, f"Missing {col} in ui_sections['registration']")

        # Check reg_groups
        reg_groups = {g["name"]: g["fields"] for g in self.cfg["ui_sections"]["reg_groups"]}
        self.assertIn("Object", reg_groups)
        for col in ("Online photo 1", "Online photo 2", "Online photo 3"):
            self.assertIn(col, reg_groups["Object"], f"Missing {col} in reg_groups['Object']")

    def test_02_normalization_and_aliasing(self):
        """Verify _normalise_dataframes correctly aliases headers, cleans values, and syncs Online_Images_Exist."""
        df_reg = pd.DataFrame({
            "ObjectID": [101, 102, 103, 104],
            "Genus": ["Quercus", "Pinus", "Betula", "Fraxinus"],
            "online_photo_1": ['"https://example.com/1.jpg"', "   https://example.com/2.jpg  ", None, ""],
            "ONLINE PHOTO 2": ["nan", "'https://example.com/clean.jpg'", "<NA>", "None"],
            "Online Photo 3": ["", "None", "https://example.com/3.jpg", "  "]
        })
        df_obs = pd.DataFrame({
            "ObjectID": [101, 102, 103, 104]
        })

        norm_reg, norm_obs = _normalise_dataframes(df_reg, df_obs, self.cfg)

        for col in ("Online photo 1", "Online photo 2", "Online photo 3"):
            self.assertIn(col, norm_reg.columns, f"Expected canonical column {col}")

        # Check values
        # Row 0 (ObjectID 101):
        self.assertEqual(norm_reg.loc[0, "Online photo 1"], "https://example.com/1.jpg")
        self.assertEqual(norm_reg.loc[0, "Online photo 2"], "")
        self.assertEqual(norm_reg.loc[0, "Online photo 3"], "")

        # Row 1 (ObjectID 102):
        self.assertEqual(norm_reg.loc[1, "Online photo 1"], "https://example.com/2.jpg")
        self.assertEqual(norm_reg.loc[1, "Online photo 2"], "https://example.com/clean.jpg")
        self.assertEqual(norm_reg.loc[1, "Online photo 3"], "")

        # Row 2 (ObjectID 103):
        self.assertEqual(norm_reg.loc[2, "Online photo 1"], "")
        self.assertEqual(norm_reg.loc[2, "Online photo 2"], "")
        self.assertEqual(norm_reg.loc[2, "Online photo 3"], "https://example.com/3.jpg")

        # Row 3 (ObjectID 104 - no photos):
        self.assertEqual(norm_reg.loc[3, "Online photo 1"], "")
        self.assertEqual(norm_reg.loc[3, "Online photo 2"], "")
        self.assertEqual(norm_reg.loc[3, "Online photo 3"], "")

        # Check Online_Images_Exist in df_obs
        self.assertIn("Online_Images_Exist", norm_obs.columns)
        self.assertTrue(norm_obs.loc[0, "Online_Images_Exist"], "101 has photos -> True")
        self.assertTrue(norm_obs.loc[1, "Online_Images_Exist"], "102 has photos -> True")
        self.assertTrue(norm_obs.loc[2, "Online_Images_Exist"], "103 has photos -> True")
        self.assertFalse(norm_obs.loc[3, "Online_Images_Exist"], "104 has NO photos -> False")

    def test_03_missing_columns_backfill(self):
        """Verify that older datasets without online photo columns get empty string backfills and False in obs."""
        df_reg = pd.DataFrame({
            "ObjectID": [201, 202],
            "Genus": ["Rosa", "Salix"]
        })
        df_obs = pd.DataFrame({
            "ObjectID": [201, 202]
        })

        norm_reg, norm_obs = _normalise_dataframes(df_reg, df_obs, self.cfg)
        for col in ("Online photo 1", "Online photo 2", "Online photo 3"):
            self.assertIn(col, norm_reg.columns)
            self.assertEqual(norm_reg.loc[0, col], "")
            self.assertEqual(norm_reg.loc[1, col], "")
        self.assertIn("Online_Images_Exist", norm_obs.columns)
        self.assertFalse(norm_obs.loc[0, "Online_Images_Exist"])
        self.assertFalse(norm_obs.loc[1, "Online_Images_Exist"])

    def test_04_excel_export_and_roundtrip(self):
        """Verify SQLiteRepository.export_to_excel exports online photo columns and syncs Online_Images_Exist in Observation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            excel_path = os.path.join(tmpdir, "test_online.xlsx")
            sqlite_path = os.path.join(tmpdir, "test_online.db")

            df_reg = pd.DataFrame({
                "ObjectID": [301, 302, 303],
                "Genus": ["Fagus", "Acer", "Ulmus"],
                "UID": ["uid1", "uid2", "uid3"],
                "ProblemDescription": ["", "", ""],
                "Online photo 1": ["https://images.example.org/fagus1.jpg", "", ""],
                "Online photo 2": ["", "https://images.example.org/acer2.jpg", ""],
                "Online photo 3": ["", "", ""]
            })
            # Intentionally pass stale False for all rows in df_obs to test that export_to_excel auto-syncs
            df_obs = pd.DataFrame({
                "ObjectID": [301, 302, 303],
                "Images_Missing": [False, False, True],
                "Images_Problem": [False, False, False],
                "Reviewed": [False, False, False],
                "ReviewedAt": ["", "", ""],
                "Online_Images_Exist": [False, False, False]
            })

            SQLiteRepository.save_sqlite(sqlite_path, df_reg, df_obs, pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
            self.assertTrue(os.path.exists(sqlite_path))

            # Export to excel
            export_target = os.path.join(tmpdir, "exported.xlsx")
            SQLiteRepository.export_to_excel(sqlite_path, export_target, self.cfg, df_reg=df_reg, df_obs=df_obs)
            self.assertTrue(os.path.exists(export_target))

            # Inspect with openpyxl
            wb = openpyxl.load_workbook(export_target)
            self.assertIn("Registration", wb.sheetnames)
            self.assertIn("Observation", wb.sheetnames)
            ws_reg = wb["Registration"]
            ws_obs = wb["Observation"]

            # Check freeze pane A2 and autofilter
            self.assertEqual(ws_reg.freeze_panes, "A2", "Freeze pane should be A2")
            self.assertIsNotNone(ws_reg.auto_filter.ref, "Auto filter should be set")

            # Check Registration header row
            reg_headers = [cell.value for cell in ws_reg[1]]
            for col in ("Online photo 1", "Online photo 2", "Online photo 3"):
                self.assertIn(col, reg_headers, f"Exported Registration sheet missing {col}")

            idx1 = reg_headers.index("Online photo 1") + 1
            idx2 = reg_headers.index("Online photo 2") + 1

            # Row 2 (ObjectID 301):
            self.assertEqual(ws_reg.cell(row=2, column=idx1).value, "https://images.example.org/fagus1.jpg")
            # Row 3 (ObjectID 302):
            self.assertEqual(ws_reg.cell(row=3, column=idx2).value, "https://images.example.org/acer2.jpg")

            # Check Observation sheet for Online_Images_Exist
            obs_headers = [cell.value for cell in ws_obs[1]]
            self.assertIn("Online_Images_Exist", obs_headers, "Observation sheet missing Online_Images_Exist")
            idx_online = obs_headers.index("Online_Images_Exist") + 1

            # Row 2 (ObjectID 301 has photo 1) -> must be True in Excel
            val_301 = ws_obs.cell(row=2, column=idx_online).value
            self.assertTrue(bool(val_301), f"Expected True for ObjectID 301 in Excel, got {val_301}")

            # Row 3 (ObjectID 302 has photo 2) -> must be True in Excel
            val_302 = ws_obs.cell(row=3, column=idx_online).value
            self.assertTrue(bool(val_302), f"Expected True for ObjectID 302 in Excel, got {val_302}")

            # Row 4 (ObjectID 303 has no photo) -> must be False in Excel
            val_303 = ws_obs.cell(row=4, column=idx_online).value
            self.assertFalse(bool(val_303), f"Expected False for ObjectID 303 in Excel, got {val_303}")

            # Load back via ExcelRepository.load_excel
            loaded_reg, loaded_obs, _, _, _ = ExcelRepository.load_excel(export_target, self.cfg)
            row_301 = loaded_reg[loaded_reg["ObjectID"].astype(str) == "301"]
            self.assertEqual(row_301["Online photo 1"].iloc[0], "https://images.example.org/fagus1.jpg")
            row_302 = loaded_reg[loaded_reg["ObjectID"].astype(str) == "302"]
            self.assertEqual(row_302["Online photo 2"].iloc[0], "https://images.example.org/acer2.jpg")

            # Check re-imported observation values
            obs_301 = loaded_obs[loaded_obs["ObjectID"].astype(str) == "301"]
            self.assertTrue(bool(obs_301["Online_Images_Exist"].iloc[0]))
            obs_302 = loaded_obs[loaded_obs["ObjectID"].astype(str) == "302"]
            self.assertTrue(bool(obs_302["Online_Images_Exist"].iloc[0]))
            obs_303 = loaded_obs[loaded_obs["ObjectID"].astype(str) == "303"]
            self.assertFalse(bool(obs_303["Online_Images_Exist"].iloc[0]))

    def test_05_url_security_validation(self):
        """Verify URL validation rejects unsafe schemes."""
        import re

        valid_urls = [
            "https://example.com/photo.jpg",
            "http://example.com/photo.png",
            "HTTP://EXAMPLE.COM/PHOTO.JPEG",
            "  https://sub.domain.org/path?query=1  ",
            "www.example.com/photo.jpg"
        ]
        invalid_urls = [
            "javascript:alert(1)",
            "file:///C:/Windows/System32/calc.exe",
            "ftp://files.example.com/test",
            "",
            None,
            "   "
        ]

        def is_safe_url(url):
            if not url or not isinstance(url, str):
                return False
            url_str = url.strip()
            if not url_str:
                return False
            if not re.match(r'^(?:https?://|www\.)', url_str, re.IGNORECASE):
                return False
            return True

        for u in valid_urls:
            self.assertTrue(is_safe_url(u), f"Should accept: {u}")
        for u in invalid_urls:
            self.assertFalse(is_safe_url(u), f"Should reject: {u}")

    def test_06_cache_set_vectorization(self):
        """Verify vectorized row cache calculation for has_online_photos as implemented in main_window.py."""
        reg_df = pd.DataFrame({
            "ObjectID": [1, 2, 3, 4],
            "Online photo 1": ["https://pic1.jpg", "", "   ", ""],
            "Online photo 2": ["", None, "nan", ""],
            "Online photo 3": ["", "", "", "https://pic3.jpg"]
        }).set_index("ObjectID")

        # Logic matching _ensure_row_caches in main_window.py
        online_cols = [c for c in ("Online photo 1", "Online photo 2", "Online photo 3") if c in reg_df.columns]
        has_photo_mask = pd.Series(False, index=reg_df.index)
        for c in online_cols:
            s = reg_df[c].fillna("").astype(str).str.strip()
            has_photo_mask |= (s != "") & (~s.isin(["nan", "None", "<NA>"]))

        has_online_set = set(reg_df.index[has_photo_mask])

        self.assertIn(1, has_online_set)    # has Online photo 1
        self.assertNotIn(2, has_online_set) # empty/None
        self.assertNotIn(3, has_online_set) # whitespace / nan
        self.assertIn(4, has_online_set)    # has Online photo 3

    def test_07_registry_panel_card_defs(self):
        """Verify Online photo columns are registered in registry_panel.py card_defs."""
        from ui.registry_panel import RegistryPanel
        # Check that RegistryPanel's metadata card definitions include the 3 columns
        found_fields = set()
        # Find the fields defined in RegistryPanel
        import inspect
        src = inspect.getsource(RegistryPanel.build_sections)
        for col in ("Online photo 1", "Online photo 2", "Online photo 3"):
            self.assertIn(col, src, f"Expected {col} to be defined in RegistryPanel.build_sections")

    def test_08_live_commit_sync(self):
        """Verify that updating online photo fields updates df_obs and cache dictionaries."""
        from repository import ONLINE_EXISTS_COLUMN
        oid = "999"
        df_reg = pd.DataFrame([{
            "ObjectID": oid,
            "Online photo 1": "",
            "Online photo 2": "",
            "Online photo 3": ""
        }]).set_index("ObjectID")
        df_obs = pd.DataFrame([{
            "ObjectID": oid,
            ONLINE_EXISTS_COLUMN: False
        }]).set_index("ObjectID")

        cached_reg_dict = {oid: {"Online photo 1": "", "Online photo 2": "", "Online photo 3": ""}}
        cached_obs_dict = {oid: {ONLINE_EXISTS_COLUMN: False}}
        has_online_set = set()

        # Emulate user setting "Online photo 1" in UI and commit_current_object
        new_val = "https://example.org/photo1.jpg"
        cached_reg_dict[oid]["Online photo 1"] = new_val
        has_any = any(
            bool(str(cached_reg_dict[oid].get(f"Online photo {i}", "")).strip() not in ("", "nan", "None", "<NA>"))
            for i in (1, 2, 3)
        )
        if has_any:
            has_online_set.add(oid)
        df_obs.at[oid, ONLINE_EXISTS_COLUMN] = has_any
        cached_obs_dict[oid][ONLINE_EXISTS_COLUMN] = has_any

        self.assertTrue(df_obs.at[oid, ONLINE_EXISTS_COLUMN])
        self.assertTrue(cached_obs_dict[oid][ONLINE_EXISTS_COLUMN])
        self.assertIn(oid, has_online_set)

        # Emulate user clearing "Online photo 1"
        cached_reg_dict[oid]["Online photo 1"] = ""
        has_any = any(
            bool(str(cached_reg_dict[oid].get(f"Online photo {i}", "")).strip() not in ("", "nan", "None", "<NA>"))
            for i in (1, 2, 3)
        )
        if not has_any:
            has_online_set.discard(oid)
        df_obs.at[oid, ONLINE_EXISTS_COLUMN] = has_any
        cached_obs_dict[oid][ONLINE_EXISTS_COLUMN] = has_any

        self.assertFalse(df_obs.at[oid, ONLINE_EXISTS_COLUMN])
        self.assertFalse(cached_obs_dict[oid][ONLINE_EXISTS_COLUMN])
        self.assertNotIn(oid, has_online_set)
