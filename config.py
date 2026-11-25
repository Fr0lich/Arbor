# =====================
# UI SCALE (DPI)
# =====================
# Set at startup in main.py based on screen DPI.
# Use sc(n) everywhere instead of raw pixel/font sizes.
UI_SCALE = 1.0
ENABLE_TUTORIALS = True
_detected_scale = 1.0  # Overwritten at startup with the actual detected DPI ratio
_PREFS_PATH = "user_prefs.json"  # Overwritten at startup with the correct exe-relative path

# =====================
# APPLICATION METADATA & UPDATES
# =====================
APP_VERSION = "2.1.0"
DEFAULT_GITHUB_REPO = "Fr0lich/arbor"

import tkinter as tk
import os
import json
import sys
from datetime import datetime
# =====================
# ICEDIG D4.1 UNKNOWN VALUE STANDARDS
# =====================
# Legacy ambiguous tokens (still valid but imprecise)
LEGACY_UNKNOWN_TOKENS: frozenset = frozenset({"unknown", "ukjent", "?", "-"})
# Single source of truth for precision ICEDIG D4.1 codes (consumed by Desktop & Mobile Companion)
ICEDIG_CODES: list = [
    {
        "code": "unknown:missing",
        "description": "blank on original label",
        "shortcut": "Ctrl+Shift+M",
        "shorthand": "?m",
    },
    {
        "code": "unknown:indecipherable",
        "description": "illegible on label",
        "shortcut": "Ctrl+Shift+I",
        "shorthand": "?i",
    },
    {
        "code": "unknown:undigitized",
        "description": "skipped during digitisation",
        "shortcut": "Ctrl+Shift+U",
        "shorthand": "?u",
    },
    {
        "code": "withheld",
        "description": "known but intentionally hidden",
        "shortcut": "Ctrl+Shift+W",
        "shorthand": "?w",
    },
]
# Precision ICEDIG D4.1 codes (derived from ICEDIG_CODES)
ICEDIG_UNKNOWN_CODES: frozenset = frozenset(item["code"] for item in ICEDIG_CODES)
# Combined set: all tokens that mean "this field is intentionally unknown"
ALL_UNKNOWN_TOKENS: frozenset = LEGACY_UNKNOWN_TOKENS | ICEDIG_UNKNOWN_CODES
# Human-readable labels for each ICEDIG code (used in context menus, tooltips, and Mobile Companion)
ICEDIG_CODE_LABELS: dict = {
    item["code"]: f"{item['code']}  ({item['description']})"
    for item in ICEDIG_CODES
}

# Single source of truth for strictly non-ICEDIG physical/specialist quick-tag pills
# (consumed dynamically by both Desktop Comment bar and Mobile Companion V2)
SPECIALIST_QUICK_TAGS: list = [
    {"label": "+ Damaged", "text": "Damaged"},
    {"label": "+ Mold / Pest", "text": "Mold / Pest"},
    {"label": "+ Mixed Specimen", "text": "Mixed specimen"},
    {"label": "+ Needs Specialist ID", "text": "Needs specialist ID"},
]

def get_system_theme():
    """Detect platform and return system theme name."""
    if sys.platform.startswith("win"):
        return "vista"
    elif sys.platform.startswith("darwin"):
        return "aqua"
    else:
        return "clam"

def get_theme():
    """Get the current theme to use (defaulting to 'clam' for now)."""
    # Defaults to clam as per requirements, but can easily be switched to get_system_theme()
    return "clam"


import atexit
# In-memory prefs cache — populated on first read, invalidated on write.
_prefs_cache = None

def load_prefs():
    global _prefs_cache
    if _prefs_cache is not None:
        return _prefs_cache
    if os.path.exists(_PREFS_PATH):
        try:
            with open(_PREFS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    _prefs_cache = data
                    return _prefs_cache
        except json.JSONDecodeError:
            try:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup = f"{_PREFS_PATH}.corrupt.{ts}"
                os.replace(_PREFS_PATH, backup)
            except Exception:
                pass
        except Exception as e:
            try:
                from utils import debug_log as _debug_log
                _debug_log("WARNING", f"Could not read user preferences, using defaults: {e}")
            except Exception:
                pass
    _prefs_cache = {}
    return _prefs_cache

import threading
import tempfile

_save_job_id = None
_prefs_dirty = False
_prefs_io_lock = threading.Lock()

def _write_prefs_now():
    global _save_job_id, _prefs_dirty
    _save_job_id = None
    snapshot = _prefs_cache
    if snapshot is None:
        return
    tmp_path = None
    with _prefs_io_lock:
        try:
            # Pre-serialize in memory before touching disk so any serialization error
            # or mid-write mutation can never leave a truncated/corrupt user_prefs.json.
            payload = json.dumps(dict(snapshot), indent=2, ensure_ascii=False)
            target_dir = os.path.dirname(os.path.abspath(_PREFS_PATH)) or "."
            os.makedirs(target_dir, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=target_dir,
                prefix="user_prefs.",
                suffix=".tmp",
                delete=False,
            ) as f:
                tmp_path = f.name
                f.write(payload)
                f.flush()
                try:
                    os.fsync(f.fileno())
                except OSError:
                    pass
            os.replace(tmp_path, _PREFS_PATH)
            tmp_path = None
            _prefs_dirty = False
        except Exception as e:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            from utils import debug_error as _debug_error
            _debug_error("Failed to save user preferences", str(e))

def flush_prefs():
    """Synchronously flush any pending debounced preference write (safe at exit)."""
    global _save_job_id
    if _prefs_dirty or _save_job_id is not None:
        root = getattr(tk, "_default_root", None)
        if root and _save_job_id is not None:
            try:
                root.after_cancel(_save_job_id)
            except Exception:
                pass
        _write_prefs_now()

atexit.register(flush_prefs)

def save_prefs(prefs):
    global _prefs_cache, _save_job_id, _prefs_dirty
    _prefs_cache = prefs  # keep cache in sync before writing
    _prefs_dirty = True

    root = getattr(tk, "_default_root", None)

    if root:
        if _save_job_id is not None:
            try:
                root.after_cancel(_save_job_id)
            except Exception:
                pass
        try:
            _save_job_id = root.after(100, _write_prefs_now)
        except Exception:
            _write_prefs_now()
    else:
        _write_prefs_now()

def get_last_dir(key):
    return load_prefs().get(key, "")

def set_last_dir(key, path):
    if not path:
        return
    directory = os.path.dirname(path) if os.path.isfile(path) else path
    prefs = load_prefs()
    prefs[key] = directory
    save_prefs(prefs)

def get_update_repo():
    """Retrieve the configured update repository.

    Priority: ``ARBOR_UPDATE_REPO`` env var -> ``user_prefs.json`` -> ``DEFAULT_GITHUB_REPO``.
    """
    env_repo = os.environ.get("ARBOR_UPDATE_REPO", "").strip()
    if env_repo:
        return env_repo.replace("https://github.com/", "").replace("http://github.com/", "").strip("/")
    return load_prefs().get("update_repository", DEFAULT_GITHUB_REPO)

def set_update_repo(repo_str):
    """Set and persist a custom update repository (e.g. 'NaturalHistoryMuseum/arbor')."""
    if not repo_str:
        repo_str = DEFAULT_GITHUB_REPO
    repo_clean = repo_str.strip().replace("https://github.com/", "").replace("http://github.com/", "").strip("/")
    prefs = load_prefs()
    prefs["update_repository"] = repo_clean
    save_prefs(prefs)
    return repo_clean

def get_recent_files():
    """Return list of recent file dicts: [{"path": str, "modified": str}, ...]"""
    return load_prefs().get("recent_files", [])

def add_recent_file(path):
    """Add or refresh a file entry in recent_files (max 8, newest first)."""
    if not path or not os.path.exists(path):
        return
    try:
        mtime = os.path.getmtime(path)
        modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
    except Exception as e:
        modified = ""
    prefs = load_prefs()
    recent = [r for r in prefs.get("recent_files", []) if r.get("path") != path]
    recent.insert(0, {"path": path, "modified": modified})
    prefs["recent_files"] = recent[:8]
    save_prefs(prefs)

# ==============================================================================
# DIRECTORY CARD & WIDGET VIEW PREFERENCES (UI PRESENTATION ONLY)
# ==============================================================================
DEFAULT_DIRECTORY_CARD_PREFS = {
    "density_mode": "standard",            # 'compact' (64px), 'standard' (78px), 'expanded' (92px)
    "show_location_row": True,             # bool
    "location_granularity": "full",        # 'full' (Building/Floor/Cab/Shelf), 'compact' (Cab/Shelf), 'none'
    "show_status_badge": True,             # bool: Row 1 status pill badge
    "show_author_citation": False,         # bool: Append botanical author to scientific name
    "unknown_taxon_fallback": "unknown",   # 'unknown' ("Unknown Specimen"), 'stored_as', 'empty'
    "visible_badge_categories": {
        "reviewed": True,                  # [ REV ], [ REV+ERR ]
        "taxonomy": True,                  # [ TAX ]
        "provenance": True,                # [ PROV ]
        "physical": True,                  # [ BOX ]
        "media": True,                     # [ IMG ]
        "conflicts": True,                 # [ CFCT ], [ ERR+HIS ]
        "general_err": True,               # [ ERR ]
        "unreviewed": True,                # [ UNREV ]
    },
    "badge_priority_preset": "default",    # 'default', 'taxonomist', 'collections_manager'
    "accent_strip_mode": "problems",       # 'problems', 'review_only', 'hidden'
    "visible_meta_tags": {
        "family": True,                    # e.g., FAGACEAE
        "photos": True,                    # e.g., 2 photos / ONLINE / NO PHOTO
        "loan": True,                      # e.g., LOAN
        "unknown": True,                   # e.g., UKN
        "unvalidated": True,               # e.g., UNVAL
    },
    "show_directory_view_strip": False,    # bool: Optional in-situ quick view controls above list (default: False)
}

def get_directory_card_prefs():
    """Retrieve current directory card display preferences merged with defaults."""
    import copy
    prefs = load_prefs()
    user_card_prefs = prefs.get("directory_card_display", {})
    merged = copy.deepcopy(DEFAULT_DIRECTORY_CARD_PREFS)
    if isinstance(user_card_prefs, dict):
        for k, v in user_card_prefs.items():
            if isinstance(v, dict) and isinstance(merged.get(k), dict):
                merged[k].update(v)
            else:
                merged[k] = v
    return merged

def save_directory_card_prefs(card_prefs):
    """Persist directory card display preferences to user_prefs.json."""
    prefs = load_prefs()
    prefs["directory_card_display"] = card_prefs
    save_prefs(prefs)

def reset_directory_card_prefs_to_default():
    """Restore directory card view customizations to factory defaults."""
    import copy
    default_copy = copy.deepcopy(DEFAULT_DIRECTORY_CARD_PREFS)
    save_directory_card_prefs(default_copy)
    return default_copy

CARD_PRESET_ALIASES = {
    "default": "standard",
    "high_speed": "compact",
    "taxonomist": "full_detail",
    "collections_manager": "minimalist",
}

def resolve_card_preset_name(preset_name: str) -> str:
    """Normalize a card layout preset or persona alias to canonical name."""
    norm = str(preset_name).strip().lower()
    return CARD_PRESET_ALIASES.get(norm, norm)

def get_card_preset_config(preset_name: str) -> dict:
    """Return dictionary of card preference overrides for a given preset."""
    import copy
    canonical = resolve_card_preset_name(preset_name)
    prefs = get_directory_card_prefs()
    if canonical == "compact":
        prefs["density_mode"] = "compact"
        prefs["show_location_row"] = False
        prefs["location_granularity"] = "none"
        prefs["show_status_badge"] = True
        prefs["show_author_citation"] = False
        prefs["badge_priority_preset"] = "default"
    elif canonical == "full_detail":
        prefs["density_mode"] = "expanded"
        prefs["show_location_row"] = True
        prefs["location_granularity"] = "full"
        prefs["show_status_badge"] = True
        prefs["show_author_citation"] = True
        prefs["badge_priority_preset"] = "taxonomist"
    elif canonical == "minimalist":
        prefs["density_mode"] = "compact"
        prefs["show_location_row"] = False
        prefs["location_granularity"] = "none"
        prefs["show_status_badge"] = False
        prefs["show_author_citation"] = False
        prefs["badge_priority_preset"] = "default"
    else:  # "standard" / "default"
        current_strip = prefs.get("show_directory_view_strip", False)
        prefs = copy.deepcopy(DEFAULT_DIRECTORY_CARD_PREFS)
        prefs["show_directory_view_strip"] = current_strip
    return prefs

def sc(n):
    """Scale a pixel or font size by the current UI scale factor."""
    return max(1, int(n * UI_SCALE))

# U2-D: Canonical monospace font family used for all data-entry widgets,
# location fields, and log viewers.  Change here to propagate everywhere.
FONT_MONO_FAMILY: str = "JetBrains Mono"

# ==============================================================================
# LEFTPANE & OVERLAY DRAWER THEME TOKENS
# Modify these values to customize colors, bounds, and animation parameters.
# ==============================================================================
RAIL_THEME = {
    "rail_bg": "#e9ece5",
    "rail_border": "#c4c7c7",
    "rail_width": 40,
    "icon_hover_bg": "#ffffff",
    "indicator_active_bg": "#c93a40",
}

DRAWER_THEME = {
    "drawer_bg": "#f2f5f1",
    "drawer_border": "#c4c7c7",
    "drawer_width": 300,
    "header_bg": "#e9ece5",
    "card_hover_bg": "#ffffff",
    "enable_animation": True,
    "anim_duration_ms": 140,
    "anim_step_interval_ms": 8,
}

# =====================
# AUTOSAVE SETTINGS
# =====================
AUTOSAVE_INTERVAL_MS = 2 * 60 * 1000   # 2 minutes — change here or via Settings menu
AUTOSAVE_SUFFIX = ".autosave.json"


# =====================
# DATABASE CONFIGS
# =====================

DATABASE_CONFIGS = {

    "Økonomisk Botanisk": {

        # ---------------------
        # GENERELT
        # ---------------------
        "has_images": True,
        "image_url_pattern": "https://www.unimus.no/photos/image/jpeg/O-V-OE-{num:04d}{suffix}.jpg",

        "sheets": {
            "reg": "Registration",
            "obs": "Observation",
            "photo": "Photo",
            "log": "Log",
        },

        # ---------------------
        # HISTORICAL DATA / BOOKS
        # ---------------------
        "books_columns": [
            "ObjectID",
            "Genus",
            "Species",
            "Family",
            "Author",
            "Plant Part",
            "Collector",
            "Innsammling Nr.",
            "Collection Date",
            "Collection Place",
            "Box Label",
            "Conservation Status"
        ],

        # ---------------------
        # UI STRUKTUR (NY MODELL)
        # ---------------------
        "ui_sections": {

            # -------- REGISTRATION --------
            "registration": [
                {"name": "Variant", "type": "text"},
                {"name": "Genus", "type": "text"},
                {"name": "Species", "type": "text"},
                {"name": "Author", "type": "text"},
                {"name": "Family", "type": "text"},
                {"name": "Higher Classification", "type": "text"},

                {"name": "(N) Plant Part", "type": "text"},
                {"name": "Plant Part", "type": "text"},

                {"name": "Collector", "type": "text"},
                {"name": "Innsammling Nr.", "type": "text"},

                {"name": "Collection Date", "type": "text"},
                {"name": "Collection Place", "type": "text"},

                {"name": "Box Label", "type": "text"},

                # ✅ multiline example
                {"name": "Observation", "type": "multiline"},

                {"name": "Conservation Status", "type": "text"},

                {"name": "Comment", "type": "multiline"},

                # ✅ låst felt
                {"name": "UID", "type": "text", "readonly": True},

                {"name": "ProblemDescription", "type": "multiline"},

                {"name": "Online photo 1", "type": "text"},
                {"name": "Online photo 2", "type": "text"},
                {"name": "Online photo 3", "type": "text"}
            ],

            "reg_groups": [
                { "name": "Taxonomy", "fields": ["Genus", "Species", "Author", "Family", "Higher Classification"] },
                { "name": "Collection", "fields": ["Collector", "Innsammling Nr.", "Collection Date", "Collection Place"] },
                { "name": "Object", "fields": ["Variant", "(N) Plant Part", "Plant Part", "Box Label", "Conservation Status", "Online photo 1", "Online photo 2", "Online photo 3"] },
                { "name": "Notes", "fields": ["Observation", "Comment", "ProblemDescription"] },
                { "name": "Admin", "fields": ["UID"] }
            ],

            # -------- LOCATION --------
            "location": [
                {
                    "name": "Stored as",
                    "type": "choice",
                    "choices": [
                        "Mounted on wooden platform",
                        "Petridish",
                        "in plastic box",
                        "in paper box",
                        "Free standing",
                        "in plastic bag"
                    ]
                },
                {
                    "name": "Floor",
                    "type": "choice",
                    "choices": [
                        "4",
                        "3",
                        "2",
                        "1",
                        "-1",
                        "-2",
                    ]
                },

                {"name": "Cabinet", "type": "text"},
                {"name": "Shelf", "type": "text"},
                {"name": "Extra", "type": "text"},
                {
                    "name": "Building",
                    "type": "choice",
                    "choices": [
                        "Lid's hus",
                        "Økern",
                        "Annet",
                    ]
                },
                {
                    "name": "Loaned out",
                    "type": "checkbox"
                },
                {
                    "name": "Loaned out date",
                    "type": "text",
                    "readonly": True
                },
            ], 

            # -------- PROBLEMS --------
            "problems": [
                {
                    "name": "Genus_Problem",
                    "type": "bool",
                    "maps_to": "Genus",
                    "category": "taxonomy",
                    "importance": "high"
                },
                {
                    "name": "Species_Problem",
                    "type": "bool",
                    "maps_to": "Species",
                    "category": "taxonomy",
                    "importance": "high"
                },
                {
                    "name": "Family_Problem",
                    "type": "bool",
                    "maps_to": "Family",
                    "category": "taxonomy",
                    "importance": "high"
                },
                {
                    "name": "Author_Problem",
                    "type": "bool",
                    "maps_to": "Author",
                    "category": "taxonomy",
                    "importance": "medium"
                },

                {
                    "name": "PlantPart_Problem",
                    "type": "bool",
                    "maps_to": "Plant Part",
                    "category": "physical",
                    "importance": "low"
                },

                {
                    "name": "Collector_Problem",
                    "type": "bool",
                    "maps_to": "Collector",
                    "category": "collection",
                    "importance": "medium"
                },
                {
                    "name": "Collection_Date_Problem",
                    "type": "bool",
                    "maps_to": "Collection Date",
                    "category": "collection",
                    "importance": "medium"
                },
                {
                    "name": "Collection_Place_Problem",
                    "type": "bool",
                    "maps_to": "Collection Place",
                    "category": "collection",
                    "importance": "medium"
                },

                {
                    "name": "Box_Label_Problem",
                    "type": "bool",
                    "maps_to": "Box Label",
                    "category": "physical",
                    "importance": "medium"
                },

                {
                    "name": "Images_Problem",
                    "type": "bool",
                    "category": "media",
                    "importance": "workflow"
                },
                {
                    "name": "Other_problem",
                    "type": "bool",
                    "category": "notes",
                    "importance": "low"
                }
            ],

            # -------- UNKNOWN FIELDS --------
            "unknown_fields": [
                {
                  "name": "Unknown_Collector",
                  "maps_to": "Collector"
                },
                {
                  "name": "Unknown_Collection_Date",
                  "maps_to": "Collection Date"
                },
                {
                    "name": "Unknown_Collection_Place",
                    "maps_to": "Collection Place"
                }
            ]
        }
    },

    "Loan Tracking": {
        "has_images": False,
        "image_url_pattern": "",
        "sheets": {
            "reg": "Registration",
            "obs": "Observation",
            "photo": "Photo",
            "log": "Log",
        },
        "ui_sections": {
            "registration": [
                {"name": "Item Name", "type": "text"},
                {"name": "Borrower", "type": "text"},
                {"name": "Institution", "type": "text"},
                {"name": "Loan Date", "type": "text"},
                {"name": "Due Date", "type": "text"},
                {"name": "Return Date", "type": "text"},
                {"name": "Purpose", "type": "multiline"},
                {"name": "Status", "type": "choice", "choices": ["Active", "Returned", "Overdue", "Pending"]},
                {"name": "Notes", "type": "multiline"},
                {"name": "UID", "type": "text", "readonly": True}
            ],
            "reg_groups": [
                {"name": "Loan Details", "fields": ["Item Name", "Borrower", "Institution", "Purpose"]},
                {"name": "Schedule & Status", "fields": ["Loan Date", "Due Date", "Return Date", "Status"]},
                {"name": "Notes & Admin", "fields": ["Notes", "UID"]}
            ],
            "location": [
                {"name": "Building", "type": "text"},
                {"name": "Room", "type": "text"},
                {"name": "Cabinet", "type": "text"},
                {"name": "Shelf", "type": "text"},
                {"name": "Stored as", "type": "text"}
            ],
            "problems": [
                {"name": "Item_Name_Problem", "type": "bool", "maps_to": "Item Name", "category": "taxonomy", "importance": "high"},
                {"name": "Borrower_Problem", "type": "bool", "maps_to": "Borrower", "category": "collection", "importance": "medium"},
                {"name": "Due_Date_Problem", "type": "bool", "maps_to": "Due Date", "category": "collection", "importance": "high"},
                {"name": "Other_problem", "type": "bool", "category": "notes", "importance": "low"}
            ],
            "unknown_fields": []
        }
    },

    "Blank Minimal": {
        "has_images": False,
        "image_url_pattern": "",
        "sheets": {
            "reg": "Registration",
            "obs": "Observation",
            "photo": "Photo",
            "log": "Log",
        },
        "ui_sections": {
            "registration": [
                {"name": "Title", "type": "text"},
                {"name": "Category", "type": "text"},
                {"name": "Date", "type": "text"},
                {"name": "Status", "type": "choice", "choices": ["Active", "Draft", "Archived"]},
                {"name": "Description", "type": "multiline"},
                {"name": "Notes", "type": "multiline"},
                {"name": "UID", "type": "text", "readonly": True}
            ],
            "reg_groups": [
                {"name": "General Info", "fields": ["Title", "Category", "Date", "Status"]},
                {"name": "Content", "fields": ["Description", "Notes"]},
                {"name": "Admin", "fields": ["UID"]}
            ],
            "location": [
                {"name": "Location", "type": "text"},
                {"name": "Storage Unit", "type": "text"}
            ],
            "problems": [
                {"name": "Title_Problem", "type": "bool", "maps_to": "Title", "category": "taxonomy", "importance": "high"},
                {"name": "Date_Problem", "type": "bool", "maps_to": "Date", "category": "collection", "importance": "medium"},
                {"name": "Other_problem", "type": "bool", "category": "notes", "importance": "low"}
            ],
            "unknown_fields": []
        }
    }
}

# ==============================================================================
# PROBLEM CATEGORY THEMES & SEMANTIC METADATA
# Canonical colors, icons, badges, and priority rankings for workflow domains
# ==============================================================================
PROBLEM_CATEGORY_THEMES = {
    "taxonomy": {
        "label": "Taxonomy & Scientific Identity",
        "short_label": "Taxonomy",
        "icon": "🧬",
        "badge": "TAX",
        "color": "#c93a40",
        "color_dark": "#f28b82",
        "bg_light": "#fdf2f2",
        "border": "#c93a40",
        "rank": 1,
    },
    "collection": {
        "label": "Collection Event & Provenance",
        "short_label": "Provenance",
        "icon": "📦",
        "badge": "PROV",
        "color": "#d9a036",
        "color_dark": "#f59e0b",
        "bg_light": "#fef9e7",
        "border": "#d9a036",
        "rank": 2,
    },
    "physical": {
        "label": "Physical Object & Storage",
        "short_label": "Storage",
        "icon": "🏷️",
        "badge": "BOX",
        "color": "#795548",
        "color_dark": "#a1887f",
        "bg_light": "#fbfaf8",
        "border": "#795548",
        "rank": 3,
    },
    "media": {
        "label": "Media & Digitization Workflow",
        "short_label": "Media",
        "icon": "📷",
        "badge": "IMG",
        "color": "#0284c7",
        "color_dark": "#5ab0e8",
        "bg_light": "#f0f8ff",
        "border": "#0284c7",
        "rank": 4,
    },
    "notes": {
        "label": "Audit Notes & Other Discrepancies",
        "short_label": "Notes",
        "icon": "📝",
        "badge": "NOTE",
        "color": "#757d77",
        "color_dark": "#9399b2",
        "bg_light": "#f2f5f1",
        "border": "#757d77",
        "rank": 5,
    }
}

# Standard built-in starter template profiles for New Database Wizard
BUILTIN_TEMPLATES = {
    "Botany / Herbarium": {
        "description": "Standard botanical specimen & herbarium collection with taxonomy, collection data, and plant part tracking.",
        "icon": "🌿",
        "badge": "Specimen & Taxonomy",
        "config_key": "Økonomisk Botanisk"
    },
    "Loan Tracking": {
        "description": "Track outbound loans, borrower institutions, due dates, return statuses, and object conditions.",
        "icon": "📋",
        "badge": "Loans & Curatorial",
        "config_key": "Loan Tracking"
    },
    "Blank Minimal": {
        "description": "Clean, light starter schema with Title, Category, Date, Status, Description, and Notes.",
        "icon": "📄",
        "badge": "Minimal & Custom",
        "config_key": "Blank Minimal"
    }
}

# Banner theme configurations
BANNER_THEME = {
    "success": {"bg": "#eef8f0", "border": "#3a7d44", "fg": "#214a27", "icon": "✔"},
    "warning": {"bg": "#fcf5e3", "border": "#d9a036", "fg": "#5e4311", "icon": "⚠"},
    "error":   {"bg": "#f9e6e7", "border": "#c93a40", "fg": "#6e1d21", "icon": "✘"},
    "info":    {"bg": "#e9f0f5", "border": "#4a7b9d", "fg": "#264154", "icon": "ℹ"},
}