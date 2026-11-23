"""
ui/tutorials/review_tutorial.py

Action-driven interactive 3-Minute Quick Tour introducing Arbor's Desktop & Mobile roles,
reading real object photos (#110), evaluating 3-source historical suggestions (#198),
flagging physical condition issues (Other Issue), and the physical-inspection rule for
Mark as Reviewed. Operates strictly in an isolated in-memory sandbox.
"""

from .sandbox_manager import SandboxManager, mark_tutorial_completed
from .tutorial_runner import TutorialRunner, ActionStep


def _get_collection_date_value(ui, oid: str) -> str:
    """Safely read Collection Date from the active form or DataFrame."""
    app = getattr(ui, "app", None)
    curr_oid = str(getattr(app, "current_object_id", "") or "")
    reg_vars = getattr(ui, "reg_vars", None) or {}
    if curr_oid == str(oid) and "Collection Date" in reg_vars:
        try:
            val = str(reg_vars["Collection Date"].get() or "").strip()
            if val:
                return val
        except Exception:
            pass
    df_reg = getattr(app, "df_reg", None)
    if df_reg is not None and str(oid) in df_reg.index and "Collection Date" in df_reg.columns:
        try:
            return str(df_reg.loc[str(oid), "Collection Date"] or "").strip()
        except Exception:
            pass
    return ""


def _is_110_date_entered(ui) -> bool:
    """Accept 00.06.1910 or 06.1910 for object #110 ('juni 1910')."""
    val = _get_collection_date_value(ui, "110")
    return val in ("00.06.1910", "06.1910")


def _is_198_date_fixed(ui) -> bool:
    """Accept 1927 or 00.00.1927 for object #198."""
    val = _get_collection_date_value(ui, "198")
    return val in ("1927", "00.00.1927")


def _is_other_problem_flagged(ui) -> bool:
    """Check whether Other_problem ('Other Issue') is flagged on the active specimen."""
    prob_vars = getattr(ui, "problem_vars", None) or {}
    if "Other_problem" in prob_vars:
        try:
            if bool(prob_vars["Other_problem"].get()):
                return True
        except Exception:
            pass
    app = getattr(ui, "app", None)
    df_obs = getattr(app, "df_obs", None)
    oid = getattr(app, "current_object_id", None)
    if df_obs is not None and oid in df_obs.index and "Other_problem" in df_obs.columns:
        try:
            return bool(df_obs.loc[oid, "Other_problem"])
        except Exception:
            pass
    return False


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


def start_review_tutorial(ui, on_complete=None):
    """Initializes zero-fear practice sandbox with real photos (#110, #198) and starts the 3-Minute Quick Tour."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="review")

    def _finish_cb():
        mark_tutorial_completed("review")
        if callable(on_complete):
            on_complete()

    steps = [
        ActionStep(
            step_id="welcome_overview",
            title="0. Welcome to Arbor (Desktop & Mobile)",
            instruction=(
                "Arbor has two parts that work together:\n"
                "• Desktop (here): Look up specific objects, inspect photos, edit registered info, compare historical ledgers, and triage issues.\n"
                "• Mobile Companion (on your phone): Walk the collection to fix simple issues & mark objects Reviewed, locate already-reviewed objects for closer inspection, or loan out objects.\n\n"
                "Everything in this tour runs in safe Practice Mode — real museum files are never touched."
            ),
            action_hint="Click Next → to begin with object #110.",
            details=(
                "You can exit Practice Mode anytime from the green banner at the top of the window, "
                "or replay any tutorial in order from HELP ▾ → Learning Path."
            ),
        ),
        ActionStep(
            step_id="transcribe_110_date",
            title="1. Read Object #110 & Fill Missing Date",
            instruction=(
                "Arbor's core job is showing what the museum already has registered for each object. "
                "Imagine you found object #110 and want to check its data — here we use photos to show you #110 "
                "(in real work you won't always have photos and will look at the physical object itself).\n\n"
                "Collection Date is blank on the right. Look at the photos of #110, find the date ('juni 1910'), and type it in.\n"
                "Format: DAY.MONTH.YEAR — use '00' for unknown parts (e.g. 1 Aug 2015 → 01.08.2015, Aug 2015 → 00.08.2015, year only → 2015)."
            ),
            target_id="reg_field:Collection Date",
            action_hint="Type 00.06.1910 (or 06.1910) in Collection Date.",
            details=(
                "Excel impact: Updates 'Collection Date' on the Registration sheet in memory. "
                "Notice #110 has no historical ledger entries — most routine checks compare registered data directly against the physical object."
            ),
            validator=_is_110_date_entered,
        ),
        ActionStep(
            step_id="select_198",
            title="2. Pull Object #198",
            instruction=(
                "Now let's check a second object that DOES have earlier historical data registered. "
                "Click specimen #198 in the Specimen Directory (or press Ctrl+F and type 198)."
            ),
            target_id="search_entry",
            action_hint="Click specimen #198 in the Specimen Directory.",
            keycaps=["Ctrl", "F"],
            details=(
                "Arbor matches object numbers even without leading zeros or prefixes (e.g. '0198' or '198'). "
                "Selecting #198 loads its front/back photos, registered fields, and historical ledger indicator."
            ),
            validator=lambda u: str(getattr(getattr(u, "app", None), "current_object_id", "") or "") == "198",
        ),
        ActionStep(
            step_id="check_198_history",
            title="3. Compare 3 Historical Sources (#198)",
            instruction=(
                "For #198, earlier historical data is registered! Click the highlighted History indicator (or press Ctrl+H) "
                "to see if it aligns with what is written on object #198.\n\n"
                "Notice the 3 sources disagree: Current (1963), Ledger Book 1 (1927), and Old Card Catalog (1912). "
                "Older ledgers can be wrong too — apply or type 1927 (or 00.00.1927) because it matches the physical object."
            ),
            target_id="history_indicator_label",
            action_hint="Open Ctrl+H and apply 1927 (or type 1927 / 00.00.1927 in Collection Date).",
            keycaps=["Ctrl", "H"],
            details=(
                "Historical suggestions are clues, never automatic truth. Always compare them against the physical object or its label "
                "before applying a change."
            ),
            validator=_is_198_date_fixed,
        ),
        ActionStep(
            step_id="flag_other_issue",
            title="4. Flag a Physical Issue (Other Issue)",
            instruction=(
                "Most field flags in Arbor (like missing dates or conflicting labels) are flagged automatically by the program. "
                "When you spot a physical condition issue yourself — like #198's bent display — check 'Other Issue' "
                "(press Space) and optionally jot a short note (e.g. 'Bent display') in Comment."
            ),
            target_id="problem_flags_frame",
            action_hint="Check 'Other Issue' (or click Skip Step →).",
            keycaps=["Space"],
            details=(
                "Excel impact: Sets 'Other_problem = TRUE' on the Observation sheet. "
                "You don't need to fix physical damage yourself — flagging it queues the object safely for follow-up later."
            ),
            validator=_is_other_problem_flagged,
        ),
        ActionStep(
            step_id="mark_reviewed",
            title="5. Only Mark Reviewed After Physical Inspection",
            instruction=(
                "Important rule: ONLY click '✓ Mark as Reviewed' when you have finished physically inspecting the object — "
                "never just because you fixed a date from historical suggestions at your desk.\n\n"
                "Since you have physically checked #198, press Ctrl+Enter or click '✓ Mark as Reviewed'. "
                "The card turns amber [REV+ERR] — checked by a human, with the open issue safely queued."
            ),
            target_id="reviewed_button",
            action_hint="Click '✓ Mark as Reviewed' or press Ctrl+Enter.",
            keycaps=["Ctrl", "Enter"],
            details=(
                "You won't always be able to solve every flagged problem yourself — and that is completely okay! "
                "Marking Reviewed confirms a human verified the physical object, while the active flag keeps it in the amber [REV+ERR] queue."
            ),
            validator=lambda u: _is_current_specimen_reviewed(u),
        ),
        ActionStep(
            step_id="review_complete",
            title="6. Practice Complete!",
            instruction=(
                "Great job! Everything here ran in Practice Mode — your real museum files were never touched. "
                "Click Finish ✓ to return to your workspace.\n\n"
                "Ready for more? Open HELP ▾ → Suggested Learning Path for Step 2 (Historical Ledger Comparison) "
                "or Step 3 (Mobile Companion Hallway Guide)."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode.",
            details=(
                "You can replay this tour or follow the full 5-step Learning Path anytime from HELP ▾ or by pressing F1."
            ),
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="3-Minute Quick Tour", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
