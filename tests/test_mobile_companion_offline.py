import pytest
from datetime import datetime, timedelta
import pandas as pd
from backend.mobile_server import MobileServer
from models import AppState

@pytest.fixture
def mock_app_state():
    app = AppState()
    app.config = {
        "ui_sections": {
            "registration": [{"name": "Genus"}, {"name": "Species"}],
            "location": [{"name": "Cabinet"}],
            "problems": [{"name": "MissingLabel"}]
        }
    }
    app.df_reg = pd.DataFrame({
        "Genus": ["Pinus", "Betula"],
        "Species": ["sylvestris", "pendula"],
        "Cabinet": ["Cab 1", "Cab 2"]
    }, index=pd.Index([1001, 1002], name="ObjectID"))

    app.df_obs = pd.DataFrame({
        "Reviewed": [True, False],
        "Cabinet": ["Cab 1", "Cab 2"]
    }, index=pd.Index([1001, 1002], name="ObjectID"))

    # Pre-populate undo stack with a recent change for 1001
    now = datetime.now()
    app.undo_stacks = {
        "1001": [
            {
                "oid": "1001",
                "timestamp": now.isoformat()
            }
        ]
    }
    return app

def test_offline_mutation_queue_batch_update_success(mock_app_state):
    server = MobileServer(mock_app_state, port=5099)
    client = server.flask_app.test_client()
    headers = {"X-Session-Token": server.session_token}

    now = datetime.now()
    # A valid queued update (newer than any stack changes, or for an object without stack)
    future_time = (now + timedelta(minutes=5)).isoformat()

    payload = {
        "updates": [
            {
                "id": "1002",
                "reviewed": True,
                "timestamp": future_time,
                "observation": {"Cabinet": "Cab 88"}
            }
        ]
    }

    res = client.post('/api/batch_update', headers=headers, json=payload)
    assert res.status_code == 200
    assert res.json["updated_count"] == 1
    assert mock_app_state.df_obs.at[1002, "Cabinet"] == "Cab 88"

def test_offline_mutation_queue_conflict_rejection(mock_app_state):
    server = MobileServer(mock_app_state, port=5098)
    client = server.flask_app.test_client()
    headers = {"X-Session-Token": server.session_token}

    now = datetime.now()
    # An older queued update for 1001 (older than the stack change)
    past_time = (now - timedelta(minutes=5)).isoformat()

    payload = {
        "updates": [
            {
                "id": "1001",
                "reviewed": False,
                "timestamp": past_time,
                "observation": {"Cabinet": "Cab 99"} # Should be rejected
            }
        ]
    }

    res = client.post('/api/batch_update', headers=headers, json=payload)
    assert res.status_code == 200
    assert res.json.get("updated_count") == 0
    # Data should not be changed
    assert mock_app_state.df_obs.at[1001, "Cabinet"] == "Cab 1"


def test_v2_offline_indexeddb_mutation_queue_and_presence_parity(mock_app_state):
    """Test that V2 template includes IndexedDB offline queue methods and server triggers presence callback."""
    observed_presence = []
    server = MobileServer(mock_app_state, port=5097)
    server.on_presence_callback = lambda oid: observed_presence.append(oid)

    client = server.flask_app.test_client()
    headers = {"X-Session-Token": server.session_token}

    # 1. Test presence callback triggering on /api/presence
    p_res = client.post('/api/presence', headers=headers, json={"oid": "1002"})
    assert p_res.status_code == 200
    assert "1002" in observed_presence

    # 2. Test V2 template contains IndexedDB queue routines
    v2_res = client.get('/v2?token=' + server.session_token)
    assert v2_res.status_code == 200
    html = v2_res.get_data(as_text=True)

    assert 'initIndexedDB()' in html
    assert 'queued_mutations' in html
    assert 'queueMutation(payload)' in html
    assert 'flushQueuedMutations()' in html
    assert 'forceSaveImmediate()' in html
    assert 'id="offlineBannerText"' in html


def test_v2_settings_icedig_reference_table(mock_app_state):
    """Test that V2 settings modal contains ICEDIG reference table."""
    server = MobileServer(mock_app_state, port=5096)
    client = server.flask_app.test_client()
    v2_res = client.get('/v2?token=' + server.session_token)
    assert v2_res.status_code == 200
    html = v2_res.get_data(as_text=True)

    assert 'ICEDIG Missing Data Standards' in html
    assert 'unknown:missing' in html
    assert 'unknown:indecipherable' in html
    assert 'unknown:undigitized' in html
    assert 'withheld' in html


def test_v2_accidental_unload_and_pagehide_guards(mock_app_state):
    """Test that V2 template includes beforeunload, pagehide, and visibilitychange guards."""
    server = MobileServer(mock_app_state, port=5097)
    client = server.flask_app.test_client()
    v2_res = client.get('/v2?token=' + server.session_token)
    assert v2_res.status_code == 200
    html = v2_res.get_data(as_text=True)

    assert "window.addEventListener('beforeunload'" in html
    assert "window.addEventListener('pagehide'" in html
    assert "document.addEventListener('visibilitychange'" in html
    assert "forceSaveImmediate()" in html


def test_v2_adjustable_tactile_haptic_feedback(mock_app_state):
    """Test that V2 and V1 settings modal contain adjustable haptic feedback controls."""
    server = MobileServer(mock_app_state, port=5098)
    client = server.flask_app.test_client()
    
    # Check V2
    v2_res = client.get('/v2?token=' + server.session_token)
    assert v2_res.status_code == 200
    html_v2 = v2_res.get_data(as_text=True)

    assert 'id="settingEnableHaptics"' in html_v2
    assert 'id="btnHapticLight"' in html_v2
    assert 'id="btnHapticMedium"' in html_v2
    assert 'id="btnHapticStrong"' in html_v2
    assert 'testHapticFeedback()' in html_v2
    assert 'id="hapticsUnsupportedNote"' in html_v2
    assert 'HAPTIC_PROFILES' in html_v2
    assert 'triggerHaptic(' in html_v2

    # Check V1 Parity
    v1_res = client.get('/?token=' + server.session_token)
    assert v1_res.status_code == 200
    html_v1 = v1_res.get_data(as_text=True)

    assert 'id="settingEnableHaptics"' in html_v1
    assert 'id="btnHapticLight"' in html_v1
    assert 'id="btnHapticMedium"' in html_v1
    assert 'id="btnHapticStrong"' in html_v1
    assert 'testHapticFeedback()' in html_v1
    assert 'id="hapticsUnsupportedNote"' in html_v1


def test_mobile_autosave_setting_and_panel_toggle(mock_app_state, monkeypatch):
    """Test mobile_autosave_on_stop preference and MobilePanel toggle behavior."""
    import config
    from ui.mobile_panel import MobilePanel
    import tkinter as tk

    fake_prefs = {"mobile_autosave_on_stop": False}
    monkeypatch.setattr(config, "load_prefs", lambda: fake_prefs)
    monkeypatch.setattr(config, "save_prefs", lambda p: fake_prefs.update(p))

    root = tk.Tk()
    try:
        panel = MobilePanel(
            parent=root,
            app_state=mock_app_state,
            root_tk=root,
            port=5099
        )
        assert panel.auto_save_var.get() is False
        assert "OFF" in panel.btn_autosave_toggle.cget("text")

        # Toggle to ON
        panel._toggle_auto_save()
        assert panel.auto_save_var.get() is True
        assert fake_prefs["mobile_autosave_on_stop"] is True
        assert "ON" in panel.btn_autosave_toggle.cget("text")
        assert "ON" in panel.btn_active_autosave_toggle.cget("text")

        # Toggle back to OFF
        panel._toggle_auto_save()
        assert panel.auto_save_var.get() is False
        assert fake_prefs["mobile_autosave_on_stop"] is False
        assert "OFF" in panel.btn_autosave_toggle.cget("text")
    finally:
        root.destroy()


def test_mobile_dialog_end_session_autosave_and_prompt(mock_app_state, monkeypatch):
    """Test MobileDialog._end_session auto-save vs confirmation prompt branches."""
    import config
    from ui.mobile_dialog import MobileDialog
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    try:
        class DummyApp:
            def __init__(self):
                self.output_path = "dummy_collection.xlsx"

        class DummyParentUI:
            def __init__(self, root):
                self.root = root
                self.app = DummyApp()
                self.saved_actions = []

            def save_session(self, action, on_complete=None):
                self.saved_actions.append(action)

            def load_object(self, oid):
                pass

        parent_ui = DummyParentUI(root)

        # Case 1: dirty is False -> no save, no prompt
        mock_app_state.dirty = False
        dlg = MobileDialog(parent_ui, root, mock_app_state)
        dlg._end_session()
        assert len(parent_ui.saved_actions) == 0

        # Case 2: dirty is True, auto-save is ON -> silent save triggered
        mock_app_state.dirty = True
        monkeypatch.setattr(config, "load_prefs", lambda: {"mobile_autosave_on_stop": True})
        dlg2 = MobileDialog(parent_ui, root, mock_app_state)
        dlg2.panel.auto_save_var.set(True)
        dlg2._end_session()
        assert "MOBILE_SESSION_END" in parent_ui.saved_actions

        # Case 3: dirty is True, auto-save is OFF -> prompt shown (user says Yes)
        parent_ui.saved_actions.clear()
        mock_app_state.dirty = True
        monkeypatch.setattr(config, "load_prefs", lambda: {"mobile_autosave_on_stop": False})
        monkeypatch.setattr(messagebox, "askyesno", lambda *args, **kwargs: True)
        dlg3 = MobileDialog(parent_ui, root, mock_app_state)
        dlg3.panel.auto_save_var.set(False)
        dlg3._end_session()
        assert "MOBILE_SESSION_END" in parent_ui.saved_actions

        # Case 4: dirty is True, auto-save is OFF -> prompt shown (user says No)
        parent_ui.saved_actions.clear()
        mock_app_state.dirty = True
        monkeypatch.setattr(messagebox, "askyesno", lambda *args, **kwargs: False)
        dlg4 = MobileDialog(parent_ui, root, mock_app_state)
        dlg4.panel.auto_save_var.set(False)
        dlg4._end_session()
        assert len(parent_ui.saved_actions) == 0
    finally:
        root.destroy()


def test_mobile_panel_live_pin_toggle_and_public_tunnel_warning(mock_app_state, monkeypatch):
    """Verify MobilePanel PIN toggle updates prefs, live server, and warns when Public Tunnel is open without PIN."""
    import tkinter as tk
    import config
    from ui.mobile_panel import MobilePanel

    fake_prefs = {"require_mobile_pin": True, "mobile_autosave_on_stop": False}
    monkeypatch.setattr(config, "load_prefs", lambda: fake_prefs)
    monkeypatch.setattr(config, "save_prefs", lambda p: fake_prefs.update(p))

    try:
        root = tk.Tk()
        root.withdraw()
    except Exception:
        pytest.skip("Tkinter display not available")

    try:
        pin_updates = []
        fake_server = type("Srv", (), {
            "pin": "9876",
            "update_pin_requirement": lambda s, val: pin_updates.append(val),
        })()
        panel = MobilePanel(parent=root, app_state=mock_app_state, root_tk=root, reuse_server=fake_server)
        assert "ON" in panel.btn_pin_toggle.cget("text")

        # Toggle PIN OFF while Public Tunnel is default -> amber warning shown & live server updated
        panel._toggle_pin_required()
        assert fake_prefs["require_mobile_pin"] is False
        assert pin_updates == [False]
        assert "OFF" in panel.btn_pin_toggle.cget("text")
        assert panel.pin_var.get() == "OFF (Open)"
        assert "Public tunnel" in panel.lbl_pin_tip.cget("text")

        # Toggle PIN back ON -> warning clears & 4-digit PIN restored
        panel._toggle_pin_required()
        assert fake_prefs["require_mobile_pin"] is True
        assert pin_updates == [False, True]
        assert panel.pin_var.get() == "9876"

        # Collapsible Advanced Options starts collapsed and expands on click
        assert panel._adv_expanded is False
        assert panel.advanced_setup_frame.winfo_manager() == ""
        panel._toggle_advanced_setup()
        assert panel._adv_expanded is True
        assert panel.advanced_setup_frame.winfo_manager() == "pack"
    finally:
        root.destroy()


# ============================================================================
# Merged from test_mobile_schemas.py
# ============================================================================

import pytest
from marshmallow import ValidationError
from backend.mobile_schemas import (
    ObjectUpdateSchema,
    BatchUpdateSchema,
    PresenceSchema,
    sanitize_string_field,
)


def test_sanitize_string_field():
    assert sanitize_string_field("Normal text") == "Normal text"
    assert sanitize_string_field("=cmd|'/C calc'!A0") == "'=cmd|'/C calc'!A0"
    assert sanitize_string_field("+SUM(A1:A10)") == "'+SUM(A1:A10)"
    assert sanitize_string_field("-123") == "'-123"
    assert sanitize_string_field("@SUM") == "'@SUM"
    assert sanitize_string_field(None) == ""


def test_object_update_schema_id_normalization():
    schema = ObjectUpdateSchema()

    # Using 'id'
    res1 = schema.load({"id": " 42 ", "observation": {"Genus": "Pinus"}})
    assert res1["oid"] == "42"
    assert res1["observation"]["Genus"] == "Pinus"

    # Using 'oid'
    res2 = schema.load({"oid": "100", "updates": {"Notes": "Test note"}})
    assert res2["oid"] == "100"
    assert res2["observation"]["Notes"] == "Test note"

    # Formula injection in observation values is sanitized
    res3 = schema.load({"id": "1", "observation": {"Species": "=2+2"}})
    assert res3["observation"]["Species"] == "'=2+2"


def test_batch_update_schema():
    schema = BatchUpdateSchema()

    valid_payload = {
        "updates": [
            {"id": "1", "observation": {"Genus": "Pinus"}},
            {"oid": "2", "reviewed": True},
        ]
    }
    loaded = schema.load(valid_payload)
    assert len(loaded["updates"]) == 2
    assert loaded["updates"][0]["oid"] == "1"
    assert loaded["updates"][1]["oid"] == "2"


def test_presence_schema():
    schema = PresenceSchema()
    assert schema.load({"oid": "  55  "})["oid"] == "55"
    assert schema.load({"id": "99"})["oid"] == "99"


# ============================================================================
# Merged from test_mobile_undo_log_safety.py
# ============================================================================

import pytest
import pandas as pd
from datetime import datetime
from models import AppState
from backend.mobile_server import MobileServer, _execute_record_update
import config


def test_mobile_undo_protects_prior_session_and_disk_logs():
    app = AppState()
    app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
    app.df_reg = pd.DataFrame([{"ObjectID": "1001", "Genus": "Acer", "Species": "rubrum"}]).set_index("ObjectID")
    app.df_obs = pd.DataFrame([{"ObjectID": "1001", "Reviewed": False, "Location": "Room 101"}]).set_index("ObjectID")
    app.df_photo = pd.DataFrame(columns=["ObjectID", "ImagePath"]).set_index("ObjectID")
    
    # Pre-populate historical log records from previous sessions
    app._log_records = [
        {
            "Timestamp": "2026-09-01T09:00:00",
            "Action": "EDIT",
            "Reviewed": "No",
            "ObjectID": "1001",
            "ChangedFields": "Species",
            "ChangedValues": 'Species: "saccharum" -> "rubrum"',
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "",
            "LocationChangedValues": "",
            "User": "prior_desktop_user",
            "SourceFile": "db.xlsx",
            "OutputFile": "db.xlsx"
        },
        {
            "Timestamp": "2026-09-02T14:00:00",
            "Action": "MOBILE_EDIT",
            "Reviewed": "No",
            "ObjectID": "1001",
            "ChangedFields": "Location",
            "ChangedValues": 'Location: "Room 100" -> "Room 101"',
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "Location",
            "LocationChangedValues": "Room 101",
            "User": "Mobile-Companion",
            "SourceFile": "db.xlsx",
            "OutputFile": "db.xlsx",
            "_session_id": "old_session_123"
        }
    ]
    app.df_log = pd.DataFrame(app._log_records)

    server = MobileServer(app, port=5120)
    client = server.flask_app.test_client()

    # Authenticate mobile client
    with client.session_transaction() as sess:
        sess['authenticated'] = True

    # 1. Perform mobile edit in current session
    resp = client.post('/api/batch_update', json={
        "updates": [{
            "id": "1001",
            "registration": {"Species": "platanoides"},
            "observation": {},
            "reviewed": True
        }]
    })
    assert resp.status_code == 200
    assert len(app._log_records) == 3
    assert app._log_records[-1]["Action"] == "MOBILE_EDIT"
    assert app._log_records[-1]["_session_id"] == server.session_id

    # 2. Perform Undo via mobile API
    undo_resp = client.post('/api/undo', json={"oid": "1001"})
    assert undo_resp.status_code == 200

    # 3. Assert current session log was popped, but the 2 prior session records remain completely intact
    assert len(app._log_records) == 2
    assert app._log_records[0]["User"] == "prior_desktop_user"
    assert app._log_records[1]["_session_id"] == "old_session_123"
    assert app._log_records[1]["ChangedValues"] == 'Location: "Room 100" -> "Room 101"'

    # 4. Perform a second Undo when there are no more current session edits for this oid
    undo_resp2 = client.post('/api/undo', json={"oid": "1001"})
    # Even if undo stack is exhausted or has past snapshots, prior session logs must NOT be popped!
    assert len(app._log_records) == 2


def test_mobile_zero_mutation_guard():
    app = AppState()
    app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
    app.df_reg = pd.DataFrame([{"ObjectID": "2001", "Genus": "Betula", "Species": "pendula"}]).set_index("ObjectID")
    app.df_obs = pd.DataFrame([{"ObjectID": "2001", "Reviewed": True}]).set_index("ObjectID")
    app._log_records = []
    app.df_log = pd.DataFrame()
    app.dirty = False

    with app.df_lock:
        summary, err = _execute_record_update(
            app_state=app,
            oid="2001",
            reg_updates={"Genus": "Betula", "Species": "pendula"},
            obs_updates={"Reviewed": True},
            reviewed=True
        )

    assert err is None
    assert len(app._log_records) == 0
    assert app.df_log.empty


# ============================================================================
# Merged from test_mobile_concurrency_features.py
# ============================================================================

import pytest
import pandas as pd
import json
import time
from unittest.mock import patch
from models import AppState
from backend.mobile_server import MobileServer
import config


@pytest.fixture
def concurrency_mock_app_state(tmp_path):
    app = AppState()
    app.config_name = "Botanical Herbarium"
    app.config = {
        "sheets": {"reg": "Registration", "obs": "Observation", "photo": "Photo", "log": "Log"},
        "ui_sections": {
            "registration": [
                {"name": "Genus"}, {"name": "Species"}, {"name": "Family"}, {"name": "Author"},
                {"name": "UID"}, {"name": "ProblemDescription"}
            ],
            "problems": [{"name": "MissingLabel", "label": "Missing Label", "maps_to": "ProblemDescription"}],
            "reg_groups": [{"name": "Taxonomy", "fields": ["Genus", "Species", "Family", "Author"]}],
            "location": [{"name": "Building"}, {"name": "Room"}, {"name": "Cabinet"}, {"name": "Shelf"}]
        },
        "image_url_pattern": "https://www.unimus.no/photos/image/jpeg/O-V-OE-{id}.jpg"
    }

    reg_data = {
        "ObjectID": ["1024", "1025", "1026"],
        "Genus": ["Pinus", "Betula", "Quercus"],
        "Species": ["sylvestris", "pendula", "robur"],
        "Family": ["Pinaceae", "Betulaceae", "Fagaceae"],
        "Author": ["L.", "Roth", "L."],
        "UID": ["u1024", "u1025", "u1026"],
        "ProblemDescription": ["", "", ""]
    }
    df_reg = pd.DataFrame(reg_data).set_index("ObjectID")

    obs_data = {
        "ObjectID": ["1024", "1025", "1026"],
        "Room": ["Room 304", "Room 304", "Room 305"],
        "Cabinet": ["C-12", "C-12", "C-15"],
        "Shelf": ["Shelf 3", "Shelf 4", "Shelf 1"],
        "Notes": ["Initial inspection note", "", ""],
        "Reviewed": [False, True, False],
        "ReviewedAt": ["", "2026-08-20T10:00:00", ""],
        "MissingLabel": [False, False, True]
    }
    df_obs = pd.DataFrame(obs_data).set_index("ObjectID")
    df_photo = pd.DataFrame({"ObjectID": ["1024", "1025", "1026"], "Images": ["1024.jpg", "", ""]}).set_index("ObjectID")
    df_log = pd.DataFrame()

    app.df_reg = df_reg
    app.df_obs = df_obs
    app.df_photo = df_photo
    app.df_log = df_log
    app.excel_path = str(tmp_path / "test_db.xlsx")
    app.output_path = app.excel_path
    app._log_records = []
    app.dirty = False

    return app


def test_cloudflare_ip_proxy_and_rate_limiting(concurrency_mock_app_state):
    """Test CF-Connecting-IP / X-Forwarded-For headers and per-IP rate limiting lockout."""
    server = MobileServer(concurrency_mock_app_state, port=5099)
    client = server.flask_app.test_client()

    ip_a = "198.51.100.1"
    ip_b = "198.51.100.2"

    # 1. Test IP extraction via CF-Connecting-IP
    with server.flask_app.test_request_context('/', headers={'CF-Connecting-IP': ip_a}):
        assert server._get_client_ip() == ip_a

    # Test IP extraction via X-Forwarded-For (with proxies in chain)
    with server.flask_app.test_request_context('/', headers={'X-Forwarded-For': f"{ip_b}, 10.0.0.1, 127.0.0.1"}):
        assert server._get_client_ip() == ip_b

    # 2. Trigger 5 failed attempts from IP A
    for _ in range(5):
        res = client.post('/api/auth', json={"pin": "WRONG_PIN"}, headers={'CF-Connecting-IP': ip_a})
        assert res.status_code == 401

    # IP A should now be rate-limited (429)
    res_a = client.post('/api/auth', json={"pin": server.pin}, headers={'CF-Connecting-IP': ip_a})
    assert res_a.status_code == 429
    assert "Too many failed attempts" in res_a.json.get("error", "")

    # IP B (different worker) should NOT be rate limited and should authenticate cleanly
    res_b = client.post('/api/auth', json={"pin": server.pin}, headers={'CF-Connecting-IP': ip_b})
    assert res_b.status_code == 200
    assert "token" in res_b.json


def test_separate_client_sessions_and_worker_tracking(concurrency_mock_app_state):
    """Test distinct worker session creation and audit log session_id tracking."""
    server = MobileServer(concurrency_mock_app_state, port=5099)
    client = server.flask_app.test_client()

    # Authenticate Worker 1
    auth1 = client.post('/api/auth', json={"pin": server.pin}, headers={'CF-Connecting-IP': '10.0.1.1'})
    assert auth1.status_code == 200
    token1 = auth1.json["token"]
    session1 = server._get_session_by_token(token1)
    assert session1 is not None
    sid1 = session1["session_id"]

    # Authenticate Worker 2
    auth2 = client.post('/api/auth', json={"pin": server.pin}, headers={'CF-Connecting-IP': '10.0.1.2'})
    assert auth2.status_code == 200
    token2 = auth2.json["token"]
    session2 = server._get_session_by_token(token2)
    assert session2 is not None
    sid2 = session2["session_id"]

    # Must be separate sessions
    assert token1 != token2
    assert sid1 != sid2

    # Worker 1 updates Object 1024
    res_w1 = client.post('/api/update',
                         json={"id": "1024", "registration": {"Genus": "Pinus", "Species": "mugo"}},
                         headers={"X-Session-Token": token1})
    assert res_w1.status_code == 200

    # Worker 2 updates Object 1025
    res_w2 = client.post('/api/update',
                         json={"id": "1025", "registration": {"Genus": "Betula", "Species": "nana"}},
                         headers={"X-Session-Token": token2})
    assert res_w2.status_code == 200

    # Verify audit log records contain correct _session_id attribution
    log_1024 = [r for r in concurrency_mock_app_state._log_records if r.get("ObjectID") == "1024"]
    assert len(log_1024) > 0
    assert log_1024[-1]["User"] == "Mobile-Companion"
    assert log_1024[-1].get("_session_id") == sid1

    log_1025 = [r for r in concurrency_mock_app_state._log_records if r.get("ObjectID") == "1025"]
    assert len(log_1025) > 0
    assert log_1025[-1]["User"] == "Mobile-Companion"
    assert log_1025[-1].get("_session_id") == sid2


def test_session_isolated_undo(concurrency_mock_app_state):
    """Test that undo operations are scoped to the requesting worker's session."""
    server = MobileServer(concurrency_mock_app_state, port=5099)
    client = server.flask_app.test_client()

    auth1 = client.post('/api/auth', json={"pin": server.pin})
    token1 = auth1.json["token"]
    sid1 = server._get_session_by_token(token1)["session_id"]

    auth2 = client.post('/api/auth', json={"pin": server.pin})
    token2 = auth2.json["token"]
    sid2 = server._get_session_by_token(token2)["session_id"]

    # Worker 1 modifies Genus of 1024 to 'Pinus-W1'
    client.post('/api/update',
                json={"id": "1024", "registration": {"Genus": "Pinus-W1", "Species": "sylvestris"}},
                headers={"X-Session-Token": token1})

    # Worker 2 modifies Species of 1024 to 'sylvestris-W2'
    client.post('/api/update',
                json={"id": "1024", "registration": {"Genus": "Pinus-W1", "Species": "sylvestris-W2"}},
                headers={"X-Session-Token": token2})

    assert concurrency_mock_app_state.df_reg.loc["1024", "Genus"] == "Pinus-W1"
    assert concurrency_mock_app_state.df_reg.loc["1024", "Species"] == "sylvestris-W2"

    # Worker 2 triggers undo
    undo_res2 = client.post('/api/undo', json={"id": "1024"}, headers={"X-Session-Token": token2})
    assert undo_res2.status_code == 200
    assert undo_res2.json["success"] is True

    # After Worker 2 undid their edit:
    # Species should revert back to 'sylvestris', but Worker 1's Genus edit ('Pinus-W1') should remain!
    assert concurrency_mock_app_state.df_reg.loc["1024", "Species"] == "sylvestris"
    assert concurrency_mock_app_state.df_reg.loc["1024", "Genus"] == "Pinus-W1"

    # Worker 1 triggers undo
    undo_res1 = client.post('/api/undo', json={"id": "1024"}, headers={"X-Session-Token": token1})
    assert undo_res1.status_code == 200
    assert undo_res1.json["success"] is True

    # Now Genus should also be restored to initial 'Pinus'
    assert concurrency_mock_app_state.df_reg.loc["1024", "Genus"] == "Pinus"


def test_pin_requirement_toggle(concurrency_mock_app_state):
    """Test that require_mobile_pin=False bypasses PIN check and auto-provisions sessions."""
    server = MobileServer(concurrency_mock_app_state, port=5099)
    client = server.flask_app.test_client()

    # 1. When PIN required (default):
    with patch("config.load_prefs", return_value={"require_mobile_pin": True}):
        server.update_pin_requirement(True)
        assert server.is_pin_required() is True
        res_fail = client.post('/api/auth', json={"pin": "WRONG_PIN"})
        assert res_fail.status_code == 401

    # 2. When PIN requirement is disabled:
    with patch("config.load_prefs", return_value={"require_mobile_pin": False}):
        server.update_pin_requirement(False)
        assert server.is_pin_required() is False

        # POST /api/auth without valid PIN succeeds
        res_auth = client.post('/api/auth', json={"pin": ""})
        assert res_auth.status_code == 200
        assert "token" in res_auth.json
        assert res_auth.json.get("success") is True

        # GET /login redirects directly to /v2 (or /) with a session cookie and token
        res_login = client.get('/login')
        assert res_login.status_code == 302
        loc = res_login.headers.get("Location", "")
        assert "token=" in loc and ("/v2" in loc or "/?token=" in loc)
        cookie_header = res_login.headers.get("Set-Cookie", "")
        assert "session=" in cookie_header


def test_independent_worker_views_and_sse_routing(concurrency_mock_app_state):
    """Test targeted vs broadcast SSE message routing."""
    server = MobileServer(concurrency_mock_app_state, port=5099)
    client = server.flask_app.test_client()

    auth1 = client.post('/api/auth', json={"pin": server.pin})
    token1 = auth1.json["token"]
    sid1 = server._get_session_by_token(token1)["session_id"]

    auth2 = client.post('/api/auth', json={"pin": server.pin})
    token2 = auth2.json["token"]
    sid2 = server._get_session_by_token(token2)["session_id"]

    # Register two simulated SSE client entries
    import queue
    q1 = queue.Queue(maxsize=10)
    q2 = queue.Queue(maxsize=10)
    server.clients = [
        {"queue": q1, "session_id": sid1, "token": token1},
        {"queue": q2, "session_id": sid2, "token": token2}
    ]

    # Targeted event for Worker 1 only
    server.broadcast_event("focus_specimen", {"id": "1024"}, target_session_id=sid1)
    server._flush_events()
    assert not q1.empty()
    assert q2.empty()
    msg1 = q1.get_nowait()
    assert msg1.get("type") == "batch"
    assert any(ev.get("type") == "focus_specimen" and ev.get("data", {}).get("id") == "1024" for ev in msg1.get("events", []))

    # Global data event for all workers
    server.broadcast_event("data_updated", {"id": "1024"})
    server._flush_events()
    assert not q1.empty()
    assert not q2.empty()
    msg1_global = q1.get_nowait()
    msg2_global = q2.get_nowait()
    assert any(ev.get("type") == "data_updated" for ev in msg1_global.get("events", []))
    assert any(ev.get("type") == "data_updated" for ev in msg2_global.get("events", []))


def test_presence_tracking_and_heartbeat(concurrency_mock_app_state):
    """Test presence tracking, viewer counting, and object detail warnings."""
    server = MobileServer(concurrency_mock_app_state, port=5099)
    client = server.flask_app.test_client()

    auth1 = client.post('/api/auth', json={"pin": server.pin})
    token1 = auth1.json["token"]
    sid1 = server._get_session_by_token(token1)["session_id"]

    auth2 = client.post('/api/auth', json={"pin": server.pin})
    token2 = auth2.json["token"]
    sid2 = server._get_session_by_token(token2)["session_id"]

    # 1. Worker 1 opens specimen 1024
    p1 = client.post('/api/presence', json={"oid": "1024"}, headers={"X-Session-Token": token1})
    assert p1.status_code == 200
    assert p1.json["other_viewers_count"] == 0

    # GET /api/object/1024 for Worker 1 shows 0 other viewers
    d1 = client.get('/api/object/1024', headers={"X-Session-Token": token1})
    assert d1.json["other_viewers_count"] == 0

    # 2. Worker 2 also opens specimen 1024
    p2 = client.post('/api/presence', json={"oid": "1024"}, headers={"X-Session-Token": token2})
    assert p2.status_code == 200
    assert p2.json["other_viewers_count"] == 1

    # Now GET /api/object/1024 shows 1 other viewer for both workers
    d1_again = client.get('/api/object/1024', headers={"X-Session-Token": token1})
    assert d1_again.json["other_viewers_count"] == 1

    d2 = client.get('/api/object/1024', headers={"X-Session-Token": token2})
    assert d2.json["other_viewers_count"] == 1

    # 3. Worker 1 leaves detail view (oid: None or empty)
    p1_leave = client.post('/api/presence', json={"oid": ""}, headers={"X-Session-Token": token1})
    assert p1_leave.status_code == 200

    # Worker 2 now sees 0 other viewers on 1024
    d2_after = client.get('/api/object/1024', headers={"X-Session-Token": token2})
    assert d2_after.json["other_viewers_count"] == 0
