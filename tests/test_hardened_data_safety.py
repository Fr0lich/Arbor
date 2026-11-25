"""
tests/test_hardened_data_safety.py

Headless regression tests for core data-safety & offline-hardening paths:
1. JSON autosave roundtrip preserving UTF-8 Norwegian characters & ObjectID index name.
2. AppState._mutation_seq concurrent-save protection (dirty stays True if edited mid-save).
3. undo_last_bulk_edit() atomic rollback of df_reg and df_obs.
4. Offline GBIF batch_gbif_match() stats_out error reporting & non-error caching.
"""

import os
import threading
import time
import pandas as pd
import pytest

from models import AppState
from ui.autosave_handler import AutosaveMixin
from ui.bulk_edit import undo_last_bulk_edit


class _DummyAutosaveHost(AutosaveMixin):
    def __init__(self, app):
        self.app = app
        self.root = type("R", (), {"after": lambda s, ms, fn: fn()})()
        self.saved_badges = []
        self.loaded = False

    def _autosave_path(self):
        return self.app.excel_path + ".autosave.json"

    def set_status_badge(self, state, text):
        self.saved_badges.append((state, text))

    def _finish_open_excel(self, df_reg, df_obs, df_photo, df_log, df_unvalidated):
        self.app.df_reg = df_reg
        self.app.df_obs = df_obs
        self.app.df_photo = df_photo
        self.app.df_log = df_log
        self.app.df_unvalidated = df_unvalidated
        self.loaded = True


def test_json_autosave_roundtrip_norwegian_utf8_and_objectid_index(tmp_path, monkeypatch):
    """JSON autosave write + recovery preserves Norwegian UTF-8 characters and ObjectID index names."""
    excel_path = tmp_path / "collection.xlsx"
    excel_path.write_bytes(b"placeholder")
    # Ensure original mtime is older than the autosave we're about to write
    old_time = time.time() - 60
    os.utime(excel_path, (old_time, old_time))

    app = AppState()
    app.excel_path = str(excel_path)
    app.df_reg = pd.DataFrame({
        "ObjectID": ["0001", "0002"],
        "Genus": ["Betula", "Juniperus"],
        "Collection Place": ["Oslo, Tøyen — Økonomisk Botanisk", "Ålesund, Ærø & Sør-Trøndelag"],
        "(N) Plant Part": ["Bærkongle", "Frukt"],
    }).set_index("ObjectID", drop=False)
    app.df_obs = pd.DataFrame({
        "ObjectID": ["0001", "0002"],
        "Building": ["Lid's hus", "Økern"],
        "Reviewed": [True, False],
    }).set_index("ObjectID", drop=False)
    app.df_photo = pd.DataFrame(columns=["ObjectID", "Filename"])
    app.df_log = pd.DataFrame(columns=["Timestamp", "User", "ObjectID", "Action", "Details"])
    app.df_unvalidated = pd.DataFrame(columns=["ObjectID", "Field_Name", "Unvalidated_Comment"])

    host = _DummyAutosaveHost(app)
    autosave_path = host._autosave_path()

    done = threading.Event()
    result_box = []

    def _cb(success, err=None):
        result_box.append((success, err))
        done.set()

    host._write_pickle_async(autosave_path, _cb)
    assert done.wait(timeout=5.0), "Async JSON autosave did not finish"
    assert result_box == [(True, None)]
    assert os.path.exists(autosave_path)

    # Clear live frames and recover via _check_autosave_recovery
    app.df_reg = None
    app.df_obs = None
    host.show_banner = lambda *a, **kw: None
    host._restore_autosave(autosave_path, str(excel_path))

    assert app.dirty is True
    assert app.df_reg.index.name == "ObjectID"
    assert app.df_obs.index.name == "ObjectID"
    assert app.df_reg.loc["0001", "Collection Place"] == "Oslo, Tøyen — Økonomisk Botanisk"
    assert app.df_reg.loc["0002", "Collection Place"] == "Ålesund, Ærø & Sør-Trøndelag"
    assert app.df_obs.loc["0002", "Building"] == "Økern"


def test_mutation_seq_concurrent_save_keeps_dirty_true(tmp_path):
    """If an edit arrives while an async save is in-flight, _mutation_seq prevents clearing dirty."""
    from ui.database_ops import DatabaseOpsMixin

    app = AppState()
    app.excel_path = str(tmp_path / "work.xlsx")
    app.output_path = app.excel_path
    app.dirty = True
    seq_before = app._mutation_seq
    assert seq_before >= 1

    # Simulate _write_excel capturing snapshot_seq before background write
    class _SaveHost(DatabaseOpsMixin):
        def __init__(self, a):
            self.app = a
            self.banners = []
            self.status_texts = []
            self._skip_validation_once = True
            self.system_status = type(
                "S", (), {
                    "after": lambda s, ms, fn: None,
                    "config": lambda s, **kw: self.status_texts.append(kw.get("text", "")),
                }
            )()
            self._autosave_removed = False

        def show_banner(self, msg, banner_type="info", **kw):
            self.banners.append((msg, banner_type))

        def _autosave_path(self):
            return str(tmp_path / "nonexistent.autosave.json")

        def _is_tutorial_sandbox_active(self):
            return False

        def commit_current_object(self, **kw):
            pass

        def log_action(self, *a, **kw):
            pass

        def validate_before_save(self, action="SAVE"):
            return True

        def invalidate_search_index(self):
            pass

        def build_search_index(self):
            pass

        def _write_excel_async(self, path, callback=None, **kw):
            # Simulate a concurrent user/mobile edit happening BEFORE callback fires!
            self.app.dirty = True
            if callback:
                callback(True, None)

    host = _SaveHost(app)
    host.save_session("SAVE")

    # Because _mutation_seq incremented mid-save, dirty MUST remain True
    assert app._mutation_seq > seq_before
    assert app.dirty is True

    # Now run a save with NO concurrent edit: dirty MUST clear to False
    host._write_excel_async = lambda path, callback=None, **kw: callback(True, None) if callback else None
    host.save_session("SAVE")
    assert app.dirty is False


def test_undo_last_bulk_edit_restores_reg_and_obs_and_clears_snapshot():
    """undo_last_bulk_edit() restores both df_reg and df_obs, marks dirty, and clears snapshot."""
    app = AppState()
    app.df_reg = pd.DataFrame({
        "ObjectID": ["1", "2"],
        "Collector": ["NEW_VAL", "NEW_VAL"],
    }).set_index("ObjectID", drop=False)
    app.df_obs = pd.DataFrame({
        "ObjectID": ["1", "2"],
        "Building": ["Økern", "Økern"],
        "Reviewed": [True, True],
    }).set_index("ObjectID", drop=False)

    app._last_bulk_edit_snapshot = {
        "oids": ["1", "2"],
        "reg": {
            "1": {"Collector": "N. Moe"},
            "2": {"Collector": "J. Lid"},
        },
        "obs": {
            "1": {"Building": "Lid's hus", "Reviewed": False},
            "2": {"Building": "", "Reviewed": False},
        },
    }

    events = []

    class _MockMainWindow:
        def __init__(self, a):
            self.app = a
            self.current_oid = "1"

        def _invalidate_row_cache(self):
            events.append("invalidate_row_cache")

        def invalidate_search_index(self):
            events.append("invalidate_search_index")

        def refresh_list(self):
            events.append("refresh_list")

        def load_object(self, oid):
            events.append(("load_object", oid))

        def log_action(self, action, **kw):
            events.append(("log_action", action))

        def show_toast(self, msg, level="info"):
            events.append(("toast", level, msg))

    mw = _MockMainWindow(app)
    assert undo_last_bulk_edit(mw) is True

    assert app.df_reg.at["1", "Collector"] == "N. Moe"
    assert app.df_reg.at["2", "Collector"] == "J. Lid"
    assert app.df_obs.at["1", "Building"] == "Lid's hus"
    assert bool(app.df_obs.at["1", "Reviewed"]) is False
    assert app.df_obs.at["2", "Building"] == ""
    assert app.dirty is True
    assert app._last_bulk_edit_snapshot is None
    assert "invalidate_row_cache" in events
    assert "invalidate_search_index" in events

    # Calling a second time with no snapshot returns False cleanly
    assert undo_last_bulk_edit(mw) is False


def test_offline_gbif_batch_match_reports_stats_out_without_caching_errors(monkeypatch):
    """Offline batch_gbif_match populates stats_out error_count cleanly."""
    import backend.gbif as gbif_mod

    monkeypatch.setattr(
        gbif_mod,
        "_query_single_taxon",
        lambda genus, species="", cancel_event=None: {"error": "ConnectionError: offline vault"},
    )

    items = [
        {"oid": "1", "genus": "Betula", "species": "pendula", "family": "Betulaceae", "author": "Roth"},
        {"oid": "2", "genus": "Pinus", "species": "sylvestris", "family": "Pinaceae", "author": "L."},
    ]
    stats = {}
    results = gbif_mod.batch_gbif_match(items, stats_out=stats)
    assert results == []
    assert stats["total_taxa"] == 2
    assert stats["error_count"] == 2


def test_check_gbif_does_not_cache_network_errors(monkeypatch):
    """check_gbif() must never cache transient offline/network error dicts in _check_gbif_cache."""
    import requests
    import backend.gbif as gbif_mod

    gbif_mod._check_gbif_cache.clear()

    class _OfflineSession:
        def get(self, *args, **kwargs):
            raise requests.exceptions.ConnectionError("No internet in vault")

    monkeypatch.setattr(gbif_mod, "_get_session", lambda: _OfflineSession())
    res = gbif_mod.check_gbif("Betula", "pendula")
    assert "error" in res
    assert ("betula", "pendula") not in gbif_mod._check_gbif_cache


# ============================================================================
# Merged from test_logging_diagnostics.py
# ============================================================================

import os
import sys
import pytest
import utils


def test_debug_log_and_debug_error(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "get_log_level", lambda: "DEBUG")
    # Verify session log path is created
    log_path = utils.get_session_log_path()
    assert log_path is not None
    assert os.path.exists(os.path.dirname(log_path))

    # Test debug_log
    utils.debug_log("INFO", "Diagnostic test message", "extra detail")
    
    # Test debug_error without exception
    initial_has_errors = utils.session_had_errors()
    utils.debug_error("Non-fatal context error", "extra detail", is_crash=False)
    assert utils.session_had_errors() is True

    # Test debug_error with exception context
    try:
        raise ValueError("Simulated diagnostic exception")
    except ValueError:
        utils.debug_error("Caught diagnostic exception", "extra info", is_crash=True)

    # Check file exists and contains message
    assert os.path.exists(log_path)
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Diagnostic test message" in content
    assert "Non-fatal context error" in content
    assert "Caught diagnostic exception" in content
    assert "ValueError: Simulated diagnostic exception" in content


def test_legacy_stubs_compatibility():
    # Verify legacy queue stubs do not crash callers
    assert hasattr(utils, "_ensure_flush_thread")
    utils._ensure_flush_thread()

    assert hasattr(utils, "_flush_loop")
    utils._flush_loop()

    assert hasattr(utils, "_flush_log_queue")
    utils._flush_log_queue()

    assert hasattr(utils, "_log_queue")


# ============================================================================
# Merged from test_caching.py
# ============================================================================

import cachetools
import pytest
from unittest.mock import MagicMock
from ui.historical_suggestions import HistoricalSuggestionsMixin


class DummyHost(HistoricalSuggestionsMixin):
    def __init__(self):
        self._history_lock = None
        self._history_cache = cachetools.LRUCache(maxsize=3)
        self.app = MagicMock()
        self.app.historical_dbs = []


def test_lru_cache_eviction_bounds():
    cache = cachetools.LRUCache(maxsize=3)
    cache[("1", False)] = {"Field": "Val1"}
    cache[("2", False)] = {"Field": "Val2"}
    cache[("3", False)] = {"Field": "Val3"}
    assert len(cache) == 3

    # Adding 4th element should evict oldest ("1", False)
    cache[("4", False)] = {"Field": "Val4"}
    assert len(cache) == 3
    assert ("1", False) not in cache
    assert ("4", False) in cache


def test_invalidate_history_cache_removes_oid_variants():
    host = DummyHost()
    host._history_cache = cachetools.LRUCache(maxsize=10)
    host._history_cache[("101", True)] = {"data": 1}
    host._history_cache[("101", False)] = {"data": 2}
    host._history_cache[(101, True)] = {"data": 3}
    host._history_cache[("202", False)] = {"data": 4}

    assert len(host._history_cache) == 4

    # Invalidate oid 101
    host.invalidate_history_cache("101")
    assert ("101", True) not in host._history_cache
    assert ("101", False) not in host._history_cache
    assert (101, True) not in host._history_cache
    assert ("202", False) in host._history_cache
    assert len(host._history_cache) == 1

    # Invalidate all
    host.invalidate_history_cache(None)
    assert len(host._history_cache) == 0


def test_finish_load_books_cache_initialization():
    from unittest.mock import patch
    host = DummyHost()
    host.root = MagicMock()
    host.app = MagicMock()
    host.system_status = MagicMock()
    host.image_scan_progress = MagicMock()
    host._hide_progress = MagicMock()
    host._history_cache = None

    with patch("tkinter.messagebox.showwarning"):
        host._finish_load_books([])

    assert host._history_cache is not None
    assert isinstance(host._history_cache, cachetools.LRUCache)


# ============================================================================
# Merged from test_demo_dataset.py
# ============================================================================

import os
import pytest
from repository import ExcelRepository
import config

def test_demo_collection_exists_and_loads():
    demo_path = os.path.join("data", "demo_collection.xlsx")
    assert os.path.exists(demo_path), "demo_collection.xlsx should exist in data/"

    cfg = config.DATABASE_CONFIGS.get("Økonomisk Botanisk")
    assert cfg is not None, "Økonomisk Botanisk config should exist"

    df_reg, df_obs, df_photo, df_log, df_unval = ExcelRepository.load_excel(demo_path, cfg)

    assert len(df_reg) == 220, f"Expected 220 specimens, got {len(df_reg)}"
    assert len(df_obs) == 220, f"Expected 220 observation rows, got {len(df_obs)}"
    assert "ObjectID" in df_reg.columns
    assert "ObjectID" in df_obs.columns
    assert "PlantPart_Problem" in df_obs.columns
    assert len(df_log) > 0, "Log rows should be preserved"
    # Check that ObjectIDs match
    assert set(df_reg["ObjectID"]) == set(df_obs["ObjectID"]), "ObjectIDs must match across Registration and Observation"


def test_frozen_demo_path_prefers_writable_exe_dir(tmp_path, monkeypatch):
    import sys
    from ui.dialogs import StartupDialog

    meipass_dir = tmp_path / "meipass"
    exe_dir = tmp_path / "dist_install"
    (meipass_dir / "data").mkdir(parents=True)
    exe_dir.mkdir(parents=True)

    bundled_demo = meipass_dir / "data" / "demo_collection.xlsx"
    bundled_demo.write_bytes(b"mock-demo-xlsx")

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(meipass_dir), raising=False)
    monkeypatch.setattr(sys, "executable", str(exe_dir / "Arbor.exe"))

    dlg = StartupDialog.__new__(StartupDialog)
    resolved = dlg._resolve_writable_demo_path()

    expected = str(exe_dir / "data" / "demo_collection.xlsx")
    assert resolved == expected
    assert os.path.exists(expected)
    assert open(expected, "rb").read() == b"mock-demo-xlsx"


# ── Release prep: writable user-data folder never lands in a read-only exe dir ──
def test_user_data_dir_uses_exe_folder_when_writable(tmp_path, monkeypatch):
    import sys
    import utils
    exe_dir = tmp_path / "portable"
    exe_dir.mkdir()
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(exe_dir / "Arbor.exe"))
    monkeypatch.setattr(utils, "_USER_DATA_DIR", None)
    assert utils.get_user_data_dir() == str(exe_dir)


def test_user_data_dir_falls_back_to_localappdata_when_exe_folder_read_only(tmp_path, monkeypatch):
    import sys
    import utils
    exe_dir = tmp_path / "Program Files" / "Arbor"
    local = tmp_path / "LocalAppData"
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(exe_dir / "Arbor.exe"))
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setattr(utils, "_USER_DATA_DIR", None)
    monkeypatch.setattr(utils, "_dir_is_writable", lambda p: False)
    result = utils.get_user_data_dir()
    assert result == os.path.join(str(local), "Arbor")
    assert os.path.isdir(result)
