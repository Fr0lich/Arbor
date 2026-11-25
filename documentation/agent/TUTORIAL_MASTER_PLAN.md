# Arbor Interactive Tutorials — Master Blueprint & Design Document

**Status:** Master Design Blueprint (Synced with Entries 61–62)  
**Target Audience:** Brand-new museum trainees, interns, and collection assistants (minimal tech comfort, zero botanical background required)  
**Core Journey:** **Desk (Safe Practice) → Collection (Live Phone) → Back at Desk (Live Real Work)**

---

## 1. Overarching Onboarding Philosophy

Arbor's onboarding follows a real museum shift seamlessly from safe practice into real curatorial work:

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                GETTING STARTED WITH ARBOR (3-PART CORE INTRO)              │
│                                                                            │
│   [ PART 1: AT YOUR DESK ]        Safe Practice Mode (#110 & #198 photos)  │
│   Desktop Basics                  Teaches the COMPLETE 3-Way Mental Model: │
│                                   1. Fix / Problem Resolution (REV+ERR)    │
│                                   2. Per-field ⋯ ICEDIG codes              │
│                                   3. Needs Specialist (REV+NOTE)           │
│              │                                                             │
│              ▼                                                             │
│   [ PART 2: IN THE COLLECTION ]   Live Workspace + Your Phone              │
│   Mobile Companion                The exact same 3 paths on your phone +   │
│                                   Set Shelf & 5-sec ↩ Undo                 │
│              │                                                             │
│              ▼  (Stopping Mobile Server triggers Post-Shift Handoff Popup) │
│   [ PART 3: BACK AT YOUR DESK ]   LIVE on Your Real Collection by Default! │
│   Desk Follow-Up (REV+ERR)        Batch Filter, Queue Mode, 1-click Clear, │
│                                   Multi-field Sidebar, ICEDIG ▾ & Ctrl+S   │
│                                   (+ 1-click Practice Sample Data option)  │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                STANDALONE / ON-DEMAND GUIDES (NOT PART OF INTRO)           │
│  • Collections & New Specimens (Practice Mode — only when creating/adding) │
│  • Quick Guides (20–30s, Live In-Place — Hallway Follow-Up, Image Zoom)    │
│  • Startup "How to Open Arbor" & Mobile Built-In Walkthrough / Field Guide │
└────────────────────────────────────────────────────────────────────────────┘
```

### Mandatory Live UI & Curatorial Rules (Synced with Entries 61–62)
1. **Explain the Desk → Collection → Back at Desk rhythm upfront** on both the **Welcome to Arbor** screen and **Part 1 Step 1**.
2. **Teach the Complete 3-Way Curatorial Decision Rule in Part 1 (BEFORE Mobile Companion):**
   - **Canonical ICEDIG Codes (`unknown:missing`, `unknown:indecipherable`, `unknown:undigitized`, `withheld`)** — *Confirmed blank or genuinely unreadable on the label, with NO conflicting older catalog books ("stop looking for it").*
     - Always use exact canonical ICEDIG code names in tutorial copy (never substitute simplified aliases like "Blank" or "Illegible" alone).
     - **Desktop Registration Form:** Per-field quiet **`⋯`** button on the right edge of every editable field (`tutorial_id = "icedig_field_btn"` on `Collection Date`; also available via right-click → *Set ICEDIG status*, `?m`/`?i`/`?u`/`?w`, and `Ctrl+Shift+M/I/U/W`). Auto-clears that field's Problem box, highlights `⋯` in amber, and warns if older books conflict. *(Zero `?` buttons on Desktop fields; no header ICEDIG button.)*
     - **Desktop Problem Resolution:** Single **`ICEDIG ▾`** dropdown button listing all 4 canonical codes.
     - **Mobile Companion V2:** On `Details`, **tap the field value itself** (`— ▾` or `unknown:missing ▾`) to open `#icedigFieldSheet`; on `History` (Problem Resolution), tap **`ICEDIG ▾`**. *(Zero `?` icons on Mobile `Details` rows.)*
     - **Finding back later:** **Filter → Archival Gaps (ICEDIG)** per-code tri-state filters.
   - **Tier 1 — Actionable Field Problems (`Collection_Date_Problem`, `Genus_Problem`, `Box_Label_Problem`, etc.)** — *Data issue fixable at the desk / Problem Resolution.*
     - Crucial guardrail: If a physical label is blank **but** older books have conflicting values, **do NOT set `unknown:missing`** — leave the field problem flagged, optionally add a passive `Comment`, stamp Storage Location, and Mark Reviewed → orange **`[REV+ERR]`**.
   - **Tier 2 — `Needs Specialist` (`Other_problem` + `Comment`)** — *Physical damage, mold/pest, mixed specimens, or archival deadlocks that desk tools cannot solve.*
     - Desktop: Synced **`Needs Specialist`** checkbox + responsive wrapping quick-tag pills (driven by `config.SPECIALIST_QUICK_TAGS` — do not hardcode a pill count) + inline hint above `Comment`, AND separated **`Needs Specialist`** checkbox (`tutorial_id = "other_problem_checkbox"`) in the Problems tab.
     - Mobile V2: Single **`Needs Specialist`** checkbox + quick-tag pills directly above `Comment` (lower card is **`Photo & Media Issues`**).
     - Produces calm teal **`[REV+NOTE]`** (reviewed) or indigo-slate **`[NOTE]`** (unreviewed) — never `[REV+ERR]`, never triggered by a plain `Comment` alone, and **unchecked by default** in `ProblemQueueDialog`.
3. **Physical-Inspection Rule:** Only mark **Reviewed** after physically inspecting the real object (*some images may be outdated, so they should not be your primary source*). Zero photography mechanics inside Arbor.
4. **Workspace Layout:** Registration header has 2 rows (Row 1: *Registration Data* + Focus Mode; Row 2: *History* and conflict pill `history_indicator_label`; *Old Names* & *GBIF* live in `TOOLS ▾` / `Ctrl+K`). Storage Location always sits below the image/summary pane in the middle column across all image modes (`F8` hides/restores images cleanly).
5. **Proximity-Anchored Tutorial HUD & Highlights (`tutorial_runner.py`):** Every step's HUD card docks right beside its highlighted target (right of left-column controls, left of right-column controls, directly below top-bar buttons, and outside popup dialogs without covering them). Steps with `target_id=None` stay in the previous step's position (carrying across Part 1 → Part 2). Set `hud_avoid_photo=True` on any `ActionStep` where the trainee must read the center specimen photo while working in the right pane. `TutorialHighlight` uses focus-aware `-topmost` on Windows and retries deferred string targets automatically.

---

## 2. Complete Tutorial Catalog Overview

| Tutorial | Series / Group | Practice Mode? | Duration | File |
| :--- | :--- | :--- | :--- | :--- |
| **Part 1: Desktop Basics** *(renamed from 3-Minute Quick Tour)* | **Core Intro (1 of 3)** | ✅ Yes (Sandbox: real photos `#110` & `#198` + `#1003`) | ~3–4 min | `ui/tutorials/review_tutorial.py` |
| **Part 2: Mobile Companion (In the Collection)** | **Core Intro (2 of 3)** | ❌ No (Live Workspace + Your Phone) | ~2 min | `ui/tutorials/micro_guides.py` (`start_armed_shelf_guide`) |
| **Post-Shift Batch Follow-Up Popup** | Automatic Handoff (on Mobile server stop) | ❌ No (Live prompt on Desktop) | Instant | `ui/mobile_panel.py` (`stop()`) |
| **Part 3: Desk Follow-Up & Batch Tools (`REV+ERR`)** | **Core Intro (3 of 3)** | ❌ **Live on Real Collection by Default** *(+ 1-click Practice Sample Data fallback)* | ~2–3 min | `ui/tutorials/triage_tutorial.py` |
| **Collections & New Specimens** | Standalone (Optional / Admin) | ✅ Yes (Sandbox: `#3001`, `#3002`) | ~2 min | `ui/tutorials/database_tutorial.py` |
| **Hallway Follow-Up (`REV+ERR`) — 30s** | Quick Guide (In-Place) | ❌ No (Live Workspace) | ~30 sec | `ui/tutorials/micro_guides.py` |
| **Image Zoom, Pan & Rotate — 20s** | Quick Guide (In-Place) | ❌ No (Live Workspace) | ~20 sec | `ui/tutorials/micro_guides.py` |
| **How to Open Arbor** | Startup Help Window | N/A (Reference Window) | ~1 min | `ui/dialogs.py` |

*(Legacy `discrepancy_tutorial.py` remains importable for backwards compatibility, while its multi-field desk skills are unified into Part 3.)*

---

## 3. Deep-Dive Specifications

### Part 1 of 3 — Desktop Basics (`ui/tutorials/review_tutorial.py`)
- **Mode:** Safe Practice Mode (`mock_type="review"`). Real photos `#110` & `#198` untouched!
- **Enhancement to `#198` in `sandbox_manager.py`:** Set `#198`'s `Collector` to `""` (blank) with `Collector_Problem = True` and NO historical collector entries — so `#198` naturally teaches **all 3 curatorial paths** in one memorable real object:
  1. `welcome_overview` — Introduces Arbor Desktop + the **Desk → Collection → Back at Desk** 3-part rhythm + Practice Mode.
  2. `orient_110` — Registration Data (right) + field problem checkboxes on `#110`.
  3. `transcribe_110_date` — Read `#110`'s photos (thumbnails below) & fill missing `Collection Date` (`00.06.1910` / `06.1910`).
  4. `mark_110_reviewed` — Uncheck date box + `✓ Mark as Reviewed` (`Ctrl+Enter`) → **green `[REV]`** + physical-inspection rule.
  5. `select_198` — Specimen Directory (left) + `Ctrl+F` search for `#198`.
  6. `open_198_history` — Click `history_indicator_label` (`Ctrl+H`) to open **Problem Resolution**.
  7. `resolve_198_date` — Compare 3 sources (`1963` / `1927` / `1912`) against `#198`'s photo and click **Apply** on `1927`.
  8. `close_198_resolver` — Click **`Save Edits`** (`hr_apply_all`) to save & close.
  9. **`mark_198_icedig` *(NEW — completes the 3-Way Rule before Mobile!)*** — `#198` has no collector on its label and no older books listing one. Click the quiet **`⋯`** button next to `Collector` and pick **`unknown:missing`** (explains canonical ICEDIG codes `unknown:missing`, `unknown:indecipherable`, `unknown:undigitized`, `withheld`, notes `⋯` turns amber and clears the problem box automatically, and states the guardrail: *never set `unknown:missing` when older books disagree!*). Auto-advances when `Collector == "unknown:missing"`.
  10. `flag_other_issue` — `#198`'s bent wire → 2-stage highlight (**Problems** tab header → **`Needs Specialist`** `other_problem_checkbox`), noting the synced **`Needs Specialist`** checkbox + quick-tag pills right above `Comment`.
  11. `mark_reviewed` — Mark `#198` Reviewed → calm teal **`[REV+NOTE]`** (*"You've done everything you can here — the rest is for a specialist to handle later."*).
  12. `review_complete` — Direct launch buttons: **`📱 Part 2: Mobile Companion (Recommended)`** and **`🎯 Part 3: Desk Follow-Up (REV+ERR)`**, plus `▸ Need help opening Arbor?`.

---

### Part 2 of 3 — Mobile Companion: In the Collection (`ui/tutorials/micro_guides.py` + `backend/mobile_template_v2.py`)
- **Mode:** Live Workspace + Hands-On Phone Coach Tutorial (`use_sandbox=False`).
- **Desktop Launch Handoff (`start_armed_shelf_guide`):**
  1. `mg_mobile_intro` — Short, calm intro explaining how Mobile Companion brings Part 1's workflow to your phone.
  2. `mg_mobile_open` — Click highlighted `MOBILE` (`mobile_nav_btn`) in the top bar.
  3. `mg_armed_setup` — Mobile Session Launch window: leave **Phone tutorial** on **Ask on the phone** (or pick **Trainee** / **Helper** / **Off**), click highlighted **`▶ Start Mobile Session`** (`mobile_start_btn`).
  4. `mg_armed_review` — **`Scan the QR Code — Continue on Your Phone`**: auto-completes when a phone connects (or via `Finish ✓`). Does **not** send the user back to Part 3 yet — the end-of-session popup offers Part 3 when they return and click Stop.
- **Phone Coach Tutorial (`#coachCard` in `mobile_template_v2.py`):**
  - **Trainee (5 steps):** `Set Shelf` → `search` → `Details / Location / History` screen tour → `Save to Shelf` + `✓ Mark Reviewed` → `You're ready!`
  - **Helper (4 steps):** `Set Shelf` → `search` → `check, save, mark reviewed` → `You're ready!`
  - **One-Time Contextual Tips (`maybeShowTip`):** `tip_flagged`, `tip_icedig` (Trainee only), `tip_specialist`, `tip_rev_err`, manageable in phone **⚙ Settings → Phone tutorial**.

---

### Post-Shift Handoff Popup (`ui/mobile_panel.py` → `stop()`)
When the user shuts down the Mobile Companion server on Desktop (unless suppressed via `user_prefs.json["suppress_mobile_stop_followup_popup"]`):
- Counts waiting actionable **`[REV+ERR]`** objects in the active workbook.
- Displays a calm, centered dialog (`<Escape>` closes):
  - **Headline:** `Mobile Session Ended — Ready for Batch Follow-Up?`
  - **Summary:** Shows exact count of `[REV+ERR]` objects ready for desk triage (or celebrates if 0 remain and reminds to press `Ctrl+S`).
  - **Self-discovery note:** *"You can open Batch Follow-Up yourself anytime from **`TOOLS ▾ → Open Problem Queue & Resolver...`**, **`Ctrl+K`**, or **`Ctrl+G → Hallway Follow-Up (REV+ERR)`**."*
  - **Checkbox:** `☐ Don't show this popup again when stopping Mobile Companion`
  - **Buttons:**
    - Primary: **`🎯 Open Batch Follow-Up (Problem Queue)`** *(if `[REV+ERR] > 0`)*
    - Secondary: **`🎓 Guided Desk Follow-Up (Part 3)`** *(if Part 3 not yet completed)*
    - Dismiss: **`Close`**

---

### Part 3 of 3 — Desk Follow-Up & Batch Tools (`REV+ERR`) (`ui/tutorials/triage_tutorial.py`)
- **Mode:** **LIVE on Your Real Collection by Default (`use_sandbox=False`)** — zero interruption to the real post-hallway workflow!
- **Smart Practice Fallback:** If the user's real collection currently has **0** `[REV+ERR]` objects (or if they click **`🛡️ Practice with Sample Data Instead`** from Help Center or Step 1), mounts a clean 4-specimen artificial sandbox (`#2001` `[REV+NOTE]` auto-excluded, `#2002` false alarm `[REV+ERR]`, `#2003` blank physical date + 2 conflicting older books `[REV+ERR]`, `#2004` clean `[REV]`).
- **Zero-Repetition 5-Step Flow (100% Pure Batch Desk Tools):**
  1. **`triage_intro`** — Back at your desk! Shows how many `[REV+ERR]` objects are ready in your current collection (and notes `[REV]` and `[REV+NOTE]` stay out of your queue automatically). Includes 1-click button **`🛡️ Practice with Sample Data Instead`** if they want risk-free sample data (highlighted prominently if 0 `[REV+ERR]` objects exist).
  2. **`triage_filter`** — Press **`Ctrl+G`** → **`Hallway Follow-Up (REV+ERR)`** (also points out **Filter → Archival Gaps (ICEDIG)** for finding `unknown:missing` / `unknown:indecipherable` records back later).
  3. **`triage_open_queue`** — Highlights `tools_nav_btn`: **`TOOLS ▾ → Open Problem Queue & Resolver... → OPEN QUEUE`** (notes `Needs Specialist` is unchecked by default so trainees focus on actionable errors while specialists can opt in). Auto-advances when **Problem Resolution** opens.
  4. **`triage_queue_tools`** — Inside **Problem Resolution (Queue Mode)** (`hr_sidebar` / `hr_cards`): introduces the 4 batch desk tools:
     - **`Alt+← / Alt+→`** or **`SKIP OBJECT →`** to step across specimens
     - **`✓ Value is Correct (Clear Flag)`** for false alarms (turns `[REV]` in 1 click)
     - **Left sidebar** + **Historical Suggestions** + **`📜 Old Names` / GBIF** for multi-field older book conflicts
     - **`ICEDIG ▾`** dropdown for confirmed absent/unreadable fields with **no** conflicting older books
  5. **`triage_complete`** — Click **`Save Edits`** / **`Close Queue`** when finished and press **`Ctrl+S`** to save your work! Celebrates completing the **3-Part Core Introduction**, plus the 1-line secondary desk rule (*if you run out of `[REV+ERR]` at your desk, you can also clean up `[UNREV]` older-book conflicts — just leave `Reviewed` unchecked until someone physically inspects the real object*).

---

### Standalone Optional Guide — Collections & New Specimens (`ui/tutorials/database_tutorial.py`)
- Clearly separated under **Optional / On-Demand Guides** in the **Arbor Help Center** (not part of the 3-Part Core Intro or Welcome screen).
- Notes Storage Location sits directly below the image/summary pane in the middle column (`Ctrl+L`).

---

## 4. Implementation Status (Completed)
1. **`ui/registry_panel.py`**: Ensure `Collector`'s `⋯` button also has `tutorial_id = "icedig_collector_btn"` (alongside `Collection Date`'s `icedig_field_btn`) so Part 1 Step 9 highlights the exact `⋯` button next to `Collector`!
2. **`ui/tutorials/sandbox_manager.py`**: Update `#198` (`Collector = ""`, `Collector_Problem = True`, no historical collector) and update `mock_type="triage"` to the clean 4-specimen artificial fallback sandbox (`#2001`–`#2004`).
3. **`ui/tutorials/review_tutorial.py`**: Rename to **Part 1: Desktop Basics**, add Desk→Collection→Desk framing in Step 1, insert Step 9 (`mark_198_icedig` highlighting `icedig_collector_btn` with canonical ICEDIG codes), and point Step 7 & Step 12 to **Part 2** & **Part 3**.
4. **`ui/tutorials/triage_tutorial.py`**: Rebuild as **Live-by-Default Part 3: Desk Follow-Up & Batch Tools (`REV+ERR`)** with 1-click **Practice with Sample Data** fallback.
5. **`ui/tutorials/micro_guides.py` & `ui/tutorials/database_tutorial.py`**: Sync Part 2 (`start_armed_shelf_guide`) to Entries 61–62 (tap field value for `#icedigFieldSheet`, `Set ICEDIG Code…`, `Photo & Media Issues`, `Needs Specialist` `[REV+NOTE]`) + Part 3 handoff button; note middle-column Storage Location in `database_tutorial.py`.
6. **`ui/mobile_panel.py`**: Add the **Post-Shift Batch Follow-Up Popup** on `stop()` with `[REV+ERR]` count, self-discovery paths, 1-click launch buttons, and persisted `Don't show this popup again` checkbox.
7. **`ui/database_ops.py` & `ui/unified_help.py`**: Update **Welcome to Arbor** and **Arbor Help Center** to the 3-Part Core Intro (`CORE INTRO: X OF 3 COMPLETED`) + separate Optional Guides section.
8. **Verify**: Run `python -m pytest tests/test_sandbox_tutorials.py tests/test_navigation_and_dialogs.py -q` (never touching `data/tutorial_images/`) and log in `documentation/CHANGE_JOURNAL.md`.
