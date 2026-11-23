import pandas as pd
import os
from unittest import mock
from repository import SQLiteRepository, _normalise_dataframes, _normalise_log_dataframe

class TestRepository:
    def test_normalise_dataframes(self):
        df_reg = pd.DataFrame({"ObjectID": [" 1 ", "2"]})
        df_obs = pd.DataFrame({"ObjectID": ["1", " 2 "]})
        config = {
            "ui_sections": {
                "problems": [{"name": "Prob1"}],
                "location": [{"name": "Loc1"}],
                "registration": [{"name": "Reg1"}]
            }
        }

        df_reg_out, df_obs_out = _normalise_dataframes(df_reg, df_obs, config)

        # Test ObjectID cleaning
        assert list(df_reg_out["ObjectID"]) == ["1", "2"]
        assert list(df_obs_out["ObjectID"]) == ["1", "2"]

        # Test registration columns
        assert "Reg1" in df_reg_out.columns
        assert "UID" in df_reg_out.columns
        assert "ProblemDescription" in df_reg_out.columns

        # Test problem columns
        assert "Prob1" in df_obs_out.columns

        # Test location columns
        assert "Loc1" in df_obs_out.columns

        # Test default obs columns
        assert "Images_Missing" in df_obs_out.columns
        assert "Images_Problem" in df_obs_out.columns
        assert "Reviewed" in df_obs_out.columns

    def test_sqlite_roundtrip(self, tmp_path):
        db_path = tmp_path / "test.db"

        df_reg = pd.DataFrame({"ObjectID": ["1", "2"], "UID": ["u1", "u2"], "ProblemDescription": ["p1", "p2"]})
        df_obs = pd.DataFrame({"ObjectID": ["1", "2"], "Images_Missing": [True, False], "Images_Problem": [False, False], "Reviewed": [False, False], "ReviewedAt": ["", ""], "Online_Images_Exist": [False, False]})
        df_photo = pd.DataFrame({"ObjectID": ["1"]})
        df_log = _normalise_log_dataframe(pd.DataFrame())
        df_unval = pd.DataFrame({"ObjectID": ["1"], "Field_Name": ["Genus"], "Unvalidated_Comment": ["Check spelling"]})

        SQLiteRepository.save_sqlite(str(db_path), df_reg, df_obs, df_photo, df_log, df_unval)

        assert os.path.exists(db_path)

        config = {"ui_sections": {}}
        df_reg_read, df_obs_read, df_photo_read, df_log_read, df_unval_read = SQLiteRepository.load_sqlite(str(db_path), config)

        assert list(df_reg_read["ObjectID"]) == ["1", "2"]
        assert list(df_obs_read["ObjectID"]) == ["1", "2"]
        assert list(df_photo_read["ObjectID"]) == ["1"]
        assert list(df_unval_read["Field_Name"]) == ["Genus"]
        assert list(df_unval_read["Unvalidated_Comment"]) == ["Check spelling"]

    @mock.patch("repository.ExcelRepository.load_excel")
    @mock.patch("repository.SQLiteRepository.save_sqlite")
    def test_import_from_excel(self, mock_save_sqlite, mock_load_excel, tmp_path):
        # Create a dummy excel file to be backed up
        excel_path = tmp_path / "data.xlsx"
        excel_path.write_text("dummy content")

        sqlite_path = tmp_path / "data.db"
        config = {"ui_sections": {}}

        # Setup mock return values for load_excel
        mock_df_reg = pd.DataFrame({"ObjectID": ["1"]})
        mock_df_obs = pd.DataFrame({"ObjectID": ["1"]})
        mock_df_photo = pd.DataFrame({"ObjectID": ["1"]})
        mock_df_log = pd.DataFrame({"ObjectID": ["1"]})
        mock_df_unval = pd.DataFrame({"ObjectID": ["1"], "Field_Name": ["Species"], "Unvalidated_Comment": ["Note"]})
        mock_load_excel.return_value = (mock_df_reg, mock_df_obs, mock_df_photo, mock_df_log, mock_df_unval)

        # Execute the method under test
        result = SQLiteRepository.import_from_excel(str(excel_path), str(sqlite_path), config)

        # Assert correct methods were called
        mock_load_excel.assert_called_once_with(str(excel_path), config)
        mock_save_sqlite.assert_called_once_with(str(sqlite_path), mock_df_reg, mock_df_obs, mock_df_photo, mock_df_log, mock_df_unval)

        # Assert return values
        assert result == (mock_df_reg, mock_df_obs, mock_df_photo, mock_df_log, mock_df_unval)

        # Assert backup was created correctly
        backup_dir = tmp_path / "backups"
        assert backup_dir.exists()
        assert backup_dir.is_dir()

        backup_files = list(backup_dir.iterdir())
        assert len(backup_files) == 1
        assert backup_files[0].name.startswith("data.xlsx.backup_")
        assert backup_files[0].name.endswith(".xlsx")
        assert backup_files[0].read_text() == "dummy content"


    def test_export_to_excel(self, tmp_path):
        excel_path = tmp_path / "test_out.xlsx"
        df_reg = pd.DataFrame({"ObjectID": ["1", "2"], "UID": ["u1", "u2"], "ProblemDescription": ["p1", "p2"]})
        df_obs = pd.DataFrame({"ObjectID": ["1", "2"]})
        df_log = pd.DataFrame()
        config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {}
        }
        SQLiteRepository.export_to_excel(None, str(excel_path), config, df_reg=df_reg, df_obs=df_obs, df_log=df_log)
        assert os.path.exists(excel_path)
        df_reg_read = pd.read_excel(excel_path, sheet_name="Registration")
        assert list(df_reg_read["ObjectID"]) == [1, 2]

    def test_normalise_dataframes_checkbox_default(self):
        config = {
            "ui_sections": {
                "location": [
                    {"name": "Building", "type": "choice"},
                    {"name": "Loaned out", "type": "checkbox"},
                    {"name": "Loaned out date", "type": "text"}
                ],
                "problems": [],
                "registration": [{"name": "Genus"}]
            }
        }
        df_reg = pd.DataFrame({"ObjectID": ["1", "2", "3", "4", "5"]})
        df_obs = pd.DataFrame({
            "ObjectID": ["1", "2", "3", "4", "5"],
            "Loaned out": ["", "True", False, True, None]
        })
        df_reg, df_obs = _normalise_dataframes(df_reg, df_obs, config)
        assert df_obs.loc[df_obs["ObjectID"] == "1", "Loaned out"].iloc[0] == "False"
        assert df_obs.loc[df_obs["ObjectID"] == "2", "Loaned out"].iloc[0] == "True"
        assert df_obs.loc[df_obs["ObjectID"] == "3", "Loaned out"].iloc[0] == "False"
        assert df_obs.loc[df_obs["ObjectID"] == "4", "Loaned out"].iloc[0] == "True"
        assert df_obs.loc[df_obs["ObjectID"] == "5", "Loaned out"].iloc[0] == "False"

    def test_sanitize_df_timezone(self):
        from utils import sanitize_df_for_excel
        df = pd.DataFrame({"a": [pd.Timestamp("2020-01-01", tz="UTC")]})
        df_safe = sanitize_df_for_excel(df)
        assert pd.api.types.is_datetime64_any_dtype(df_safe["a"])
        assert df_safe["a"].dt.tz is None

    def test_sanitize_df_illegal_chars(self):
        from utils import sanitize_df_for_excel
        df = pd.DataFrame({"a": ["hello\x00world"]})
        df_safe = sanitize_df_for_excel(df)
        assert df_safe["a"].iloc[0] == "helloworld"

    def test_sanitize_df_formula_injection(self):
        from utils import sanitize_df_for_excel
        df = pd.DataFrame({"a": ["=1+1", "-2+2", "cmd|foo", "test"]})
        df_safe = sanitize_df_for_excel(df)
        assert df_safe["a"].iloc[0] == "'=1+1"
        assert df_safe["a"].iloc[1] == "'-2+2"
        assert df_safe["a"].iloc[2] == "'cmd|foo"
        assert df_safe["a"].iloc[3] == "test"

    def test_atomic_save_failure_leaves_original_intact(self, tmp_path):
        """Verify that if an error occurs midway through writing, the original Excel file remains untouched."""
        excel_path = tmp_path / "botanical_records.xlsx"
        config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {}
        }
        # Create valid original file
        df_reg_orig = pd.DataFrame({"ObjectID": ["001", "002"], "Genus": ["Rosa", "Pinus"]})
        df_obs_orig = pd.DataFrame({"ObjectID": ["001", "002"], "Reviewed": [True, False]})
        SQLiteRepository.export_to_excel(None, str(excel_path), config, df_reg=df_reg_orig, df_obs=df_obs_orig)
        original_mtime = os.path.getmtime(excel_path)
        original_size = os.path.getsize(excel_path)

        # Attempt to overwrite with new data but simulate failure during save
        df_reg_bad = pd.DataFrame({"ObjectID": ["999"], "Genus": ["Corrupted"]})
        def failing_progress(cur, total, label):
            if cur >= 1:
                raise RuntimeError("Simulated write failure")

        import pytest
        with pytest.raises(RuntimeError, match="Simulated write failure"):
            SQLiteRepository.export_to_excel(
                None, str(excel_path), config,
                df_reg=df_reg_bad, df_obs=df_obs_orig,
                progress_callback=failing_progress
            )

        # Verify original file is completely intact
        assert os.path.exists(excel_path)
        assert os.path.getsize(excel_path) == original_size
        assert os.path.getmtime(excel_path) == original_mtime
        from repository import ExcelRepository
        df_reg_check, _, _, _, _ = ExcelRepository.load_excel(str(excel_path), config)
        assert list(df_reg_check["ObjectID"]) == ["001", "002"]

        # Verify no orphan temporary files left behind
        tmp_files = [f for f in os.listdir(tmp_path) if ".tmp_" in f]
        assert len(tmp_files) == 0

    def test_permission_error_locked_excel_handling(self, tmp_path):
        """Simulate Windows file lock (PermissionError) when desktop Excel has the file open."""
        from utils import ExcelFileLockedError
        import pytest
        excel_path = tmp_path / "locked_curation.xlsx"
        config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {}
        }
        df_reg = pd.DataFrame({"ObjectID": ["000142"], "Genus": ["Betula"]})
        df_obs = pd.DataFrame({"ObjectID": ["000142"], "Reviewed": [True]})

        with mock.patch("os.replace", side_effect=PermissionError(13, "Permission denied")):
            with pytest.raises(ExcelFileLockedError) as exc_info:
                SQLiteRepository.export_to_excel(None, str(excel_path), config, df_reg=df_reg, df_obs=df_obs)

            # Check that the trainee-friendly error message is surfaced
            msg = str(exc_info.value)
            assert "locked_curation.xlsx" in msg
            assert "currently open in Microsoft Excel or another program" in msg
            assert "Please close Excel and click 'Retry Save'" in msg

        # Ensure temporary file was removed
        tmp_files = [f for f in os.listdir(tmp_path) if ".tmp_" in f]
        assert len(tmp_files) == 0

    def test_presave_backup_rolling_limit(self, tmp_path):
        """Verify automatic pre-save backups in .arbor_backups capped at rolling limit of 5."""
        from utils import create_presave_backup
        excel_path = tmp_path / "rolling_test.xlsx"
        config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {}
        }
        df_reg = pd.DataFrame({"ObjectID": ["1"], "Genus": ["Carex"]})
        df_obs = pd.DataFrame({"ObjectID": ["1"]})

        # Save once to create the file
        SQLiteRepository.export_to_excel(None, str(excel_path), config, df_reg=df_reg, df_obs=df_obs)

        # Trigger 7 backup cycles directly
        for _ in range(7):
            create_presave_backup(str(excel_path), max_backups=5)

        backup_dir = tmp_path / ".arbor_backups"
        assert backup_dir.exists()
        backups = [f for f in os.listdir(backup_dir) if f.startswith("rolling_test.xlsx.") and f.endswith(".bak")]
        assert len(backups) <= 5

    def test_leading_zero_and_data_type_preservation(self, tmp_path):
        """Ensure string accession numbers with leading zeros (e.g. '000142') and booleans are preserved."""
        from repository import ExcelRepository
        excel_path = tmp_path / "accessions.xlsx"
        config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {
                "problems": [{"name": "Genus_Problem"}],
                "location": [{"name": "Cabinet"}],
                "registration": [{"name": "Genus"}]
            }
        }
        raw_ids = ["000142", "000007", "008901", "12345"]
        df_reg = pd.DataFrame({
            "ObjectID": raw_ids,
            "Genus": ["Salix", "Vaccinium", "Empetrum", "Taraxacum"],
            "UID": ["u1", "u2", "u3", "u4"],
            "ProblemDescription": ["", "", "", ""]
        })
        df_obs = pd.DataFrame({
            "ObjectID": raw_ids,
            "Reviewed": [True, False, True, False],
            "ReviewedAt": ["2026-11-13 10:00:00", "", "2026-11-13 11:00:00", ""],
            "Genus_Problem": [False, True, False, False],
            "Images_Missing": [False, True, False, False],
            "Images_Problem": [False, False, False, False],
            "Online_Images_Exist": [False, False, False, False]
        })

        # Save and reload through Arbor's ExcelRepository
        SQLiteRepository.export_to_excel(None, str(excel_path), config, df_reg=df_reg, df_obs=df_obs)
        df_reg_loaded, df_obs_loaded, _, _, _ = ExcelRepository.load_excel(str(excel_path), config)

        # Assert leading zeroes are never coerced to integers
        assert list(df_reg_loaded["ObjectID"]) == raw_ids
        assert list(df_obs_loaded["ObjectID"]) == raw_ids

        # Assert booleans are strictly preserved
        assert list(df_obs_loaded["Reviewed"]) == [True, False, True, False]
        assert list(df_obs_loaded["Genus_Problem"]) == [False, True, False, False]
        assert list(df_obs_loaded["Images_Missing"]) == [False, True, False, False]


# ============================================================================
# Merged from test_loading.py
# ============================================================================

from repository import ExcelRepository
import pandas as pd

class TestLoading:
    def test_loading_excel(self, tmp_path):
        excel_path = tmp_path / "test.xlsx"

        # Create a dummy excel file
        df_reg = pd.DataFrame({"ObjectID": ["1", "2"]})
        df_obs = pd.DataFrame({"ObjectID": ["1", "2"]})

        with pd.ExcelWriter(excel_path) as writer:
            df_reg.to_excel(writer, sheet_name="Registration", index=False)
            df_obs.to_excel(writer, sheet_name="Observation", index=False)

        config = {
            "sheets": {"reg": "Registration", "obs": "Observation"},
            "ui_sections": {
                "problems": [{"name": "Prob1"}],
                "location": [{"name": "Loc1"}],
                "registration": [{"name": "Reg1"}]
            }
        }

        df_reg_out, df_obs_out, df_photo_out, df_log_out, df_unval_out = ExcelRepository.load_excel(excel_path, config)

        assert not df_reg_out.empty
        assert not df_obs_out.empty
        assert list(df_reg_out["ObjectID"]) == ["1", "2"]

    def test_loading_excel_missing_sheets(self, tmp_path):
        excel_path = tmp_path / "test_missing.xlsx"

        # Create a dummy excel file with ONLY Registration
        df_reg = pd.DataFrame({"ObjectID": ["1", "2"]})

        with pd.ExcelWriter(excel_path) as writer:
            df_reg.to_excel(writer, sheet_name="Registration", index=False)

        config = {
            "sheets": {"reg": "Registration", "obs": "Observation", "log": "Log"},
            "ui_sections": {
                "problems": [{"name": "Prob1"}],
                "location": [{"name": "Loc1"}],
                "registration": [{"name": "Reg1"}]
            }
        }

        df_reg_out, df_obs_out, df_photo_out, df_log_out, df_unval_out = ExcelRepository.load_excel(excel_path, config)

        assert not df_reg_out.empty
        assert not df_obs_out.empty
        assert list(df_reg_out["ObjectID"]) == ["1", "2"]
        assert list(df_obs_out["ObjectID"]) == ["1", "2"]
        assert "Prob1" in df_obs_out.columns
        assert "Loc1" in df_obs_out.columns
        assert df_log_out.empty  # Normalised log DataFrame is empty of rows
        assert "Timestamp" in df_log_out.columns

    def test_precompute_startup_caches_clean_object(self):
        from ui.database_ops import DatabaseOpsMixin
        from repository import REVIEWED_COLUMN

        class DummyOps(DatabaseOpsMixin):
            def __init__(self):
                self.problem_columns = ["Genus_Problem", "Other_problem"]
                self.problem_to_field = {"Genus_Problem": "Genus", "Other_problem": "Other"}
                self.image_mode = "online"

        ops = DummyOps()
        df_reg = pd.DataFrame({"Genus": ["Quercus"]}, index=["1"])
        df_obs = pd.DataFrame({REVIEWED_COLUMN: [False], "Genus_Problem": [False], "Other_problem": [False]}, index=["1"])

        ops._precompute_startup_caches(df_reg, df_obs, df_photo=None)
        assert ops._problem_cache["1"] == False


# ============================================================================
# Merged from test_excel_architecture.py
# ============================================================================

import os
import pytest
import pandas as pd
import openpyxl
from unittest import mock
from repository import (
    ExcelRepository,
    SQLiteRepository,
    _normalise_dataframes,
    _coerce_bool_series,
    _normalize_object_id_series,
    _find_sheet_name
)


class TestExcelArchitecture:

    def test_boolean_coercion_edge_cases(self):
        # Truthy cases
        truthy_series = pd.Series(["True", "true", "TRUE", "1", 1, 1.0, "yes", "YES", "y", "t", "on", True])
        coerced_true = _coerce_bool_series(truthy_series, default=False)
        assert coerced_true.all(), "All truthy variants should coerce to True"

        # Falsy cases - CRITICAL: string "False" must NOT be evaluated as truthy
        falsy_series = pd.Series(["False", "false", "FALSE", "0", 0, 0.0, "no", "NO", "n", "f", "off", "", None, False])
        coerced_false = _coerce_bool_series(falsy_series, default=False)
        assert not coerced_false.any(), "All falsy variants should coerce to False"

    def test_object_id_normalization_edge_cases(self):
        # 1024.0 -> "1024", but "1024.1" -> "1024.1", "00123" -> "00123", "  ABC-1  " -> "ABC-1"
        oids = pd.Series([1024, 1025.0, "1026.0", "1027.5", "0042", "  999  ", "O-V-001", None, ""])
        normalized = _normalize_object_id_series(oids)
        assert list(normalized) == ["1024", "1025", "1026", "1027.5", "0042", "999", "O-V-001", "", ""]

    def test_normalise_dataframes_comprehensive(self):
        config = {
            "ui_sections": {
                "registration": [{"name": "Genus"}, {"name": "Species"}, {"name": "UID"}],
                "location": [
                    {"name": "Building", "type": "choice"},
                    {"name": "Loaned out", "type": "checkbox"}
                ],
                "problems": [
                    {"name": "Genus_Problem", "type": "bool", "maps_to": "Genus"}
                ]
            }
        }

        df_reg = pd.DataFrame({
            "ObjectID": [101.0, " 00102 ", "103.5"],
            "Genus": ["Quercus", "Rosa", "Betula"],
            "UID": ["", None, "custom_uid"]
        })

        df_obs = pd.DataFrame({
            "ObjectID": [101.0, "00102", "103.5"],
            "Genus_Problem": ["False", "True", "0"],
            "Loaned out": [1, "false", "yes"],
            "Reviewed": ["no", "yes", "False"]
        })

        df_reg_out, df_obs_out = _normalise_dataframes(df_reg, df_obs, config)

        # Verify ObjectID cleaning
        assert list(df_reg_out["ObjectID"]) == ["101", "00102", "103.5"]
        assert list(df_obs_out["ObjectID"]) == ["101", "00102", "103.5"]

        # Verify UID generation
        assert len(df_reg_out.loc[0, "UID"]) == 8
        assert len(df_reg_out.loc[1, "UID"]) == 8
        assert df_reg_out.loc[2, "UID"] == "custom_uid"

        # Verify Problem boolean coercion
        assert df_obs_out.loc[0, "Genus_Problem"] == False
        assert df_obs_out.loc[1, "Genus_Problem"] == True
        assert df_obs_out.loc[2, "Genus_Problem"] == False
        assert df_obs_out["Genus_Problem"].dtype == bool

        # Verify Location Checkbox string contract ("True"/"False")
        assert df_obs_out.loc[0, "Loaned out"] == "True"
        assert df_obs_out.loc[1, "Loaned out"] == "False"
        assert df_obs_out.loc[2, "Loaned out"] == "True"

        # Verify Reviewed boolean coercion
        assert df_obs_out.loc[0, "Reviewed"] == False
        assert df_obs_out.loc[1, "Reviewed"] == True
        assert df_obs_out.loc[2, "Reviewed"] == False

    def test_find_sheet_name_case_and_whitespace(self):
        sheets = ["Registration ", "OBSERVATION", "Photo", "Log_Sheet"]
        assert _find_sheet_name(sheets, "registration") == "Registration "
        assert _find_sheet_name(sheets, "observation") == "OBSERVATION"
        assert _find_sheet_name(sheets, "Photo") == "Photo"
        assert _find_sheet_name(sheets, "NonExistent") is None

    def test_export_and_import_with_photo_sheet_and_styling(self, tmp_path):
        excel_path = str(tmp_path / "styled_export.xlsx")

        config = {
            "sheets": {
                "reg": "Registration",
                "obs": "Observation",
                "photo": "Photo",
                "log": "Log"
            },
            "ui_sections": {
                "registration": [{"name": "Genus"}],
                "location": [],
                "problems": [{"name": "Genus_Problem"}]
            }
        }

        df_reg = pd.DataFrame({"ObjectID": ["1", "2"], "Genus": ["Quercus", "Pinus"], "UID": ["u1", "u2"]})
        df_obs = pd.DataFrame({"ObjectID": ["1", "2"], "Genus_Problem": [False, True]})
        df_photo = pd.DataFrame({"ObjectID": ["1", "1", "2"], "Filename": ["img1.jpg", "img2.jpg", "img3.jpg"]})
        df_log = pd.DataFrame({"Timestamp": ["2026-08-17 12:00:00"], "Action": ["TEST"], "ObjectID": ["1"]})

        # Export to Excel
        SQLiteRepository.export_to_excel(
            sqlite_path=None,
            excel_path=excel_path,
            config=config,
            df_reg=df_reg,
            df_obs=df_obs,
            df_log=df_log,
            df_photo=df_photo
        )

        assert os.path.exists(excel_path)

        # Inspect with openpyxl for freeze_panes and auto_filter
        wb = openpyxl.load_workbook(excel_path)
        assert set(wb.sheetnames) == {"Registration", "Observation", "Photo", "Log"}

        ws_reg = wb["Registration"]
        assert ws_reg.freeze_panes == "A2"
        assert ws_reg.auto_filter.ref is not None
        assert ws_reg.column_dimensions["A"].width >= 10

        # Load back with ExcelRepository and verify data integrity
        df_reg_in, df_obs_in, df_photo_in, df_log_in, df_unval_in = ExcelRepository.load_excel(excel_path, config)
        assert list(df_reg_in["ObjectID"]) == ["1", "2"]
        assert list(df_obs_in["ObjectID"]) == ["1", "2"]
        assert list(df_photo_in["ObjectID"]) == ["1", "1", "2"]
        assert list(df_photo_in["Filename"]) == ["img1.jpg", "img2.jpg", "img3.jpg"]
        assert len(df_log_in) == 1

    def test_permission_error_handling_on_export(self, tmp_path):
        excel_path = str(tmp_path / "locked.xlsx")
        config = {"sheets": {}, "ui_sections": {}}
        df_reg = pd.DataFrame({"ObjectID": ["1"]})
        df_obs = pd.DataFrame({"ObjectID": ["1"]})

        with mock.patch("os.replace", side_effect=PermissionError("File locked by Excel")):
            with pytest.raises(PermissionError) as exc_info:
                SQLiteRepository.export_to_excel(
                    sqlite_path=None,
                    excel_path=excel_path,
                    config=config,
                    df_reg=df_reg,
                    df_obs=df_obs
                )
            assert "open in Microsoft Excel" in str(exc_info.value)
            # Ensure no orphan tmp file matching .tmp.xlsx remains
            remaining_tmps = [f for f in os.listdir(str(tmp_path)) if f.endswith(".tmp.xlsx")]
            assert len(remaining_tmps) == 0

    def test_scientific_notation_and_formula_errors_in_object_id(self):
        from repository import _normalize_object_id_series
        # Scientific notation: 1E+05 -> 100000, 1.0e+05 -> 100000, 1.5e3 -> 1500
        # Preserving leading zeros: "00123" -> "00123"
        # Alphanumeric: "BOT-1E5" -> "BOT-1E5"
        # Formula errors: "#REF!", "#VALUE!" -> ""
        oids = pd.Series(["1E+05", "1.0E+05", "1e5", "1.5e3", "00123", "BOT-1E5", "#REF!", "#VALUE!", None])
        res = list(_normalize_object_id_series(oids))
        assert res == ["100000", "100000", "100000", "1500", "00123", "BOT-1E5", "", "", ""]

    def test_header_promotion_and_blank_columns(self):
        from repository import _detect_and_promote_header, _clean_trailing_and_blank_columns
        # DataFrame with leading title row and blank row before real header
        raw_data = [
            ["Museum Specimen Database 2026", None, None],
            [None, None, None],
            ["ObjectID", "Genus", "Unnamed: 2"],
            ["1001", "Quercus", None],
            ["1002", "Pinus", None],
            [None, None, None]  # Trailing ghost row
        ]
        df = pd.DataFrame(raw_data)
        df_promoted = _detect_and_promote_header(df, "ObjectID")
        assert "ObjectID" in df_promoted.columns
        assert "Genus" in df_promoted.columns

        df_cleaned = _clean_trailing_and_blank_columns(df_promoted)
        assert "Unnamed: 2" not in df_cleaned.columns
        assert len(df_cleaned) == 2
        assert list(df_cleaned["ObjectID"]) == ["1001", "1002"]

    def test_duplicate_column_deduplication(self):
        from repository import _deduplicate_columns
        from utils import sanitize_df_for_excel
        import sqlite3

        df_dups = pd.DataFrame([["val1", "val2", "val3"]], columns=["Comment", "Comment", "Comment"])
        deduped = _deduplicate_columns(df_dups)
        assert list(deduped.columns) == ["Comment", "Comment.1", "Comment.2"]

        # sanitize_df_for_excel should not crash on duplicate columns
        safe_df = sanitize_df_for_excel(df_dups)
        assert safe_df is not None

        # SQLite to_sql should succeed with deduplicated columns
        conn = sqlite3.connect(":memory:")
        deduped.to_sql("test_table", conn, index=False)
        read_back = pd.read_sql("SELECT * FROM test_table", conn)
        assert len(read_back) == 1


# ============================================================================
# Merged from test_audit_log_lifecycle.py
# ============================================================================

import os
import tempfile
import pytest
import pandas as pd
from unittest.mock import MagicMock
from models import AppState
from repository import ExcelRepository, SQLiteRepository, _normalise_log_dataframe
import config


def test_normalise_log_dataframe_canonical_columns():
    # Test normalization of empty and incomplete log dataframes
    empty_df = pd.DataFrame()
    norm_empty = _normalise_log_dataframe(empty_df)
    expected_cols = [
        "Timestamp", "Action", "Reviewed", "ObjectID", "ChangedFields",
        "ChangedValues", "ProblemsChanged", "ProblemsChangedValues",
        "LocationChanged", "LocationChangedValues", "User", "SourceFile", "OutputFile"
    ]
    assert list(norm_empty.columns) == expected_cols
    assert norm_empty.empty

    partial_df = pd.DataFrame([{
        "Timestamp": "2026-09-03T10:00:00",
        "Action": "EDIT",
        "ObjectID": "1001",
        "ChangedFields": "Species"
    }])
    norm_partial = _normalise_log_dataframe(partial_df)
    assert set(norm_partial.columns) == set(expected_cols)
    assert len(norm_partial.columns) == len(expected_cols)
    assert norm_partial.at[0, "ChangedFields"] == "Species"
    assert norm_partial.at[0, "User"] == ""


def test_excel_sqlite_log_roundtrip_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        excel_path = os.path.join(tmpdir, "test_roundtrip.xlsx")
        sqlite_path = os.path.join(tmpdir, "test_roundtrip.db")

        df_reg = pd.DataFrame([{"ObjectID": "1001", "Genus": "Quercus", "Species": "robur"}]).set_index("ObjectID")
        df_obs = pd.DataFrame([{"ObjectID": "1001", "Reviewed": True, "Location": "Shelf A"}]).set_index("ObjectID")
        df_photo = pd.DataFrame(columns=["ObjectID", "ImagePath", "ImageNote"]).set_index("ObjectID")
        df_unval = pd.DataFrame([{"ObjectID": "1001", "Field_Name": "Collector", "Unvalidated_Comment": "Needs verification"}])
        
        raw_log = pd.DataFrame([{
            "Timestamp": "2026-09-03T10:00:00",
            "Action": "EDIT",
            "Reviewed": "Yes",
            "ObjectID": "1001",
            "ChangedFields": "Species",
            "ChangedValues": 'Species: "petraea" -> "robur"',
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "Location",
            "LocationChangedValues": "Shelf A",
            "User": "admin",
            "SourceFile": "test_roundtrip.xlsx",
            "OutputFile": "test_roundtrip.xlsx"
        }])
        df_log = _normalise_log_dataframe(raw_log)

        cfg = config.DATABASE_CONFIGS["Økonomisk Botanisk"]

        # 1. Save to Excel
        ExcelRepository.save_excel(excel_path, cfg, df_reg=df_reg, df_obs=df_obs, df_photo=df_photo, df_log=df_log, df_unvalidated=df_unval)
        assert os.path.exists(excel_path)

        # 2. Import Excel to SQLite via SQLiteRepository.import_from_excel
        SQLiteRepository.import_from_excel(excel_path, sqlite_path, cfg)
        assert os.path.exists(sqlite_path)

        # 3. Load from SQLite
        l_reg, l_obs, l_photo, l_log, l_unval = SQLiteRepository.load_sqlite(sqlite_path, cfg)
        assert len(l_log) == 1
        assert l_log.at[0, "Action"] == "EDIT"
        assert str(l_log.at[0, "ObjectID"]) == "1001"
        assert l_log.at[0, "ChangedValues"] == 'Species: "petraea" -> "robur"'
        assert len(l_unval) == 1
        assert l_unval.at[0, "Field_Name"] == "Collector"

        # 4. Export SQLite back to Excel
        excel_out = os.path.join(tmpdir, "exported_back.xlsx")
        SQLiteRepository.export_to_excel(sqlite_path, excel_out, cfg, df_unvalidated=df_unval)
        assert os.path.exists(excel_out)

        # 5. Load exported Excel
        e_reg, e_obs, e_photo, e_log, e_unval = ExcelRepository.load_excel(excel_out, cfg)
        assert len(e_log) == 1
        assert e_log.at[0, "ChangedFields"] == "Species"
        assert len(e_unval) == 1


def test_import_to_sqlite_and_save_as_integration():
    app = AppState()
    app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
    app.excel_path = "test.xlsx"
    app.output_path = "test.xlsx"
    app.df_reg = pd.DataFrame([{"ObjectID": "1", "Genus": "Pinus"}]).set_index("ObjectID")
    app.df_obs = pd.DataFrame([{"ObjectID": "1", "Reviewed": False}]).set_index("ObjectID")
    app.df_photo = pd.DataFrame(columns=["ObjectID", "ImagePath"]).set_index("ObjectID")
    app.df_log = pd.DataFrame([{
        "Timestamp": "2026-09-03T10:00:00", "Action": "EDIT", "Reviewed": "No", "ObjectID": "1",
        "ChangedFields": "Genus", "ChangedValues": 'Genus: "" -> "Pinus"',
        "ProblemsChanged": "", "ProblemsChangedValues": "",
        "LocationChanged": "", "LocationChangedValues": "",
        "User": "tester", "SourceFile": "test.xlsx", "OutputFile": "test.xlsx"
    }])
    app.df_unvalidated = pd.DataFrame([{"ObjectID": "1", "Field_Name": "Genus", "Unvalidated_Comment": "Auto"}])
    app._log_records = app.df_log.to_dict(orient="records")

    with tempfile.TemporaryDirectory() as tmpdir:
        test_xl = os.path.join(tmpdir, "test.xlsx")
        dest_db = os.path.join(tmpdir, "imported.db")
        ExcelRepository.save_excel(test_xl, app.config, df_reg=app.df_reg, df_obs=app.df_obs, df_photo=app.df_photo, df_log=app.df_log, df_unvalidated=app.df_unvalidated)
        
        # Test import to sqlite flow
        SQLiteRepository.import_from_excel(test_xl, dest_db, app.config)
        df_reg, df_obs, df_photo, df_log, df_unvalidated = SQLiteRepository.load_sqlite(dest_db, app.config)
        
        app.excel_path = dest_db
        app.df_reg = df_reg
        app.df_obs = df_obs
        app.df_photo = df_photo
        app.df_log = df_log
        app.df_unvalidated = df_unvalidated
        app._log_records = df_log.to_dict(orient="records")

        assert app.excel_path == dest_db
        assert len(app._log_records) == 1
        assert app._log_records[0]["Action"] == "EDIT"
        assert app.df_unvalidated is not None
        assert len(app.df_unvalidated) == 1


def test_sqlite_strict_schema_log_save_with_session_id():
    import sqlite3
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "strict_log_test.db")
        conn = sqlite3.connect(db_path)
        canonical_cols = [
            "Timestamp", "Action", "Reviewed", "ObjectID",
            "ChangedFields", "ChangedValues",
            "ProblemsChanged", "ProblemsChangedValues",
            "LocationChanged", "LocationChangedValues",
            "User", "SourceFile", "OutputFile"
        ]
        col_defs = ", ".join([f'"{col}" TEXT' for col in canonical_cols])
        conn.execute(f'CREATE TABLE "Log" ({col_defs});')
        conn.execute('CREATE TABLE "Registration" ("ObjectID" TEXT, "Genus" TEXT);')
        conn.execute('CREATE TABLE "Observation" ("ObjectID" TEXT, "Reviewed" BOOLEAN);')
        conn.commit()
        conn.close()

        df_reg = pd.DataFrame([{"ObjectID": "101", "Genus": "Quercus"}]).set_index("ObjectID")
        df_obs = pd.DataFrame([{"ObjectID": "101", "Reviewed": True}]).set_index("ObjectID")
        df_photo = pd.DataFrame()
        df_log = pd.DataFrame([{
            "Timestamp": "2026-09-03T12:00:00",
            "Action": "MOBILE_EDIT",
            "Reviewed": "Yes",
            "ObjectID": "101",
            "ChangedFields": "Genus",
            "ChangedValues": 'Genus: "Fagus" -> "Quercus"',
            "ProblemsChanged": "",
            "ProblemsChangedValues": "",
            "LocationChanged": "",
            "LocationChangedValues": "",
            "User": "Mobile-Companion",
            "SourceFile": "test.db",
            "OutputFile": "test.db",
            "_session_id": "session_abc123"
        }])

        SQLiteRepository.save_sqlite(db_path, df_reg, df_obs, df_photo, df_log)
        df_read_log = SQLiteRepository.load_sqlite(db_path, {"ui_sections": {}})[3]
        assert len(df_read_log) == 1
        assert "_session_id" not in df_read_log.columns
        assert df_read_log.iloc[0]["Action"] == "MOBILE_EDIT"


def test_concurrent_log_action_thread_safety():
    import threading
    from models import AppState
    from ui.main_window import ObjectProgramUI
    from unittest.mock import MagicMock

    app = AppState()
    app.config = config.DATABASE_CONFIGS["Økonomisk Botanisk"]
    app.df_reg = pd.DataFrame([{"ObjectID": f"{i}", "Genus": "Pinus"} for i in range(100)]).set_index("ObjectID")
    app.df_obs = pd.DataFrame([{"ObjectID": f"{i}", "Reviewed": False} for i in range(100)]).set_index("ObjectID")
    app.df_photo = pd.DataFrame(columns=["ObjectID", "ImagePath"]).set_index("ObjectID")
    app.df_log = pd.DataFrame()
    app._log_records = []

    mock_ui = MagicMock()
    mock_ui.app = app
    mock_ui.log_action = ObjectProgramUI.log_action.__get__(mock_ui, MagicMock)

    errors = []
    def worker(worker_id):
        try:
            for i in range(25):
                oid = f"{(worker_id * 25 + i) % 100}"
                mock_ui.log_action(
                    "EDIT",
                    changed_fields=["Genus"],
                    changed_values=[f'Genus: "Pinus" -> "Pinus_{worker_id}_{i}"'],
                    oid=oid
                )
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(app._log_records) == 100
    assert len(app.df_log) == 100
