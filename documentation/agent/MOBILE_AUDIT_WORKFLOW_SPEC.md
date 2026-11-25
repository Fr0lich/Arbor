# Mobile Companion Ground-Truth Workflow & Object View Specification
**Authoritative Architectural & Curatorial Guide for AI Agents**

---

## 1. Executive Context & Architectural Ground Truth

Arbor is an active, production desktop application written in **Tkinter** with an embedded **Flask** mobile companion server (`backend/mobile_server.py`). The mobile client is designed for museum interns, collection assistants, and trainees walking physical vaults and hallway glass cases.

### The Real-World Curatorial Problem Arbor Solves:
1. **Location Data is Unknown Ahead of Time**: 
   A museum collection database rarely knows where historical specimens physically sit. Decades of reorganizations, loans, and misplacements leave location fields blank or outdated.
2. **The Search-First Workflow**:
   An intern stands at a glass cabinet, picks up a physical specimen folder/box, reads the physical accession number on the label, searches for that accession number on their phone, and opens the record.
3. **Auditing Consecutive Batches in One Cabinet**:
   Once an intern opens a cabinet, they will inspect 30 to 50 specimens on the same shelf before moving to the next. The mobile app must make assigning physical coordinates (*Building*, *Floor*, *Cabinet*, *Shelf*) instantaneous without requiring repetitive, error-prone typing.
4. **Two-Path Discrepancy Triage**:
   - **Path A (Resolvable on the spot)**: The physical label in hand clarifies a historical contradiction (e.g. verified collection year "1998" vs conflicting "2008"). The intern taps **"Apply Fix"** from the Historical Suggestions picker.
   - **Path B (Actionable desk error — e.g., blank physical label with conflicting historical ledgers)**: The problem requires desktop flora literature, historical ledger reconciliation, or box-label cleanup. **Do NOT set `unknown:missing`** if historical sources still disagree. Leave the specific field problem flagged (`Collection_Date_Problem = True`, `Species_Problem = True`), optionally write a passive `Comment` (*"No date on physical box label"*), **AND STILL MARK THE OBJECT AS REVIEWED (`Reviewed = True`)** → shows **`REV+ERR`** for desktop curation.
   - **Path C (Confirmed blank/illegible with NO conflicting history)**: Tap the **`?`** ICEDIG button directly on that field in `Details` and select `unknown:missing` or `unknown:indecipherable`.
   - **Path D (Physical condition / specialist escalation — broken jar, mold/pest, mixed specimen, archival deadlock)**: Check **`Needs Specialist`** (`Other_problem = True`) next to **`Comment`** and add a brief note (or tap a non-ICEDIG physical quick-tag pill). Marking Reviewed produces **`REV+NOTE`** (never `REV+ERR`) and keeps it out of the default trainee desk queue.
5. **Architectural Constraints (Non-Negotiable)**:
   - **Zero Barcodes**: Barcode scanning is completely removed from Arbor. Never add barcode dependencies.
   - **Zero Build Mobile Stack**: The mobile frontend lives strictly as an embedded pure-Python string constant (`INDEX_TEMPLATE_V2` in `backend/mobile_template_v2.py`, re-exported by `backend/mobile_server.py`) using Vanilla HTML/JS, deferred Tailwind CSS CDN, and scoped `html.arbor-offline-css` offline fallback. Never introduce Node.js, npm, webpack, Vite, or external asset builds.
   - **Dual-Perspective Store**: Edits must be validated through Marshmallow (`backend/mobile_schemas.py`) and written cleanly into in-memory DataFrames (`df_reg`, `df_obs`), persisting to Excel.

---

## 2. ⚠️ THE ACCIDENTAL LOOKUP HAZARD & THE "ARMED SHELF" DEFENSIVE PATTERN

> **CRITICAL CURATORIAL WARNING FOR AGENTS:**
> **NEVER** implement an "auto-stamp on open" feature that silently assigns or overwrites coordinates the moment a record loads. Doing so is curatorial poison.

### Why Silent Auto-Stamping Fails in Production:
1. **Accidental Typos**: Interns frequently mistype digits while walking down a dim vault aisle (e.g., typing `#101` instead of `#1001`, or looking up `#181` instead of `#18`). If opening a record automatically stamps coordinates, an innocent lookup instantly corrupts an unrelated specimen.
2. **Auto-Save Flushing Trap**: Arbor’s mobile companion employs debounced auto-saving (800ms) and flushes immediately on navigation (`showListView()` calls `forceSaveImmediate()`). An intern who opens the wrong object and immediately taps `< Back` would silently commit the wrong coordinates to the server before noticing the mistake.
3. **Destructive Relocation**: If an accidentally opened specimen already has valid registered coordinates in a different cabinet (e.g., *Cabinet 04, Shelf 02*), an automatic silent stamp would overwrite that data and effectively "lose" the specimen in the database.

---

### The Defensive Architecture: "Armed Target Shelf" + Intentional Confirmation

To solve the friction of auditing 50 consecutive specimens without risking accidental data corruption, agents must implement the **Armed Target Shelf Pattern**:

```
+-----------------------------------------------------------------------------------+
|                        ARMED TARGET SHELF PATTERN                                 |
|                                                                                   |
|  [Session State]                                                                  |
|   Target Anchor Armed: [ Lid's hus · Floor 1 · Cabinet 21 · Shelf 01 ]            |
|                                                                                   |
|  [Scenario A: Object Opened Has NO Location (—)]                                  |
|   Record loads cleanly. dirtyFields is EMPTY.                                     |
|   Above-the-fold banner displays:                                                 |
|   +-----------------------------------------------------------------------------+ |
|   | ⚡ Target Shelf Armed: Lid's hus · Fl 1 · Cab 21 · Sh 01                     | |
|   | [ 1-Tap Stamp Shelf ]  <-- Explicit single tap required to dirty/commit     | |
|   +-----------------------------------------------------------------------------+ |
|   If user presses Back without tapping: 0 bytes written, record stays pristine.   |
|                                                                                   |
|  [Scenario B: Object Opened Already Has A Location (e.g., Cab 04 · Sh 02)]        |
|   Record displays existing location prominently.                                  |
|   Relocation Guard prevents silent overwrite:                                     |
|   +-----------------------------------------------------------------------------+ |
|   | 📍 Current Location: Lid's hus · Fl 1 · Cab 04 · Sh 02                      | |
|   | ⚠️ Different from Armed Target (Cab 21 · Sh 01)                             | |
|   | [ Relocate to Cab 21 · Sh 01 ] <-- Guarded action with confirmation toast   | |
|   +-----------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

#### Defensive Rules for Implementation:
1. **Pristine State on Open**: Opening an object via `fetchObjectDetail(oid)` must **never** add fields to `dirtyFields` or invoke `triggerAutoSave()`.
2. **Explicit 1-Tap Arming**: Applying the armed shelf requires exactly one intentional tap on a prominent, thumb-friendly banner directly below the specimen header.
3. **Deferred Commit via "Mark Reviewed"**: Alternatively, the UI can allow the intern to tap **"Mark Reviewed"**, which can check:
   *If the object has no location and an active shelf is armed, prompt/apply: "Stamp to active Shelf 21 and Mark Reviewed?"*

---

## 3. Verified Audit Scenarios & Simulation Findings

An automated simulation was executed against `data/demo_collection.xlsx` (configuration profile: **"Økonomisk Botanisk"**, 220 registered specimens) using the Flask test client. All future modifications must preserve parity with these verified behaviors:

### Scenario 1: Initial Discovery & Location Stamping
- **Search**: `GET /api/objects?q=<number>` searches both `ObjectID` and `Object Number`, as well as scientific name and taxon fields.
- **Fetch**: `GET /api/object/<oid>` returns `review_status` (`"pending"` or `"reviewed"`), `registration` dict, `observation` dict, and `images` dict.
- **Update**: `POST /api/update` payload validated via `ObjectUpdateSchema` (`backend/mobile_schemas.py`):
  ```json
  {
    "oid": "1",
    "observation": {
      "Building": "Lid's hus",
      "Floor": "1",
      "Cabinet": "21",
      "Shelf": "1"
    }
  }
  ```
- **Verification**: Updates `app.df_obs` synchronously under `with app.df_lock:` and returns `{"success": true}`.

### Scenario 2: Consecutive Auditing via Cached Coordinates
- Client caches last confirmed coordinates in `localStorage` under `arbor_last_location`.
- The `btnCopyPrevSpecimen` action replicates `Building`, `Floor`, `Cabinet`, `Shelf`, and `Stored as`.
- **Finding**: Currently, this button is buried inside Tab 1 (`Location`). It must be promoted to the top-level sticky header to prevent requiring interns to switch tabs for every single specimen.

### Scenario 3: On-the-Spot Resolution via Historical Data Picker
- **History Endpoint**: `GET /api/object/<oid>/history` aggregates conflicting determinations from loaded historical databases (`app.historical_dbs`).
- **UI Resolver**: Tapping "Apply Fix" calls `resolveFieldDiscrepancy(targetField, probName, newVal, clearFlag=true)`.
- **Payload**:
  ```json
  {
    "oid": "1",
    "registration": { "Collection Date": "1998" },
    "observation": { "Collection_Date_Problem": false }
  }
  ```
- **Verification**: Resolves both perspectives: updates `df_reg` with the accepted value and sets `df_obs[Problem_Column] = False`.

### Scenario 4: Deferring Unresolvable Issues & Marking Reviewed
- Specimen `#181` has active `Species_Problem = True` and `Box_Label_Problem = True`.
- Intern sets `Reviewed = True` while keeping problem flags `True`.
- **Finding**: The server handles `reviewed=True` alongside problem flags without conflict, transitioning `review_status` to `"reviewed"`.
- **Ergonomic Pitfall**: The current mobile UI changes the badge to a generic green `REVIEWED` pill. Interns report hesitation because there is no visual indication that their problem flags were safely preserved.

---

## 4. Object Detail View Ergonomics Blueprint (`INDEX_TEMPLATE_V2`)

`INDEX_TEMPLATE_V2` lives in `backend/mobile_template_v2.py` (re-exported by `backend/mobile_server.py`).

### A. Above-the-Fold Visual Hierarchy (The 50% Rule)
When an intern opens a specimen in dim museum lighting, the top 50% of the viewport must immediately answer three questions:
1. *What object is in my hand?* (Accession `#`, Botanical Latin name, Family).
2. *Where does it physically belong?* (Current coordinates or 1-tap Armed Shelf Stamping Pill).
3. *What is its audit status?* (Unreviewed vs Reviewed with Issues).

```
+-----------------------------------------------------------------------+
|  [< Vault List]      #1001 · Welwitschia           [REV + 2 ISSUES]   |
|                                                                       |
|  Welwitschia mirabilis Hook.f.                                        |
|  Family: Welwitschiaceae  ·  Stored as: Box                           |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  | ⚡ TARGET SHELF: Lid's hus · Fl 1 · Cab 21 · Sh 01               |  |
|  | [ 1-Tap Stamp Shelf ]             [ Edit Coordinates ]          |  |
|  +-----------------------------------------------------------------+  |
|                                                                       |
|  [ Folio (0) ]       [ Problems & Fixes (2) ]        [ Full Label ]   |
|  ===================================================================  |
|  (Scrollable tab content below the fold)                              |
|                                                                       |
+-----------------------------------------------------------------------+
|  [ ✓ MARK REVIEWED (STAMP & DEFER) ]             [ ⚑ Quick Flag ]     |
|  "Coordinates recorded. 2 problems flagged for desktop curation."     |
+-----------------------------------------------------------------------+
```

### B. Search Ergonomics & Numeric Keypad Optimization
* **Problem**: `#searchBox` is `<input type="text">`, which forces mobile keyboards into QWERTY mode, requiring interns to tap `?123` every time.
* **Solution**:
  1. Add `inputmode="numeric"` to `#searchBox` by default, with an inline toggle icon to switch to alphabetic mode when searching by genus/species.
  2. In `showListView()`, automatically clear the search input and focus it (`searchBox.value = ''; searchBox.focus();`) so the intern can immediately type the next accession number without tapping backspace or small clear buttons.

### C. Tri-State Status Badge & Micro-Copy Reassurance
Modify `renderDetailView()` to support three distinct visual curatorial states:

| Status | Badge Classes | Badge Text | Micro-Copy Reassurance |
| :--- | :--- | :--- | :--- |
| **Unreviewed** | `bg-stone-100 text-stone-600 border-stone-300` | `UNREVIEWED` | *"Physical inspection pending. Verify location and label."* |
| **Reviewed (Clean)** | `bg-emerald-50 text-fern-dark border-fern/30` | `REVIEWED` | *"Location recorded & verified. Specimen clean."* |
| **Reviewed + Problems** | `bg-amber-50 text-amber-900 border-amber-300` | `REV + [N] ISSUES` | *"Location recorded & verified. Flagged issues will be triaged on the desktop suite."* |

### D. Eliminating Empty Folio Screen Waste
In Tab 0 (`Details`):
- Currently, if a specimen has no images, a massive 192px empty box (`📷 Tap to Inspect Photo`) occupies vertical space.
- If `rec.images` is empty, collapse the photo section to a single compact row:
  `<div class="text-[11px] font-mono text-muted py-1 flex items-center justify-between"><span>Archival Scans: None available</span><button onclick="...">+ Add Photo</button></div>`
  This moves the registration metadata and problem resolver directly into the visible viewport.

### E. Adaptive Tab Badges
Update the segmented tab controller headers:
- **Folio Tab**: Display scan count (`Photos (0)` vs `Photos (3)`).
- **Problems Tab**: Prominent red badge (`Problems (2)`).
- **Location Tab**: Display current cabinet (`Cab 21` or `Unset ⚠️`).

---

## 5. Technical Implementation Checklist for Coding Agents

When tasked with updating `backend/mobile_server.py`:

- [ ] **Dual Template Synchronization**: Apply backend and shared logic changes to **both** `INDEX_TEMPLATE` and `INDEX_TEMPLATE_V2`.
- [ ] **Declarative Validation**: Route all inbound update payloads through `ObjectUpdateSchema` in `backend/mobile_schemas.py`. Never parse raw POST dictionaries with ad-hoc string checks.
- [ ] **No Silent Mutations**: Verify that `fetchObjectDetail()` leaves `dirtyFields` completely empty.
- [ ] **EventBus Thread Marshaling**: If dispatching desktop sync events from Flask routes, wrap `app_bus.publish()` inside `root_tk.after(0, ...)`.
- [ ] **Canonical Lexicon**: Adhere to `documentation/MASTER_DOCUMENTATION_MAP.md` (*"Specimen Directory"*, *"Storage Location"*, *"Mark Reviewed"*).
- [ ] **Documentation Journaling**: Whenever modifying user-facing toggles, badges, or workflows, append an entry to `documentation/CHANGE_JOURNAL.md`.
- [ ] **Simulation Test**: Run `python tests/test_mobile_companion.py` or the custom simulation script against `data/demo_collection.xlsx` to confirm zero regression before completing the task.
