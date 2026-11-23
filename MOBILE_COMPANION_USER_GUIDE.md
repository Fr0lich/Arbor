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
* **First-Time 3-Step Guide & `?` Field Guide**: By default, the desktop Phone Connector has **"Launch with mobile companion tutorial for first-time users"** checked ON so new phone users automatically see a quick 3-slide visual guide (with a **Skip** button). Experienced staff can uncheck this option on the desktop launch screen anytime. Even when disabled, you can always tap **`?`** in the phone's top bar to open **"What the Fields Mean"** or replay the 3-Step Guide from **`⚙ Settings`**.

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

### 3.2. The 1-Tap Armed Target Shelf & Loaned Out Toggle
Opening a specimen **never** overwrites its coordinates automatically — so mistyping a number (like `#101` instead of `#1001`) can never corrupt another record.
1. **Set Your Floor, Cabinet & Shelf Once**: Pick the Building, **Floor** (`-2` to `4`), Cabinet, and Shelf you are standing in front of. Arbor arms that shelf as your active target.
2. **1-Tap Stamping**: On every next box from that shelf, a green thumb banner appears right under the plant name:
   `⚡ Armed Target: Fl 1 · Cab 21 · Sh 01  [ Stamp Target ]`
3. Tap **Stamp Target** once to assign all coordinates in a single tap! (If a specimen already belongs to a different cabinet, the button turns amber **`⚠️ Relocate to Cab 21`** so you never relocate a specimen by accident.)
4. **Lending Objects Out**: Need to borrow or loan out a specimen? Switch to the **Location** tab and toggle **`Loaned Out`** directly from your phone.

### 3.3. Non-Coercive Review Safeguard
If you tap **`✓ Mark Reviewed`** on a specimen that has no Storage Location yet while a shelf is armed, Arbor politely asks:
* **`✓ Yes, Stamp to Target & Review`**: Assigns your armed shelf and marks the specimen Reviewed.
* **`✕ No, Keep Location & Review`**: Saves your edits, notes, and problem flags and marks Reviewed **without changing its location**.

### 3.4. Physical Review Rule & Flagging Issues (`REV + [N] ISSUES`)
* **Only tap `✓ Mark Reviewed` once you have physically checked the object.**
* Found a bent display, crushed box, unreadable 19th-century handwriting, or a confusing plant name?
  * Check **`Other Issue`** (or the relevant issue flag), optionally jot a short note in **`Comment`** (e.g. `"Bent display"`), and **still tap `✓ Mark Reviewed`**.
  * **It is completely okay if you cannot solve a problem in the hallway.** The amber **`REV + 1 ISSUE`** badge confirms you physically held the object and verified its shelf while safely queueing the question for someone else to look at later on the office computer (**`🎯 Hallway Follow-Up (REV+ERR)`**).
* **Outdated Plant Names (`Genus` & `Species`)**: Sometimes the scientific name printed on an old box is outdated or a synonym. Just type what is written on the physical box label — it can be updated automatically later using the **GBIF Name Check** tool on the desktop program.
* **Not sure what a field means?** Tap **`?`** in the top bar anytime to open **What the Fields Mean** (explaining every field, including `Author` vs. `Collector`, right on your phone).

### 3.5. Viewport-Reclaimed Photo Folio
If a specimen has no verified online scan yet, Arbor automatically collapses the empty photo frame into a compact single-line bar (`📷 Scan: None verified online`), keeping metadata and problem checkboxes right under your thumb.

### 3.6. Batch Location Registrator
To move a stack of specimen folders to a new cabinet at once:
1. Tap **📦 Batch Relocation** in the header toolbar.
2. Set your **Target Location** (Building, Floor, Cabinet, Shelf) — or tap **`⚡ Use Cab XX · Sh XX`** to copy your active Armed Target Shelf in 1 tap.
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
* **Horizontal Tab Swipe**: Swipe left or right on any specimen screen to glide effortlessly between **Details ↔ Location ↔ Problems** with one thumb (vertical scrolling stays locked so swipes never misfire).
* **Fullscreen Photo Pinch, Pan & Double-Tap**: Tap a specimen photo to open it fullscreen, then **pinch with two fingers** to zoom (`0.8×–4.5×`), **drag with one finger** to pan across tiny handwriting, or **double-tap** to jump cleanly between `1.0×` and `2.2×`.
* **Swipe-Down Bottom Sheet**: Pull down on the top drag handle of the Storage Vessel sheet to dismiss it naturally with one thumb.

---

## 4. Blank or Unreadable Labels (Standard Codes)

When transcribing damaged, faded, or incomplete historical labels, use standard ICEDIG markers rather than leaving ambiguous blank fields:

| Marker String | Standard Meaning |
| :--- | :--- |
| `unknown:missing` | Information was omitted on the physical label. |
| `unknown:indecipherable` | Text is physically illegible, damaged, or torn. |
| `unknown:undigitized` | Information was skipped during initial digitization. |
| `withheld` | Data withheld due to conservation or legal sensitivity. |

> [!TIP]
> **In-App Cheat Sheet**: Tap the **⚙ Settings** icon in the mobile header anytime to view the ICEDIG quick-reference table directly on your phone.

---

## 5. Ending the Session & Auto-Save Options

### Saving During or After Your Shift
All edits synced from your phone are protected in workstation memory (RAM) and by desktop background autosave (`.autosave.json`). You also have three direct ways to save to Excel:

1. **Save Anytime (`💾 Save Workbook Now`)**: Click **`💾 Save Workbook Now`** directly inside the Mobile Companion window to write your Excel workbook to disk immediately without stopping the phone session.
2. **Prompt to Save on Stop (Default — `Auto-save: OFF`)**:
   * When you click **🔴 End Mobile Session** or close the launch dialog with unsaved edits, Arbor prompts you:
     > *"Mobile session ended with unsaved changes in memory. Save the workbook to disk now?"*
   * Clicking **Yes** automatically executes a background asynchronous save, preventing accidental loss if you step away or close Arbor.
3. **Silent Auto-Save (`Auto-save: ON`)**:
   * Automatically persists in-memory edits to disk the moment the server is stopped, without prompting.
   * **Quick Toggle**: Click the `[ ⏸️ Auto-save on stop: OFF ]` / `[ 💾 Auto-save on stop: ON ]` pill directly in the Mobile Companion window at any time to switch modes, or configure it permanently in Desktop **Settings ▾ General ▾ Autosave & Storage**.

