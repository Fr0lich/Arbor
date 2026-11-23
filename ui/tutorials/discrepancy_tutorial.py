"""
ui/tutorials/discrepancy_tutorial.py

Action-driven interactive tutorial for comparing specimens against conflicting historical ledgers.
Operates strictly in an isolated in-memory sandbox without mutating real user files.
"""

from .sandbox_manager import SandboxManager, mark_tutorial_completed
from .tutorial_runner import TutorialRunner, ActionStep


def _has_widget_with_tutorial_id(root, target_id: str) -> bool:
    """Recursively check whether any live descendant widget carries tutorial_id == target_id."""
    if root is None:
        return False
    try:
        if not root.winfo_exists():
            return False
        if getattr(root, "tutorial_id", None) == target_id:
            return True
        for child in root.winfo_children():
            if _has_widget_with_tutorial_id(child, target_id):
                return True
    except Exception:
        pass
    return False


def _has_applied_1001_change(ui, initial_place: str, initial_date: str) -> bool:
    """Detect whether the trainee applied a confirmed change to #1001."""
    app = getattr(ui, "app", None)
    if getattr(app, "dirty", False):
        return True
    df_reg = getattr(app, "df_reg", None)
    if df_reg is not None and "1001" in df_reg.index:
        try:
            cur_place = str(df_reg.loc["1001", "Collection Place"] or "")
            cur_date = str(df_reg.loc["1001", "Collection Date"] or "")
            if cur_place != initial_place or cur_date != initial_date:
                return True
        except Exception:
            pass
    return False


def start_discrepancy_tutorial(ui, on_complete=None):
    """Initializes sandbox and starts the Historical Ledger Comparison tutorial."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="discrepancy")

    if hasattr(ui, "load_object"):
        try:
            ui.load_object("1001")
        except Exception:
            pass

    initial_place = ""
    initial_date = ""
    if getattr(ui.app, "df_reg", None) is not None and "1001" in ui.app.df_reg.index:
        try:
            initial_place = str(ui.app.df_reg.loc["1001", "Collection Place"] or "")
            initial_date = str(ui.app.df_reg.loc["1001", "Collection Date"] or "")
        except Exception:
            pass

    def _finish_cb():
        mark_tutorial_completed("discrepancy")
        if callable(on_complete):
            on_complete()

    steps = [
        ActionStep(
            step_id="discrepancy_intro",
            title="When to Use Historical Ledger Comparison",
            instruction=(
                "Use this workflow at your desk when older museum catalog books disagree with multiple fields in your currently registered collection.\n\n"
                "In this Practice Sandbox, specimen #1001 is compared against TWO older books that disagree with each other — "
                "so you can practice evaluating historical clues carefully."
            ),
            action_hint="Click Next → to open Historical Ledger Comparison.",
            details=(
                "Remember: comparing older catalog books at your desk is NOT a physical inspection of the object, "
                "so you will leave 'Reviewed' unchecked unless you also inspect the physical object itself."
            ),
        ),
        ActionStep(
            step_id="open_resolver",
            title="Open Historical Ledger Comparison",
            instruction="Click the blue 'History' pill above the registration form (or press Ctrl+H) to open Historical Ledger Comparison.",
            target_id="history_indicator_label",
            action_hint="Click the History pill or press Ctrl+H.",
            keycaps=["Ctrl", "H"],
            details=(
                "Whenever loaded historical ledger books disagree with your currently registered record, "
                "Arbor shows a blue History pill and a slate-blue [CFCT] badge so you can compare versions side by side."
            ),
            validator=lambda u: bool(
                getattr(u, "_current_resolver_win", None)
                or _has_widget_with_tutorial_id(getattr(u, "root", None), "hr_sidebar")
            ),
        ),
        ActionStep(
            step_id="field_directory",
            title="Browse Fields That Disagree",
            instruction="The left sidebar lists every field where the current collection record differs from older ledgers. Click any field to jump straight to its card.",
            target_id="hr_sidebar",
            action_hint="Click a field in the left sidebar, then click Next →.",
            details=(
                "You never have to change a field if you aren't sure — only fields you explicitly apply are updated."
            ),
        ),
        ActionStep(
            step_id="select_resolution",
            title="Compare Multiple Books — Pick Carefully",
            instruction=(
                "Each card shows your currently registered value alongside suggestions from multiple older ledgers. "
                "Notice Book 1 and Book 2 disagree with each other! Click a suggested value card to preview it in the input box."
            ),
            target_id="hr_cards",
            action_hint="Click a suggested value card to preview it, then click Next →.",
            details=(
                "Excel impact: Clicking a suggestion only previews it in the field input. "
                "Nothing is written to the Registration sheet until you click Apply."
            ),
        ),
        ActionStep(
            step_id="apply_changes",
            title="Apply One Card (Without Marking Reviewed)",
            instruction=(
                "Click 'Apply' on a single confirmed card (avoid clicking 'Apply All' until you have checked every card!).\n\n"
                "Important: fixing data from historical ledgers at your desk does NOT count as a physical review — "
                "leave 'Reviewed' unchecked until someone inspects the physical object."
            ),
            target_id="hr_cards",
            action_hint="Click 'Apply' on a card (or click Skip Step →).",
            details=(
                "Excel impact: Applying a card updates the Registration sheet in memory, logs 'before -> after' on the Log sheet, "
                "and pushes an Undo state (Ctrl+Z). Experienced curators can use 'Apply All' after verifying every card."
            ),
            validator=lambda u: _has_applied_1001_change(u, initial_place, initial_date),
        ),
        ActionStep(
            step_id="discrepancy_complete",
            title="Practice Complete!",
            instruction="You finished Historical Ledger Comparison! Click Finish ✓ to exit Practice Mode and return to your workspace.",
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "If a historical conflict cannot be resolved right now, it is completely fine to close the window and leave it for a specialist later."
            ),
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Historical Ledger Comparison", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
