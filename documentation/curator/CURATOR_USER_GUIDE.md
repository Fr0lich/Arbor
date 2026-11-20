# Arbor Herbarium Curation Suite — Trainee Work Manual
**A Friendly, Plain-Language Guide for Museum Assistants, Interns, and Work-Placement Trainees**

---

## 📖 Welcome to Your New Curation Assistant

Welcome to the team! As a museum assistant, work-placement intern, or collection volunteer, your role is the heart of the herbarium: you help preserve biological history by making sure our physical plant specimens match our digital records.

This manual was written for you. You do not need any computer science experience or advanced botanical background to use Arbor. Arbor is designed to make auditing physical boxes, paper sheets, and handwritten labels fast, accurate, and comfortable.

---

## 📑 Table of Contents
1. [Chapter 1: Welcome to Arbor & Your Daily Purpose](#chapter-1-welcome-to-arbor--your-daily-purpose)
2. [Chapter 2: The Three Main Screen Areas](#chapter-2-the-three-main-screen-areas)
3. [Chapter 3: The 5-Step Daily Curation Routine](#chapter-3-the-5-step-daily-curation-routine)
4. [Chapter 4: What the Status Badges Mean](#chapter-4-what-the-status-badges-mean)
5. [Chapter 5: Looking at the Excel Spreadsheet (The Tab-by-Tab Guide)](#chapter-5-looking-at-the-excel-spreadsheet-the-tab-by-tab-guide)
6. [Chapter 6: Helpful Keyboard Shortcuts (Rest Your Mouse Hand)](#chapter-6-helpful-keyboard-shortcuts-rest-your-mouse-hand)
7. [Chapter 7: Changing the View (If Text Is Too Small or Crowded)](#chapter-7-changing-the-view-if-text-is-too-small-or-crowded)
8. [Chapter 8: Working with Specimen Photos](#chapter-8-working-with-specimen-photos)
9. [Chapter 9: Using the Mobile Companion in Collection Aisles](#chapter-9-using-the-mobile-companion-in-collection-aisles)
10. [Chapter 10: "Don't Panic!" Troubleshooting Guide](#chapter-10-dont-panic-troubleshooting-guide)

---

## Chapter 1: Welcome to Arbor & Your Daily Purpose

### The Digital Filing Cabinet
Think of Arbor as a visual assistant sitting on top of an ordinary Microsoft Excel workbook (`.xlsx`). 

Instead of forcing you to scroll through hundreds of wide columns and thousands of tiny cells in Excel, Arbor presents each physical specimen as a clean, easy-to-read card. When you make a change or click a button in Arbor, it quietly updates the real Excel spreadsheet on your computer. Nothing is hidden, and there are no complicated database servers running in the background.

### What Your Job Involves
During your shift, you will typically work through a batch of physical plant folders or high-resolution photos. Your daily goal is simple:
1. **Check the plant label**: Compare the typed text on the screen with the physical label on the paper sheet or photograph.
2. **Verify where it lives**: Confirm that the physical cabinet number and shelf number match the museum records.
3. **Flag mistakes**: If a name is misspelled, a label is illegible, or a box is misplaced, check the appropriate problem box.
4. **Mark it done**: Click **Mark Reviewed** (or press `Ctrl+Enter`) to give the specimen a green checkmark and move to the next sheet.

> **In the Excel Spreadsheet**: When you open your collection file in Arbor, Arbor reads the `Registration` and `Observation` sheets. Everything you see on screen reflects the exact data stored in those spreadsheet rows.

---

## Chapter 2: The Three Main Screen Areas

When you open Arbor, the workspace is arranged into three clean vertical columns designed to keep your eyes moving naturally from left to right:

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│     1. LEFT COLUMN      │    2. CENTER COLUMN     │     3. RIGHT COLUMN     │
│   "Your Task List"      │  "Label Info & Storage" │    "Specimen Photos"    │
│                         │                         │                         │
│ • Specimen Directory    │ • Plant name & Family   │ • High-resolution scans │
│ • Accession ID cards    │ • Collector & Date      │ • Zoom, pan, and rotate │
│ • Status badges (Green, │ • Cabinet & Shelf locs  │ • Multi-photo gallery   │
│   Red, Amber, Gray)     │ • Problem checkboxes    │                         │
│ • Fast search bar       │ • [✓ MARK AS REVIEWED]  │                         │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

### 1. The Left Column: "Your Task List" (Specimen Directory)
* **What it is**: A vertical scroll of specimen cards representing every plant in your collection.
* **Top Search Bar**: Press `Ctrl+F` and start typing any ID number (e.g. `1042`) or plant name to jump straight to that card.
* **Card Information**: Each card displays the Specimen ID in bold, the scientific plant name, and a single colored status badge showing whether the plant is verified or needs attention.
* **Hiding the Sidebar**: If you need more room on a small laptop screen, press `Ctrl+O` or `F6` to smoothly collapse or expand this list.

### 2. The Center Column: "The Label Information & Storage Location"
* **Registration Form**: Displays the plant's scientific name (Genus, Species, Author), Family, Collector, Collection Date, and Collection Place.
* **Storage Location**: Shows where the plant physically lives in the herbarium (Building, Floor, Cabinet, Shelf, and Box Type).
* **Problem Checkboxes**: A set of checkboxes (e.g. *Genus Problem*, *Label Problem*, *Box Mismatch*) used to report issues.
* **The Big Green Button**: The prominent **✓ MARK AS REVIEWED** button at the top of this panel stamps your verification into the record.

### 3. The Right Column: "Specimen Photos"
* **High-Resolution Viewer**: Displays museum scans and photographs of the active specimen.
* **Image Toolbar**: Rotate upside-down sheets (`Alt+R`), zoom in to inspect faint pencil handwriting (`Ctrl++` / `Ctrl+-`), or reset the view (`Ctrl+0`).
* **Multi-Photo Dots**: If a specimen has multiple photos, click the thumbnail dots or press `Shift+Left` / `Shift+Right` to flip between them.

---

## Chapter 3: The 5-Step Daily Curation Routine

To help you work smoothly without mental fatigue, follow this 5-step rhythm for every specimen:

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│ 1. SELECT│ ──> │2. INSPECT│ ──> │ 3. FLAG IF   │ ──> │ 4. MARK DONE │ ──> │ 5. SAVE  │
│          │     │          │     │    WRONG     │     │   IF CORRECT │     │   WORK   │
│ Down Key │     │ Label vs │     │ Spacebar on  │     │ Ctrl + Enter │     │ Ctrl + S │
│ or Click │     │ Screen   │     │ Problem Box  │     │ (Turns Green)│     │ Hourly   │
└──────────┘     └──────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Step 1: Select Your Specimen
Click any card in the left list, or simply press the `Down Arrow` key on your keyboard to advance down the list one card at a time.

### Step 2: Inspect the Physical Sheet or Photo
Look at the photograph on the right and compare it with the typed fields in the center:
* Is the botanical name spelled correctly?
* Is the collector's name accurate?
* Does the accession number on the paper label match the ID at the top of the screen?

### Step 3: Flag Any Problems (Or Fix Obvious Typos)
* If there is an obvious typing error, click inside the box and fix it.
* If something is wrong, illegible, or missing, press `Space` to check the corresponding problem box (e.g. *Collector_Problem*).
* If handwriting cannot be read at all, press `Ctrl+Shift+I` to insert the international missing marker `?i` (*Indecipherable*).

### Step 4: Mark as Reviewed
* If the specimen details are confirmed and its storage location verified, press **`Ctrl + Enter`** (or click the green **✓ Mark as Reviewed** button).
* The card turns crisp herb-green (`[ REV ]`), Arbor records your verification timestamp, and the cursor automatically steps down to the next plant!

### Step 5: Save Your Work to Excel
Before heading to lunch, taking a break, or ending your shift, press `Ctrl + S` to save all your work.
> **In the Excel Spreadsheet**: Arbor writes all pending updates directly to the `.xlsx` file on your hard drive.

---

## Chapter 4: What the Status Badges Mean

To prevent visual confusion, Arbor uses a strict **single-badge discipline**: each specimen card displays at most **one** high-contrast priority badge telling you the single most important action required.

| Status Badge | Badge Color | What It Means in Plain Language | Action Needed | What It Means in Excel (`Observation` Sheet) |
| :--- | :--- | :--- | :--- | :--- |
| `[ REV ]` | **Herb Green**<br>(`#3a7d44`) | **Reviewed & Verified**<br>The specimen has been thoroughly checked and confirmed correct. | None! It's finished. Move to the next sheet. | `Reviewed = TRUE`<br>(All problem columns are `FALSE` or blank) |
| `[ REV+ERR ]` | **Ochre Gold**<br>(`#F57C00`) | **Reviewed with Known Issue**<br>You checked the sheet, but an unresolvable issue was intentionally noted. | None. Supervisor knows an issue exists on this verified sheet. | `Reviewed = TRUE`<br>AND at least one problem flag is `TRUE` |
| `[ TAX ]` | **Coral Red**<br>(`#c93a40`) | **Plant Name Issue**<br>The scientific name, genus, species, or author citation is misspelled or uncertain. | Check the label spelling or click GBIF Verify in the toolbar. | `Genus_Problem = TRUE`, `Species_Problem = TRUE`, or `Family_Problem = TRUE` |
| `[ PROV ]` | **Warm Amber**<br>(`#d9a036`) | **Origin / Collector Issue**<br>The collector name, collection date, or locality is missing or questioned. | Check the label handwriting or insert a missing data marker (`?m`). | `Collector_Problem = TRUE`, `Collection_Date_Problem = TRUE`, etc. |
| `[ BOX ]` | **Earth Brown**<br>(`#795548`) | **Storage Box Issue**<br>The physical box label, folder housing, or storage location is mismatched. | Verify which cabinet/shelf the box sits on and update the location. | `Box_Label_Problem = TRUE` |
| `[ IMG ]` | **Ocean Blue**<br>(`#0284c7`) | **Photo Issue**<br>The photograph is missing, unlinked, blurry, or belongs to another plant. | Confirm the photo link or notify your supervisor to rescan. | `Images_Problem = TRUE` or `Images_Missing = TRUE` |
| `[ CFCT ]` | **Slate Blue**<br>(`#4a7b9d`) | **Ledger Conflict**<br>An old historical handwritten ledger book disagrees with modern data. | Press `Ctrl+H` to open the Conflict Resolver and compare sources. | Conflict detected against loaded Historical Books |
| `[ ERR ]` | **Coral Red**<br>(`#c93a40`) | **General Error**<br>An uncategorized issue or general quality note was flagged. | Read the Notes field to see what previous curators wrote. | `Other_problem = TRUE` |
| `[ UNREV ]` | **Cool Gray**<br>(`#757d77`) | **Pending Review**<br>A fresh or untouched record waiting for your inspection. | Inspect the specimen, verify fields, and click Mark Reviewed. | `Reviewed = FALSE` (or empty) |

---

## Chapter 5: Looking at the Excel Spreadsheet (The Tab-by-Tab Guide)

One of Arbor's greatest strengths is transparency: it stores everything in standard Microsoft Excel files (`.xlsx`). You can open the spreadsheet in Excel at any time to see your work.

### The Golden Rule: Close Excel Before Opening Arbor
> ⚠️ **Important Safety Rule**: Windows locks Excel files when Microsoft Excel has them open. Always **close Microsoft Excel** before launching or saving in Arbor. If you forget, Arbor will pop up a gentle reminder saying the file is in use.

### The Golden Key: `ObjectID`
In every sheet inside the Excel file, the very first column is **`ObjectID`** (e.g. `1001`, `1042`, or `O-V-0042`). This accession number is the golden key that links all the sheets together.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ARBOR EXCEL WORKBOOK STRUCTURE                        │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────┤
│ 1. Registration │ 2. Observation  │ 3. Photo        │ 4. Unvalidated_source │
│ (Catalog Data)  │ (Your Curation) │ (Image Links)   │ (Illegible Notes)     │
│                 │                 │                 │                       │
│ • ObjectID      │ • ObjectID      │ • ObjectID      │ • ObjectID            │
│ • Genus         │ • Reviewed      │ • Online photo1 │ • Field_Name          │
│ • Species       │ • ReviewedAt    │ • Online photo2 │ • Unvalidated_Comment │
│ • Collector     │ • 11 Problems   │ • Local path    │                       │
│ • Date & Place  │ • Cabinet/Shelf │                 │                       │
└─────────────────┴─────────────────┴─────────────────┴───────────────────────┘
```

### The 4 Core Sheets Explained:

#### 1. `Registration` (The Master Specimen Catalog)
Contains standard botanical catalog data:
* `ObjectID`: Accession number printed on the label.
* `Genus`, `Species`, `Author`: The scientific botanical name.
* `Family`: The broader plant family (e.g. *Pinaceae*, *Asteraceae*).
* `Collector`, `Collection Date`, `Collection Place`: When, where, and by whom the specimen was collected.

#### 2. `Observation` (Your Curation Record)
Where Arbor records your physical audit work:
* `Reviewed`: Shows `TRUE` when marked reviewed, or `FALSE` when pending.
* `ReviewedBy`: The user name stamped when reviewed.
* `ReviewedAt`: Exact timestamp of review.
* Problem Columns: 11 boolean flags (`Genus_Problem`, `Box_Label_Problem`, etc.) showing `TRUE` if flagged.
* Storage Columns: `Building`, `Floor`, `Cabinet`, `Shelf`, and `Stored as`.

#### 3. `Photo` (Archival Image Links)
Tracks local file paths and remote URLs for specimen scans.

#### 4. `Unvalidated_source` (Historical Notes)
Stores transcription notes or questions about faded handwriting for senior curator review.

---

## Chapter 6: Helpful Keyboard Shortcuts (Rest Your Mouse Hand)

Arbor is designed so you rarely have to reach for your mouse:

```
┌───────────────────────────┬─────────────────────────────────────────────────┐
│ Primary Action            │ Shortcut                                        │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Mark Reviewed & Advance   │ [Ctrl] + [Enter] or [Ctrl] + [R]                │
│ Toggle Problem Checkbox   │ [Spacebar] on highlighted checkbox              │
│ Save Active Workbook      │ [Ctrl] + [S]                                    │
│ Move Down / Up Cards      │ [Down Arrow] / [Up Arrow]                       │
│ Jump to Next Problem      │ [Ctrl] + [Down Arrow]                           │
│ Fast Search Bar           │ [Ctrl] + [F]                                    │
│ Command Palette (Omni)    │ [Ctrl] + [K]                                    │
│ Filter Objects Menu       │ [Ctrl] + [Shift] + [F] or [Ctrl] + [G]          │
│ Jump to Form Fields       │ [Ctrl] + [E] or [Ctrl] + [I]                    │
│ Jump to Storage Location  │ [Ctrl] + [L] or [F4]                            │
│ Undo / Redo Typing        │ [Ctrl] + [Z] / [Ctrl] + [Y]                     │
│ Rotate Photo Scan         │ [Alt] + [R]                                     │
│ Zoom Photo In / Out       │ [Ctrl] + [+] / [-] (or Mouse Wheel)             │
│ Reset Photo View          │ [Ctrl] + [0]                                    │
│ Open Shortcuts HUD        │ [F1]                                            │
└───────────────────────────┴─────────────────────────────────────────────────┘
```

---

## Chapter 7: Changing the View (If Text Is Too Small or Crowded)

Trainees work on different computer screens (13-inch laptops vs wide 27-inch desktop monitors). Arbor provides 4 one-click layout profiles:

```
┌─────────────────┬─────────────────┬─────────────────┬───────────────────────┐
│ 1. Standard     │ 2. Compact      │ 3. Full Details │ 4. Minimalist         │
│ (78px height)   │ (64px height)   │ (92px height)   │ (Compact & Lean)      │
│                 │                 │                 │                       │
│ • Everyday view │ • Laptop dense  │ • Large text    │ • Pure ID & taxon     │
│ • Balanced info │ • 15+ cards     │ • Author names  │ • No badges / chips   │
│ • ID + name +   │ • Fast checking │ • Full storage  │ • Distraction-free    │
│   status badge  │   through boxes │   location line │   data transcription  │
└─────────────────┴─────────────────┴─────────────────┴───────────────────────┘
```

### How to Switch Profiles:
1. Press **`Ctrl + K`** and type `Card View`.
2. Select your preferred layout:
   * **`Card View: Standard (78px)`**: The default balanced view (~12 cards visible).
   * **`Card View: Compact (64px)`**: High-density view showing 15+ cards on screen at once.
   * **`Card View: Full Details (92px)`**: Expanded research view showing botanical authors (e.g. *L.*) and full Building/Floor/Cabinet/Shelf coordinates on every card.
   * **`Card View: Minimalist`**: Clean, bare view showing strictly the ID number and plant name without extra badges or chips.
3. You can also adjust profiles in **`Settings ⚙` $\rightarrow$ `Appearance` $\rightarrow$ `Directory Card Profiles`**, where an interactive live preview shows you how cards will look before you apply them.

### Toggling Workspace Panels
If you want to maximize screen space for inspecting photos or typing notes, use the function keys:
* **`[F6]`**: Toggle the Specimen Directory (left column) on or off.
* **`[F7]`**: Toggle the Registration Form (center column) on or off.
* **`[F8]`**: Toggle the Specimen Photos Viewport (right column) on or off.

---

## Chapter 8: Working with Specimen Photos

High-resolution scans let you inspect plant hairs, seeds, and faded ink labels without touching fragile 100-year-old paper sheets:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SPECIMEN IMAGE VIEWPORT CONTROLS                         │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Action                   │ How to Do It                                     │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ Rotate 90° Clockwise     │ Press [Alt] + [R] or click ↻ in the toolbar       │
│ Zoom In / Zoom Out       │ Press [Ctrl] + [+] / [-], or roll your Mouse Wheel│
│ Reset Zoom to Full Page  │ Press [Ctrl] + [0] or click ↺ in the toolbar     │
│ Pan Across Large Photo   │ Click and drag with your left mouse button       │
│ Browse Multiple Photos   │ Press [Shift] + [Left] / [Right], or [Ctrl] + [B]│
│ Detached Full-Res Popout │ Double-click anywhere on the image canvas        │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### The Detached High-Resolution Viewer
For very difficult handwriting or tiny pressed leaves, **double-click** the image. 
* A detached window (`ZoomableImagePopup`) appears on top of your workspace.
* Use your mouse wheel to zoom up to 500% into the scan.
* Click and drag to pan across the label.
* Press `Escape` to close the popout and return to your form.

---

## Chapter 9: Using the Mobile Companion in Collection Aisles

When auditing physical specimens walking down vault corridors or glass cabinet aisles, you do not need to carry a heavy laptop or balance a keyboard on your knees. Arbor includes a built-in **Mobile Companion** that works on any smartphone or tablet browser:

```
┌────────────────────────┐      Local Wi-Fi      ┌────────────────────────┐
│  DESKTOP WORKSTATION   │ ───────────────────>  │  PHONE / TABLET BROWSER│
│                        │    Secure PIN Code    │                        │
│ • Runs Arbor           │                       │ • Step through records │
│ • Shows QR Code & PIN  │                       │ • Search-first audit   │
│ • Holds Excel workbook │                       │ • Armed shelf stamping │
└────────────────────────┘                       └────────────────────────┘
```

### How to Connect in 4 Easy Steps:
1. **Launch the Server**: In Arbor on your desktop computer, click the **`📱 MOBILE`** menu at the top, or press `Ctrl+K` and type `Mobile Companion`.
2. **Scan the Screen**: A window appears displaying a QR code, a web address, and a 4-digit security PIN.
3. **Open on Your Phone**: Scan the QR code with your phone camera, or type the address into your phone's browser (Safari, Chrome, or Firefox).
4. **Enter Your PIN**: Enter the 4-digit PIN shown on your desktop screen to start your session.

---

### The Real-World Hallway Audit Workflow

In a real museum vault, historical records rarely know which cabinet or shelf an object lives in ahead of time. You will typically work cabinet by cabinet, pulling physical boxes or folders:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. PULL OBJECT  │ ──> │ 2. FAST LOOKUP  │ ──> │ 3. STAMP SHELF  │ ──> │ 4. MARK REVIEWED│
│ Read Accession  │     │ Numeric keypad  │     │ 1-tap on Armed  │     │ Done or Flags   │
│ Number on label │     │ auto-normalizes │     │ Shelf Banner    │     │ Preserved       │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### 1. Fast Number Lookup (Search-First)
* Tap the search bar at the top of your phone screen. Arbor automatically brings up the **numeric keypad** for fast typing (with a `[Aa / 123]` button to switch to letters if your museum uses prefixes).
* **Automatic Zero Normalization**: If your physical specimen label says `#001` or `#1`, simply type `1` or `001`. Arbor recognizes both formats instantly.
* When you finish reviewing an object and tap `< Back`, Arbor automatically clears and focuses the search box so you can immediately type the next specimen number!

#### 2. The Armed Target Shelf (Auditing 30–50 Specimens at Once)
When you open a cabinet, you will usually inspect dozens of consecutive specimens on the same shelf before moving to the next. Typing the same Building, Floor, Cabinet, and Shelf numbers fifty times would be slow and cause typos.

* **Set the Shelf Once**: On your first specimen, set the correct Cabinet (e.g. `21`) and Shelf (e.g. `01`). Arbor immediately **arms this location as your active target shelf**.
* **1-Tap Stamping**: When you look up the next specimen, a prominent thumb banner appears directly under the plant title:
  `📍 Armed Target: Cab 21 › Sh 01 [Stamp to This Shelf]`
* Simply tap the banner to instantly assign the coordinates!

#### 3. The Non-Coercive Review Safeguard
To keep you moving fast, if you tap **`[ ✓ Mark Reviewed ]`** on a specimen that has no location recorded yet while a shelf is armed, Arbor will politely ask:
> *"Stamp to Armed Shelf 21 & Mark Reviewed?"*

You are given two completely safe choices:
1. **`✓ Yes, Stamp to Target & Review`**: Assigns Cabinet 21, Shelf 01 and marks the specimen as reviewed.
2. **`✕ No, Keep Location & Review`**: **100% safe!** If you found the specimen in a temporary sorting box or don't want to change its location, choosing "No" saves all your edits, problem checkboxes, and notes, and marks the specimen as reviewed **without altering its location**.
3. **`Cancel`**: Returns to the form without saving.

#### 4. Flagging Problems While Marking Reviewed (`REV + [N] ISSUES`)
What if you pull a specimen and discover physical damage (e.g., a crushed box), an illegible handwritten label, or a conflicting year?
* **Path A (Fix on the spot)**: If the physical label in your hand resolves a historical contradiction (e.g., the label says `1998` but a book noted `2008`), tap the suggestion from the Historical Data picker to fix it immediately.
* **Path B (Flag for desktop triage)**: If the issue requires desktop research or physical box repair, check the appropriate problem box (e.g. `Box / Label Problem` or `Species Problem`), **BUT STILL MARK THE OBJECT AS REVIEWED**.
* **Why this is a success**: Marking it reviewed stamps the physical coordinates and verifies that a human held the object. The status badge will display **`REV + [N] ISSUES` (Amber)**. This tells the entire team: *"This plant was physically found and its location is confirmed, but there is a note queued for office curation."*

#### 5. Viewport-Reclaimed Photo Folio
If an archival photo scan has not yet been uploaded for the specimen, Arbor automatically collapses the empty 192px photo box into a compact 28px single-line bar (`📷 Scan: None verified online`). This reclaims phone screen space so the plant information and problem checkboxes are right under your thumb without endless scrolling!

---

### Returning to Your Desk: Desktop Hallway Follow-Up

When you finish your aisle audit and return to your computer:
1. Click **🔴 End Mobile Session** on your desktop screen and confirm **Yes** to write your changes to the Excel file.
2. Press **`Ctrl + Shift + F`** (or click the Filter button) to open the Filter Objects dialog.
3. Click the dedicated preset button:
   `🎯 Hallway Follow-Up (REV+ERR)`
4. Arbor immediately filters your Specimen Directory to show every plant you handled in the vault that has a pending question or damage flag (`Reviewed = Has` and `Any_Problem = Has`), ready for office research!

---

### Ending Your Mobile Session & Offline Vault Mode
* **Works Completely Offline**: If your museum vault has thick concrete walls with no Wi-Fi, the Mobile Companion continues working in offline mode. It securely holds your updates in phone storage and uploads them automatically the moment you walk back into Wi-Fi range.
* When you return to your desk, click **🔴 End Mobile Session** on your computer. Arbor will check for any updates made on your phone and ask to save your changes to the Excel workbook.

---

## Chapter 10: "Don't Panic!" Troubleshooting Guide

If something unexpected happens, do not panic! Arbor is engineered with multiple safety nets to protect your work:

### 1. "What does the yellow dot mean?"
* **What you see**: A small amber dot (`● Unsaved`) appears next to the specimen ID number in the top bar.
* **What it means**: You have typed edits or changed a problem box, but have not yet saved to disk.
* **The fix**: Press **`Ctrl + S`** to save your changes. The yellow dot will disappear.

### 2. "I accidentally marked a specimen as reviewed!"
* **What happened**: You pressed `Ctrl + Enter` by mistake on a sheet that is not finished.
* **The fix**: Simply click the **✓ MARK AS REVIEWED** button again (or press `Ctrl + Enter` a second time). The checkmark will turn off, the green badge will revert to cool gray `[ UNREV ]`, and the record is marked unreviewed again.

### 3. "The computer says: 'File is locked by another program'"
* **What happened**: Microsoft Excel is currently open on your computer with the same `.xlsx` file.
* **The fix**: 
  1. Switch to Microsoft Excel and close the workbook window.
  2. Return to Arbor and press **`Ctrl + S`**. Arbor will now save cleanly.

### 4. "I made a big mistake or deleted something by accident!"
* **Don't panic!** Arbor automatically creates timestamped safety backup copies in a hidden `.arbor_backups/` folder inside your project directory before every major operation.
* **The fix**: Notify your supervisor. They can restore your workbook to the exact state it was in 10 minutes ago with zero data loss.

### 5. "A text box is glowing with a yellow background"
* **What it means**: This is a helpful visual reminder! A problem checkbox is currently active for that specific field (for example, if `Species_Problem` is checked, the Species box glows yellow).
* **The fix**: Double-check the text on the physical label. If you resolve the issue and uncheck the problem box, the yellow highlight disappears.

### 6. "The photograph is missing or showing a black box"
* **The fix**:
  1. Press **`F8`** twice to toggle the photo viewport off and on again.
  2. If the photo was stored on an external USB hard drive, check that the drive cable is securely plugged into your computer.
  3. If the photo is still missing, check the **Images_Problem** checkbox to alert the digitization team.

---

*End of Trainee Work Manual. Happy Curating!*
