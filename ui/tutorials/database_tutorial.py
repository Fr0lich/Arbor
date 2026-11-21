"""
ui/tutorials/database_tutorial.py

Action-driven interactive tutorial for creating new collections and adding new specimens.
Operates strictly in an isolated in-memory sandbox without mutating real user files.
"""

from .sandbox_manager import SandboxManager
from .tutorial_runner import TutorialRunner, ActionStep


def start_database_tutorial(ui, on_complete=None):
    """Initializes sandbox and starts the Creating Collections & Specimens tutorial."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="review")

    initial_count = len(ui.app.df_reg) if ui.app.df_reg is not None else 0

    steps = [
        ActionStep(
            step_id="open_db_wizard",
            title="1. Creating a New Collection Workbook",
            instruction="When starting a brand-new collection, use File → New Database (or '+ Create New Database' on startup) to generate a clean 4-sheet Excel workbook.",
            action_hint="Click Next → to practice adding a specimen.",
            details=(
                "Excel impact: Creates Registration, Observation, Log, and Unvalidated_source sheets with standard columns automatically — no manual spreadsheet setup required."
            ),
        ),
        ActionStep(
            step_id="add_new_object",
            title="2. Add a New Specimen Record",
            instruction="Press Ctrl+N (or right-click in the Specimen Directory and choose 'New Object') to add a fresh specimen row.",
            action_hint="Press Ctrl+N (or click Skip Step →).",
            keycaps=["Ctrl", "N"],
            details=(
                "Excel impact: Appends a new unique ObjectID row to both the Registration and Observation sheets in memory."
            ),
            validator=lambda u: bool(
                u.app.df_reg is not None and len(u.app.df_reg) > initial_count
            )
        ),
        ActionStep(
            step_id="enter_specimen_data",
            title="3. Fill In Specimen Details",
            instruction="Click into the highlighted Registration Form on the right to type Genus, Species, Collector, or Collection Place.",
            target_id="object_editor_frame",
            action_hint="Type into any field, then click Next →.",
            details=(
                "Tip: Press Ctrl+L or F4 anytime to jump straight to Storage Location (Building, Floor, Cabinet, Shelf)."
            ),
        ),
        ActionStep(
            step_id="database_complete",
            title="4. Practice Complete!",
            instruction="You have practiced creating collections and adding new specimens safely in Practice Mode. Click Finish ✓ to return to your workspace.",
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "In real workbooks, Arbor creates a rolling backup in .arbor_backups/ every time you press Ctrl+S."
            ),
        )
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Collections & New Specimens", on_complete=on_complete)
    sm._active_runner = runner
    return runner
