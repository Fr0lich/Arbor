"""
ui/tutorials/micro_guides.py

Contextual "Show Me How in 30 Seconds" micro-guides.
Run directly in-place (use_sandbox=False) without mutating or resetting the user's open workbook.
"""

from .tutorial_runner import TutorialRunner, ActionStep


def start_hallway_followup_guide(ui, on_complete=None):
    """30-second micro-guide explaining the Hallway Follow-Up (REV+ERR) office triage loop."""
    steps = [
        ActionStep(
            step_id="mg_hallway_filter",
            title="1. Isolate Vault-Flagged Specimens",
            instruction=(
                "Click 'Hallway Follow-Up (REV+ERR)' in the Filter dialog (Ctrl+G) or search it in Ctrl+K. "
                "Arbor filters the Specimen Directory to records verified in the vault that still have open flags."
            ),
            action_hint="Use Ctrl+G (Filter) or Ctrl+K → Hallway Follow-Up.",
            keycaps=["Ctrl", "G"],
            details=(
                "Excel impact: Filters for rows where Observation.Reviewed = TRUE AND at least one problem flag column is TRUE."
            ),
        ),
        ActionStep(
            step_id="mg_hallway_resolve",
            title="2. Triage, Clear, or Leave for Later",
            instruction=(
                "Open 'Triage Problem Queue' (Ctrl+K) to step through the amber [REV+ERR] cards. "
                "Fix the entry or click '✓ Value is Correct (Clear Flag)' — and if you can't solve a problem today, that's completely okay: just leave the flag active so someone else can look at it later."
            ),
            action_hint="Click Finish ✓ to return to your workspace.",
            keycaps=["Ctrl", "K"],
            details=(
                "Once all problem flags on a specimen are cleared, its badge automatically changes from amber [REV+ERR] to green [REV]. "
                "Leaving an unresolved flag active keeps it safely queued for a specialist in the future."
            ),
        ),
    ]
    return TutorialRunner(
        ui,
        steps,
        tutorial_name="Hallway Follow-Up (30s)",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="⚡ QUICK GUIDE",
    )


def start_armed_shelf_guide(ui, on_complete=None):
    """45-second micro-guide explaining the 1-Tap Armed Target Shelf pattern on phones."""
    steps = [
        ActionStep(
            step_id="mg_armed_setup",
            title="1. Set Your Cabinet & Shelf Once",
            instruction=(
                "On your phone, pick the Building, Floor, Cabinet, and Shelf you are standing in front of. "
                "Arbor arms that location as your Target Shelf."
            ),
            action_hint="Click Next → to see how 1-tap stamping works.",
            details=(
                "You can also use the Batch Location Registrator in Mobile V2 and tap '⚡ Use Cab XX · Sh XX' to copy your armed shelf in one tap."
            ),
        ),
        ActionStep(
            step_id="mg_armed_stamp",
            title="2. Opening a Specimen Never Overwrites It",
            instruction=(
                "Pull a box and type its number (001 matches 1). Mistyped numbers never corrupt a record — "
                "tap the green 'Stamp Target' banner once to stamp 30+ boxes on the same shelf."
            ),
            action_hint="Click Next → for the final tip.",
            details=(
                "If a specimen already has a different Storage Location saved, Arbor shows an amber 'Relocate' warning instead of silently overwriting it."
            ),
        ),
        ActionStep(
            step_id="mg_armed_review",
            title="3. Flag Problems & Still Mark Reviewed",
            instruction=(
                "If a box is damaged or handwriting is unclear, check the problem box and still tap '✓ Mark Reviewed'. "
                "It's completely okay if you can't solve the issue in the hallway — the amber [REV+ERR] badge keeps it queued for someone else later."
            ),
            action_hint="Click Finish ✓ to close this guide.",
            details=(
                "Works even in concrete basement vaults with zero Wi-Fi/internet: offline edits queue safely on your phone and sync automatically once reconnected."
            ),
        ),
    ]
    return TutorialRunner(
        ui,
        steps,
        tutorial_name="1-Tap Armed Shelf (45s)",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="⚡ QUICK GUIDE",
    )


def start_image_controls_guide(ui, on_complete=None):
    """20-second micro-guide explaining scan zooming, panning, and rotation."""
    steps = [
        ActionStep(
            step_id="mg_img_zoom",
            title="1. Zoom & Pan High-Resolution Scans",
            instruction=(
                "Scroll the mousewheel over the highlighted scan to zoom in on handwritten labels, and click-drag to pan. "
                "Press Ctrl+0 anytime to reset the view."
            ),
            target_id="image_container",
            action_hint="Use mousewheel or Ctrl+1 / Ctrl+2 / Ctrl+3 / Ctrl+0.",
            keycaps=["Ctrl", "0"],
            details=(
                "Quick zoom presets: Ctrl+1 fits the whole sheet, Ctrl+2 fits to width for reading bottom labels, and Ctrl+3 zooms to 100% pixel inspection."
            ),
        ),
        ActionStep(
            step_id="mg_img_rotate",
            title="2. Rotate & Pop Out for Side-by-Side Reading",
            instruction=(
                "Press Alt+R (or click ↻) to rotate sideways labels by 90°. "
                "Double-click the photo to pop it out onto a second monitor."
            ),
            target_id="image_container",
            action_hint="Click Finish ✓ to close this guide.",
            keycaps=["Alt", "R"],
            details=(
                "All zooming and rotating is non-destructive — your original scan files on disk are never modified."
            ),
        ),
    ]
    return TutorialRunner(
        ui,
        steps,
        tutorial_name="Image Zoom & Rotate (20s)",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="⚡ QUICK GUIDE",
    )
