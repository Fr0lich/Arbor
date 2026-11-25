# Arbor Herbarium Curation Suite — Trainee Work Manual
**A Friendly, Plain-Language Guide for Museum Assistants, Interns, and Work-Placement Trainees**

---

## 📖 Welcome to Your New Curation Assistant

Welcome to the team! As a museum assistant, work-placement intern, or collection volunteer, your role is the heart of the herbarium: you help preserve biological history by making sure our physical plant specimens match our digital records.

This manual was written for you. You do not need any computer science experience or advanced botanical background to use Arbor. Arbor is designed to make auditing physical boxes, paper sheets, and handwritten labels fast, accurate, and comfortable.

> 🎓 **New Here? Start with the 2-Part Core Introduction!**  
> Click **`HELP`** in the top bar (or press **`F1`**) to open the **Help Center** and launch **Part 1: Desktop Basics** (~3–4 min, using real sample photos `#110` & `#198` in safe **Practice Mode**), followed by **Part 2: Mobile Companion** (~2 min on your phone). When you are ready for more, explore **Optional & Advanced Tutorials** (*Batch Problem Queue*, *Collections & New Specimens*) or open the **Badges & Reference** tab anytime for a quick lookup. Saving is paused in Practice Mode, so nothing you do can affect real museum files.

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
│   "Your Task List"      │   "Photos & Storage"    │  "Registration & Review"│
│                         │                         │                         │
│ • Specimen Directory    │ • High-resolution scans │ • Plant name & Family   │
│ • Accession ID cards    │ • Zoom, pan, and rotate │ • Collector, Date, Place│
│ • Status badges (Green, │ • Multi-photo gallery   │ • Per-field ⋯ ICEDIG    │
│   Amber, Teal, Gray)    │ • Storage Location      │ • Problem checkboxes &  │
│ • Fast search bar       │   (Cabinet / Shelf)     │   Needs Specialist      │
│                         │   directly below photos │ • [✓ MARK AS REVIEWED]  │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

### 1. The Left Column: "Your Task List" (Specimen Directory)
* **What it is**: A vertical scroll of specimen cards representing every plant in your collection.
* **Top Search Bar**: Press `Ctrl+F` and start typing any ID number (e.g. `1042`) or plant name to jump straight to that card.
* **Card Information**: Each card displays the Specimen ID in bold, the scientific plant name, and a single colored status badge showing whether the plant is verified or needs attention.
* **Hiding the Sidebar**: If you need more room on a small laptop screen, press `Ctrl+O` or `F6` to smoothly collapse or expand this list.

### 2. The Center Column: "Specimen Photos & Storage Location"
* **High-Resolution Viewer**: Displays museum scans and photographs of the active specimen (or a clean Specimen Audit Summary if no photo folder is attached).
* **Image Toolbar**: Rotate upside-down sheets (`Alt+R`), zoom in to inspect faint pencil handwriting (`Ctrl++` / `Ctrl+-`), or reset the view (`Ctrl+0`).
* **Multi-Photo Dots**: If a specimen has multiple photos, click the thumbnail dots or press `Shift+Left` / `Shift+Right` to flip between them.
* **Storage Location (Below Photos)**: Always sits directly beneath the photo pane so you can confirm or edit **Building, Floor, Cabinet, Shelf, Stored as**, and **Loaned Out** (`Ctrl+L` jumps straight here).

### 3. The Right Column: "Registration Data, Problems & Review"
* **The Big Green Button**: The prominent **✓ MARK AS REVIEWED** button at the top stamps your physical verification into the record.
* **Registration Form**: Displays the plant's scientific name (`Genus`, `Species`, `Author`), `Family`, `Collector`, `Collection Date`, `Collection Place`, `Box Label`, and `Comment`. Every editable field has a **`⋯`** button on its right edge for standard ICEDIG missing-data codes.
* **Problem Checkboxes & `Needs Specialist`**: Tick the checkbox next to any field that disagrees with the real object, or check **`Needs Specialist`** right above **`Comment`** for physical damage, pests, or expert botanical questions.

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
Look at the physical object (or its photograph in the center) and compare it with the registered fields on the right:
* Is the botanical name spelled correctly?
* Does the collector's name and collection date match the label? *(Dates use **`DAY.MONTH.YEAR`** with `00` for unknown parts — e.g. 1 August 2015 → `01.08.2015`, August 2015 → `00.08.2015`, or just `1927` if only the year is known.)*
* **Historical Suggestions (`Ctrl+H`)**: If earlier catalog books are loaded and disagree with the current record, a blue **`History: N suggestion(s) · Ctrl+H`** pill appears above the form. Click it to compare sources — remember that older ledgers can be wrong too, so always check them against the physical object.
* Does the physical storage box on your desk match the Cabinet and Shelf listed on screen?

### Step 3: Handle Missing Info, Mismatches, or Damage (The 3-Way Rule)
Arbor separates three different situations so every issue reaches the right person:
1. **Confirmed Blank or Unreadable Label → Use ICEDIG (`⋯` button)**: If the physical label genuinely has no date, collector, or readable ink *(and no older catalog book has a value)*, click the **`⋯`** button on the right edge of that field (or type `?m` / `?i`) to insert `unknown:missing` or `unknown:indecipherable`. Do **not** flag a problem for genuinely missing label info.
2. **Data or Label Mismatch → Tick the Field's Problem Box**: If the real object disagrees with what is on file (for example, the box says Africa while the record says China), tick that field's problem checkbox, or press **`Ctrl+H`** to compare older books in **Problem Resolution**. *(Note: Typing a new value into a flagged field does **not** automatically untick its problem box by default — untick the box once you are confident the fix is verified.)*
3. **Physical Damage or Expert Question → `Needs Specialist` + `Comment`**: For torn/moldy/pest-damaged boxes, mixed specimens, or botanical doubts that need a specialist, check **`Needs Specialist`** (right above **`Comment`**) and write a short note.
> **In the Excel Spreadsheet**: Checking **`Needs Specialist`** writes `TRUE` into `Other_problem` on the `Observation` sheet; field-specific checkboxes write `TRUE` into columns like `Collection_Date_Problem`.

### Step 4: Mark Done After Physical Inspection
**Important Rule**: Only click the big green **✓ MARK AS REVIEWED** button (or press `Ctrl + Enter`) once you have **finished physically inspecting the object** — never just because you fixed a typo from a historical ledger at your desk.
* Clean specimens receive a green **`[ REV ]`** badge; physically checked specimens with an open actionable data error receive an amber **`[ REV+ERR ]`** badge; physically checked specimens with **only `Needs Specialist`** checked receive a calm slate-teal **`[ REV+NOTE ]`** badge.
* By default, **`Auto-next` is OFF** so Arbor stays on the current specimen after you mark it reviewed — press `Down` / `Right` when you are ready for the next card (or tick **Auto-next** if you prefer jumping automatically).
> **In the Excel Spreadsheet**: This writes `TRUE` into the `Reviewed` column on the `Observation` sheet for that specimen's `ObjectID`, timestamps your review time into `ReviewedAt`, and records your username in the `Log` sheet.

### Step 5: Save Your Work
Before heading to lunch, taking a break, or ending your shift, press `Ctrl + S` to save all your work.
> **In the Excel Spreadsheet**: Arbor writes all pending updates directly to the `.xlsx` file on your hard drive.

---

## Chapter 4: What the Status Badges Mean

To prevent visual confusion, Arbor uses a strict **single-badge discipline**: each specimen card displays at most **one** high-contrast priority badge telling you the single most important action required.

| Status Badge | Badge Color | What It Means in Plain Language | Action Needed | What It Means in Excel (`Observation` Sheet) |
| :--- | :--- | :--- | :--- | :--- |
| `[ REV ]` | **Herb Green**<br>(`#3a7d44`) | **Reviewed & Verified**<br>The specimen has been thoroughly checked and confirmed correct. | None! It's finished. Move to the next sheet. | `Reviewed = TRUE`<br>(All problem columns are `FALSE` or blank) |
| `[ REV+ERR ]` | **Ochre Gold**<br>(`#F57C00`) | **Reviewed with Actionable Error**<br>You checked the sheet, but a data/label error remains for desk triage. | Resolve in Office Triage / Historical Conflict Resolver. | `Reviewed = TRUE`<br>AND at least one actionable problem flag is `TRUE` |
| `[ REV+NOTE ]` | **Slate Teal**<br>(`#4a6b7c`) | **Reviewed — Needs Specialist**<br>You checked the sheet; ONLY **`Needs Specialist`** is flagged (never triggered by a plain Comment). | Excluded from default trainee queue; specialists filter for it directly. | `Reviewed = TRUE`<br>AND ONLY `Other_problem = TRUE` |
| `[ NOTE ]` | **Cool Slate**<br>(`#5c6f7e`) | **Pending — Needs Specialist**<br>Unreviewed specimen with ONLY **`Needs Specialist`** checked. | Specialist / conservator follow-up. | `Reviewed = FALSE`<br>AND ONLY `Other_problem = TRUE` |
| `[ TAX ]` | **Coral Red**<br>(`#c93a40`) | **Plant Name Issue**<br>The scientific name, genus, species, or author citation is misspelled or uncertain. | Check the label spelling or open `📜 Old names` (`Ctrl+K → Old Names`). | `Genus_Problem = TRUE`, `Species_Problem = TRUE`, or `Family_Problem = TRUE` |
| `[ PROV ]` | **Warm Amber**<br>(`#d9a036`) | **Origin / Collector Issue**<br>The collector name, collection date, or locality is missing or questioned. | Check the label handwriting or insert an ICEDIG code (`⋯` button / `?m`). | `Collector_Problem = TRUE`, `Collection_Date_Problem = TRUE`, etc. |
| `[ BOX ]` | **Earth Brown**<br>(`#795548`) | **Storage Box Issue**<br>The physical box label, folder housing, or storage location is mismatched. | Verify which cabinet/shelf the box sits on and update the location. | `Box_Label_Problem = TRUE` |
| `[ IMG ]` | **Ocean Blue**<br>(`#0284c7`) | **Photo Issue**<br>The photograph is missing, unlinked, blurry, or belongs to another plant. | Confirm the photo link or notify your supervisor to rescan. | `Images_Problem = TRUE` or `Images_Missing = TRUE` |
| `[ ERR+HIS ]` | **Slate Blue**<br>(`#4a7b9d`) | **Error + Older Books**<br>An unreviewed specimen has an actionable flag AND older catalog books loaded. | Press `Ctrl+H` to open Problem Resolution and compare older books. | Actionable flag `TRUE` + loaded Historical Books |
| `[ CFCT ]` | **Slate Blue**<br>(`#4a7b9d`) | **Catalog Book Conflict**<br>An old historical catalog book disagrees with modern data. | Press `Ctrl+H` to open Problem Resolution and compare sources. | Conflict detected against loaded Historical Books |
| `[ ERR ]` | **Coral Red**<br>(`#c93a40`) | **General Error**<br>An uncategorized actionable error was flagged. | Review the Problems tab for details. | Actionable problem flag is `TRUE` |
| `[ UNREV ]` | **Cool Gray**<br>(`#757d77`) | **Pending Review**<br>A fresh or untouched record waiting for your inspection. | Inspect the specimen, verify fields, and click Mark Reviewed. | `Reviewed = FALSE` (or empty) |

> 💡 **Card Chips & Quick Reference**: Specimen cards may also show small secondary chips: **`LOAN`** (loaned out — `↗ Loaned` on phone), **`UKN`** (has an ICEDIG `unknown:*`/`withheld` code), **`UNVAL`** (has an `Unvalidated_source` draft note), and **`NO PHOTO`** / **`ONLINE`**. Press **`F1`** → **Badges & Reference** anytime for a visual cheat sheet.

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
This sheet contains the permanent historical record of the specimen:
* **`ObjectID`**: The accession number.
* **`Genus` & `Species`**: The scientific botanical name.
* **`Family` & `Author`**: The higher classification and person who named the plant.
* **`Collector` & `Collection Date`**: Who found the plant in the wild and when.
* **`Collection Place`**: The geographic locality where the plant was collected.
* **`UID`**: An 8-character safety fingerprint (e.g. `7921ac45`) created automatically by Arbor to prevent accidental row mix-ups.

#### 2. `Observation` (Your Curation Work & Storage Location)
This is where your daily work in Arbor is saved!
* **`Reviewed`**: Displays `TRUE` if you marked the specimen as reviewed, or `FALSE` if it is still pending.
* **`ReviewedAt`**: An automatic timestamp recording the exact date and time the specimen was verified.
* **The 11 Problem Columns**: Columns like `Genus_Problem`, `Species_Problem`, `Collector_Problem`, and `Box_Label_Problem` store `TRUE` if flagged, or `FALSE` if clear.
* **Storage Coordinates**: `Building`, `Floor`, `Cabinet`, `Shelf`, and `Stored as` record where the plant physically lives in the museum stacks.

#### 3. `Photo` (Attached Photos & Scans)
Contains the file paths and web links for photos:
* Links high-resolution image files on your local drive or online museum repositories to the matching `ObjectID`.

#### 4. `Unvalidated_source` (Notes for Illegible Handwriting)
A scratchpad sheet for messy labels:
* If a 19th-century label is torn or unreadable, this sheet stores draft comments (e.g. *"Label partially eaten by insects; looks like 'Quercus' but uncertain"*) without corrupting the clean scientific name fields.

#### 5. `Log` (The Audit Trail)
Whenever an edit is made, Arbor quietly appends a row here recording the date, time, user, and what value changed (e.g. *"Changed Cabinet from 4 to 5"*). This protects you by providing a full history of all updates.

---

## Chapter 6: Helpful Keyboard Shortcuts (Rest Your Mouse Hand)

Clicking a mouse thousands of times a day can strain your wrist and fingers. Arbor is built to let you complete your entire curation shift using only your keyboard:

### Primary Daily Work Keys (The "Top 5")

| Shortcut Key | What It Does | Why You Will Love It |
| :--- | :--- | :--- |
| **`[Ctrl] + [Enter]`** | **Mark Reviewed** | Signs off on the active specimen (`[REV]` / `[REV+ERR]` / `[REV+NOTE]`; auto-advances if **Auto-next** is enabled). |
| **`[Space]`** | **Toggle Problem Checkbox** | Checks or un-checks whichever problem box you are currently focused on. |
| **`[Down]` / `[Up]`** | **Next / Previous Specimen** | Moves down or up your specimen list card by card. |
| **`[Ctrl] + [Down]` / `[Up]`** | **Jump to Next Problem Card** | Skips clean records and jumps straight to cards with open problem flags. |
| **`[Ctrl] + [S]`** | **Save Active Session** | Writes all changes safely to the Excel workbook on your hard drive. |

### Searching & Finding Records
* **`[Ctrl] + [K]`**: Opens the **Universal Command Palette**. Type any specimen number (`#1042`), plant name, or command (e.g. `save`, `dark mode`, `export`) to jump immediately.
* **`[Ctrl] + [F]`**: Jumps your cursor directly into the search bar at the top of the Specimen Directory.
* **`[Ctrl] + [G]`**: Opens the **Filter Menu** to view only unreviewed specimens, only plants with photos, or only problem records.

### Typing & Editing Data
* **`[Ctrl] + [E]`** or **`[Ctrl] + [I]`**: Jumps your cursor into the first Registration form field so you can start typing immediately.
* **`[Ctrl] + [L]`** or **`[F4]`**: Jumps your cursor into the first Storage Location field (Cabinet / Shelf).
* **`[Ctrl] + [Z]`** / **`[Ctrl] + [Y]`**: Undo or redo any text edit.
* **`[Ctrl] + [H]`**: Opens the **Conflict Resolver** when historical books disagree with your sheet.

### Standard Museum Codes for Missing Information (ICEDIG)
When an old label has missing or damaged text, do not leave the field blank. Use these standard museum shortcuts while typing in any text box:

| Shortcut | Quick Code | What It Types | When to Use It |
| :--- | :--- | :--- | :--- |
| **`[Ctrl] + [Shift] + [M]`** | `?m` | `unknown:missing` | Information was omitted on the physical label (e.g. no date written). |
| **`[Ctrl] + [Shift] + [I]`** | `?i` | `unknown:indecipherable`| Text is faded, torn, water-damaged, or completely illegible. |
| **`[Ctrl] + [Shift] + [U]`** | `?u` | `unknown:undigitized` | Information was skipped during the initial digitization pass. |
| **`[Ctrl] + [Shift] + [W]`** | `?w` | `withheld` | Data is legally sensitive (e.g. exact GPS of an endangered orchid). |
| **`[Ctrl] + [Shift] + [Backspace]`**| *(None)* | *(Clears field)* | Erases the entire contents of the field cleanly. |

---

## Chapter 7: Changing the View (If Text Is Too Small or Crowded)

Everyone's eyes and monitors are different. If the text feels cramped on a small laptop or you want to see more cards at once on a desktop display, Arbor gives you **4 one-click layout profiles**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         4 DIRECTORY VIEW PROFILES                           │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────┤
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

### Toggling Workspace Panels & Working Without Photos
If you want to maximize screen space for inspecting photos or typing notes, use the function keys:
* **`[F6]`**: Toggle the Specimen Directory (left column) on or off.
* **`[F7]`**: Toggle the Registration Form (right column) on or off.
* **`[F8]`**: Toggle the Specimen Photos Viewport (middle column) on or off.
* **Clean 2-Column Layout When Photos Are Hidden**: When you press `F8` (or switch to Offline image mode), Arbor collapses the empty middle column so the Specimen Directory and Registration Form expand cleanly — and if **Storage Location** is set to Center/Bottom, it docks neatly along the bottom of your screen right above the Bottom Progress Bar.
* **Working on a Second Monitor**: If you drag Arbor onto an external monitor, all dialogs, photo popouts, dropdown menus, tooltips, and status notifications automatically open on that same screen.

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

### When No Photo Folder Is Connected Yet
If you open a collection without selecting an image folder, Arbor displays a clean **Specimen Audit Summary** in the center with 1-click buttons right at the top: **Select Image Folder…**, **Use Online Photos**, or **Hide Photo Pane (F8)**.

### The Detached High-Resolution Viewer
For very difficult handwriting or tiny pressed leaves, **double-click** the image. 
* A **Full-Screen Photo Popout** window appears on top of your workspace.
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
│ • Holds Excel workbook │                       │ • 1-tap Set Shelf save │
└────────────────────────┘                       └────────────────────────┘
```

### How to Connect in 4 Easy Steps:
1. **Open Mobile Companion**: In Arbor on your desktop computer, click **`MOBILE`** in the top bar, or press `Ctrl+K` and type `Mobile Companion`.
2. **Check PIN & Phone Tutorial Options**: Choose whether to require the 4-digit PIN (`🔒 Require 4-Digit PIN: ON / OFF` — keep **ON** on public tunnels, optional on private offline Wi-Fi) and pick a **Phone tutorial** mode (**Ask on the phone** recommended, **Trainee**, **Helper**, or **Off**), then click **▶ Start Mobile Session**.
3. **Scan the QR Code**: Point your phone camera at the QR code on screen (or copy the link). Scanning the QR code signs you in automatically and launches the hands-on phone coach tutorial on your first object (anyone can also start the Trainee or Helper tutorial anytime from **⚙ Settings → Phone tutorial**).
4. **Walk & Audit with Touch Gestures**:
   * Swipe left/right to glide between **Data ↔ Location ↔ Problems (Problem Resolution)**.
   * Quickly glance at **`Data`** against the physical object: tick the **inline checkbox next to any disagreeing field** (e.g. box says Africa, file says China) to flag it (`[REV+ERR]`), **tap the field value** (or **`ICEDIG ▾`** on **`Problems`**) to set an **ICEDIG** code (`unknown:missing`, `unknown:indecipherable`), or tap **`⚑ Needs Specialist`** in the bottom bar + add a short **`Comment`** for physical damage (`[REV+NOTE]`).
   * Tap **`📜 Old names`** (read-only) to check if an unfamiliar box label is just an older plant or family name.
   * Use **`Set Shelf`** at the top of the list for 1-tap **Storage Location** saving (with a **5-second `↩ Undo`** toast), and use the **Location** tab for **`Stored as`** and **`Loaned Out`** (displays an amber **`↗ Loaned`** badge).
5. **Tap `?` or `⚙` Anytime on Your Phone**: Open the **Badges, ICEDIG & Field Guide**, restart the Trainee/Helper tutorial, or manage one-time contextual tips right from your phone.

---

### The Real-World Hallway Audit Workflow

In a real museum vault, historical records rarely know which cabinet or shelf an object lives in ahead of time. You will typically work cabinet by cabinet, pulling physical boxes or folders:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. SET SHELF    │ ──> │ 2. FAST LOOKUP  │ ──> │ 3. 1-TAP SAVE   │ ──> │ 4. MARK REVIEWED│
│ Building, Floor,│     │ Numeric keypad  │     │ Save to Cab/Sh  │     │ [REV] or        │
│ Cabinet & Shelf │     │ auto-normalizes │     │ (5s ↩ Undo)     │     │ [REV+ERR]       │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

#### 1. Fast Number Lookup (Search-First)
* Tap the search bar at the top of your phone screen. Arbor automatically brings up the **numeric keypad** for fast typing (with a `[123 / Aa]` button to switch to plant names).
* **Automatic Zero Normalization**: If your physical specimen label says `#001` or `#1`, simply type `1` or `001`. Arbor recognizes both formats instantly.
* When you finish reviewing an object and tap `< Back`, Arbor automatically clears and focuses the search box so you can immediately type the next specimen number!

#### 2. 1-Tap Storage Location Saving (`Set Shelf` + 5-Second Undo)
When you open a cabinet, you will usually inspect dozens of consecutive specimens on the same shelf before moving to the next. Typing the same Building, Floor, Cabinet, and Shelf numbers fifty times would be slow and cause typos.

* **Set Your Shelf Once**: Tap **`Set Shelf`** in the top bar of the Specimen List (`Shelf: Not set [Set Shelf]`) and pick the Building, Floor, Cabinet, and Shelf you are standing in front of.
* **1-Tap Save**: Inside every specimen you open, a green thumb button appears right under the plant title:
  `📍 Save to Cab 21 · Sh 01`
* Simply tap it once to save all coordinates! If a specimen already belongs to a different shelf, the button turns amber **`⚠️ Move to Cab 21 · Sh 01`** so you never relocate an object by accident — and every 1-tap save or move shows a **5-second `↩ Undo`** button in case you tapped by mistake.

#### 3. Checking Old Names (`📜 Old names`) & Solving Conflicts (`Problems` Tab)
* **Unfamiliar Latin or family name on the box?** Tap **`📜 Old names`** (read-only) to immediately check past museum names, classical/APG old family names (like *Compositae* for *Asteraceae*), and known GBIF synonyms — if it matches, keep the modern name!
* **Disagreement between older catalog books?** Swipe right to the **`Problems`** tab (`[CFCT]`) — it works just like Desktop's Problem Resolution. For example, if one source says England and another says Finland, look at the physical object in your hand and tap **`Apply`** on the matching value (or **`✓ Value is Correct`**).

#### 4. Flagging Problems While Marking Reviewed (`[REV+ERR]`)
What if you pull a specimen and discover a clear mismatch (e.g. the label says Africa while the record says China), physical damage (a crushed box), or an illegible handwritten label?
* **Path A (Fix on the spot)**: If the physical label in your hand resolves a conflict or flagged field, swipe to **`Problems`** and tap **`Apply`** (or **`✓ Value is Correct`**).
* **Path B (Flag for desktop triage)**: Tap the **checkbox right next to the disagreeing field on `Data`** (or tap **`⚑ Needs Specialist`** in the bottom bar + add a short **`Comment`** for physical damage/conservation issues), **AND STILL TAP `✓ Mark Reviewed`**.
* **Why this is a success**: Marking it reviewed stamps the physical verification and location while displaying **`[REV+ERR]`** for desk data errors or calm **`[REV+NOTE]`** for `Needs Specialist` items.

#### 5. Viewport-Reclaimed Photo Folio
If an archival photo scan has not yet been uploaded for the specimen, Arbor automatically collapses the empty photo box into a compact single-line bar, keeping Registration Data and inline problem checkboxes right under your thumb without endless scrolling!

---

### Returning to Your Desk: Saving & Exploring Your Results

When you finish your aisle audit and return to your computer:
1. Click **🔴 End Mobile Session** (or click **`💾 Save Workbook Now`** / press **`Ctrl + S`**). Arbor shows a calm wrap-up dialog (**"All Your Phone Work Is Now in Arbor!"**) with one-click shortcuts to **`💾 Save File Now (Ctrl+S)`**, **`🔍 Filter (Ctrl+G)`**, or **`❓ Help & Tutorials`**.
2. Press **`Ctrl + G`** (or press **`Ctrl + K`** and type `Hallway`) and click **`🎯 Hallway Follow-Up (REV+ERR)`** to isolate every verified specimen with an open flag.
3. Want to step through every flagged specimen one by one in a dedicated queue? Press **`Ctrl + K`** → **`Triage Problem Queue (Filtered List)`**:
   * Click **`✓ Value is Correct (Clear Flag)`** if a flagged value turns out to be fine (turns `[REV+ERR]` back to green `[REV]`, with full `Ctrl+Z` Undo support).
   * Press **`Alt + ←` / `Alt + →`** to step between queued specimens.
   * **Can't solve a problem today?** That is completely okay — simply skip it and leave the flag active so a specialist or curator can revisit it later.
   * *(Tip: You can practice this optional desk workflow anytime in **HELP → Interactive Tutorials → Optional & Advanced → Batch Problem Queue**!)*

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

### 4. "I made a big mistake or edited the wrong field!"
* **Don't panic!**
  * Press **`Ctrl + Z`** to immediately undo your last text change or review toggle.
  * If you just ran a **Bulk Edit** across many specimens, press **`Ctrl + K`** and select **`Undo Last Bulk Edit`** to revert the entire batch in one click.
  * Arbor also creates automatic timestamped safety backups in the `.arbor_backups/` folder before major operations, so your supervisor can always restore an earlier copy with zero data loss.

### 5. "A text box is glowing with a yellow background"
* **What it means**: This is a helpful visual reminder! A problem checkbox is currently active for that specific field (for example, if `Species_Problem` is checked, the Species box glows yellow).
* **The fix**: Double-check the text on the physical label. If you resolve the issue and uncheck the problem box, the yellow highlight disappears.

### 6. "The photograph is missing or showing a black box"
* **The fix**:
  1. Press **`F8`** twice to toggle the photo viewport off and on again.
  2. If the photo was stored on an external USB hard drive, check that the drive cable is securely plugged into your computer.
  3. If the photo is still missing, check the **Images_Problem** checkbox to alert the digitization team.

### 7. Checking for Updates & Running Arbor from Any Folder
* **Checking for Updates**: Open **Help → Check for Updates** (or **Settings → Check for Updates**) to see if a newer version of `Arbor.exe` is available. After downloading, you can choose **Restart & Restore Session** (Arbor will prompt to save any unsaved work first) or **Apply on Next Exit** to install the update automatically the next time you close Arbor.
* **Read-Only Folders**: If Arbor is placed in a locked folder (such as `Program Files`), it automatically saves your settings, word lists, and error logs in your personal Windows AppData folder (`%LOCALAPPDATA%\Arbor`) so nothing is ever lost.

---

*End of Trainee Work Manual. Happy Curating!*
