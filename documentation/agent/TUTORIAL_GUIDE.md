# Arbor Interactive Tutorial System — Developer & AI Agent Guide

Welcome, Agent. This document defines the architecture, rules, and procedures for maintaining and extending the interactive tutorial system in Arbor.

---

## 1. Core Principles & Philosophy

When modifying or adding tutorials in Arbor, you **MUST** follow these mandatory rules:

1. **Strictly Operational Copy (No Domain Lectures):**
   * Do **NOT** explain what constitutes valid botanical data, taxonomic rules, or why a record needs curation.
   * Focus exclusively on software actions: *"Click the 'History' button"*, *"Press Ctrl+Enter to mark as reviewed"*, *"Type an ID in the search bar"*.
2. **Absolute Sandbox Isolation:**
   * Interactive tutorials must **NEVER** modify or write to real user Excel files on disk.
   * All tutorial actions run against ephemeral, in-memory mock datasets via `SandboxManager`.
   * The user's active session is snapshot on entry and cleanly restored upon tutorial exit or completion.
3. **Action-Driven Stepping with User Autonomy:**
   * Steps should use validator callbacks or UI signal listeners to advance automatically when the user performs the requested action.
   * **Never block the user:** Always provide persistent `"Skip Step"`, `"Back"`, and `"Exit Tutorial"` controls.
4. **Modular Architecture:**
   * Each distinct tutorial flow must reside in its own dedicated Python file inside `ui/tutorials/`.

---

## 1.5 Mandatory Curatorial Logic for Tutorial Authors (ICEDIG vs. Field Errors vs. `Needs Specialist`)

Whenever a tutorial demonstrates flagging problems, handling blank/illegible labels, or leaving notes, you **MUST** keep these three mechanisms strictly distinct:

1. **ICEDIG Codes (`unknown:missing`, `unknown:indecipherable`, `unknown:undigitized`, `withheld`)** — *Field-level standard for confirmed absent or illegible data*:
   * Accessible on Desktop via the quiet per-field **`⋯`** button on the right edge of each editable field (`tutorial_id = "icedig_field_btn"` on `Collection Date`, `tutorial_id = "icedig_collector_btn"` on `Collector`), right-click → *Set ICEDIG status*, or **`ICEDIG ▾`** in Problem Resolution (no header ICEDIG button, no `?` buttons on fields); and on Mobile V2 by **tapping the field value** on `Details` (`#icedigFieldSheet`) or tapping **`ICEDIG ▾`** on the `History` tab.
   * **Rule**: Setting `unknown:missing` tells Arbor *"confirmed absent — stop looking for it"* and clears the missing-field warning. **Never** teach trainees to set `unknown:missing` when historical ledgers still contain conflicting candidate values!
   * **Finding back later**: Curators can filter directly by per-code ICEDIG filters (`ICEDIG: unknown:missing`, `ICEDIG: unknown:indecipherable`, etc.) under **Filter → Problems & History → Archival Gaps**.
2. **Tier 1 — Actionable Field Problems (`Genus_Problem`, `Collection_Date_Problem`, `Box_Label_Problem`, etc.)** — *Fixable at the desk*:
   * Use for data discrepancies, missing fields that still need ledger lookup, or **blank physical labels that have 2+ conflicting historical sources**.
   * In the hallway on Mobile Companion, trainees leave the field problem flagged, optionally add a passive `Comment` (*"No date on physical label"*), stamp Storage Location, and tap **Mark Reviewed** → produces **`REV+ERR`** so it lands in the desk Problem Triage Queue / Historical Conflict Resolver.
3. **Tier 2 — `Needs Specialist` (`Other_problem` + `Comment`)** — *Non-desk / physical / specialist escalations*:
   * Use **only** for physical damage, mold/pest, mixed specimens, or archival deadlocks that standard desk tools cannot solve.
   * **NEVER** teach trainees to use `Needs Specialist` for a single unreadable date/collector when ICEDIG (`unknown:indecipherable`) applies.
   * Checking **`Needs Specialist`** (either in the Problem Flags tab or via the synced checkbox above **`Comment`**) produces **`NOTE`** (unreviewed) or **`REV+NOTE`** (reviewed) — **never `REV+ERR`** — and is **unchecked by default** in the batch Problem Triage Queue (`ProblemQueueDialog`).
   * A plain `Comment` *without* `Needs Specialist` checked is a passive informational/provenance note and **never** triggers `NOTE` or `REV+NOTE`.

---

## 2. Directory Structure

```
ui/tutorials/
├── __init__.py               # Package exports
├── sandbox_manager.py        # Snapshot, mock dataset factory ("review", "discrepancy", "triage"), and state restore
├── tutorial_runner.py        # Floating HUD card, auto-dodge positioning, collapsible details, single-runner guard
├── review_tutorial.py        # Part 1 of 3: Desktop Basics (real photos #110 & #198, 3-way rule)
├── micro_guides.py           # Part 2 of 3: Mobile Companion launch handoff + 20–30s Quick Guides (use_sandbox=False)
├── triage_tutorial.py        # Part 3 of 3: Desk Follow-Up & Batch Tools (REV+ERR, live-by-default + sandbox fallback)
├── discrepancy_tutorial.py   # Legacy standalone: Historical Ledger Comparison
├── database_tutorial.py      # Optional guide: Creating collections & new specimens
└── startup_guide.py          # Project Setup Quick Guide: Loading Economic Botany collection (F1 / Help)
```

---

## 2.5 Phone Coach Tutorial (`backend/mobile_template_v2.py`)

Mobile Companion V2 includes a built-in hands-on **Phone Coach Tutorial** that runs directly on the user's real collection (never mutating data itself) using a floating bottom card (`#coachCard`, `z-40`, positioned above the sticky bottom bar) and pulsing `.coach-target` outlines:
* **`PHONE_TUTORIALS`**: Defines two versions — `trainee` (5 steps: `t_shelf`, `t_search`, `t_tour`, `t_save_review`, `t_ready`) and `helper` (4 steps: `h_shelf`, `h_search`, `h_check_save_review`, `h_ready`). Every card has `← Back`, `Skip step`, and `✕` exit.
* **`COACH_TIPS` & `maybeShowTip(id)`**: One-time contextual tips (`tip_flagged`, `tip_icedig` Trainee-only, `tip_specialist`, `tip_rev_err`) triggered on first encounter after the routine finishes (never overlapping open modals or active Undo toasts).
* **Persistence**: Stored in `localStorage['arbor_phone_tutorial']` (`{ mode, stepIdx, finished, dismissed, tipsSeen, tipsDisabled }`), surviving phone sleep and reloads.
* **Server Mode Injection**: `backend/mobile_server.py` injects `{{ phone_tutorial_mode }}` (`"ask" | "trainee" | "helper" | "off"`), controlled from Desktop `ui/mobile_panel.py` (`user_prefs.json["mobile_phone_tutorial_mode"]`).
* **Adding a Step or Tip**: Append a step object `{ id, badge, title, body, target, check }` to `PHONE_TUTORIALS.trainee` / `.helper`, or add an entry to `COACH_TIPS` and call `maybeShowTip('tip_id')` from the relevant UI handler.

---

## 3. How the Core Engine Works

### `SandboxManager` (`ui/tutorials/sandbox_manager.py`)
* `enter_sandbox(ui, mock_type)`:
  1. Deep-copies the active `AppState` (DataFrames, file paths, dirty flags, history caches) and snapshots `ui.image_panel` state (`image_mode`, `image_folder`, `image_index`, `show_images_var`).
  2. Generates in-memory DataFrames (`df_reg`, `df_obs`, `df_photo`, `df_log`): for `"review"`, loads real specimens `#110` (*Ephedra major*, blank Collection Date, no historical records) and `#198` (*Corylus colurna*, 3-source historical conflict across 2 ledgers), auto-mounting bundled front/back photos from `data/tutorial_images/`.
  3. Re-initializes UI caches and refreshes the main visualizer via `ui._finish_open_excel("[Tutorial Sandbox]", ...)`.
* `exit_sandbox(ui)`:
  1. Restores the exact prior `AppState`, DataFrames, and `image_panel` state.
  2. Rebuilds the UI back to the user's real open file. Zero disk operations occur.
* `mark_tutorial_completed(tutorial_id)` / `get_completed_tutorials()`:
  * Persists finished tutorial IDs (`review`, `discrepancy`, `mobile`, `triage`, `database`) in `user_prefs.json["completed_tutorials"]` for the 5-step Suggested Learning Path in `ui/help_dialogs.py`.

### `TutorialRunner` & `ActionStep` (`ui/tutorials/tutorial_runner.py`)
* Manages a non-modal, top-level floating HUD displaying progress, step titles, action hints, and control buttons.
* **Proximity-Anchored HUD Positioning (`_position_hud`)**:
  * Always docks the HUD **immediately beside** the highlighted target (`gap = sc(16)`) so the user's eyes never have to jump across the screen: right of left-column targets (e.g., search bar), left of right-column targets (anchored to the Registration pane edge and vertically aligned to the target), directly below top-bar buttons (`MOBILE`), and immediately outside popup dialogs (`Problem Resolution`, `Mobile Session Launch`) without covering them.
  * **Unhighlighted steps (`target_id=None`)** keep the exact previous HUD position (`_last_hud_pos`, also carried across tutorial transitions such as Part 1 → Part 2) instead of jumping to a corner; only a fresh Step 1 with no prior position centers calmly in the workspace.
  * **Center-photo protection**: Pass `hud_avoid_photo=True` on any `ActionStep` where the trainee needs to read the specimen photo in the middle pane while typing in the right pane (e.g., Part 1 Step 3 `transcribe_110_date`).
  * **2-stage & deferred targets**: `_sync_dynamic_highlight()` automatically retries unmounted string `target_id`s (e.g., newly opened dialogs) and repositions the HUD whenever a dynamic target changes stage.
* **Windows-Safe Glowing Highlights (`TutorialHighlight`)**: Uses focus-aware `-topmost` (`_sync_topmost` active only while Arbor has OS focus, automatically disabled on Alt-Tab) so green highlight rings always stay above Arbor windows without ever floating over other OS apps.
* Polls `validator(ui)` (every ~300ms) to detect when the required action has occurred and automatically advances to the next step.

---

## 4. How to Create or Modify a Tutorial

### Step 1: Define the Tutorial in a Modular File
Create a new file (e.g., `ui/tutorials/my_new_tutorial.py`):

```python
from .sandbox_manager import SandboxManager
from .tutorial_runner import TutorialRunner, ActionStep

def start_my_new_tutorial(ui, on_complete=None):
    # 1. Mount isolated sandbox
    SandboxManager().enter_sandbox(ui, mock_type="review")

    # 2. Define action-driven steps
    steps = [
        ActionStep(
            step_id="step_one",
            title="Locate the Action Button",
            instruction="Click the target button in the toolbar to begin.",
            target_id="my_button_tutorial_id",  # tutorial_id on widget or ui attribute name
            action_hint="Click the highlighted button.",
            validator=lambda u: getattr(u, "some_flag", False) is True
        ),
        ActionStep(
            step_id="step_two",
            title="Complete the Task",
            instruction="You have performed the action. Click Finish to exit sandbox mode.",
            action_hint="Click Finish below."
        )
    ]

    # 3. Launch the runner
    return TutorialRunner(ui, steps, tutorial_name="My New Feature", on_complete=on_complete)
```

### Step 2: Register in `ui/tutorials/__init__.py`
Export your new launcher function in `ui/tutorials/__init__.py`.

### Step 3: Wire into Help Menu & Shortcuts (`ui/help_dialogs.py`)
Add an entry in `ui/help_dialogs.py` `show_help_menu()` to make the tutorial launchable on demand.

---

## 5. Testing & Verification

Always write unit tests in `tests/test_sandbox_tutorials.py` when adding or modifying tutorials. Ensure tests verify:
1. `SandboxManager.enter_sandbox()` isolates state without altering `app.excel_path`.
2. Steps progress when `validator` evaluates to `True`.
3. `SandboxManager.exit_sandbox()` cleanly reinstates the original `df_reg` and `current_object_id`.

To run tests:
```powershell
python -m unittest tests/test_sandbox_tutorials.py
```
