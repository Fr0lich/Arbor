"""
ui/tutorials/discrepancy_tutorial.py

Action-driven interactive tutorial for comparing specimens against conflicting historical ledgers
inside the Problem Resolution window. Operates strictly in an isolated in-memory sandbox without
mutating real user files.
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


def _is_resolver_open(ui) -> bool:
    """Detect whether the Problem Resolution window is currently open."""
    win = getattr(ui, "_current_resolver_win", None)
    if win is not None:
        try:
            if win.winfo_exists():
                return True
        except Exception:
            pass
    root = getattr(ui, "root", None)
    if _has_widget_with_tutorial_id(root, "hr_sidebar"):
        return True
    if root is not None:
        try:
            for w in root.winfo_children():
                title = str(getattr(w, "title", lambda: "")())
                if "Problem Resolution" in title:
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

    def _ensure_history_pill(u):
        try:
            if hasattr(u, "update_history_indicator"):
                u.update_history_indicator("1001")
        except Exception:
            pass

    if hasattr(ui, "load_object"):
        try:
            ui.load_object("1001")
        except Exception:
            pass
    _ensure_history_pill(ui)

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

    def _launch_triage_tutorial(runner):
        from .triage_tutorial import start_triage_tutorial
        mark_tutorial_completed("discrepancy")
        if callable(on_complete):
            try:
                on_complete()
            except Exception:
                pass
        start_triage_tutorial(ui)

    def _launch_mobile_guide(runner):
        from .micro_guides import start_armed_shelf_guide
        runner.finish_tutorial()
        start_armed_shelf_guide(ui)

    steps = [
        ActionStep(
            step_id="discrepancy_intro",
            title="When to Compare Older Catalog Books",
            instruction=(
                "Use this workflow at your desk when older museum catalog books disagree with multiple fields in your "
                "currently registered collection.\n\n"
                "In this Practice Mode, specimen #1001 is compared against TWO older books that disagree with each other — "
                "so you can practice evaluating historical clues carefully."
            ),
            action_hint="Click Next → to open the Problem Resolution window.",
            details=(
                "Remember: comparing older books at your desk is NOT a physical inspection of the object, "
                "so leave 'Reviewed' unchecked unless you also inspect the physical object itself."
            ),
        ),
        ActionStep(
            step_id="open_resolver",
            title="Open Problem Resolution",
            instruction=(
                "Click the highlighted History button above the registration form (or press Ctrl+H) "
                "to open the Problem Resolution window."
            ),
            target_id="history_indicator_label",
            action_hint="Click the History button or press Ctrl+H.",
            keycaps=["Ctrl", "H"],
            on_enter=_ensure_history_pill,
            details=(
                "Whenever older catalog books disagree with your current record, Arbor shows the History button "
                "and a slate-blue [CFCT] badge so you can compare versions side by side."
            ),
            validator=_is_resolver_open,
        ),
        ActionStep(
            step_id="field_directory",
            title="Browse Fields That Disagree",
            instruction=(
                "The left sidebar lists every field where your current record differs from older catalog books. "
                "Click any field to jump straight to its card."
            ),
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
                "Each card shows your currently registered value on top alongside Historical Suggestions from older books below. "
                "Notice Book 1 and Book 2 disagree with each other! Click a suggestion to preview it in the input box."
            ),
            target_id="hr_cards",
            action_hint="Click a suggested value to preview it, then click Next →.",
            details=(
                "Clicking a suggestion only previews it — nothing is changed until you click Apply. "
                "Tip: Unsure if a plant name from an older book is just an older synonym? You can check it anytime with 'Old Names & Synonyms'."
            ),
        ),
        ActionStep(
            step_id="apply_changes",
            title="Apply One Card (Without Marking Reviewed)",
            instruction=(
                "Click 'Apply' on a single confirmed card (avoid clicking 'Apply All Resolved' until you have checked every card).\n\n"
                "Important: fixing data from older books at your desk does NOT count as a physical review — "
                "leave 'Reviewed' unchecked until someone inspects the physical object."
            ),
            target_id="hr_cards",
            action_hint="Click 'Apply' on a card (or click Skip Step →).",
            details=(
                "Applying a card updates the record in memory, records 'before -> after' in the Log, "
                "and supports Undo (Ctrl+Z)."
            ),
            validator=lambda u: _has_applied_1001_change(u, initial_place, initial_date),
        ),
        ActionStep(
            step_id="close_discrepancy_resolver",
            title="Save & Close Problem Resolution",
            instruction=(
                "Nice! Your confirmed change is applied.\n\n"
                "Click the highlighted \"Apply All Resolved\" button to save your changes and close the Problem Resolution window."
            ),
            target_id="hr_apply_all",
            action_hint="Click \"Apply All Resolved\" to save and close.",
            validator=lambda u: not _is_resolver_open(u),
        ),
        ActionStep(
            step_id="discrepancy_complete",
            title="Practice Complete!",
            instruction=(
                "Great job! You now know how to compare multiple older catalog books inside Problem Resolution.\n\n"
                "If a conflict cannot be resolved right now, it is completely fine to leave it for a specialist later.\n\n"
                "Click Finish ✓ to return to your workspace, or jump straight into another guide below."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode, or launch another guide above.",
            action_buttons=[
                ("🎯 Office Triage (REV+ERR)", _launch_triage_tutorial, True),
                ("📱 Mobile Companion Hallway Guide", _launch_mobile_guide, False),
            ],
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Historical Ledger Comparison", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
