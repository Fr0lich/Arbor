"""
ui/tutorials/triage_tutorial.py

Action-driven Practice Sandbox tour for the Office Triage (REV+ERR) workflow.
Teaches curators how to isolate hallway-flagged specimens, clear confirmed-correct flags,
navigate the triage queue with Alt+Left/Right, and safely leave unsolvable issues for later.
"""

from .sandbox_manager import SandboxManager, mark_tutorial_completed
from .tutorial_runner import TutorialRunner, ActionStep


def _is_problem_queue_open(ui) -> bool:
    """Detect whether the Problem Resolution Queue / Resolver window is open."""
    root = getattr(ui, "root", None)
    if root is not None:
        try:
            for w in root.winfo_children():
                title = str(getattr(w, "title", lambda: "")())
                if "Problem" in title or "Triage" in title:
                    return True
        except Exception:
            pass
    return False


def _is_2002_date_flag_cleared(ui) -> bool:
    """Detect whether #2002's Collection_Date_Problem flag has been cleared."""
    app = getattr(ui, "app", None)
    df_obs = getattr(app, "df_obs", None)
    if df_obs is not None and "2002" in df_obs.index and "Collection_Date_Problem" in df_obs.columns:
        try:
            val = df_obs.loc["2002", "Collection_Date_Problem"]
            return not bool(val) or str(val).lower() in ("false", "0", "nan", "none")
        except Exception:
            pass
    return False


def start_triage_tutorial(ui, on_complete=None):
    """Initializes the triage Practice Sandbox and starts the Office Triage (REV+ERR) tour."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="triage")

    def _finish_cb():
        mark_tutorial_completed("triage")
        if callable(on_complete):
            on_complete()

    steps = [
        ActionStep(
            step_id="triage_intro",
            title="0. What Is Office Triage (REV+ERR)?",
            instruction=(
                "When someone walks the collection with a phone and flags an issue they couldn't fix on the spot, "
                "the specimen gets an amber [REV+ERR] badge.\n\n"
                "In this Practice Sandbox, #2001 has a physical 'Other Issue' (bent display — keep flagged for the workshop), "
                "while #2002 has a date flag whose value is actually fine (clear in 1 click)."
            ),
            action_hint="Click Next → to isolate the [REV+ERR] queue.",
            details=(
                "Clean, finished specimens like #2003 carry a green [REV] badge and stay out of your triage queue."
            ),
        ),
        ActionStep(
            step_id="triage_filter",
            title="1. Isolate Hallway Follow-Up (REV+ERR)",
            instruction=(
                "Open Filter (press Ctrl+G) and pick 'Hallway Follow-Up (REV+ERR)' — or press Ctrl+K and search 'Hallway Follow-Up'. "
                "This hides clean [REV] specimens like #2003 so you only see items needing attention."
            ),
            target_id="search_entry",
            action_hint="Press Ctrl+G (or Ctrl+K → Hallway Follow-Up), then click Next →.",
            keycaps=["Ctrl", "G"],
            details=(
                "Excel impact: Filters the Specimen Directory to rows where Observation.Reviewed = TRUE "
                "and at least one problem flag column is TRUE."
            ),
        ),
        ActionStep(
            step_id="triage_open_queue",
            title="2. Open Problem Resolution Queue",
            instruction=(
                "Click TOOLS ▾ → Problem Resolution Queue in the top bar (or press Ctrl+K and pick 'Triage Problem Queue') "
                "to step through all flagged specimens in one streamlined window."
            ),
            target_id="problem_flags_frame",
            action_hint="Open Problem Resolution Queue (or click Skip Step →).",
            keycaps=["Ctrl", "K"],
            details=(
                "Queue mode lets you work through dozens of hallway-flagged specimens without hunting through the Specimen Directory one by one."
            ),
            validator=_is_problem_queue_open,
        ),
        ActionStep(
            step_id="triage_clear_or_defer",
            title="3. Clear False Alarms — Leave Hard Issues Flagged",
            instruction=(
                "Use Next (Alt+→) to step between #2001 and #2002:\n"
                "• On #2001 ('Bent display'): you can't fix physical damage at a desk — leave 'Other Issue' active and skip it!\n"
                "• On #2002 ('1972' is already correct): click '✓ Value is Correct (Clear Flag)' to turn it green [REV]."
            ),
            action_hint="Clear #2002's flag with '✓ Value is Correct' (or click Skip Step →).",
            keycaps=["Alt", "→"],
            details=(
                "Excel impact: '✓ Value is Correct (Clear Flag)' sets the problem column to FALSE without altering Registration text, "
                "logs PROBLEM_CLEARED, and pushes an Undo snapshot (Ctrl+Z). Leaving #2001 flagged keeps it safely queued for the workshop."
            ),
            validator=_is_2002_date_flag_cleared,
        ),
        ActionStep(
            step_id="triage_complete",
            title="4. Office Triage Complete!",
            instruction=(
                "Great work! You now know the full vault-to-desk triage loop: isolate [REV+ERR], clear confirmed values in 1 click, "
                "and safely leave hard issues flagged for later. Click Finish ✓ to exit Practice Mode."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "Everything in this tour ran inside Practice Mode — your real museum collection files were never modified."
            ),
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Office Triage (REV+ERR)", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
