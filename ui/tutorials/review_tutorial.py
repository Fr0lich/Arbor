"""
ui/tutorials/review_tutorial.py

Part 1 of 3 — Desktop Basics (formerly 3-Minute Quick Tour).
Action-driven interactive Practice Mode walkthrough introducing Arbor's complete
3-Way Curatorial Mental Model on real specimen photos (#110 & #198):
  1. Checking Registration Data & fixing/resolving older catalog conflicts (#110, #198)
  2. Recording confirmed-blank/unreadable fields with canonical ICEDIG codes via ⋯ (#198 Collector)
  3. Escalating physical damage via Needs Specialist -> calm teal [REV+NOTE] (#198 bent wire)
Operates strictly in an isolated in-memory sandbox.
"""

from .sandbox_manager import SandboxManager, mark_tutorial_completed
from .tutorial_runner import TutorialRunner, ActionStep


def _get_field_value(ui, oid: str, field_name: str) -> str:
    """Safely read a Registration field from the active form or DataFrame."""
    app = getattr(ui, "app", None)
    curr_oid = str(getattr(app, "current_object_id", "") or "")
    reg_vars = getattr(ui, "reg_vars", None) or {}
    if curr_oid == str(oid) and field_name in reg_vars:
        try:
            val = str(reg_vars[field_name].get() or "").strip()
            if val:
                return val
        except Exception:
            pass
    reg_entries = getattr(ui, "reg_entries", None) or {}
    if curr_oid == str(oid) and field_name in reg_entries:
        try:
            w = reg_entries[field_name]
            if hasattr(w, "get"):
                val = str(w.get() or "").strip()
                if val:
                    return val
        except Exception:
            pass
    df_reg = getattr(app, "df_reg", None)
    if df_reg is not None and field_name in df_reg.columns:
        for key in (str(oid), int(oid) if str(oid).isdigit() else None):
            if key is not None and key in df_reg.index:
                try:
                    return str(df_reg.loc[key, field_name] or "").strip()
                except Exception:
                    pass
    return ""


def _get_collection_date_value(ui, oid: str) -> str:
    """Safely read Collection Date from the active form or DataFrame."""
    return _get_field_value(ui, oid, "Collection Date")


def _is_110_date_entered(ui) -> bool:
    """Accept 00.06.1910, 06.1910, 00.6.1910, 6.1910, 1910, or 00.00.1910 for object #110 ('juni 1910')."""
    raw = _get_collection_date_value(ui, "110")
    if not raw:
        return False
    norm = raw.replace("-", ".").replace("/", ".").replace(" ", ".")
    while ".." in norm:
        norm = norm.replace("..", ".")
    norm = norm.strip(".")
    return norm in ("00.06.1910", "06.1910", "00.6.1910", "6.1910", "1910", "00.00.1910")


def _is_198_date_fixed(ui) -> bool:
    """Accept 1927 or 00.00.1927 for object #198."""
    val = _get_collection_date_value(ui, "198")
    return val in ("1927", "00.00.1927")


def _is_198_collector_icedig_set(ui) -> bool:
    """Accept canonical ICEDIG code unknown:missing (or ?m) for #198's blank Collector."""
    val = _get_field_value(ui, "198", "Collector").lower()
    return val in ("unknown:missing", "?m")


def _is_other_problem_flagged(ui) -> bool:
    """Check whether Other_problem ('Needs Specialist') is flagged on the active specimen."""
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


def _is_specimen_reviewed(ui, target_oid: str | None = None) -> bool:
    """Safely check whether the given (or active) specimen in the sandbox is marked Reviewed."""
    app = getattr(ui, "app", None)
    curr_oid = str(getattr(app, "current_object_id", "") or "")
    oid = str(target_oid) if target_oid is not None else curr_oid
    if not oid:
        return False
    if curr_oid == oid and getattr(ui, "reviewed_var", None) and ui.reviewed_var.get():
        return True
    df_obs = getattr(app, "df_obs", None)
    if df_obs is None:
        return False
    for key in (oid, int(oid) if oid.isdigit() else None):
        if key is not None and key in df_obs.index:
            try:
                return bool(df_obs.loc[key].get("Reviewed", False))
            except Exception:
                pass
    return False


def _is_current_specimen_reviewed(ui) -> bool:
    """Backwards-compatible wrapper checking whether the active specimen is marked Reviewed."""
    return _is_specimen_reviewed(ui, None)


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
    """Detect whether the Problem Resolution / Historical Comparison window is currently open."""
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


def _is_problems_tab_active(ui) -> bool:
    """Return True if the Problems tab in reg_notebook is currently selected."""
    try:
        nb = getattr(ui, "reg_notebook", None)
        tabs = getattr(ui, "_reg_tabs", None) or {}
        if nb is None or "Problems" not in tabs:
            return False
        prob_container = tabs["Problems"].get("container")
        if prob_container is None:
            return False
        return str(nb.select()) == str(prob_container)
    except Exception:
        return False


def _problems_tab_bbox(ui):
    """Compute exact screen (x, y, w, h) of the 'Problems' tab header in reg_notebook."""
    try:
        nb = getattr(ui, "reg_notebook", None)
        tabs = getattr(ui, "_reg_tabs", None) or {}
        if nb is None or "Problems" not in tabs or not nb.winfo_exists() or not nb.winfo_viewable():
            return None
        prob_container = str(tabs["Problems"]["container"])
        all_tabs = [str(t) for t in nb.tabs()]
        if prob_container not in all_tabs:
            return None
        target_idx = all_tabs.index(prob_container)
        nb_w = nb.winfo_width()
        if nb_w <= 20:
            return None

        min_x = None
        max_x = None
        for x in range(2, nb_w, 4):
            try:
                if nb.index(f"@{x},10") == target_idx:
                    if min_x is None:
                        min_x = x
                    max_x = x
            except Exception:
                continue
        if min_x is None or max_x is None:
            return None

        mid_x = (min_x + max_x) // 2
        tab_h = 26
        for y in range(2, 44, 2):
            try:
                if nb.index(f"@{mid_x},{y}") == target_idx:
                    tab_h = y + 3
            except Exception:
                break

        return (
            nb.winfo_rootx() + max(0, min_x - 2),
            nb.winfo_rooty(),
            max(40, (max_x - min_x) + 8),
            max(20, tab_h),
        )
    except Exception:
        return None


def _step9_target_selector(ui):
    """Highlight the Problems tab header first, then the 'Needs Specialist' checkbox once opened."""
    if _is_problems_tab_active(ui):
        cb_map = getattr(ui, "problem_checkbutton_map", None) or {}
        if "Other_problem" in cb_map:
            return cb_map["Other_problem"]
        return "other_problem_checkbox"
    nb = getattr(ui, "reg_notebook", None)
    if nb is not None:
        return (nb, lambda: _problems_tab_bbox(ui))
    return "problem_flags_frame"


def _is_110_date_problem_checked(ui) -> bool:
    """Return True if Collection_Date_Problem is still checked on #110."""
    prob_vars = getattr(ui, "problem_vars", None) or {}
    if "Collection_Date_Problem" in prob_vars:
        try:
            return bool(prob_vars["Collection_Date_Problem"].get())
        except Exception:
            pass
    app = getattr(ui, "app", None)
    df_obs = getattr(app, "df_obs", None)
    if df_obs is not None and "Collection_Date_Problem" in df_obs.columns:
        for key in ("110", 110):
            if key in df_obs.index:
                try:
                    return bool(df_obs.loc[key, "Collection_Date_Problem"])
                except Exception:
                    pass
    return False


def _step4_target_selector(ui):
    """Highlight Collection Date's problem checkbox first, then '✓ Mark as Reviewed' once unchecked."""
    if _is_110_date_problem_checked(ui):
        inline_cbs = getattr(ui, "inline_problem_checkbuttons", None) or {}
        if "Collection_Date_Problem" in inline_cbs:
            return inline_cbs["Collection_Date_Problem"]
        return "inline_prob_Collection_Date_Problem"
    return "reviewed_button"


def _collector_icedig_target(ui):
    """Highlight Collector's per-field ⋯ ICEDIG button (falling back to Collector entry)."""
    btns = getattr(ui, "icedig_field_btns", None) or {}
    if "Collector" in btns:
        return btns["Collector"]
    return "icedig_collector_btn"


def start_review_tutorial(ui, on_complete=None):
    """Initializes zero-fear practice sandbox with real photos (#110, #198) and starts Part 1: Desktop Basics."""
    sm = SandboxManager()
    sm.enter_sandbox(ui, mock_type="review")

    def _focus_details_tab(u):
        try:
            nb = getattr(u, "reg_notebook", None)
            tabs = getattr(u, "_reg_tabs", None) or {}
            if nb is not None:
                if "Details" in tabs and isinstance(tabs["Details"], dict) and "container" in tabs["Details"]:
                    nb.select(tabs["Details"]["container"])
                elif nb.tabs():
                    nb.select(0)
        except Exception:
            pass

    def _finish_cb():
        mark_tutorial_completed("review")
        if callable(on_complete):
            on_complete()

    def _launch_mobile_guide(runner):
        from .micro_guides import start_armed_shelf_guide
        runner.finish_tutorial()
        start_armed_shelf_guide(ui)

    def _launch_triage_tutorial(runner):
        from .triage_tutorial import start_triage_tutorial
        runner.finish_tutorial()
        start_triage_tutorial(ui)

    steps = [
        ActionStep(
            step_id="welcome_overview",
            title="Part 1 of 3 — Desktop Basics",
            instruction=(
                "Welcome to Part 1! We are now in a safe Practice Mode with example objects, "
                "so real museum files are never touched.\n\n"
                "Over the next few minutes, you'll practice Arbor Desktop's core workflow on two real example objects:\n"
                "• How to read Registration Data and inspect photos\n"
                "• How to compare older historical records\n"
                "• What ICEDIG codes are, and how and when to use them\n"
                "• What to do when you find an issue you can't fix (Needs Specialist)\n"
                "• How and when to mark objects as Reviewed\n\n"
                "Tip: You can exit Practice Mode and end the tutorial anytime from the green banner at the top."
            ),
            action_hint="Click Next → to inspect your first object (#110).",
        ),
        ActionStep(
            step_id="orient_110",
            title="Registration Data (#110)",
            instruction=(
                "Let's take a look at Object #110, an Ephedra major.\n\n"
                "On the right side of the screen you can see the Registration Data fields. Here we see everything "
                "the museum currently has recorded for this object — both scientific data (Taxonomy), such as the "
                "species and genus, and information about who collected the object and where they found it.\n\n"
                "Next to many of the fields you will see a checkbox. A checked box means that Arbor or another user "
                "has documented a problem with that field — either missing information, or conflicting data from older sources.\n\n"
                "Arbor is designed to help you solve such problems."
            ),
            target_id="object_editor_frame",
            action_hint="Take a look at the Registration Data, then click Next →.",
            on_enter=_focus_details_tab,
        ),
        ActionStep(
            step_id="transcribe_110_date",
            title="Read Object #110 & Fill Missing Date",
            instruction=(
                "Notice that this object is missing a \"Collection Date\".\n\n"
                "If you look at the middle of the screen, you should see some photos of the object. See if you can "
                "use the photos of #110 to discover when it was collected. You can click the thumbnails underneath "
                "the main image to switch between images.\n"
                "Once you find the date, write it into the Collection Date field.\n\n"
                "Hint: When writing the date we use the format DAY.MONTH.YEAR using '00' for unknown parts. "
                "So 1 Aug 2015 → 01.08.2015, while Aug 2015 → 00.08.2015. "
                "If we only see the year, it is fine to write just 2015."
            ),
            target_id="reg_field:Collection Date",
            hud_avoid_photo=True,
            action_hint="Find the date on #110's photos and type it into Collection Date.",
            on_enter=_focus_details_tab,
            details=(
                "Excel impact: Updates 'Collection Date' on the Registration sheet in memory. "
                "Notice #110 has no historical ledger entries — most routine checks compare registered data directly against the physical object."
            ),
            answer=(
                "Look at the back photo of #110 — the handwritten label says 'juni 1910'. "
                "Since the day is unknown, type 00.06.1910 (or 06.1910) into Collection Date."
            ),
            validator=_is_110_date_entered,
        ),
        ActionStep(
            step_id="mark_110_reviewed",
            title="Mark Object #110 as Reviewed",
            instruction=(
                "Well done! You found the missing Collection Date.\n\n"
                "Let's uncheck the Collection Date problem box.\n\n"
                "Since we don't see any other problems with #110, we can go ahead and mark it as reviewed. "
                "Go ahead and click '✓ Mark as Reviewed' (or press Ctrl+Enter) to turn #110 green [REV].\n\n"
                "IMPORTANT: In this example we are marking the object as Reviewed after just looking at photos of the object. "
                "In real museum work you should only mark an object as Reviewed after you have physically inspected the real object. "
                "Some images may be outdated, so they should not be your primary source.\n\n"
                "In Arbor, \"Reviewed\" means \"A person has looked at this object and updated the Registration Data accordingly\"."
            ),
            target_id=_step4_target_selector,
            action_hint="Uncheck the Collection Date problem box, then click '✓ Mark as Reviewed' or press Ctrl+Enter.",
            keycaps=["Ctrl", "Enter"],
            details=(
                "Marking an object as Reviewed logs the date in the Log so the team knows this physical object has been checked."
            ),
            validator=lambda u: _is_specimen_reviewed(u, "110"),
        ),
        ActionStep(
            step_id="select_198",
            title="Search the Specimen Directory (#198)",
            instruction=(
                "Nice — Object #110 is now marked Reviewed!\n\n"
                "Now let's navigate to a different object.\n\n"
                "On the left is the Specimen Directory, where you can browse or search all objects.\n\n"
                "Click the search bar (or press Ctrl+F), type 198, and click Object #198."
            ),
            target_id="search_entry",
            action_hint="Search for 198 and click Object #198.",
            keycaps=["Ctrl", "F"],
            validator=lambda u: str(getattr(getattr(u, "app", None), "current_object_id", "") or "") == "198",
        ),
        ActionStep(
            step_id="open_198_history",
            title="Use the Historical Sources",
            instruction=(
                "Object #198 has two problems: Collector is blank, and Collection Date still has its problem checkbox "
                "checked even though a date is filled in.\n\n"
                "We'll handle Collector in a moment — let's look at Collection Date first. This time the date isn't "
                "missing: Arbor noticed that older historical sources list different years for this object.\n\n"
                "Click the highlighted History button (or press Ctrl+H) to open the Problem Resolution tool and see "
                "what those older records say."
            ),
            target_id="history_indicator_label",
            action_hint="Click the History button or press Ctrl+H.",
            keycaps=["Ctrl", "H"],
            on_enter=_focus_details_tab,
            validator=_is_resolver_open,
        ),
        ActionStep(
            step_id="resolve_198_date",
            title="Compare Sources & Apply the Right Year (#198)",
            instruction=(
                "This is the Problem Resolution window, where you can compare current values against older records side by side.\n\n"
                "While there is no historical data for the Collector issue, look at the Collection Date box — you'll see "
                "the current value on top and Historical Suggestions from older records below.\n\n"
                "Look back at the photos of #198 — do you spot the real collection date? Click the matching suggestion, "
                "then click Apply."
            ),
            target_id="hr_cards",
            action_hint="Click the matching suggestion for #198, then click Apply.",
            details=(
                "Historical suggestions are clues, never automatic truth. Always compare them against the physical object or its label "
                "before applying a change."
            ),
            answer=(
                "The 3 sources show Current (1963), Ledger Book 1 (1927), and Old Card Catalog (1912). "
                "Object #198's label says 1927 — apply 1927 from Ledger Book 1, or type 1927 (or 00.00.1927) into Collection Date."
            ),
            validator=_is_198_date_fixed,
        ),
        ActionStep(
            step_id="close_198_resolver",
            title="Save & Close Problem Resolution",
            instruction=(
                "Nice! The Collection Date for Object #198 is updated.\n\n"
                "Click the highlighted \"Save Edits\" button to save your changes and close the Problem Resolution window."
            ),
            target_id="hr_apply_all",
            action_hint="Click \"Save Edits\" to save and close.",
            validator=lambda u: not _is_resolver_open(u),
        ),
        ActionStep(
            step_id="mark_198_icedig",
            title="Confirmed Blank Labels — ICEDIG Menu (⋯)",
            instruction=(
                "Now let's look back at #198's Collector field.\n\n"
                "When we inspect the images of #198 we can't see a collector written anywhere, and none of our "
                "historical sources list one either.\n"
                "When a field is confirmed absent or unreadable on the label (with NO conflicting older records), "
                "click the quiet ⋯ button on the right edge of that field and choose unknown:missing "
                "(or unknown:indecipherable if the ink is unreadable).\n\n"
                "Click the highlighted ⋯ button next to Collector and pick unknown:missing."
            ),
            target_id=_collector_icedig_target,
            action_hint="Click ⋯ next to Collector and select unknown:missing.",
            on_enter=_focus_details_tab,
            details=(
                "Canonical ICEDIG codes (unknown:missing, unknown:indecipherable, unknown:undigitized, withheld) tell Arbor "
                "'confirmed — stop looking for it' and clear that field's problem box automatically (turning ⋯ amber). "
                "Important: NEVER set unknown:missing if older books still have conflicting values — leave the field flagged [REV+ERR] instead!"
            ),
            validator=_is_198_collector_icedig_set,
        ),
        ActionStep(
            step_id="flag_other_issue",
            title="If You Discover a Physical Issue (Needs Specialist)",
            instruction=(
                "Hang on, take another look at #198's first image.\n\n"
                "That metal wire looks pretty bent. It looks like we have spotted an issue with the physical condition of this object.\n\n"
                "That is something we should take note of.\n\n"
                "Let's note that so a specialist knows this object needs attention. "
                "Click on the Problems tab and check \"Needs Specialist\" (since this is physical damage, not a desk data error).\n\n"
                "Tip: You can also toggle \"Needs Specialist\" right above the Comment field on the General Data tab "
                "and tap a quick-tag pill (like + Damaged) to explain it in one click. The Comment field is at the bottom of the General Data tab."
            ),
            target_id=_step9_target_selector,
            action_hint="Click the Problems tab and check \"Needs Specialist\".",
            details=(
                "Excel impact: Sets 'Other_problem = TRUE' on the Observation sheet. "
                "Flagging 'Needs Specialist' gives the object a calm teal [REV+NOTE] badge (or indigo-slate [NOTE] when unreviewed) "
                "and keeps it out of the default trainee desk queue so specialists can filter for it directly."
            ),
            validator=_is_other_problem_flagged,
        ),
        ActionStep(
            step_id="mark_reviewed",
            title="Mark Object #198 as Reviewed (With Specialist Note)",
            instruction=(
                "Now let's mark Object #198 as Reviewed — click '✓ Mark as Reviewed' or press Ctrl+Enter. "
                "(Remember: in real museum work, only mark an object as Reviewed after physically inspecting the real object.)\n\n"
                "Because \"Needs Specialist\" is checked (and no data errors remain), #198 turns calm teal [REV+NOTE] "
                "instead of green [REV] or orange [REV+ERR]. That tells the team you inspected the object and fixed what you could, "
                "while leaving the bent wire safely flagged for a specialist.\n\n"
                "You've done everything you can here — the rest is for a specialist to handle later."
            ),
            target_id="reviewed_button",
            action_hint="Click '✓ Mark as Reviewed' or press Ctrl+Enter.",
            keycaps=["Ctrl", "Enter"],
            details=(
                "You won't always be able to solve every issue yourself — and that is completely okay! "
                "Marking Reviewed confirms a human verified the physical object, while 'Needs Specialist' marks it [REV+NOTE] for follow-up."
            ),
            validator=lambda u: _is_specimen_reviewed(u, "198"),
        ),
        ActionStep(
            step_id="review_complete",
            title="Part 1 Complete — Ready for the Collection!",
            instruction=(
                "Great job! You've learned the basics of Arbor — you're ready to resolve flagged issues and record new ones you spot yourself.\n\n"
                "Because real curation happens at the physical shelves, carrying a computer isn't always convenient. "
                "Next up is Part 2: Mobile Companion, which shows you how to use Arbor on your phone with the exact same steps "
                "while walking the collection.\n\n"
                "Click Finish ✓ to return to your workspace, or launch Part 2 below. "
                "If you opened Arbor with the Demo Project, close Arbor and load your real museum files before starting a real shift.\n\n"
                "You can always reopen any tutorial from the HELP button."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode, or launch Part 2 above.",
            details="Double-click the .exe file and click the \"Help\" button in the bottom left.",
            details_label="▸ Need help opening Arbor?",
            action_buttons=[
                ("📱 Continue to Part 2: Mobile Companion (Recommended)", _launch_mobile_guide, True),
            ],
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="Part 1: Desktop Basics", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
