"""
ui/tutorials/micro_guides.py

Contextual "Show Me How in 30 Seconds" micro-guides.
Run directly in-place (use_sandbox=False) without mutating or resetting the user's open workbook.
"""

from .tutorial_runner import TutorialRunner, ActionStep
from .sandbox_manager import mark_tutorial_completed


def start_hallway_followup_guide(ui, on_complete=None):
    """30-second micro-guide explaining the Hallway Follow-Up (REV+ERR) office triage loop."""
    def _launch_triage_sandbox(runner):
        from .triage_tutorial import start_triage_tutorial
        runner.finish_tutorial()
        start_triage_tutorial(ui)

    steps = [
        ActionStep(
            step_id="mg_hallway_filter",
            title="Show Only Hallway-Flagged Specimens",
            instruction=(
                "Click 'Hallway Follow-Up (REV+ERR)' in the Filter dialog (Ctrl+G) or search it in Ctrl+K. "
                "Arbor filters the Specimen Directory to objects verified in the hallway that still have open flags."
            ),
            action_hint="Use Ctrl+G (Filter) or Ctrl+K → Hallway Follow-Up.",
            keycaps=["Ctrl", "G"],
            details=(
                "Shows only objects that have already been physically Reviewed and still have at least one active problem box."
            ),
        ),
        ActionStep(
            step_id="mg_hallway_resolve",
            title="Clear False Alarms or Leave for a Specialist",
            instruction=(
                "Open 'Triage Problem Queue' (Ctrl+K) to step through the amber [REV+ERR] cards. "
                "Fix the entry or click '✓ Value is Correct (Clear Flag)' — and if you can't solve a problem today, "
                "that's completely okay: just leave the flag active for a specialist later."
            ),
            action_hint="Click Finish ✓ to return to your workspace, or try the Practice Sandbox above.",
            keycaps=["Ctrl", "K"],
            details=(
                "Once all problem flags on a specimen are cleared, its badge automatically changes from amber [REV+ERR] to green [REV]. "
                "Leaving an unresolved flag active keeps it safely queued for a specialist later."
            ),
            action_buttons=[
                ("🎯 Practice in Sandbox (Office Triage)", _launch_triage_sandbox, True),
            ],
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
        md = getattr(u, "mobile_dialog", None) or getattr(u, "_mobile_dialog", None)
        if md is not None:
            win = getattr(md, "win", md)
            try:
                if win and win.winfo_exists():
                    return True
            except Exception:
                pass
        active_hud = getattr(getattr(TutorialRunner, "_active_instance", None), "hud_win", None)
        root = getattr(u, "root", None)
        if root is not None:
            try:
                for w in root.winfo_children():
                    if w is active_hud:
                        continue
                    title = str(getattr(w, "title", lambda: "")())
                    if "Arbor Guide" in title:
                        continue
                    if "Phone Connector" in title or "Mobile Companion" in title:
                        return True
            except Exception:
                pass
        return False

    def _is_mobile_session_running(u) -> bool:
        srv = getattr(u, "mobile_server", None) or getattr(getattr(u, "mobile_dialog", None), "server", None)
        if srv is not None and getattr(srv, "running", False):
            return True
        md = getattr(u, "mobile_dialog", None) or getattr(u, "_mobile_dialog", None)
        panel = getattr(md, "panel", md) if md is not None else None
        if panel is not None and getattr(getattr(panel, "server", None), "running", False):
            return True
        return False

    steps = [
        ActionStep(
            step_id="mg_mobile_intro",
            title="Take Arbor Into the Hallway (Part 2)",
            instruction=(
                "Mobile Companion brings Arbor onto your phone so you can walk the collection without a laptop:\n"
                "• Record each object's Physical Location in 1 tap so we can always find it again\n"
                "• Check real boxes against Registration Data, flag mismatches, and mark Reviewed — using the same badges you just learned on Desktop."
            ),
            action_hint="Click Next → to open the Phone Connector on your desktop.",
            details=(
                "This guide runs directly on your workspace without entering Practice Mode so your real collection stays ready to pair."
            ),
        ),
        ActionStep(
            step_id="mg_mobile_open",
            title="Open the Phone Connector",
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
            title="Start the Mobile Session",
            instruction=(
                "In the Phone Connector window:\n"
                "• Keep 'Launch with mobile companion tutorial for first-time users' checked so the Hallway Quick Guide opens automatically on your phone.\n"
                "• Click '▶ Start Mobile Session' to generate your QR code."
            ),
            action_hint="Click '▶ Start Mobile Session' (or click Skip Step →).",
            validator=_is_mobile_session_running,
            details=(
                "Tip: Keep 'Require 4-Digit PIN' ON whenever using Public (Internet) mode. On private museum Wi-Fi (LAN only), you can toggle PIN off for faster sign-in."
            ),
        ),
        ActionStep(
            step_id="mg_armed_review",
            title="Scan the QR Code & Save After Your Shift (Ctrl+S)",
            instruction=(
                "1. Scan the QR code with your phone's camera — the Hallway Quick Guide will open automatically on your phone.\n"
                "2. Every edit you make on your phone syncs straight into Arbor on this computer (and queues automatically if you walk into an offline basement vault).\n"
                "3. When your hallway shift ends, press Ctrl+S (or click '💾 Save Workbook Now') on this computer to save everything to disk."
            ),
            action_hint="Scan the QR code, then click Finish ✓ to close this desktop guide.",
            keycaps=["Ctrl", "S"],
            details=(
                "Excel impact: Pressing Ctrl+S writes all phone-synced edits from memory to your Excel workbook and creates a safety backup. "
                "You can replay the Hallway Quick Guide anytime on your phone from Settings or '?'."
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
            title="Zoom, Pan & Switch Specimen Photos",
            instruction=(
                "Scroll the mousewheel over the highlighted scan to zoom in on handwritten labels, and click-drag to pan. "
                "Click the thumbnails underneath the main photo to switch between front and back images, or press Ctrl+0 anytime to reset the view."
            ),
            target_id="image_container",
            action_hint="Use mousewheel, click thumbnails below, or press Ctrl+0.",
            keycaps=["Ctrl", "0"],
            details=(
                "Quick zoom presets: Ctrl+1 fits the whole sheet, Ctrl+2 fits to width for reading bottom labels, and Ctrl+3 zooms to 100% pixel inspection."
            ),
        ),
        ActionStep(
            step_id="mg_img_rotate",
            title="Rotate & Pop Out for Side-by-Side Reading",
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
