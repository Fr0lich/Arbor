# Arbor Mobile Companion — Field & Curator Guide

The **Arbor Mobile Companion** is a dedicated, zero-install mobile web application that turns any smartphone or tablet into a companion terminal for physical specimen auditing in herbarium vaults, compactors, and collection stacks.

---

## 1. Quick Start & Pairing

```
┌────────────────────────────────────────────────────────┐
│ 1. On your Desktop Workstation:                        │
│    Click MOBILE in the top navigation bar.             │
│                                                        │
│ 2. Choose your Network Mode:                           │
│    • 🌐 Public (Internet): Campus & Eduroam Wi-Fi      │
│    • 📶 LAN only: Private Home / Offline Travel Router │
│                                                        │
│ 3. Click ▶ Start Mobile Session                        │
│                                                        │
│ 4. Scan the on-screen QR Code with your phone camera   │
└────────────────────────────────────────────────────────┘
```

### Network Modes Explained

* **🌐 Public (Internet) [Recommended for Institutions]**:
  * **When to use**: On university, museum, or hospital Wi-Fi networks (such as **Eduroam**).
  * **Why**: Institutional networks enforce "Client Isolation" firewalls that prevent mobile phones from talking directly to laptops on the local network. The Public mode establishes an encrypted tunnel (via Cloudflare or Pinggy/SSH) that bypasses network firewalls seamlessly.
  * **Warm-up**: While the secure tunnel connects in the background (3–10 seconds), Arbor displays the local LAN QR code immediately as a fast fallback. Once the tunnel is live, the QR code updates automatically.

* **📶 LAN only [Fast & Offline]**:
  * **When to use**: When your laptop and phone are connected to a private home Wi-Fi network or a portable travel router inside an underground vault with no internet access.
  * **Why**: Direct local Wi-Fi connection without sending any traffic through the outside web.

### Pairing Options & PIN Toggle
* **QR Code**: Open your phone's camera app and tap the link that appears on screen. The secure session link logs you in automatically — no passwords required.
* **Copy Link Button**: Click **📋 Copy** in the desktop pairing window to copy the full URL to your clipboard for instant sharing.
* **Live 4-Digit PIN Toggle**: By default, phones typing the address manually must enter the 4-digit PIN shown on your desktop screen. You can toggle **`🔒 Require 4-Digit PIN: ON / OFF`** directly inside the Mobile Companion window at any time (even while the server is running).
  * *Safety Tip*: Turning PIN **OFF** is great on a private, offline vault Wi-Fi router so staff can reconnect effortlessly. Keep PIN **ON** whenever using a **Public (Internet)** tunnel.
* **Phone Tutorial Dropdown & `?` Quick Reference**: In the desktop Mobile Companion launcher, use the compact **`Phone tutorial:`** dropdown to choose **Ask on the phone (recommended)**, **Trainee (after Desktop Part 1)**, **Helper (short — helping out today)**, or **Off (no tutorial)**. Even when set to **Off**, you can always tap **`?`** in the phone's top bar to open the **Badges, ICEDIG & Field Reference** or launch either tutorial from **`⚙ Settings → Phone tutorial`**.

---

## 2. Offline Concrete Vaults & Automatic Sync

Herbarium vaults are often located in basements or shielded behind heavy steel doors where Wi-Fi drops completely. The Mobile Companion is built to keep working smoothly offline:

```
📱 Trainee Edits Specimen
         │
         ▼
[Is Wi-Fi Connected?]
   ├── YES ──► Saved immediately to Desktop (✓ Synced)
   │
   └── NO ───► Saved safely in Phone's Offline Storage
               Banner shows: "⚠️ Offline — 4 edits queued on device"
               (Zero data loss; phone retains all values)
                     │
                     ▼ (Walk back into Wi-Fi range)
               Automatic Reconnection & Auto-Sync
               Banner shows: "🔄 Connected — Syncing 4 queued edits..."
               Desktop receives: "📥 Synced 4 offline edits"
```

### Clear Save Feedback
1. **Auto-Save While Working**: Edits save automatically when you tap away from a field or pause typing for a moment.
2. **Sync Confirmation**:
   * When connected, a confirmation badge shows: `✓ Saved & synchronized`.
   * When offline, a reassuring badge shows: `💾 Saved offline (queued for sync)`.

> **Never worry about losing data in the vault:**  
> Both the PIN login screen and the main Mobile Companion use built-in offline styling so they load instantaneously even on a local Wi-Fi router with zero internet. If you lose Wi-Fi behind a steel door, keep auditing normally — all storage coordinates, review checkmarks, and notes stay safely saved in your phone's `localStorage` queue and sync automatically to your desktop the moment Wi-Fi returns.

---

## 3. Hallway Auditing Workflows

### 3.1. Search-First Number Lookup & Finding Reviewed Objects
* **Numeric Keypad Default**: Pull a physical box, read its accession number, and type it in the top search bar — or filter for **already-reviewed objects** when pulling items for closer inspection. Use the **`[123 / Aa]`** button to switch between numbers and plant names.
* **Automatic Zero & Prefix Handling**: Typing `001`, `1`, or `O-V-1` all find Specimen `#1`. When you tap `< Back` to return to the list, Arbor automatically clears and focuses the search bar for the next box.

### 3.2. 1-Tap Storage Location Saving (`Set Shelf` + 5-Sec Undo), `Stored as` & `Loaned Out`
Opening a specimen **never** overwrites its coordinates automatically — so mistyping a number (like `#101` instead of `#1001`) can never corrupt another record.
1. **Set Your Shelf Once**: Tap **`Set Shelf`** in the compact top bar (`Shelf: Not set [Set Shelf]`) and pick the **Building, Floor** (`-2` to `4`), **Cabinet**, and **Shelf** you are standing in front of.
2. **1-Tap Save**: Inside every next box from that shelf, a green thumb button appears right under the plant name:
   `📍 Save to Cab 21 · Sh 01`
3. Tap once to save all coordinates! If a specimen already belongs to a different shelf, the button turns amber **`⚠️ Move to Cab 21 · Sh 01`** so you never relocate a specimen by accident — and **every 1-tap save or move shows a protected 5-second `↩ Undo` button** in case you tapped by mistake.
4. **Container (`Stored as`) & Lending (`Loaned Out`)**: Switch to the **Location** tab to pick **`Stored as`** from a full-width bottom sheet or toggle **`Loaned Out`** (displays an amber **`↗ Loaned`** pill on both the List and Detail header).

### 3.3. Checking Old Plant Names (`📜 Old names`) & Problem Resolution (`Problems` Tab)
* **Unfamiliar Latin or family name on the box?** Tap **`📜 Old names`** (read-only) right below the scientific name to see past museum names, classical/APG old family names (like *Compositae* → *Asteraceae*), and known GBIF synonyms — if it matches, keep the modern name!
* **Problem Resolution (`Problems` tab):** Swipe right to **`Problems`** — it works just like Desktop Arbor's Problem Resolution. When older catalog books disagree (for example, one says England and another says Finland), check the real label in your hand and:
  * Tap **`Apply`** on a matching older-book value,
  * Type a corrected value manually and tap **`Apply`**,
  * Tap **`ICEDIG ▾`** for a confirmed blank or unreadable field (only when no older books conflict), or
  * Tap **`✓ Value is Correct`** if the current value matches the real object.

### 3.4. Physical Review Rule, Quick-Glance Checking & `⚑ Needs Specialist`
* **Only tap `✓ Mark Reviewed` once you have physically checked the object.** If an object still has no saved Storage Location when you mark it Reviewed, Arbor completes the review and shows a gentle 6-second **`📍 Set Shelf`** reminder toast (never blocking your flow).
* Always give the **`Data`** tab a quick glance against the real object in your hand:
  * **Field mismatch (`[REV+ERR]`):** If something clearly disagrees with the real object (for example, the label says Africa while the file says China), tick the **checkbox right next to that field on `Data`** and still tap **`✓ Mark Reviewed`**. Leaving an unresolvable field ticked queues it safely for desk follow-up (**`🎯 Hallway Follow-Up (REV+ERR)`**).
  * **Confirmed blank/unreadable (`ICEDIG`):** **Tap the field value** on **`Data`** (or **`ICEDIG ▾`** on **`Problems`**) and pick **`unknown:missing`** or **`unknown:indecipherable`** — *only* when no older catalog book has a conflicting value.
  * **Physical damage / specialist escalation (`[REV+NOTE]`):** Tap **`⚑ Needs Specialist`** right in the bottom action bar (or above **`Comment`** on **`Data`**) and tap a quick tag (e.g. `+ Damaged`, `+ Mold / Pest`, `+ Mixed Specimen`). Marking Reviewed produces calm teal **`[REV+NOTE]`**, keeping it out of the default trainee desk queue so specialists can filter for it directly.
* **Not sure what a badge, code, or field means?** Tap **`?`** in the top bar anytime to open the **Badges, ICEDIG & Field Reference** or launch the **Phone tutorial…**.

### 3.5. Viewport-Reclaimed Photo Folio
If a specimen has no verified online scan yet, Arbor automatically collapses the empty photo frame into a compact single-line bar, keeping Registration Data and inline problem checkboxes right under your thumb.

### 3.6. Batch Location Registrator
To move a stack of specimen folders to a new cabinet at once:
1. Open **⚙ Settings → Advanced Tools → 📦 Batch Location Registrator**.
2. Set your **Target Location** (Building, Floor, Cabinet, Shelf) — or tap to reuse your active **`Shelf`**.
3. Type the Specimen IDs using the numeric keypad (tap **`123 / ABC`** if you need letters).
4. Tap **Commit Batch Location** to update all listed specimens together (works offline too!).

### 3.7. Gentle Vibration Feedback (Glove Calibration)
Auditing specimens requires looking between physical shelf tags and your phone screen. Gentle vibration feedback confirms every action without needing constant eye contact:
* **Steppers**: Crisp tick on Cabinet/Shelf `−` / `+` clicks.
* **Mark Reviewed**: Double confirmation pulse when marked Reviewed.
* **Flag Problem**: Distinct warning pulse when checking a problem flag.

> **Adjusting Vibration Strength:**  
> Open **⚙ Settings** on your phone to toggle vibration or choose **Light** (bare hands), **Medium** (standard nitrile gloves), or **Strong** (heavy cotton archival gloves), and tap `⚡ Test` to feel it immediately. *(Supported on Android Chrome/Firefox; iOS Safari restricts browser vibration.)*

### 3.8. Accidental Refresh & Tab Closure Guard
If you accidentally swipe down to refresh or swipe backwards to close the browser tab in the vault:
* The application intercepts the gesture and confirms whether you wish to leave if any field is actively being edited.
* Background app switching or phone lock triggers an immediate `pagehide` flush, saving in-flight keystrokes to `localStorage` or the server before the browser pauses.

### 3.9. Touch Gestures (One-Handed Hallway Navigation & Photo Inspection)
* **Horizontal Tab Swipe**: Swipe left or right on any specimen screen to glide effortlessly between **Data ↔ Location ↔ Problems** with one thumb (vertical scrolling stays locked so swipes never misfire).
* **Fullscreen Photo Pinch, Pan, Double-Tap & Arrows**: Tap a specimen photo to open it fullscreen, then **pinch with two fingers** to zoom (`0.8×–4.5×`), **drag with one finger** to pan across tiny handwriting, **double-tap** to jump cleanly between `1.0×` and `2.2×`, or tap `‹` / `›` to step between multiple photos.
* **Swipe-Down Bottom Sheets**: Pull down on the top drag handle of the **Set Shelf** or **Stored as** sheet to dismiss it naturally with one thumb.

### 3.10. The Phone Tutorial & One-Time Tips
Arbor includes a built-in hands-on **coach card tutorial** that runs directly on your real collection (never modifying data on its own) and survives phone sleep or reloads:
* **Two Versions:**
  * **Trainee (5 steps):** For users who completed Desktop Part 1 — walks through `Set Shelf → search → how Data · Location · Problems fit together → Save to Shelf & Mark Reviewed → ready`.
  * **Helper (4 steps):** Shorter version for someone helping out for a day.
* **One-Time Contextual Tips:** After you finish the core routine, Arbor shows brief one-time tips the very first time you open the **`Problems`** tab, see an actionable flagged field, open the ICEDIG sheet (Trainee), toggle **Needs Specialist**, or mark an object `[REV+ERR]`.
* **Replay or Reset Anytime:** Open **⚙ Settings → Phone tutorial** on your phone to start either tutorial, toggle tips on/off, or reset seen tips.

---

## 4. Blank or Unreadable Labels (Standard Codes)

When transcribing damaged, faded, or incomplete historical labels (with **no** conflicting older catalog books), **tap the field value on `Data`** (or tap **`ICEDIG ▾`** on **`Problems`**) to pick a standard ICEDIG marker:

| Marker String | Standard Meaning |
| :--- | :--- |
| `unknown:missing` | Information was omitted on the physical label. |
| `unknown:indecipherable` | Text is physically illegible, damaged, or torn. |
| `unknown:undigitized` | Information was skipped during initial digitization. |
| `withheld` | Data withheld due to conservation or legal sensitivity. |

> [!TIP]
> **In-App Quick Reference**: Tap **`?`** in the mobile header anytime to view all **Status Badges**, the **3-Way Problem Rule**, **ICEDIG codes**, and **Field Explanations** directly on your phone.

---

## 5. Ending the Session & Auto-Save Options

### Saving During or After Your Shift
All edits synced from your phone are protected in workstation memory (RAM) and by desktop background autosave (`.autosave.json`). You also have three direct ways to save to Excel:

1. **Save Anytime (`💾 Save Workbook Now`)**: Click **`💾 Save Workbook Now`** directly inside the Mobile Companion window to write your Excel workbook to disk immediately without stopping the phone session.
2. **Wrap-Up Dialog on Stop (Default — `Auto-save: OFF`)**:
   * When you click **🔴 End Mobile Session**, Arbor shows a calm wrap-up dialog (**"All Your Phone Work Is Now in Arbor!"**) reminding you that every phone update is already loaded on your desk computer, with one-click buttons to **`💾 Save File Now (Ctrl+S)`**, **`🔍 Filter (Ctrl+G)`**, or **`❓ Help & Tutorials`**.
3. **Silent Auto-Save (`Auto-save: ON`)**:
   * Automatically persists in-memory edits to disk the moment the server is stopped, without prompting.
   * **Quick Toggle**: Click the `[ ⏸️ Auto-save on stop: OFF ]` / `[ 💾 Auto-save on stop: ON ]` pill directly in the Mobile Companion window at any time to switch modes, or configure it permanently in Desktop **Settings ▾ General ▾ Autosave & Storage**.

---

## 6. Helping Out for a Day (Quick Routine)

Just helping in the collection today? You don't need to learn Desktop Arbor — scan the QR code, pick **"I'm new / helping out today"** (or start the **Helper tutorial** in **⚙ Settings**), and follow this 5-step loop:

1. **Set Shelf:** Standing at a cabinet? Tap **`Set Shelf`** at the top of the list and pick your Building, Floor, Cabinet, and Shelf. Update it whenever you move to a new shelf.
2. **Search:** Pick up a physical object and type its number into the search bar.
3. **Check:** Compare the screen with the real object:
   * Something wrong on a field? Tick the checkbox next to that field on **`Data`**.
   * See a number on **`Problems`**? Open it and tap **`Apply`** on the value that matches the label in your hand — **not sure? Leave it.**
   * Physical damage, mold/pest, or mixed specimen? Tap **`⚑ Needs Specialist`** in the bottom bar and tap a quick tag under **Comment**.
4. **Save to Shelf:** Tap **`📍 Save to Cab XX · Sh YY`** (has a 5-second `↩ Undo` if you tap by mistake).
5. **Mark Reviewed:** Tap **`✓ Mark Reviewed`**, then pick up the next object. Anything you left flagged will be checked at the desk by the main worker later.


