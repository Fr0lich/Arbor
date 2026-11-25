"""
ui/tutorials/triage_tutorial.py

Optional / Advanced Tutorial — Batch Problem Queue (One-by-One Desk Review).
Independent of the 2-part Core Introduction. Runs LIVE on the user's real collection by
default (use_sandbox=False), with a 1-click Practice Mode fallback (mock_type="triage").
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


def _count_live_rev_err(ui) -> int:
    """Count actionable REV+ERR specimens in the active workbook (excluding Needs Specialist only)."""
    try:
        app = getattr(ui, "app", None)
        df_obs = getattr(app, "df_obs", None)
        if df_obs is None or df_obs.empty or "Reviewed" not in df_obs.columns:
            return 0
        rev_mask = df_obs["Reviewed"].fillna(False).astype(bool)
        prob_cols = [c for c in df_obs.columns if c.endswith("_Problem") and c != "Other_problem"]
        if not prob_cols:
            return 0
        prob_mask = df_obs[prob_cols].fillna(False).astype(bool).any(axis=1)
        return int((rev_mask & prob_mask).sum())
    except Exception:
        return 0


def _is_2002_date_flag_cleared(ui) -> bool:
    """Detect whether sandbox #2002's Collection_Date_Problem flag has been cleared."""
    app = getattr(ui, "app", None)
    df_obs = getattr(app, "df_obs", None)
    if df_obs is not None and "2002" in df_obs.index and "Collection_Date_Problem" in df_obs.columns:
        try:
            val = df_obs.loc["2002", "Collection_Date_Problem"]
            return not bool(val) or str(val).lower() in ("false", "0", "nan", "none")
        except Exception:
            pass
    return False


def start_triage_tutorial(ui, on_complete=None, use_sandbox: bool = False):
    """Starts the optional Advanced tutorial: Batch Problem Queue (Live by default, or Practice Mode)."""
    sm = SandboxManager()
    if use_sandbox:
        sm.enter_sandbox(ui, mock_type="triage")

    live_rev_err_count = _count_live_rev_err(ui)

    def _finish_cb():
        mark_tutorial_completed("triage")
        if callable(on_complete):
            on_complete()

    def _switch_to_sandbox(runner):
        runner._cleanup()
        start_triage_tutorial(ui, on_complete=on_complete, use_sandbox=True)

    def _launch_database_tutorial(runner):
        from .database_tutorial import start_database_tutorial
        runner.finish_tutorial()
        start_database_tutorial(ui)

    if use_sandbox:
        intro_text = (
            "Practice Mode loaded! This optional guide shows how to use Arbor's Problem Queue to step through "
            "objects with flagged problems one by one.\n\n"
            "Here are 4 sample objects:\n"
            "• #2001 ([REV+NOTE] — Needs Specialist) and #2004 ([REV] — clean) stay out of the queue automatically.\n"
            "• #2002 ([REV+ERR]) has a false-alarm date flag you can clear in 1 click.\n"
            "• #2003 ([REV+ERR]) has a blank date with 2 conflicting older books to compare."
        )
        intro_buttons = []
        badge_text = "🛡️ ADVANCED · PRACTICE MODE"
    else:
        if live_rev_err_count > 0:
            intro_text = (
                "This optional advanced guide shows how to use Arbor's Problem Queue to step through objects "
                f"with flagged problems one by one. You currently have {live_rev_err_count} reviewed object(s) "
                "with actionable flags ([REV+ERR]) in your workspace.\n\n"
                "Clean [REV] objects and specialist-only [REV+NOTE] objects stay out of the queue automatically."
            )
        else:
            intro_text = (
                "This optional advanced guide shows how to filter your collection and step through objects "
                "with flagged problems one by one using the Problem Queue.\n\n"
                "You currently have 0 [REV+ERR] objects open. You can still look through the tools on your "
                "workspace, or click below to try it on safe sample data first."
            )
        intro_buttons = [
            ("🛡️ Practice with Sample Data Instead", _switch_to_sandbox, live_rev_err_count == 0),
        ]
        badge_text = "⚡ ADVANCED · LIVE WORKSPACE"

    steps = [
        ActionStep(
            step_id="triage_intro",
            title="Batch Problem Queue — Stepping Through Flagged Objects",
            instruction=intro_text,
            action_hint="Click Next → to see how to narrow your list with Filter (Ctrl+G).",
            details=(
                "Notice how Needs Specialist ([REV+NOTE]) is separated from actionable data errors ([REV+ERR]): "
                "the default Problem Queue focuses on fixable desk issues, while specialists can opt into Needs Specialist anytime."
            ),
            action_buttons=intro_buttons,
        ),
        ActionStep(
            step_id="triage_filter",
            title="Filter to Just Your Follow-Up List (Ctrl+G)",
            instruction=(
                "Press Ctrl+G (Filter) and pick 'Hallway Follow-Up (REV+ERR)' — or press Ctrl+K and type 'Hallway Follow-Up'.\n\n"
                "This hides clean [REV] and specialist-only [REV+NOTE] items so only actionable [REV+ERR] objects remain."
            ),
            action_hint="Press Ctrl+G (or Ctrl+K → Hallway Follow-Up), then click Next →.",
            keycaps=["Ctrl", "G"],
            details=(
                "Tip: Under Filter → Archival Gaps (ICEDIG), you can also filter directly by canonical ICEDIG codes "
                "(unknown:missing, unknown:indecipherable, unknown:undigitized, withheld) whenever you want to review archival gaps later."
            ),
        ),
        ActionStep(
            step_id="triage_open_queue",
            title="Open Problem Resolution in Queue Mode",
            instruction=(
                "In Part 1 you opened Problem Resolution on one object (Ctrl+H). For a whole shift's batch, "
                "click TOOLS ▾ → Open Problem Queue & Resolver... → OPEN QUEUE (or Ctrl+K → Triage Problem Queue).\n\n"
                "Notice 'Needs Specialist' is unchecked by default so you focus on actionable errors (specialists can opt in anytime)."
            ),
            target_id="tools_nav_btn",
            action_hint="Open Problem Resolution Queue (or click Skip Step →).",
            keycaps=["Ctrl", "K"],
            details=(
                "Queue mode lets you step through dozens of flagged objects in one streamlined window without hunting through the Specimen Directory."
            ),
            validator=_is_problem_queue_open,
        ),
        ActionStep(
            step_id="triage_queue_tools",
            title="Batch Desk Tools Inside Queue Mode",
            instruction=(
                "Inside Problem Resolution (Queue Mode), you have 4 fast desk tools:\n"
                "• Alt+← / Alt+→ (or SKIP OBJECT →): Step between queued objects\n"
                "• ✓ Value is Correct (Clear Flag): Clear false alarms in 1 click (turns [REV] without editing text)\n"
                "• Left Sidebar + Historical Suggestions (+ Old Names / GBIF in TOOLS ▾ or Ctrl+K): Resolve multi-field conflicts across older books\n"
                "• ICEDIG ▾ dropdown: Set unknown:missing / unknown:indecipherable when confirmed absent with NO conflicting older books"
            ),
            target_id="hr_cards",
            action_hint=(
                "Clear #2002's flag with '✓ Value is Correct' and explore #2003 (or click Skip Step →)."
                if use_sandbox
                else "Try these tools on your queued objects, then click Next → when ready."
            ),
            keycaps=["Alt", "→"],
            details=(
                "Every Apply and Clear Flag supports Undo (Ctrl+Z). Never set unknown:missing if older catalog books still disagree — resolve or leave [REV+ERR] instead."
            ),
            validator=_is_2002_date_flag_cleared if use_sandbox else None,
        ),
        ActionStep(
            step_id="triage_complete",
            title="Batch Problem Queue Guide Complete!",
            instruction=(
                "Click 'Save Edits' or 'Close Queue' when finished, and press Ctrl+S to save your Excel workbook.\n\n"
                "You can use this queue anytime you want to step through flagged objects one by one — "
                "and if you're cleaning up unreviewed [UNREV] older-book conflicts at your desk, just leave "
                "'Reviewed' unchecked until someone physically inspects the real object."
            ),
            action_hint="Click 'Finish ✓' below to close this guide.",
            keycaps=["Ctrl", "S"],
            details=(
                "Need to create a brand-new collection file or add a missing specimen record? "
                "Open HELP → Interactive Tutorials → Optional & Advanced Tutorials anytime."
            ),
            action_buttons=[
                ("📁 Optional: Collections & New Specimens", _launch_database_tutorial, False),
            ],
        ),
    ]

    runner = TutorialRunner(
        ui,
        steps,
        tutorial_name="Batch Problem Queue (Advanced)",
        on_complete=_finish_cb,
        use_sandbox=use_sandbox,
        badge_text=badge_text,
    )
    if use_sandbox:
        sm._active_runner = runner
    return runner
