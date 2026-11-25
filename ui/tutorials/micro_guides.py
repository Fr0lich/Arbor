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
        candidates = [
            getattr(u, "_mobile_server_instance", None),
            getattr(u, "mobile_server", None),
            getattr(getattr(u, "app", None), "_mobile_server_instance", None),
        ]
        for attr in ("_mobile_dialog", "mobile_dialog"):
            md = getattr(u, attr, None)
            if md is not None:
                candidates.append(getattr(md, "server", None))
                panel = getattr(md, "panel", md)
                if panel is not None:
                    candidates.append(getattr(panel, "server", None))
        for srv in candidates:
            if srv is not None and (getattr(srv, "is_running", False) or getattr(srv, "running", False)):
                return True
        return False

    def _is_mobile_client_connected(u) -> bool:
        candidates = [
            getattr(u, "_mobile_server_instance", None),
            getattr(u, "mobile_server", None),
            getattr(getattr(u, "app", None), "_mobile_server_instance", None),
        ]
        for attr in ("_mobile_dialog", "mobile_dialog"):
            md = getattr(u, attr, None)
            if md is not None:
                candidates.append(getattr(md, "server", None))
                panel = getattr(md, "panel", md)
                if panel is not None:
                    candidates.append(getattr(panel, "server", None))
        for srv in candidates:
            if srv is not None:
                clients = getattr(srv, "clients", None)
                if clients is not None and len(clients) > 0:
                    return True
        return False

    steps = [
        ActionStep(
            step_id="mg_mobile_intro",
            title="Part 2 of 2 — Launch Mobile Companion",
            instruction=(
                "In Part 2, you'll learn how to launch Arbor's Mobile Companion so you can use the exact same "
                "workflow from Part 1 on your phone while walking the collection — no laptop needed.\n\n"
                "This guide runs on your normal workspace instead of Practice Mode so your collection is ready to pair. "
                "Don't worry — nothing is saved to disk until you choose to save, and every mistake can be undone or fixed."
            ),
            action_hint="Click Next → to open the Mobile Companion window.",
        ),
        ActionStep(
            step_id="mg_mobile_open",
            title="Open Mobile Companion",
            instruction=(
                "Click the highlighted MOBILE button in the top navigation bar to open the Mobile Session Launch window.\n\n"
                "No app store download is needed — your phone connects through its normal web browser (Safari or Chrome)."
            ),
            target_id="mobile_nav_btn",
            action_hint="Click 'MOBILE' in the top bar.",
            validator=_is_mobile_dialog_open,
        ),
        ActionStep(
            step_id="mg_armed_setup",
            title="Start Your Mobile Session",
            instruction=(
                "This is the Mobile Session Launch window.\n\n"
                "Mobile Companion works by starting a small server on this computer, which your phone connects to by scanning a QR code.\n\n"
                "The default settings are already ready to go! Leave Phone tutorial on Ask on the phone (or pick Trainee), "
                "then click ▶ Start Mobile Session to generate your QR code."
            ),
            target_id="mobile_start_btn",
            action_hint="Click '▶ Start Mobile Session'.",
            validator=_is_mobile_session_running,
        ),
        ActionStep(
            step_id="mg_armed_review",
            title="Scan the QR Code — Continue on Your Phone",
            instruction=(
                "Point your phone's camera at the QR code. The tutorial continues on your phone and ends with you "
                "working on real objects.\n\n"
                "You can leave the computer now. When your shift is over, come back and press Stop — "
                "Arbor will confirm your phone edits are synced and remind you to save."
            ),
            action_hint="Scan the QR code on your phone (or click Finish ✓).",
            validator=_is_mobile_client_connected,
        ),
    ]

    def _finish_armed():
        mark_tutorial_completed("mobile")
        if callable(on_complete):
            on_complete()

    return TutorialRunner(
        ui,
        steps,
        tutorial_name="Part 2: Mobile Companion",
        on_complete=_finish_armed,
        use_sandbox=False,
        badge_text="⚡ PART 2 · PHONE GUIDE",
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
