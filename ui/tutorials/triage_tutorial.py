"""
ui/tutorials/triage_tutorial.py

Action-driven Practice Sandbox tour for the Office Triage (REV+ERR) workflow.
Teaches curators how to isolate hallway-flagged specimens, clear confirmed-correct flags,
navigate the triage queue with Alt+Left/Right, and safely leave unsolvable issues for later.
"""

from .sandbox_manager import SandboxManager
from .tutorial_runner import TutorialRunner, ActionStep


def start_triage_tutorial(ui, on_complete=None):
    """Initializes the triage Practice Sandbox and starts the Office Triage (REV+ERR) tour."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="triage")

    steps = [
        ActionStep(
            step_id="triage_filter",
            title="1. Isolate Hallway Follow-Up (REV+ERR)",
            instruction=(
                "Specimens #2001 and #2002 were verified in the vault but flagged with open issues. "
                "Press Ctrl+K and run 'Filter: Hallway Follow-Up (REV+ERR)' (or open Filter with Ctrl+G) to isolate them."
            ),
            target_id="search_entry",
            action_hint="Press Ctrl+K → Hallway Follow-Up (or click Next →).",
            keycaps=["Ctrl", "K"],
            details=(
                "Excel impact: Filters the Specimen Directory to rows where Observation.Reviewed = TRUE "
                "and at least one problem flag column is TRUE, hiding clean [REV] specimens like #2003."
            ),
        ),
        ActionStep(
            step_id="triage_open_queue",
            title="2. Open Problem Resolution Queue",
            instruction=(
                "Press Ctrl+K and select 'Triage Problem Queue (Filtered List)' to open all flagged specimens in one streamlined window."
            ),
            target_id="problem_flags_frame",
            action_hint="Open Triage Problem Queue via Ctrl+K (or click Next →).",
            keycaps=["Ctrl", "K"],
            details=(
                "Queue mode lets you work through dozens of hallway-flagged specimens without hunting through the Specimen Directory one by one."
            ),
        ),
        ActionStep(
            step_id="triage_clear_or_defer",
            title="3. Clear Confirmed Values — Or Leave Hard Ones for Later",
            instruction=(
                "If a flagged value is actually fine, click '✓ Value is Correct (Clear Flag)' to turn [REV+ERR] back to green [REV]. "
                "Use Alt+← / Alt+→ to move between specimens — and if you can't solve a problem right now, that's completely okay: just skip it and leave the flag active for someone else in the future."
            ),
            action_hint="Use Alt+→ to step forward, or click Next →.",
            keycaps=["Alt", "→"],
            details=(
                "Excel impact: '✓ Value is Correct (Clear Flag)' sets the problem column to FALSE without altering Registration text, "
                "logs PROBLEM_CLEARED, and pushes an Undo snapshot (Ctrl+Z). Leaving a flag active keeps the specimen safely visible in [REV+ERR] for a future specialist."
            ),
        ),
        ActionStep(
            step_id="triage_complete",
            title="4. Office Triage Complete!",
            instruction=(
                "Great work! You now know the full vault-to-desk triage loop: isolate [REV+ERR], resolve what you can, and safely leave hard issues flagged for later. "
                "Click Finish ✓ to exit Practice Mode."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "Everything in this tour ran inside Practice Mode — your real Excel workbooks were never modified."
            ),
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Office Triage (REV+ERR)", on_complete=on_complete)
    sm._active_runner = runner
    return runner
