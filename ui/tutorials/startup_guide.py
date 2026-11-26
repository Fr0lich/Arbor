"""
ui/tutorials/startup_guide.py

Interactive Quick Startup Guide for loading the Economic Botany collection
directly inside the StartupDialog (Project Setup) window.
Runs in-place (use_sandbox=False) using Arbor's standard TutorialRunner HUD
and glowing highlight rings.
"""

from .tutorial_runner import TutorialRunner, ActionStep


ECONOMIC_BOTANY_EXCEL_DIR = r"\\hypatia.uio.no\lh-nhm-felles\objekt-bilder\johannes.d.f\Arbor"
ECONOMIC_BOTANY_PHOTO_DIR = r"\\hypatia.uio.no\lh-nhm-felles\objekt-bilder\eirik"


class _StartupTutorialHost:
    """Lightweight adapter so TutorialRunner can attach cleanly to StartupDialog."""

    def __init__(self, startup_dialog):
        self.dialog = startup_dialog
        self.root = startup_dialog.win


def _is_real_path(val: str, placeholder_prefix: str = "No ") -> bool:
    v = (val or "").strip()
    return bool(v) and not v.startswith(placeholder_prefix)


def _copy_to_clipboard(win, text: str, runner=None, feedback_label: str = "Path copied!"):
    """Copy a folder path to the OS clipboard and show brief feedback on the HUD."""
    try:
        win.clipboard_clear()
        win.clipboard_append(text)
        win.update()
    except Exception:
        pass
    if runner is not None and hasattr(runner, "action_hint_lbl"):
        try:
            if runner.action_hint_lbl.winfo_exists():
                runner.action_hint_lbl.config(text=f"✓ {feedback_label} Paste it into the folder window.")
        except Exception:
            pass


def start_economic_botany_startup_guide(startup_dialog, on_complete=None):
    """Launch an interactive step-by-step guide on StartupDialog for loading the Economic Botany collection."""
    host = _StartupTutorialHost(startup_dialog)

    # Track initial values so we only auto-advance on a fresh user selection,
    # OR let already-filled fields advance smoothly via Next ->.
    init_db = startup_dialog.db_path_var.get().strip()
    init_folder = startup_dialog.image_folder_var.get().strip()
    init_books = startup_dialog.books_path_var.get().strip()

    def _copy_excel_dir(runner):
        _copy_to_clipboard(
            startup_dialog.win,
            ECONOMIC_BOTANY_EXCEL_DIR,
            runner=runner,
            feedback_label="Excel folder path copied!",
        )

    def _copy_photo_dir(runner):
        _copy_to_clipboard(
            startup_dialog.win,
            ECONOMIC_BOTANY_PHOTO_DIR,
            runner=runner,
            feedback_label="Photo folder path copied!",
        )

    def _has_selected_db(h) -> bool:
        val = h.dialog.db_path_var.get().strip()
        return _is_real_path(val) and val != init_db

    def _has_selected_photos(h) -> bool:
        val = h.dialog.image_folder_var.get().strip()
        return _is_real_path(val) and val != init_folder

    def _has_selected_books(h) -> bool:
        val = h.dialog.books_path_var.get().strip()
        return _is_real_path(val) and val != init_books

    steps = [
        ActionStep(
            step_id="eb_startup_intro",
            title="Load the Economic Botany Collection",
            instruction=(
                "Welcome! To open the Economic Botany collection in Arbor, you just need to pick 3 things "
                "on this screen:\n"
                "• The main Excel file (Økonomisk_Botanisk_Arbor.xlsx)\n"
                "• The specimen photo folder (Øko)\n"
                "• The historical catalog file (Books.xlsx)\n\n"
                "Quick reminder: Always close Microsoft Excel first, and make sure only one person opens the "
                "main file on a computer at a time (use Mobile Companion if several people are working together)."
            ),
            action_hint="Click Next → to pick the main Excel file.",
        ),
        ActionStep(
            step_id="eb_startup_excel",
            title="Step 1 — Pick the Main Collection File",
            instruction=(
                "Click Browse… on the highlighted row and open:\n"
                "Økonomisk_Botanisk_Arbor.xlsx\n\n"
                "Where to find it on the shared server:\n"
                f"{ECONOMIC_BOTANY_EXCEL_DIR}\n\n"
                "Profile dropdown (right below): Leave this on 'Økonomisk Botanisk'. "
                "The Profile tells Arbor which form fields, problem boxes, and historical columns your Excel file uses — "
                "you will almost never need to change it.\n\n"
                "Tip: Click '📋 Copy Folder Path' below, then paste it into the address bar of the file window."
            ),
            target_id="db_path_entry",
            action_hint="Select Økonomisk_Botanisk_Arbor.xlsx (or click Next → if already filled).",
            validator=_has_selected_db,
            action_buttons=[
                ("📋 Copy Folder Path", _copy_excel_dir, True),
            ],
            details=(
                "The other options in Profile (Loan Tracking, Blank Minimal) are only for separate custom spreadsheets. "
                "Always keep 'Økonomisk Botanisk' selected when working on the Economic Botany collection."
            ),
        ),
        ActionStep(
            step_id="eb_startup_photos",
            title="Step 2 — Pick the Photo Folder (Øko)",
            instruction=(
                "Keep Local Directory selected, click the … button, and choose the entire Øko folder.\n\n"
                "Where to find it on the shared server:\n"
                f"{ECONOMIC_BOTANY_PHOTO_DIR}\n\n"
                "You only need to select the Øko folder itself — Arbor automatically matches each photo "
                "to its specimen ID."
            ),
            target_id="image_source_frame",
            action_hint="Select the Øko folder (or click Next → if already filled).",
            validator=_has_selected_photos,
            action_buttons=[
                ("📋 Copy Photo Folder Path", _copy_photo_dir, True),
            ],
            details=(
                "If you are working without access to the local photo folder, you can switch to "
                "'Online Repository' or 'Offline (No Images)' instead."
            ),
        ),
        ActionStep(
            step_id="eb_startup_books",
            title="Step 3 — Attach Historical Books (Books.xlsx)",
            instruction=(
                "Click the … button on the highlighted Historical Data (Books) row and select:\n"
                "Books.xlsx\n\n"
                "It lives in the exact same folder as the main Excel file:\n"
                f"{ECONOMIC_BOTANY_EXCEL_DIR}\n\n"
                "This lets Arbor show historical suggestions (Ctrl+H) from older digitized catalogs while you work."
            ),
            target_id="books_path_entry",
            action_hint="Select Books.xlsx (or click Next → if already filled).",
            validator=_has_selected_books,
            action_buttons=[
                ("📋 Copy Folder Path", _copy_excel_dir, False),
            ],
            details=(
                "Important: Never edit Books.xlsx directly in Excel. It is a read-only historical reference file "
                "matched by ObjectID."
            ),
        ),
        ActionStep(
            step_id="eb_startup_launch",
            title="You're Ready — Open the Collection!",
            instruction=(
                "Everything is set up! Click the highlighted Open Collection → button in the bottom right "
                "to launch Arbor.\n\n"
                "New to the main workspace? Once your collection opens, press F1 (or click HELP in the top bar) "
                "to try Part 1: Desktop Basics in safe Practice Mode — nothing you do in Practice Mode can "
                "change real museum files."
            ),
            target_id="launch_button",
            action_hint="Click 'Open Collection →' or Finish ✓ to close this guide.",
            keycaps=["F1"],
        ),
    ]

    return TutorialRunner(
        host,
        steps,
        tutorial_name="Load Economic Botany Collection",
        on_complete=on_complete,
        use_sandbox=False,
        badge_text="⚡ STARTUP GUIDE",
    )
