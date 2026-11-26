# Arbor Living Change Journal (User-Facing Delta Log)

This file tracks all user-facing changes made to Arbor. Whenever a feature, shortcut, setting, or workflow is updated in code, the authoring agent **MUST** record the change here so the documentation agent can synchronize all user guides, cheat sheets, and in-app touchpoints.

---

## 📌 Instructions for Coding Agents
1. Every time you change, add, or remove a user-facing feature (keyboard shortcut, status badge, setting toggle, panel layout, or dialog flow), append a new entry to the `[Unreleased / Recent Updates]` section below.
2. Use plain, non-technical language to describe the **User Impact** (what a trainee or museum assistant experiences at their desk).
3. Do not close a feature task until you have filled out the **Documentation Sync Checklist**.

---

## [Unreleased / Recent Updates]

### Entry 72: Compact Phone Tutorial Dropdown, Mobile Tabs Renamed (`Data · Location · Problems`) & Workflow-Focused Phone Tutorial
- **Date**: 2026-11-25
- **Feature Area**: Mobile Session Launcher & Mobile Companion V2 (`ui/mobile_panel.py`, `backend/mobile_template_v2.py`, `ui/unified_help.py`, `USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`, `tests/test_navigation_and_dialogs.py`)
- **What Changed**:
  1. **Compact Phone Tutorial Dropdown (`ui/mobile_panel.py`)**: Replaced the 4 stacked radio buttons (`Ask on the phone` / `Trainee` / `Helper` / `Off`) with a single read-only `ttk.Combobox` dropdown so the Mobile Companion launcher stays compact and unintimidating for first-time users.
  2. **Mobile Tabs Renamed (`Data` · `Location` · `Problems`)**: Renamed the 3 visible Mobile Companion tabs from `Details` / `Location` / `History` to **`Data`** / **`Location`** / **`Problems`** (keeping internal DOM IDs unchanged for compatibility).
  3. **Workflow-Focused Phone Coach Tutorial (`backend/mobile_template_v2.py`)**: Rewrote Trainee Step 3 (`t_tour`), Helper Step 3 (`h_check_save_review`), and contextual tips (`tip_flagged`, `tip_history`) to teach trainees to quickly glance at **`Data`** against the real object (flagging clear mismatches like Africa vs. China) and use **`Problems`** (just like Desktop Problem Resolution) to resolve conflicting sources (like England vs. Finland) right from the physical object in hand.
  4. **Synced Manuals & CI Doc-Parity Guard**: Updated `USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`, `ui/unified_help.py`, and `tests/test_navigation_and_dialogs.py` to enforce **`Data ↔ Location ↔ Problems`**.
- **User Impact**: Cleaner, shorter Mobile Companion launcher, clearer tab names on the phone, and a phone tutorial that actively teaches trainees to spot mismatches on `Data` and solve conflicts on `Problems`.
- **Documentation Sync Checklist**:
  - [x] Bundled User Manuals (`USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`)
  - [x] CI Doc-Parity Guard (`tests/test_navigation_and_dialogs.py`)
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`

---

### Entry 71: 2-Part Core Onboarding Intro, Standalone Advanced Batch Problem Queue Tutorial & Post-Mobile Wrap-Up Popup
- **Date**: 2026-11-25
- **Feature Area**: Interactive Tutorials & Mobile Handoff (`ui/unified_help.py`, `ui/database_ops.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/review_tutorial.py`, `ui/tutorials/micro_guides.py`, `ui/mobile_dialog.py`, `backend/mobile_template_v2.py`)
- **What Changed**:
  1. **2-Part Core Introduction (`unified_help.py`, `database_ops.py`, `review_tutorial.py`, `micro_guides.py`)**: Narrowed the Core Introduction (`LEARNING_PATH_IDS = ("review", "mobile")`) to **Part 1: Desktop Basics** and **Part 2: Mobile Companion**, updating Welcome to Arbor, Arbor Help Center (`CORE INTRO: X OF 2 COMPLETED`), and Part 1/Part 2 handoff copy.
  2. **Independent Advanced Tutorial (`triage_tutorial.py`, `unified_help.py`)**: Moved `triage_tutorial.py` out of the Core Intro into **Optional & Advanced Tutorials** as **Batch Problem Queue (One-by-One Desk Review)** — completely independent of Parts 1 & 2, with honest, clear framing of the queue tool (live by default + 1-click Practice Mode fallback).
  3. **Updated Post-Mobile Stop Popup (`mobile_dialog.py`, `mobile_template_v2.py`)**: Stopping Mobile Companion now shows a calm wrap-up popup confirming that all phone edits are already synced in Arbor, reminding the user to save (`💾 Save File Now (Ctrl+S)`), and inviting them to explore using **Filter (`Ctrl+G`)** or **Help & Tutorials (`HELP`)**.
- **User Impact**: New trainees finish the core introduction cleanly after Part 2 with a clear save-and-explore wrap-up, while the Batch Problem Queue remains available as an independent advanced guide whenever they want it.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Automated Tests: `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py`, `tests/test_mobile_companion.py`

---

### Entry 70: Mobile Companion Phone Coach Tutorial Polish — `tip_history`, Teacher-Voice Copy & Anti-Overwhelm Pacing
- **Date**: 2026-11-25
- **Feature Area**: Mobile Companion V2 Phone Coach Tutorial (`backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Added `tip_history` on First `History` Tab Visit**: Triggered `maybeShowTip('tip_history')` in `switchTab(2)` so trainees and helpers get a clear, one-time explanation of the History (Problem Resolution) screen the very first time they open it.
  2. **Fixed Contextual Tip Triggers**: Restricted `tip_flagged` to actionable problem flags (excluding `Needs Specialist`-only `[REV+NOTE]` objects), queued `_pendingCoachTip` during active 5-second Undo toasts so `tip_rev_err` is never silently dropped, and auto-dismissed detail tips when returning to the Search List (`showListView()`).
  3. **Teacher-Voice Copy & Anti-Overwhelm Pacing**: Rewrote `PHONE_TUTORIALS` and `COACH_TIPS` in an encouraging, natural teacher tone (*"This is the History tab — use it to compare..."*, badge **`QUICK TIP · SHOWN ONCE`**), prevented tips from stacking on top of each other, and added a 10-second passive-tip cooldown so users are never bombarded.
- **User Impact**: Phone trainees and helpers get warm, well-timed one-time guidance the first time they encounter each screen or tool, without ever feeling nagged or missing tips behind an Undo toast.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Mobile Companion Tests Verified

---

### Entry 69: Proximity-Anchored Tutorial HUD Positioning & Windows Highlight Z-Order Fix
- **Date**: 2026-11-25
- **Feature Area**: Interactive Tutorials (`ui/tutorials/tutorial_runner.py`, `ui/tutorials/review_tutorial.py`, `tests/test_sandbox_tutorials.py`)
- **What Changed**:
  1. **Proximity-Based HUD Placement (`_position_hud`)**: Replaced the far-corner opposite-edge placement with target-adjacent anchoring so the tutorial card always appears right beside the highlighted element — immediately right of left-column targets (like Step 5's search bar), immediately left of right-column targets (Registration fields, `⋯`, `✓ Mark as Reviewed`), directly below top-bar buttons (`MOBILE`), and outside popup dialogs (`Problem Resolution`, `Mobile Session Launch`) without covering them.
  2. **Stable Position When Unhighlighted**: Steps without a highlight (such as Step 12 completion or Part 2 Step 4 QR scan) now stay in the exact same position as the previous step (and carry over cleanly from Part 1 → Part 2) instead of jumping to the far top-right. Step 3 (`transcribe_110_date`) sets `hud_avoid_photo=True` so `#110`'s center photo stays completely unobstructed.
  3. **Reliable Windows Highlight Stacking**: Updated `TutorialHighlight` with focus-aware `-topmost` (active only while Arbor has OS focus, automatically disabled on Alt-Tab) and added deferred string-target retry + HUD repositioning in `_sync_dynamic_highlight()`.
- **User Impact**: Trainees no longer have to scan across the entire monitor between the tutorial card and the highlighted button, highlights stay crisply visible on Windows without covering other apps, and unhighlighted steps never jump around.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`

---

### Entry 68: Hands-On Phone Coach Tutorial (Trainee & Helper), One-Time Tips, `⚑ Needs Specialist` Bottom Bar & Problem Resolution Parity
- **Date**: 2026-11-25
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`, `backend/mobile_server.py`, `backend/mobile_archived_flag_issue.py`), Desktop Launch Selector & Part 2 Handoff (`ui/mobile_panel.py`, `ui/tutorials/micro_guides.py`), User & Agent Docs (`MOBILE_COMPANION_USER_GUIDE.md`, `USER_GUIDE.md`, `documentation/agent/TUTORIAL_GUIDE.md`, `documentation/agent/TUTORIAL_MASTER_PLAN.md`, `documentation/agent/MOBILE_COMPANION_GUIDE.md`, `documentation/MASTER_DOCUMENTATION_MAP.md`)
- **What Changed**:
  1. **Removed Buggy `⚑ Flag Issue` & Archived Legacy Code**: Deleted `#addDiscrepancyModal`, `openAddDiscrepancyModal()`, `submitDiscrepancy()`, and non-config fallback `General_Problem` (which created stray Excel columns and flagged damaged specimens as `[REV+ERR]` instead of `[REV+NOTE]`), archiving them in `backend/mobile_archived_flag_issue.py`.
  2. **Added `⚑ Needs Specialist` to the Phone Bottom Bar**: Replaced Flag Issue with `#btnDetailNeedsSpecialist` synced to `Other_problem`; turning it ON switches to `Details`, scrolls `Comment` into view, and briefly highlights the quick-tag pills while keeping `[REV+NOTE]` helper copy synchronized.
  3. **Gentle Non-Blocking Storage Location Reminder**: Marking an object Reviewed with blank Cabinet & Shelf now completes immediately and displays a 6-second toast (`✓ Reviewed. Tip: save where it's stored first`) with a **`📍 Set Shelf`** action button (never clobbering an active Undo toast).
  4. **History Tab Aligned to Desktop Problem Resolution**: Added **Problem Resolution** heading + *"Compare with the label in your hand."*, updated summary bar to **`N to resolve`** / **`Nothing to resolve`**, empty state to **`No problems to resolve`**, card clear button to **`✓ Value is Correct`**, and ICEDIG button to **`ICEDIG ▾`**.
  5. **Hands-On Phone Coach Tutorial & One-Time Contextual Tips**: Replaced the 4-slide `Hallway Quick Guide` modal with floating `#coachCard` (`z-40`, offline-CSS supported, persisted in `localStorage['arbor_phone_tutorial']`), offering **Trainee (5 steps)** and **Helper (4 steps)** paths on real objects plus 4 one-time contextual tips (`tip_flagged`, `tip_icedig`, `tip_specialist`, `tip_rev_err`) manageable in phone **⚙ Settings → Phone tutorial**.
  6. **Desktop 4-Option Tutorial Selector & Part 2 Phone Handoff**: Replaced the desktop launch checkbox with 4 radio choices (**Ask on the phone**, **Trainee**, **Helper**, **Off**) persisted in `mobile_phone_tutorial_mode` (migrating legacy `mobile_show_walkthrough`), and updated Desktop Part 2's final step to hand off cleanly to the phone (auto-completing on phone connect, leaving Part 3 to the post-session stop popup).
  7. **Field Guide & Documentation Sync**: Rewrote Field Guide section 6, cleaned up all `Physical Location` / `Other Issue` strings in V2, and synced `MOBILE_COMPANION_USER_GUIDE.md` (adding §3.10 & §6 *Helping Out for a Day*), `USER_GUIDE.md` Chapter 9, `TUTORIAL_GUIDE.md`, `TUTORIAL_MASTER_PLAN.md`, `MOBILE_COMPANION_GUIDE.md`, and `MASTER_DOCUMENTATION_MAP.md`.
- **User Impact**: Both full trainees and one-day helpers get a calm, hands-on coach card on their phone that teaches the real hallway routine (`Set Shelf → search → check → Save to Shelf → Mark Reviewed`), explains problems right when they first appear, and makes flagging physical damage (`⚑ Needs Specialist` → `[REV+NOTE]`) one tap away without ever corrupting the Excel sheet.
- **Documentation Sync Checklist**:
  - [x] `MOBILE_COMPANION_USER_GUIDE.md` (§3.2–3.4, §3.10, §4, §6)
  - [x] `USER_GUIDE.md` (Chapter 9)
  - [x] `documentation/agent/TUTORIAL_GUIDE.md`, `TUTORIAL_MASTER_PLAN.md`, `MOBILE_COMPANION_GUIDE.md`
  - [x] `documentation/MASTER_DOCUMENTATION_MAP.md` (Row 11)
  - [x] `documentation/CHANGE_JOURNAL.md` (Entry 68)
  - [x] Automated tests: `tests/test_mobile_companion.py`, `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py`

---

### Entry 67: Part 2 Mobile Companion Tutorial Polish, Non-Blocking Modal Focus & Start-Session Auto-Advance Fix
- **Date**: 2026-11-25
- **Feature Area**: Interactive Tutorial Part 2 (`ui/tutorials/micro_guides.py`, `ui/mobile_dialog.py`, `ui/mobile_panel.py`)
- **What Changed**:
  1. **Beginner-Friendly Part 2 Copy (`micro_guides.py`)**: Shortened and warmed all 4 steps of **Part 2: Mobile Companion**, standardized naming on *"Mobile Companion"* / *"Mobile Session Launch window"*, removed all redundant `More Details` drawers and `"(or click Skip Step →)"` hints, and removed the redundant `Ctrl+S` save step/keycaps from Step 4 (since Arbor prompts to save when closing the mobile server).
  2. **Fixed Tutorial HUD Click Blocking (`mobile_dialog.py`)**: Skipped `self.win.grab_set()` while an interactive `TutorialRunner` HUD is active so trainees can freely click `Skip Step →`, `← Back`, `Finish ✓`, and `Exit Tutorial` while the Mobile Session Launch window is open.
  3. **Fixed Step 3 → Step 4 Auto-Advance & Highlight (`micro_guides.py`, `mobile_panel.py`)**: Fixed `_is_mobile_session_running()` to check `server.is_running` across `_mobile_server_instance` and `_mobile_dialog.panel.server` (instead of the nonexistent `.running` attribute) and tagged `▶ Start Mobile Session` with `tutorial_id="mobile_start_btn"` so Step 3 highlights the button and advances automatically to Step 4 when clicked.
- **User Impact**: Launching Mobile Companion during Part 2 is calm, clear, and responsive — the Start button highlights directly, clicking it immediately moves to the QR-scan step, and the tutorial card stays interactive the entire time.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Minimal Tutorial Tests: `tests/test_sandbox_tutorials.py` (25 passed)

---

### Entry 66: Decluttered Header Buttons (`GBIF Verify`, `Books`, `Phone`, `Old Names`) & `Auto-next` Unchecked by Default
- **Date**: 2026-11-25
- **Feature Area**: Workspace Simplification & Review Defaults (`ui/object_context_bar.py`, `ui/main_window.py`, `ui/unified_settings.py`)
- **What Changed**:
  1. **Hidden Cluttered Inline Header Buttons**: Un-packed **`GBIF Verify`**, **`Books`**, and **`Phone`** from the Curatorial Command Strip (`ui/object_context_bar.py`) and **`📜 Old Names`** from the Registration header (`ui/main_window.py`). All underlying tools remain accessible via `TOOLS ▾`, `Ctrl+K` Command Palette, `Ctrl+H`, and the Mobile menu.
  2. **`Auto-next` Off by Default**: Changed `auto_advance_on_review` default from `True` to **`False`** so the **Auto-next** checkbox below **Mark as Reviewed** starts unchecked by default.
- **User Impact**: Cleaner, less confusing workspace headers with fewer duplicate entry points, and marking a specimen as reviewed keeps the user on the current specimen unless they opt into **Auto-next**.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] UI & Settings Tests Verified

---

### Entry 65: Part 1 Tutorial Polish, Highlight Z-Order Fix, Sandbox Historical Suggestions Fix & "Save Edits" Button Rename
- **Date**: 2026-11-25
- **Feature Area**: Interactive Tutorial Part 1 (`ui/tutorials/review_tutorial.py`, `ui/tutorials/tutorial_runner.py`, `ui/tutorials/sandbox_manager.py`, `ui/historical_suggestions.py`, `ui/main_window.py`) & Problem Resolution Footer (`ui/object_problem_resolver.py`, `ui/historical_resolver.py`)
- **What Changed**:
  1. **Part 1 Copy & Step Refinement (`review_tutorial.py`)**: Polished all 12 steps of **Part 1: Desktop Basics** based on live `.exe` walkthrough feedback — including explicit manual unchecking of `Collection Date` on `#110` (matching Entry 64), clear physical-inspection reminders on both `#110` and `#198`, removal of the non-working `Ctrl+Shift+M` shortcut reference from Step 9, `"General Data"` tab naming in Step 10, and streamlined Part 2 transition copy in Step 12.
  2. **Problem Resolution Button Rename (`object_problem_resolver.py`, `historical_resolver.py`)**: Renamed the footer confirmation button from `"APPLY ALL RESOLVED (CTRL+A)"` / `"Apply All Resolved (Ctrl+A)"` to plain-language **`"Save Edits"`**.
  3. **Bug #1 — Reliable `TutorialHighlight` Z-Order (`tutorial_runner.py`)**: Fixed `TutorialHighlight` so `overrideredirect` highlight frames stay stacked directly above their owner window (`win.lift(owner)` when Arbor is active, without floating over other OS apps), guarded against zero-size geometry, and moved HUD-to-main refocus before `show_step()` so advancing steps no longer buries the green highlight box behind the main window.
  4. **Bug #2 — No Auto-Jump Past Step 5 (`main_window.py`)**: Suppressed auto-advance on `✓ Mark as Reviewed` while inside the Part 1 (`review`) Practice Mode sandbox so marking `#110` Reviewed keeps focus on `#110` and lets trainees practice searching for `#198` in Step 5.
  5. **Bug #3 — Restored Sandbox Historical Suggestions (`sandbox_manager.py`, `historical_suggestions.py`)**: Added `"reg_by_id"` alongside `"df"` to all mock historical databases (`review`, `triage`, `discrepancy`) and added a `"df"` + `str`/`int` index fallback in `_get_db_dict_cache()` so `#198`'s Collection Date historical suggestions (`1927` from `Historical Ledger Book 1`, `1912` from `Old Card Catalog (Ledger 2)`) always appear in Problem Resolution.
- **User Impact**: New trainees walking through Part 1 see crisp green highlight boxes on every step, get to practice searching for `#198` without being auto-jumped past it, see the real conflicting historical years (`1927` vs `1912` vs `1963`) in Problem Resolution, and click a clear **`Save Edits`** button to save and close.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Minimal Tutorial & Dialog Tests: `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py` (62 passed)
  - [x] `data/tutorial_images/` untouched

---

### Entry 64: Safer Manual Problem-Flag Clearing Default, Opt-In Blank-Fill Toggle & Batch-Safe Auto-Clear Toasts
- **Date**: 2026-11-25
- **Feature Area**: Problem Flag Safety, Settings & Notifications (`ui/main_window.py`, `ui/unified_settings.py`, `ui/historical_resolver.py`, `ui/object_problem_resolver.py`, `ui/registry_panel.py`, `tests/test_problem_persistence_fix.py`, `tests/test_unified_settings.py`)
- **What Changed**:
  1. **Manual Uncheck by Default (`auto_clear_problem_on_fill = False`)**: Typing into a Registration text field (`commit_current_object`) no longer silently unchecks its mapped problem checkbox by default — preventing uncertain or partial edits from hiding real issues. Dedicated resolution tools (Historical Conflict Resolver, Batch Problem Resolver, GBIF, ICEDIG) continue to auto-clear resolved flags automatically.
  2. **Settings Toggles (Settings → General → Workflow & Navigation)**: Added **`Auto-clear problem flag when filling a blank field`** (default `False`; when enabled, clears only on strict `blank → filled` transitions, never wiping deliberate flags on populated fields) and **`Show brief notification when Arbor auto-clears a problem flag`** (default `True`).
  3. **Efficient, Batch-Safe Auto-Clear Toasts**: Added `ObjectProgramUI.notify_auto_cleared_flags()` showing a single brief, non-blocking, coalesced toast (`2.2 s`) whenever a tool or blank-fill rule auto-clears flag(s), with re-entrant batch suppression (`_suppress_auto_clear_toasts`) so multi-field or batch resolutions never spam toasts.
- **User Impact**: Trainees will never accidentally wipe a problem flag while typing an uncertain guess; dedicated resolution tools still clear flags automatically with a subtle confirmation toast that can be turned off anytime in Settings.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_problem_persistence_fix.py`, `tests/test_unified_settings.py`

---

### Entry 63: 3-Part Core Onboarding Architecture (Desk → Collection → Back at Desk), Part 1 ICEDIG Step, Live Part 3 & Post-Mobile Batch Follow-Up Popup
- **Date**: 2026-11-25
- **Feature Area**: Interactive Tutorials, Onboarding & Mobile Handoff (`ui/tutorials/review_tutorial.py`, `ui/tutorials/micro_guides.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/database_tutorial.py`, `ui/tutorials/sandbox_manager.py`, `ui/registry_panel.py`, `ui/mobile_dialog.py`, `ui/database_ops.py`, `ui/unified_help.py`, `documentation/agent/TUTORIAL_MASTER_PLAN.md`)
- **What Changed**:
  1. **Part 1 — Desktop Basics (`review_tutorial.py`, `sandbox_manager.py`, `registry_panel.py`)**: Renamed the former 3-Minute Quick Tour to **Part 1: Desktop Basics** (12 steps), framed the **Desk → Collection → Back at Desk** 3-part rhythm upfront, tagged `Collector`'s `⋯` button (`tutorial_id="icedig_collector_btn"`), and added Step 9 (`mark_198_icedig`) on real specimen `#198` (blank `Collector`, no older books) teaching canonical ICEDIG codes (`unknown:missing`, `unknown:indecipherable`, `unknown:undigitized`, `withheld`) and the 3-way guardrail before trainees ever pick up Mobile Companion.
  2. **Part 2 — Mobile Companion (`micro_guides.py`)**: Synced to Entries 61–62 (inline checkboxes on `Details`, tap field value for canonical ICEDIG codes, `History` swipe tab + `Set ICEDIG Code…` + `📜 Old names`, `Needs Specialist` `[REV+NOTE]`, `Set Shelf` + 5-sec `↩ Undo`) with a direct launch button to Part 3.
  3. **Live-by-Default Part 3 — Desk Follow-Up & Batch Tools (`triage_tutorial.py`, `sandbox_manager.py`)**: Converted Part 3 to run **live on the user's real collection by default** (`use_sandbox=False`) so trainees immediately work on their actual hallway shift results, with a 1-click **Practice with Sample Data Instead** fallback (`#2001` `[REV+NOTE]` auto-excluded, `#2002` false-alarm clear, `#2003` blank-date + 2 conflicting older books, `#2004` clean `[REV]`).
  4. **Post-Shift Batch Follow-Up Popup (`ui/mobile_dialog.py`)**: Stopping the Mobile Companion server on Desktop now displays a calm popup counting actionable `[REV+ERR]` specimens (strictly excluding `Needs Specialist`-only `[REV+NOTE]`), offering 1-click **Open Batch Follow-Up** and **Guided Desk Follow-Up (Part 3)** buttons, self-discovery instructions (`TOOLS ▾`, `Ctrl+K`, `Ctrl+G`), and a persisted **`Don't show this popup again`** checkbox (`user_prefs.json["suppress_mobile_stop_followup_popup"]`).
  5. **Welcome to Arbor & Help Center (`database_ops.py`, `unified_help.py`)**: Updated both windows to present the **3-Part Core Introduction (`CORE INTRO: X OF 3 COMPLETED`)** and cleanly separated **Collections & New Specimens** under **Optional / On-Demand Guides**.
- **User Impact**: New trainees follow a natural Desk → Collection → Back at Desk journey, learn all 3 curatorial paths (including per-field `⋯` ICEDIG codes) before walking into the hallway, get a seamless popup handoff when stopping Mobile Companion, and can immediately do real batch follow-up on their own collection.
- **Documentation Sync Checklist**:
  - [x] Master Tutorial Blueprint: `documentation/agent/TUTORIAL_MASTER_PLAN.md`
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Automated Tests & Manual Parity Guard: `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py` (62 passed)
  - [x] `data/tutorial_images/` untouched

---

### Entry 62: Live Dark Mode, WCAG Card Contrast, Mobile Negative-Floor Undo & 390px Ergonomics Fixes
- **Date**: 2026-11-25
- **Feature Area**: Desktop Live Theming & Contrast (`ui/registry_panel.py`, `ui/widgets.py`, `ui/layout_settings.py`, `ui/main_window.py`, `ui/status_bar.py`) & Mobile Companion V2 (`backend/mobile_schemas.py`, `backend/mobile_server.py`, `backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Desktop Live Light ↔ Dark Mode Parity**: Registered all Registration Data cards, headers, labels, field rows, focus bars, and canvas in `RegistryPanel.apply_theme()` using Arbor's forest-charcoal dark palette (`#181c19` / `#212622` / `#262c28`, replacing `#1e1e2d`), and added `DetailedObjectList.refresh_theme()` wired into `apply_theme()` so Specimen Directory cards immediately re-theme on live toggle without restarting.
  2. **Desktop Specimen Directory WCAG AA Contrast & ICEDIG Trigger Comfort**: Replaced low-contrast Light Mode card text colors (`#0bd45b` / `#f0ad4e` on `#f2f5f1`, 1.77:1–1.81:1) with theme-aware WCAG AA colors (`#1f5c2e` / `#8a5200` Light; `#b0f3a9` / `#f6c467` Dark), updated status bar separators (`#8b948d`), and slightly widened per-field `⋯` ICEDIG buttons (`padx=sc(6)`).
  3. **Mobile Companion Negative Basement Floor Preservation**: Updated `sanitize_string_field()` in `backend/mobile_schemas.py` to preserve plain numeric values (`-1`, `-2`, `+1`) and standalone `-` so basement floors no longer turn into `'-1` after saving or tapping `↩ Undo`.
  4. **Mobile Companion V2 ID Parity & `390×844` Ergonomics**: Unified `/api/object/<oid>` `accession_number` with `/api/objects` so List and Detail headers always show the same `#`; abbreviated building names on Specimen List cards so `Sh XX` never truncates; reset Detail view synchronously to `Details` on specimen open; and raised key mobile tap targets (`Bldg` select, `Needs Specialist`, `Set Shelf`/`Change`, `📜 Old names`, `↩ Undo`, search bar controls, Shelf modal inputs, short field values `min-w-[44px]`, and quick-tag pills `min-h-[36px]`).
- **User Impact**: Switching between Light and Dark mode updates every panel and specimen card cleanly without restarting; reviewed specimen names are crisp and readable in both themes; basement floor `-1` / `-2` locations survive saves and Undo intact; and phone controls are easier to tap one-handed on 390px screens.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [ ] Interactive Tutorials (`ui/tutorials/*`) — intentionally untouched per user request (handled by tutorial agent)

---

### Entry 61: Unified Per-Field ICEDIG UX, Future-Proof Quick-Tags, Live Dark Mode & 390px/Laptop Polish
- **Date**: 2026-11-25
- **Feature Area**: ICEDIG UX, Dark Mode, Responsive Layout & Mobile V2 Parity (`config.py`, `ui/widgets.py`, `ui/main_window.py`, `ui/registry_panel.py`, `ui/layout_settings.py`, `ui/object_context_bar.py`, `ui/object_problem_resolver.py`, `ui/filter_dialog.py`, `ui/new_database_wizard.py`, `backend/mobile_server.py`, `backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Unified, Config-Driven ICEDIG System (Zero `?` Icons, Zero Competing UIs)**:
     - Added `ICEDIG_CODES` in `config.py` (canonical codes `unknown:missing`, `unknown:indecipherable`, `unknown:undigitized`, `withheld` + descriptions + shortcuts) as the single source of truth for Desktop and Mobile Companion (`/api/schema`).
     - Removed the `?` Unvalidated Source button from Desktop registration rows (preserving `df_unvalidated` backend safety) and removed the crowded `Blank / Unreadable ▾` header button; replaced them with a quiet per-field **`⋯`** ICEDIG menu trigger in Column 3 of every editable field (amber-highlighted when an ICEDIG code is active, clearing the field's problem flag on apply, with a historical-conflict reminder).
     - Replaced the competing hardcoded `📄 Blank` / `🔍 Illegible` buttons in `ObjectProblemResolver` with a single `ICEDIG ▾` dropdown menu.
     - On Mobile Companion V2, removed the `?` field button and the competing `toggleIcedigTray` in `History`; tapping any field value on `Details` (or `Set ICEDIG Code…` on `History`) opens the unified `#icedigFieldSheet` showing canonical codes, a `Clear field value` option, case-insensitive `Collection Place`/`Box Label` key resolution, and a historical-conflict warning banner.
  2. **Future-Proof Quick-Tag Pills (`SPECIALIST_QUICK_TAGS` + `FlowWrapFrame`)**:
     - Centralized specialist quick-tag pills in `config.SPECIALIST_QUICK_TAGS` (exposed via `/api/schema` to Mobile V2) and built a reusable `FlowWrapFrame` in `ui/widgets.py` so pills automatically wrap across rows at any right-pane width regardless of tag count or label length.
  3. **Laptop Layout, Sash & Live Dark Mode Fixes**:
     - Split Desktop Registration Header into 2 clean rows so controls never clip on 1366×768 screens; added balanced default vertical sash sizing for Storage Location below Images and sash rebalancing on `F8` restore.
     - Wired `RegistryPanel.apply_theme()` into `ui/layout_settings.py`, fixed Dark Mode `fg`/`selectcolor` in `ProblemQueueDialog`, fixed Dark Mode `HAS`/`NOT` badges in `FilterDialog`, and fixed `status_badge` border updates in `ObjectContextBar.set_dark_mode()`.
     - Packed Desktop's specialist inline hint **above** `Comment` to match Mobile V2.
  4. **Badge Distinction & Mobile List/Details Parity**:
     - Differentiated `[REV+NOTE]` (calm teal) and `[NOTE]` (indigo-slate) from `[CFCT]` and `[UNREV]` across Desktop Directory, Context Bar, and Mobile V2 (including Specimen List cards via `has_actionable_problems` / `is_specialist_note` in `/api/objects`).
     - Removed duplicate `Needs Specialist` from Mobile's lower `#problemFlagsGrid` (renamed `"Photo & Media Issues"`) and excluded `Other_problem` from actionable flag counts; cleaned up remaining `"Needs Specialist (Other)"` / `"[🚩 Other_problem]"` labels.
- **User Impact**: Trainees get one clean, consistent ICEDIG workflow on Desktop and Phone with canonical codes, zero clipped buttons on laptops or 390px phones, clean live Dark Mode switching, and visually distinct `[REV+NOTE]` / `[NOTE]` badges everywhere.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Automated Tests & Mobile V2 JS check verified

---

### Entry 60: `Needs Specialist` (`NOTE` / `REV+NOTE`) Redesign, Discoverable ICEDIG UI, Per-Code ICEDIG Filters & Tutorial-Agent Contract
- **Date**: 2026-11-25
- **Feature Area**: Problem Philosophy, Status Badges, ICEDIG Usability, Filters & Agent Docs (`ui/widgets.py`, `ui/object_context_bar.py`, `ui/registry_panel.py`, `ui/object_problem_resolver.py`, `ui/main_window.py`, `ui/filter_dialog.py`, `backend/filter.py`, `backend/mobile_template_v2.py`, `ui/tutorials/review_tutorial.py`, `ui/tutorials/triage_tutorial.py`, `documentation/MASTER_DOCUMENTATION_MAP.md`, `documentation/agent/TUTORIAL_GUIDE.md`, `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`, `AGENTS.md`, `USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`)
- **What Changed**:
  1. **Two-Tier Flag Badges (`REV+NOTE` & `NOTE`)**: Separated `Other_problem` (**Needs Specialist**) from actionable desk data errors across Desktop Directory cards, Context Bar, and Mobile Companion V2. Specimens with **only** `Other_problem = True` display calm **`REV+NOTE`** (reviewed) or **`NOTE`** (unreviewed) instead of alarming **`REV+ERR`** / **`ERR`**. Plain `Comment` text alone never triggers `NOTE` / `REV+NOTE`, and actionable errors still take priority when both are active.
  2. **Renamed `"Other Issue"` → `"Needs Specialist"` & Tight `Comment` Coupling**: Renamed the UI label everywhere (keeping Excel column `Other_problem` unchanged), visually separated `Needs Specialist` in the Problem Flags tab, and added a synced **`Needs Specialist`** checkbox + 4 strictly non-ICEDIG physical/specialist quick-tag pills (`+ Damaged`, `+ Mold / Pest`, `+ Mixed Specimen`, `+ Needs Specialist ID`) + non-blocking inline hint directly above `Comment` on both Desktop and Mobile V2.
  3. **Batch Desk Triage (`ProblemQueueDialog`)**: Defaulted **`Needs Specialist`** to **unchecked (`False`)** so trainees only triage actionable desk errors by default, and separated `Images_Problem` into its own Media category checkbox.
  4. **Discoverable ICEDIG UI & Per-Code Filters**: Added a **`Blank / Unreadable ▾`** (`tutorial_id = "icedig_quick_btn"`) header button on Desktop Registration, a 1-tap **`?`** ICEDIG bottom sheet on every field in Mobile V2 `Details`, and per-code tri-state ICEDIG filters (`ICEDIG: unknown:missing`, `ICEDIG: unknown:indecipherable`, `ICEDIG: unknown:undigitized`, `ICEDIG: withheld`) in `backend/filter.py` and `ui/filter_dialog.py`.
  5. **Permanent Tutorial-Agent Contract**: Codified the 3-way curatorial decision rule (ICEDIG vs. Actionable Field Errors vs. `Needs Specialist`, including the blank-label + conflicting-historical-sources hallway workflow) across `MASTER_DOCUMENTATION_MAP.md`, `TUTORIAL_GUIDE.md`, `MOBILE_AUDIT_WORKFLOW_SPEC.md`, and `AGENTS.md`.
- **User Impact**: Trainees no longer get false `REV+ERR` alarms or unfixable physical-damage items in their default desk queue; specialists can filter directly for `Needs Specialist` or specific ICEDIG codes like `unknown:missing`; and ICEDIG is now 1-click accessible on both Desktop and Mobile.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`documentation/MASTER_DOCUMENTATION_MAP.md`)
  - [x] Tutorial Guide (`documentation/agent/TUTORIAL_GUIDE.md`) & Mobile Spec (`documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`)
  - [x] Bundled User Manuals (`USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`)
  - [x] Automated Tests (`tests/test_filter.py`, `tests/test_ui_ergonomics.py`)

---

### Entry 59: Storage Location Always Below Images by Default (All Image Modes & Clean F8 Docking)
- **Date**: 2026-11-25
- **Feature Area**: Main Workspace Layout (`ui/main_window.py`, `ui/image_panel.py`, `tests/test_location_panel.py`)
- **What Changed**:
  1. **Fixed Startup Pane Inversion**: Guarded `_sync_middle_panes()` against running mid-init during `ImagePanel.__init__()` before `self.right_frame` was assigned, and enforced the ordering invariant so `ImagePanel` is always at index 0 (top) and **Storage Location** (`_middle_loc_slot`) is always at index 1 (bottom) of `middle_panes`.
  2. **Consistent Layout in Offline & Missing-Image Modes**: Stopped collapsing `middle_frame` when `image_mode == "offline"`. Whether images are loaded (`online`/`folder`), missing, or disabled (`offline`), the middle column stays open with the photo viewer / Specimen Summary Hub on top and **Storage Location** directly below it.
  3. **Predictable `F8` Photo-Pane Toggle**: Pressing `F8` with Storage Location in the Left column hides the entire middle column; pressing `F8` with Storage Location in the default bottom position hides only the images and docks **Storage Location** cleanly at full height below the main panes and above the status bar.
- **User Impact**: Storage Location now consistently appears below the specimen images (or summary panel when offline/missing images) on every startup, and toggling `F8` never overlaps other panels.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Regression Test: `tests/test_location_panel.py` (`test_real_main_window_storage_location_always_below_images`)

---

### Entry 58: Full Clean Removal of Legacy PySide6 / Qt Experiment (~46,600 Lines)
- **Date**: 2026-11-24
- **Feature Area**: Repository Cleanup & Single-Stack Focus (`main.py`, `main.spec`, `requirements-dev.txt`, `tests/test_gbif.py`, `AGENTS.md`, `MAINTAINER_HANDOFF.md`)
- **What Changed**:
  1. **Bookmarked Full Snapshot in Git**: Created lightweight Git tag `archive/pyside6-blueprint` before removal so the earlier Qt Designer `.ui` blueprint remains recoverable in Git history if ever needed.
  2. **Removed All 115 Legacy PySide6 / Qt Assets**: Deleted `pyside_new_uis/` (32 `.ui` files), `ui_qt/` (56 files), `qt designer/` (20 files), `main_qt.py`, `scripts/verify_all_uis.py`, `scripts/open_designer.py`, `scripts/verify_ui.py`, `PYSIDE_UI_EXTRACTION_PLAN_PHASE1.md`, `PYSIDE_UI_INTEGRATION_PIPELINE.md`, `documentation/agent/PYSIDE6_MIGRATION_GUIDE.md`, and `tests/test_startup_selection.py`.
  3. **Simplified Startup & Tests**: Removed `select_ui_framework()` and the Qt branch from `main.py` (preserving `--mobile`/`-m` and Tkinter launch), removed `TestAutoResolveSafeguardsInQt` from `tests/test_gbif.py`, removed `'ui_qt'` from `main.spec` (retaining `'PySide6'` and `'shiboken6'` as defensive PyInstaller guards), and updated `requirements-dev.txt`, `AGENTS.md`, and `MAINTAINER_HANDOFF.md`.
- **User Impact**: Zero change to the live Desktop app or Mobile Companion workflows; launching `python main.py` from a terminal no longer prompts for a UI framework choice, and the repository is cleanly single-stack.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Maintainer & Agent Guides: `AGENTS.md`, `MAINTAINER_HANDOFF.md`
  - [x] Full test suite & dangling-reference check verified

---

### Entry 57: Codebase Cleanup — Retired Mobile V1 (`4,709` Lines), Pruned Legacy Help Hub (`337` Lines) & Isolated Test Prefs
- **Date**: 2026-11-24
- **Feature Area**: Codebase Hygiene & Test Isolation (`backend/mobile_template_v1.py`, `backend/mobile_server.py`, `ui/help_dialogs.py`, `conftest.py`, `.gitignore`, `tests/test_mobile_companion.py`, `tests/test_problem_persistence_fix.py`)
- **What Changed**:
  1. **Retired Obsolete Mobile Companion V1 (`-4,709` lines)**: Deleted `backend/mobile_template_v1.py`, routed `GET /` directly to `index_v2()` in `backend/mobile_server.py` (keeping `INDEX_TEMPLATE = INDEX_TEMPLATE_V2` as a compatibility alias), and removed V1-only template assertions from tests.
  2. **Pruned Dead Legacy Help Hub (`-337` lines)**: Deleted the unused `_legacy_open_help_window()` from `ui/help_dialogs.py` (retaining active `show_main_help()` and `show_shortcuts()`).
  3. **Eliminated Repo-Root `user_prefs.json.corrupt.*` Pollution**: Added an `autouse=True` `_isolate_user_prefs` fixture in `conftest.py` redirecting `config._PREFS_PATH` to `tmp_path` for every test, deleted 11 stray `.corrupt.*` files, and added `.arbor_synonyms_cache.json` to `.gitignore`.
- **User Impact**: Visiting the bare Mobile Companion URL (`/`) now lands directly on the modern Mobile Companion V2, the packaged `.exe` drops ~5,000 lines of dead code, and running tests never touches local user preferences.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Full test suite verified: `python -m pytest tests/ -q`

---

### Entry 56: Automatic Offline Synonym Cache Warm-Up During Batch GBIF
- **Date**: 2026-11-24
- **Feature Area**: Taxonomy Reference & Offline Vault Cache (`backend/gbif.py`, `ui/gbif_batch_config.py`)
- **What Changed**:
  - Added `record_batch_diffs_to_synonym_cache()` in `backend/gbif.py` and wired it cleanly into `GBIFBatchConfigDialog` (`ui/gbif_batch_config.py`) right after `batch_gbif_match()` finishes.
  - Whenever a curator runs Batch GBIF at their desk, every discovered old name (`Genus`/`Species`) and old family rename is silently merged into `.arbor_synonyms_cache.json` next to the workbook (atomic write, zero extra HTTP requests, zero slowdown).
- **User Impact**: Offline basement vault checks using **`📜 Old names`** on Mobile Companion automatically know about previously updated synonyms and family names across the collection without requiring any manual pre-cache step.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_gbif.py`

---

### Entry 55: In-App Manuals Synced & Permanent Automated Doc-Parity Guard Added
- **Date**: 2026-11-24
- **Feature Area**: Bundled User Manuals (`USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`, `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`), CI Parity Guard (`tests/test_navigation_and_dialogs.py`), & Agent Watchlist (`documentation/agent/CLAUDE_BUG_REVIEW_GUIDE.md`)
- **What Changed**:
  1. **Synced Bundled In-App Manuals**: Updated `USER_GUIDE.md` and `MOBILE_COMPANION_USER_GUIDE.md` to match the live UI 1:1 — direct **`HELP`** button → Help Center, **Details ↔ Location ↔ History** tabs, inline checkboxes on `Details`, **`Set Shelf` + 5-sec `↩ Undo`**, **`📜 Old names`**, **`Stored as`** bottom sheet, **`↗ Loaned`** badges, **⚙ Settings → Advanced Tools** for Batch Location Registrator, and the reordered 5-Step Learning Path. Updated `F1` on `KEYBOARD_SHORTCUTS_CHEAT_SHEET.md` to `OPEN HELP CENTER & LEARNING PATH`.
  2. **Permanent Doc-Parity Guard (`tests/test_navigation_and_dialogs.py`)**: Added `test_in_app_user_manuals_stay_synced_with_ui()` so every pytest/CI run automatically fails if retired UI labels (`Armed Target Shelf`, `Details ↔ Location ↔ Problems`, `HELP ▾`, `Stamp Target`, etc.) ever creep back into the bundled manuals.
  3. **Agent Watchlist Rule #8 (`CLAUDE_BUG_REVIEW_GUIDE.md`)**: Documented that `USER_GUIDE.md` and `MOBILE_COMPANION_USER_GUIDE.md` are live bundled UI and must be updated in the same turn as any UI rename.
- **User Impact**: Trainees opening the Desktop Work Manual or Mobile Vault Guide inside Arbor's Help Center now see accurate, up-to-date instructions matching every button and tab in the app, and CI prevents them from drifting out of sync again.
- **Documentation Sync Checklist**:
  - [x] `USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`, `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`
  - [x] Automated parity guard: `tests/test_navigation_and_dialogs.py`
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`

---

### Entry 54: Aligned 5-Step Learning Path Order & Cleaned Up Stale "Armed Target Shelf" Copy
- **Date**: 2026-11-24
- **Feature Area**: Help Center & Tutorials (`ui/unified_help.py`, `ui/help_dialogs.py`, `ui/tutorials/review_tutorial.py`)
- **What Changed**:
  1. **Reordered Learning Path to Match a Real Museum Shift (`ui/unified_help.py`, `ui/help_dialogs.py`)**: Aligned both Help Center views to **1. 3-Minute Quick Tour → 2. Mobile Companion Hallway Guide → 3. Office Triage (REV+ERR) → 4. Historical Ledger Comparison → 5. Collections & New Specimens (Optional)**.
  2. **Removed Stale `"Armed Target Shelf"` Wording (`ui/unified_help.py`, `ui/help_dialogs.py`)**: Updated all 3 remaining Help Center descriptions to **`Set Shelf` / `Physical Location` + 5-sec Undo + `Old names`**.
  3. **Quick Tour Handoff Copy (`ui/tutorials/review_tutorial.py`)**: Updated the final-step Mobile Companion description to echo Slide 1 (*"record Physical Locations and check real objects"*).
- **User Impact**: Every Help Center card and tutorial transition now follows one consistent, natural workflow (**Learn Desk → Walk Hallway → Triage Back at Desk**) with unified plain-English terminology.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py`

---

### Entry 53: Seamless Desktop-to-Phone Mobile Companion Tutorial (4-Step Hallway Quick Guide & `?` Field Guide Sync)
- **Date**: 2026-11-24
- **Feature Area**: Interactive Tutorials (`ui/tutorials/micro_guides.py`) & Mobile Companion V2 Onboarding / Field Guide (`backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Desktop-to-Phone Handoff (`ui/tutorials/micro_guides.py`)**: Reframed `start_armed_shelf_guide` as Part 2 right after the Desktop 3-Minute Quick Tour — Step 3 (`Start the Mobile Session`) auto-advances when `▶ Start Mobile Session` starts the server, and Step 4 guides the user to scan the QR code and remember `Ctrl+S` after their shift.
  2. **Visual, Location-First 4-Step `Hallway Quick Guide` + Auto-Dismissing Coach Nudge (`backend/mobile_template_v2.py`)**: Upgraded `WALKTHROUGH_SLIDES` to ≤25-word scannable cards with bold action labels, real-styled visual pill/badge previews (`Set Shelf`, `📍 Save to Cab 21 · Sh 01`, `↩ Undo`, `📜 Old names`, `[REV]` / `[REV+ERR]`), touch swipe + tappable dots, calm "you can't break anything" reassurance, `sessionStorage` per-session tracking (so shared museum phones and re-tests actually show the guide when enabled), and an auto-dismissing 1-line `#listCoachNudge` under `Shelf: Not set` that disappears automatically once a shelf is set.
  3. **In-Phone `?` Field Guide Sync (`backend/mobile_template_v2.py`)**: Fixed all 3 remaining stale `"Problems tab"` references (`Genus`, `Species`, `Collector`) to reference the inline checkboxes on `Details`, and added `[CFCT]` and `↗ Loaned` to the Status Badges section.
- **User Impact**: New trainees transitioning from the Desktop 3-Minute Quick Tour into the Mobile Companion now get a single, continuous onboarding flow whose instructions match every button, tab, and badge on the phone 1:1.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`, `tests/test_mobile_companion_offline.py`, `tests/test_sandbox_tutorials.py`
  - [x] Mobile V2 JS syntax verified via `node --check`

---

### Entry 52: Mobile Companion V2 Hallway QA Fixes — Location Sync, 5-Second Undo Toast, History Resolution & 390px Ergonomics
- **Date**: 2026-11-24
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`) & Mobile Server Detail Payload (`backend/mobile_server.py`)
- **What Changed**:
  1. **List-vs-Detail Location Sync**: Updated `/api/object/<oid>` to inherit non-empty Storage Location and Loan fields from Registration in the read-only GET payload when Observation is blank (mirroring `/api/objects` without mutating any data on disk), fixing the bug where specimens with saved shelves showed `Loc: Unrecorded` / `Location [Unset]` on open.
  2. **5-Second `↩ Undo` Toast on All 1-Tap Shelf Saves & 390px Shelf Bar Polish**: Added the protected 5-second `↩ Undo` action button to both relocation and initial 1-tap shelf saves so `"✓ Saved & synchronized"` never overwrites it; shortened `Current Shelf:` → `Shelf:` and `Floor` → `Fl` across List, Detail, and Location summaries so `Sh 01` never truncates at `390px`, and stacked `Fam:`/`Loc:` cleanly beside `📜 Old names` to eliminate orphaned `•` wrapping.
  3. **Post-`Apply` `History` Sync, Flagged Status Pill & Scroll Reset**: Filtered resolved/matching historical suggestions out of `#tabHistoryBadge` and `[CFCT]` cards immediately after tapping `Apply`; updated the Detail header pill on unreviewed flagged specimens to `[UNREV] · ⚠ N` (matching List View); reset tab scroll to top when switching specimens; and removed stray indentation whitespace in the Comment preview box.
  4. **Offline Vault CSS & 390px Touch Ergonomics**: Added `[id$="Sheet"]` bottom-sheet and `.inline-flag-btn` fallback rules in `html.arbor-offline-css`; enlarged Batch Location Registrator steppers (`36×36px`), Quick Filter Pills (`34px` height + right-edge scroll fade), and Settings modal `Save`/`Cancel` (`40px`); fixed double dropdown chevrons on `<select>` controls; and raised `#toast` above sticky footer buttons (`bottom-24`). Walk Mode icons (`🌙` / `☀️`) were kept unchanged.
- **User Impact**: Trainees opening any specimen in the hallway now immediately see its true saved shelf, never lose `Sh 01` off the edge of a 390px screen, get a reliable 5-second `↩ Undo` button after every 1-tap shelf save, see `History` conflict badges clear immediately after tapping `Apply`, and have comfortable one-handed tap targets both online and in offline vaults.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`, `tests/test_mobile_companion_offline.py`
  - [x] Live `390×844` browser re-verification

---

### Entry 51: Mobile Companion V2 Desktop-Parity Redesign (`Details` Inline Checkboxes, `History` Swipe Tab & Compact Current Shelf Sheet)
- **Date**: 2026-11-24
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`, `tests/test_mobile_companion.py`)
- **What Changed**:
  1. **3-Tab Horizontal Swipe Redesign (`Details` · `Location` · `History`)**: Added 40×40px inline problem checkboxes (`data-no-swipe`) directly beside each Registration Data field in **Details** (mirroring Desktop Arbor's exact layout), added a 1-tap flagged-fields jump chip (`#detailsFlagSummaryChip`) and a compact **Physical & Other Issues** card (`Other Issue`, `Images Issue`) at the bottom of **Details**, and converted Tab 2 into a dedicated **History** resolver tab (Current value + Historical Suggestions + 1-tap `Apply` + slate-blue count badge + calm empty state with `📜 Check Old Names & Synonyms` shortcut).
  2. **Compact 1-Line `Current Shelf` Bar + Swipe-Down Bottom Sheet (`#stationSetupSheet`)**: Replaced the expanded 140px List View shelf form with a 1-line bar (`Current Shelf: Not set [Set Shelf]` / `[Change]`) opening a touch-friendly bottom sheet with swipe-down-to-dismiss; auto-hides redundant `Copy from Previous` on Tab 1 when `Current Shelf` is set, and quiets the Detail shelf banner to `✓ On Cab X · Sh Y` when the specimen already matches.
  3. **Desktop Badge Parity & Cleaner Top Bar**: Aligned Quick Filter pills to Desktop badges (`UNREV`, `REV`, `CFCT`), kept `🌙` Wake Lock directly toggleable in the List top bar, tucked the advanced **Batch Location Registrator** into **Settings → Advanced Tools**, updated Mobile's in-app `?` Field Guide copy, and pruned 4 orphaned dead-code references (`presetsConfigModal`, `openCommentModal`, `commentInput`).
- **User Impact**: Trainees moving from Desktop Arbor to Mobile Companion now see the exact same mental model — inline field checkboxes on `Details`, one swipe over to `History` to compare older catalog books, more visible specimen cards on small phones, and zero broken modals or buttons.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Mobile V2 JS syntax verified via `node --check` (0 errors) & static DOM/handler audit (0 missing)
  - [x] Unit Tests: `tests/test_mobile_companion.py`, `tests/test_mobile_companion_offline.py` (80 passed)

---

### Entry 50: Mobile Companion V2 Polish Pass 2 — Undo Guard, Full Curatorial Filters, Loaned Out Visibility, Stored As Sheet & 390px Ergonomics (Batch C + D + E)
- **Date**: 2026-11-24
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`), Mobile Server List Payload (`backend/mobile_server.py`), & Schema Choice (`config.py`)
- **What Changed**:
  1. **Critical Bug Fixes (Batch C)**:
     - **5-Second `↩ Undo` Toast Protection**: Prevented background auto-save toasts (`✓ Saved & synchronized`) from overwriting active Undo action toasts, and updated the relocation `↩ Undo` callback to write against the live `state.currentRecord.observation` object so SSE reloads cannot detach the rollback.
     - **Curatorial Advanced Filters**: Populated the previously empty **Specific Problems & Verification** section with Review Status pills (`All Objects`, `Unreviewed`, `Reviewed`, `Flagged`, `Conflicts`) and Specific Problem checkboxes, wired all Spatial Location inputs (`loc_*`) and `specific_problems` into `/api/objects`, and synced `#filterActiveBadge`.
     - **Immediate Footer Micro-Copy Refresh**: Refreshed the review helper message immediately after 1-tap `Save to Shelf` and `↩ Undo` so reviewed specimens never show stale *"location not recorded yet"* text.
     - **Dropdown & Offline CSS Polish**: Eliminated double `<select>` carets and 2-line `Bldg` wrapping via `.arbor-compact-select` (`appearance: none`), shortened `Cab`/`Shelf` placeholders (`21` / `01`), replaced undefined `bg-tonal` with `bg-tonal1`, and added high-contrast `html.arbor-offline-css` rules for `Retry`, `Old names`, and all three states of `Mark Reviewed`.
  2. **One-Handed 390px Ergonomics, `Loaned Out` & `Stored As` (Batch D)**:
     - Raised primary and modal tap targets across Specimen List, Specimen Detail, Field Guide, Walkthrough, Filters, Old Names, and Photo Viewer to `≥ 40px` (`36–40px` inside compact search bar/steppers) and fixed search icon padding (`pl-10`).
     - Locked all 3 segmented tabs (`Details`, `Location`, `Problems`) to an identical `40px` height by using a non-wrapping `Unset` badge.
     - **Loaned Out Visibility**: Added normalized `loaned_out` + `loaned_out_date` to `/api/objects`, rendered an amber **`↗ Loaned`** pill on Specimen List cards and **`↗ Loaned · DD.MM.YYYY`** in the sticky Detail header, and auto-stamped/cleared `Loaned out date` in Desktop's `DAY.MONTH.YEAR` format with toast confirmation.
     - **Stored As Bottom Sheet**: Replaced the clipped `26.5px` horizontal pill strip with a `44px` tap-to-pick selector opening `#storedAsBottomSheet` with full-width `44px` choices and plain trainee wording, and fixed `"Mounted on wooded platform"` → `"Mounted on wooden platform"` in `config.py`.
  3. **Final Copy, Desktop Parity & Photo Viewer (Batch E)**:
     - Replaced remaining `"Set Target Shelf"` / `"target shelf armed"` copy with **`📍 My Current Shelf`** / **`Set My Current Shelf first`**, humanized flagged/cleared problem toasts and discrepancy card badges (removing raw `*_Problem` column names), included Building in Walkthrough Slide 2 and the active shelf bar, and updated the `?` Field Guide copy to match Mobile V2's read-only Registration Data (removing absent Desktop-only fields and the `"Innsammling"` typo).
     - Constrained bottom sheets (`#oldNamesSheetCard`, `#storedAsSheetCard`) to `max-w-[440px] mx-auto` and added `‹` / `›` prev/next photo arrows + counter + mouse-drag panning to the fullscreen Photo Viewer.
- **User Impact**: Trainees walking the hallway with one hand now get reliable 5-second Undo after moving a specimen, working status and problem filters, immediate `↗ Loaned` badges on both the list and detail header, a clean full-width `Stored As` picker with zero clipped text, uniform tab heights, clear offline contrast, and plain English across every toast, modal, and Field Guide entry.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`, `tests/test_mobile_companion_offline.py` (80 passed)
  - [x] Mobile V2 JS syntax verified via `node --check` (0 errors)
  - [x] Live `390×844` browser verification completed (0 console errors)
  - [ ] Trainee Manual (`USER_GUIDE.md`) — sync updated Mobile Companion filters, `Loaned Out` badges, and `Stored As` picker via 1-Prompt Sync Protocol

---

### Entry 49: Mobile Companion V2 Polish — Bug Fixes, 390px Ergonomics & Desktop Parity (Batch A + B)
- **Date**: 2026-11-24
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`) & Desktop Phone Guide (`ui/tutorials/micro_guides.py`)
- **What Changed**:
  1. **Critical Bug Fixes (`backend/mobile_template_v2.py`)**:
     - Fixed `Uncaught ReferenceError: activeSchema is not defined` in the Curatorial Filters modal (`openFilterModal`, `applyAdvancedFilters`, `openAddDiscrepancyModal`) by referencing `state.activeSchema`.
     - Fixed double-counting of active problems in `countActiveProblemsOnRecord()` so the detail header badge, footer button, and `Problems` tab badge always agree.
     - Fixed false `"✓ Location recorded"` review micro-copy on specimens with no location set, fixed the `detailTotalCount` cap (`220` vs `200`), fixed photo count display (`N Photos`), guarded `<img id="specimenImg">` `onerror` on initial load, and made `?tutorial=1` reliably launch the walkthrough.
  2. **390px Phone Layout Fixes (`backend/mobile_template_v2.py`)**:
     - Widened `Cabinet` and `Shelf` inputs (`w-14 min-w-[48px]`) with `36px` `−`/`+` steppers so 2- and 3-digit numbers never clip (`0.` / `0:`).
     - Shortened the active shelf bar (`Current Shelf: Fl 1 · Cab 04 · Sh 02`) and removed the redundant `Coordinates` label on the `Saved:` breadcrumb so the Shelf number is always visible on 390px screens.
     - Raised key hallway buttons (`Set Current Shelf`, `Save to Shelf` / `Move to ...`, walkthrough `Back`/`Next`, `Write / Edit Comment`) to `≥ 40px` height.
  3. **Desktop Continuity & Plain Trainee Language (`backend/mobile_template_v2.py`, `ui/tutorials/micro_guides.py`)**:
     - Renamed **`Physical Coordinate Audit`** → **`Physical Location`** (*"Where this object lives so we can find it again"*), **`Active Audit Station` / `Armed Target`** → **`My Current Shelf` / `Current Shelf`** (**`Set Current Shelf`**, **`📍 Save to Cab … · Sh …`**, **`⚠️ Move to Cab … · Sh …`**), **`Vault List`** → **`Specimen List`**, and **`Botanical Registration`** → **`Registration Data`** (with a 1-line trainee cue).
     - Aligned status badges on both Specimen List and Detail View to Desktop's canonical **`[REV]`**, **`[REV+ERR]`**, and **`[UNREV]`** (eliminating `Taxon Issue ⚠` mislabeling on `Other Issue`).
     - Replaced developer and botanical jargon (`Testing candidate...`, `Viewport reclaimed`, `Other_problem` / `Current Value: True`, `Basionym & Homotypic` / `Homotypic`) with plain trainee wording, and aligned the `?` Field Guide `Collection Date` example to Desktop's `DAY.MONTH.YEAR` format (`15.07.1965`).
     - Refreshed the 3-step Mobile Walkthrough and Desktop's Mobile Companion Hallway Guide around the two core hallway goals: **(1) check that the physical object matches what is on file**, and **(2) record its Physical Location so it can be found again**.
- **User Impact**: New trainees moving from the Desktop 3-Minute Quick Tour to the Mobile Companion now see familiar labels (`Registration Data`, `[REV]` / `[REV+ERR]`, `Physical Location`, `DAY.MONTH.YEAR` dates), a warm non-intimidating **My Current Shelf** workflow, readable Cabinet/Shelf inputs on narrow phones, and working Curatorial Filters.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`, `tests/test_mobile_companion_offline.py` (80 passed)
  - [x] Mobile V2 JS syntax verified via `node --check`
  - [ ] Trainee Manual (`USER_GUIDE.md`) — sync Mobile Companion terminology (`My Current Shelf`, `Physical Location`) via 1-Prompt Sync Protocol

---

### Entry 48: Tutorial HUD App-Scoped Layering (No Longer Floats Over Chrome) & Live Multi-Monitor Tracking
- **Date**: 2026-11-24
- **Feature Area**: Interactive Tutorials (`ui/tutorials/tutorial_runner.py`)
- **What Changed**:
  1. **Removed OS-Global `-topmost` on Tutorial HUD**: Replaced `hud_win.attributes("-topmost", True)` with `hud_win.transient(self.root)` so the tutorial popup stays above Arbor's main window without hovering over Chrome or other applications when you switch windows.
  2. **Zero Primary-Monitor Flash & Mid-Step Monitor Following**: Withdrew `hud_win` until after `_position_hud()` runs so it opens directly on Arbor's current monitor without flashing on the primary monitor, and added a debounced `<Configure>` listener (cleanly unbound on exit) so dragging Arbor to another monitor mid-step brings the tutorial HUD along automatically.
- **User Impact**: Switching to Chrome or another app during a tutorial no longer leaves the tutorial popup stuck on top of your browser, and moving Arbor between monitors keeps both the tutorial HUD and highlight frames on the right screen.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`

---

### Entry 47: Default Physical Location Panel Position Changed to Middle (Below Images)
- **Date**: 2026-11-24
- **Feature Area**: Workspace Layout Defaults (`ui/main_window.py`, `ui/layout_settings.py`, `ui/unified_settings.py`)
- **What Changed**:
  - Updated all default fallbacks for `location_in_center` from `False` (Left column below Specimen Directory) to `True` (Middle column below the specimen images) across initial window setup, saved layout loading, and Unified Settings. Existing user preferences that explicitly saved `location_in_center: false` continue to be honored.
- **User Impact**: New users and default layouts now see the Storage Location panel centered below the specimen images, leaving the full height of the left column dedicated to the Specimen Directory.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_location_panel.py`, `tests/test_unified_settings.py`

---

### Entry 46: Unified Help Center Window (Matching Settings Layout & Persistent Learning Path)
- **Date**: 2026-11-24
- **Feature Area**: Help Center & Navigation (`ui/unified_help.py`, `ui/navigation_bar.py`, `ui/main_window.py`, `ui/help_dialogs.py`, `ui/tutorials/sandbox_manager.py`)
- **What Changed**:
  1. **New `UnifiedHelpWindow` (`ui/unified_help.py`)**: Created a Settings-style Help Center window (`840 × 620`, vertical left sidebar, scrollable bordered cards, `<Escape>` close, single-instance reuse) with 5 tabs: **Interactive Tutorials** (read-before-starting cards for all 5 Suggested Learning Path steps), **Quick Guides (30s)** (including an inline *How to Open Arbor* reference), **User Manuals** (Desktop Manual, Mobile Vault Guide, *"Don't Panic!"* Troubleshooting), **Keyboard Shortcuts** (visual keycaps + Cheat Sheet button), and **About & Updates** (version, update check, and **Reset Tutorial Checkmarks**).
  2. **Direct Top-Bar `HELP` Launch (`ui/navigation_bar.py`, `ui/main_window.py`, `ui/help_dialogs.py`)**: Replaced the nested `HELP ▾` dropdown menu with a direct **`HELP`** button opening the Unified Help Center (matching `F1` and `SETTINGS`).
  3. **Persistent Learning Path Progress (`ui/tutorials/sandbox_manager.py`)**: Confirmed `completed_tutorials` persists across sessions in `user_prefs.json` and added `reset_completed_tutorials()` so supervisors can reset checkmarks cleanly for a new trainee.
- **User Impact**: Clicking **HELP** (or pressing `F1`) now opens a calm, organized Help Center matching the Settings window where trainees can read what each tutorial covers before starting it, see their saved completion progress across sessions, and access manuals and shortcuts without navigating nested dropdown menus.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` (24 passed)

---

### Entry 45: Startup "How to Open Arbor" Guide Window & Desktop Tutorials Polish
- **Date**: 2026-11-24
- **Feature Area**: Startup Window Help (`ui/dialogs.py`) & Interactive Tutorials (`ui/tutorials/discrepancy_tutorial.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/database_tutorial.py`, `ui/tutorials/micro_guides.py`)
- **What Changed**:
  1. **Startup "How to Open Arbor" Window (`ui/dialogs.py`)**: Renamed the first item in the Startup Window's bottom-left **Help** menu to plain `"How to Open Arbor"` (no icon) and upgraded `_show_setup_help_msg` into a scrollable 4-step plain-English guide covering every section on Project Setup (`REQUIRED` Excel `.xlsx` collection file / Recent Projects / Demo Project, `RECOMMENDED` Specimen Photos, `OPTIONAL` Historical Books, and `LAUNCH SYSTEM` / `Mobile Companion`).
  2. **Historical Ledger Comparison (`ui/tutorials/discrepancy_tutorial.py`)**: Aligned window terminology to **"Problem Resolution"**, added Step 6 (`close_discrepancy_resolver`) highlighting `"Apply All Resolved"` (`hr_apply_all`) to save & close cleanly, added an **Old Names & Synonyms** tip in `More Details`, and added direct launch buttons on Step 7 (`Office Triage (REV+ERR)` and `Mobile Companion Hallway Guide`).
  3. **Office Triage (REV+ERR) (`ui/tutorials/triage_tutorial.py`)**: Replaced jargon with plain trainee language, removed the misleading `search_entry` highlight on Step 2, added an **Old Names & Synonyms** tip in `More Details`, and added direct launch buttons on Step 5.
  4. **Collections & New Specimens & Short Quick Guides (`ui/tutorials/database_tutorial.py`, `ui/tutorials/micro_guides.py`)**: Removed raw sheet/column jargon, prevented premature auto-advance on Step 4 of Collections & New Specimens (now requires ≥ 3 characters), added a direct **Practice in Sandbox (Office Triage)** button to `Hallway Follow-Up (30s)`, and noted photo thumbnail switching in `Image Zoom & Rotate (20s)`.
- **User Impact**: New trainees opening Arbor for the first time can click **Help → How to Open Arbor** for a simple visual guide to which files to load, and all desktop tutorials now share consistent window names, accurate highlights, and one-click next-tutorial handoffs.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` (23 passed)
  - [ ] Mobile Companion Hallway Guide (`micro_guides.py` → `start_armed_shelf_guide`) — intentionally paused pending upcoming Mobile Companion updates

---

### Entry 44: 1-Tap "Old Names & Synonyms" Lookup (Desktop + Mobile Companion V2)
- **Date**: 2026-11-24
- **Feature Area**: Taxonomy Reference (`backend/gbif.py`, `backend/mobile_server.py`, `backend/mobile_template_v2.py`, `ui/old_names_dialog.py`, `ui/main_window.py`, `ui/command_palette.py`)
- **What Changed**:
  1. **Offline Old-Family Map, Herbarium-Ranked GBIF Synonyms & Silent Disk Cache (`backend/gbif.py`)**: Added `get_old_family_names()` (8 classical botanical families + 20 common APG family merges/splits, 100% offline), `get_synonyms()` (fetches basionym & GBIF synonyms ranked **Basionym → Homotypic → Other**, cached in memory and silently persisted to `.arbor_synonyms_cache.json` next to the workbook for offline vaults), `collect_local_old_names()` (extracts prior museum names from `Log` & historical ledgers), and `compare_label_name()` with calibrated 3-state verdicts.
  2. **Mobile Companion V2 1-Tap `📜 Old names` Bottom Sheet (`backend/mobile_server.py`, `backend/mobile_template_v2.py`)**: Added `/api/object/<oid>/synonyms` and `/api/object/<oid>/check-label` endpoints and a hidden-by-default **`📜 Old names`** pill in the specimen header opening a read-only bottom sheet (`#oldNamesSheet`) with 0-typing ranked results, collapsible `Show more`, optional filter / GBIF check fallback, and a 1-tap `Flag Taxon Mismatch & Add Note` handoff.
  3. **Desktop `📜 Old Names` Popover (`ui/old_names_dialog.py`, `ui/main_window.py`, `ui/command_palette.py`)**: Added a compact `📜 Old Names` button in the Registration header (plus `TOOLS ▾ → View Old Names & Synonyms...` and `Ctrl+K`) opening a non-blocking, `<Escape>`-closable, read-only `OldNamesDialog`.
- **User Impact**: Trainees walking the hallway with a phone (or working at a desk) see a clean specimen card by default, and can tap **`📜 Old names`** once whenever a physical label has an unfamiliar name — immediately confirming whether it is an outdated synonym/family (keep the modern name!) or a genuine mismatch, even offline in concrete vaults.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_gbif.py`, `tests/test_mobile_companion.py`
  - [x] Mobile V2 JS syntax verified via `node --check`

---

### Entry 43: Redesigned 11-Step 3-Minute Quick Tour with Dynamic Highlights & Direct Next-Tutorial Buttons
- **Date**: 2026-11-24
- **Feature Area**: Interactive Tutorials (`ui/tutorials/review_tutorial.py`, `ui/tutorials/tutorial_runner.py`, `ui/registry_panel.py`)
- **What Changed**:
  1. **Streamlined 11-Step Quick Tour (`ui/tutorials/review_tutorial.py`)**: Starts cleanly on `#110` (removing the `#1003` jump), adds a dedicated Registration Data orientation step highlighting the entire Registration Data panel, adds a `Mark Object #110 as Reviewed` step so trainees see green `[REV]` before contrasting it with `#198`'s amber `[REV+ERR]`, splits `#198`'s Problem Resolution workflow into three focused steps (open Problem Resolution → apply `1927` → click `"Apply All Resolved"` to save & close), and removes the `[Space]` shortcut and auto-tab-switch on `"Other Issue"`.
  2. **2-Stage Dynamic Highlights, Custom Dropdown Label & Direct Launch Buttons (`ui/tutorials/tutorial_runner.py`, `ui/registry_panel.py`)**: Tagged `"Other Issue"` (`Other_problem`) with `tutorial_id="other_problem_checkbox"`, added sub-region `bbox_fn` + callable `target_id` support in `TutorialRunner` so Step 9 highlights the **Problems** tab header first and transitions to the **"Other Issue"** checkbox once clicked, added optional `details_label` (used for `"▸ Need help opening Arbor?"` on Step 11), and added reusable `action_buttons` so trainees can launch **Mobile Companion Hallway Guide (Recommended)** or **Historical Ledger Comparison** directly from the final step.
- **User Impact**: New trainees get a calmer, clearer desktop walkthrough that starts right on Object `#110`, teaches both clean `[REV]` and flagged `[REV+ERR]` badges, guides them step by step inside Problem Resolution, and lets them jump straight into the Mobile Companion Hallway Guide or Historical Ledger Comparison in one click.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` (22 passed)
  - [ ] Trainee Manual (`USER_GUIDE.md`) — sync if Quick Tour step summary is referenced via 1-Prompt Sync Protocol

---

### Entry 42: Multi-Monitor Negative-Coordinate Fix for Tutorial Highlights, HUD & Popups
- **Date**: 2026-11-24
- **Feature Area**: Multi-Monitor Positioning (`utils.py`, `ui/tutorials/tutorial_runner.py`, `ui/toast.py`, `ui/widgets.py`, `ui/image_toolbar.py`, `ui/main_window.py`) & Engineering Watchlist (`documentation/agent/CLAUDE_BUG_REVIEW_GUIDE.md`)
- **What Changed**:
  1. **Fixed Tk Negative-Coordinate Geometry (`utils.py`, `tutorial_runner.py`, `toast.py`, `widgets.py`, `image_toolbar.py`, `main_window.py`)**: Replaced all 12 `{:+d}` `.geometry(...)` format strings with explicit `+` anchors (`+{int(x)}+{int(y)}` via `utils.format_tk_geometry()`). In Tkinter, `-500` means *"500px from the right edge of the primary monitor"*, whereas `+-500` places the window at virtual coordinate `-500` on a secondary monitor.
  2. **Dialog-Aware Highlight Ownership (`ui/tutorials/tutorial_runner.py`)**: Updated `TutorialHighlight` to bind `transient(target_widget.winfo_toplevel())` so highlights over child dialogs (like Historical Ledger Comparison) track that dialog's monitor and Z-order cleanly.
  3. **Live Tk Regression Test & Watchlist**: Updated `test_multimonitor_negative_coordinates_positioning` in `tests/test_navigation_and_dialogs.py` to verify live `winfo_x() == -500`, and documented the `+{x}+{y}` (never `{:+d}`) rule in Section 4 of `CLAUDE_BUG_REVIEW_GUIDE.md`.
- **User Impact**: When running Arbor on a secondary monitor (including monitors to the left of or above the primary screen), tutorial highlight boxes, tutorial HUD popups, dialogs, toasts, and tooltips now stay locked to the exact monitor where Arbor is open.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Recurring Issues Watchlist: `documentation/agent/CLAUDE_BUG_REVIEW_GUIDE.md`
  - [x] Unit Tests: `tests/test_navigation_and_dialogs.py`, `tests/test_sandbox_tutorials.py`

---

### Entry 41: Tutorial HUD Global Shortcut Passthrough & Auto-Refocus
- **Date**: 2026-11-24
- **Feature Area**: Interactive Tutorials & Keyboard Shortcuts (`ui/keybindings.py`, `ui/tutorials/tutorial_runner.py`)
- **What Changed**:
  1. **Target-Window Shortcut Forwarding (`ui/keybindings.py`)**: Extended `KeybindingManager.bind_global_shortcuts(target=None)` so Arbor's global shortcuts (`Ctrl+F`, `Ctrl+H`, `Ctrl+K`, `Ctrl+G`, `Ctrl+Enter`, `Alt+R`, etc.) can be forwarded from a floating non-modal HUD onto the main window (returning focus to `root` before invoking the handler) without leaking into modal dialogs.
  2. **Floating HUD Passthrough & Gentle Refocus (`ui/tutorials/tutorial_runner.py`)**: Bound global shortcuts onto `TutorialRunner.hud_win` on creation and added `_refocus_main_if_hud_focused()` after `Next →`, `← Back`, and drawer toggles so keyboard focus immediately returns to Arbor's main window without stealing focus from any open child dialog (like Historical Ledger Comparison).
- **User Impact**: Trainees can now press `Ctrl+F`, `Ctrl+H`, `Ctrl+K`, or any other Arbor shortcut immediately while reading or clicking through the tutorial HUD — no more having to click the main window first.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py`

---

### Entry 40: Overnight Smoke-Test Fixes (Tutorial Validator & `← Previous` Bounce Fixes, 6 Dialog `<Escape>` Bindings, Shortcut Parity, Mobile `Retry` Contrast, & High-DPI Toolbar Spacing)
- **Date**: 2026-11-24
- **Feature Area**: Tutorials (`ui/tutorials/micro_guides.py`, `ui/tutorials/tutorial_runner.py`, `ui/tutorials/review_tutorial.py`, `ui/tutorials/discrepancy_tutorial.py`), Dialog Ergonomics (`ui/database_ops.py`, `ui/dialogs.py`, `ui/group_editor.py`, `ui/new_database_wizard.py`), Menus & Toolbars (`ui/main_window.py`, `ui/command_palette.py`, `ui/filter_panel.py`, `ui/object_context_bar.py`, `ui/registry_panel.py`, `ui/image_toolbar.py`), & Mobile Companion V2 (`backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Fixed Tutorial Auto-Skip & `← Previous` Bounce (`micro_guides.py`, `tutorial_runner.py`, `review_tutorial.py`)**: Excluded `TutorialRunner`'s own HUD window from `_is_mobile_dialog_open()` so Step 2 of the Mobile Companion Hallway Guide no longer self-skips; added `auto_validate=False` on `TutorialRunner.prev_step()` so stepping backward never bounces forward on already-satisfied steps; decoupled `#1003` initial selection in `review_tutorial.py` so `load_object("1003")` always runs cleanly.
  2. **Fixed Missing Tutorial Highlights & Prefixes (`main_window.py`, `discrepancy_tutorial.py`, `micro_guides.py`)**: Tagged `self.problem_frame.tutorial_id = "problem_flags_frame"` on initial build, ensured `update_history_indicator("1001")` runs on entering `discrepancy` Step 2 so `history_indicator_label` is mapped, and stripped remaining `1.`/`2.` prefixes in `start_image_controls_guide`.
  3. **Menu & Command Palette Shortcut Truthfulness (`command_palette.py`, `main_window.py`)**: Changed `Open Excel Database...` shortcut label in Command Palette from `Ctrl+O` → `File`, and moved `(F1)` from `Keyboard Shortcuts` to `Help Hub & Suggested Learning Path (F1)` to match `ui/keybindings.py`.
  4. **Consistent `<Escape>` Close & DPI Scaling (`database_ops.py`, `dialogs.py`, `group_editor.py`, `new_database_wizard.py`, `registry_panel.py`, `image_toolbar.py`, `filter_panel.py`, `object_context_bar.py`)**: Bound `<Escape>` on the 6 remaining modal/popup dialogs (`Excel File In Use`, `StartupDialog`, `Delete Tab`, `Move Field`, `Dropdown Choices`, `Batch Add Multiple Fields`), wrapped 3 remaining unscaled fonts in `sc(...)`, and compacted the directory/context toolbar buttons (`🔍`, `📱`, `📱 Phone`) so nothing clips at 1280×800 under 125–150% DPI.
  5. **Mobile V2 `Retry` Contrast (`backend/mobile_template_v2.py`)**: Replaced undefined `bg-forest` with `bg-emerald-700 text-white` + inline `#2d5a3c` fallback so the error-recovery `Retry` button is high-contrast both online and offline.
- **User Impact**: Tutorials never auto-skip or bounce backward when pressing `← Previous`, every dialog closes with `Escape`, menus display accurate shortcuts, high-DPI laptop toolbars don't clip, and the mobile `Retry` button is clearly legible offline.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Full test suite verified: `python -m pytest tests/ -q`
  - [x] Mobile V2 JS syntax verified via `node --check`
  - [x] `data/tutorial_images/` untouched

---

### Entry 39: Responsive Loading States Across Desktop & Mobile (Indeterminate Progress, Async Historical DBs & SQLite Import, Mobile Detail Loading)
- **Date**: 2026-11-23
- **Feature Area**: Status Bar Progress (`ui/main_window.py`), Database Exports & Imports (`ui/database_ops.py`), Backup Restore (`ui/autosave_handler.py`), & Mobile Companion V2 (`backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Ref-Counted Indeterminate Progress & Timer Cancellation (`ui/main_window.py`)**: Upgraded `_show_progress(text, maximum, indeterminate=False, task_id=None)` to animate in `indeterminate` mode for unknown-duration tasks (instead of sitting frozen at 0%), track overlapping background tasks by `task_id` so one finishing never kills another's progress bar, and cancel any stale 1.5s status-clear timer when a new operation starts.
  2. **Non-Blocking Historical DBs, SQLite Import & Autosave Restore (`ui/main_window.py`, `ui/database_ops.py`, `ui/autosave_handler.py`)**: Moved `load_historical_databases()`, `import_to_sqlite()`, and `_restore_autosave()` off the main Tkinter thread into `app_worker.run_in_background` with in-flight re-entrancy guards, progress bars, and top-of-screen toast cues.
  3. **Wired `open_excel_from_path()` Progress & Chained `save_as()` (`ui/database_ops.py`, `ui/main_window.py`)**: Added `_show_progress` to `open_excel_from_path()` (presets/recent/new DB loads), chained `save_as()` export via `save_session(..., on_complete=...)` so saves and exports never race, and added in-flight guards + toasts to `export_filtered_list()` and `check_gbif_action()`.
  4. **Mobile V2 Detail Loading Overlay, Race Guard & Error Retry (`backend/mobile_template_v2.py`)**: Added `#detailLoadingOverlay` over `#swipeArea` in `openDetailView(oid)` so trainees cannot accidentally tap the previous specimen's form or review button on slow vault Wi-Fi, ignored stale fetch responses on rapid taps, and added an inline **Retry / Back to List** recovery state on network errors.
- **User Impact**: Long operations (loading older Excel databases, exporting, importing, restoring backups, checking GBIF, and opening specimens on mobile) now show clear, animated loading states instead of appearing frozen or flashing stale data.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_ui_ergonomics.py`, `tests/test_mobile_companion.py`, `tests/test_historical.py`, `tests/test_gbif.py`, `tests/test_hardened_data_safety.py`
  - [x] Mobile V2 JS syntax verified via `node --check`

---

### Entry 38: Round 3 Pre-Release Audit Fixes & Permanent Recurring Issues Watchlist
- **Date**: 2026-11-23
- **Feature Area**: Tutorials (`ui/tutorials/triage_tutorial.py`, `ui/tutorials/review_tutorial.py`, `ui/tutorials/micro_guides.py`), Image Viewport (`ui/image_panel.py`), File Menu (`ui/main_window.py`), Problem Queue Dialog (`ui/object_problem_resolver.py`), & Engineering Watchlist (`documentation/agent/CLAUDE_BUG_REVIEW_GUIDE.md`)
- **What Changed**:
  1. **Tightened Triage Queue Validator (`triage_tutorial.py`)**: Narrowed `_is_problem_queue_open` from `"Problem"` to `"Problem Resolution"` so opening the modal scope picker (`Process Objects with Problems`) no longer prematurely advances Step 3 before the trainee clicks `OPEN QUEUE`.
  2. **Fixed Image Guide Highlight & Step Numbering (`image_panel.py`, `micro_guides.py`)**: Tagged `self.image_container.tutorial_id = "image_container"` so `Image Zoom & Rotate — 20 sec` highlights the image viewport cleanly, and removed the remaining `1.`/`2.` title prefixes in `start_hallway_followup_guide`.
  3. **Fixed Quick Tour `← Previous` Tab Trap (`review_tutorial.py`)**: Added `_focus_details_tab` as `on_enter` on Steps 2 and 4 so navigating backward from Step 5 (`Problems` tab) restores the `Details` tab and keeps `Collection Date` visible for highlighting.
  4. **Removed Misleading Shortcut Label (`main_window.py`)**: Removed `(Ctrl+O)` from `FILE ▾ → Open Excel Database...` since `Ctrl+O` toggles the Left Specimen Directory.
  5. **Added `<Escape>` Close to `ProblemQueueDialog` (`object_problem_resolver.py`)**: Bound `<Escape>` to `self.destroy` for full dialog keyboard consistency.
  6. **Permanent Recurring Issues Watchlist (`documentation/agent/CLAUDE_BUG_REVIEW_GUIDE.md`)**: Documented all 7 recurring pre-release issue patterns (missing `<Escape>`, unscaled/float fonts, multi-monitor centering, tutorial `target_id` & `← Previous` tab-switching, shallow/broad validators, stale menu labels/shortcuts, and tutorial copy discipline) so every future agent checks them automatically.
- **User Impact**: Tutorials advance at the exact right moment, `← Previous` never leaves you stuck on the wrong tab, `Escape` closes the Problem Queue dialog cleanly, and the File menu no longer shows a conflicting shortcut.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Recurring Issues Watchlist: `documentation/agent/CLAUDE_BUG_REVIEW_GUIDE.md` (Section 4)
  - [x] Full test suite verified: `python -m pytest tests/ -q`

---

### Entry 37: Tutorial Polish & Menu Parity (Auto-Tab Switch, Nested Validator Fix, 5-Step `HELP ▾` Sync, Exact Menu Labels)
- **Date**: 2026-11-23
- **Feature Area**: Interactive Tutorials (`ui/tutorials/review_tutorial.py`, `ui/tutorials/discrepancy_tutorial.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/database_tutorial.py`, `ui/tutorials/micro_guides.py`, `ui/tutorials/tutorial_runner.py`) & Top Bar Menus (`ui/main_window.py`, `ui/navigation_bar.py`)
- **What Changed**:
  1. **Quick Tour Flow Polish (`review_tutorial.py`, `tutorial_runner.py`)**: Automatically switches `reg_notebook` to the `Problems` tab on Step 5 (`flag_other_issue`), calls `update_idletasks()` after `step.on_enter` so the highlight frame renders accurately on the first frame, tightened Step 2 copy, and removed the 3-year spoiler from Step 4's main text (kept inside `▸ The Answer`).
  2. **Clean Step Numbering Across All 5 Tutorials**: Removed redundant `0.`/`1.`/... prefixes from step titles so the HUD's `STEP X OF Y` header is always consistent.
  3. **Fixed Stuck Validator & Highlight Target (`discrepancy_tutorial.py`)**: Replaced the shallow `winfo_children()` check in Step 2 (`open_resolver`) with recursive `_has_widget_with_tutorial_id()` so opening Historical Ledger Comparison (`Ctrl+H`) auto-advances reliably, and pointed Step 4 (`apply_changes`) to `hr_cards` instead of `hr_apply_all`.
  4. **Synced `HELP ▾` Dropdown & Menu Labels (`main_window.py`, `navigation_bar.py`, `triage_tutorial.py`, `database_tutorial.py`)**: Updated `HELP ▾` to mirror the 5-Step Suggested Learning Path (removed stale `"Cabinet 21"`, added `"4. Office Triage (REV+ERR)"`, wired `start_tutorial_flow("triage")`, and renamed Hub entry to `"Help Hub & Suggested Learning Path"`). Tagged `TOOLS ▾` with `tutorial_id="tools_nav_btn"` and aligned tutorial copy with exact menu labels (`Open Problem Queue & Resolver...`, `New Database Wizard...`, `New Specimen Object...`).
- **User Impact**: Every step in the 5-Step Suggested Learning Path now matches the exact menu items in the top bar, highlights visible controls cleanly, and auto-advances when the trainee performs the action.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`, `tests/test_navigation_and_dialogs.py`

---

### Entry 36: Pre-Release DPI & Ergonomics Polish (Welcome Card Scaling, Quick Tour `#110` Search + "The Answer" Dropdown, `<Escape>` Close on 6 Dialogs, `MobilePanel` `sc()` Scaling)
- **Date**: 2026-11-23
- **Feature Area**: Demo Welcome Card (`ui/database_ops.py`), 3-Minute Quick Tour & HUD (`ui/tutorials/review_tutorial.py`, `ui/tutorials/tutorial_runner.py`), Dialog Keyboard Ergonomics (`ui/image_popup.py`, `ui/quick_peek.py`, `ui/create_collection_dialog.py`, `ui/mobile_dialog.py`, `ui/update_dialog.py`, `ui/autosave_handler.py`), & Phone Connector DPI Scaling (`ui/mobile_panel.py`)
- **What Changed**:
  1. **Welcome Card Button Scaling (`ui/database_ops.py`)**: Stacked the primary **`🎓 Start 3-Minute Quick Tour`** CTA full-width above a clean 2-button secondary row (`View Learning Path` | `Explore on My Own`) with auto-fit `winfo_reqwidth()` sizing so button labels never clip at 125%–150% Windows DPI.
  2. **Quick Tour `#110` Search Step & Collapsible `▸ The Answer` Dropdown (`ui/tutorials/review_tutorial.py`, `ui/tutorials/tutorial_runner.py`)**: Started the Quick Tour sandbox on `#1003` so Step 1 has trainees actively search up **`#110`** (`Ctrl+F`); removed the `00.06.1910` spoiler from Step 2's prompt, added the tip *"You might have to check out both images (front & back)!"*, and added a collapsible amber **`▸ The Answer`** drawer (`ActionStep.answer`) for Steps 2 and 4.
  3. **Consistent `<Escape>` Close Across 6 Dialogs**: Bound `<Escape>` to close on `ImagePopup` (matching `USER_GUIDE.md`), `Quick Peek`, `Create New Collection`, `MobileDialog`, `UpdateDialog`, and `Autosave Archive Manager`.
  4. **Phone Connector DPI Scaling (`ui/mobile_panel.py`)**: Wrapped all 76 hardcoded font sizes in `sc(...)` so the Phone Connector scales uniformly with the rest of Arbor on high-DPI Windows laptops.
- **User Impact**: The Demo Welcome Card and Phone Connector scale crisply without clipped buttons, the Quick Tour lets trainees genuinely discover `#110`'s date from its photos (with a 1-click "The Answer" safety net), and pressing `Escape` closes every popup window consistently.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`, `tests/test_mobile_companion.py`, `tests/test_navigation_and_dialogs.py`, `tests/test_images.py`
  - [x] `data/tutorial_images/O-V-OE-110-02.jpg` preserved untouched

---

### Entry 35: Unified `Comment` Field, Non-Destructive Legacy Note Reveal & Opt-In Cleanup
- **Date**: 2026-11-23
- **Feature Area**: Registration Form (`ui/registry_panel.py`, `ui/main_window.py`, `ui/command_palette.py`), Mobile V2 Field Guide (`backend/mobile_template_v2.py`), & Tests (`tests/test_navigation_and_dialogs.py`)
- **What Changed**:
  1. **Unified `Comment` Box with Non-Destructive Legacy Reveal (`ui/registry_panel.py`)**: Placed **`Comment`** first inside *Audit Notes & Descriptions* (matching Mobile Companion V2) and automatically hid empty `Observation` / `ProblemDescription` boxes. Whenever an older specimen has existing text in `Observation` or `ProblemDescription`, that field automatically appears underneath `Comment` labeled `(Legacy)` so zero existing museum data is ever hidden or overwritten.
  2. **Calm, Reassuring One-Time Opt-In Cleanup (`TOOLS ▾ → Combine Legacy Notes into Comment...` & `Ctrl+K`)**: Added `RegistryPanel.merge_legacy_notes_into_comment()` with a clear, reassuring confirmation prompt explaining that existing comments are never overwritten, nothing is written to disk until `Ctrl+S`, and opting out leaves everything untouched.
  3. **Mobile V2 Field Guide Parity (`backend/mobile_template_v2.py`)**: Replaced `Observation` and `ProblemDescription` in Mobile V2's `?` *What the Fields Mean* guide with **`Comment`** so Desktop and Mobile match 1:1.
- **User Impact**: Trainees see one clear `Comment` box on both Desktop and Phone (zero confusion about which of 3 note boxes to type in), while older specimens with text in legacy fields still display them safely until optionally combined.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_navigation_and_dialogs.py`
  - [x] Master Lexicon & Mobile V2 parity verified

---

### Entry 34: Test Suite Consolidation (52 → 21 Domain Suites), Zero-Warning Tkinter Teardown & Full-Repo CI Coverage
- **Date**: 2026-11-23
- **Feature Area**: Test Suite (`tests/`, `conftest.py`), CI Pipeline (`.github/workflows/ci.yml`), & Maintainer Docs (`MAINTAINER_HANDOFF.md`)
- **What Changed**:
  1. **Zero-Warning Headless Tkinter Teardown (`conftest.py`)**: Guarded `tk.Variable.__del__` during headless pytest GC after root destruction and ran `gc.collect()` before `root.destroy()`, eliminating all 13 recurring `PytestUnraisableExceptionWarning` teardown warnings.
  2. **Consolidated 52 Fragmented Test Files → 21 Clean Domain Suites (`tests/`)**: Merged 32 tiny/overlapping micro-files into cohesive domain suites (`test_gbif.py`, `test_images.py`, `test_repository.py`, `test_hardened_data_safety.py`, `test_historical.py`, `test_problem_persistence_fix.py`, `test_location_panel.py`, `test_navigation_and_dialogs.py`, `test_ui_ergonomics.py`, `test_filter.py`, `test_mobile_companion_offline.py`), and replaced 17 brittle HTML/CSS substring-mirror tests in `test_mobile_companion.py` with a concise high-signal contract test while keeping 100% of API, auth, data-safety, and UI-smoke coverage.
  3. **Full-Repo CI Verification (`.github/workflows/ci.yml`, `MAINTAINER_HANDOFF.md`)**: Upgraded CI from running 9 hardcoded test files to running the entire consolidated `tests/` directory (`python -m pytest tests/ -q`) on every push and PR.
- **User Impact**: Zero runtime change for museum trainees; faster, cleaner maintenance and 100% automated CI protection across the entire application before every `.exe` release.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Maintainer Handoff: `MAINTAINER_HANDOFF.md`
  - [x] CI Pipeline: `.github/workflows/ci.yml`

---

### Entry 33: Slate-Blue Historical Suggestions Pill, Mobile First-Time Tutorial Toggle & Learning Path Steps 2–5 Upgrade
- **Date**: 2026-11-23
- **Feature Area**: Historical Suggestions Indicator (`ui/main_window.py`, `ui/historical_suggestions.py`), Phone Connector & Mobile V2 (`ui/mobile_panel.py`, `backend/mobile_server.py`, `backend/mobile_template_v2.py`), Learning Path Tutorials Steps 2–5 (`ui/tutorials/discrepancy_tutorial.py`, `ui/tutorials/micro_guides.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/database_tutorial.py`, `ui/tutorials/sandbox_manager.py`), & Tests (`tests/test_sandbox_tutorials.py`, `tests/test_mobile_companion.py`)
- **What Changed**:
  1. **Slate-Blue Clickable Historical Suggestions Pill (`ui/main_window.py`, `ui/historical_suggestions.py`)**: Upgraded `history_indicator_label` from plain blue text into an Arbor-styled Slate Blue (`#4a7b9d`) hoverable pill showing the exact count (`History: N suggestion(s) · Ctrl+H`), a calm muted pill when historical records match (`History: matches current`), and hidden cleanly when no historical data exists for the specimen (full Light & Dark Mode support).
  2. **Mobile First-Time Tutorial Toggle (`ui/mobile_panel.py`, `backend/mobile_server.py`, `backend/mobile_template_v2.py`)**: Added a `"Launch with mobile companion tutorial for first-time users"` checkbox to the Phone Connector setup card (ON by default, persisted to `user_prefs.json["mobile_show_walkthrough"]`), wired live to `MobileServer.update_walkthrough_setting()` and injected into Mobile V2 (`ARBOR_SHOW_WALKTHROUGH`) so experienced staff can disable auto-launching the 3-step phone guide while keeping manual replay available.
  3. **Learning Path Steps 2–5 Polish (User1 & User2 Pass)**:
     - **Plain-Language Copy**: Removed bare *"Excel"* references from main tutorial instructions in favor of *"your currently registered collection"* / *"collection file"* (keeping Excel details inside the optional collapsible drawer).
     - **Step 2 (`discrepancy_tutorial.py`)**: Added Step 0 framing, per-card `Apply` validator (guarding User1 against blind `Apply All`), and kept the desk-only physical-review rule.
     - **Step 3 (`micro_guides.py:start_armed_shelf_guide`)**: Upgraded into an interactive Desktop-to-Phone walkthrough highlighting the top-bar `MOBILE` button (`mobile_nav_btn`), explaining QR pairing, PIN & tutorial toggles, and end-of-shift saving on desktop.
     - **Step 4 (`triage_tutorial.py`, `sandbox_manager.py`)**: Added Step 0, clickable menu paths for User1 alongside `Ctrl+G`/`Ctrl+K`/`Alt+→` for User2, real validators, and updated `#2001` to realistic `Other Issue` (`"Bent display — needs workshop check"`) vs. `#2002` clearable date flag.
     - **Step 5 (`database_tutorial.py`, `sandbox_manager.py`)**: Added dedicated clean 2-row `mock_type="database"` sandbox (decoupled from `#110` photos), Step 0 optional framing, `New Specimen` wording, and a hands-on Step 3 field-entry validator.
- **User Impact**: Curators immediately spot when historical suggestions exist via a crisp Slate Blue pill, staff launching Mobile Companion can toggle the first-time phone walkthrough on or off, and every tutorial in the 5-step Learning Path is hands-on, jargon-free, and tailored for both brand-new trainees and experienced curators.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` & `tests/test_mobile_companion.py`
  - [x] AI UI Guide & Master Lexicon compliance

---

### Entry 32: Real-Photo 3-Minute Quick Tour (#110 & #198), 3-Source Historical Verification & 5-Step Suggested Learning Path
- **Date**: 2026-11-23
- **Feature Area**: Interactive Tutorials (`ui/tutorials/review_tutorial.py`, `ui/tutorials/sandbox_manager.py`, `ui/tutorials/discrepancy_tutorial.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/database_tutorial.py`, `ui/tutorials/micro_guides.py`), Help Hub & Demo Welcome (`ui/help_dialogs.py`, `ui/database_ops.py`), Mobile V2 Walkthrough (`backend/mobile_template_v2.py`), Bundled Tutorial Photos (`data/tutorial_images/`, `main.spec`, `build_exe.bat`), & Tests (`tests/test_sandbox_tutorials.py`)
- **What Changed**:
  1. **Real-Photo Quick Tour (`#110` & `#198`)**: Optimized and bundled 4 real front/back specimen photos in `data/tutorial_images/` (~886 KB total, packaged in `main.spec` & `build_exe.bat`) and auto-mounted them inside `SandboxManager` (restoring the user's original image mode/folder on exit).
  2. **Redesigned 7-Step 3-Minute Quick Tour (`ui/tutorials/review_tutorial.py`)**:
     - **Step 0**: Concise Desktop vs. Mobile Companion overview (hallway auditing, finding already-reviewed objects, loaning out objects) + Practice Mode safety.
     - **Step 1 (`#110` *Ephedra major*, NO historical data)**: Teaches that Arbor shows currently registered data, clarifies that photos stand in for inspecting the physical object, and teaches the `DAY.MONTH.YEAR` format (`01.08.2015` / `00.08.2015` / year-only) — validator accepts `00.06.1910` or `06.1910` for *"juni 1910"*.
     - **Steps 2–3 (`#198` *Corylus colurna*, 3-source historical conflict)**: Compares Current (`1963`), Ledger Book 1 (`1927` ✅), and Old Card Catalog (`1912` ❌) so trainees learn that older ledgers can be wrong and must be checked against the physical object (`1927` or `00.00.1927`).
     - **Step 4 (`Other Issue`)**: Explains that field-specific flags are mostly auto-flagged by Arbor, while physical condition issues (like `#198`'s bent display) are flagged with **`Other Issue`** (`Other_problem`) + optional `Comment`.
     - **Step 5 (Golden Rule of `✓ Mark as Reviewed`)**: Explicitly teaches that **`✓ Mark as Reviewed` is ONLY for objects you have physically inspected** — never just from historical data at a desk.
  3. **5-Step Suggested Learning Path (`ui/help_dialogs.py`, `ui/database_ops.py`)**: Replaced the unlabeled 4-button sandbox row in the Help Hub with an ordered 5-step Learning Path (1. 3-Minute Quick Tour · 2. Historical Ledger Comparison · 3. Mobile Companion Hallway Guide *(Optional · Needs your phone)* · 4. Office Triage · 5. Collections & New Specimens *(Optional)*) with persistent `✓ Done` badges, plus a **Learning Path** button on the Demo Welcome Card.
  4. **Aligned Discrepancy Tour & Mobile 3-Step Walkthrough**: Upgraded `discrepancy` sandbox to 2 conflicting historical books + explicit reminder NOT to mark Reviewed without physical inspection; updated Mobile V2 `WALKTHROUGH_SLIDES` to cover already-reviewed lookups, **Loaned Out** toggling, `Other Issue` + `Comment`, and the physical-inspection rule.
- **User Impact**: New trainees immediately understand Desktop vs. Mobile roles, practice transcribing real labels (`#110` & `#198`) with the exact `DD.MM.YYYY` convention, learn to treat historical suggestions critically, never confuse desk edits with physical review, and can follow a clear 5-step Learning Path at their own pace.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Tutorial Developer Guide: `documentation/agent/TUTORIAL_GUIDE.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` & `tests/test_mobile_companion.py`
  - [x] Packaging: `main.spec` & `build_exe.bat`

---

### Entry 31: Mobile Companion V2 Touch Gestures Pass (Horizontal Tab Swipe, Pinch/Pan/Double-Tap Photo Zoom, Swipe-Down Bottom Sheet & 40px+ Targets)
- **Date**: 2026-11-23
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`) & Tests (`tests/test_mobile_companion.py`)
- **What Changed**:
  1. **Horizontal Tab Swipe (`initTouchGestures()` on `#swipeArea`)**: Wired real `touchstart` / `touchend` swipe detection (with vertical-scroll lock `|dx| >= 52 && |dx| > |dy| * 1.5` and input/horizontal-scroller guards) so hallway auditors can flick one-handed between **Details ↔ Location ↔ Problems** with light haptic feedback.
  2. **Pinch-to-Zoom, 1-Finger Drag-Pan & Double-Tap Zoom (`initPhotoViewerTouchGestures()` on `#photoViewerViewport`)**: Added 2-finger pinch zoom (`0.8×–4.5×`), 1-finger drag panning (`photoPanX` / `photoPanY`) when zoomed in, and double-tap toggle between `1.0×` and `2.2×` inside the fullscreen Specimen Photo viewer (`touch-action: none`).
  3. **Swipe-Down Bottom Sheet Dismiss (`#storedAsSheetCard`)**: Added a top drag handle and live pull-down-to-close gesture (`>= 85px`) on the Storage Vessel bottom sheet.
  4. **Enlarged 40px+ Modal & Action Touch Targets**: Bumped close `✕` buttons across modals/bottom sheets (`min-w-[40px] min-h-[40px]`), fullscreen photo controls (`min-h-[38px]`–`40px`), offline Retry button (`min-h-[38px]`), and Batch queue remove buttons (`min-w-[38px] min-h-[38px]`) with consistent `tap-active` press feedback.
- **User Impact**: Phone auditing feels genuinely native in the hallway—trainees can swipe between tabs with one thumb, pinch and pan handwritten specimen labels cleanly, pull bottom sheets down to dismiss them, and tap close/action buttons reliably even while wearing gloves.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`
  - [x] Zero-Build, Offline-First & Zero-Barcodes compliance verified

---

### Entry 30: Desktop Visual Polish Pass (Clean Top Nav Icons, Crisp Image Toolbar Glyphs & DPI Scaling, Hardened Atomic `save_prefs()`)
- **Date**: 2026-11-23
- **Feature Area**: Top Navigation Bar (`ui/navigation_bar.py`, `ui/main_window.py`, `ui/database_ops.py`), Image Toolbar (`ui/image_toolbar.py`), Preferences Persistence (`config.py`), & Tests (`tests/test_config.py`, `tests/test_image_toolbar.py`)
- **What Changed**:
  1. **Cohesive, Laptop-Friendly Top Navigation Bar (`ui/navigation_bar.py`, `ui/main_window.py`, `ui/database_ops.py`)**: Replaced clashing color emojis and the macOS `⌘` glyph with clean labels (`TOOLS ▾`, `MOBILE`, `⚙ SETTINGS`, `HELP ▾`, `Commands (Ctrl+K)`), kept legacy `toolbar_buttons` aliases intact, and synced `responsive_btn_config` (including `Next Ledger Match`) so narrow-window Tabler icon collapse stays aligned.
  2. **Crisp Typographic Image Toolbar Icons & DPI `sc()` Scaling (`ui/image_toolbar.py`)**: Replaced emoji `➕`/`➖`/`🔍` with uniform typographic `+` / `−` / `{pct}% · ↻ {deg}°`, switched `"Segoe UI"` → `"Inter"`, and wrapped hardcoded font sizes and paddings in `sc(...)`.
  3. **Hardened Atomic `save_prefs()` (`config.py`)**: Added a thread lock (`_prefs_io_lock`), in-memory JSON pre-serialization before touching disk, unique per-write temp files (`tempfile.NamedTemporaryFile`), `flush()` + `os.fsync()`, atomic `os.replace()`, and automatic temp cleanup on failure so rapid or concurrent preference saves can never corrupt `user_prefs.json`.
- **User Impact**: The top navigation bar and image toolbar look calmer, sharper, and less cramped on 13-inch laptops at 125%–150% scaling, and user preferences are protected against accidental file corruption on rapid/concurrent saves.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_config.py` & `tests/test_image_toolbar.py`
  - [x] AI UI Guide & Master Lexicon compliance

---

### Entry 29: No-Images Bottom Location Dock, Dark-Mode Summary Hub & Multi-Monitor Window Positioning Pass
- **Date**: 2026-11-23
- **Feature Area**: Main Workspace Layout (`ui/main_window.py`, `ui/layout_settings.py`), Specimen Image Panel (`ui/image_panel.py`), Multi-Monitor Window & Overlay Positioning (`utils.py`, `ui/gbif_dialog.py`, `ui/toast.py`, `ui/autosave_handler.py`, `ui/quick_peek.py`, `ui/image_popup.py`, `ui/image_toolbar.py`, `ui/widgets.py`), & Tests (`tests/test_location_center_toggle.py`, `tests/test_navigation_and_dialogs.py`)
- **What Changed**:
  1. **Clean 2-Column Workspace + Bottom Storage Location Dock (`ui/main_window.py`, `ui/image_panel.py`, `ui/layout_settings.py`)**: When the photo viewport is hidden (`F8` or Offline mode), Arbor now collapses the empty middle column so the **Specimen Directory** and **Registration Panel** expand into a clean 2-column layout, docks the **Curatorial Command Strip** along the top of the workspace, and—if **Storage Location** is set to Center/Bottom—docks it neatly along the bottom of the screen just above the Bottom Progress Bar (with zero blank void). Also fixed `ImagePanel.update_image_view_button()` to delegate to `_sync_middle_panes()` and restore images at index `0`.
  2. **Actionable, Dark-Mode-Aware No-Images Summary Hub (`ui/image_panel.py`)**: Upgraded `render_specimen_summary_hub()` with full Dark Mode palette support, a compact top action bar when no image folder is connected (**Select Image Folder…**, **Use Online Photos**, **Hide Photo Pane (F8)**), a subtle `Change Image Source…` link when a single specimen has 0 matched photos, humanized 2-column wrapping issue pills (`Box Label Issue`, `Collection Date Issue`), and Canonical Trainee Lexicon copy.
  3. **Complete Multi-Monitor Window & Overlay Positioning (`utils.py`, `ui/gbif_dialog.py`, `ui/toast.py`, `ui/autosave_handler.py`, `ui/quick_peek.py`, `ui/image_popup.py`, `ui/image_toolbar.py`, `ui/widgets.py`, `ui/main_window.py`)**: Added `utils.format_tk_geometry()`, routed `GBIFMatchDialog`, `Autosave Archive Manager`, `Quick Peek`, and `ImagePopup` through `utils.center_and_fit_toplevel()`, and switched `Toast`, tooltips, top-bar dropdown menus, and the search popup to signed `{x:+d}{y:+d}` coordinates (removing primary-monitor `max(0, x)` / `screen_w` snapping on secondary displays).
- **User Impact**: Curators working without specimen photos get a spacious 2-column layout with Storage Location cleanly anchored along the bottom of the screen (or 1-click folder/hide buttons when the middle pane is open), and users who drag Arbor onto a second monitor see every dialog, toast, dropdown, and tooltip open on that exact screen.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_location_center_toggle.py` & `tests/test_navigation_and_dialogs.py`
  - [x] Master Lexicon & AI UI Guide compliance

---

### Entry 28: Mobile Companion V2 Hallway Ergonomics & Visual Polish (Floor Selector, Glove-Friendly Touch Targets, 360px Header, Offline Active Tab)
- **Date**: 2026-11-22
- **Feature Area**: Mobile Companion V2 (`backend/mobile_template_v2.py`) & Tests (`tests/test_mobile_companion.py`)
- **What Changed**:
  1. **Added `Floor` Selector to Audit Station Launchpad**: Added `#launchFloorSelect` (`-2`, `-1`, `1`–`4`) to `#stationSetupCard`, wired it into `applyStationSetup()` and `initStationLaunchpad()` (replacing hardcoded `floor: '1'`), and included `Fl <floor>` in the active station pill.
  2. **Glove-Friendly Touch Targets & 360px-Safe Header**: Enlarged `#btnStampArmedShelf` to `min-h-[38px]` (`text-xs`), enlarged `#detailView` Prev/Next steppers from `28px` to `36px` (`w-9 h-9`), hid `#btnListUndo` until edits exist, and tightened `#listView` header spacing + `#detailView` chrome so 360px phones have more room without collisions.
  3. **Clean Plain-English Mobile Labels**: Updated `"Accession ID (0894...)"` → `"Object # (1, 2, 3...)"`, `"Archival Photo Folio"` → `"Specimen Photos"`, `"0 Active Discrepancies"` → `"0 Open Issues"`, `"Data Integrity Flags"` → `"Issue Checklist"`, and removed duplicate raw `${probName}` code subtitles under humanized problem buttons.
  4. **Offline Active-Tab Highlight**: Added `html.arbor-offline-css .tab-btn.text-ink` active pill styling so the selected tab (`Details` / `Location` / `Problems`) stays clearly highlighted in offline concrete vaults.
- **User Impact**: Trainees auditing basement floors (`-1`/`-2`) can arm the exact Floor from the Audit Station, tap Stamp Target and Prev/Next comfortably even with gloves, and read cleaner jargon-free labels on narrow phones both online and offline.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`
  - [x] Zero-Barcodes & Zero-Build compliance verified

---

### Entry 27: Design-System Visual Polish (`MobilePanel` CTAs & Dark Mode, Startup Typography, Top-Bar `⌘ Commands (Ctrl+K)` Pill)
- **Date**: 2026-11-22
- **Feature Area**: Phone Connector (`ui/mobile_panel.py`), Startup Dialog (`ui/dialogs.py`), & Top Navigation Bar (`ui/navigation_bar.py`)
- **What Changed**:
  1. **`MobilePanel` Visual Alignment (`ui/mobile_panel.py`)**: Replaced native grey `ttk.Button` Start/Stop controls with Arbor's Vibrant Fern (`#3a7d44`) primary CTA (`▶ Start Mobile Session`) and outlined danger button (`End Mobile Session`), upgraded the panel title to `Lora`, and propagated Dark Mode background/title tokens from `parent_ui`.
  2. **Startup Typography Alignment (`ui/dialogs.py`)**: Upgraded `StartupDialog` headings and paths from legacy `Courier New` / `Segoe UI` to Arbor's canonical `Lora` (title) and `JetBrains Mono` (section headers, paths, wordmark) per `AI_UI_GUIDE.md`.
  3. **1-Click Command Palette Pill (`ui/navigation_bar.py`)**: Added a subtle **`⌘ Commands (Ctrl+K)`** pill in the top navigation bar so both new trainees and power users can discover and launch `Ctrl+K` actions in 1 click.
- **User Impact**: Arbor looks cohesive from the very first launch screen through the Phone Connector and main workspace, with instant 1-click access to Command Palette actions.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Design Tokens verified against `documentation/agent/AI_UI_GUIDE.md`

---

### Entry 26: UI/UX Ergonomics & Clarity Pass (Plain Buttons, Focus Mode Escape Hatch, Friendly Problem Labels, Desktop Field Tooltips & Calm Mobile Setup)
- **Date**: 2026-11-22
- **Feature Area**: Startup Dialog (`ui/dialogs.py`), Top Navigation Bar (`ui/navigation_bar.py`), Registration Form (`ui/registry_panel.py`), Mobile Panel (`ui/mobile_panel.py`), & Mobile V2 (`backend/mobile_template_v2.py`)
- **What Changed**:
  1. **Plain-Language Primary Buttons & Placeholders**: Renamed Startup **`LAUNCH SYSTEM`** → **`Open Collection →`** and **`…`** → **`Browse…`**; renamed Desktop top bar **`Next+Hist`** → **`Next Ledger Match`** with a descriptive tooltip; updated Mobile V2 search placeholder to `"Search object # or plant name..."` and `"Set as Unknown (ICEDIG)..."` → `"Mark as Blank or Unreadable..."`.
  2. **Focus Mode Safety Escape Hatch (`ui/registry_panel.py`)**: Added a 1-click **`Show All Fields`** button directly underneath the Focus Mode empty-state message so new users who accidentally toggle Focus Mode on a clean specimen can restore all fields immediately.
  3. **Human-Friendly Problem Flag Labels & Desktop Field Tooltips**: Formatted raw underscore problem flags (`Box_Label_Problem`, `Collection_Date_Problem`, `PlantPart_Problem`, `Other_problem`) into readable labels (`Box Label Issue`, `Collection Date Issue`, `Plant Part Issue`, `Other Issue`) on Desktop and Mobile V2 while preserving exact Excel column names underneath. Added hover tooltips on `Genus`, `Species`, and `Author` in `ui/registry_panel.py` matching Mobile V2's Field Guide.
  4. **Calmer `MobilePanel` Setup Card (`ui/mobile_panel.py`)**: Collapsed *Tunnel Provider (Cloudflare/Pinggy)* and *Interface Version (V2/V1)* inside a **`▸ Advanced Connection & Version Options`** toggle so the default launch screen stays clean and 1-glance, and wired live PIN warning updates when switching between Public and LAN modes.
- **User Impact**: Both experienced curators and brand-new trainees encounter warm, jargon-free labels, instant tooltips for `Author` vs. `Collector` and `Genus`/`Species` GBIF updates, zero Focus Mode panic, and a streamlined Mobile Companion setup screen.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py` & `tests/test_mobile_companion_offline.py`
  - [x] Master Lexicon compliance

---

### Entry 25: User1 & User2 Independence Pass (Mobile PIN Toggle, Offline Login CSS, "What the Fields Mean" Mirror Guide & Docs Cleanup)
- **Date**: 2026-11-22
- **Feature Area**: Mobile Server Security & Offline Login (`backend/mobile_server.py`), Phone Connector Panel (`ui/mobile_panel.py`), Mobile V2 Field Guide & Walkthrough (`backend/mobile_template_v2.py`), Problem Triage Queue (`ui/object_problem_resolver.py`), & Documentation (`MOBILE_COMPANION_USER_GUIDE.md`, `README.md`, `MAINTAINER_HANDOFF.md`)
- **What Changed**:
  1. **Instant-Load Offline `LOGIN_TEMPLATE` & Security Hardening (`backend/mobile_server.py`)**: Replaced the render-blocking Tailwind CDN script in `LOGIN_TEMPLATE` with self-contained inline CSS so the PIN screen loads instantaneously in concrete vaults, and removed the hardcoded `"43110"` fallback PIN.
  2. **Live PIN Toggle & Direct Save in `MobilePanel` (`ui/mobile_panel.py`)**: Added a live **Require 4-Digit PIN: ON/OFF** toggle directly in both the setup and active session views (persisted to `user_prefs.json` and calling `server.update_pin_requirement()` live), showing an amber warning if Public Tunnel mode is active without a PIN, plus a 1-click **`💾 Save Workbook Now`** button.
  3. **1-Tap "What the Fields Mean" Mirror Guide (`backend/mobile_template_v2.py`)**: Added a `?` button in both the Vault List and Specimen Detail headers opening `#fieldGuideModal`, which mirrors the exact specimen page layout with plain-English explanations for every field—including the tip that outdated/synonym `Genus`/`Species` names can be entered as printed on the box and updated later via desktop **GBIF Name Check**, and clarifying `Author` vs. `Collector`.
  4. **Updated 3-Step Hallway Guide & Unwrapped Reassurance**: Updated Slide 1 to **"Find an Object and Search Its Listed Number"**, added *"it's okay to leave unsolvable problems flagged for someone else later"* reassurance on Slide 3, and removed `truncate` from `#reviewHelperText` so full reassuring text wraps cleanly on narrow phones.
  5. **Desktop & Documentation Cleanup**: Renamed `BATCH_PROBLEM_QUEUE` → `"Problem Triage Queue"`, renamed `"4. ICEDIG Missing Data Standards"` → `"4. Blank or Unreadable Labels (Standard Codes)"` in `MOBILE_COMPANION_USER_GUIDE.md`, corrected `README.md` `"IndexedDB"` → `"localStorage offline queue + Service Worker"`, and added a `"Customizing Collection Columns (config.py)"` guide to `MAINTAINER_HANDOFF.md`.
- **User Impact**: New workers without museum training can work independently in concrete vaults with instant login, a 1-tap plain-English Field Guide matching the exact screen in front of them, live PIN control on private Wi-Fi, and 1-click workbook saving.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Mobile Guide, README & Maintainer Handoff synced
  - [x] Unit Tests: `tests/test_mobile_companion.py` & `tests/test_mobile_companion_offline.py`

---

### Entry 24: Tutorial Engine Polish (Auto-Dodge HUD, Collapsible Details, Accurate Highlights) & Office Triage (`REV+ERR`) Sandbox Tour
- **Date**: 2026-11-21
- **Feature Area**: Interactive Tutorials (`ui/tutorials/tutorial_runner.py`, `ui/tutorials/sandbox_manager.py`, `ui/tutorials/review_tutorial.py`, `ui/tutorials/triage_tutorial.py`, `ui/tutorials/discrepancy_tutorial.py`, `ui/tutorials/database_tutorial.py`, `ui/tutorials/micro_guides.py`), Help Hub (`ui/help_dialogs.py`), Command Palette (`ui/command_palette.py`), & Tests (`tests/test_sandbox_tutorials.py`)
- **What Changed**:
  1. **Tutorial Engine Upgrades (`ui/tutorials/tutorial_runner.py`)**: Added a single-runner guard (preventing overlapping HUDs), smart left/right auto-dodge positioning so the HUD never covers the highlighted target control, precise `reg_field:<FieldName>` target resolution, a collapsible **`▸ 💡 More Details & Excel Impact`** drawer (`ActionStep.details`), standardized badges (`🛡️ PRACTICE SANDBOX` / `⚡ QUICK GUIDE`), and calm `show_toast` completion feedback.
  2. **Fixed Broken & Broad Target Highlights Across All Tutorials**: Fixed `discrepancy_tutorial.py` (`history_btn` → `history_indicator_label`), narrowed `review_tutorial.py` Steps 2–3 to `reg_field:Collection Date` and `problem_flags_frame`, removed misleading `search_entry` highlight in `database_tutorial.py`, added `image_container` highlight in `micro_guides.py`, and wired `sm._active_runner` everywhere.
  3. **New Office Triage (`REV+ERR`) Practice Sandbox Tour (`ui/tutorials/triage_tutorial.py`)**: Added a 4-step sandbox tour with a dedicated `"triage"` mock dataset (`#2001`/`#2002` `[REV+ERR]`, `#2003` clean `[REV]`), wired into the Help Hub and `Ctrl+K` Command Palette.
  4. **Explicit `REV+ERR` Reassurance**: Updated the Quick Tour, Hallway Follow-Up & Armed Shelf guides, and Office Triage Tour to reassure trainees that **you won't always be able to solve every flagged problem right away — and that is completely okay**, since leaving the flag active while marking Reviewed keeps it safely queued for someone else in the future.
- **User Impact**: Tutorials highlight the exact control on screen without blocking it, stay clean and scannable with optional deeper Excel explanations, reassure trainees when problems can't be solved immediately, and now include a dedicated Practice Sandbox for Office Triage (`REV+ERR`).
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Tutorial Developer Guide: `documentation/agent/TUTORIAL_GUIDE.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py`
  - [x] Master Lexicon & Zero-Barcodes compliance

---

### Entry 23: Modular Mobile Template Split (`mobile_template_v1.py` & `mobile_template_v2.py`)
- **Date**: 2026-11-21
- **Feature Area**: Mobile Companion Architecture (`backend/mobile_server.py`, `backend/mobile_template_v1.py`, `backend/mobile_template_v2.py`), Agent/Maintainer Docs (`AGENTS.md`, `MAINTAINER_HANDOFF.md`, `documentation/agent/MOBILE_COMPANION_GUIDE.md`, `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`), & Tests (`tests/test_mobile_companion.py`)
- **What Changed**:
  1. **Extracted Pure-Python Template Modules**: Moved `INDEX_TEMPLATE` (~4,696 lines) verbatim into `backend/mobile_template_v1.py` and `INDEX_TEMPLATE_V2` (~4,580 lines) verbatim into `backend/mobile_template_v2.py` (SHA-256 byte-for-byte identical), shrinking `backend/mobile_server.py` from 12,380 lines down to 3,101 lines of focused Flask backend logic.
  2. **100% Backward-Compatible Re-Exports**: Re-exported `INDEX_TEMPLATE` and `INDEX_TEMPLATE_V2` from `backend/mobile_server.py` so all existing imports, tests, and PyInstaller builds (`collect_submodules('backend')`) work identically with zero external `.html` files or build steps.
  3. **Full Documentation Sync**: Updated `AGENTS.md`, `MAINTAINER_HANDOFF.md`, `documentation/agent/MOBILE_COMPANION_GUIDE.md`, and `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md` to reference the new module locations.
- **User Impact**: Zero runtime change for museum trainees; significantly faster, safer maintenance and cleaner diffs for any future developer or agent working on the Mobile Companion backend or UI.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Agent & Handoff Guides: `AGENTS.md`, `MAINTAINER_HANDOFF.md`, `MOBILE_COMPANION_GUIDE.md`, `MOBILE_AUDIT_WORKFLOW_SPEC.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`
  - [x] Zero-Build & PyInstaller compliance verified

---

### Entry 22: Handoff & Release Hygiene (GitHub Actions CI, Pinned Dependencies, Repo Cleanup & Maintainer Guide)
- **Date**: 2026-11-20
- **Feature Area**: CI/CD (`.github/workflows/ci.yml`), Dependencies (`requirements.txt`, `requirements-dev.txt`), Repo Hygiene (`.gitignore`, removed corrupt pref dumps), & Handoff Docs (`MAINTAINER_HANDOFF.md`, `README.md`)
- **What Changed**:
  1. **Pinned Runtime & Split Dev Dependencies**: Pinned all runtime packages in `requirements.txt` to tested compatible major ranges (preventing silent breakage on major upgrades like `pandas 3.x`) and moved `pytest`, `pytest-xvfb`, `pyinstaller`, and optional `PySide6` into `requirements-dev.txt`.
  2. **GitHub Actions CI & Portable Build Pipeline (`.github/workflows/ci.yml`)**: Added an automated Windows CI workflow that runs the 9-suite core regression tests on every push/PR to `main`, and automatically builds + uploads the verified `Arbor-Windows-Portable` (`dist\`) artifact on `v*` tags or manual dispatch.
  3. **Repository Hygiene**: Removed 3 stray `user_prefs.json.corrupt.20261120_*` files from the root and updated `.gitignore` to ignore `user_prefs.json.*`, `.arbor_backups/`, `.arbor_logs/`, and `*.autosave.json`.
  4. **Maintainer Handoff Guide (`MAINTAINER_HANDOFF.md`) & `README.md` Sync**: Added a concise 1-page handoff guide covering quickstart, active vs. archived folders, non-negotiable offline/zero-build/zero-barcode invariants, and the release checklist; updated `README.md` to Python 3.10+ and linked the handoff and mobile guides.
- **User Impact**: Future maintainers can onboard in minutes, automated CI catches regressions before release, and tagged releases produce verified portable Windows bundles automatically.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Handoff & Root Docs: `MAINTAINER_HANDOFF.md` & `README.md`
  - [x] CI Workflow & Dependency Hygiene verified

---

### Entry 21: Hardened Data-Safety Regression Suite & 13-Inch Laptop DPI / Dark Mode Polish
- **Date**: 2026-11-20
- **Feature Area**: Regression Tests (`tests/test_hardened_data_safety.py`, `tests/test_navigation_and_dialogs.py`) & Secondary Dialog DPI/Dark Mode (`ui/mobile_dialog.py`, `ui/filter_dialog.py`, `ui/object_problem_resolver.py`, `ui/historical_resolver.py`)
- **What Changed**:
  1. **Headless Data-Safety Regression Suite (`tests/test_hardened_data_safety.py`)**: Added 5 dedicated headless tests locking in JSON autosave UTF-8 Norwegian character & `ObjectID` index roundtrip, `AppState._mutation_seq` concurrent-save protection, `undo_last_bulk_edit()` atomic rollback, offline `batch_gbif_match()` `stats_out` error reporting, and non-caching of transient GBIF network errors.
  2. **13-Inch Laptop DPI Scrollability (`ui/mobile_dialog.py`, `ui/filter_dialog.py`, `ui/object_problem_resolver.py`)**: Replaced hardcoded `540x750` / `minsize(500, 700)` and primary-monitor clamping in `MobileDialog` with `utils.center_and_fit_toplevel()`, a scrollable `tk.Canvas` host (with `bind_mousewheel`), and compact `minsize(420, 460)`; relaxed `FilterDialog` `minsize` to `640×480`; and enabled resizing on `ProblemQueueDialog` (`minsize(440, 400)`) so bottom action buttons are never clipped at 125%–150% Windows scaling.
  3. **Secondary Dialog Dark Mode Consistency**: Added Arbor Charcoal & Vibrant Fern Dark Mode palette propagation to `MobileDialog`, `FilterDialog`, `ObjectProblemResolver`, and `HistoricalConflictResolverWindow` while keeping Light Mode palettes 100% unchanged.
- **User Impact**: Trainees on 13-inch laptops at 125%–150% Windows scaling can scroll and reach every button in the Phone Connector, Filter, and Problem Queue dialogs without clipping, and Dark Mode stays visually consistent across secondary curation dialogs.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_hardened_data_safety.py` & `tests/test_navigation_and_dialogs.py`
  - [x] Master Lexicon & AI UI Guide compliance

---

### Entry 20: Office Triage & Conflict Resolution UX (1-Click Clear Flag, Alt+Arrow Queue Nav, Plain-Language Titles)
- **Date**: 2026-11-20
- **Feature Area**: Office Triage & Conflict Resolution (`ui/object_problem_resolver.py`, `ui/historical_resolver.py`, `ui/gbif_review.py`), Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`), & Tests (`tests/test_problem_persistence_fix.py`)
- **What Changed**:
  1. **1-Click "✓ Value is Correct (Clear Flag)" Button (`ui/object_problem_resolver.py`)**: Added a dedicated soft-green confirmation button on every Problem Resolution field card with an active problem flag. Clicking it leaves the specimen's existing value untouched, clears the mapped problem flag(s) in `Observation`, pushes an Undo snapshot (`Ctrl+Z` safe), logs `PROBLEM_CLEARED`, updates the Specimen Directory card, and marks the card resolved.
  2. **Queue Keyboard Navigation (`Alt + ←` / `Alt + →`)**: Bound `<Alt-Left>` and `<Alt-Right>` in `ObjectProblemResolverWindow` when triaging a queue of flagged specimens, with visible shortcut hints on the `← Prev (Alt+←)` and `Next (Alt+→) →` buttons.
  3. **Canonical Trainee Lexicon Cleanup**: Replaced `"Object ... (OID: ...)"` with `"Specimen ... (#...)"` in Problem Resolution, simplified `HistoricalConflictResolverWindow` title/header to **"Historical Ledger Comparison"** (`SPECIMEN REVIEW: N ITEMS TO CHECK`), and simplified `GBIFReviewDialog` title to **"GBIF Name Check & Update Review"**.
- **User Impact**: Curators triaging hallway-flagged `REV+ERR` specimens at their desk can confirm correct values and clear flags in a single Undo-safe click, step through queued specimens with `Alt+Left`/`Alt+Right`, and read calmer, jargon-free dialog headers.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Desk Cheat Sheet: `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`
  - [x] Unit Tests: `tests/test_problem_persistence_fix.py`
  - [x] Master Lexicon compliance

---

### Entry 19: Mobile Companion Offline Concrete-Vault Styling & Batch Location Hallway Ergonomics
- **Date**: 2026-11-20
- **Feature Area**: Mobile Companion (`backend/mobile_server.py`) & Regression Tests (`tests/test_mobile_companion.py`)
- **What Changed**:
  1. **Non-Blocking Tailwind CDN & Instant Offline Render (`INDEX_TEMPLATE` & `INDEX_TEMPLATE_V2`)**: Loaded `cdn.tailwindcss.com` with `defer` and Google Fonts with non-blocking `media="print" onload="this.media='all'"`, eliminating 10–30 second white-screen hangs when a phone connects to a local museum Wi-Fi hotspot with no internet uplink. `<html>` starts with `arbor-offline-css` and automatically removes it in `onload` when Tailwind finishes loading—guaranteeing zero CSS specificity collision online.
  2. **Comprehensive Scoped Offline Fallback CSS (`html.arbor-offline-css`)**: Expanded `#arbor-offline-fallback` in V2 (and core parity in V1) so specimen cards, headers, search bar, Armed Target Shelf banner, segmented tabs, sticky **Mark Reviewed** action bar, Batch Location Registrator, offline banner, toasts, and all modals stay clean, legible, and thumb-friendly with zero internet.
  3. **Batch Location Registrator Hallway Ergonomics (`INDEX_TEMPLATE_V2`)**: Set `#batchIdInput` to `inputmode="numeric"` by default with a 1-tap `123 / ABC` keypad toggle (`toggleBatchInputMode()`), and added a 1-tap **⚡ Use Cab XX · Sh XX** (`#btnBatchCopyArmed` / `copyArmedShelfToBatch()`) button to copy the active Armed Target Shelf into the batch anchor without retyping coordinates.
- **User Impact**: Trainees walking concrete herbarium vaults without internet see the Mobile Companion render instantly with crisp cards, buttons, and modals—and can switch into Batch Location Registrator with a numeric keypad and 1-tap armed shelf coordinates.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_mobile_companion.py`
  - [x] Zero-Barcodes & Zero-Build compliance verified

---

### Entry 18: Standalone Build & Live Smoke-Test Polish (Setup Guide Crash, Chapter Top-Align, Persistent Welcome Card, Multi-Monitor Tutorial)
- **Date**: 2026-11-20
- **Feature Area**: Packaging & Demo Provisioning (`build_exe.bat`, `main.spec`, `scripts/create_demo_dataset.py`, `ui/dialogs.py`), Startup Setup Guide (`ui/dialogs.py`), Unified Guide Reader (`ui/help_dialogs.py`), Demo/First-Run Welcome Card (`ui/database_ops.py`), & Multi-Monitor Dialog/Tutorial Positioning (`utils.py`, `ui/tutorials/tutorial_runner.py`)
- **What Changed**:
  1. **Offline Demo Generator & Writable Frozen Demo Path**: Added a deterministic 220-specimen `Økonomisk Botanisk` fallback generator in `scripts/create_demo_dataset.py` (keeps GitHub lean with no committed `.xlsx`), auto-generated `data/demo_collection.xlsx` in `build_exe.bat` (with optional `--no-pause` flag), and updated `StartupDialog._resolve_writable_demo_path()` so frozen `Arbor.exe` copies the bundled demo to `<exe_dir>\data\demo_collection.xlsx` instead of writing into PyInstaller's temporary `_MEIPASS` directory.
  2. **Fixed Startup "Getting Started & Setup Guide" Crash**: Replaced undefined `self.C_MUTED` references in `StartupDialog._show_setup_help_msg()` with `self.C_ON_VARIANT`.
  3. **Guide Reader Chapter Top-Alignment**: Replaced `txt.see(mark)` with `txt.yview(mark)` (`_scroll_reader_to_top` / `_scroll_to_top`) in `ui/help_dialogs.py` so clicking any chapter in the Left Chapter Sidebar (both Desktop Work Manual and Mobile Vault Guide) or inline anchor link aligns the chapter heading directly to the top of the reading pane.
  4. **Prominent, Persistent Centered Welcome Card**: Replaced the 15-second auto-vanishing first-run toast banner with a large, calm Arbor-styled centered **Welcome to Arbor / 3-Minute Quick Tour** card (`_show_welcome_tour_prompt`) when opening the Demo Project (or on first run). It never auto-vanishes until the user starts the tour or explicitly dismisses it, with an optional *"Don't show this welcome screen again"* checkbox.
  5. **Multi-Monitor Window & Tutorial Positioning**: Updated `utils.center_and_fit_toplevel()`, `TutorialRunner._position_hud()`, and `TutorialHighlight.update_position()` to position relative to the main window using signed Tk geometry (`{x:+d}{y:+d}`) without clamping negative secondary-monitor coordinates to `+0`/`+10`, so tutorials, highlights, and dialogs always stay on the same monitor as the main Arbor window.
- **User Impact**: Standalone `Arbor.exe` launches cleanly with a built-in writable Demo Project, the Startup Setup Guide opens without errors, clicking any manual chapter jumps straight to the top of that section, Demo trainees see a clear persistent Welcome Card in the center of the screen, and multi-monitor workstations keep the interactive tutorial on the active monitor.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_demo_dataset.py`, `tests/test_navigation_and_dialogs.py`, `tests/test_sandbox_tutorials.py`
  - [x] Packaging: `build_exe.bat` & `main.spec`
  - [x] Master Lexicon compliance

---

### Entry 17: Help Hub, Startup Setup Guide, Unified Desktop/Mobile Reader & Documentation Sync
- **Date**: 2026-11-20
- **Feature Area**: Startup Help (`ui/dialogs.py`), Unified Guide Reader & Help Hub (`ui/help_dialogs.py`), Help Dropdown (`ui/main_window.py`), Mobile Panel (`ui/mobile_panel.py`), User Guides (`USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`, `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`), & Packaging (`main.spec`, `build_exe.bat`)
- **What Changed**:
  1. **Startup Window Setup Guide**: Replaced the raw Windows `messagebox.showinfo()` in `StartupDialog` with a calm, Arbor-themed Setup Guide window (Warm Alabaster, Lora/Inter/JetBrains Mono, Vibrant Fern step cards) and expanded the Startup `Help` menu to include **Getting Started & Setup Guide**, **Desktop Work Manual**, **Mobile Vault Guide**, and **Keyboard Shortcuts** (available before opening any workbook or demo).
  2. **Unified Tabbed Guide Reader (`show_main_help`)**: Added a 2-tab pill switcher (**📖 Desktop Work Manual** | **📱 Mobile Vault Guide**), a clickable left-hand **Chapter Sidebar** with Vibrant Fern active highlight, direct chapter jumping (`initial_chapter="dont-panic"`), inline `Find (Ctrl+F)`, and quick links to **Shortcuts (F1)** and **3-Min Practice Tour**.
  3. **Calm Scrollable Help Hub & Consistent `❓ HELP ▾` Menu**: Redesigned `open_help_window()` into a scrollable `640×650` hub with a 2×2 Quick Answer grid (Desktop Manual, Mobile Guide, Shortcuts `F1`, `"Don't Panic!"` Help) plus pill rows for all 3 in-place **30-Second Quick Guides** and 3 **Practice Sandboxes**. Fixed `(F1)` labeling in `show_help_dropdown()`, made `show_shortcuts()` work on bare Tk roots, and added a `📖 Mobile Guide` button directly to `MobilePanel`.
  4. **Guide Content Sync & Zero-Barcodes Compliance**: Removed all remaining barcode references and technical jargon from `MOBILE_COMPANION_USER_GUIDE.md` and rewrote Section 3 around the real V2 Armed Target Shelf & 3-Step Guide workflow; updated `USER_GUIDE.md` and `KEYBOARD_SHORTCUTS_CHEAT_SHEET.md` with Practice Mode, `Ctrl+Alt+K`, `F3`, `Ctrl+Z`, and `Undo Last Bulk Edit`; bundled `MOBILE_COMPANION_USER_GUIDE.md` in `main.spec` and `build_exe.bat`.
- **User Impact**: Whether launching Arbor for the first time, working on a real collection at a desk, or running Mobile Companion in a vault, trainees have calm, consistent, jargon-free help and manuals 1 click away without needing to enter sandbox or demo mode.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Trainee Manuals: `USER_GUIDE.md` & `MOBILE_COMPANION_USER_GUIDE.md`
  - [x] Desk Cheat Sheet: `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`
  - [x] Packaging: `main.spec` & `build_exe.bat`
  - [x] Master Lexicon & Zero-Barcodes compliance

---

### Entry 16: Pre-Phase 3 Stabilization Polish & Tutorial Phase 3 (Contextual 30-Second Micro-Guides)
- **Date**: 2026-11-20
- **Feature Area**: Specimen Directory (`ui/widgets.py`), Bottom Progress Bar (`ui/status_bar.py`), Settings (`ui/unified_settings.py`), Offline GBIF (`backend/gbif.py`, `ui/gbif_batch_config.py`), Bulk Edit (`ui/bulk_edit.py`, `ui/command_palette.py`), & Contextual Micro-Guides (`ui/tutorials/micro_guides.py`, `ui/tutorials/tutorial_runner.py`, `ui/filter_dialog.py`, `ui/mobile_panel.py`, `ui/image_panel.py`)
- **What Changed**:
  1. **High-Contrast `[REV+ERR]` Card Badge**: Restored `#F57C00` ochre-amber background with `#ffffff` text on Specimen Directory `[REV+ERR]` cards in light mode (`#c46200` in dark mode).
  2. **Plain-Language Bottom Progress Bar**: Replaced developer labels (`OBJECT_COUNT:`, `REVIEWED:`, `PROBLEMS:`, `LAST_SAVE:`, `DB_STATUS`, `LOG_VIEWER`) with Canonical Trainee Lexicon labels (`Specimens:`, `Reviewed:`, `Problems:`, `Last Saved:`, `Collection Stats`, `Activity Log`).
  3. **Removed Unused `Strict Input Validation` Toggle**: Cleaned up the dead checkbox from Unified Settings (`disable_tutorials` remains active from Phase 1).
  4. **Offline GBIF Batch Warning**: Added optional `stats_out` error tracking to `batch_gbif_match()` so offline runs display a clear connectivity warning instead of falsely reporting *"All checked taxonomy records are up to date"*.
  5. **Bulk Edit Audit Log & Single-Action Rollback**: Added `BULK_EDIT` audit log entries and `undo_last_bulk_edit()` exposed via Command Palette (`Ctrl+K` → `"Undo Last Bulk Edit"`).
  6. **Contextual 30-Second Micro-Guides (Phase 3)**: Added `use_sandbox=False` support to `TutorialRunner` and created `ui/tutorials/micro_guides.py` with 3 in-place micro-guides (**Hallway Follow-Up 30s**, **1-Tap Armed Shelf 45s**, **Image Zoom & Rotate 20s**), accessible via subtle `[?]` triggers in Filter Dialog, Mobile Companion, Image Viewport HUD, and `Ctrl+K` Command Palette.
  7. **Test Suite GC Hygiene**: Added `autouse=True` `gc.collect()` teardown fixture in `conftest.py` to prevent cross-thread Tk/PIL finalizer aborts on Windows.
- **User Impact**: Trainees see crisp high-contrast amber `[REV+ERR]` badges, plain-language bottom progress indicators, honest offline GBIF feedback, safer bulk edits with 1-click undo, and instant 30-second micro-guides right beside key tools without leaving their open workbook.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_problem_persistence_fix.py`, `tests/test_status_bar.py`, `tests/test_sandbox_tutorials.py`
  - [x] Master Lexicon compliance

---

### Entry 15: Tutorial Phase 2 — Floating Visual Keycap HUD & Mobile Companion 3-Step Hallway Walkthrough
- **Date**: 2026-11-20
- **Feature Area**: Desktop Tutorial HUD (`ui/tutorials/tutorial_runner.py`, `ui/tutorials/review_tutorial.py`) & Mobile Companion V2 (`backend/mobile_server.py`)
- **What Changed**:
  1. **Floating Visual Keycap Pills**: Added `keycaps` support to `ActionStep` and `TutorialRunner` to render high-contrast physical keycap chips (`[ Ctrl ] + [ F ]`, `[ Space ]`, `[ Ctrl ] + [ Enter ]`) inside the tutorial HUD, and optimized `TutorialHighlight.update_position()` to skip redundant geometry calls when coordinates haven't changed.
  2. **Mobile Companion V2 3-Step Hallway Walkthrough**: Added a zero-build, offline-safe 3-slide modal (`walkthroughModal`) to `INDEX_TEMPLATE_V2` covering fast accession search (`001`/`1`), 1-tap Armed Target Shelf stamping, and flagging issues while still tapping **Mark Reviewed**. Tracked via `localStorage` (`arbor_v2_walkthrough_seen`) with a **Skip** button and a **"🎓 3-Step Guide"** replay button inside Mobile Settings.
- **User Impact**: Desktop trainees build keyboard muscle memory via visual keycaps during the Quick Tour, and first-time phone auditors learn the 3 core hallway mechanics in under 20 seconds without needing supervision.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` & `tests/test_mobile_companion.py`
  - [x] Master Lexicon compliance

---

### Entry 14: Tutorial Phase 1 — Zero-Fear Practice Sandbox, Physical Cabinet 21 Quick Tour & First-Run Prompt
- **Date**: 2026-11-20
- **Feature Area**: Interactive Tutorials (`ui/tutorials/sandbox_manager.py`, `ui/tutorials/review_tutorial.py`), Save/Autosave Guards (`ui/database_ops.py`, `ui/autosave_handler.py`), & Help Hub (`ui/help_dialogs.py`)
- **What Changed**:
  1. **Zero-Disk-Write Sandbox Guards**: Blocked `save_session()`, `_write_excel()`, and background `_autosave_tick()` whenever `SandboxManager().is_sandboxed` is `True`, showing a reassuring *"Practice Mode — saving is disabled so real files stay safe"* toast instead of attempting disk writes.
  2. **Persistent Practice Mode Banner**: Mounted a slim top-of-window green banner (`🛡️ PRACTICE MODE — Nothing you do here affects real museum files`) with a 1-click **Exit Practice Mode** button while any sandbox tutorial is active.
  3. **Physical Cabinet 21 Scenario & Real Schema Columns**: Upgraded `SandboxManager._create_mock_datasets()` to use real production columns (`Collection Date`, `Collection Place`, `Building`, `Floor`, `Cabinet`, `Shelf`, `Box_Label_Problem`, `df_obs["Reviewed"]`) with a Cabinet 21 specimen (`#1002`, `2008` vs historical ledger `1998`). Rewrote `start_review_tutorial()` into the 5-step **3-Minute Quick Tour** walking trainees through pulling `#1002`, fixing the year, flagging `Box_Label_Problem`, and marking Reviewed to see the amber `REV + 1 ISSUE` badge.
  4. **First-Run Prompt & Help Hub Hero Card**: Added a prominent **"🎓 Take the 3-Minute Quick Tour (Zero Risk — Practice Sandbox)"** card at the top of the Help Hub and a gentle first-run banner in `_on_startup_ready()` respecting `disable_tutorials` and `quick_tour_seen`.
- **User Impact**: New unsupervised trainees can practice real vault curation workflows with zero fear of damaging museum files and immediately understand why flagged specimens are still marked Reviewed.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Unit Tests: `tests/test_sandbox_tutorials.py` (added banner, schema, and disk-save guard tests)
  - [x] Master Lexicon compliance: Used canonical terms (*"Specimen Directory"*, *"Mark Reviewed"*, *"Practice Mode"*)

---

### Entry 13: Full-Stack Stabilization Sprint (Data Safety, Mobile Live Sync, Desktop Shortcuts & Triage Cohesion)
- **Date**: 2026-11-20
- **Feature Area**: Core Persistence (`models.py`, `ui/autosave_handler.py`, `ui/database_ops.py`, `utils.py`, `config.py`, `main.py`, `backend/updater.py`, `backend/task_queue.py`, `repository.py`), Mobile Companion (`backend/mobile_server.py`, `ui/mobile_panel.py`, `ui/mobile_dialog.py`, `ui/mobile_host_app.py`), Desktop Workspace (`ui/main_window.py`, `ui/widgets.py`, `ui/location_panel.py`, `ui/registry_panel.py`, `ui/image_panel.py`, `ui/keybindings.py`, `ui/status_bar.py`, `ui/object_context_bar.py`), Triage & Search (`backend/search.py`, `backend/filter.py`, `backend/gbif.py`, `ui/command_palette.py`, `ui/object_problem_resolver.py`, `ui/gbif_review.py`, `ui/bulk_edit.py`), Onboarding & Settings (`ui/dialogs.py`, `ui/tutorials/review_tutorial.py`, `ui/unified_settings.py`)
- **What Changed**:
  1. **Data Integrity & Crash Safety**: Fixed JSON autosave recovery dropping `"ObjectID"` index names and UTF-8 encoding (preserving Norwegian characters); prevented the Excel formula sanitizer from quoting valid negative Floor values (`-1`, `-2`) and standalone `-`; closed the async save `dirty = False` race and `UnboundLocalError` on `is_locked`; fixed `--restore-session` post-update startup `NameError` and clean updater exit; added `atexit` flushing and corrupt-file backup for `user_prefs.json`; aligned `MobileHostApp` autosave suffix to `.autosave.xlsx`; guarded `BackgroundWorker` shutdown and `save_sqlite()` schema drift.
  2. **Mobile Companion & Desktop↔Mobile Live Sync**: Fixed `MobilePanel`/`MobileDialog` server wiring so "Push to Phone", live desktop→mobile updates, server reuse, and the "Enable simultaneous edit" checkbox work reliably; restored V2 SSE `batch` event unwrapping (`record_updated`, `push_navigation`, `session_ended`) with exponential-backoff reconnect; added offline vault `tailwind` guards + inline fallback CSS and resilient service worker caching; fixed Armed Target Shelf matching to check `Building` and `Floor` alongside normalized `Cabinet`/`Shelf`; preserved phone problem flags during desktop simultaneous-edit sync.
  3. **Desktop Workspace & Shortcuts**: Restored `Ctrl+Z` undo inside single-line entry fields and Caps Lock-tolerant `Ctrl+R`/`Z`/`Y`; fixed `Ctrl+L`/`F4` Storage Location focus, commit-on-blur, and `Ctrl+Alt+K` preset label; fixed Focus Mode problem fallback, `F3` problem focus, and `Ctrl+Shift+P` Command Palette conflict; made `ImagePanel` thread-safe with stale-404 token guards; published `OBJECT_DATA_CHANGED` so top/bottom status bars stay synchronized.
  4. **Search, Filtering & Hallway Triage**: Fixed `Ctrl+K` → "Filter: Hallway Follow-Up (REV+ERR)" crash (`win=None`); added leading-zero and museum-prefix normalization across desktop search and Command Palette (removing the 1,000-row cap); guarded `Ctrl+A` inside text inputs in Problem Resolver and GBIF Review; allowed clearing verified-correct problem flags and restored `" -> "` provenance log diffs; fixed `not_reviewed_only` filter short-circuit, thread-safe non-error-caching GBIF lookups, GBIF Undo cache invalidation, and `df_lock` protection in Bulk Edit.
  5. **Onboarding, Settings & Canonical Trainee Lexicon**: Fixed `StartupDialog` demo image-mode toggle and graceful offline fallback when no local image folder is picked; fixed Review Tutorial Step 1 auto-skipping by targeting specimen `1002`; wired live PIN toggle updates in Unified Settings; replaced remaining technical jargon in Settings and `ObjectContextBar` with Canonical Trainee Lexicon terms.
- **User Impact**: Trainees and curators get safer Excel saving/recovery, working real-time sync and offline vault rendering on phones, responsive desktop shortcuts (`Ctrl+Z`, `Ctrl+L`, `F3`, `Ctrl+K`), crash-free hallway triage, and smoother first-run onboarding.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Master Lexicon compliance: Updated `ObjectContextBar` badges/tooltips and Settings helper text to Canonical Trainee Lexicon terms.
  - [ ] Optional follow-up: Update `ui/status_bar.py` labels (`OBJECT_COUNT:` → `Specimens:`) together with `tests/test_status_bar.py`, and remove or wire the two unused settings toggles (`disable_tutorials`, `strict_input_validation`).

---

### Entry 12: Mobile Review Safeguard Restoration, Hallway Triage Command Palette, Tutorial & Help Viewer Upgrades
- **Date**: 2026-11-20
- **Feature Area**: Mobile Companion (`backend/mobile_server.py`), Desktop Triage (`ui/command_palette.py`, `ui/object_problem_resolver.py`, `ui/mobile_dialog.py`), Interactive Tutorials (`ui/tutorials/`), & Help Center (`ui/help_dialogs.py`)
- **What Changed**:
  1. **Mobile V2 JS Syntax Fix & Non-Coercive Review Guard**: Removed an orphaned closing brace in `INDEX_TEMPLATE_V2` (`handleReviewButtonClick`) and restored the conditional non-coercive prompt (`armedConfirmModal`) when marking an unplaced or differently located specimen as reviewed while a target shelf is armed.
  2. **Dynamic Mobile Building & Collection Labels**: Populated `#launchBldgSelect` dynamically from the active workbook's Storage Location choices instead of hardcoded building names, replaced the hardcoded `vascular_plants.csv` subtitle in Batch Location Registrator, and added a `"📍 Set Target Shelf"` re-open button when dismissing the station setup card.
  3. **Desktop Hallway Triage Shortcuts**: Added **"Filter: Hallway Follow-Up (REV+ERR)"** and **"Triage Problem Queue (Filtered List)"** to the Command Palette (`Ctrl+K`), bound `Escape` to close the Problem Resolution window, and added a post-mobile-sync toast showing how many `REV+ERR` specimens are ready for desktop follow-up.
  4. **Interactive Tutorial Fixes & Styling**: Fixed `review_tutorial.py` validators to read `app.current_object_id` and `df_obs["Reviewed"]` so steps auto-advance reliably, and aligned `TutorialRunner` and `TutorialHighlight` with Arbor's Charcoal & Vibrant Fern design tokens with a step progress bar.
  5. **User Guide & Shortcuts HUD Upgrades**: Fixed Dark Mode propagation into `show_main_help(ui)`, upgraded the in-app manual reader (`_render_markdown_to_text`) with styled callout blocks (`>`), clickable Table of Contents jump links, cleaner tables, and an inline **Find in Guide** (`Ctrl+F`) search bar, plus mousewheel scrolling in the Shortcuts HUD.
- **User Impact**: Trainees using the Mobile Companion get reliable 1-tap Armed Target Shelf protection without accidental blank-location reviews; collection managers can jump straight into `REV+ERR` triage from `Ctrl+K`; and new interns reading the manual or running sandbox tutorials get working auto-advance steps, Dark Mode support, clickable chapters, and instant keyword search.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Trainee Manual: `USER_GUIDE.md` (`Ctrl+G` filter shortcut alignment)
  - [x] Desk Cheat Sheet: `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md` (`Ctrl+G` vs `Ctrl+Shift+F`)
  - [x] Master Lexicon compliance: Used canonical terms (*"Specimen Directory"*, *"Storage Location"*, *"Mark Reviewed"*)

---

### Entry 8: PyInstaller Windowed Standalone Executable Launch Fix & Build Pipeline Hardening
- **Date**: 2026-11-20
- **Feature Area**: Standalone Executable Build Pipeline & Logging Infrastructure (`build_exe.bat`, `main.spec`, `main.py`, `utils.py`, `ui/dialogs.py`)
- **What Changed**:
  1. **Loguru Windowed `sys.stdout` Guard**: Fixed startup crash (`TypeError: Cannot log to objects of type 'NoneType'`) occurring when running `Arbor.exe` built with PyInstaller `console=False`. In windowed GUI mode without a console, Windows sets `sys.stdout` to `None`. In [utils.py](file:///c:/Users/ijbrekke/Documents/arbor/utils.py), `logger.add(sys.stdout)` is now safely guarded so it only attaches when stdout exists, while preserving full disk logging to `.arbor_logs/`.
  2. **Top-Level Stream Sanitization**: Moved stdout/stderr fallback initialization to the very top of [main.py](file:///c:/Users/ijbrekke/Documents/arbor/main.py) before any package imports execute.
  3. **Build Pipeline Hardening**: Updated [build_exe.bat](file:///c:/Users/ijbrekke/Documents/arbor/build_exe.bat) to detect and warn if an existing `dist\Arbor.exe` is currently locked by a running instance, and automatically copies `data\demo_collection.xlsx` to `dist\data\` so trainees launching the standalone executable can test the demo collection immediately.
  4. **Spec Asset Bundling**: Added `data/demo_collection.xlsx` and `requests` to [main.spec](file:///c:/Users/ijbrekke/Documents/arbor/main.spec) and updated [ui/dialogs.py](file:///c:/Users/ijbrekke/Documents/arbor/ui/dialogs.py) to resolve demo paths via `utils.get_resource_path()`.
- **User Impact**: Double-clicking `Arbor.exe` launches cleanly on Windows without crashing on startup, and trainees can immediately click "Load Demo Project" from the startup dialog.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Master Lexicon compliance

---

### Entry 7: Armed Target Shelf Pattern, Non-Coercive Review, Pixel Verification, and Hallway Follow-Up Filter Preset
- **Date**: 2026-11-20
- **Feature Area**: Mobile Companion Curation & Desktop Filter Integration (`backend/mobile_server.py`, `ui/image_panel.py`, `ui/filter_dialog.py`)
- **What Changed**:
  1. **Armed Target Shelf Pattern with Non-Coercive Confirmation**: Interns auditing consecutive specimens in a glass cabinet can arm an active target shelf (e.g. Cabinet 21, Shelf 01) and stamp it with 1 tap. Tapping "Mark Reviewed" on an unplaced specimen prompts: *"Stamp to Armed Shelf 21 & Mark Reviewed?"* with two safe choices: *"Yes, Stamp & Review"* or *"No, Keep Location & Review"*. If the trainee chooses "No", all edits and review status are saved without altering coordinates. Fixed the render-cycle cache bug that previously mutated `state.lastSavedLocation`.
  2. **Leading-Zero & Museum Prefix Normalization**: Auditing searches now automatically normalize leading zeroes (e.g. searching `'001'` matches `'1'`), strip museum accession prefixes, and match against `"Object Number"` and accession columns.
  3. **True Client-Side Pixel Verification & Graceful Folio Collapse**: Both the mobile companion and desktop image panel now verify decoded pixel dimensions (`>= 50x50`) to reject 1x1 tracking pixels, stub placeholders, or HTML error pages from museum webservers. If no valid image is verified, the mobile folio collapses from 192px to a compact 28px single-line bar, reclaiming screen viewport for data fields. Prioritized registered `Online photo 1..3` links from `df_reg` over synthetic pattern guessing.
  4. **Tri-State Status Badges**: Added `REV + [N] ISSUES` (Amber) badge alongside `UNREVIEWED` and `REVIEWED` to reassure interns that flagged physical or botanical issues are safely queued for desktop office triage.
  5. **Desktop 1-Click "Hallway Follow-Up (REV+ERR)" Preset**: Added a dedicated 1-click filter button in the Filter Objects dialog (`ui/filter_dialog.py`) allowing collection assistants back at their desk to isolate specimens reviewed in the vault that have unresolved problems (`Reviewed = Has` and `Any_Problem = Has`).
- **User Impact**: Trainees walking physical herbarium vaults enjoy fast, safe, error-free auditing without risking accidental location corruption. Trainees never lose viewport space to empty image frames, and collection assistants returning to desktop workstations can filter and resolve hallway-flagged issues with a single click.
- **Documentation Sync Checklist**:
  - [x] Change Journal: `documentation/CHANGE_JOURNAL.md`
  - [x] Agent Operational Blueprint: `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`
  - [x] Master Lexicon compliance: Used canonical terms (*"Storage Location"*, *"Mark Reviewed"*, *"Specimen Directory"*)

---

### Entry 4: Mobile Companion Ground-Truth Hallway Audit Specification & Armed Shelf Pattern
- **Date**: 2026-11-20
- **Feature Area**: Mobile Companion UX & Defensive Location Stamping Architecture (`documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`, `backend/mobile_server.py`)
- **What Changed**: Conducted end-to-end ground-truth audit simulation using `data/demo_collection.xlsx`. Established the **"Armed Target Shelf" defensive design pattern** in `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md` to prevent accidental location overwriting when interns mistype accession numbers. Defined specifications for numeric keypad default, above-the-fold location stamping, and tri-state review badges (`[ UNREV ]`, `[ REV ]`, `[ REV+ERR ]`).
- **User Impact**: Trainees walking physical herbarium vaults will have single-tap target shelf stamping without fear of accidentally overwriting records if they mistype an accession number. When marking a damaged or botanically uncertain specimen as "Reviewed", reassuring micro-copy clarifies that location verification is complete and problems are safely preserved for desktop curation.
- **Documentation Sync Checklist**:
  - [x] Agent Operational Blueprint: `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`
  - [x] Mobile Companion Guide: `documentation/agent/MOBILE_COMPANION_GUIDE.md`
  - [x] Master Agent Router: `AGENTS.md`
  - [x] Master Documentation Map Canonical Lexicon adherence

---

### Entry 1: Startup Column Sashes & Proportional Auto-Layout
- **Date**: 2026-11-13
- **Feature Area**: Workspace Layout & Panel Sizing (`ui/main_window.py`, `ui/layout_settings.py`)
- **What Changed**: Implemented `apply_proper_sash_positions()` and smooth 120ms animated transitions for the 3-column workspace. Arbor now dynamically measures the user's screen resolution and positions the Specimen Directory (left column), Image Viewport (middle column), and Registration Form (right column) in balanced proportions on startup, while remembering user manual drags between sessions.
- **User Impact**: When trainees launch Arbor or toggle the sidebar (`Ctrl+O` or `F6`), the screen opens with clean, readable panel widths instead of cramped columns, and the image viewer never collapses into an invisible sliver.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Touchpoint Matrix
  - [x] Trainee Manual (`USER_GUIDE.md`) Chapter 2: The Three Main Screen Areas
  - [x] Desk Cheat Sheet (`KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`) Panel Controls
  - [x] In-App Help Center (`ui/help_dialogs.py`) Panel Layout HUD

---

### Entry 2: Single-Badge Discipline for Specimen Directory Cards
- **Date**: 2026-11-13
- **Feature Area**: Specimen Directory & Visual Status Hierarchy (`ui/widgets.py`, `ui/unified_settings.py`)
- **What Changed**: Streamlined the card status display using `_resolve_card_badge_display()` to enforce a strict **single-badge discipline**. Each card now displays at most **one** high-contrast priority badge (`[ TAX ]`, `[ PROV ]`, `[ BOX ]`, `[ IMG ]`, `[ CFCT ]`, `[ REV+ERR ]`, `[ REV ]`, `[ UNREV ]`), ranked according to the active workflow priority preset (`default`, `taxonomist`, or `collections_manager`).
- **User Impact**: Trainees are never confused by a crowded row of multi-colored flags on a single card. A glance at the directory immediately highlights the single most important action required for each specimen.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Canonical Badge Reference
  - [x] Trainee Manual (`USER_GUIDE.md`) Chapter 4: What the Status Badges Mean
  - [x] Desk Cheat Sheet (`KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`): Badge Color Legend with Excel Columns
  - [x] Dual-Perspective Excel Bridge: Mapped each badge to its `Observation` sheet column

---

### Entry 3: Non-Blocking GBIF Toast Alerts
- **Date**: 2026-11-13
- **Feature Area**: Online Taxonomic Verification & Notifications (`ui/toast.py`, `ui/gbif_review.py`, `ui/main_window.py`)
- **What Changed**: Replaced disruptive modal alert popups during GBIF taxonomic checks with sleek, non-blocking floating toast notifications (`ToastManager`). Toasts appear anchored at the top/bottom for 2.5 seconds with clear status icons (`✓ Valid exact match`, `ℹ Fuzzy match found`, `⚠️ Genus required`, `❌ Connection error`).
- **User Impact**: Trainees can verify plant names rapidly without having to repeatedly press Enter or click "OK" on modal popups. If the internet drops out or a name is not found, a soft alert appears without interrupting active typing.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Touchpoint Matrix Feature 7
  - [x] Trainee Manual (`USER_GUIDE.md`) Chapter 4 & 6: GBIF Verification Workflow
  - [x] Desk Cheat Sheet (`KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`) Search & Verification

---

### Entry 4: Directory Card Layout Profiles & Interactive Live Preview
- **Date**: 2026-11-13
- **Feature Area**: Appearance Settings & Card Density (`ui/unified_settings.py`, `ui/command_palette.py`)
- **What Changed**: Added 4 one-click card layout profiles (`Standard` at 78px, `Compact` at 64px, `Full Details` at 92px, and `Minimalist`) selectable via Appearance Settings or Command Palette (`Ctrl+K`). Unified Settings now includes an interactive real-time card preview widget that renders exactly how cards will look before applying changes.
- **User Impact**: Trainees working on small 13-inch museum laptops can switch to "Compact" to see 15+ specimens at once without scrolling, while taxonomists working on wide monitors can choose "Full Details" to view botanical author citations and complete storage locations.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Layout Profiles Section
  - [x] Trainee Manual (`USER_GUIDE.md`) Chapter 7: Changing the View (4 Card Profiles)
  - [x] Desk Cheat Sheet (`KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`): Card View Controls
  - [x] Command Palette Hints: Card View actions (`Standard`, `Compact`, `Full Details`, `Minimalist`)

---

### Entry 5: Non-Destructive Trackpad Zoom & Smooth Mousewheel Navigation
- **Date**: 2026-11-13
- **Feature Area**: Specimen Image Viewport & Canvases (`ui/scroll_helper.py`, `ui/image_panel.py`, `ui/image_popup.py`)
- **What Changed**: Centralized all scroll and zoom routing through `ui/scroll_helper.py` (`bind_mousewheel`), preventing event conflicts between the outer window and inner image viewport. High-resolution specimen scans now support smooth pinch/scroll zooming (`Ctrl+Mousewheel` or `+`/`-` buttons) and direct click-and-drag panning.
- **User Impact**: Trainees inspecting fine details on specimen labels (such as faded pencil handwriting or tiny pressed flowers) can zoom in and out smoothly using their laptop trackpad or mouse wheel without the whole window accidentally scrolling away.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Touchpoint Matrix Feature 2
  - [x] Trainee Manual (`USER_GUIDE.md`) Chapter 8: Working with Specimen Photos
  - [x] Desk Cheat Sheet (`KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`): Photo Zoom & Rotation Gestures

---

### Entry 6: Trainee Work Manual & Printable Desk Cheat Sheet Release
- **Date**: 2026-11-13
- **Feature Area**: Full Documentation Suite Synchronization (`USER_GUIDE.md`, `documentation/curator/`)
- **What Changed**: Fully authored the comprehensive 10-chapter Trainee Work Manual (`CURATOR_USER_GUIDE.md` and `USER_GUIDE.md`) and the single-page printable Desk Cheat Sheet (`KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`). Strictly implemented the Dual-Perspective Excel Bridge rule across all chapters, dynamically aligned all status badge codes with `ui/widgets.py`, and completely removed barcode scanning references.
- **User Impact**: Trainees, interns, and museum assistants have a warm, zero-jargon handbook walking them through daily curation, explaining the exact Excel columns affected by every button, and providing a glanceable keycap cheat sheet beside their monitors.
- **Documentation Sync Checklist**:
  - [x] Trainee Manual (`documentation/curator/CURATOR_USER_GUIDE.md`)
  - [x] Root User Guide (`USER_GUIDE.md`)
  - [x] Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`)
  - [x] Master Documentation Map (`documentation/MASTER_DOCUMENTATION_MAP.md`)

---

### Entry 7: In-App User Assistance Hub & Dynamic Shortcuts HUD
- **Date**: 2026-11-13
- **Feature Area**: In-App User Assistance Hub & Dynamic Shortcuts HUD (`ui/help_dialogs.py`, `ui/unified_settings.py`, `ui/keybindings.py`, `ui/main_window.py`)
- **What Changed**: Upgraded `ui/help_dialogs.py` into a central 4-tile assistance hub (`open_help_window`), dynamic `show_about` displaying `config.APP_VERSION` and Tkinter runtime, and dynamic searchable `show_shortcuts` HUD populated directly from `CANONICAL_SHORTCUTS` in `ui/keybindings.py` displaying visual keycaps and Excel column impacts. Embedded markdown reader now provides a chapter jump dropdown. Rewrote all `SETTING_INFO_TEXTS` in `ui/unified_settings.py` into the Dual-Depth Learning Format (trainee explanation + Excel impact). Wired `F1` globally to launch the Help Hub seamlessly.
- **Trainee Impact**: Instant in-app access to manual, shortcuts, tutorials, and Excel translation bridge directly from the UI or by pressing `F1`, without leaving the desktop workspace or opening external browser windows.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Tier 1-3 update
  - [x] Trainee Work Manual (`USER_GUIDE.md`) Chapter 6 & 7
  - [x] Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`)
  - [x] Zero barcode references verified across all dialogs and tooltips
  - [x] Test suite updated in `tests/test_navigation_and_dialogs.py`

---

### Entry 8: Excel Data Engine, Safety & Atomic Save Hardening
- **Date**: 2026-11-13
- **Feature Area**: Excel Data Engine, Atomic File Persistence & Shortcuts HUD (`repository.py`, `utils.py`, `backend/data_store.py`, `ui/database_ops.py`, `ui/autosave_handler.py`, `ui/help_dialogs.py`, `ui/keybindings.py`)
- **What Changed**:
  1. **Atomic Save Pipeline**: Sibling temporary file writing (`filename.xlsx.tmp_xxxx`) followed by `os.replace` ensures destination workbooks are never corrupted if a crash or write error occurs midway. Orphan temporary files are cleanly removed in all failure branches.
  2. **Pre-Save Automatic Backups**: Implemented `create_presave_backup` which snapshots the active workbook to `.arbor_backups/` capped at a rolling limit of 5 copies prior to atomic replacement.
  3. **Excel Lock & PermissionError Detection**: Defined `ExcelFileLockedError` with transient lock retry loops. If desktop Microsoft Excel holds a Windows file lock on the `.xlsx` file, Arbor catches the error gracefully and surfaces a friendly dialog (*"The Excel file '[Filename]' is currently open in Microsoft Excel or another program. Please close Excel and click 'Retry Save'."*) with immediate "Retry Save" and "Save a Copy" options so trainee work is never lost.
  4. **Data Type Preservation**: Preserves string accession numbers and ObjectIDs with leading zeros (e.g., `"000142"`) across pandas/openpyxl read-write cycles using `dtype=str`. Boolean flags (`Reviewed = TRUE / FALSE`) and ISO timestamps are strictly preserved.
  5. **Dynamic Shortcuts HUD Alignment**: Synchronized `CANONICAL_SHORTCUTS` in `ui/keybindings.py` and `show_shortcuts` in `ui/help_dialogs.py` to match `documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`. Formatted keys with visual keycaps (`[ CTRL ] + [ ENTER ]`, `[ SPACE ]`, `[ CTRL ] + [ S ]`, `[ CTRL ] + [ K ]`, `[ CTRL ] + [ F ]`, `[ CTRL ] + [ G ]`, `[ CTRL ] + [ 0 ]`, `[ F1 ]`) and ensured `Space` is explicitly documented as Toggle Problem Checkbox, never Mark Reviewed.
- **Trainee Impact**: Trainees will never lose museum collection edits or corrupt the primary `.xlsx` workbook if Excel is left open on the desktop or if power is suddenly interrupted. If a workbook is locked by Excel, a clear, friendly prompt explains exactly what to do and allows retrying or saving a copy.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Data Persistence & Safety
  - [x] Trainee Work Manual (`USER_GUIDE.md`) Chapter 5: Saving Your Work Safely
  - [x] Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`) Don't Panic Safety Tip & Primary Work Keys
  - [x] In-App Shortcuts HUD (`ui/help_dialogs.py` & `ui/keybindings.py`)
  - [x] Zero barcode references verified across all dialogs and tooltips
  - [x] Test suite updated in `tests/test_repository.py`

---

### Entry 9: Specimen Image Inspection Canvas, Zoom Ergonomics & Async Pre-Caching
- **Date**: 2026-11-13
- **Feature Area**: Specimen Image Viewport, Async Pre-Caching & Zoom Ergonomics (`ui/image_panel.py`, `ui/image_handler.py`, `ui/image_toolbar.py`, `ui/image_popup.py`)
- **What Changed**:
  1. **Asynchronous Adjacent Image Pre-Caching (`ui/image_handler.py`)**: Implemented `ImagePreCacher` backed by `cachetools.LRUCache(maxsize=10)` to asynchronously pre-load and pre-decode adjacent ($N-1$ and $N+1$) specimen scans in a background thread. Eliminates disk read and JPEG/TIFF decompression lag on the Tkinter UI thread during rapid sequential review.
  2. **High-Quality Zoom Ergonomics & Safe Presets (`ui/image_panel.py` & `ui/image_toolbar.py`)**:
     - `Ctrl + 1`: Fit Whole Sheet to Window (entire herbarium scan visible).
     - `Ctrl + 2`: Fit to Width (sheet fills viewport width, optimal for reading bottom botanical labels).
     - `Ctrl + 3`: 100% 1:1 Pixel Inspection (unscaled native resolution for examining fine botanical hairs, seeds, and veins).
     - Kept `Ctrl + 0` as existing reset view with zero shortcut conflicts with `ui/keybindings.py`.
     - Resampling Optimization: Uses `Image.Resampling.LANCZOS` for crisp resting renders and fast `NEAREST` during live drag-panning for 60 FPS fluidity.
  3. **Corrupted & Missing Image Resilience**: If a photo path listed in the Excel sheet is missing from disk, unreadable, or corrupted, Arbor renders an attractive visual placeholder canvas with an explanatory badge: *"Image not found on disk: [filename]"* or *"Corrupted image file: [filename]"*, preventing any Tkinter crash or unhandled `FileNotFoundError` / `PIL.UnidentifiedImageError`.
  4. **Image Toolbar Updates (`ui/image_toolbar.py`)**: Integrated `Fit Width` (`Ctrl+2`) and `100%` (`Ctrl+3`) buttons alongside existing zoom, rotate, and reset controls with full Light and Dark theme token support.
- **Trainee Impact**: Specimen review is instantaneous when pressing Left/Right arrow keys with zero decompression stutter. Interns and trainees can instantly jump to reading the label with `Ctrl+2` or inspecting fine microscopic plant structures at 1:1 resolution with `Ctrl+3`. If files are missing from storage, an informative placeholder explains the situation without interrupting work.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Specimen Photos & View Controls
  - [x] Trainee Work Manual (`USER_GUIDE.md`) Chapter 8: Working with Specimen Photos
  - [x] Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`) Photo Zoom & Rotation Gestures
  - [x] In-App Image Toolbar Tooltips & Status Badges
  - [x] Test suite updated in `tests/test_image_display.py` and `tests/test_navigation_and_dialogs.py`

---

### Entry 9: Mobile Companion Auditing & Offline Vault Sync
- **Date**: 2026-11-13
- **Feature Area**: Mobile Companion Auditing, Offline Sync, & Desktop Pairing (`backend/mobile_server.py`, `backend/mobile_schemas.py`, `ui/mobile_dialog.py`, `ui/mobile_panel.py`)
- **What Changed**:
  1. **Storage Location Vault Filtering**: Added quick Cabinet and Shelf dropdown selectors directly above the mobile specimen list in both V1 and V2, allowing trainees to filter expected physical sheets by cabinet and shelf.
  2. **Status Badge Discipline**: Standardized visual status badges on mobile cards to clearly display `Reviewed`, `Pending`, and `Taxon Issue`.
  3. **Prominent Mark Reviewed & Problem Flagging**: Added sticky one-tap "Mark Reviewed" button and "Flag Issue" modal in the mobile detail view. Trainees can quickly flag damaged physical sheets or misplaced specimens with custom problem notes, updating observation flags and writing to the audit log.
  4. **Offline-Resilient localStorage Change Queue**: In spotty vault Wi-Fi, pending mobile updates are automatically stored in browser `localStorage` (`arbor_offline_queue`). When connection resumes, edits flush to workstation via `/api/batch_update` without dropping data.
  5. **Desktop Pairing & Zero-Barcode Guarantee**: Desktop pairing dialog clearly displays local Wi-Fi IP and clean QR code for camera pairing. Strictly removed all barcode terms across mobile templates and server routes.
- **Trainee Impact**: Interns and trainees walking through physical collection vaults with a smartphone or tablet can filter sheets by cabinet/shelf, check physical sheets, tap "Mark Reviewed", and flag damage without fear of losing data when Wi-Fi drops out.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`)
  - [x] Trainee Work Manual (`USER_GUIDE.md`) Chapter 9: Mobile Auditing & Companion Workflow
  - [x] Mobile Companion Guide (`documentation/agent/MOBILE_COMPANION_GUIDE.md`)
  - [x] Test suite updated in `tests/test_mobile_companion.py`

---

### Entry 10: Critical UI/UX Design Token Standardization, Responsive Sashes & Modal Shielding
- **Date**: 2026-11-20
- **Feature Area**: Design System, Workspace Responsiveness, Form Polish & Trainee Ergonomics (`ui/main_window.py`, `ui/widgets.py`, `ui/registry_panel.py`, `ui/location_panel.py`, `ui/historical_resolver.py`, `ui/filter_dialog.py`, `ui/bulk_edit.py`, `ui/navigation_bar.py`, `ui/new_database_wizard.py`)
- **What Changed**:
  1. **Typography & Font Stack Normalization**: Eradicated fragmented `"Hanken Grotesk"` across 20+ modules, aligning the entire desktop UI with canonical `"Inter"` for systematic sans body text, `"Lora"` for scholarly botanical titles, and `"JetBrains Mono"` for tabular numeric fields (`Collection Date`, `Innsammling Nr.`, geographic coordinates).
  2. **Responsive Window Sash Positioning**: Added a debounced `<Configure>` listener to `panes` in `ui/main_window.py`. The center inspection canvas now dynamically maintains $\ge 480\text{ px}$ of breathing room on standard $1366\times768$ and compact workstation screens without squeezing out specimen details.
  3. **High-Contrast Form Field Focus**: Updated entry field highlight rings in `ui/registry_panel.py` from invisible pale `#f2f5f1` to high-contrast Vibrant Fern `#3a7d44`, providing clear cursor feedback when tabbing between fields. Replaced Bootstrap pastels with canonical Material 3 container tokens (`#ffdad6`, `#fef9e7`, `#e9f0f5`).
  4. **Call-to-Action Hierarchy Consolidation**: Eliminated the redundant secondary review button in the image panel footer, elevating the right audit rail's `✓ MARK AS REVIEWED` button as the single dominant CTA. Visually guarded destructive batch actions in `ui/bulk_edit.py` and `ui/autosave_handler.py` with `#ba1a1a` error tokens.
  5. **Modal Dialog Keyboard & Error Shielding**: Added `<Escape>` key closure and a visible "Close" button to `HistoricalConflictResolverWindow`. Shielded deferred canvas mousewheel bindings in `ui/filter_dialog.py` to prevent `_tkinter.TclError: bad window path name` on rapid dismissal.
  6. **Trainee Lexicon Cleanup**: Replaced all developer database jargon (`"schema"`, `"primary key"`, `"relational join"`) across new database wizards and dialogs with plain English trainee terms (*"Field Profile"*, *"Unique Specimen ID"*, *"Linked Records"*).
- **Trainee Impact**: Trainees working on laptops and desktop workstations experience crisp, readable typography with aligned dates, a center image canvas that never gets crushed on resize, clear green outlines showing which box is currently typed into, and safe dialogs that close reliably with `Escape` without errors.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`) Canonical Trainee Lexicon
  - [x] Trainee Work Manual (`USER_GUIDE.md`) Chapter 2 & 4: Interface Navigation & Form Editing
  - [x] Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`)
  - [x] Single-Badge Discipline and Design Token compliance verified against `documentation/agent/AI_UI_GUIDE.md`

---

### Entry 11: Ground-Truth Mobile Vault Audit Workflow, Armed Target Shelf & Relocation Guard
- **Date**: 2026-11-20
- **Feature Area**: Mobile Companion Ground-Truth Hallway Auditing, Armed Target Shelf, Ergonomics & Offline Service Worker (`backend/mobile_server.py`, `documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`)
- **What Changed**:
  1. **In-Vault Audit Station Launchpad (`#auditStationLaunchpad`)**: Added a collapsible audit station setup card and compact active station pill above the search bar in `#listView`. Trainees walking to a physical glass case can set Building, Cabinet, and Shelf once.
  2. **Armed Target Shelf & One-Tap Stamping**: Opening any specimen card displays the armed target shelf in the detail header. Unrecorded specimens feature a one-tap `[ ⚡ Stamp Target (Cab XX) ]` button that populates Building, Floor, Cabinet, and Shelf in one tap.
  3. **Defensive Relocation Guard & 5-Second Undo Toast**: Protected against accidental location overwrites when trainees mistype accession numbers. If a specimen already has coordinates registered in a different cabinet, the stamp CTA clearly warns `[ ⚠️ Relocate to Cab XX ]`, updates the record immediately, and displays a prominent 5-second animated `[ ↩ Undo ]` toast to restore original coordinates if accidental.
  4. **Non-Blocking Review Flow & Reassurance Micro-Copy**: Removed interrupting confirmation modals from the "Mark Reviewed" button (`handleReviewButtonClick`). Added dynamic reassurance helper copy under the review button (`"✓ Location recorded. Issues flagged for desktop curation."`) confirming that marking reviewed records the physical verification while preserving flagged issues for curator research.
  5. **Dynamic Location Tab Status Badge**: Added `#tabLocationBadge` on the Location tab header indicating current status (`Cab 21` in green when validated, or `Unset ⚠️` in amber when missing coordinates).
  6. **Vault Service Worker Caching & Login V2 Redirect**: Added `/v2` to `/service-worker.js` asset precache with Stale-While-Revalidate caching for seamless offline usage in shielded concrete herbarium vaults. Fixed `/login` to route trainees directly to `/v2`.
  7. **Tactile Haptic Feedback**: Added `save_success` haptic profile triggered on server sync, and wired `discrepancy` haptics into problem flag toggles.
- **Trainee Impact**: Trainees standing in dim physical collection vaults with a specimen in hand can search accession numbers, stamp entire cabinets of specimens in 1 tap without retyping, safely undo accidental relocations, flag damaged boxes without losing their place, and mark physical verification without modal interruptions.
- **Documentation Sync Checklist**:
  - [x] Master Documentation Map (`MASTER_DOCUMENTATION_MAP.md`)
  - [x] Ground-Truth Workflow Spec (`documentation/agent/MOBILE_AUDIT_WORKFLOW_SPEC.md`)
  - [x] Mobile Companion Guide (`documentation/agent/MOBILE_COMPANION_GUIDE.md`)
  - [x] Verification simulation passed with 100% success in `scratch/simulate_vault_audit.py`
  - [x] Full test suite verified in `tests/test_mobile_companion.py`


---

### Entry 73: Desktop & Mobile Quick Reference Sheet + User Manuals Sync
- **Date**: 2026-11-25
- **Area**: Help Center (`ui/unified_help.py`), Mobile Companion V2 Field Guide (`backend/mobile_template_v2.py`), User Manuals (`USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`), Tests (`tests/test_navigation_and_dialogs.py`)
- **Code Delta**:
  - Added a dedicated **`Badges & Reference`** tab (`reference`) to the Desktop Help Center (`ui/unified_help.py`) explaining all 12 status badges (`REV+ERR`, `REV+NOTE`, `REV`, `TAX`, `PROV`, `BOX`, `IMG`, `ERR+HIS`, `CFCT`, `ERR`, `NOTE`, `UNREV`) with exact color tokens, card chips (`LOAN` / `↗ Loaned`, `UKN`, `UNVAL`, `NO PHOTO`, `● Unsaved`, yellow field highlight), the **3-Way Problem Rule**, all 4 **ICEDIG** codes + guardrails, and everyday conventions (`DD.MM.YYYY` dates, `Author` vs. `Collector`, Physical-Inspection Rule, `📜 Old names`, and Desktop ↔ Mobile tabs).
  - Updated Mobile Companion V2's `?` Field Guide modal (`openFieldGuideModal()` & `FIELD_GUIDE_EXPLANATIONS` in `backend/mobile_template_v2.py`) to align 1:1 with Desktop: replaced stale `Details`/`History` wording with `Data`/`Problems`, added `[REV+NOTE]`/`[NOTE]` and a Desktop-only unreviewed badge summary (`[TAX]`, `[PROV]`, `[BOX]`, `[IMG]`, `[ERR+HIS]`, `[ERR]`, `UKN`, `UNVAL`), added the **3-Way Problem Rule & ICEDIG Codes** card, and added a **3 Tabs & Everyday Rules** summary.
  - Audited and updated both `USER_GUIDE.md` and `MOBILE_COMPANION_USER_GUIDE.md`: fixed the swapped Center/Right column diagram in `USER_GUIDE.md` Chapter 2 (Center = Photos + Storage Location below; Right = Registration Data + Problems + `✓ MARK AS REVIEWED`), updated the welcome callout to the 2-Part Core Introduction + Optional & Advanced Tutorials, documented per-field `⋯` ICEDIG buttons, manual problem-flag unchecking, `Auto-next` OFF default, `[ERR+HIS]` and card chips, the `Phone tutorial:` dropdown, `Data ↔ Location ↔ Problems` quick-glance & Problem Resolution workflow, and the Post-Session Wrap-Up dialog.
  - Updated `test_unified_help_and_old_names_dialogs_smoke` in `tests/test_navigation_and_dialogs.py` to exercise all 6 Help Center tabs including `"reference"`.
- **Plain-Language Trainee Impact**: Trainees and helpers now have a single, consistent visual reference for every badge, chip, ICEDIG code, and rule both at their desk (`F1 → Badges & Reference`) and on their phone (`?`), and both user manuals accurately match the live screen layout and workflows.
- **Documentation Sync Checklist**:
  - [x] `USER_GUIDE.md` updated and verified
  - [x] `MOBILE_COMPANION_USER_GUIDE.md` updated and verified
  - [x] In-app Desktop Help Center & Mobile `?` Field Guide synced
  - [ ] Printable Desk Cheat Sheet (`documentation/curator/KEYBOARD_SHORTCUTS_CHEAT_SHEET.md`) — no shortcut keys changed


---

### Entry 74: Hover & Tap Tooltips Directly on Status Badges (Desktop + Mobile V2)
- **Date**: 2026-11-25
- **Area**: Specimen Directory Cards (`ui/widgets.py`), Mobile Companion V2 (`backend/mobile_template_v2.py`)
- **Code Delta**:
  - Added `STATUS_BADGE_TOOLTIPS` and recycled-card-safe hover tooltip methods (`_schedule_badge_tooltip`, `_show_badge_tooltip`, `_hide_badge_tooltip`) to `SpecimenDirectory` in `ui/widgets.py` with a 220ms hover delay, dark-mode-aware styling, and screen-edge clamping.
  - Added `MOBILE_BADGE_TOOLTIPS` and `showBadgeTooltip()` / `hideBadgeTooltip()` in `backend/mobile_template_v2.py`, wired to all Specimen List status badge pills (`[REV]`, `[REV+ERR]`, `[REV+NOTE]`, `Flagged ⚠`, `[NOTE]`, `[UNREV]`, `↗ Loaned`) and the Detail View `↗ Loaned` pill (with `event.stopPropagation()` so tapping a badge explains it without opening the specimen, plus a 1-tap `Guide →` link to the full Field Guide modal).
- **Plain-Language Trainee Impact**: Trainees can hover over any Desktop status badge or tap any Mobile status badge to immediately see a 1-line plain-English explanation without opening Help.
- **Documentation Sync Checklist**:
  - [x] Passive UI discoverability enhancement — no shortcut, setting, or workflow change required in manuals


---

### Entry 75: 1-Click "Reviewed Today / This Mobile Session" Filter & Batch Problem Solver Handoff
- **Date**: 2026-11-25
- **Area**: Mobile Session Tracking (`backend/mobile_server.py`), Filter & Batch Handoff (`ui/main_window.py`, `ui/filter_dialog.py`, `ui/command_palette.py`), Batch Problem Queue (`ui/object_problem_resolver.py`), Post-Mobile Popup (`ui/mobile_dialog.py`)
- **Code Delta**:
  - Tracked `session_reviewed_ids` in `MobileServer` (`backend/mobile_server.py`) and synced it to `app_state.last_mobile_session_reviewed_ids` whenever a phone marks or unmarks `Reviewed`.
  - Added `get_reviewed_today_oids()`, `get_mobile_session_reviewed_oids()`, `apply_reviewed_batch_filter()`, and `send_reviewed_batch_to_problem_queue()` in `ui/main_window.py` using existing `ReviewedAt` ISO timestamps and session IDs (zero new Excel columns).
  - Added **`📅 Reviewed Today`** (and **`📱 This Mobile Session`** when active) quick buttons to the Filter Dialog (`Ctrl+G`) and 4 matching commands to the Command Palette (`Ctrl+K`).
  - Added **`📅 Reviewed Today (N)`** and **`📱 Reviewed This Mobile Session (N)`** scopes (plus `initial_scope` parameter) to `ProblemQueueDialog` (`ui/object_problem_resolver.py`).
  - Upgraded the Post-Mobile Wrap-Up Popup (`ui/mobile_dialog.py`) to show exact session counts (clean, flagged, `Needs Specialist`) with 1-click **`✅ View N Reviewed`** and **`🔧 Batch Problem Solver`** buttons.
  - Added `test_reviewed_today_and_mobile_session_batch_and_problem_queue` to `tests/test_navigation_and_dialogs.py`.
- **Plain-Language Trainee Impact**: After a desk shift or vault walk, users can see all objects they reviewed today or during their mobile session in 1 click — and send that exact batch straight into the Batch Problem Solver to finish flagged items at a keyboard.
- **Documentation Sync Checklist**:
  - [ ] `USER_GUIDE.md` & `MOBILE_COMPANION_USER_GUIDE.md` — can be synced in the next doc pass if desired


---

### Entry 76: Standalone `Arbor.exe` Release-Prep & Hardening Pass
- **Date**: 2026-11-25
- **Area**: Packaging (`main.spec`, `build_exe.bat`), Writable File Locations (`utils.py`, `main.py`, `ui/main_window.py`, `ui/dialogs.py`), Mobile Companion shutdown (`backend/mobile_server.py`, `ui/main_window.py`), Logging, Repo hygiene
- **Code Delta**:
  - Added `utils.get_user_data_dir()`: settings (`user_prefs.json`), `logs/`, `ignored_words.json`, `filter_presets.json`, and the Demo Project copy are saved next to `Arbor.exe` when that folder is writable, otherwise in `%LOCALAPPDATA%\Arbor` (e.g. when Arbor sits in `Program Files`). They never go into the temporary unpack folder.
  - Log files are now only created when something is actually logged (no more empty `arbor_*.log` files every launch). Leftover `print()` calls now go to the session log instead.
  - Windows Firewall helper calls in the Mobile Companion no longer flash a black console window. Closing Arbor now also ends any active Mobile Companion session so internet tunnels never keep running in the background.
  - `main.spec`: disabled UPX packing (avoids antivirus false alarms), removed unneeded Flask data collection and the stale `archive` exclude. `build_exe.bat`: only the two readable user guides are copied next to `Arbor.exe`; the word list, Demo Project and tutorial images are already bundled inside the exe.
  - Fixed a pandas FutureWarning in the problem-flag check (`ui/database_ops.py`) with identical results.
  - Removed retired `archive/` folder (Qt prototypes, Qt tests, design mockups), `backend/mobile_archived_flag_issue.py`, throwaway `scripts/test_*.py`, and untracked `scratch/` and `filter_presets.json`. Merged the duplicate `.Jules`/`.jules` folder. Everything stays recoverable from Git history.
  - Tests: renamed 3 same-named tests for clarity, added 2 tests for the writable-folder fallback.
- **Plain-Language Trainee Impact**: No visible change to screens, buttons, shortcuts, or workflows. Arbor is safer to run from any folder (including read-only ones), leaves no empty log clutter, shows no console flashes, and fully stops phone sessions when closed.
- **Documentation Sync Checklist**:
  - [x] No shortcut, setting, badge, or workflow changed — `USER_GUIDE.md` / `MOBILE_COMPANION_USER_GUIDE.md` need no sync
  - [x] `documentation/agent/codebase_guide.md` updated (archive removed)


---

## 2026-11-26 — Startup Quick Guide for Economic Botany Collection (`F1` & Help Menu)
- **Feature Area:** Project Setup (`StartupDialog`) & Interactive Tutorials (`ui/tutorials/startup_guide.py`)
- **Code Delta:**
  - Added `ui/tutorials/startup_guide.py` (`start_economic_botany_startup_guide`) using `TutorialRunner` (`use_sandbox=False`) to guide first-time users step-by-step through selecting `Økonomisk_Botanisk_Arbor.xlsx`, the `Øko` photo folder, and `Books.xlsx` with one-click folder path copy buttons and glowing widget highlights.
  - Wired `<F1>`, a subtle clickable onboarding tip banner (*"New to Arbor? Check how to load the Economic Botany collection"*), and a top `Help` menu item in `StartupDialog` (`ui/dialogs.py`), with automatic HUD cleanup on close/launch.
  - Updated `README.md` (English) with clear purpose (auditing collections & preparing data for Specify), Windows `.exe` quick start, Mobile Companion multi-user workflow, and AI Agent Guide overview.
- **Trainee Impact:** First-time users landing on the Project Setup screen can now press `F1` or click the tip banner / `Help` button to get an interactive walkthrough of how to load the Economic Botany collection before entering the main workspace.
- **Documentation Sync Checklist:**
  - [x] `README.md` updated
  - [x] `tests/test_sandbox_tutorials.py` updated
