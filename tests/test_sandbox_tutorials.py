"""
tests/test_sandbox_tutorials.py

Unit tests for sandboxed interactive tutorials:
- Sandbox state snapshot and zero-disk restore
- TutorialRunner HUD creation and step progression
- Review, Discrepancy, and Database tutorial flows
"""

import unittest
import tkinter as tk
import pandas as pd
from models import AppState
from ui.tutorials import (
    SandboxManager,
    TutorialRunner,
    ActionStep,
    start_review_tutorial,
    start_discrepancy_tutorial,
    start_database_tutorial
)


class MockUI:
    def __init__(self, root):
        self.root = root
        self.app = AppState()
        self.app.excel_path = "C:/fake/real_database.xlsx"
        self.app.config_name = "Standard"
        self.app.config = {"name": "Standard"}
        self.app.df_reg = pd.DataFrame([{"ObjectID": "999", "Taxon": "Real Specimen"}]).set_index("ObjectID", drop=False)
        self.app.df_obs = pd.DataFrame([{"ObjectID": "999"}]).set_index("ObjectID", drop=False)
        self.app.df_photo = pd.DataFrame()
        self.app.df_log = pd.DataFrame()
        self.app.df_unvalidated = pd.DataFrame()
        self.app.current_object_id = "999"
        self.current_id = "999"

        # Mock UI elements
        self.search_entry = tk.Entry(root)
        self.search_entry.tutorial_id = "search_entry"
        self.object_editor_frame = tk.Frame(root)
        self.object_editor_frame.tutorial_id = "object_editor_frame"
        self.history_btn = tk.Button(root, text="History")
        self.reviewed_button = tk.Button(root, text="Mark Reviewed")
        self.reviewed_button.tutorial_id = "reviewed_button"
        self.reviewed_var = tk.BooleanVar(value=False)

    def _precompute_startup_caches(self, df_reg, df_obs, df_photo):
        pass

    def _finish_open_excel(self, path, output_path, df_reg, df_obs, df_photo, df_log, df_unval=None):
        self.app.excel_path = path
        self.app.df_reg = df_reg
        self.app.df_obs = df_obs
        self.app.df_photo = df_photo
        self.app.df_log = df_log
        self.app.df_unvalidated = df_unval


class TestSandboxTutorials(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def setUp(self):
        self.ui = MockUI(self.root)
        self.sm = SandboxManager()
        # Reset singleton state
        self.sm.is_sandboxed = False
        self.sm.snapshot = None

    def tearDown(self):
        if self.sm.is_sandboxed:
            self.sm.exit_sandbox(self.ui)

    def test_sandbox_enter_and_exit_isolation(self):
        orig_path = self.ui.app.excel_path
        orig_id = self.ui.app.current_object_id

        # 1. Enter sandbox
        self.sm.enter_sandbox(self.ui, mock_type="review")
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, "[Tutorial Sandbox]")
        # Sandbox must contain mock specimen 1001
        self.assertIn("1001", self.ui.app.df_reg.index)

        # 2. Mutate sandbox state (simulate user doing tutorial work)
        self.ui.app.df_reg.loc["1001", "Reviewed"] = True

        # 3. Exit sandbox
        self.sm.exit_sandbox(self.ui)
        self.assertFalse(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, orig_path)
        self.assertIn("999", self.ui.app.df_reg.index)
        self.assertNotIn("1001", self.ui.app.df_reg.index)

    def test_tutorial_runner_step_progression(self):
        step1 = ActionStep(
            step_id="s1",
            title="Step One",
            instruction="Test instruction 1",
            action_hint="Hint 1"
        )
        step2 = ActionStep(
            step_id="s2",
            title="Step Two",
            instruction="Test instruction 2",
            action_hint="Hint 2"
        )

        runner = TutorialRunner(self.ui, [step1, step2], tutorial_name="Test Runner")
        self.assertIsNotNone(runner.hud_win)
        self.assertEqual(runner.current_idx, 0)
        self.assertEqual(runner.title_lbl.cget("text"), "Step One")

        # Skip to step 2
        runner.next_step()
        self.assertEqual(runner.current_idx, 1)
        self.assertEqual(runner.title_lbl.cget("text"), "Step Two")

        # Go back to step 1
        runner.prev_step()
        self.assertEqual(runner.current_idx, 0)

        # Exit tutorial cleans up HUD
        runner.exit_tutorial()
        self.assertIsNone(runner.hud_win)

    def test_start_review_tutorial(self):
        runner = start_review_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(len(runner.steps), 5)
        self.assertEqual(runner.steps[0].step_id, "select_object")
        self.assertEqual(runner.steps[3].step_id, "mark_reviewed")

        runner.exit_tutorial()
        self.assertFalse(self.sm.is_sandboxed)

    def test_start_discrepancy_tutorial(self):
        runner = start_discrepancy_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(len(runner.steps), 5)
        self.assertEqual(runner.steps[0].step_id, "open_resolver")
        self.assertEqual(runner.steps[3].step_id, "apply_changes")

        runner.exit_tutorial()
        self.assertFalse(self.sm.is_sandboxed)

    def test_start_database_tutorial(self):
        runner = start_database_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(len(runner.steps), 4)
        self.assertEqual(runner.steps[0].step_id, "open_db_wizard")
        self.assertEqual(runner.steps[1].step_id, "add_new_object")

    def test_sandbox_exit_when_initial_state_was_none(self):
        self.ui.app.excel_path = None
        self.ui.app.df_reg = None
        self.ui.app.df_obs = None
        self.ui.app.current_object_id = None

        self.sm.enter_sandbox(self.ui, mock_type="review")
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, "[Tutorial Sandbox]")

        self.sm.exit_sandbox(self.ui)
        self.assertFalse(self.sm.is_sandboxed)
        self.assertIsNone(self.ui.app.excel_path)
        self.assertIsNone(self.ui.app.df_reg)

    def test_tutorial_runner_validator_advancement(self):
        self.ui.test_action_done = False
        step = ActionStep(
            step_id="val_test",
            title="Validator Step",
            instruction="Perform action",
            validator=lambda u: getattr(u, "test_action_done", False) is True
        )
        step_end = ActionStep(
            step_id="end_step",
            title="Done Step",
            instruction="Done"
        )

        runner = TutorialRunner(self.ui, [step, step_end], tutorial_name="Validator Runner")
        self.assertEqual(runner.current_idx, 0)

        # Trigger validator condition
        self.ui.test_action_done = True
        # Manually invoke poll validator check or process
        runner._poll_validator(step.validator)
        self.assertEqual(runner.current_idx, 1)
        runner.exit_tutorial()

    def test_sandbox_practice_banner_and_physical_scenario_columns(self):
        """Phase 1: Practice Mode banner mounts/unmounts cleanly and mock 1002 has Cabinet 21 scenario."""
        self.sm.enter_sandbox(self.ui, mock_type="review")
        self.assertIsNotNone(self.sm._practice_banner)
        self.assertTrue(self.sm._practice_banner.winfo_exists())
        self.assertEqual(self.ui.app.df_reg.loc["1002", "Collection Date"], "2008")
        self.assertEqual(self.ui.app.df_obs.loc["1002", "Cabinet"], "21")
        self.assertFalse(bool(self.ui.app.df_obs.loc["1002", "Box_Label_Problem"]))
        self.assertFalse(bool(self.ui.app.df_obs.loc["1002", "Reviewed"]))
        self.assertTrue(len(self.ui.app.historical_dbs) >= 1)

        self.sm.exit_sandbox(self.ui)
        self.assertIsNone(self.sm._practice_banner)

    def test_sandbox_blocks_disk_saves_and_autosaves(self):
        """Phase 1: Disk saves and autosaves must be blocked while SandboxManager.is_sandboxed is True."""
        from ui.database_ops import DatabaseOpsMixin
        from ui.autosave_handler import AutosaveMixin

        class SaveGuardUI(DatabaseOpsMixin, AutosaveMixin):
            def __init__(self, mock_ui):
                self.root = mock_ui.root
                self.app = mock_ui.app
                self.toasts = []
                self.committed = False
                self._autosave_job = None

            def show_toast(self, msg, level="info"):
                self.toasts.append(msg)

            def commit_current_object(self):
                self.committed = True

            def _schedule_autosave(self):
                pass

        self.sm.enter_sandbox(self.ui, mock_type="review")
        self.ui.app.dirty = True
        guard_ui = SaveGuardUI(self.ui)
        callback_result = []
        guard_ui.save_session("SAVE", on_complete=lambda ok, err=None: callback_result.append((ok, err)))
        self.assertFalse(guard_ui.committed)
        self.assertEqual(callback_result, [(False, "Practice Mode")])
        self.assertTrue(any("Practice Mode" in t for t in guard_ui.toasts))

        # Autosave tick must also skip commit/disk write while sandboxed
        guard_ui._autosave_tick()
        self.assertFalse(guard_ui.committed)
        self.sm.exit_sandbox(self.ui)

    def test_tutorial_runner_renders_keycap_pills(self):
        """Phase 2: ActionStep.keycaps renders visual keycap widgets in HUD and hides when empty."""
        s1 = ActionStep(step_id="k1", title="With Keycaps", instruction="Press shortcut", keycaps=["Ctrl", "Enter"])
        s2 = ActionStep(step_id="k2", title="No Keycaps", instruction="Click finish")
        runner = TutorialRunner(self.ui, [s1, s2], tutorial_name="Keycap Test")
        self.assertTrue(len(runner.keycaps_frame.winfo_children()) > 0)
        runner.next_step()
        self.assertEqual(len(runner.keycaps_frame.winfo_children()), 0)
        runner.exit_tutorial()

    def test_contextual_micro_guides_run_without_sandbox(self):
        """Phase 3: Micro-guides run in-place (use_sandbox=False) without entering or resetting SandboxManager."""
        from ui.tutorials import (
            start_hallway_followup_guide,
            start_armed_shelf_guide,
            start_image_controls_guide,
        )
        orig_path = self.ui.app.excel_path
        for launcher in (start_hallway_followup_guide, start_armed_shelf_guide, start_image_controls_guide):
            runner = launcher(self.ui)
            self.assertFalse(self.sm.is_sandboxed)
            self.assertFalse(runner.use_sandbox)
            self.assertIn("QUICK GUIDE", runner.badge_lbl.cget("text"))
            runner.finish_tutorial()
            self.assertEqual(self.ui.app.excel_path, orig_path)
            self.assertFalse(self.sm.is_sandboxed)

    def test_show_main_help_window_creation(self):
        from ui.help_dialogs import show_main_help
        # Calling show_main_help should construct a top-level window without raising exceptions
        show_main_help(self.ui)

    def test_tutorial_hud_stays_on_secondary_monitor_negative_coords(self):
        """Regression: TutorialRunner HUD must stay on secondary monitors with negative X/Y coordinates."""
        from unittest.mock import MagicMock

        step = ActionStep(step_id="m1", title="Multi-monitor", instruction="Check HUD placement")
        runner = TutorialRunner(self.ui, [step], tutorial_name="Monitor Test", use_sandbox=False)
        fake_root = MagicMock()
        fake_root.winfo_exists.return_value = True
        fake_root.winfo_rootx.return_value = -1600
        fake_root.winfo_rooty.return_value = -200
        fake_root.winfo_width.return_value = 1280
        fake_root.winfo_height.return_value = 800

        captured = []
        orig_geom = runner.hud_win.geometry
        runner.hud_win.geometry = lambda g=None: captured.append(g) if g else orig_geom()
        runner.ui = MagicMock(root=fake_root)
        runner._position_hud()
        runner.hud_win.geometry = orig_geom
        runner.exit_tutorial()

        self.assertTrue(captured, "Expected HUD geometry to be set")
        geom = captured[-1]
        self.assertTrue(geom.startswith("-"), f"Expected negative X for left monitor, got {geom}")
        self.assertNotIn("+-", geom, f"Invalid Tcl geometry string: {geom}")

    def test_welcome_tour_prompt_centered_and_persistent(self):
        """Regression: Demo/first-run welcome prompt is a persistent centered Toplevel (no auto-dismiss)."""
        from ui.database_ops import DatabaseOpsMixin

        class _Host(DatabaseOpsMixin):
            pass

        host = _Host()
        host.root = self.root
        host.dark_mode = False
        host._show_welcome_tour_prompt(is_demo=True)
        self.root.update_idletasks()
        win = getattr(host, "_welcome_tour_win", None)
        self.assertIsNotNone(win)
        self.assertTrue(win.winfo_exists())
        self.assertEqual(win.title(), "Welcome to Arbor")
        win.destroy()

    def test_details_drawer_toggle_and_single_runner_guard(self):
        """Verify ActionStep.details expands/collapses cleanly and a second runner closes the first."""
        s1 = ActionStep(
            step_id="d1",
            title="With Details",
            instruction="Short operational step.",
            details="Excel impact: Sets Observation.Reviewed = TRUE.",
        )
        s2 = ActionStep(step_id="d2", title="No Details", instruction="Plain step.")
        r1 = TutorialRunner(self.ui, [s1, s2], tutorial_name="Details Test", use_sandbox=False)
        self.assertFalse(r1._details_expanded)
        self.assertEqual(r1.details_lbl.cget("text"), "Excel impact: Sets Observation.Reviewed = TRUE.")

        r1._toggle_details()
        self.assertTrue(r1._details_expanded)
        self.assertIn("Hide Details", r1.details_toggle_btn.cget("text"))

        # Advancing resets drawer to collapsed
        r1.next_step()
        self.assertFalse(r1._details_expanded)

        # Launching a second runner closes the first HUD cleanly
        old_hud = r1.hud_win
        r2 = TutorialRunner(self.ui, [s2], tutorial_name="Second Runner", use_sandbox=False)
        self.assertIsNone(r1.hud_win)
        self.assertFalse(old_hud.winfo_exists())
        self.assertTrue(r2.hud_win.winfo_exists())
        r2.exit_tutorial()

    def test_hud_auto_dodges_right_side_target_widget(self):
        """Verify HUD docks on the left when target_widget is on the right half of parent_root."""
        from unittest.mock import MagicMock

        step = ActionStep(step_id="ad1", title="Auto-Dodge", instruction="Dodge right target")
        runner = TutorialRunner(self.ui, [step], tutorial_name="Dodge Test", use_sandbox=False)

        fake_root = MagicMock()
        fake_root.winfo_exists.return_value = True
        fake_root.winfo_rootx.return_value = 100
        fake_root.winfo_rooty.return_value = 50
        fake_root.winfo_width.return_value = 1200
        fake_root.winfo_height.return_value = 800

        fake_target = MagicMock()
        fake_target.winfo_exists.return_value = True
        fake_target.winfo_viewable.return_value = True
        fake_target.winfo_rootx.return_value = 950  # Right half of [100..1300]
        fake_target.winfo_width.return_value = 200

        captured = []
        orig_geom = runner.hud_win.geometry
        runner.hud_win.geometry = lambda g=None: captured.append(g) if g else orig_geom()
        runner.ui = MagicMock(root=fake_root)
        runner._position_hud(target_widget=fake_target)
        runner.hud_win.geometry = orig_geom
        runner.exit_tutorial()

        self.assertTrue(captured)
        # Docked left near rx + 24 (~124), not right side (~900)
        x_val = int(captured[-1].split("+")[1])
        self.assertLess(x_val, 300, f"Expected HUD to dock left away from right-side target, got {captured[-1]}")

    def test_triage_tutorial_sandbox_and_target_ids_valid(self):
        """Verify start_triage_tutorial mounts REV+ERR sandbox cleanly and all tutorial target_ids are valid."""
        from ui.tutorials import start_triage_tutorial
        import ui.tutorials.discrepancy_tutorial as dt_mod

        orig_path = self.ui.app.excel_path
        runner = start_triage_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertIn("2001", self.ui.app.df_reg.index)
        self.assertIn("2002", self.ui.app.df_reg.index)
        self.assertTrue(bool(self.ui.app.df_obs.loc["2001", "Reviewed"]))
        self.assertTrue(bool(self.ui.app.df_obs.loc["2001", "Box_Label_Problem"]))
        self.assertEqual(runner.badge_lbl.cget("text"), "🛡️ PRACTICE SANDBOX")
        runner.finish_tutorial()
        self.assertFalse(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, orig_path)

        # Ensure broken target_id="history_btn" is completely gone from discrepancy_tutorial.py
        with open(dt_mod.__file__, "r", encoding="utf-8") as f:
            dt_src = f.read()
        self.assertNotIn('target_id="history_btn"', dt_src)
        self.assertIn('target_id="history_indicator_label"', dt_src)

    def test_switching_between_sandbox_tutorials_reloads_mock_dataset_and_preserves_snapshot(self):
        """Switching directly from Quick Tour (review) -> Office Triage (triage) reloads #2001 and still restores original workbook."""
        from ui.tutorials import start_review_tutorial, start_triage_tutorial

        orig_path = self.ui.app.excel_path
        r1 = start_review_tutorial(self.ui)
        self.assertIn("1002", self.ui.app.df_reg.index)

        # Switch directly into Office Triage without exiting Practice Mode first
        r2 = start_triage_tutorial(self.ui)
        self.assertIsNone(r1.hud_win)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertIn("2001", self.ui.app.df_reg.index)
        self.assertNotIn("1002", self.ui.app.df_reg.index)

        # Exiting restores the real original workbook (not the intermediate review sandbox)
        r2.exit_tutorial()
        self.assertFalse(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, orig_path)
        self.assertIn("999", self.ui.app.df_reg.index)


if __name__ == "__main__":
    unittest.main()
