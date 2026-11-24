"""
ui/tutorials/triage_tutorial.py

Action-driven Practice Sandbox tour for the Office Triage (REV+ERR) workflow.
Teaches curators how to isolate hallway-flagged specimens, clear confirmed-correct flags,
navigate the problem queue with Alt+Left/Right, and safely leave unsolvable issues for a specialist.
"""

from .sandbox_manager import SandboxManager, mark_tutorial_completed
from .tutorial_runner import TutorialRunner, ActionStep


def _is_problem_queue_open(ui) -> bool:
    """Detect whether the ObjectProblemResolver window (Queue Mode or single) is open."""
    root = getattr(ui, "root", None)
    if root is not None:
        try:
            for w in root.winfo_children():
                title = str(getattr(w, "title", lambda: "")())
                if "Problem Resolution" in title:
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

    def _launch_discrepancy_tutorial(runner):
        from .discrepancy_tutorial import start_discrepancy_tutorial
        mark_tutorial_completed("triage")
        if callable(on_complete):
            try:
                on_complete()
            except Exception:
                pass
        start_discrepancy_tutorial(ui)

    def _launch_database_tutorial(runner):
        from .database_tutorial import start_database_tutorial
        mark_tutorial_completed("triage")
        if callable(on_complete):
            try:
                on_complete()
            except Exception:
                pass
        start_database_tutorial(ui)

    steps = [
        ActionStep(
            step_id="triage_intro",
            title="Sorting Through Hallway-Flagged Objects (REV+ERR)",
            instruction=(
                "Office Triage simply means sorting through objects that were checked in the hallway "
                "but still have an open issue — marked with an amber [REV+ERR] badge.\n\n"
                "In this Practice Mode, #2001 has a physical 'Other Issue' (bent display — leave flagged for a specialist), "
                "while #2002 has a date flag whose value is actually fine (clear in 1 click)."
            ),
            action_hint="Click Next → to filter to just the [REV+ERR] queue.",
            details=(
                "Clean, finished specimens like #2003 carry a green [REV] badge and stay out of your follow-up list."
            ),
        ),
        ActionStep(
            step_id="triage_filter",
            title="Show Only Hallway Follow-Up (REV+ERR)",
            instruction=(
                "Open Filter (press Ctrl+G) and pick 'Hallway Follow-Up (REV+ERR)' — or press Ctrl+K and search 'Hallway Follow-Up'.\n\n"
                "This hides clean green [REV] objects like #2003 so you only see items that still need attention."
            ),
            action_hint="Press Ctrl+G (or Ctrl+K → Hallway Follow-Up), then click Next →.",
            keycaps=["Ctrl", "G"],
            details=(
                "This filter shows only objects that have already been physically Reviewed and still have at least one active problem checkbox."
            ),
        ),
        ActionStep(
            step_id="triage_open_queue",
            title="Open Problem Queue & Resolver",
            instruction=(
                "Click the highlighted TOOLS ▾ menu → Open Problem Queue & Resolver... → OPEN QUEUE "
                "(or press Ctrl+K and pick 'Triage Problem Queue') to step through all flagged objects in one window."
            ),
            target_id="tools_nav_btn",
            action_hint="Open Problem Resolution Queue (or click Skip Step →).",
            keycaps=["Ctrl", "K"],
            details=(
                "Queue mode lets you work through dozens of hallway-flagged objects one after another without hunting through the Specimen Directory."
            ),
            validator=_is_problem_queue_open,
        ),
        ActionStep(
            step_id="triage_clear_or_defer",
            title="Clear False Alarms — Leave Hard Issues Flagged",
            instruction=(
                "Use Next (Alt+→) to step between #2001 and #2002:\n"
                "• On #2001 ('Bent display'): you can't fix physical damage at a desk — leave 'Other Issue' active for a specialist and move on.\n"
                "• On #2002 ('1972' is already correct): click '✓ Value is Correct (Clear Flag)' to turn it green [REV]."
            ),
            action_hint="Clear #2002's flag with '✓ Value is Correct' (or click Skip Step →).",
            keycaps=["Alt", "→"],
            details=(
                "'✓ Value is Correct (Clear Flag)' clears the problem box without changing the text and supports Undo (Ctrl+Z). "
                "Tip: For flagged plant name issues, you can also check 'Old Names & Synonyms' to see if an older label name is just a synonym."
            ),
            validator=_is_2002_date_flag_cleared,
        ),
        ActionStep(
            step_id="triage_complete",
            title="Office Triage Complete!",
            instruction=(
                "Great work! You now know the full hallway-to-desk follow-up loop: filter to [REV+ERR], clear false alarms in 1 click, "
                "and safely leave harder issues flagged for a specialist.\n\n"
                "Click Finish ✓ to return to your workspace, or open another guide below."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode, or launch another guide above.",
            action_buttons=[
                ("📚 Historical Ledger Comparison", _launch_discrepancy_tutorial, True),
                ("📁 Collections & New Specimens (Optional)", _launch_database_tutorial, False),
            ],
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Office Triage (REV+ERR)", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
