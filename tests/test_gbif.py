

# ============================================================================
# Merged from test_gbif_mass_update.py
# ============================================================================

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from models import AppState
from backend.gbif import batch_gbif_match
from ui.gbif_review import rollback_gbif_updates


def test_batch_gbif_match_detects_taxonomic_changes():
    items = [
        {
            "oid": "1001",
            "genus": "Pinus",
            "species": "sylvestris",
            "author": "L.",
            "family": "Pinaceae",
            "higher_classification": "3456"  # Dalla Torre number
        },
        {
            "oid": "1002",
            "genus": "Betula",
            "species": "pendula",
            "author": "Roth",
            "family": "Betulaceae",
            "higher_classification": "1234"
        }
    ]

    mock_gbif_responses = {
        ("Pinus", "sylvestris"): {
            "genus": "Pinus",
            "species": "sylvestris",
            "author": "Linnaeus, 1753",
            "family": "Pinaceae",
            "higherClassification": "Plantae | Tracheophyta | Pinopsida | Pinales",
            "status": "ACCEPTED",
            "matchType": "EXACT",
            "rank": "SPECIES",
            "synonym": False
        },
        ("Betula", "pendula"): {
            "genus": "Betula",
            "species": "pendula",
            "author": "Roth",
            "family": "Betulaceae",
            "higherClassification": "Plantae | Tracheophyta",
            "status": "ACCEPTED",
            "matchType": "EXACT",
            "rank": "SPECIES",
            "synonym": False
        }
    }

    def mock_check(g, s):
        return mock_gbif_responses.get((g, s))

    with patch("backend.gbif.check_gbif", side_effect=mock_check):
        diffs = batch_gbif_match(items)

    assert len(diffs) == 1
    diff = diffs[0]
    assert diff["oid"] == "1001"
    changed_fields = [c["field"] for c in diff["changes"]]
    assert "Author" in changed_fields
    assert "Higher Classification" not in changed_fields
    assert "Genus" not in changed_fields


def test_dalla_torre_numbers_not_overwritten():
    items = [{
        "oid": "500",
        "genus": "Pinus",
        "species": "sylvestris",
        "author": "L.",
        "family": "Pinaceae",
        "higher_classification": "3456.0"  # Dalla Torre number
    }]
    gbif_data = {
        "genus": "Pinus",
        "species": "sylvestris",
        "author": "L.",
        "family": "Pinaceae",
        "higherClassification": "Plantae | Tracheophyta | Pinopsida | Pinales",
        "status": "ACCEPTED",
        "synonym": False,
        "matchType": "EXACT",
        "rank": "SPECIES"
    }
    with patch("backend.gbif.check_gbif", return_value=gbif_data):
        diffs = batch_gbif_match(items)
        assert len(diffs) == 0  # No changes proposed since Genus, Species, Author, Family all match


def test_gbif_apply_and_rollback():
    app = AppState()
    app.df_reg = pd.DataFrame([
        {
            "ObjectID": "1001",
            "Genus": "Pinus",
            "Species": "sylvestris",
            "Author": "L.",
            "Family": "Pinaceae",
            "Higher Classification": "3456"
        }
    ]).set_index("ObjectID")
    app.df_obs = pd.DataFrame([
        {
            "ObjectID": "1001",
            "Genus_Problem": False,
            "Author_Problem": True,
            "Collector_Problem": True  # Unrelated problem
        }
    ]).set_index("ObjectID")
    app.df_log = pd.DataFrame(columns=["Timestamp", "User", "Action", "ObjectID", "ChangedFields", "ChangedValues", "ProblemsChanged", "ProblemsChangedValues"])

    # Mock GBIF dialog application
    with app.df_lock:
        app.df_reg.at["1001", "Author"] = "Linnaeus"
        app.df_obs.at["1001", "Author_Problem"] = False
        app._log_records = [{
            "Timestamp": "2026-09-03T12:00:00",
            "User": "test_user",
            "Action": "GBIF_UPDATE",
            "ObjectID": "1001",
            "Reviewed": "",
            "ChangedFields": "Author",
            "ChangedValues": 'Author: "L." -> "Linnaeus"',
            "ProblemsChanged": "Author_Problem",
            "ProblemsChangedValues": 'Author_Problem: "True" -> "False"',
            "LocationChanged": "",
            "LocationChangedValues": ""
        }]
        app.df_log = pd.DataFrame(app._log_records)
        app.dirty = True

    assert app.df_reg.at["1001", "Author"] == "Linnaeus"
    assert app.df_reg.at["1001", "Higher Classification"] == "3456"
    assert bool(app.df_obs.at["1001", "Author_Problem"]) is False
    assert bool(app.df_obs.at["1001", "Collector_Problem"]) is True

    # Test Rollback
    success, msg = rollback_gbif_updates(app)
    assert success is True
    assert app.df_reg.at["1001", "Author"] == "L."
    assert app.df_reg.at["1001", "Higher Classification"] == "3456"
    assert bool(app.df_obs.at["1001", "Author_Problem"]) is True
    assert bool(app.df_obs.at["1001", "Collector_Problem"]) is True
    assert len(app._log_records) == 2
    assert app._log_records[-1]["Action"] == "GBIF_ROLLBACK"


def test_check_gbif_network_error_returns_dict():
    from backend.gbif import check_gbif
    check_gbif.cache_clear()
    with patch("requests.Session.get", side_effect=Exception("Connection timed out")):
        res = check_gbif("Quercus", "robur")
        assert isinstance(res, dict)
        assert "error" in res
        assert "Connection timed out" in res["error"]


def test_check_gbif_higher_classification_formatting():
    from backend.gbif import check_gbif
    check_gbif.cache_clear()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "scientificName": "Quercus robur L.",
        "canonicalName": "Quercus robur",
        "genus": "Quercus",
        "species": "Quercus robur",
        "kingdom": "Plantae",
        "phylum": "Tracheophyta",
        "class": "",  # Empty
        "order": None,  # None
        "matchType": "EXACT",
        "status": "ACCEPTED",
        "rank": "SPECIES"
    }
    with patch("requests.Session.get", return_value=mock_resp):
        res = check_gbif("Quercus", "robur")
        assert res["higherClassification"] == "Plantae | Tracheophyta"


def test_batch_gbif_match_skip_missing_genus():
    items = [
        {"oid": "1", "genus": "", "species": "robur"},
        {"oid": "2", "genus": "   ", "species": "sylvestris"}
    ]
    with patch("backend.gbif.check_gbif") as mock_check:
        res = batch_gbif_match(items)
        assert len(res) == 0
        mock_check.assert_not_called()


def test_batch_gbif_match_synonym_partial_overwrite():
    items = [{
        "oid": "101",
        "genus": "OldGenus",
        "species": "old_spec",
        "author": "OldAuthor",
        "family": "OldFamily"
    }]
    gbif_synonym = {
        "genus": "SynGenus",
        "species": "syn_spec",
        "author": "SynAuthor",
        "family": "SynFamily",
        "higherClassification": "SynHigher",
        "status": "SYNONYM",
        "synonym": True,
        "acceptedUsageKey": 99999,
        "matchType": "EXACT",
        "rank": "SPECIES"
    }
    # Accepted name only returns genus/species, empty author/family/higher
    acc_name = {
        "genus": "NewGenus",
        "species": "new_spec",
        "author": "",
        "family": "",
        "higherClassification": ""
    }

    with patch("backend.gbif.check_gbif", return_value=gbif_synonym), \
         patch("backend.gbif.get_accepted_name", return_value=acc_name):
        res = batch_gbif_match(items, max_workers=2)

    assert len(res) == 1
    proposed = res[0]["proposed"]
    assert proposed["Genus"] == "NewGenus"
    assert proposed["Species"] == "new_spec"
    assert proposed["Author"] == "SynAuthor"  # Retained from gbif_synonym because acc_data had empty
    assert proposed["Family"] == "SynFamily"
    assert "Higher Classification" not in proposed


def test_batch_gbif_match_cancellation():
    import threading
    items = [{"oid": str(i), "genus": "Pinus", "species": f"spec_{i}"} for i in range(20)]
    cancel_event = threading.Event()
    cancel_event.set()

    with patch("backend.gbif.check_gbif") as mock_check:
        res = batch_gbif_match(items, cancel_event=cancel_event, max_workers=2)
        assert len(res) == 0


def test_batch_gbif_match_taxon_deduplication():
    # 100 items with only 2 unique taxa
    items = []
    for i in range(50):
        items.append({"oid": f"p_{i}", "genus": "Pinus", "species": "sylvestris", "author": "L.", "family": "Pinaceae"})
    for i in range(50):
        items.append({"oid": f"b_{i}", "genus": "Betula", "species": "pendula", "author": "Roth", "family": "Betulaceae"})

    mock_resp = {
        ("Pinus", "sylvestris"): {"genus": "Pinus", "species": "sylvestris", "author": "Linnaeus", "family": "Pinaceae", "status": "ACCEPTED", "matchType": "EXACT", "rank": "SPECIES"},
        ("Betula", "pendula"): {"genus": "Betula", "species": "pendula", "author": "Roth", "family": "Betulaceae", "status": "ACCEPTED", "matchType": "EXACT", "rank": "SPECIES"}
    }

    with patch("backend.gbif.check_gbif", side_effect=lambda g, s: mock_resp.get((g, s))) as mock_check:
        diffs = batch_gbif_match(items, max_workers=2)
        # Should only call check_gbif 2 times (once per unique taxon) instead of 100 times!
        assert mock_check.call_count == 2
        # Diff for all 50 Pinus specimens (author changed)
        assert len(diffs) == 50


def test_batch_apply_clears_mapped_problems_and_records_audit_log():
    import tkinter as tk
    from ui.gbif_review import GBIFReviewDialog
    app = AppState()
    app.config = {
        "ui_sections": {
            "problems": [
                {"name": "Genus_Problem", "maps_to": "Genus"},
                {"name": "Species_Problem", "maps_to": "Species"},
                {"name": "Location_Problem", "maps_to": "Location"}
            ]
        }
    }
    app.df_reg = pd.DataFrame([
        {"ObjectID": "101", "Genus": "Pinu", "Species": "sylvestri", "Author": "L.", "Family": "Pinaceae"}
    ]).set_index("ObjectID")
    app.df_obs = pd.DataFrame([
        {"ObjectID": "101", "Genus_Problem": True, "Species_Problem": True, "Location_Problem": True}
    ]).set_index("ObjectID")
    app.df_log = pd.DataFrame(columns=["Timestamp", "User", "Action", "ObjectID", "ChangedFields", "ChangedValues", "ProblemsChanged", "ProblemsChangedValues"])

    diff_results = [{
        "oid": "101",
        "current": {"Genus": "Pinu", "Species": "sylvestri", "Author": "L.", "Family": "Pinaceae"},
        "proposed": {"Genus": "Pinus", "Species": "sylvestris", "Author": "L.", "Family": "Pinaceae"},
        "changes": [
            {"field": "Genus", "old": "Pinu", "new": "Pinus"},
            {"field": "Species", "old": "sylvestri", "new": "sylvestris"}
        ],
        "status": "ACCEPTED",
        "rank": "SPECIES"
    }]

    root = tk.Tk()
    root.withdraw()
    try:
        dialog = GBIFReviewDialog(root, app, diff_results)
        # Apply selected
        with patch("tkinter.messagebox.showinfo"):
            dialog._apply_selected()

        # Verify registration DataFrame updated
        assert app.df_reg.at["101", "Genus"] == "Pinus"
        assert app.df_reg.at["101", "Species"] == "sylvestris"

        # Verify problem flags mapped to Genus and Species are cleared
        assert bool(app.df_obs.at["101", "Genus_Problem"]) is False
        assert bool(app.df_obs.at["101", "Species_Problem"]) is False
        # Unrelated problem remains intact
        assert bool(app.df_obs.at["101", "Location_Problem"]) is True

        # Verify audit log contains Action GBIF_UPDATE and problem diffs
        assert len(app._log_records) == 1
        log_rec = app._log_records[0]
        assert log_rec["Action"] == "GBIF_UPDATE"
        assert "Genus" in log_rec["ChangedFields"]
        assert "Species" in log_rec["ChangedFields"]
        assert "Genus_Problem" in log_rec["ProblemsChanged"]
        assert "Species_Problem" in log_rec["ProblemsChanged"]
        assert 'Genus_Problem: "True" -> "False"' in log_rec["ProblemsChangedValues"]
    finally:
        root.destroy()


def test_gbif_batch_config_dialog_scopes():
    import tkinter as tk
    from ui.gbif_batch_config import GBIFBatchConfigDialog
    from unittest.mock import MagicMock

    root = tk.Tk()
    root.withdraw()
    try:
        main_app = MagicMock()
        main_app.root = root
        main_app.app.df_reg = pd.DataFrame([
            {"ObjectID": "1", "Genus": "Pinus", "Species": "sylvestris", "Author": "L.", "Family": "Pinaceae"},
            {"ObjectID": "2", "Genus": "Betula", "Species": "pendula", "Author": "Roth", "Family": "Betulaceae"},
            {"ObjectID": "3", "Genus": "Quercus", "Species": "robur", "Author": "L.", "Family": "Fagaceae"}
        ]).set_index("ObjectID")
        main_app.app.active_object_ids = ["1", "2"]
        main_app.object_list.get_selected_ids.return_value = ["1"]

        config_dlg = GBIFBatchConfigDialog(root, main_app)
        assert config_dlg.all_count == 3
        assert config_dlg.filtered_count == 2
        assert config_dlg.selected_count == 1
        assert config_dlg.scope_var.get() == "selected"
    finally:
        root.destroy()


def test_author_equivalence_and_validation():
    from backend.gbif import is_author_equivalent
    # Identical with punctuation / dot variations
    assert is_author_equivalent("L.", "L") is True
    assert is_author_equivalent("L.", "L.") is True
    assert is_author_equivalent("(L.) Ehrh.", "(L.) Ehrh.") is True
    assert is_author_equivalent("Hook. f.", "Hook.f.") is True
    assert is_author_equivalent("", "") is True

    # Genuine differences
    assert is_author_equivalent("", "L.") is False
    assert is_author_equivalent("Ehrh.", "Roth") is False
    assert is_author_equivalent("L.", "Linnaeus") is False


def test_classification_equivalence_subsets_and_synonyms():
    from backend.gbif import is_classification_equivalent
    gbif_standard = "Plantae | Tracheophyta | Magnoliopsida | Fagales"

    # Subset with at least 3 ranks (e.g. Tracheophyta + Magnoliopsida + Fagales)
    assert is_classification_equivalent("Tracheophyta | Magnoliopsida | Fagales", gbif_standard) is True
    assert is_classification_equivalent("Plantae | Magnoliopsida | Fagales", gbif_standard) is True

    # Superset (with Family)
    assert is_classification_equivalent("Plantae | Tracheophyta | Magnoliopsida | Fagales | Fagaceae", gbif_standard) is True

    # Traditional division synonym
    assert is_classification_equivalent("Plantae | Magnoliophyta | Magnoliopsida | Fagales", gbif_standard) is True
    assert is_classification_equivalent("Plantae | Angiospermae | Magnoliopsida | Fagales", gbif_standard) is True

    # Incomplete high-level only (e.g. only 2 ranks, missing order & class) -> flags for update
    assert is_classification_equivalent("Plantae | Tracheophyta", gbif_standard) is False

    # Conflicting order
    assert is_classification_equivalent("Plantae | Tracheophyta | Magnoliopsida | Rosales", gbif_standard) is False

    # Empty vs filled
    assert is_classification_equivalent("", gbif_standard) is False
    assert is_classification_equivalent(None, gbif_standard) is False


def test_gbif_toolbar_button_and_dropdown():
    import tkinter as tk
    from ui.navigation_bar import NavigationBar
    from unittest.mock import MagicMock, patch

    root = tk.Tk()
    root.withdraw()
    try:
        mock_app = MagicMock()
        mock_app.root = root
        mock_app.toolbar_buttons = {}
        mock_app.toolbar_vars = {}
        mock_app.config = {"ui_sections": {"problems": []}}

        nav_bar = tk.Frame(root)
        NavigationBar.build_nav_ui(mock_app, nav_bar)

        assert "🌿 GBIF ▾" in mock_app.toolbar_buttons
        btn = mock_app.toolbar_buttons["🌿 GBIF ▾"]
        assert btn is not None

        # Test show_gbif_dropdown method
        from ui.main_window import ObjectProgramUI
        with patch("tkinter.Menu") as mock_menu_cls:
            mock_menu_instance = MagicMock()
            mock_menu_cls.return_value = mock_menu_instance
            ui_instance = MagicMock()
            ui_instance.root = root
            ObjectProgramUI.show_gbif_dropdown(ui_instance)

            # Ensure batch update and rollback were added as commands
            added_labels = [call.kwargs.get("label") for call in mock_menu_instance.add_command.call_args_list]
            assert any(("Run GBIF Taxonomy Check" in str(l) or "Batch Update Taxonomy" in str(l)) for l in added_labels)
            assert any("Revert Latest GBIF" in str(l) for l in added_labels)
    finally:
        root.destroy()


def test_gbif_batch_config_progress_and_percent():
    import tkinter as tk
    from ui.gbif_batch_config import GBIFBatchConfigDialog
    from backend.task_queue import app_worker
    from unittest.mock import MagicMock, patch

    root = tk.Tk()
    root.withdraw()
    app_worker.start(root)
    try:
        main_app = MagicMock()
        main_app.root = root
        main_app.app.df_reg = pd.DataFrame([
            {"ObjectID": "1", "Genus": "Pinus", "Species": "sylvestris", "Author": "L.", "Family": "Pinaceae"},
            {"ObjectID": "2", "Genus": "Betula", "Species": "pendula", "Author": "Roth", "Family": "Betulaceae"}
        ]).set_index("ObjectID")
        main_app.app.active_object_ids = ["1", "2"]
        main_app.object_list.get_selected_ids.return_value = []

        config_dlg = GBIFBatchConfigDialog(root, main_app)

        # Progress bar and percentage elements exist
        assert hasattr(config_dlg, "progress_bar")
        assert hasattr(config_dlg, "pct_var")
        assert hasattr(config_dlg, "status_var")
        assert hasattr(config_dlg, "detail_var")

        # Mock batch_gbif_match with progress callback execution
        def mock_batch_match(items, progress_callback=None, cancel_event=None, *args, **kwargs):
            if progress_callback:
                progress_callback(1, 2, "Pinus sylvestris")
                progress_callback(2, 2, "Betula pendula")
            return []

        with patch("backend.gbif.batch_gbif_match", side_effect=mock_batch_match), \
             patch.object(config_dlg, "_on_analysis_complete") as mock_complete:
            config_dlg._start_analysis()
            config_dlg._worker_thread.join(timeout=2.0)

            # Process task queue tasks on the main thread
            app_worker._poll()
            root.update()

            assert config_dlg.progress_var.get() == 100.0
            assert config_dlg.pct_var.get() == "100%"
            assert "Betula pendula" in config_dlg.detail_var.get()
            mock_complete.assert_called_once()
    finally:
        app_worker.stop()
        root.destroy()


def test_gbif_review_dialog_pagination_and_cross_page_selection():
    import tkinter as tk
    from ui.gbif_review import GBIFReviewDialog
    from unittest.mock import MagicMock, patch

    # Generate 150 mock diff items (simulating large dataset)
    diff_results = []
    reg_rows = []
    obs_rows = []
    for i in range(150):
        oid = str(i + 1)
        reg_rows.append({"ObjectID": oid, "Genus": f"OldGen{i}", "Species": f"oldspec{i}", "Author": "L.", "Family": "Fam"})
        obs_rows.append({"ObjectID": oid, "Genus_Problem": True, "Species_Problem": False})
        diff_results.append({
            "oid": oid,
            "current": {"Genus": f"OldGen{i}", "Species": f"oldspec{i}", "Author": "L.", "Family": "Fam"},
            "proposed": {"Genus": f"NewGen{i}", "Species": f"newspec{i}", "Author": "L.", "Family": "Fam"},
            "changes": [
                {"field": "Genus", "old": f"OldGen{i}", "new": f"NewGen{i}"},
                {"field": "Species", "old": f"oldspec{i}", "new": f"newspec{i}"}
            ],
            "status": "SYNONYM" if i % 2 == 0 else "ACCEPTED",
            "rank": "SPECIES"
        })

    app = MagicMock()
    app.df_reg = pd.DataFrame(reg_rows).set_index("ObjectID")
    app.df_obs = pd.DataFrame(obs_rows).set_index("ObjectID")
    app._log_records = []
    app.df_log = pd.DataFrame()
    app.config = {"ui_sections": {"problems": [{"name": "Genus_Problem", "maps_to": "Genus"}]}}

    root = tk.Tk()
    root.withdraw()
    try:
        dialog = GBIFReviewDialog(root, app, diff_results)

        # 1. Check pagination structure (default page_size = 25 -> 150 / 25 = 6 pages)
        assert dialog.page_size == 25
        assert dialog.current_page == 0
        assert len(dialog.item_cards) == 25  # Only 25 rendered on screen!
        assert len(dialog.selection_state) == 300  # All 300 field changes tracked globally!

        # 2. Test next page navigation
        dialog._goto_next_page()
        assert dialog.current_page == 1
        assert len(dialog.item_cards) == 25
        assert "26" in dialog.item_cards  # Second page starts at #26

        # 3. Test last page navigation
        dialog._goto_last_page()
        assert dialog.current_page == 5
        assert "150" in dialog.item_cards

        # 4. Test Search filter
        dialog.search_var.set("NewGen10")
        filtered = dialog._get_filtered_results()
        assert len(filtered) >= 1
        assert dialog.current_page == 0

        # Reset search
        dialog.search_var.set("")

        # 5. Test Status filter
        dialog.status_var.set("Synonyms (75)")
        dialog._on_status_filter_changed()
        assert dialog.status_filter == "synonym"
        assert len(dialog._get_filtered_results()) == 75

        # Reset status
        dialog.status_var.set("All (150)")
        dialog._on_status_filter_changed()

        # 6. Test Deselect & Select Page vs Batch
        dialog._deselect_all_batch()
        assert sum(1 for v in dialog.selection_state.values() if v) == 0

        dialog._select_current_page()
        # Page 1 has 25 specimens * 2 changes = 50 selected
        assert sum(1 for v in dialog.selection_state.values() if v) == 50

        dialog._select_all_batch()
        assert sum(1 for v in dialog.selection_state.values() if v) == 300

        # 7. Test Applying updates across all pages
        with patch("tkinter.messagebox.showinfo"):
            dialog._apply_selected()

        # Check all 150 items were updated
        assert app.df_reg.at["1", "Genus"] == "NewGen0"
        assert app.df_reg.at["150", "Genus"] == "NewGen149"
        assert bool(app.df_obs.at["1", "Genus_Problem"]) is False
        assert len(app._log_records) == 150
    finally:
        root.destroy()


def test_single_specimen_gbif_update_dialog():
    import tkinter as tk
    from ui.gbif_dialog import GBIFUpdateDialog

    root = tk.Tk()
    root.withdraw()
    try:
        updates = [
            {
                "field": "Taxonomy (Spelling)",
                "current": "Quercus robur",
                "gbif": "Quercus robur L.",
                "selected": True,
                "data": {"genus": "Quercus", "species": "robur"}
            },
            {
                "field": "Author",
                "current": "L.",
                "gbif": "Linnaeus",
                "selected": True,
                "data": {"author": "Linnaeus"}
            }
        ]

        dialog = GBIFUpdateDialog(root, updates)
        assert len(dialog.vars) == 2
        assert dialog.vars[0].get() is True
        assert dialog.vars[1].get() is True

        # Deselect second item and apply
        dialog.vars[1].set(False)
        dialog.apply()

        assert dialog.result_data == {"genus": "Quercus", "species": "robur"}
    finally:
        root.destroy()



def test_sequential_gbif_rollbacks():
    from ui.gbif_review import rollback_gbif_updates
    app = AppState()
    app.df_reg = pd.DataFrame([
        {"ObjectID": "101", "Genus": "Pinus", "Species": "sylvestris", "Author": "Linnaeus"},
        {"ObjectID": "102", "Genus": "Betula", "Species": "pendula", "Author": "Roth"}
    ]).set_index("ObjectID")

    app._log_records = [
        {
            "Timestamp": "2026-09-03T10:00:00",
            "User": "botanist",
            "Action": "GBIF_UPDATE",
            "ObjectID": "101",
            "Reviewed": "",
            "ChangedFields": "Author",
            "ChangedValues": 'Author: "L." -> "Linnaeus"',
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "",
            "LocationChangedValues": "",
            "SourceFile": "test.xlsx",
            "OutputFile": "test.xlsx"
        },
        {
            "Timestamp": "2026-09-03T11:00:00",
            "User": "botanist",
            "Action": "GBIF_UPDATE",
            "ObjectID": "102",
            "Reviewed": "",
            "ChangedFields": "Author",
            "ChangedValues": 'Author: "Ehrh." -> "Roth"',
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "",
            "LocationChangedValues": "",
            "SourceFile": "test.xlsx",
            "OutputFile": "test.xlsx"
        }
    ]
    app.df_log = pd.DataFrame(app._log_records)

    success, msg = rollback_gbif_updates(app)
    assert success is True
    assert app.df_reg.at["102", "Author"] == "Ehrh."
    assert app.df_reg.at["101", "Author"] == "Linnaeus"


def test_gbif_rollback_timestamp_space_and_iso_normalization():
    from ui.gbif_review import rollback_gbif_updates
    from unittest.mock import MagicMock, patch
    with patch("tkinter.messagebox.showinfo"):
        app = AppState()
        app.df_reg = pd.DataFrame([
            {"ObjectID": "201", "Genus": "Pinus", "Species": "sylvestris", "Author": "Linnaeus"}
        ]).set_index("ObjectID")

        app._log_records = [
            {
                "Timestamp": "2026-09-03T10:30:00",
                "User": "botanist",
                "Action": "GBIF_UPDATE",
                "ObjectID": "201",
                "Reviewed": "",
                "ChangedFields": "Author",
                "ChangedValues": 'Author: "L." -> "Linnaeus"',
                "ProblemsChanged": "",
                "ProblemsChangedValues": "",
                "LocationChanged": "",
                "LocationChangedValues": "",
                "SourceFile": "test.xlsx",
                "OutputFile": "test.xlsx"
            }
        ]
        app.df_log = pd.DataFrame(app._log_records)

        mock_ui = MagicMock()
        mock_ui.app = app
        mock_ui._invalidate_row_cache = MagicMock()
        mock_ui.invalidate_search_index = MagicMock()

        success, msg = rollback_gbif_updates(app, main_window=mock_ui)
        assert success is True
        assert app.df_reg.at["201", "Author"] == "L."
        assert mock_ui._invalidate_row_cache.called
        assert mock_ui.invalidate_search_index.called


# ============================================================================
# Merged from test_gbif_family_resolution.py
# ============================================================================

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from backend.gbif import (
    is_undetermined_species,
    _query_single_taxon,
    _evaluate_item_diff,
    batch_gbif_match,
    check_gbif
)


class TestUndeterminedSpeciesDetection:
    """Test recognition of open nomenclature and undetermined species markers."""

    def test_exact_undetermined_tokens(self):
        assert is_undetermined_species("") is True
        assert is_undetermined_species(None) is True
        assert is_undetermined_species("sp.") is True
        assert is_undetermined_species("sp") is True
        assert is_undetermined_species("SP.") is True
        assert is_undetermined_species("spp.") is True
        assert is_undetermined_species("spp") is True
        assert is_undetermined_species("spec.") is True
        assert is_undetermined_species("species") is True
        assert is_undetermined_species("indet.") is True
        assert is_undetermined_species("indet") is True
        assert is_undetermined_species("undet.") is True
        assert is_undetermined_species("unknown") is True
        assert is_undetermined_species("?") is True
        assert is_undetermined_species("-") is True
        assert is_undetermined_species("none") is True
        assert is_undetermined_species("n/a") is True

    def test_morphospecies_patterns(self):
        assert is_undetermined_species("sp. 1") is True
        assert is_undetermined_species("sp. A") is True
        assert is_undetermined_species("sp. nov.") is True
        assert is_undetermined_species("sp. nr.") is True
        assert is_undetermined_species("indet. 2") is True
        assert is_undetermined_species("species 14") is True

    def test_valid_species_not_undetermined(self):
        assert is_undetermined_species("terrestris") is False
        assert is_undetermined_species("pascuorum") is False
        assert is_undetermined_species("mellifera") is False
        assert is_undetermined_species("vulgaris") is False


class TestTaxonQueryingAndFamilyResolution:
    """Test that GBIF queries resolve Family for both binomials and genus-only taxa."""

    @patch("backend.gbif.check_gbif")
    def test_binomial_resolves_family_and_species(self, mock_check):
        mock_check.return_value = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "genus": "Bombus",
            "species": "pascuorum",
            "author": "(Scopoli, 1763)",
            "family": "Apidae",
            "rank": "SPECIES",
            "synonym": False
        }

        res = _query_single_taxon("Bombus", "pascuorum")
        assert res is not None
        assert res["family"] == "Apidae"
        assert res["species"] == "pascuorum"
        assert res["is_undetermined"] is False
        mock_check.assert_called_once_with("Bombus", "pascuorum")

    @patch("backend.gbif.check_gbif")
    def test_undetermined_queries_genus_only_and_preserves_sp(self, mock_check):
        mock_check.return_value = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "genus": "Bombus",
            "species": "",
            "author": "Latreille, 1802",
            "family": "Apidae",
            "rank": "GENUS",
            "synonym": False
        }

        res = _query_single_taxon("Bombus", "sp.")
        assert res is not None
        assert res["family"] == "Apidae"
        assert res["species"] == "sp."  # Preserves raw undetermined string
        assert res["is_undetermined"] is True
        # Verify it passed empty species to check_gbif
        mock_check.assert_called_once_with("Bombus", "")


class TestDiffEvaluation:
    """Test diff generation for missing metadata and undetermined records."""

    def test_missing_family_populated_for_binomial(self):
        item = {
            "oid": "101",
            "genus": "Bombus",
            "species": "terrestris",
            "author": "(Linnaeus, 1758)",
            "family": ""  # Missing family
        }
        gbif_data = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "genus": "Bombus",
            "species": "terrestris",
            "author": "(Linnaeus, 1758)",
            "family": "Apidae",
            "rank": "SPECIES",
            "is_undetermined": False
        }

        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        assert diff["missing_family"] is True
        assert diff["is_undetermined"] is False
        assert len(diff["changes"]) == 1
        assert diff["changes"][0]["field"] == "Family"
        assert diff["changes"][0]["new"] == "Apidae"

    def test_undetermined_item_never_changes_species(self):
        item = {
            "oid": "102",
            "genus": "Bombus",
            "species": "sp.",
            "author": "",
            "family": ""
        }
        gbif_data = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "genus": "Bombus",
            "species": "sp.",
            "author": "Latreille, 1802",  # Genus author from GBIF
            "family": "Apidae",
            "rank": "GENUS",
            "is_undetermined": True
        }

        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        assert diff["is_undetermined"] is True
        assert diff["missing_family"] is True
        assert diff["missing_author"] is True
        # Verify Species is NEVER changed, but Family and Genus Author are proposed
        changed_fields = [c["field"] for c in diff["changes"]]
        assert "Species" not in changed_fields
        assert "Family" in changed_fields
        assert "Author" in changed_fields


class TestBatchGBIFMatchScope:
    """Test batch matching with deduplication and exclusion flags."""

    @patch("backend.gbif._query_single_taxon")
    def test_batch_match_deduplicates_undetermined_records(self, mock_query):
        mock_query.return_value = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "genus": "Bombus",
            "species": "sp.",
            "author": "",
            "family": "Apidae",
            "rank": "GENUS",
            "is_undetermined": True
        }

        items = [
            {"oid": "1", "genus": "Bombus", "species": "sp.", "author": "", "family": ""},
            {"oid": "2", "genus": "Bombus", "species": "indet.", "author": "", "family": ""},
            {"oid": "3", "genus": "Bombus", "species": "sp.", "author": "", "family": ""}
        ]

        results = batch_gbif_match(items, exclude_undetermined=False)
        assert len(results) == 3
        # Should have queried unique undetermined taxon only once
        assert mock_query.call_count == 1

    @patch("backend.gbif._query_single_taxon")
    def test_batch_match_excludes_undetermined_when_flagged(self, mock_query):
        mock_query.return_value = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "genus": "Apis",
            "species": "mellifera",
            "author": "Linnaeus, 1758",
            "family": "Apidae",
            "rank": "SPECIES",
            "is_undetermined": False
        }

        items = [
            {"oid": "1", "genus": "Bombus", "species": "sp.", "author": "", "family": ""},
            {"oid": "2", "genus": "Apis", "species": "mellifera", "author": "", "family": ""},
        ]

        results = batch_gbif_match(items, exclude_undetermined=True)
        # Bombus sp. excluded; only Apis mellifera processed
        assert len(results) == 1
        assert results[0]["oid"] == "2"
        assert mock_query.call_count == 1


# ============================================================================
# Merged from test_gbif_rank_discrepancy_and_provenance.py
# ============================================================================

import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

from backend.gbif import (
    check_gbif,
    _evaluate_item_diff,
    is_likely_family_name
)
from backend.cross_validation import (
    collect_field_provenance,
    validate_candidate_with_gbif,
    get_validated_provenance_candidates,
    scan_taxonomic_rank_inversions,
    restore_provenance_candidate
)
from models import AppState


class TestGBIFRankDiscrepancyAndPrevention:
    """Test prevention of family-as-species pollution and proper rank classification."""

    def test_is_likely_family_name(self):
        assert is_likely_family_name("Pinaceae") is True
        assert is_likely_family_name("pinaceae") is True
        assert is_likely_family_name("Asteraceae") is True
        assert is_likely_family_name("Compositae") is True
        assert is_likely_family_name("Fabaceae") is True
        assert is_likely_family_name("excelsa") is False
        assert is_likely_family_name("sylvestris") is False
        assert is_likely_family_name("") is False

    def test_gbif_homonym_disambiguation_with_genus(self):
        # When genus is passed, Pinus excelsa must resolve to species wallichiana, NOT family Pinaceae
        res = check_gbif("Pinus", "excelsa")
        assert res is not None
        assert res.get("rank") == "SPECIES"
        assert res.get("genus") == "Pinus"
        assert res.get("species") == "wallichiana"
        assert res.get("status") == "SYNONYM"
        assert res.get("family") == "Pinaceae"

    def test_higher_rank_never_pollutes_species(self):
        # Mock a GBIF response that returns FAMILY
        mock_resp = {
            "usageKey": 3925,
            "scientificName": "Pinaceae",
            "canonicalName": "Pinaceae",
            "rank": "FAMILY",
            "status": "ACCEPTED",
            "confidence": 97,
            "matchType": "HIGHERRANK",
            "family": "Pinaceae"
        }
        with patch("backend.gbif._session.get") as mock_get:
            mock_res = MagicMock()
            mock_res.json.return_value = mock_resp
            mock_res.raise_for_status = MagicMock()
            mock_get.return_value = mock_res

            # Clear cache for isolated test
            check_gbif.cache_clear()
            res = check_gbif("UnknownGenus", "fakeSpecies")
            assert res is not None
            assert res.get("rank") == "FAMILY"
            # Species must be empty, NEVER Pinaceae!
            assert res.get("species") == ""
            assert res.get("family") == "Pinaceae"

    def test_low_similarity_is_never_labeled_as_spelling(self):
        item = {
            "oid": "67",
            "genus": "Pinus",
            "species": "excelsa",
            "family": "Pinaceae"
        }
        gbif_data = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "is_synonym": False,
            "genus": "Pinus",
            "species": "wallichiana",
            "rank": "SPECIES",
            "is_undetermined": False
        }
        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        sp_chg = next(c for c in diff["changes"] if c["field"] == "Species")
        # excelsa -> wallichiana is NOT a spelling typo (similarity 22%)
        assert sp_chg["reason_code"] != "SPELLING"
        assert sp_chg["reason_code"] == "RECLASSIFICATION"

    def test_rank_discrepancy_flags_and_disables_auto_resolve(self):
        # Corrupted item where current species is a family name
        item = {
            "oid": "67",
            "genus": "Pinus",
            "species": "Pinaceae",
            "family": "Pinaceae"
        }
        gbif_data = {
            "matchType": "EXACT",
            "status": "SYNONYM",
            "is_synonym": True,
            "genus": "Pinus",
            "species": "wallichiana",
            "rank": "SPECIES",
            "is_undetermined": False
        }
        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        assert diff["has_rank_discrepancy"] is True
        assert "Species → Family" in diff["rank_discrepancy"]
        assert diff["auto_resolve_eligible"] is False

        sp_chg = next(c for c in diff["changes"] if c["field"] == "Species")
        assert sp_chg["has_rank_discrepancy"] is True
        assert sp_chg["auto_resolve_eligible"] is False
        assert sp_chg["reason_code"] == "RANK_DISCREPANCY"


class TestProvenanceAndValidation:
    """Test multi-source collection from books (preserving sheet names) and audit log with GBIF checks."""

    def test_collect_provenance_multi_sheets_and_audit_log(self):
        app = AppState()
        # Mock 2 different book sheets with different names
        df_sheet1 = pd.DataFrame([{"ObjectID": "67", "Species": "excelsa"}])
        df_sheet2 = pd.DataFrame([{"ObjectID": "67", "Species": "wallichiana"}])

        app.historical_dbs = [
            {"name": "Books: 1912 Ledger", "df_reg": df_sheet1},
            {"name": "Books: 1955 Catalog", "df_reg": df_sheet2}
        ]

        # Mock an audit log entry for this OID
        app._log_records = [
            {
                "Timestamp": "2026-09-03T10:00:00",
                "Action": "GBIF_UPDATE",
                "ObjectID": "67",
                "ChangedValues": 'Species: "excelsa" -> "Pinaceae"'
            }
        ]
        app.df_log = pd.DataFrame(app._log_records)

        candidates = collect_field_provenance(app, "67", "Species")
        assert len(candidates) == 3

        # Check that sheet names are accurately recorded
        source_names = [c["source_name"] for c in candidates]
        assert "Books: 1912 Ledger" in source_names
        assert "Books: 1955 Catalog" in source_names
        assert any("Audit Log" in s for s in source_names)

        values = [c["value"] for c in candidates]
        assert "excelsa" in values
        assert "wallichiana" in values

    def test_preflight_gbif_validation_on_candidates(self):
        # excelsa -> Valid historical synonym
        val_excelsa = validate_candidate_with_gbif("Pinus", "excelsa")
        assert val_excelsa["status"] == "SYNONYM"
        assert "Valid Synonym" in val_excelsa["badge_label"]
        assert "wallichiana" in val_excelsa["accepted_name"].lower()

        # wallichiana -> Accepted species
        val_wall = validate_candidate_with_gbif("Pinus", "wallichiana")
        assert val_wall["status"] == "ACCEPTED"
        assert "Current Accepted Species" in val_wall["badge_label"]


class TestScanAndRestoreTaxonomicInversions:
    """Test dataset-wide scan and safe audit-logged restoration."""

    def test_scan_and_restore_workflow(self):
        app = AppState()
        app.df_reg = pd.DataFrame([
            {"ObjectID": "101", "Genus": "Pinus", "Species": "Pinaceae", "Family": "Pinaceae"},
            {"ObjectID": "102", "Genus": "Betula", "Species": "pendula", "Family": "Betulaceae"}
        ]).set_index("ObjectID")

        # Mock historical books containing the genuine species for 101
        app.historical_dbs = [
            {
                "name": "Books: Primary Ledger",
                "df_reg": pd.DataFrame([{"ObjectID": "101", "Species": "sylvestris"}])
            }
        ]

        # 1. Scan detects the rank inversion on 101, but not on 102
        anomalies = scan_taxonomic_rank_inversions(app)
        assert len(anomalies) == 1
        assert anomalies[0]["oid"] == "101"
        assert anomalies[0]["current_species"] == "Pinaceae"
        assert len(anomalies[0]["candidates"]) == 1
        assert anomalies[0]["candidates"][0]["value"] == "sylvestris"

        # 2. Restore 101 to sylvestris
        ok = restore_provenance_candidate(app, "101", "Species", "sylvestris", "Books: Primary Ledger")
        assert ok is True
        assert app.df_reg.at["101", "Species"] == "sylvestris"

        # Verify audit log recorded the restoration
        assert len(app._log_records) == 1
        log_e = app._log_records[-1]
        assert log_e["Action"] == "TAXONOMIC_INVERSION_RESTORE"
        assert log_e["ObjectID"] == "101"
        assert 'Species: "Pinaceae" -> "sylvestris"' in log_e["ChangedValues"]

        # 3. Subsequent scan finds zero anomalies
        clean_scan = scan_taxonomic_rank_inversions(app)
        assert len(clean_scan) == 0


# ============================================================================
# Merged from test_gbif_synonym_reasoning.py
# ============================================================================

import pytest
from unittest.mock import patch, MagicMock
from backend.gbif import (
    _evaluate_item_diff,
    _query_single_taxon,
    batch_gbif_match
)


class TestGBIFSynonymReasoning:
    """Test explicit reasoning and categorization for Genus/Species updates."""

    def test_synonym_genus_transfer_generates_synonym_reason_and_explanation(self):
        item = {
            "oid": "1",
            "genus": "Apis",
            "species": "terrestris",
            "author": "Linnaeus, 1758",
            "family": "Apidae"
        }
        gbif_data = {
            "matchType": "EXACT",
            "status": "SYNONYM",
            "is_synonym": True,
            "genus": "Bombus",
            "species": "terrestris",
            "author": "(Linnaeus, 1758)",
            "family": "Apidae",
            "rank": "SPECIES",
            "is_undetermined": False,
            "original_scientific_name": "Apis terrestris Linnaeus, 1758",
            "accepted_scientific_name": "Bombus terrestris (Linnaeus, 1758)"
        }

        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        assert diff["is_synonym"] is True
        assert diff["status"] == "SYNONYM"

        # Check Genus change reason
        genus_chg = next((c for c in diff["changes"] if c["field"] == "Genus"), None)
        assert genus_chg is not None
        assert genus_chg["reason_code"] == "SYNONYM_GENUS"
        assert "Synonym" in genus_chg["reason_label"]
        assert "is cataloged as a synonym" in genus_chg["explanation"]

    def test_spelling_correction_generates_spelling_reason(self):
        item = {
            "oid": "2",
            "genus": "Bumbus",
            "species": "pascuorum",
            "author": "(Scopoli, 1763)",
            "family": "Apidae"
        }
        gbif_data = {
            "matchType": "FUZZY",
            "status": "ACCEPTED",
            "is_synonym": False,
            "genus": "Bombus",
            "species": "pascuorum",
            "author": "(Scopoli, 1763)",
            "family": "Apidae",
            "rank": "SPECIES",
            "is_undetermined": False
        }

        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        assert diff["is_synonym"] is False

        genus_chg = next((c for c in diff["changes"] if c["field"] == "Genus"), None)
        assert genus_chg is not None
        assert genus_chg["reason_code"] == "SPELLING"
        assert "Spelling" in genus_chg["reason_label"]
        assert "Corrected genus spelling" in genus_chg["explanation"]

    def test_missing_family_generates_missing_reason(self):
        item = {
            "oid": "3",
            "genus": "Bombus",
            "species": "sp.",
            "author": "",
            "family": ""
        }
        gbif_data = {
            "matchType": "EXACT",
            "status": "ACCEPTED",
            "is_synonym": False,
            "genus": "Bombus",
            "species": "sp.",
            "author": "Latreille, 1802",
            "family": "Apidae",
            "rank": "GENUS",
            "is_undetermined": True
        }

        diff = _evaluate_item_diff(item, gbif_data)
        assert diff is not None
        fam_chg = next((c for c in diff["changes"] if c["field"] == "Family"), None)
        assert fam_chg is not None
        assert fam_chg["reason_code"] == "MISSING_FAMILY"
        assert "Missing Family" in fam_chg["reason_label"]


class TestOldNamesAndSynonyms:
    """Tests for 1-tap Old Names & Synonyms engine, silent disk cache, and label comparison."""

    def test_offline_old_family_names_classical_and_apg(self):
        from backend.gbif import get_old_family_names

        ast = [x["name"] for x in get_old_family_names("Asteraceae")]
        assert "Compositae" in ast
        comp = [x["name"] for x in get_old_family_names("Compositae")]
        assert "Asteraceae" in comp
        malv = [x["name"] for x in get_old_family_names("Malvaceae")]
        assert "Tiliaceae" in malv and "Sterculiaceae" in malv
        assert get_old_family_names("") == []

    def test_get_synonyms_ranking_disk_cache_and_offline_fallback(self, tmp_path):
        import os
        from backend import gbif as gbif_mod

        gbif_mod.check_gbif.cache_clear()
        cache_file = str(tmp_path / ".arbor_synonyms_cache.json")

        fake_match = {
            "matchType": "EXACT", "status": "ACCEPTED", "canonicalName": "Betula pendula",
            "usageKey": 5331916, "acceptedUsageKey": None, "family": "Betulaceae",
            "confidence": 99, "synonym": False,
        }
        sp_resp = MagicMock(ok=True)
        sp_resp.json.return_value = {"basionym": "Betula alba L."}
        syn_resp = MagicMock(ok=True)
        syn_resp.raise_for_status = lambda: None
        syn_resp.json.return_value = {
            "results": [
                {"canonicalName": "Betula verrucosa", "authorship": "Ehrh.", "taxonomicStatus": "HETEROTYPIC_SYNONYM", "rank": "SPECIES"},
                {"canonicalName": "Betula alba", "authorship": "L.", "taxonomicStatus": "HOMOTYPIC_SYNONYM", "rank": "SPECIES"},
                {"canonicalName": "Betula pendula var. carelica", "authorship": "", "taxonomicStatus": "HETEROTYPIC_SYNONYM", "rank": "VARIETY"},
            ]
        }

        mock_sess = MagicMock()
        mock_sess.get.side_effect = [sp_resp, syn_resp]

        with patch.object(gbif_mod, "check_gbif", return_value=fake_match), \
             patch.object(gbif_mod, "_get_session", return_value=mock_sess):
            res = gbif_mod.get_synonyms("Betula", "pendula", family="Betulaceae", cache_path=cache_file)

        assert res["offline"] is False
        assert res["primary_synonyms"][0]["name"] == "Betula alba"
        assert res["primary_synonyms"][0]["kind"] == "Basionym"
        assert any(s["name"] == "Betula verrucosa" for s in res["other_synonyms"])
        assert os.path.exists(cache_file)

        # Clear in-memory cache and simulate offline -> disk cache still serves results cleanly!
        gbif_mod.check_gbif.cache_clear()
        with patch.object(gbif_mod, "check_gbif", return_value={"error": "offline"}):
            cached = gbif_mod.get_synonyms("Betula", "pendula", family="Betulaceae", cache_path=cache_file)
        assert cached["from_cache"] is True
        assert cached["offline"] is False
        assert cached["primary_synonyms"][0]["name"] == "Betula alba"

        # Uncached taxon offline -> returns offline=True + offline family aliases cleanly
        with patch.object(gbif_mod, "check_gbif", return_value={"error": "offline"}):
            off = gbif_mod.get_synonyms("Taraxacum", "officinale", family="Asteraceae", cache_path=cache_file)
        assert off["offline"] is True
        assert any(f["name"] == "Compositae" for f in off["old_families"])

    def test_compare_label_name_verdicts(self):
        from backend import gbif as gbif_mod

        # 1. Offline classical family match -> zero network calls needed
        fam_res = gbif_mod.compare_label_name("Compositae", "Taraxacum", "officinale", reg_family="Asteraceae")
        assert fam_res["verdict"] == "synonym_match"

        # 2. Same acceptedUsageKey -> synonym_match
        with patch.object(gbif_mod, "check_gbif", side_effect=[
            {"usageKey": 100, "acceptedUsageKey": None, "canonicalName": "Betula pendula", "confidence": 99, "matchType": "EXACT"},
            {"usageKey": 200, "acceptedUsageKey": 100, "canonicalName": "Betula verrucosa", "confidence": 98, "matchType": "EXACT", "synonym": True},
        ]):
            r = gbif_mod.compare_label_name("Betula verrucosa", "Betula", "pendula")
        assert r["verdict"] == "synonym_match"

        # 3. Different acceptedUsageKey (EXACT) -> different_species
        with patch.object(gbif_mod, "check_gbif", side_effect=[
            {"usageKey": 100, "acceptedUsageKey": None, "canonicalName": "Betula pendula", "confidence": 99, "matchType": "EXACT"},
            {"usageKey": 300, "acceptedUsageKey": None, "canonicalName": "Quercus robur", "confidence": 99, "matchType": "EXACT", "synonym": False},
        ]):
            r = gbif_mod.compare_label_name("Quercus robur", "Betula", "pendula")
        assert r["verdict"] == "different_species"

        # 4. Offline -> neutral uncertain verdict
        with patch.object(gbif_mod, "check_gbif", return_value={"error": "offline"}):
            r = gbif_mod.compare_label_name("Unknownus plantus", "Betula", "pendula")
        assert r["verdict"] == "uncertain"
        assert r.get("offline") is True

    def test_record_batch_diffs_populates_offline_synonym_cache(self, tmp_path):
        from backend import gbif as gbif_mod

        gbif_mod.check_gbif.cache_clear()
        cache_file = str(tmp_path / ".arbor_synonyms_cache.json")
        diffs = [
            {
                "oid": "10",
                "current": {"Genus": "Betula", "Species": "alba", "Family": "Betulaceae"},
                "proposed": {"Genus": "Betula", "Species": "pendula", "Family": "Betulaceae"},
                "is_synonym": True,
            },
            {
                "oid": "11",
                "current": {"Genus": "Tilia", "Species": "cordata", "Family": "Tiliaceae"},
                "proposed": {"Genus": "Tilia", "Species": "cordata", "Family": "Malvaceae"},
                "is_synonym": False,
            },
        ]
        count = gbif_mod.record_batch_diffs_to_synonym_cache(diffs, cache_file)
        assert count == 2

        # Clear memory cache and verify offline vault lookup serves the recorded old name immediately
        gbif_mod.check_gbif.cache_clear()
        with patch.object(gbif_mod, "check_gbif", return_value={"error": "offline"}):
            res = gbif_mod.get_synonyms("Betula", "pendula", family="Betulaceae", cache_path=cache_file)
        assert res["from_cache"] is True
        assert res["offline"] is False
        assert any(s["name"] == "Betula alba" for s in res["primary_synonyms"])
