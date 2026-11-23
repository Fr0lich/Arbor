"""
ui/tutorials/database_tutorial.py

Action-driven interactive tutorial for creating new collections and adding new specimens.
Operates strictly in an isolated in-memory sandbox without mutating real user files.
"""

from .sandbox_manager import SandboxManager, mark_tutorial_completed
from .tutorial_runner import TutorialRunner, ActionStep


def _has_typed_new_specimen_info(ui, initial_ids: set) -> bool:
    """Detect whether the user typed Genus or Collection Place on a newly added specimen."""
    app = getattr(ui, "app", None)
    oid = str(getattr(app, "current_object_id", "") or "")
    reg_vars = getattr(ui, "reg_vars", None) or {}
    if oid and oid not in initial_ids:
        for field in ("Genus", "Collection Place"):
            if field in reg_vars:
                try:
                    if str(reg_vars[field].get() or "").strip():
                        return True
                except Exception:
                    pass
    df_reg = getattr(app, "df_reg", None)
    if df_reg is not None:
        for idx in df_reg.index:
            if str(idx) not in initial_ids:
                for field in ("Genus", "Collection Place"):
                    if field in df_reg.columns:
                        try:
                            val = str(df_reg.loc[idx, field] or "").strip()
                            if val and val.lower() not in ("nan", "none"):
                                return True
                        except Exception:
                            pass
    return False


def start_database_tutorial(ui, on_complete=None):
    """Initializes clean minimal sandbox and starts the Creating Collections & Specimens tutorial."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="database")

    initial_count = len(ui.app.df_reg) if ui.app.df_reg is not None else 0
    initial_ids = set(str(i) for i in ui.app.df_reg.index) if ui.app.df_reg is not None else set()

    def _finish_cb():
        mark_tutorial_completed("database")
        if callable(on_complete):
            on_complete()

    steps = [
        ActionStep(
            step_id="database_intro",
            title="Optional: Starting a New Collection or Adding Objects",
            instruction=(
                "This short tour is optional — if you are working on an existing museum collection file, you can skip it.\n\n"
                "Use these steps when you need to create a brand-new collection file from scratch or register a specimen that isn't listed yet."
            ),
            action_hint="Click Next → to see how new collections and specimens are created.",
            details=(
                "Everything here runs inside a clean 2-specimen Practice Sandbox — your real collection files stay untouched."
            ),
        ),
        ActionStep(
            step_id="open_db_wizard",
            title="Creating a New Collection File",
            instruction="To start a brand-new collection, use FILE ▾ → New Database Wizard... (or '+ Create New Database' on startup) to generate a ready-to-use collection file with all standard fields.",
            action_hint="Click Next → to practice adding a new specimen.",
            details=(
                "Excel impact: Creates Registration, Observation, Log, and Unvalidated_source sheets with standard columns automatically — no manual spreadsheet setup required."
            ),
        ),
        ActionStep(
            step_id="add_new_object",
            title="Add a New Specimen Record",
            instruction="Click SPECIMEN ▾ → New Specimen Object... in the top bar (or press Ctrl+N) to add a fresh specimen row to this collection.",
            action_hint="Press Ctrl+N or click SPECIMEN ▾ → New Specimen Object... (or Skip Step →).",
            keycaps=["Ctrl", "N"],
            details=(
                "Excel impact: Appends a new unique ObjectID row to both the Registration and Observation sheets in memory."
            ),
            validator=lambda u: bool(
                u.app.df_reg is not None and len(u.app.df_reg) > initial_count
            ),
        ),
        ActionStep(
            step_id="enter_specimen_data",
            title="Fill In Specimen Details & Location",
            instruction=(
                "Click into the highlighted Registration Form on the right and type a Genus or Collection Place for your new specimen. "
                "When you're ready to record where it sits, press Ctrl+L to jump straight to Storage Location."
            ),
            target_id="object_editor_frame",
            action_hint="Type into Genus or Collection Place (or click Skip Step →).",
            keycaps=["Ctrl", "L"],
            details=(
                "In real workbooks, Arbor creates a rolling safety backup in .arbor_backups/ every time you press Ctrl+S."
            ),
            validator=lambda u: _has_typed_new_specimen_info(u, initial_ids),
        ),
        ActionStep(
            step_id="database_complete",
            title="Practice Complete!",
            instruction="You have practiced creating collections and adding new specimens safely in Practice Mode. Click Finish ✓ to return to your workspace.",
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "You can replay any step of the Suggested Learning Path anytime from HELP ▾ or by pressing F1."
            ),
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Collections & New Specimens", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
