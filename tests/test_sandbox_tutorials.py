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
        # Sandbox must contain real tutorial specimens 110 and 198
        self.assertIn("110", self.ui.app.df_reg.index)
        self.assertIn("198", self.ui.app.df_reg.index)

        # 2. Mutate sandbox state (simulate user doing tutorial work)
        self.ui.app.df_reg.loc["110", "Reviewed"] = True

        # 3. Exit sandbox
        self.sm.exit_sandbox(self.ui)
        self.assertFalse(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, orig_path)
        self.assertIn("999", self.ui.app.df_reg.index)
        self.assertNotIn("110", self.ui.app.df_reg.index)

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
        from tkinter import ttk
        from ui.tutorials.review_tutorial import _is_resolver_open, _step9_target_selector

        runner = start_review_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(len(runner.steps), 11)
        self.assertEqual(
            [s.step_id for s in runner.steps],
            [
                "welcome_overview",
                "orient_110",
                "transcribe_110_date",
                "mark_110_reviewed",
                "select_198",
                "open_198_history",
                "resolve_198_date",
                "close_198_resolver",
                "flag_other_issue",
                "mark_reviewed",
                "review_complete",
            ],
        )
        # Starts cleanly on #110 (no #1003 jump)
        self.assertEqual(str(self.ui.app.current_object_id), "110")
        # Step 2 (orient_110) highlights entire Registration Data panel and has no More Details
        self.assertEqual(runner.steps[1].target_id, "object_editor_frame")
        self.assertIsNone(runner.steps[1].details)
        # Step 3 hides 00.06.1910 behind the collapsible "The Answer" dropdown
        self.assertNotIn("00.06.1910", runner.steps[2].instruction)
        self.assertIn("00.06.1910", runner.steps[2].answer or "")
        # Advance to Step 3 and verify the collapsible Answer drawer toggles cleanly
        runner.next_step()
        runner.next_step()
        self.assertFalse(runner._answer_expanded)
        runner._toggle_answer()
        self.assertTrue(runner._answer_expanded)
        runner._toggle_answer()
        self.assertFalse(runner._answer_expanded)

        # Step 6 & 8: _is_resolver_open detects open Problem Resolution Toplevel
        self.assertFalse(_is_resolver_open(self.ui))
        res_win = tk.Toplevel(self.root)
        res_win.withdraw()
        res_win.title("Problem Resolution")
        try:
            self.assertTrue(_is_resolver_open(self.ui))
        finally:
            res_win.destroy()
        self.assertFalse(_is_resolver_open(self.ui))

        # Step 9: dynamic 2-stage target switches from reg_notebook -> Other Issue checkbox
        nb = ttk.Notebook(self.root)
        details_tab = ttk.Frame(nb)
        prob_tab = ttk.Frame(nb)
        nb.add(details_tab, text="Details")
        nb.add(prob_tab, text="Problems")
        other_cb = ttk.Checkbutton(prob_tab, text="Other Issue")
        other_cb.tutorial_id = "other_problem_checkbox"
        self.ui.reg_notebook = nb
        self.ui._reg_tabs = {"Details": {"container": details_tab}, "Problems": {"container": prob_tab}}
        self.ui.problem_checkbutton_map = {"Other_problem": other_cb}
        try:
            nb.select(details_tab)
            stage1 = _step9_target_selector(self.ui)
            self.assertIsInstance(stage1, tuple)
            self.assertIs(stage1[0], nb)
            nb.select(prob_tab)
            stage2 = _step9_target_selector(self.ui)
            self.assertIs(stage2, other_cb)
        finally:
            nb.destroy()

        # Step 11: custom details_label + 2 direct launch action buttons
        runner.current_idx = 10
        runner.show_step()
        self.assertEqual(runner.details_toggle_btn.cget("text"), "▸ Need help opening Arbor?")
        self.assertEqual(len(runner.action_buttons_frame.winfo_children()), 2)

        runner.exit_tutorial()
        self.assertFalse(self.sm.is_sandboxed)

    def test_start_discrepancy_tutorial(self):
        runner = start_discrepancy_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(len(runner.steps), 7)
        self.assertEqual(runner.steps[0].step_id, "discrepancy_intro")
        self.assertEqual(runner.steps[1].step_id, "open_resolver")
        self.assertEqual(runner.steps[4].step_id, "apply_changes")
        self.assertEqual(runner.steps[5].step_id, "close_discrepancy_resolver")
        self.assertEqual(runner.steps[5].target_id, "hr_apply_all")
        self.assertEqual(len(runner.steps[6].action_buttons), 2)

        runner.exit_tutorial()
        self.assertFalse(self.sm.is_sandboxed)

    def test_start_database_tutorial(self):
        from ui.tutorials.database_tutorial import _has_typed_new_specimen_info

        runner = start_database_tutorial(self.ui)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertEqual(len(runner.steps), 5)
        self.assertEqual(runner.steps[0].step_id, "database_intro")
        self.assertEqual(runner.steps[2].step_id, "add_new_object")
        self.assertIn("3001", self.ui.app.df_reg.index)
        self.assertNotIn("110", self.ui.app.df_reg.index)

        # Validator must not prematurely advance on 1-2 characters
        initial_ids = {"3001", "3002"}
        self.ui.app.current_object_id = "3003"
        self.ui.reg_vars = {"Genus": tk.StringVar(value="Be")}
        self.assertFalse(_has_typed_new_specimen_info(self.ui, initial_ids))
        self.ui.reg_vars["Genus"].set("Bet")
        self.assertTrue(_has_typed_new_specimen_info(self.ui, initial_ids))

        runner.exit_tutorial()

    def test_startup_how_to_open_arbor_window_and_menu_label(self):
        """Verify StartupDialog Help menu starts with plain 'How to Open Arbor' and opens the guide window."""
        import inspect
        from ui.dialogs import StartupDialog

        src = inspect.getsource(StartupDialog.show_help)
        self.assertIn('label="How to Open Arbor"', src)

        dlg = StartupDialog.__new__(StartupDialog)
        dlg.win = self.root
        dlg._bind_canvas_mousewheel = lambda c, f=None: None
        dlg.load_demo_project = lambda: None
        dlg._show_setup_help_msg()
        win = getattr(dlg, "_setup_help_win", None)
        self.assertIsNotNone(win)
        self.assertTrue(win.winfo_exists())
        self.assertEqual(win.title(), "Arbor — How to Open Arbor")
        win.destroy()

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
        """Practice Mode banner mounts/unmounts cleanly and #110/#198 have real data + 3-source historical conflict."""
        self.sm.enter_sandbox(self.ui, mock_type="review")
        self.assertIsNotNone(self.sm._practice_banner)
        self.assertTrue(self.sm._practice_banner.winfo_exists())
        # #110: Ephedra major, blank date, NO historical entries
        self.assertEqual(self.ui.app.df_reg.loc["110", "Genus"], "Ephedra")
        self.assertEqual(self.ui.app.df_reg.loc["110", "Collection Date"], "")
        # #198: Corylus colurna, wrong current date 1963, 2 conflicting historical books (1927 & 1912)
        self.assertEqual(self.ui.app.df_reg.loc["198", "Genus"], "Corylus")
        self.assertEqual(self.ui.app.df_reg.loc["198", "Collection Date"], "1963")
        self.assertFalse(bool(self.ui.app.df_obs.loc["198", "Other_problem"]))
        self.assertFalse(bool(self.ui.app.df_obs.loc["198", "Reviewed"]))
        self.assertEqual(len(self.ui.app.historical_dbs), 2)
        for h in self.ui.app.historical_dbs:
            self.assertNotIn("110", h["df"].index)
            self.assertIn("198", h["df"].index)

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
        self.assertTrue(geom.startswith("+-"), f"Expected Tk '+-' anchor for negative left-monitor X, got {geom}")

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
        self.assertTrue(bool(self.ui.app.df_obs.loc["2001", "Other_problem"]))
        self.assertEqual(len(runner.steps), 5)
        self.assertEqual(runner.steps[0].step_id, "triage_intro")
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
        self.assertIn("198", self.ui.app.df_reg.index)

        # Switch directly into Office Triage without exiting Practice Mode first
        r2 = start_triage_tutorial(self.ui)
        self.assertIsNone(r1.hud_win)
        self.assertTrue(self.sm.is_sandboxed)
        self.assertIn("2001", self.ui.app.df_reg.index)
        self.assertNotIn("198", self.ui.app.df_reg.index)

        # Exiting restores the real original workbook (not the intermediate review sandbox)
        r2.exit_tutorial()
        self.assertFalse(self.sm.is_sandboxed)
        self.assertEqual(self.ui.app.excel_path, orig_path)
        self.assertIn("999", self.ui.app.df_reg.index)

    def test_quick_tour_date_validators_and_tutorial_image_mounting(self):
        """Verify #110 accepts 00.06.1910 or 06.1910, #198 accepts 1927 or 00.00.1927, and tutorial images mount & restore."""
        from ui.tutorials.review_tutorial import _is_110_date_entered, _is_198_date_fixed

        class _DummyImgPanel:
            def __init__(self, root):
                self.image_mode = None
                self.image_folder = None
                self.image_index = {}
                self.show_images_var = tk.BooleanVar(value=False)

        self.ui.image_panel = _DummyImgPanel(self.root)
        self.sm.enter_sandbox(self.ui, mock_type="review")

        # Bundled tutorial photos for #110 and #198 must mount automatically
        self.assertEqual(self.ui.image_panel.image_mode, "folder")
        self.assertEqual(len(self.ui.image_panel.image_index.get("110", [])), 2)
        self.assertEqual(len(self.ui.image_panel.image_index.get("198", [])), 2)
        self.assertTrue(self.ui.image_panel.show_images_var.get())

        # #110 date validator: accepts 00.06.1910 and 06.1910, rejects wrong/blank
        self.assertFalse(_is_110_date_entered(self.ui))
        self.ui.app.df_reg.loc["110", "Collection Date"] = "06.1910"
        self.assertTrue(_is_110_date_entered(self.ui))
        self.ui.app.df_reg.loc["110", "Collection Date"] = "00.06.1910"
        self.assertTrue(_is_110_date_entered(self.ui))

        # #198 date validator: accepts 1927 and 00.00.1927, rejects 1963/1912
        self.assertFalse(_is_198_date_fixed(self.ui))
        self.ui.app.df_reg.loc["198", "Collection Date"] = "1912"
        self.assertFalse(_is_198_date_fixed(self.ui))
        self.ui.app.df_reg.loc["198", "Collection Date"] = "00.00.1927"
        self.assertTrue(_is_198_date_fixed(self.ui))
        self.ui.app.df_reg.loc["198", "Collection Date"] = "1927"
        self.assertTrue(_is_198_date_fixed(self.ui))

        # Exiting sandbox restores original image_panel state cleanly
        self.sm.exit_sandbox(self.ui)
        self.assertIsNone(self.ui.image_panel.image_mode)
        self.assertEqual(self.ui.image_panel.image_index, {})
        self.assertFalse(self.ui.image_panel.show_images_var.get())

    def test_historical_suggestions_slate_blue_pill(self):
        """Verify update_history_indicator renders the Slate-Blue pill with count, matches state, and hides when none."""
        from ui.historical_suggestions import HistoricalSuggestionsMixin

        class _PillHost(HistoricalSuggestionsMixin):
            def __init__(self, root, app):
                self.root = root
                self.app = app
                self.dark_mode_active = False
                self.history_indicator_label = tk.Label(root, text="")
                self._suggestions = []

            def collect_historical_suggestions(self, oid):
                return self._suggestions

            def _get_reg_by_id(self, db):
                return db["df"]

        self.sm.enter_sandbox(self.ui, mock_type="review")
        host = _PillHost(self.root, self.ui.app)

        # 1. Suggestions available -> Slate-Blue pill with count
        host._suggestions = [{"field": "Collection Date", "value": "1927"}]
        host.update_history_indicator("198")
        self.assertIn("History: 1 suggestion", host.history_indicator_label.cget("text"))
        self.assertEqual(host.history_indicator_label.cget("bg"), "#e6f0f6")

        # 2. Historical data exists for #198, but no differing suggestions -> muted pill
        host._suggestions = []
        host.update_history_indicator("198")
        self.assertEqual(host.history_indicator_label.cget("text"), "History: matches current")

        # 3. #110 has NO historical data -> cleared and hidden
        host.update_history_indicator("110")
        self.assertEqual(host.history_indicator_label.cget("text"), "")
        self.sm.exit_sandbox(self.ui)

    def test_tutorial_validators_and_menu_parity(self):
        """Verify nested hr_sidebar & Problem Resolution validators, menu parity, and Escape close."""
        from ui.tutorials import start_triage_tutorial
        from ui.tutorials.discrepancy_tutorial import _has_widget_with_tutorial_id
        from ui.tutorials.triage_tutorial import _is_problem_queue_open
        import ui.main_window as mw_mod
        import ui.image_panel as ip_mod
        import ui.object_problem_resolver as opr_mod
        import inspect

        # 1. Nested hr_sidebar validator finds grandchild inside a Toplevel
        self.assertFalse(_has_widget_with_tutorial_id(self.root, "hr_sidebar"))
        top = tk.Toplevel(self.root); top.withdraw()
        sidebar = tk.Frame(tk.Frame(top)); sidebar.tutorial_id = "hr_sidebar"
        try:
            self.assertTrue(_has_widget_with_tutorial_id(self.root, "hr_sidebar"))
        finally:
            top.destroy()

        # 2. _is_problem_queue_open ignores modal scope picker, matches Problem Resolution
        for title, expected in [("Process Objects with Problems", False), ("Problem Resolution (Queue: 2 Specimens)", True)]:
            w = tk.Toplevel(self.root); w.withdraw(); w.title(title)
            try:
                self.assertIs(_is_problem_queue_open(self.ui), expected)
            finally:
                w.destroy()

        # 3. Triage Step 3 target & wording + menu/shortcut parity + ProblemQueueDialog <Escape>
        runner = start_triage_tutorial(self.ui)
        step3 = next(s for s in runner.steps if s.step_id == "triage_open_queue")
        self.assertEqual(step3.target_id, "tools_nav_btn")
        self.assertIn("Open Problem Queue & Resolver...", step3.instruction)
        runner.exit_tutorial()

        help_src = inspect.getsource(mw_mod.ObjectProgramUI.show_help_dropdown)
        self.assertNotIn("Cabinet 21", help_src)
        self.assertIn("Suggested Learning Path", help_src)
        self.assertIn("4. Office Triage (REV+ERR)", help_src)
        self.assertIn('tutorial_type == "triage"', inspect.getsource(mw_mod.ObjectProgramUI.start_tutorial_flow))
        self.assertNotIn("Open Excel Database... (Ctrl+O)", inspect.getsource(mw_mod.ObjectProgramUI.show_file_dropdown))
        self.assertIn("<Escape>", inspect.getsource(opr_mod.ProblemQueueDialog.__init__))
        with open(ip_mod.__file__, "r", encoding="utf-8") as f:
            self.assertIn('self.image_container.tutorial_id = "image_container"', f.read())

        # 4. H1/H2/L2 regressions: Mobile guide HUD doesn't self-validate; prev_step disables auto-bounce; no 1./2. in image guide
        from ui.tutorials import start_armed_shelf_guide, start_image_controls_guide
        m_runner = start_armed_shelf_guide(self.ui)
        try:
            self.assertFalse(m_runner.steps[1].validator(self.ui))
            m_runner.current_idx = 2
            m_runner.prev_step()
            self.assertEqual(m_runner.current_idx, 1)
            self.assertIsNone(m_runner._poll_job)
        finally:
            m_runner.exit_tutorial()

        img_runner = start_image_controls_guide(self.ui)
        try:
            for s in img_runner.steps:
                self.assertFalse(s.title.startswith(("1.", "2.")))
        finally:
            img_runner.exit_tutorial()

    def test_hud_forwards_global_shortcuts_and_returns_focus(self):
        """Verify floating tutorial HUD binds Ctrl+F / Ctrl+H passthrough and avoids stealing dialog focus."""
        from unittest.mock import MagicMock
        from ui.keybindings import KeybindingManager

        mock_ui = MagicMock()
        mock_ui.root = self.root
        called = []
        mock_ui.handle_ctrl_f = lambda e=None: called.append("ctrl_f")
        mock_ui.open_history_shortcut = lambda e=None: called.append("ctrl_h")

        runner = TutorialRunner(
            mock_ui,
            [ActionStep(step_id="s1", title="Step", instruction="Test")],
            tutorial_name="Shortcut Passthrough",
            use_sandbox=False,
        )
        try:
            self.assertTrue(runner.hud_win.bind("<Control-f>"))
            self.assertTrue(runner.hud_win.bind("<Control-h>"))
            self.assertTrue(runner.hud_win.bind("<Control-k>"))
            # Verify target forwarding actually invokes handlers cleanly
            bound = {}
            class _Rec:
                def bind(self, seq, fn):
                    bound[seq] = fn
            KeybindingManager(mock_ui, self.root).bind_global_shortcuts(target=_Rec())
            bound["<Control-f>"](None)
            bound["<Control-h>"](None)
            self.assertEqual(called, ["ctrl_f", "ctrl_h"])
        finally:
            runner.exit_tutorial()


if __name__ == "__main__":
    unittest.main()
