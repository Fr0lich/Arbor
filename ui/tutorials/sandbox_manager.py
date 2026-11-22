"""
ui/tutorials/sandbox_manager.py

Manages entering and exiting isolated in-memory sandbox environments for tutorials.
Ensures zero mutations to user files by snapshotting existing session state and
restoring it upon tutorial exit or completion.
"""

import copy
import pandas as pd
import config
from utils import debug_error


class SandboxManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SandboxManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.is_sandboxed = False
            self._current_mock_type = None
            self.snapshot = None
            self._practice_banner = None
            self._active_runner = None

    def enter_sandbox(self, ui, mock_type="review"):
        """Snapshots the active state (if not already sandboxed) and loads isolated mock data."""
        try:
            app = ui.app
            if not self.is_sandboxed:
                # 1. Snapshot existing real session state once
                self.snapshot = {
                    "config": copy.deepcopy(app.config) if app.config else None,
                    "config_name": app.config_name,
                    "excel_path": app.excel_path,
                    "output_path": app.output_path,
                    "df_reg": app.df_reg.copy() if app.df_reg is not None else None,
                    "df_obs": app.df_obs.copy() if app.df_obs is not None else None,
                    "df_photo": app.df_photo.copy() if app.df_photo is not None else None,
                    "df_log": app.df_log.copy() if app.df_log is not None else None,
                    "df_unvalidated": app.df_unvalidated.copy() if app.df_unvalidated is not None else None,
                    "historical_dbs": copy.deepcopy(app.historical_dbs),
                    "dirty": app.dirty,
                    "current_object_id": app.current_object_id,
                }
            elif getattr(self, "_current_mock_type", None) == mock_type:
                return

            self._current_mock_type = mock_type

            # 2. Build mock DataFrames according to standard DB config
            cfg = app.config or config.DATABASE_CONFIGS.get("Standard", list(config.DATABASE_CONFIGS.values())[0])
            app.config = cfg

            mock_reg, mock_obs, mock_photo, mock_log, mock_unval, mock_hist = self._create_mock_datasets(mock_type)

            self.is_sandboxed = True

            # 3. Apply mock dataset in UI
            ui._precompute_startup_caches(mock_reg, mock_obs, mock_photo)
            ui._finish_open_excel(
                "[Tutorial Sandbox]",
                "[Tutorial Sandbox]",
                mock_reg,
                mock_obs,
                mock_photo,
                mock_log,
                mock_unval
            )

            # Inject mock historical discrepancy data if needed
            if mock_hist:
                app.historical_dbs = mock_hist
                if hasattr(ui, "_history_cache"):
                    ui._history_cache.clear()

            # Select first mock specimen
            if mock_reg is not None and not mock_reg.empty:
                first_id = str(mock_reg.index[0])
                ui.current_id = first_id
                ui.app.current_object_id = first_id
                if hasattr(ui, "object_list"):
                    try:
                        ui.object_list.select_by_id(first_id)
                    except Exception:
                        pass
                if hasattr(ui, "load_object"):
                    try:
                        ui.load_object(first_id)
                    except Exception:
                        pass
                if hasattr(ui, "update_history_indicator"):
                    try:
                        ui.update_history_indicator(first_id)
                    except Exception:
                        pass

            self._show_practice_banner(ui)

        except Exception as e:
            debug_error("SandboxManager.enter_sandbox", str(e))

    def _show_practice_banner(self, ui):
        """Mount a persistent zero-fear Practice Mode banner at the top of the window."""
        self._hide_practice_banner()
        root = getattr(ui, "root", None)
        if root is None:
            return
        try:
            import tkinter as tk
            from config import sc
            if not root.winfo_exists():
                return
            banner = tk.Frame(root, bg="#1e4620", padx=sc(12), pady=sc(5))
            # Pack at the very top before existing children if any
            children = root.winfo_children()
            packed_children = [c for c in children if c is not banner and c.winfo_manager() == "pack"]
            if packed_children:
                banner.pack(side="top", fill="x", before=packed_children[0])
            else:
                banner.pack(side="top", fill="x")

            tk.Label(
                banner,
                text="🛡️ PRACTICE MODE — Nothing you do here affects real museum files. Saving is safely paused.",
                font=("Segoe UI", sc(9), "bold"),
                bg="#1e4620",
                fg="#d8f5dc",
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            def _exit_now():
                runner = getattr(self, "_active_runner", None)
                if runner is not None and hasattr(runner, "exit_tutorial"):
                    runner.exit_tutorial()
                else:
                    self.exit_sandbox(ui)

            tk.Button(
                banner,
                text="Exit Practice Mode",
                font=("Segoe UI", sc(8.5), "bold"),
                bg="#2e6b32",
                fg="#ffffff",
                activebackground="#3a7d44",
                activeforeground="#ffffff",
                relief="flat",
                cursor="hand2",
                padx=sc(8),
                pady=sc(2),
                command=_exit_now,
            ).pack(side="right")
            self._practice_banner = banner
        except Exception:
            self._practice_banner = None

    def _hide_practice_banner(self):
        banner = getattr(self, "_practice_banner", None)
        if banner is not None:
            try:
                if banner.winfo_exists():
                    banner.destroy()
            except Exception:
                pass
        self._practice_banner = None
        self._active_runner = None

    def exit_sandbox(self, ui):
        """Restores the original workspace state from snapshot."""
        if not self.is_sandboxed:
            return

        try:
            self._hide_practice_banner()
            self.is_sandboxed = False
            self._current_mock_type = None
            if not self.snapshot:
                return

            snap = self.snapshot
            self.snapshot = None

            app = ui.app
            app.config = snap["config"]
            app.config_name = snap["config_name"]
            app.historical_dbs = snap["historical_dbs"]
            app.dirty = snap["dirty"]

            if snap["df_reg"] is not None and snap["df_obs"] is not None:
                ui._precompute_startup_caches(snap["df_reg"], snap["df_obs"], snap["df_photo"])
                ui._finish_open_excel(
                    snap["excel_path"] or "",
                    snap["output_path"] or "",
                    snap["df_reg"],
                    snap["df_obs"],
                    snap["df_photo"],
                    snap["df_log"],
                    snap["df_unvalidated"]
                )
                if snap["current_object_id"]:
                    oid = snap["current_object_id"]
                    ui.current_id = oid
                    ui.app.current_object_id = oid
                    if hasattr(ui, "object_list"):
                        try:
                            ui.object_list.select_by_id(oid)
                        except Exception:
                            pass
                    if hasattr(ui, "load_object"):
                        try:
                            ui.load_object(oid)
                        except Exception:
                            pass
            else:
                app.excel_path = snap["excel_path"]
                app.output_path = snap["output_path"]
                app.df_reg = None
                app.df_obs = None
                app.df_photo = None
                app.df_log = None
                app.df_unvalidated = None
                app.current_object_id = None
                ui.current_id = None
                if hasattr(ui, "refresh_list"):
                    try:
                        ui.refresh_list()
                    except Exception:
                        pass
                if hasattr(ui, "reset_object_editor"):
                    try:
                        ui.reset_object_editor()
                    except Exception:
                        pass

        except Exception as e:
            debug_error("SandboxManager.exit_sandbox", str(e))

    def _create_mock_datasets(self, mock_type):
        """Creates sample in-memory DataFrames matching Arbor's real workbook columns."""
        reg_data = [
            {
                "ObjectID": "1001",
                "Genus": "Betula",
                "Species": "nana",
                "Taxon": "Betula nana",
                "Family": "Betulaceae",
                "Author": "L.",
                "Collector": "E. Dahl",
                "CollectorNumber": "142",
                "Collection Date": "1965-07-15",
                "Year": "1965",
                "Collection Place": "Dovrefjell, Kongsvoll",
                "Locality": "Dovrefjell, Kongsvoll",
                "Country": "Norway",
                "Reviewed": False,
                "Reviewed_By": "",
                "Reviewed_At": "",
                "Problem_Flags": ""
            },
            {
                "ObjectID": "1002",
                "Genus": "Pinus",
                "Species": "sylvestris",
                "Taxon": "Pinus sylvestris",
                "Family": "Pinaceae",
                "Author": "L.",
                "Collector": "J. M. Norman",
                "CollectorNumber": "89",
                "Collection Date": "2008",
                "Year": "2008",
                "Collection Place": "Alvdal, Hedmark",
                "Locality": "Alvdal, Hedmark",
                "Country": "Norway",
                "Reviewed": False,
                "Reviewed_By": "",
                "Reviewed_At": "",
                "Problem_Flags": "Collection_Date_Problem"
            },
            {
                "ObjectID": "1003",
                "Genus": "Salix",
                "Species": "herbacea",
                "Taxon": "Salix herbacea",
                "Family": "Salicaceae",
                "Author": "L.",
                "Collector": "R. F. Fristedt",
                "CollectorNumber": "304",
                "Collection Date": "1853-06-22",
                "Year": "1853",
                "Collection Place": "Jotunheimen",
                "Locality": "Jotunheimen",
                "Country": "Norway",
                "Reviewed": True,
                "Reviewed_By": "Curator",
                "Reviewed_At": "2026-01-10 14:30:00",
                "Problem_Flags": ""
            }
        ]

        obs_data = [
            {
                "ObjectID": "1001",
                "Reviewed": False,
                "ReviewedAt": "",
                "Building": "Lid's hus",
                "Floor": "1",
                "Cabinet": "21",
                "Shelf": "01",
                "Stored as": "Box",
                "Genus_Problem": False,
                "Species_Problem": False,
                "Collection_Date_Problem": False,
                "Box_Label_Problem": False,
                "Taxon_Mismatch": False,
                "Coordinate_Problem": False,
                "Unidentified": False
            },
            {
                "ObjectID": "1002",
                "Reviewed": False,
                "ReviewedAt": "",
                "Building": "Lid's hus",
                "Floor": "1",
                "Cabinet": "21",
                "Shelf": "01",
                "Stored as": "Box",
                "Genus_Problem": False,
                "Species_Problem": False,
                "Collection_Date_Problem": True,
                "Box_Label_Problem": False,
                "Taxon_Mismatch": True,
                "Coordinate_Problem": False,
                "Unidentified": False
            },
            {
                "ObjectID": "1003",
                "Reviewed": True,
                "ReviewedAt": "10.01.2026 14:30",
                "Building": "Lid's hus",
                "Floor": "1",
                "Cabinet": "21",
                "Shelf": "01",
                "Stored as": "Box",
                "Genus_Problem": False,
                "Species_Problem": False,
                "Collection_Date_Problem": False,
                "Box_Label_Problem": False,
                "Taxon_Mismatch": False,
                "Coordinate_Problem": False,
                "Unidentified": False
            }
        ]

        if mock_type == "triage":
            reg_data = [
                {
                    "ObjectID": "2001",
                    "Genus": "Betula",
                    "Species": "pendula",
                    "Taxon": "Betula pendula",
                    "Family": "Betulaceae",
                    "Author": "Roth",
                    "Collector": "N. Moe",
                    "CollectorNumber": "41",
                    "Collection Date": "1954",
                    "Year": "1954",
                    "Collection Place": "Oslo, Tøyen",
                    "Locality": "Oslo, Tøyen",
                    "Country": "Norway",
                    "Reviewed": True,
                    "Reviewed_By": "Hallway Intern",
                    "Reviewed_At": "2026-11-20 10:15:00",
                    "Problem_Flags": "Box_Label_Problem",
                },
                {
                    "ObjectID": "2002",
                    "Genus": "Pinus",
                    "Species": "sylvestris",
                    "Taxon": "Pinus sylvestris",
                    "Family": "Pinaceae",
                    "Author": "L.",
                    "Collector": "J. Lid",
                    "CollectorNumber": "88",
                    "Collection Date": "1972",
                    "Year": "1972",
                    "Collection Place": "Dovrefjell",
                    "Locality": "Dovrefjell",
                    "Country": "Norway",
                    "Reviewed": True,
                    "Reviewed_By": "Hallway Intern",
                    "Reviewed_At": "2026-11-20 10:18:00",
                    "Problem_Flags": "Collection_Date_Problem",
                },
                {
                    "ObjectID": "2003",
                    "Genus": "Salix",
                    "Species": "caprea",
                    "Taxon": "Salix caprea",
                    "Family": "Salicaceae",
                    "Author": "L.",
                    "Collector": "O. Dahl",
                    "CollectorNumber": "12",
                    "Collection Date": "1921",
                    "Year": "1921",
                    "Collection Place": "Bergen",
                    "Locality": "Bergen",
                    "Country": "Norway",
                    "Reviewed": True,
                    "Reviewed_By": "Hallway Intern",
                    "Reviewed_At": "2026-11-20 10:20:00",
                    "Problem_Flags": "",
                },
            ]
            obs_data = [
                {
                    "ObjectID": "2001",
                    "Reviewed": True,
                    "ReviewedAt": "20.11.2026 10:15",
                    "Building": "Lid's hus",
                    "Floor": "1",
                    "Cabinet": "21",
                    "Shelf": "01",
                    "Stored as": "Box",
                    "Genus_Problem": False,
                    "Species_Problem": False,
                    "Collection_Date_Problem": False,
                    "Box_Label_Problem": True,
                    "Taxon_Mismatch": False,
                    "Coordinate_Problem": False,
                    "Unidentified": False,
                },
                {
                    "ObjectID": "2002",
                    "Reviewed": True,
                    "ReviewedAt": "20.11.2026 10:18",
                    "Building": "Lid's hus",
                    "Floor": "1",
                    "Cabinet": "21",
                    "Shelf": "01",
                    "Stored as": "Box",
                    "Genus_Problem": False,
                    "Species_Problem": False,
                    "Collection_Date_Problem": True,
                    "Box_Label_Problem": False,
                    "Taxon_Mismatch": False,
                    "Coordinate_Problem": False,
                    "Unidentified": False,
                },
                {
                    "ObjectID": "2003",
                    "Reviewed": True,
                    "ReviewedAt": "20.11.2026 10:20",
                    "Building": "Lid's hus",
                    "Floor": "1",
                    "Cabinet": "21",
                    "Shelf": "01",
                    "Stored as": "Box",
                    "Genus_Problem": False,
                    "Species_Problem": False,
                    "Collection_Date_Problem": False,
                    "Box_Label_Problem": False,
                    "Taxon_Mismatch": False,
                    "Coordinate_Problem": False,
                    "Unidentified": False,
                },
            ]
            df_reg = pd.DataFrame(reg_data).set_index("ObjectID", drop=False)
            df_obs = pd.DataFrame(obs_data).set_index("ObjectID", drop=False)
            df_photo = pd.DataFrame(columns=["ObjectID", "PhotoURL", "PhotoType"])
            df_log = pd.DataFrame(columns=["Timestamp", "ObjectID", "Action", "User"])
            df_unval = pd.DataFrame()
            return df_reg, df_obs, df_photo, df_log, df_unval, []

        df_reg = pd.DataFrame(reg_data).set_index("ObjectID", drop=False)
        df_obs = pd.DataFrame(obs_data).set_index("ObjectID", drop=False)
        df_photo = pd.DataFrame(columns=["ObjectID", "PhotoURL", "PhotoType"])
        df_log = pd.DataFrame(columns=["Timestamp", "ObjectID", "Action", "User"])
        df_unval = pd.DataFrame()

        mock_hist = []
        if mock_type in ("discrepancy", "review"):
            hist_books = pd.DataFrame([
                {
                    "ObjectID": "1001",
                    "Taxon": "Betula pendula",
                    "Author": "Roth",
                    "Family": "Betulaceae",
                    "Collection Place": "Dovre, Kongsvold",
                    "Locality": "Dovre, Kongsvold",
                    "Collection Date": "1965",
                    "Year": "1965"
                },
                {
                    "ObjectID": "1002",
                    "Genus": "Pinus",
                    "Species": "sylvestris",
                    "Taxon": "Pinus sylvestris",
                    "Family": "Pinaceae",
                    "Collection Date": "1998",
                    "Year": "1998",
                    "Collection Place": "Alvdal, Hedmark"
                }
            ]).set_index("ObjectID", drop=False)

            mock_hist.append({
                "name": "Historical Ledger Book 1",
                "df": hist_books
            })

        return df_reg, df_obs, df_photo, df_log, df_unval, mock_hist
