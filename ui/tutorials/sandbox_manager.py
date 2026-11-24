"""
ui/tutorials/sandbox_manager.py

Manages entering and exiting isolated in-memory sandbox environments for tutorials.
Ensures zero mutations to user files by snapshotting existing session state and
restoring it upon tutorial exit or completion.
"""

import copy
import os
import sys
import pandas as pd
import config
from utils import debug_error


def get_completed_tutorials() -> set:
    """Return the set of completed tutorial IDs persisted in user preferences."""
    try:
        prefs = config.load_prefs() or {}
        done = prefs.get("completed_tutorials", [])
        if isinstance(done, list):
            return set(str(x) for x in done)
    except Exception:
        pass
    return set()


def mark_tutorial_completed(tutorial_id: str) -> None:
    """Persist a completed tutorial ID to user preferences safely."""
    if not tutorial_id:
        return
    try:
        prefs = config.load_prefs() or {}
        done = list(prefs.get("completed_tutorials", []) or [])
        if tutorial_id not in done:
            done.append(tutorial_id)
            prefs["completed_tutorials"] = done
            config.save_prefs(prefs)
    except Exception:
        pass


def _resolve_tutorial_images_dir() -> str | None:
    """Locate bundled data/tutorial_images across source runs and PyInstaller builds."""
    candidates = []
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
        candidates.append(os.path.join(exe_dir, "data", "tutorial_images"))
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(os.path.join(meipass, "data", "tutorial_images"))
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    candidates.append(os.path.join(repo_root, "data", "tutorial_images"))
    candidates.append(os.path.join(os.getcwd(), "data", "tutorial_images"))
    for cand in candidates:
        if os.path.isdir(cand):
            return cand
    return None


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
                # 1. Snapshot existing real session state once (including image panel state)
                img_panel = getattr(ui, "image_panel", None)
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
                    "image_mode": getattr(img_panel, "image_mode", None) if img_panel else None,
                    "image_folder": getattr(img_panel, "image_folder", None) if img_panel else None,
                    "image_index": copy.deepcopy(getattr(img_panel, "image_index", {})) if img_panel else {},
                    "show_images": bool(img_panel.show_images_var.get()) if (img_panel and getattr(img_panel, "show_images_var", None) is not None) else True,
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
            app.historical_dbs = mock_hist if mock_hist else []
            if hasattr(ui, "_history_cache"):
                ui._history_cache.clear()

            # Mount bundled real tutorial photos for #110 and #198 in the Quick Tour sandbox
            img_panel = getattr(ui, "image_panel", None)
            if mock_type == "review" and img_panel is not None:
                tut_img_dir = _resolve_tutorial_images_dir()
                if tut_img_dir:
                    tut_index = {}
                    for oid_key, patterns in [
                        ("110", ("O-V-OE-0110-01.jpg", "O-V-OE-110-02.jpg")),
                        ("198", ("O-V-OE-0198-01.jpg", "O-V-OE-0198-02.jpg")),
                    ]:
                        found = [
                            os.path.join(tut_img_dir, fn)
                            for fn in patterns
                            if os.path.isfile(os.path.join(tut_img_dir, fn))
                        ]
                        if found:
                            tut_index[oid_key] = found
                    if tut_index:
                        img_panel.image_mode = "folder"
                        img_panel.image_folder = tut_img_dir
                        img_panel.image_index = tut_index
                        if getattr(img_panel, "show_images_var", None) is not None:
                            img_panel.show_images_var.set(True)
                        if hasattr(ui, "_sync_middle_panes"):
                            try:
                                ui._sync_middle_panes()
                            except Exception:
                                pass

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

            # Restore image panel state before reloading the real workspace
            img_panel = getattr(ui, "image_panel", None)
            if img_panel is not None:
                img_panel.image_mode = snap.get("image_mode")
                img_panel.image_folder = snap.get("image_folder")
                img_panel.image_index = copy.deepcopy(snap.get("image_index", {}))
                if getattr(img_panel, "show_images_var", None) is not None:
                    img_panel.show_images_var.set(bool(snap.get("show_images", True)))
                if hasattr(ui, "_sync_middle_panes"):
                    try:
                        ui._sync_middle_panes()
                    except Exception:
                        pass

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
        if mock_type == "review":
            reg_data = [
                {
                    "ObjectID": "110",
                    "Object Number": "110",
                    "UID": "e1566f8d",
                    "Genus": "Ephedra",
                    "Species": "major",
                    "Taxon": "Ephedra major",
                    "Author": "Host",
                    "Family": "Ephedraceae",
                    "Higher Classification": "46",
                    "(N) Plant Part": "Greiner med blad og hannblomster",
                    "Plant Part": "branches with leaves and male flowers",
                    "Collector": "Vicioso",
                    "Innsammling Nr.": "",
                    "Collection Date": "",  # Intentionally blank for Step 1 (label says "juni 1910" -> 00.06.1910)
                    "Year": "",
                    "Collection Place": "Spain, Aragon",
                    "Locality": "Spain, Aragon",
                    "Country": "Spain",
                    "Box Label": "Ephedra scopasia Lange Spania: Aragon juni 1910 Vicioso",
                    "Conservation Status": "plant behind glass frame, tape starting to fall off. Okay form",
                    "Comment": "",
                    "Reviewed": False,
                    "Reviewed_By": "",
                    "Reviewed_At": "",
                    "Problem_Flags": "Collection_Date_Problem",
                },
                {
                    "ObjectID": "198",
                    "Object Number": "198",
                    "UID": "98ba9882",
                    "Genus": "Corylus",
                    "Species": "colurna",
                    "Taxon": "Corylus colurna",
                    "Author": "L.",
                    "Family": "Betulaceae",
                    "Higher Classification": "1886",
                    "(N) Plant Part": "Fruktstander",
                    "Plant Part": "fruitcluster",
                    "Collector": "F. C. Schübeler",
                    "Innsammling Nr.": "",
                    "Collection Date": "1963",  # Intentionally wrong current value (real label: 1927; Ledger 1: 1927; Ledger 2: 1912)
                    "Year": "1963",
                    "Collection Place": "Norway, Oslo, Tøyen",
                    "Locality": "Norway, Oslo, Tøyen",
                    "Country": "Norway",
                    "Box Label": "Corylus colurna Töyenhaven 1927",
                    "Conservation Status": "two clusters mounted on a wooden platform. good form",
                    "Comment": "",
                    "Reviewed": False,
                    "Reviewed_By": "",
                    "Reviewed_At": "",
                    "Problem_Flags": "Collection_Date_Problem",
                },
                {
                    "ObjectID": "1003",
                    "Object Number": "1003",
                    "UID": "a4c91003",
                    "Genus": "Salix",
                    "Species": "herbacea",
                    "Taxon": "Salix herbacea",
                    "Author": "L.",
                    "Family": "Salicaceae",
                    "Higher Classification": "",
                    "(N) Plant Part": "",
                    "Plant Part": "",
                    "Collector": "R. F. Fristedt",
                    "Innsammling Nr.": "304",
                    "Collection Date": "22.06.1853",
                    "Year": "1853",
                    "Collection Place": "Norway, Jotunheimen",
                    "Locality": "Norway, Jotunheimen",
                    "Country": "Norway",
                    "Box Label": "Salix herbacea Jotunheimen 1853",
                    "Conservation Status": "Good",
                    "Comment": "",
                    "Reviewed": True,
                    "Reviewed_By": "Curator",
                    "Reviewed_At": "2026-01-10 14:30:00",
                    "Problem_Flags": "",
                },
            ]

            obs_data = [
                {
                    "ObjectID": "110",
                    "Reviewed": False,
                    "ReviewedAt": "",
                    "Building": "Økern",
                    "Floor": "1",
                    "Cabinet": "04",
                    "Shelf": "02",
                    "Stored as": "in plastic box",
                    "Genus_Problem": False,
                    "Species_Problem": False,
                    "Collection_Date_Problem": True,
                    "Box_Label_Problem": False,
                    "Other_problem": False,
                },
                {
                    "ObjectID": "198",
                    "Reviewed": False,
                    "ReviewedAt": "",
                    "Building": "Økern",
                    "Floor": "1",
                    "Cabinet": "06",
                    "Shelf": "06",
                    "Stored as": "Mounted on wooded platform",
                    "Genus_Problem": False,
                    "Species_Problem": False,
                    "Collection_Date_Problem": True,
                    "Box_Label_Problem": False,
                    "Other_problem": False,
                },
                {
                    "ObjectID": "1003",
                    "Reviewed": True,
                    "ReviewedAt": "10.01.2026 14:30",
                    "Building": "Økern",
                    "Floor": "1",
                    "Cabinet": "21",
                    "Shelf": "01",
                    "Stored as": "in plastic box",
                    "Genus_Problem": False,
                    "Species_Problem": False,
                    "Collection_Date_Problem": False,
                    "Box_Label_Problem": False,
                    "Other_problem": False,
                },
            ]

            df_reg = pd.DataFrame(reg_data).set_index("ObjectID", drop=False)
            df_obs = pd.DataFrame(obs_data).set_index("ObjectID", drop=False)
            df_photo = pd.DataFrame(columns=["ObjectID", "PhotoURL", "PhotoType"])
            df_log = pd.DataFrame(columns=["Timestamp", "ObjectID", "Action", "User"])
            df_unval = pd.DataFrame()

            # 3-source historical conflict for #198 ONLY (#110 intentionally has NO historical records)
            hist_book_1 = pd.DataFrame([
                {
                    "ObjectID": "198",
                    "Genus": "Corylus",
                    "Species": "colurna",
                    "Taxon": "Corylus colurna",
                    "Family": "Betulaceae",
                    "Collection Date": "1927",
                    "Year": "1927",
                    "Collection Place": "Norway, Oslo, Tøyen",
                }
            ]).set_index("ObjectID", drop=False)

            hist_book_2 = pd.DataFrame([
                {
                    "ObjectID": "198",
                    "Genus": "Corylus",
                    "Species": "colurna",
                    "Taxon": "Corylus colurna",
                    "Family": "Betulaceae",
                    "Collection Date": "1912",
                    "Year": "1912",
                    "Collection Place": "Oslo, Tøyenhaven",
                }
            ]).set_index("ObjectID", drop=False)

            mock_hist = [
                {"name": "Historical Ledger Book 1", "df": hist_book_1},
                {"name": "Old Card Catalog (Ledger 2)", "df": hist_book_2},
            ]
            return df_reg, df_obs, df_photo, df_log, df_unval, mock_hist

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

        if mock_type == "database":
            reg_data = [
                {
                    "ObjectID": "3001",
                    "Genus": "Betula",
                    "Species": "pubescens",
                    "Taxon": "Betula pubescens",
                    "Family": "Betulaceae",
                    "Author": "Ehrh.",
                    "Collector": "O. Dahl",
                    "Collection Date": "1952",
                    "Collection Place": "Norway, Oslo",
                    "Comment": "",
                    "Reviewed": False,
                    "Problem_Flags": "",
                },
                {
                    "ObjectID": "3002",
                    "Genus": "Picea",
                    "Species": "abies",
                    "Taxon": "Picea abies",
                    "Family": "Pinaceae",
                    "Author": "(L.) H.Karst.",
                    "Collector": "J. Lid",
                    "Collection Date": "1961",
                    "Collection Place": "Norway, Nordmarka",
                    "Comment": "",
                    "Reviewed": False,
                    "Problem_Flags": "",
                },
            ]
            obs_data = [
                {
                    "ObjectID": "3001",
                    "Reviewed": False,
                    "ReviewedAt": "",
                    "Building": "Økern",
                    "Floor": "1",
                    "Cabinet": "01",
                    "Shelf": "01",
                    "Stored as": "in plastic box",
                    "Other_problem": False,
                },
                {
                    "ObjectID": "3002",
                    "Reviewed": False,
                    "ReviewedAt": "",
                    "Building": "Økern",
                    "Floor": "1",
                    "Cabinet": "01",
                    "Shelf": "02",
                    "Stored as": "in plastic box",
                    "Other_problem": False,
                },
            ]
            df_reg = pd.DataFrame(reg_data).set_index("ObjectID", drop=False)
            df_obs = pd.DataFrame(obs_data).set_index("ObjectID", drop=False)
            df_photo = pd.DataFrame(columns=["ObjectID", "PhotoURL", "PhotoType"])
            df_log = pd.DataFrame(columns=["Timestamp", "ObjectID", "Action", "User"])
            df_unval = pd.DataFrame()
            return df_reg, df_obs, df_photo, df_log, df_unval, []

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
                    "Comment": "Bent display — needs workshop check",
                    "Problem_Flags": "Other_problem",
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
                    "Box_Label_Problem": False,
                    "Other_problem": True,
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
        if mock_type == "discrepancy":
            hist_book_1 = pd.DataFrame([
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

            hist_book_2 = pd.DataFrame([
                {
                    "ObjectID": "1001",
                    "Taxon": "Betula pubescens",
                    "Author": "Ehrh.",
                    "Family": "Betulaceae",
                    "Collection Place": "Rondane",
                    "Locality": "Rondane",
                    "Collection Date": "1958",
                    "Year": "1958"
                },
                {
                    "ObjectID": "1002",
                    "Genus": "Pinus",
                    "Species": "sylvestris",
                    "Taxon": "Pinus sylvestris",
                    "Family": "Pinaceae",
                    "Collection Date": "1987",
                    "Year": "1987",
                    "Collection Place": "Tynset, Hedmark"
                }
            ]).set_index("ObjectID", drop=False)

            mock_hist.append({
                "name": "Historical Ledger Book 1",
                "df": hist_book_1
            })
            mock_hist.append({
                "name": "Old Card Catalog (Ledger 2)",
                "df": hist_book_2
            })

        return df_reg, df_obs, df_photo, df_log, df_unval, mock_hist
