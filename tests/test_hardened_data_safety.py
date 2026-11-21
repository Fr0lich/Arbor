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
