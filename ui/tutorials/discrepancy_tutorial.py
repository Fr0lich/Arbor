"""
ui/tutorials/discrepancy_tutorial.py

Action-driven interactive tutorial for comparing specimens against historical ledgers and GBIF.
Operates strictly in an isolated in-memory sandbox without mutating real user files.
"""

from .sandbox_manager import SandboxManager
from .tutorial_runner import TutorialRunner, ActionStep


def start_discrepancy_tutorial(ui, on_complete=None):
    """Initializes sandbox and starts the Historical Ledger Comparison tutorial."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="discrepancy")

    if hasattr(ui, "load_object"):
        try:
            ui.load_object("1001")
        except Exception:
            pass

    steps = [
        ActionStep(
            step_id="open_resolver",
            title="1. Open Historical Ledger Comparison",
            instruction="Click the highlighted history indicator above the form (or press Ctrl+H) to open Historical Ledger Comparison.",
            target_id="history_indicator_label",
            action_hint="Click the history indicator or press Ctrl+H.",
            keycaps=["Ctrl", "H"],
            details=(
                "Whenever a loaded historical ledger book disagrees with the current specimen sheet, "
                "Arbor flags it with a slate-blue [CFCT] badge so you can compare both versions side by side."
            ),
            validator=lambda u: bool(
                getattr(u, "_current_resolver_win", None) or
                any(getattr(w, "tutorial_id", "") == "hr_sidebar" for w in u.root.winfo_children() if hasattr(w, "winfo_children"))
            )
        ),
        ActionStep(
            step_id="field_directory",
            title="2. Browse Fields That Disagree",
            instruction="The left sidebar lists every field where the current workbook differs from historical ledgers. Click any field to jump straight to its card.",
            target_id="hr_sidebar",
            action_hint="Inspect the field sidebar, then click Next →.",
            details=(
                "You never have to change a field if you aren't sure — only fields you explicitly select or apply are updated."
            ),
        ),
        ActionStep(
            step_id="select_resolution",
            title="3. Pick the Confirmed Value",
            instruction="Each card shows the current Excel value alongside historical ledger suggestions. Click a suggested card to load that value into the box.",
            target_id="hr_cards",
            action_hint="Click a suggested value card, then click Next →.",
            details=(
                "Excel impact: Clicking a suggestion previews it in the field input. Nothing is written to the Registration sheet until you click Apply."
            ),
        ),
        ActionStep(
            step_id="apply_changes",
            title="4. Apply Confirmed Changes",
            instruction="Click 'Apply' on a card (or 'Apply All') to update the specimen and automatically clear its mapped problem flag.",
            target_id="hr_apply_all",
            action_hint="Click 'Apply' or Next → to finish.",
            details=(
                "Every applied fix records a 'before -> after' entry in the Log sheet and pushes an Undo state so Ctrl+Z can reverse it cleanly."
            ),
        ),
        ActionStep(
            step_id="discrepancy_complete",
            title="5. Practice Complete!",
            instruction="You finished the Historical Ledger Comparison walkthrough. Click Finish ✓ to exit Practice Mode and return to your workspace.",
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "Remember: if a historical conflict cannot be resolved right now, it is completely fine to close the window and leave the flag active for a specialist later."
            ),
        )
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Historical Ledger Comparison", on_complete=on_complete)
    sm._active_runner = runner
    return runner
