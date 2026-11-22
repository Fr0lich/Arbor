# Arbor Maintainer Handoff Guide

This 1-page reference is for anyone inheriting or maintaining **Arbor**, an offline-first desktop museum/herbarium collection curation suite with an embedded mobile companion.

---

## 1. Quickstart (5 Minutes)

- **Python**: 3.10–3.12 (Windows recommended for native Tkinter + PyInstaller builds).
- **Install runtime + dev/test tools**:
  ```bash
  pip install -r requirements-dev.txt
  ```
- **Generate the offline 220-specimen Demo Project** (not stored in git):
  ```bash
  python scripts/create_demo_dataset.py
  ```
- **Run Arbor from source**:
  ```bash
  python main.py
  ```
- **Run the core verification test suite (~130 tests, ~13s)**:
  ```bash
  python -m pytest tests/test_hardened_data_safety.py tests/test_demo_dataset.py tests/test_navigation_and_dialogs.py tests/test_sandbox_tutorials.py tests/test_mobile_companion.py tests/test_mobile_companion_offline.py tests/test_command_palette_and_search.py tests/test_problem_persistence_fix.py tests/test_status_bar.py -q
  ```

---

## 2. Repository Map (Active vs. Archived)

| Path | Status | Purpose |
| :--- | :--- | :--- |
| `main.py`, `ui/` | **ACTIVE PRODUCTION** | Live Tkinter desktop application, dialogs, tutorials, command palette, image viewer. |
| `backend/` | **ACTIVE PRODUCTION** | Embedded Flask mobile companion (`mobile_server.py` + pure-Python frontend modules `mobile_template_v1.py` / `mobile_template_v2.py`), Marshmallow validation (`mobile_schemas.py`), search, filtering, GBIF lookups, background worker, updater. |
| `models.py`, `repository.py`, `config.py`, `utils.py` | **ACTIVE PRODUCTION** | `AppState` (`_mutation_seq`, undo/redo), atomic Excel/SQLite persistence, preferences, logging (`loguru`), DPI scaling (`sc()`). |
| `USER_GUIDE.md`, `MOBILE_COMPANION_USER_GUIDE.md`, `documentation/` | **ACTIVE DOCS** | Trainee manuals, desk cheat sheet, Canonical Trainee Lexicon (`MASTER_DOCUMENTATION_MAP.md`), and `CHANGE_JOURNAL.md`. |
| `build_exe.bat`, `main.spec` | **ACTIVE PACKAGING** | Builds standalone portable `dist\Arbor.exe` (`console=False`) + bundled guides and demo workbook. |
| `pyside_new_uis/` | **PAUSED (Phase 1 Blueprint)** | 32 verified `.ui` XML files if a future team ever resumes a Qt migration. Do not build everyday features here. |
| `ui_qt/`, `qt designer/`, `archive/` | **ARCHIVED / REFERENCE** | Early prototypes and superseded code. Do not edit for production changes. |

---

## 3. Non-Negotiable Architecture Rules

1. **Offline-First in Concrete Vaults**: Core desktop curation, Excel saves, and mobile companion auditing must work with **zero internet**. Cloud calls (GBIF, tunnels) are strictly optional with graceful fallbacks.
2. **Zero-Friction Portable `.exe`**: Never require external database engines (PostgreSQL, MySQL, Redis, Docker) or system compilers. Everything freezes cleanly into `dist\Arbor.exe`.
3. **Zero-Build Mobile Frontend**: The mobile UI lives strictly as pure-Python string constants in `backend/mobile_template_v1.py` (`INDEX_TEMPLATE`) and `backend/mobile_template_v2.py` (`INDEX_TEMPLATE_V2`), re-exported by `backend/mobile_server.py` (Vanilla HTML/JS + deferred Tailwind CDN + scoped `html.arbor-offline-css` fallback). No Node.js, npm, Vite, or React.
4. **Zero Barcodes**: Barcode scanning was permanently removed. Never re-introduce barcode libraries, UI, or documentation references.
5. **Atomic Excel Safety**: Saves write to a sibling temp file + `os.replace`, create rolling snapshots in `.arbor_backups/`, and protect against mid-save edits via `AppState._mutation_seq`.
6. **Canonical Trainee Lexicon & Change Journal**: User-facing copy uses plain museum language (*Specimen Directory*, *Storage Location*, *Mark Reviewed*, *Phone Connector*). Record all user-facing changes in `documentation/CHANGE_JOURNAL.md`.

---

## 4. Release & Packaging Checklist

1. Bump `APP_VERSION` in `config.py`.
2. Ensure `documentation/CHANGE_JOURNAL.md` (and `USER_GUIDE.md` / `MOBILE_COMPANION_USER_GUIDE.md` if shortcuts or workflows changed) are up to date.
3. Run the core verification test suite above and confirm 100% pass.
4. Build locally via `build_exe.bat` (or `build_exe.bat --no-pause` in CLI) and verify `dist\Arbor.exe` launches cleanly from an isolated folder outside the repo.
5. Push a version tag (`git tag vX.Y.Z && git push origin vX.Y.Z`) — `.github/workflows/ci.yml` automatically runs tests and uploads the portable `Arbor-Windows-Portable` artifact.

---

## 5. Customizing Collection Columns (`config.py`)

To adapt Arbor to a different museum's Excel column layout without touching UI code:
1. Open `config.py` and locate `DATABASE_CONFIGS`.
2. Copy an existing entry (e.g. `"Økonomisk Botanisk"` or `"Blank Minimal"`) under a new profile name.
3. Update `sheets` (`reg`, `obs`, `photo`, `log`), `ui_sections["registration"]`, `ui_sections["location"]`, and `ui_sections["problems"]` (mapping each problem flag column via `maps_to`).
4. The new profile automatically appears in the Startup dialog's **Profile** dropdown and **Create New Database** wizard.

