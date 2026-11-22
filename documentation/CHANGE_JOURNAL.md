# Arbor Living Change Journal (User-Facing Delta Log)

This file tracks all user-facing changes made to Arbor. Whenever a feature, shortcut, setting, or workflow is updated in code, the authoring agent **MUST** record the change here so the documentation agent can synchronize all user guides, cheat sheets, and in-app touchpoints.

---

## 📌 Instructions for Coding Agents
1. Every time you change, add, or remove a user-facing feature (keyboard shortcut, status badge, setting toggle, panel layout, or dialog flow), append a new entry to the `[Unreleased / Recent Updates]` section below.
2. Use plain, non-technical language to describe the **User Impact** (what a trainee or museum assistant experiences at their desk).
3. Do not close a feature task until you have filled out the **Documentation Sync Checklist**.

---

## [Unreleased / Recent Updates]

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
