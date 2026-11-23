"""
ui/tutorials/micro_guides.py

Contextual "Show Me How in 30 Seconds" micro-guides.
Run directly in-place (use_sandbox=False) without mutating or resetting the user's open workbook.
"""

from .tutorial_runner import TutorialRunner, ActionStep
from .sandbox_manager import mark_tutorial_completed


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
    """Interactive in-place Desktop-to-Phone Setup & Hallway Walkthrough (Step 3 of Learning Path)."""
    def _is_mobile_dialog_open(u) -> bool:
        md = getattr(u, "mobile_dialog", None)
        if md is not None:
            win = getattr(md, "win", md)
            try:
                if win and win.winfo_exists():
                    return True
            except Exception:
                pass
        root = getattr(u, "root", None)
        if root is not None:
            try:
                for w in root.winfo_children():
                    if "Mobile" in str(getattr(w, "title", lambda: "")()):
                        return True
            except Exception:
                pass
        return False

    steps = [
        ActionStep(
            step_id="mg_mobile_intro",
            title="0. Why Use Mobile Companion? (Optional · Needs Your Phone)",
            instruction=(
                "Connect your phone to walk the collection aisles without carrying a laptop:\n"
                "• Stamp Storage Locations for 30+ boxes in 1 tap (Armed Target Shelf)\n"
                "• Find already-reviewed objects when pulling items for closer inspection\n"
                "• Mark objects as Loaned Out, or flag physical issues & mark Reviewed on the spot\n\n"
                "Works offline in concrete basement vaults too!"
            ),
            action_hint="Click Next → to open the Phone Connector on your desktop.",
            details=(
                "This guide runs directly on your workspace without entering Practice Mode so your real collection stays ready to pair."
            ),
        ),
        ActionStep(
            step_id="mg_mobile_open",
            title="1. Open the Phone Connector",
            instruction="Click the highlighted 'MOBILE' button in the top navigation bar to open the Phone Connector window.",
            target_id="mobile_nav_btn",
            action_hint="Click 'MOBILE' in the top bar (or click Skip Step →).",
            validator=_is_mobile_dialog_open,
            details=(
                "No app store download is required — your phone connects through its normal web browser (Safari or Chrome)."
            ),
        ),
        ActionStep(
            step_id="mg_armed_setup",
            title="2. Start Session & Scan the QR Code",
            instruction=(
                "In the Phone Connector window:\n"
                "• Keep 'Launch with mobile companion tutorial' checked for first-time phone users (you can turn it off anytime).\n"
                "• Click '▶ Start Mobile Session' and scan the QR code with your phone's camera.\n"
                "• On your phone, set Floor, Cabinet, and Shelf once to arm your Target Shelf (or toggle Loaned Out on the Location tab)."
            ),
            action_hint="Click Next → for the end-of-shift saving rule.",
            details=(
                "Tip: Keep 'Require 4-Digit PIN' ON whenever using Public (Internet) mode. On private museum Wi-Fi (LAN only), you can toggle PIN off for faster sign-in."
            ),
        ),
        ActionStep(
            step_id="mg_armed_review",
            title="3. Flag Issues, Mark Reviewed & Save on Desktop",
            instruction=(
                "In the hallway, only tap '✓ Mark Reviewed' after physically checking the object. "
                "Spot a physical issue? Check 'Other Issue', jot a quick Comment, and still tap '✓ Mark Reviewed' (amber [REV+ERR] queues it safely for the desk).\n\n"
                "When your shift ends, click '💾 Save Workbook Now' (or press Ctrl+S) on this desktop computer to save all phone edits to disk."
            ),
            action_hint="Click Finish ✓ to close this guide.",
            keycaps=["Ctrl", "S"],
            details=(
                "Offline vault edits queue automatically on your phone and sync into desktop memory as soon as your phone reconnects."
            ),
        ),
    ]

    def _finish_armed():
        mark_tutorial_completed("mobile")
        if callable(on_complete):
            on_complete()

    return TutorialRunner(
        ui,
        steps,
        tutorial_name="Mobile Companion Hallway Guide",
        on_complete=_finish_armed,
        use_sandbox=False,
        badge_text="⚡ PHONE QUICK GUIDE",
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
