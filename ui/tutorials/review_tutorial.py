"""
ui/tutorials/review_tutorial.py

Action-driven interactive tutorial for reviewing and verifying specimen records.
Operates strictly in an isolated in-memory sandbox without mutating real user files.
"""

from .sandbox_manager import SandboxManager
from .tutorial_runner import TutorialRunner, ActionStep


def _is_current_specimen_reviewed(ui) -> bool:
    """Safely check whether the active specimen in the sandbox is marked Reviewed."""
    if getattr(ui, "reviewed_var", None) and ui.reviewed_var.get():
        return True
    app = getattr(ui, "app", None)
    df_obs = getattr(app, "df_obs", None)
    oid = getattr(app, "current_object_id", None)
    if df_obs is None or oid is None:
        return False
    for key in (oid, str(oid), int(oid) if str(oid).isdigit() else None):
        if key is not None and key in df_obs.index:
            try:
                return bool(df_obs.loc[key].get("Reviewed", False))
            except Exception:
                pass
    return False


def _is_collection_date_fixed(ui) -> bool:
    """Check whether specimen 1002's Collection Date was updated to 1998."""
    reg_vars = getattr(ui, "reg_vars", None) or {}
    if "Collection Date" in reg_vars:
        try:
            if "1998" in str(reg_vars["Collection Date"].get()):
                return True
        except Exception:
            pass
    app = getattr(ui, "app", None)
    df_reg = getattr(app, "df_reg", None)
    if df_reg is not None and "1002" in df_reg.index and "Collection Date" in df_reg.columns:
        try:
            return "1998" in str(df_reg.loc["1002", "Collection Date"])
        except Exception:
            pass
    return False


def _is_box_problem_flagged(ui) -> bool:
    """Check whether Box_Label_Problem is flagged on the active specimen."""
    prob_vars = getattr(ui, "problem_vars", None) or {}
    if "Box_Label_Problem" in prob_vars:
        try:
            if bool(prob_vars["Box_Label_Problem"].get()):
                return True
        except Exception:
            pass
    app = getattr(ui, "app", None)
    df_obs = getattr(app, "df_obs", None)
    oid = getattr(app, "current_object_id", None)
    if df_obs is not None and oid in df_obs.index and "Box_Label_Problem" in df_obs.columns:
        try:
            return bool(df_obs.loc[oid, "Box_Label_Problem"])
        except Exception:
            pass
    return False


def start_review_tutorial(ui, on_complete=None):
    """Initializes zero-fear practice sandbox and starts the 3-Minute Quick Tour."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="review")

    steps = [
        ActionStep(
            step_id="select_object",
            title="1. Pull Specimen #1002 (Cabinet 21)",
            instruction="You pulled box #1002 from Cabinet 21. Click specimen 1002 in the Specimen Directory (or press Ctrl+F and type 1002).",
            target_id="search_entry",
            action_hint="Click specimen #1002 in the Specimen Directory.",
            keycaps=["Ctrl", "F"],
            details=(
                "Arbor matches accession numbers even if you omit leading zeros or museum prefixes (e.g. '001' matches '1'). "
                "Selecting a card updates the center photo viewer and the right-hand Registration Form together."
            ),
            validator=lambda u: str(getattr(getattr(u, "app", None), "current_object_id", "") or "") == "1002"
        ),
        ActionStep(
            step_id="fix_year",
            title="2. Fix a Mismatched Label Year (2008 → 1998)",
            instruction="The screen says 2008, but the paper label in your hand says 1998. Type 1998 in Collection Date (or pick 1998 from Historical Suggestions).",
            target_id="reg_field:Collection Date",
            action_hint="Change Collection Date to 1998 (or click Skip Step →).",
            details=(
                "Excel impact: Updates 'Collection Date' on the Registration sheet in memory. "
                "Nothing is written to disk until you press Ctrl+S, and Ctrl+Z undoes mistakes anytime."
            ),
            validator=_is_collection_date_fixed
        ),
        ActionStep(
            step_id="flag_box",
            title="3. Flag a Crushed Storage Box",
            instruction="The box corner is crushed and needs repair later. Check Box_Label_Problem (or press Space on it) to queue it for the workshop.",
            target_id="problem_flags_frame",
            action_hint="Check Box_Label_Problem (or click Skip Step →).",
            keycaps=["Space"],
            details=(
                "Excel impact: Sets 'Box_Label_Problem = TRUE' on the Observation sheet. "
                "You don't need to fix physical box damage right now — flagging it safely queues it for someone else to handle later."
            ),
            validator=_is_box_problem_flagged
        ),
        ActionStep(
            step_id="mark_reviewed",
            title="4. Mark Reviewed (Even With a Flag!)",
            instruction="Press Ctrl+Enter or click '✓ Mark as Reviewed'. The card turns amber [REV+ERR] — confirming you checked the box while keeping the repair flag open.",
            target_id="reviewed_button",
            action_hint="Click '✓ Mark as Reviewed' or press Ctrl+Enter.",
            keycaps=["Ctrl", "Enter"],
            details=(
                "You won't always be able to solve every flagged problem yourself — and that is completely okay! "
                "Marking a specimen Reviewed sets 'Reviewed = TRUE' (confirming a human verified it physically), "
                "while the active flag keeps it in the amber [REV+ERR] queue so a specialist or curator can revisit it in the future."
            ),
            validator=lambda u: _is_current_specimen_reviewed(u)
        ),
        ActionStep(
            step_id="review_complete",
            title="5. Practice Complete!",
            instruction="Great job! Everything here ran in Practice Mode — your real museum files were never touched. Click Finish ✓ to return to your workspace.",
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "You can replay this tour, run the Office Triage Tour, or open the Desktop & Mobile guides anytime from ❓ HELP ▾ or by pressing F1."
            ),
        )
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="3-Minute Quick Tour", on_complete=on_complete)
    sm._active_runner = runner
    return runner
