# Arbor — Museum & Herbarium Collection Curation Suite

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

**Arbor** is an offline-first desktop application (with an embedded **Mobile Companion**) designed to help museums and herbaria **audit physical collections, document object condition and storage locations, and clean up catalog data** stored in standard Microsoft Excel (`.xlsx`) files.

Originally built for auditing an **Economic Botany collection**, one of Arbor's core goals is to **produce a clean, verified Excel dataset**—resolving historical discrepancies, flagging damaged or mislabeled specimens, and standardizing missing values—so the collection can be cleanly imported into a long-term collection management system such as **Specify**.

> **Scope note:** While Arbor also supports creating new Excel-based collection databases from scratch, **that is not its primary focus**. Arbor is first and foremost a practical auditing, data-cleaning, and verification tool for existing collections.
>
> *All of the code in this repository was written with AI agents (Gemini, Claude, and others).*

---

## Table of Contents
1. [Documentation & In-App Help Center](#documentation--in-app-help-center)
2. [Key Features](#key-features)
3. [Getting Started (Download or Run from Source)](#getting-started-download-or-run-from-source)
4. [Mobile Companion & Multi-User Workflow](#mobile-companion--multi-user-workflow)
5. [Testing](#testing)
6. [Project Architecture](#project-architecture)
7. [Configuration & Custom Profiles](#configuration--custom-profiles)
8. [Troubleshooting & FAQ](#troubleshooting--faq)
9. [Building the Windows Executable & Releases](#building-the-windows-executable--releases)
10. [Contributing Guidelines & AI Agent Guides](#contributing-guidelines--ai-agent-guides)

---

## Documentation & In-App Help Center

| Guide | Audience | What It Covers |
| :--- | :--- | :--- |
| **[Desktop Work Manual (`USER_GUIDE.md`)](USER_GUIDE.md)** | Trainees, assistants, curators | Daily auditing workflow, status badges, Excel sheet structure, ICEDIG codes, and keyboard shortcuts. |
| **[Mobile Vault Guide (`MOBILE_COMPANION_USER_GUIDE.md`)](MOBILE_COMPANION_USER_GUIDE.md)** | Vault & aisle teams | QR code pairing, 1-tap `Set Shelf` location logging, offline vault syncing, and condition flagging on a phone. |
| **[Maintainer Handoff Guide (`MAINTAINER_HANDOFF.md`)](MAINTAINER_HANDOFF.md)** | Future developers & maintainers | 5-minute dev quickstart, architecture rules, customizing columns in `config.py`, and release packaging. |
| **[Den Økonomisk Botaniske Samlingen — Overleveringsdokument (2026)](https://github.com/Fr0lich/arbor/wiki/Overleveringsdokument-Arbor)** | NHM UiO collection team *(Norwegian)* | Collection-specific handover guide on the GitHub Wiki (Excel sheets, `Books.xlsx` history, and daily rules). |

On the **Project Setup** startup screen, press **`F1`** or click **`Help`** for an interactive startup guide. Inside the main application, press **`F1`** or click **`HELP`** in the top bar at any time to open the **Arbor Help Center**, which includes:
- **Interactive Tutorials:** A 2-part Core Introduction (*Desktop Basics* in safe **Practice Mode** using sample photos + *Mobile Companion*), plus optional advanced tutorials.
- **Badges & Reference:** Visual guide to all status badges, card chips, the 3-way problem rule, ICEDIG codes, date conventions, and GBIF name checks.
- **Quick Guides (20–30s), Full Manuals, Troubleshooting, & Printable Shortcuts.**
- **Reset Tutorial Checkmarks** (under *About & Updates*) when handing a workstation to a new trainee.

---

## Key Features

- **Physical Collection Auditing & Condition Tracking:** Inspect specimens side-by-side with high-resolution photos (zoom, pan, rotate), verify storage coordinates (*Building, Floor, Cabinet, Shelf*), flag field mismatches, and escalate damaged objects or taxonomic doubts via `Needs Specialist` (`[REV+NOTE]`).
- **Mobile Companion for Vault & Aisle Work:** An embedded Flask web app that lets staff audit shelves and document specimen condition directly on their phones—**with full offline support** (Service Worker + `localStorage`/IndexedDB queue) for concrete basement vaults, and **multi-user support** when several phones connect to one desktop session.
- **Historical Catalog Comparison (`Ctrl+H`):** Load older digitized spreadsheets or catalog ledgers alongside your main Excel file to spot missing fields, surface discrepancies, and compare historical sources side-by-side against the physical object.
- **GBIF Taxonomic Name Checking:** Run single-specimen or batch lookups against GBIF to catch Latin spelling errors, outdated synonyms, and missing Family/Author data—always shown side-by-side before applying any change.
- **Standardized Missing Data (ICEDIG D4.1) & Single-Badge Priority:** Insert standardized codes (`unknown:missing`, `unknown:indecipherable`, `unknown:undigitized`, `withheld`) with quick shortcuts (`?m`, `?i`, `?u`, `?w`), while every specimen card displays one clear priority badge (`[REV]`, `[REV+ERR]`, `[REV+NOTE]`, `[CFCT]`, `[UNREV]`, etc.).
- **Safe, Atomic Excel Persistence:** Works directly on standard `.xlsx` workbooks with no external database servers (no PostgreSQL, MySQL, Redis, or Docker). Saves use atomic temp-file replacement, rolling backups in `.arbor_backups/`, Undo/Redo, and CSV/Excel formula-injection sanitization.
- **Zero-Friction Windows Deployment:** Distributed as a standalone, double-click `Arbor.exe` built with PyInstaller.

---

## Getting Started (Download or Run from Source)

### Option A: Windows Users (Recommended — No Python Required)
1. Go to the **[GitHub Releases](https://github.com/Fr0lich/arbor/releases)** page and download the latest `Arbor.exe`.
2. Double-click `Arbor.exe` to launch Arbor—no Python installation, admin privileges, or database setup is required.
3. Select your main Excel collection file (`.xlsx`), optional photo folder, and optional historical books file, then click **Open Collection →**.

> **Important:** Always **close Microsoft Excel** before opening or saving the same `.xlsx` file in Arbor, as Windows locks open Excel files.

### Option B: Running from Source (Windows, macOS, & Linux)
Arbor runs on **Windows**, **macOS**, and **Linux** using Python and Tkinter.

#### Prerequisites
- **Python 3.10 or higher** (Python 3.12 recommended on Windows).
- **Linux only:** Install Tkinter (and `xvfb` if running headless UI tests):
  ```bash
  sudo apt-get update && sudo apt-get install -y python3-tk xvfb
  ```

#### Installation & Launch
```bash
git clone https://github.com/Fr0lich/arbor.git
cd arbor

# Install runtime dependencies:
pip install -r requirements.txt

# (Optional) Install dev/test and PyInstaller build tools:
pip install -r requirements-dev.txt

# Launch Arbor Desktop:
python main.py
```

---

## Mobile Companion & Multi-User Workflow

The **Mobile Companion** is designed for walking through collection aisles and vaults—updating shelf locations, documenting object condition, checking old plant names, and flagging discrepancies right where the physical specimens live.

- **How to connect:** Click **`MOBILE`** in Arbor Desktop (or **`Mobile Companion`** on the Project Setup screen), scan the QR code on your phone (no app store install required—runs in your mobile browser), and enter the optional 4-digit PIN.
- **Network & Tunneling:** Works over local Wi-Fi, or over mobile data via optional Cloudflare Quick Tunnels / Pinggy SSH tunnels, secured by an `X-Session-Token` and PIN.
- **Offline Vault Mode:** If your phone loses signal in a basement vault, edits are queued locally and sync automatically once connectivity returns. *(Do not close the browser tab while pending offline edits are queued.)*

### Concurrency & Multi-User Rule
- **Desktop instances (Single-User per File):** **Do not open the same `.xlsx` file in two separate Arbor Desktop instances at the same time.** Each desktop instance loads the workbook into memory and replaces the file on save, meaning the last save will overwrite the other user's changes.
- **Mobile Companion (Multi-User Supported):** **Multiple people can work simultaneously** by connecting their phones to the **same single Arbor Desktop instance**. All mobile edits are routed through that desktop session with thread-safe locking and per-field conflict checks, then saved cleanly to Excel from one place.

---

## Testing

Arbor uses `pytest` for its automated test suite (~470 tests across desktop UI, repository persistence, and mobile server endpoints).

```bash
# Windows / Desktop environment:
python -m pytest tests/ -q

# Linux headless environment (requires xvfb):
xvfb-run -a python3 -m pytest tests/ -q
```

---

## Project Architecture

Arbor cleanly separates UI, state management, persistence, and background services:

- **UI Layer (`main.py`, `ui/`):** Built with Tkinter, featuring modular panels, DPI scaling (`sc()`), unified Help Center & Settings windows, interactive tutorials, and high-resolution image tools.
- **EventBus & State (`ui/state.py`, `models.py`):** Thread-safe Pub/Sub (`app_bus`) decouples background workers and mobile updates from Tkinter UI redraws (`root.after()`), backed by `AppState` with Undo/Redo and mutation tracking.
- **Backend Services (`backend/`):** Embedded Flask **Mobile Companion** (with an optional experimental **Waitress** WSGI server engine in `mobile_server.py` + zero-build frontend in `mobile_template_v2.py`), Marshmallow payload validation (`mobile_schemas.py`), search/filtering, GBIF lookups, and the GitHub Releases updater (`updater.py`).
- **Data Repository (`repository.py`):** Manages Excel loading, normalization, and atomic saving across `Registration`, `Observation`, and `Log` sheets (plus optional `Photo` and legacy `Unvalidated_source` sheets), along with rolling backups and SQLite snapshots.

---

## Configuration & Custom Profiles

- **`config.py`:** Defines global application settings (`APP_VERSION`, `DEFAULT_GITHUB_REPO`), ICEDIG codes, and collection schemas (`DATABASE_CONFIGS`). You can adapt Arbor to a different museum's Excel layout by adding a profile in `DATABASE_CONFIGS`.
- **`user_prefs.json`:** Persists user preferences, window layout, tutorial completion state, and update repository settings.

---

## Troubleshooting & FAQ

**Q: Arbor says it cannot save because the Excel file is locked.**  
A: Close Microsoft Excel (or pause cloud sync if the file is inside OneDrive/Dropbox) and press `Ctrl+S` again.

**Q: My mobile edits aren't appearing immediately on Desktop.**  
A: Check the connection badge in the mobile header. If you are offline in a vault, edits are safely queued on the phone and will flush automatically once reconnected. Keep the browser tab open until synced.

**Q: I get `TclError: no display name` when running tests on Linux.**  
A: Wrap the test command with `xvfb-run -a` (see [Testing](#testing)).

**Q: The Mobile Server complains that a port is already in use.**  
A: Arbor dynamically assigns available ports on startup, but if a stale process holds a port on Linux/macOS, you can clear it manually (e.g. `kill $(lsof -t -i :3000) 2>/dev/null || true`).

---

## Building the Windows Executable & Releases

### Creating a Standalone `.exe`
To build a portable Windows executable (`dist\Arbor.exe`):
```bat
build_exe.bat
```

### Handover & GitHub Releases (For Future Maintainers)
Arbor includes a built-in GitHub Releases updater (`backend/updater.py` + `ui/update_dialog.py`):

1. **Pointing Arbor to a new GitHub repository:**
   - **Code default (for new builds):** Update `DEFAULT_GITHUB_REPO` (and `APP_VERSION`) at the top of `config.py`.
   - **Existing installs:** Users can change the repository in **Settings → Check for Updates → Update Repository** (`owner/repo`), or set the `ARBOR_UPDATE_REPO` environment variable. If the GitHub repository is transferred to a new owner/org, Arbor follows GitHub's redirect automatically.
2. **Publishing a new release:**
   - Bump `APP_VERSION` in `config.py` and update `documentation/CHANGE_JOURNAL.md`.
   - Run the test suite (`python -m pytest tests/ -q`).
   - Run `build_exe.bat` to verify `dist\Arbor.exe`, or push a version tag (`git tag vX.Y.Z && git push origin vX.Y.Z`) to trigger the GitHub Actions workflow.
   - Attach `Arbor.exe` to the GitHub Release.

For full developer details, see **[MAINTAINER_HANDOFF.md](MAINTAINER_HANDOFF.md)**.

---

## Contributing Guidelines & AI Agent Guides

Arbor was built with AI coding agents (Gemini, Claude, and others), and the repository includes a structured **AI Agent Guide system** so future developers—whether working with AI assistants or by hand—can safely modify the codebase without breaking architecture rules or drifting out of sync with user manuals:

- **`AGENTS.md` (Master Router):** The entry point for any AI coding assistant. It defines Arbor's core constraints (single-stack Tkinter + zero-build Flask Mobile Companion, offline-first design, approved vs. prohibited packages) and includes a **Task Routing Directory** pointing to the exact guide(s) to read *before* making changes.
- **`documentation/agent/` (Domain-Specific Guides):** Focused technical references covering architecture (`codebase_guide.md`, `feature_catalog.md`), UI tokens (`AI_UI_GUIDE.md`), threading/Pandas safety (`CLAUDE_BUG_REVIEW_GUIDE.md`), Mobile Companion rules (`MOBILE_COMPANION_GUIDE.md`, `MOBILE_AUDIT_WORKFLOW_SPEC.md`), and interactive tutorials (`TUTORIAL_GUIDE.md`).
- **`documentation/MASTER_DOCUMENTATION_MAP.md` & `documentation/CHANGE_JOURNAL.md`:** Enforce plain museum terminology (*Canonical Trainee Lexicon*) and track user-facing deltas so `USER_GUIDE.md`, cheat sheets, and in-app tutorials stay aligned with the code.

> **Tip for future developers:** When using an AI coding assistant on this repo, always instruct it to read **`AGENTS.md`** first.

### Core Rules
1. **Verify Your Work:** Always run the full `pytest` suite before submitting changes.
2. **EventBus Over Direct Calls:** Never update Tkinter widgets directly from a background thread—publish events to `app_bus` and let the UI subscribe.
3. **Widget Lifecycle:** Always check `.winfo_exists()` before querying widget geometry after `update_idletasks()`.
4. **Mobile Frontend:** Keep the mobile UI inside `INDEX_TEMPLATE_V2` in `backend/mobile_template_v2.py` (zero-build, no Node.js/npm).
