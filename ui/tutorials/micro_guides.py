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
                "Click '🎯 Hallway Follow-Up (REV+ERR)' in the Filter dialog (or search it in Ctrl+K). "
                "Arbor filters the Specimen Directory to records physically verified in the vault that still have open problem flags."
            ),
            action_hint="Use Ctrl+G (Filter) or Ctrl+K → Hallway Follow-Up.",
            keycaps=["Ctrl", "G"],
        ),
        ActionStep(
            step_id="mg_hallway_resolve",
            title="2. Triage & Clear Flags in Queue Mode",
            instruction=(
                "Open 'Triage Problem Queue' (Ctrl+K) or step through the amber [REV+ERR] cards. "
                "Fix the handwriting, confirm the value, or repair the box label — once cleared, the badge turns herb-green [REV]."
            ),
            action_hint="Click Finish ✓ to return to your workspace.",
            keycaps=["Ctrl", "K"],
        ),
    ]
    return TutorialRunner(
        ui,
        steps,
        tutorial_name="Hallway Follow-Up (30s)",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="30-SEC QUICK GUIDE",
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
        ),
        ActionStep(
            step_id="mg_armed_stamp",
            title="2. Opening a Specimen Never Overwrites It",
            instruction=(
                "Pull a box and type its number (001 matches 1). Mistyped numbers never corrupt a record — "
                "tap the green '⚡ Stamp Target' banner once to stamp 30+ boxes on the same shelf."
            ),
            action_hint="Click Next → for the final tip.",
        ),
        ActionStep(
            step_id="mg_armed_review",
            title="3. Flag Problems & Still Mark Reviewed",
            instruction=(
                "If a box is damaged or handwriting is unclear, check the problem box and still tap '✓ Mark Reviewed'. "
                "The badge turns amber (REV + ISSUES) so your desktop queues it for office follow-up."
            ),
            action_hint="Click Finish ✓ to close this guide.",
        ),
    ]
    return TutorialRunner(
        ui,
        steps,
        tutorial_name="1-Tap Armed Shelf (45s)",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="45-SEC QUICK GUIDE",
    )


def start_image_controls_guide(ui, on_complete=None):
    """20-second micro-guide explaining scan zooming, panning, and rotation."""
    steps = [
        ActionStep(
            step_id="mg_img_zoom",
            title="1. Zoom & Pan High-Resolution Scans",
            instruction=(
                "Scroll the mousewheel over the scan to zoom in on handwritten labels, and click-drag to pan. "
                "Press Ctrl+0 anytime to reset the view."
            ),
            action_hint="Use mousewheel or Ctrl+Plus / Ctrl+Minus / Ctrl+0.",
            keycaps=["Ctrl", "0"],
        ),
        ActionStep(
            step_id="mg_img_rotate",
            title="2. Rotate & Pop Out for Side-by-Side Reading",
            instruction=(
                "Press Alt+R (or click ↻) to rotate sideways labels by 90°. "
                "Double-click or use the popout button to inspect scans on a second monitor."
            ),
            action_hint="Click Finish ✓ to close this guide.",
            keycaps=["Alt", "R"],
        ),
    ]
    return TutorialRunner(
        ui,
        steps,
        tutorial_name="Image Zoom & Rotate (20s)",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="20-SEC QUICK GUIDE",
    )
