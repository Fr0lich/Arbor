# Arbor Mobile Companion — Field & Curator Guide

The **Arbor Mobile Companion** is a dedicated, zero-install mobile web application that turns any smartphone or tablet into a companion terminal for physical specimen auditing in herbarium vaults, compactors, and collection stacks.

---

## 1. Quick Start & Pairing

```
┌────────────────────────────────────────────────────────┐
│ 1. On your Desktop Workstation:                        │
│    Click 📱 MOBILE in the top navigation bar.          │
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

### Pairing Options
* **QR Code**: Open your phone's camera app and tap the link that appears on screen. The secure session link logs you in automatically — no passwords required.
* **Copy Link Button**: Click **📋 Copy** in the desktop pairing window to copy the full URL to your clipboard for instant sharing.
* **4-Digit PIN**: If opening a saved bookmark on your phone, enter the 4-digit PIN displayed on your desktop screen.
* **First-Time 3-Step Guide**: The first time your phone connects, Arbor displays a quick 3-slide visual guide (with a **Skip** button) walking you through searching, 1-tap shelf stamping, and flagging issues. You can replay it anytime from **⚙ Settings → 🎓 3-Step Guide**.

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
> If you lose Wi-Fi behind a steel door, keep auditing normally! All storage coordinates, review checkmarks, and notes stay safely saved on your phone and sync automatically to your desktop the moment Wi-Fi returns.

---

## 3. Hallway Auditing Workflows

### 3.1. Search-First Number Lookup
* **Numeric Keypad Default**: Pull a physical box, read its accession number, and type it in the top search bar. Use the **`[123 / Aa]`** button to switch between numbers and plant names.
* **Automatic Zero & Prefix Handling**: Typing `001`, `1`, or `O-V-1` all find Specimen `#1`. When you tap `< Back` to return to the list, Arbor automatically clears and focuses the search bar for the next box.

### 3.2. The 1-Tap Armed Target Shelf (Auditing 30–50 Boxes at Once)
Opening a specimen **never** overwrites its coordinates automatically — so mistyping a number (like `#101` instead of `#1001`) can never corrupt another record.
1. **Set Your Shelf Once**: Pick the Building, Floor, Cabinet, and Shelf you are standing in front of. Arbor arms that shelf as your active target.
2. **1-Tap Stamping**: On every next box from that shelf, a green thumb banner appears right under the plant name:
   `⚡ Armed Target: Cab 21 · Sh 01  [ Stamp Target ]`
3. Tap **Stamp Target** once to assign all coordinates in a single tap! (If a specimen already belongs to a different cabinet, the button turns amber **`⚠️ Relocate to Cab 21`** so you never relocate a specimen by accident.)

### 3.3. Non-Coercive Review Safeguard
If you tap **`✓ Mark Reviewed`** on a specimen that has no Storage Location yet while a shelf is armed, Arbor politely asks:
* **`✓ Yes, Stamp to Target & Review`**: Assigns your armed shelf and marks the specimen Reviewed.
* **`✕ No, Keep Location & Review`**: Saves your edits, notes, and problem flags and marks Reviewed **without changing its location**.

### 3.4. Flagging Issues While Still Marking Reviewed (`REV + [N] ISSUES`)
Found a crushed box or unreadable 19th-century handwriting?
* Check the problem box (e.g., `Box_Label_Problem`) and **still tap `✓ Mark Reviewed`**.
* The badge turns amber (**`REV + 1 ISSUE`**). This confirms you physically held the box and verified its shelf while queueing the issue for office desktop follow-up (**`🎯 Hallway Follow-Up (REV+ERR)`**).

### 3.5. Viewport-Reclaimed Photo Folio
If a specimen has no verified online scan yet, Arbor automatically collapses the empty photo frame into a compact single-line bar (`📷 Scan: None verified online`), keeping metadata and problem checkboxes right under your thumb.

### 3.6. Batch Location Registrator
To move a stack of specimen folders to a new cabinet at once:
1. Tap **📦 Batch Relocation** in the header toolbar.
2. Set your **Target Location** (Building, Floor, Cabinet, Shelf).
3. Enter the Specimen IDs into the rapid list.
4. Tap **Commit Batch Location** to update all listed specimens together.

### 3.7. Gentle Vibration Feedback (Glove Calibration)
Auditing specimens requires looking between physical shelf tags and your phone screen. Gentle vibration feedback confirms every action without needing constant eye contact:
* **Steppers**: Crisp tick on Cabinet/Shelf `−` / `+` clicks.
* **Mark Reviewed**: Double confirmation pulse when marked Reviewed.
* **Flag Problem**: Distinct warning pulse when checking a problem flag.

> **Adjusting Vibration Strength:**  
> Open **⚙ Settings** on your phone to toggle vibration or choose **Light** (bare hands), **Medium** (standard nitrile gloves), or **Strong** (heavy cotton archival gloves), and tap `⚡ Test` to feel it immediately. *(Supported on Android Chrome/Firefox; iOS Safari restricts browser vibration.)*

### 3.6. Accidental Refresh & Tab Closure Guard
If you accidentally swipe down to refresh or swipe backwards to close the browser tab in the vault:
* The application intercepts the gesture and confirms whether you wish to leave if any field is actively being edited.
* Background app switching or phone lock triggers an immediate `pagehide` flush, saving in-flight keystrokes to IndexedDB or the server before the browser pauses.

---

## 4. ICEDIG Missing Data Standards

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

### Desktop Auto-Save Preference
By default, all edits synced from your mobile phone are held securely in workstation memory (RAM). When you stop the server, Arbor provides two safe persistence paths:

1. **Prompt to Save (Default — `Auto-save: OFF`)**:
   * When you click **🔴 End Mobile Session** or close the launch dialog with unsaved edits, Arbor prompts you:
     > *"Mobile session ended with unsaved changes in memory. Save the workbook to disk now?"*
   * Clicking **Yes** automatically executes a background asynchronous save (`save_session`), preventing accidental loss if you step away or close Arbor.
2. **Silent Auto-Save (`Auto-save: ON`)**:
   * Automatically persists in-memory edits to disk the moment the server is stopped, without prompting.
   * **Quick Toggle**: You can click the `[ ⏸️ Auto-save on stop: OFF ]` / `[ 💾 Auto-save on stop: ON ]` pill directly in the Mobile Companion launch window at any time to switch modes, or configure it permanently in Desktop **Settings ▾ General ▾ Autosave & Storage**.

