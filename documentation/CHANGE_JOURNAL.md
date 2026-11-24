# Arbor Living Change Journal (User-Facing Delta Log)

This file tracks all user-facing changes made to Arbor. Whenever a feature, shortcut, setting, or workflow is updated in code, the authoring agent **MUST** record the change here so the documentation agent can synchronize all user guides, cheat sheets, and in-app touchpoints.

---

## 📌 Instructions for Coding Agents
1. Every time you change, add, or remove a user-facing feature (keyboard shortcut, status badge, setting toggle, panel layout, or dialog flow), append a new entry to the `[Unreleased / Recent Updates]` section below.
2. Use plain, non-technical language to describe the **User Impact** (what a trainee or museum assistant experiences at their desk).
3. Do not close a feature task until you have filled out the **Documentation Sync Checklist**.

---

## [Unreleased / Recent Updates]

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
