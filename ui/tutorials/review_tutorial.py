"""
ui/tutorials/review_tutorial.py

Action-driven interactive 3-Minute Quick Tour introducing Arbor Desktop's core workflow:
orienting on Registration Data (#110), reading real object photos (#110), marking Reviewed,
searching the Specimen Directory (#198), resolving 3-source historical conflicts in Problem
Resolution (#198), flagging physical condition issues (Other Issue), and contrasting green
[REV] vs. amber [REV+ERR] badges. Operates strictly in an isolated in-memory sandbox.
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
    """Highlight the Problems tab header first, then the 'Other Issue' checkbox once opened."""
    if _is_problems_tab_active(ui):
        cb_map = getattr(ui, "problem_checkbutton_map", None) or {}
        if "Other_problem" in cb_map:
            return cb_map["Other_problem"]
        return "other_problem_checkbox"
    nb = getattr(ui, "reg_notebook", None)
    if nb is not None:
        return (nb, lambda: _problems_tab_bbox(ui))
    return "problem_flags_frame"


def start_review_tutorial(ui, on_complete=None):
    """Initializes zero-fear practice sandbox with real photos (#110, #198) and starts the 3-Minute Quick Tour."""
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

    def _launch_discrepancy_tutorial(runner):
        from .discrepancy_tutorial import start_discrepancy_tutorial
        mark_tutorial_completed("review")
        if callable(on_complete):
            try:
                on_complete()
            except Exception:
                pass
        start_discrepancy_tutorial(ui)

    steps = [
        ActionStep(
            step_id="welcome_overview",
            title="Welcome to Arbor",
            instruction=(
                "In this quick start, you will practice the basic workflow of Arbor Desktop.\n"
                "You will learn how to look up an object in the database, check its photos and registered data, "
                "compare the current data with older records, update the data, and mark an object as Reviewed.\n\n"
                "(Arbor also has a Mobile Companion which you can use while you walk around the collection — "
                "covered in its own guide later.)\n\n"
                "Everything in this tour runs in safe Practice Mode — real museum files are never touched."
            ),
            action_hint="Click Next → to inspect your first object (#110).",
            details=(
                "You can exit Practice Mode anytime from the green banner at the top of the window, "
                "or replay any tutorial in order from HELP ▾ → Suggested Learning Path."
            ),
        ),
        ActionStep(
            step_id="orient_110",
            title="Registration Data (#110)",
            instruction=(
                "Here we have Object #110.\n"
                "On the right you will see the Registration Data, which shows everything the museum currently has "
                "recorded for this object. Both scientific data such as the species and genus and also information "
                "about who collected the object and where they found it.\n\n"
                "Next to many of the text fields you'll see a checkbox. A checked box means that field has a problem, "
                "such as missing information or different data from conflicting sources."
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
                "In the middle of the screen you should see some photos of #110. See if you can use the photos of "
                "#110 to discover when it was collected.\n"
                "You can click the thumbnails underneath the main image to switch between images.\n\n"
                "Hint:\n"
                "When writing the date we use the format DAY.MONTH.YEAR using '00' for unknown parts. "
                "So 1 Aug 2015 → 01.08.2015, while Aug 2015 → 00.08.2015. "
                "If we only see the year, it is fine to write just 2015."
            ),
            target_id="reg_field:Collection Date",
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
                "Right now, we don't see any other issues with Object #110. Uncheck the Collection Date problem box "
                "and click '✓ Mark as Reviewed' (or press Ctrl+Enter) to turn #110 green [REV].\n\n"
                "Important: Only mark an object as Reviewed after you have physically inspected the real object. "
                "Some images may be outdated, so they should not be your primary source."
            ),
            target_id="reviewed_button",
            action_hint="Click '✓ Mark as Reviewed' or press Ctrl+Enter.",
            keycaps=["Ctrl", "Enter"],
            details=(
                "Marking Reviewed stamps the date and your status in the Log so the team knows this physical object has been checked."
            ),
            validator=lambda u: _is_specimen_reviewed(u, "110"),
        ),
        ActionStep(
            step_id="select_198",
            title="Search the Specimen Directory (#198)",
            instruction=(
                "Nice — Object #110 is now marked Reviewed!\n\n"
                "Next, let's try an object with the opposite problem — contradicting data from older records. "
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
            title="Open Historical Sources (#198)",
            instruction=(
                "Object #198 already has a Collection Date filled in, yet its problem checkbox is still checked.\n"
                "This time the data isn't missing — Arbor noticed that older historical sources have different dates "
                "recorded for this object.\n\n"
                "Click the highlighted History button (or press Ctrl+H) to open the Problem Resolution tool and see "
                "if we can solve this issue too."
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
                "This is the Problem Resolution window, where you can compare current values against older records "
                "side by side (we'll cover all its features in more detail in the Historical Ledger Comparison tutorial).\n\n"
                "In the Collection Date box, you see the current value on top and Historical Suggestions from older "
                "records below.\n\n"
                "Look back at the photo of #198 — do you spot the real collection date? Click the matching suggestion, "
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
                "Click the highlighted \"Apply All Resolved\" button to save your changes and close the Problem Resolution window."
            ),
            target_id="hr_apply_all",
            action_hint="Click \"Apply All Resolved\" to save and close.",
            validator=lambda u: not _is_resolver_open(u),
        ),
        ActionStep(
            step_id="flag_other_issue",
            title="If You Discover a New Issue",
            instruction=(
                "Sometimes you'll spot a new problem while inspecting an object — either with the registered data "
                "or with the physical condition of the object.\n\n"
                "Look at the first photo of #198: the metal wire is clearly bent.\n\n"
                "Let's note that so future people working with the collection know that this object should be fixed.\n\n"
                "Click on the Problems tab and check \"Other Issue\" (since this is a physical issue, not a data issue).\n\n"
                "Tip: To be extra thorough, you can also switch back to the General Data tab and explain the issue in the Comment field."
            ),
            target_id=_step9_target_selector,
            action_hint="Click the Problems tab and check \"Other Issue\".",
            details=(
                "Excel impact: Sets 'Other_problem = TRUE' on the Observation sheet. "
                "You don't need to fix physical damage yourself — flagging it queues the object safely for follow-up later."
            ),
            validator=_is_other_problem_flagged,
        ),
        ActionStep(
            step_id="mark_reviewed",
            title="Mark Object #198 as Reviewed (With an Open Issue)",
            instruction=(
                "Now mark Object #198 as Reviewed — click '✓ Mark as Reviewed' or press Ctrl+Enter.\n\n"
                "Because \"Other Issue\" is still checked, #198 turns amber [REV+ERR] instead of green [REV]. "
                "That tells the team you inspected the object and fixed what you could, while leaving the bent wire "
                "safely queued for follow-up.\n\n"
                "You've done everything you can here — the rest is for a specialist to handle later."
            ),
            target_id="reviewed_button",
            action_hint="Click '✓ Mark as Reviewed' or press Ctrl+Enter.",
            keycaps=["Ctrl", "Enter"],
            details=(
                "You won't always be able to solve every flagged problem yourself — and that is completely okay! "
                "Marking Reviewed confirms a human verified the physical object, while the active flag keeps it in the amber [REV+ERR] queue."
            ),
            validator=lambda u: _is_specimen_reviewed(u, "198"),
        ),
        ActionStep(
            step_id="review_complete",
            title="Practice Complete!",
            instruction=(
                "Great job! You have now solved two issues and uncovered a third.\n\n"
                "Wondering what to do next?\n\n"
                "The recommended next step is Mobile Companion Hallway Guide (walk the collection and check physical objects with your phone).\n\n"
                "Or if you want to stay at your desk, check out Historical Ledger Comparison (resolve multi-field conflicts across older catalog books).\n\n"
                "Either way, you are ready to work with the real museum files.\n\n"
                "Click Finish ✓ to return to your workspace, or click one of the tutorials below to begin it. "
                "If you loaded this tutorial using the demo project, you may need to close Arbor and load it using the real files.\n\n"
                "Remember, you can always find all the tutorials by opening Arbor and clicking on the HELP ▾ icon."
            ),
            action_hint="Click 'Finish ✓' below to exit Practice Mode, or launch your next guide above.",
            details="Double-click the .exe file and click the \"Help\" button in the bottom left.",
            details_label="▸ Need help opening Arbor?",
            action_buttons=[
                ("📱 Mobile Companion Hallway Guide (Recommended)", _launch_mobile_guide, True),
                ("📚 Historical Ledger Comparison", _launch_discrepancy_tutorial, False),
            ],
        ),
    ]

    runner = TutorialRunner(ui, steps, tutorial_name="3-Minute Quick Tour", on_complete=_finish_cb)
    sm._active_runner = runner
    return runner
