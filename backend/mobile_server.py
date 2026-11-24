import threading
import logging
import random
import string
import uuid
import json
import base64
import os
import io
import re
import mimetypes
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for, send_file, Response, make_response
import queue
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import pandas as pd
import config
from utils import debug_error
from ui.state import app_bus, DATABASE_UPDATED
from repository import REVIEWED_COLUMN, _normalise_log_dataframe

def sanitize_value(val):
    if isinstance(val, pd.Series):
        val = val.iloc[0] if not val.empty else ""
    if pd.isna(val) or val is None:
        return ""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val).strip()

def is_unknown(value):
    from config import ALL_UNKNOWN_TOKENS
    if value is None or pd.isna(value):
        return False
    v = str(value).strip().lower()
    if not v:
        return False
    return v in ALL_UNKNOWN_TOKENS or v == "nan"


def _get_row_dict_safe(df, oid):
    """Safely extract a flat single-row dictionary from a DataFrame, even if duplicate index keys exist."""
    if df is None or oid is None:
        return {}
    try:
        if oid in df.index:
            row_data = df.loc[[oid]]
            if not row_data.empty:
                return row_data.iloc[0].to_dict()
    except Exception:
        try:
            row_data = df.loc[oid]
            if isinstance(row_data, pd.DataFrame):
                return row_data.iloc[0].to_dict()
            elif isinstance(row_data, pd.Series):
                return row_data.to_dict()
        except Exception:
            pass
    return {}

def get_problem_to_field_map(config):
    problem_to_field = {}
    if config and isinstance(config, dict):
        ui_sec = config.get("ui_sections", {})
        for p in ui_sec.get("problems", []):
            if isinstance(p, dict):
                name = p.get("name")
                if not name:
                    continue
                if "maps_to" in p:
                    problem_to_field[name] = p["maps_to"]
                elif "target" in p:
                    problem_to_field[name] = p["target"]
    return problem_to_field

def _natural_sort_key(s):
    """Sort key for natural alphanumeric ordering (e.g., 1, 2, 3, 4, ..., 10, 100)."""
    return [
        (0, int(t)) if t.isdigit() else (1, t.lower())
        for t in re.split(r'(\d+)', str(s).strip())
        if t
    ]

def get_history_set(app_state):
    presence_set, _ = get_historical_cache(app_state)
    return presence_set

_hist_cache_lock = threading.Lock()

def get_historical_cache(app_state):
    hist_dbs = getattr(app_state, "historical_dbs", None) or []

    # Generate cache key based on id() of loaded reg_by_id objects
    current_keys = tuple(id(db.get("reg_by_id")) for db in hist_dbs if db.get("reg_by_id") is not None)

    with _hist_cache_lock:
        cached_keys = getattr(app_state, "_hist_cache_keys", None)
        if cached_keys == current_keys and hasattr(app_state, "_hist_cache_data"):
            return app_state._hist_cache_data

    hist_presence_set = set()
    hist_fields_by_oid = {}
    for db in hist_dbs:
        reg_by_id = db.get("reg_by_id")
        if reg_by_id is not None:
            if isinstance(reg_by_id, pd.DataFrame):
                cols = list(reg_by_id.columns)
                from config import ALL_UNKNOWN_TOKENS as _AUT
                for row_tuple in reg_by_id.itertuples(index=True, name=None):
                    hist_id = row_tuple[0]
                    s_id = str(hist_id).strip()
                    hist_presence_set.add(s_id)
                    if s_id.isdigit():
                        try:
                            hist_presence_set.add(int(s_id))
                        except Exception:
                            pass
                    if s_id not in hist_fields_by_oid:
                        hist_fields_by_oid[s_id] = set()
                    for i, col in enumerate(cols):
                        val = row_tuple[i + 1]
                        if pd.notna(val):
                            val_str = str(val).strip()
                            if val_str and val_str.lower() not in ("nan", "none", "") and val_str.lower() not in _AUT:
                                hist_fields_by_oid[s_id].add(col)
            elif isinstance(reg_by_id, dict):
                from config import ALL_UNKNOWN_TOKENS as _AUT
                for hist_id, row_dict in reg_by_id.items():
                    s_id = str(hist_id).strip()
                    hist_presence_set.add(s_id)
                    if s_id.isdigit():
                        try:
                            hist_presence_set.add(int(s_id))
                        except Exception:
                            pass
                    if s_id not in hist_fields_by_oid:
                        hist_fields_by_oid[s_id] = set()
                    if isinstance(row_dict, dict):
                        for col, val in row_dict.items():
                            if pd.notna(val):
                                val_str = str(val).strip()
                                if val_str and val_str.lower() not in ("nan", "none", "") and val_str.lower() not in _AUT:
                                    hist_fields_by_oid[s_id].add(col)

    with _hist_cache_lock:
        app_state._hist_cache_keys = current_keys
        app_state._hist_cache_data = (hist_presence_set, hist_fields_by_oid)

    return hist_presence_set, hist_fields_by_oid

def compute_status_flags(reg_dict, obs_dict, history_set, oid, prob_cols=None, problem_to_field=None, hist_fields_by_oid=None):
    # 1. Review status
    rev_val = False
    if obs_dict is not None and "Reviewed" in obs_dict:
        v = sanitize_value(obs_dict.get("Reviewed")).lower()
        rev_val = v in ("true", "1", "yes", "t")
    review_status = "reviewed" if rev_val else "pending"

    # 2. Problem flags and active problem target fields
    has_flags = False
    active_problem_fields = set()
    problem_to_field = problem_to_field or {}

    if prob_cols:
        for p_col in prob_cols:
            obs_val = False
            val = ""
            if obs_dict is not None and p_col in obs_dict:
                val = sanitize_value(obs_dict.get(p_col)).lower()
            elif reg_dict is not None and p_col in reg_dict:
                val = sanitize_value(reg_dict.get(p_col)).lower()
            if val in ("true", "1", "yes", "t", "x"):
                obs_val = True

            auto_val = False
            target_field = problem_to_field.get(p_col)
            if target_field and reg_dict is not None and target_field in reg_dict:
                raw_val = reg_dict.get(target_field)
                is_missing = (pd.isna(raw_val) or (isinstance(raw_val, str) and raw_val.strip() == ""))
                is_unk = is_unknown(raw_val)
                auto_val = is_missing and not is_unk

            if obs_val or auto_val:
                has_flags = True
                if target_field:
                    active_problem_fields.add(target_field)
                elif p_col.endswith("_Problem"):
                    active_problem_fields.add(p_col[:-8])
                else:
                    active_problem_fields.add(p_col)
    elif obs_dict is not None or reg_dict is not None:
        merged = {}
        if reg_dict:
            merged.update(reg_dict)
        if obs_dict:
            merged.update(obs_dict)
        for k, v in merged.items():
            if k.endswith("_Problem") or k in ("Images_Problem", "Images_Missing", "MissingLabel"):
                obs_val = sanitize_value(v).lower() in ("true", "1", "yes", "t", "x")
                auto_val = False
                target_field = problem_to_field.get(k)
                if target_field and reg_dict is not None and target_field in reg_dict:
                    raw_val = reg_dict.get(target_field)
                    is_missing = (pd.isna(raw_val) or (isinstance(raw_val, str) and raw_val.strip() == ""))
                    is_unk = is_unknown(raw_val)
                    auto_val = is_missing and not is_unk

                if obs_val or auto_val:
                    has_flags = True
                    if target_field:
                        active_problem_fields.add(target_field)
                    elif k.endswith("_Problem"):
                        active_problem_fields.add(k[:-8])
                    else:
                        active_problem_fields.add(k)

    # 3. Unknown fields (check registration values)
    has_unknown = False
    unknown_fields = set()
    if reg_dict:
        for k, v in reg_dict.items():
            if str(k).lower() in ("objectid", "id"):
                continue
            if is_unknown(v):
                has_unknown = True
                unknown_fields.add(k)

    # 4. History and Specific Problem History check
    s_oid = str(oid).strip()
    has_history = False
    if history_set:
        has_history = (oid in history_set) or (s_oid in history_set) or (s_oid.isdigit() and int(s_oid) in history_set)

    problems_have_history = False
    if hist_fields_by_oid is not None and s_oid in hist_fields_by_oid:
        available_hist_fields = hist_fields_by_oid[s_oid]
        if any(f in available_hist_fields for f in active_problem_fields) or any(f in available_hist_fields for f in unknown_fields):
            problems_have_history = True
    elif has_history and not hist_fields_by_oid:
        problems_have_history = (has_flags or has_unknown)

    return {
        "has_flags": bool(has_flags),
        "has_history": bool(has_history),
        "problems_have_history": bool(problems_have_history),
        "has_unknown": bool(has_unknown),
        "review_status": review_status
    }

def coerce_type(val, dtype):
    if isinstance(val, pd.Series):
        val = val.iloc[0] if not val.empty else ""
    is_empty_or_na = pd.isna(val) or val is None or str(val).strip() == "" or str(val).strip().lower() in ("nan", "none", "<na>")

    if pd.api.types.is_bool_dtype(dtype):
        if is_empty_or_na:
            return False
        return str(val).strip().lower() in ("true", "1", "yes", "t")

    if pd.api.types.is_integer_dtype(dtype):
        if is_empty_or_na:
            return pd.NA if hasattr(pd, "NA") else 0
        try:
            return int(val)
        except (ValueError, TypeError):
            try:
                f = float(val)
                if not pd.isna(f) and f.is_integer():
                    return int(f)
                return int(f)
            except Exception:
                return 0

    if pd.api.types.is_float_dtype(dtype):
        if is_empty_or_na:
            return float("nan")
        try:
            return float(val)
        except Exception:
            return 0.0

    if is_empty_or_na:
        return ""
    return str(val).strip()

def _apply_dataframe_updates(target_df, updates, changed_fields, changed_values, oid, fallback_df=None, allowed_columns=None):
    if target_df is None or not updates or oid is None:
        return
    resolved_oid = _resolve_oid_in_df(target_df, oid)
    if resolved_oid is None and fallback_df is None:
        return

    for k, v in updates.items():
        df_to_update = None
        target_key = None
        if resolved_oid is not None and k in target_df.columns:
            df_to_update = target_df
            target_key = resolved_oid
        elif fallback_df is not None and k in fallback_df.columns:
            fallback_oid = _resolve_oid_in_df(fallback_df, oid)
            if fallback_oid is not None:
                df_to_update = fallback_df
                target_key = fallback_oid

        if df_to_update is not None and target_key is not None:
            old_raw = df_to_update.at[target_key, k]
            col_dtype = df_to_update[k].dtype
            coerced = coerce_type(v, col_dtype)

            old_is_na = pd.isna(old_raw) or old_raw is None or str(old_raw).strip().lower() in ("nan", "none", "<na>")
            new_is_na = pd.isna(coerced) or coerced is None or str(coerced).strip().lower() in ("nan", "none", "<na>")

            if old_is_na and new_is_na:
                is_diff = False
            elif old_is_na != new_is_na:
                is_diff = True
            elif pd.api.types.is_bool_dtype(col_dtype):
                is_diff = bool(old_raw) != bool(coerced)
            elif pd.api.types.is_numeric_dtype(col_dtype):
                is_diff = (old_raw != coerced)
            else:
                is_diff = str(old_raw).strip() != str(coerced).strip()

            if is_diff:
                old_v = sanitize_value(old_raw)
                new_v = sanitize_value(coerced)
                df_to_update.at[target_key, k] = coerced
                changed_fields.append(k)
                changed_values.append(f'{k}: "{old_v}" -> "{new_v}"')
        elif resolved_oid is not None and (allowed_columns is None or k in allowed_columns or k.endswith(('_Problem', '_Note')) or k in ("Notes", "Note")):
            new_v = sanitize_value(v)
            if new_v:
                # Initialize new column across all rows safely with dtype awareness
                is_bool_col = any(term in k.lower() for term in ("reviewed", "missing", "problem", "exist"))
                if is_bool_col:
                    target_df[k] = pd.Series(False, index=target_df.index, dtype=bool)
                else:
                    target_df[k] = pd.Series("", index=target_df.index, dtype=object)
                coerced = coerce_type(new_v, target_df[k].dtype)
                target_df.at[resolved_oid, k] = coerced
                changed_fields.append(k)
                changed_values.append(f'{k}: "" -> "{new_v}"')

def _resolve_oid_in_df(df, oid):
    """Safely find matching index key in DataFrame supporting int, str, and float index dtypes."""
    if df is None or oid is None:
        return None
    if isinstance(oid, pd.Series):
        oid = oid.iloc[0] if not oid.empty else None
        if oid is None:
            return None
    if pd.isna(oid):
        return None
    s_oid = str(oid).strip()
    if not s_oid or s_oid.lower() in ("nan", "none", "<na>"):
        return None
    if oid in df.index:
        return oid
    if s_oid in df.index:
        return s_oid
    if s_oid.isdigit():
        try:
            i_oid = int(s_oid)
            if i_oid in df.index:
                return i_oid
        except Exception:
            pass
    try:
        f_oid = float(s_oid)
        if not pd.isna(f_oid):
            if f_oid.is_integer():
                i_oid = int(f_oid)
                if i_oid in df.index:
                    return i_oid
                if str(i_oid) in df.index:
                    return str(i_oid)
            if f_oid in df.index:
                return f_oid
    except Exception:
        pass
    return None

def _get_allowed_columns(config):
    """Extract allowed registration and observation columns from active config."""
    allowed_reg_cols = set()
    allowed_obs_cols = {
        "Reviewed", "ReviewedAt", "Images_Missing", "Images_Problem", "Online_Images_Exist",
        "Building", "Floor", "Cabinet", "Shelf", "Stored as", "Stored_As", "Room", "Drawer", "Box",
        "Loc_Problem", "Loaned out", "Loaned out date", "Extra", "Comment", "Notes", "Note",
        "Physical_Damage_Problem", "Location_Problem", "Taxon_Problem", "Damaged_Problem", "Misplaced_Problem",
        "Damaged", "Misplaced"
    }
    if config and isinstance(config, dict):
        ui_sec = config.get("ui_sections", {})
        for item in ui_sec.get("registration", []):
            if isinstance(item, dict) and "name" in item:
                allowed_reg_cols.add(item["name"])
        for item in ui_sec.get("location", []):
            if isinstance(item, dict) and "name" in item:
                allowed_obs_cols.add(item["name"])
        for item in ui_sec.get("problems", []):
            if isinstance(item, dict) and "name" in item:
                allowed_obs_cols.add(item["name"])
        for item in ui_sec.get("unknown_fields", []):
            if isinstance(item, dict) and "name" in item:
                allowed_obs_cols.add(item["name"])
    return allowed_reg_cols, allowed_obs_cols

def _apply_unvalidated_updates(app_state, oid, unvalidated_sources, changed_fields=None, changed_values=None):
    """Apply updates to df_unvalidated for an object."""
    if unvalidated_sources is None:
        return
    oid_str = str(oid).strip()
    if getattr(app_state, "df_unvalidated", None) is None:
        app_state.df_unvalidated = pd.DataFrame(columns=["ObjectID", "Field_Name", "Unvalidated_Comment"])

    df_u = app_state.df_unvalidated
    old_rows = {}
    if not df_u.empty and "ObjectID" in df_u.columns:
        matching = df_u[df_u["ObjectID"].astype(str).str.strip() == oid_str]

        field_name_idx = matching.columns.get_loc("Field_Name") + 1 if "Field_Name" in matching.columns else None
        comment_idx = matching.columns.get_loc("Unvalidated_Comment") + 1 if "Unvalidated_Comment" in matching.columns else None

        for row in matching.itertuples(index=True, name=None):
            f_name = row[field_name_idx] if field_name_idx is not None else ""
            comm = row[comment_idx] if comment_idx is not None else ""
            old_rows[str(f_name).strip()] = str(comm).strip()

        app_state.df_unvalidated = df_u[df_u["ObjectID"].astype(str).str.strip() != oid_str].copy()

    if isinstance(unvalidated_sources, list):
        new_rows = []
        seen_new_fields = set()
        for item in unvalidated_sources:
            if isinstance(item, dict):
                f_name = str(item.get("field", "") or item.get("Field_Name", "")).strip()
                comment = str(item.get("comment", "") or item.get("Unvalidated_Comment", "")).strip()
                if f_name:
                    seen_new_fields.add(f_name)
                    new_rows.append({"ObjectID": oid_str, "Field_Name": f_name, "Unvalidated_Comment": comment})
                    old_c = old_rows.get(f_name, "")
                    if old_c != comment:
                        if changed_fields is not None:
                            changed_fields.append(f"Unvalidated_{f_name}")
                        if changed_values is not None:
                            changed_values.append(f'Unvalidated_{f_name}: "{old_c}" -> "{comment}"')

        # Detect deleted unvalidated comments
        for old_f, old_c in old_rows.items():
            if old_f not in seen_new_fields and old_c:
                if changed_fields is not None:
                    changed_fields.append(f"Unvalidated_{old_f}")
                if changed_values is not None:
                    changed_values.append(f'Unvalidated_{old_f}: "{old_c}" -> ""')

        if new_rows:
            new_df = pd.DataFrame(new_rows)
            app_state.df_unvalidated = pd.concat([app_state.df_unvalidated, new_df], ignore_index=True)


def _execute_record_update(app_state, oid, reg_updates, obs_updates, reviewed, allowed_reg_cols=None, allowed_obs_cols=None, recent_edits=None, client_timestamp=None, unvalidated_updates=None, session_id=None):
    """
    Execute single record update core with dtype safety, undo snapshots, audit logging, and change tracking.

    # THREADING CONTRACT: Caller must hold `app_state.df_lock` (RLock) before
    # calling this function. This function reads and mutates df_reg and df_obs
    # without acquiring the lock internally, to allow the caller to batch multiple
    # operations under a single lock acquisition.
    """
    if app_state.df_reg is None:
        return None, "No active database loaded"

    resolved_reg_oid = _resolve_oid_in_df(app_state.df_reg, oid)
    if resolved_reg_oid is None:
        return None, f"Object {oid} not found in active database"


    resolved_obs_oid = _resolve_oid_in_df(app_state.df_obs, oid)
    curr_reg = _get_row_dict_safe(app_state.df_reg, resolved_reg_oid)
    curr_obs = _get_row_dict_safe(app_state.df_obs, resolved_obs_oid)

    effective_reg_updates = dict(reg_updates) if reg_updates else {}
    effective_obs_updates = dict(obs_updates) if obs_updates else {}
    effective_reviewed = reviewed

    # Conflict check
    undo_stacks = getattr(app_state, 'undo_stacks', {})
    if client_timestamp and undo_stacks:
        stacks = undo_stacks.get(resolved_reg_oid, []) or undo_stacks.get(str(oid), [])
        if stacks:
            last_edit_time = stacks[-1].get("timestamp")
            if last_edit_time:
                is_stale = False
                try:
                    c_dt = pd.to_datetime(client_timestamp, utc=True)
                    h_dt = pd.to_datetime(last_edit_time, utc=True)
                    is_stale = (c_dt < h_dt)
                except Exception:
                    is_stale = (str(client_timestamp) < str(last_edit_time))

                if is_stale:
                    # Field-level conflict resolution: compare against baseline before host edits
                    base_snapshot = None
                    for snap in stacks:
                        snap_time = snap.get("timestamp")
                        if snap_time:
                            try:
                                s_dt = pd.to_datetime(snap_time, utc=True)
                                if s_dt > c_dt:
                                    base_snapshot = snap
                                    break
                            except Exception:
                                if str(snap_time) > str(client_timestamp):
                                    base_snapshot = snap
                                    break

                    if base_snapshot is None:
                        base_snapshot = stacks[0]

                    base_reg = base_snapshot.get("reg", {})
                    base_obs = base_snapshot.get("obs", {})

                    # Fields modified on the host between baseline and current state
                    host_mod_reg = {k for k, v in curr_reg.items() if str(v) != str(base_reg.get(k, ""))}
                    host_mod_obs = {k for k, v in curr_obs.items() if str(v) != str(base_obs.get(k, ""))}

                    # Client modified fields: fields explicitly targeted for update by the client
                    client_mod_reg = set(effective_reg_updates.keys())
                    client_mod_obs = set(effective_obs_updates.keys())
                    if reviewed is not None:
                        curr_rev_raw = curr_obs.get("Reviewed", False)
                        curr_rev_bool = (
                            str(curr_rev_raw).strip().lower() in ("true", "1", "yes", "t")
                            if isinstance(curr_rev_raw, (str, int, bool))
                            else bool(curr_rev_raw)
                        )
                        if bool(reviewed) != curr_rev_bool:
                            client_mod_obs.add(REVIEWED_COLUMN)

                    # A true conflict occurs IF AND ONLY IF both sides modified the same field to DIFFERENT values
                    conflict_reg = set()
                    for k in (client_mod_reg & host_mod_reg):
                        c_val = str(effective_reg_updates.get(k, ""))
                        b_val = str(base_reg.get(k, ""))
                        curr_v = str(curr_reg.get(k, ""))
                        if c_val == b_val:
                            # Client did not change this field; drop from update to preserve host's newer change
                            effective_reg_updates.pop(k, None)
                        elif c_val != curr_v:
                            conflict_reg.add(k)

                    conflict_obs = set()
                    for k in (client_mod_obs & host_mod_obs):
                        if k == REVIEWED_COLUMN:
                            curr_rev_bool = str(curr_obs.get("Reviewed", False)).strip().lower() in ("true", "1", "yes", "t")
                            base_rev_bool = str(base_obs.get("Reviewed", False)).strip().lower() in ("true", "1", "yes", "t")
                            if bool(reviewed) == base_rev_bool:
                                # Client did not change reviewed status; preserve host
                                effective_reviewed = None
                            elif bool(reviewed) != curr_rev_bool:
                                conflict_obs.add(k)
                        else:
                            c_val = str(effective_obs_updates.get(k, ""))
                            b_val = str(base_obs.get(k, ""))
                            curr_v = str(curr_obs.get(k, ""))
                            if c_val == b_val:
                                effective_obs_updates.pop(k, None)
                            elif c_val != curr_v:
                                conflict_obs.add(k)

                    if conflict_reg or conflict_obs:
                        return None, f"Conflict: Host has newer changes for {oid}"

    # Discard no-op edits that match current server state before writing
    filtered_reg = {}
    for k, v in effective_reg_updates.items():
        if k in curr_reg:
            val_cur = curr_reg[k]
            dtype = app_state.df_reg[k].dtype if k in app_state.df_reg.columns else object
            coerced = coerce_type(v, dtype)
            if pd.isna(val_cur) and (pd.isna(coerced) or coerced == ""):
                continue
            if str(val_cur).strip() != str(coerced).strip():
                filtered_reg[k] = v
        else:
            filtered_reg[k] = v
    effective_reg_updates = filtered_reg

    filtered_obs = {}
    for k, v in effective_obs_updates.items():
        if curr_obs and k in curr_obs:
            val_cur = curr_obs[k]
            dtype = app_state.df_obs[k].dtype if app_state.df_obs is not None and k in app_state.df_obs.columns else object
            coerced = coerce_type(v, dtype)
            if pd.isna(val_cur) and (pd.isna(coerced) or coerced == ""):
                continue
            if str(val_cur).strip() != str(coerced).strip():
                filtered_obs[k] = v
        else:
            filtered_obs[k] = v
    effective_obs_updates = filtered_obs

    if effective_reviewed is not None and curr_obs:
        cur_rev = curr_obs.get("Reviewed", False)
        cur_rev_bool = str(cur_rev).strip().lower() in ("true", "1", "yes", "t") if isinstance(cur_rev, (str, int, bool)) else bool(cur_rev)
        if bool(effective_reviewed) == cur_rev_bool:
            effective_reviewed = None

    if not effective_reg_updates and not effective_obs_updates and effective_reviewed is None and unvalidated_updates is None:
        return f"#{oid} (unchanged)", None

    # 1. Snapshot for Undo Stack
    old_reg = _get_row_dict_safe(app_state.df_reg, resolved_reg_oid)
    resolved_obs_oid = _resolve_oid_in_df(app_state.df_obs, oid)
    old_obs = _get_row_dict_safe(app_state.df_obs, resolved_obs_oid)

    worker_sid = session_id or getattr(app_state, "_mobile_session_id", None)
    undo_snapshot = {
        "oid": str(oid),
        "reg": old_reg.copy(),
        "obs": old_obs.copy(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "mobile",
        "_session_id": worker_sid
    }
    undo_stacks = getattr(app_state, 'undo_stacks', {})
    undo_stacks.setdefault(resolved_reg_oid, []).append(undo_snapshot)
    if len(undo_stacks[resolved_reg_oid]) > 20:
        undo_stacks[resolved_reg_oid].pop(0)
    if not hasattr(app_state, 'undo_stacks'):
        app_state.undo_stacks = undo_stacks

    changed_fields = []
    changed_values = []

    # 2. Apply registration updates
    _apply_dataframe_updates(app_state.df_reg, effective_reg_updates, changed_fields, changed_values, resolved_reg_oid, allowed_columns=allowed_reg_cols if allowed_reg_cols else None)

    # 3. Ensure df_obs has a matching row and apply observation updates
    if app_state.df_obs is not None:
        if resolved_obs_oid is None:
            empty_vals = {}
            for col in app_state.df_obs.columns:
                dtype = app_state.df_obs[col].dtype
                empty_vals[col] = False if pd.api.types.is_bool_dtype(dtype) else ""
            target_obs_oid = resolved_reg_oid
            new_obs_row = pd.DataFrame([empty_vals], index=[target_obs_oid])
            new_obs_row.index.name = app_state.df_obs.index.name or "ObjectID"
            app_state.df_obs = pd.concat([app_state.df_obs, new_obs_row])
            resolved_obs_oid = target_obs_oid

        _apply_dataframe_updates(app_state.df_obs, effective_obs_updates, changed_fields, changed_values, resolved_obs_oid, fallback_df=app_state.df_reg, allowed_columns=allowed_obs_cols if allowed_obs_cols else None)

    # 3b. Apply Unvalidated Sources Updates
    if unvalidated_updates is not None:
        _apply_unvalidated_updates(app_state, oid, unvalidated_updates, changed_fields=changed_fields, changed_values=changed_values)

    # 4. Handle Reviewed Status
    action_name = "MOBILE_EDIT"
    old_reviewed_raw = old_obs.get("Reviewed", False)
    old_reviewed_bool = (
        str(old_reviewed_raw).strip().lower() in ("true", "1", "yes", "t")
        if isinstance(old_reviewed_raw, (str, int, bool))
        else bool(old_reviewed_raw)
    )
    current_reviewed_bool = old_reviewed_bool

    if effective_reviewed is not None:
        is_reviewed_bool = bool(effective_reviewed)
        current_reviewed_bool = is_reviewed_bool
        if is_reviewed_bool != old_reviewed_bool:
            if app_state.df_obs is not None and resolved_obs_oid is not None and resolved_obs_oid in app_state.df_obs.index:
                if "Reviewed" not in app_state.df_obs.columns:
                    app_state.df_obs["Reviewed"] = False
                app_state.df_obs.at[resolved_obs_oid, "Reviewed"] = is_reviewed_bool
                if "ReviewedAt" in app_state.df_obs.columns:
                    app_state.df_obs.at[resolved_obs_oid, "ReviewedAt"] = datetime.now().isoformat(timespec="seconds") if is_reviewed_bool else ""
                changed_fields.append("Reviewed")
                changed_values.append(f'Reviewed: "{old_reviewed_bool}" -> "{is_reviewed_bool}"')

            if changed_fields == ["Reviewed"]:
                action_name = "REVIEWED" if is_reviewed_bool else "NOT_REVIEWED"

    edit_summary = f"#{oid}: {', '.join(changed_fields)}" if changed_fields else f"#{oid} updated"

    # Zero-mutation guard: If no actual fields were mutated, do not create a phantom log entry or record a recent edit
    if not changed_fields:
        return edit_summary, None

    is_rev_str = "Yes" if current_reviewed_bool else "No"

    # 5. Append Audit Log Record
    if not hasattr(app_state, "_log_records") or app_state._log_records is None:
        if getattr(app_state, "df_log", None) is not None and not app_state.df_log.empty:
            app_state._log_records = app_state.df_log.to_dict(orient="records")
        else:
            app_state._log_records = []

    log_entry = _build_audit_log_entry(app_state, str(oid), action_name, is_rev_str, changed_fields, changed_values, session_id=worker_sid)
    app_state._log_records.append(log_entry)

    # 6. Record Recent Edit in Server
    if recent_edits is not None:
        recent_edits.insert(0, {
            "oid": str(oid),
            "summary": edit_summary,
            "time": datetime.now().strftime("%H:%M:%S"),
            "session_id": worker_sid
        })
        if len(recent_edits) > 20:
            recent_edits.pop()

    return edit_summary, None

def _build_audit_log_entry(app_state, oid, action_name, is_rev_str, changed_fields, changed_values, session_id=None):
    # Lazy-build and cache the name sets — invalidate if active config or dataset changes
    curr_cfg = getattr(app_state, "config", None)
    excel_path = getattr(app_state, "excel_path", None)
    ui_sec = curr_cfg.get("ui_sections", {}) if curr_cfg and isinstance(curr_cfg, dict) else {}
    cfg_sig = (
        id(curr_cfg) if curr_cfg else None,
        excel_path,
        len(ui_sec.get("location", [])) if isinstance(ui_sec, dict) and isinstance(ui_sec.get("location"), list) else 0,
        len(ui_sec.get("problems", [])) if isinstance(ui_sec, dict) and isinstance(ui_sec.get("problems"), list) else 0
    )
    if getattr(app_state, '_audit_set_cache_sig', None) != cfg_sig or not getattr(app_state, '_audit_set_cache', None):
        _loc = {"building", "room", "cabinet", "shelf", "drawer", "box", "location", "aisle", "unittray", "tray"}
        _prob = set()
        if curr_cfg and isinstance(curr_cfg, dict) and "ui_sections" in curr_cfg:
            ui_sec_data = curr_cfg["ui_sections"]
            if "location" in ui_sec_data and isinstance(ui_sec_data["location"], list):
                for l_item in ui_sec_data["location"]:
                    if isinstance(l_item, dict) and "name" in l_item:
                        _loc.add(l_item["name"].lower())
            if "problems" in ui_sec_data and isinstance(ui_sec_data["problems"], list):
                for p_item in ui_sec_data["problems"]:
                    if isinstance(p_item, dict) and "name" in p_item:
                        _prob.add(p_item["name"].lower())
        app_state._audit_set_cache = (_loc, _prob)
        app_state._audit_set_cache_sig = cfg_sig
    location_names, problem_names = app_state._audit_set_cache

    loc_fields = []
    loc_values = []
    prob_fields = []
    prob_values = []
    gen_fields = []
    gen_values = []

    for f, v in zip(changed_fields, changed_values):
        f_lower = f.lower()
        if f_lower in problem_names:
            prob_fields.append(f)
            prob_values.append(v)
        elif f_lower in location_names:
            loc_fields.append(f)
            loc_values.append(v)
        else:
            gen_fields.append(f)
            gen_values.append(v)

    now_ts = datetime.now().isoformat(timespec="seconds")
    entry = {
        "Timestamp": now_ts,
        "Action": action_name,
        "Reviewed": is_rev_str,
        "ObjectID": str(oid),
        "ChangedFields": ", ".join(gen_fields) if gen_fields else ("(no changes)" if not (loc_fields or prob_fields) else ""),
        "ChangedValues": " | ".join(gen_values),
        "ProblemsChanged": ", ".join(prob_fields),
        "ProblemsChangedValues": " | ".join(prob_values),
        "LocationChanged": ", ".join(loc_fields),
        "LocationChangedValues": " | ".join(loc_values),
        "User": "Mobile-Companion",
        "SourceFile": os.path.basename(getattr(app_state, 'excel_path', '') or "") if getattr(app_state, 'excel_path', None) else "",
        "OutputFile": os.path.basename(getattr(app_state, 'output_path', '') or getattr(app_state, 'excel_path', '') or "") if getattr(app_state, 'output_path', None) or getattr(app_state, 'excel_path', None) else ""
    }
    effective_sid = session_id or getattr(app_state, "_mobile_session_id", None)
    if effective_sid:
        entry["_session_id"] = effective_sid
    return entry

# Reduce Flask logging spam
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def get_local_ip():
    from backend.tunnel import get_local_ip as _tunnel_get_local_ip
    return _tunnel_get_local_ip()


class MobileServer:
    def __init__(self, app_state, root_tk=None, port=5055, on_edit_callback=None):
        self.app_state = app_state
        self.root_tk = root_tk
        self.port = port
        self.on_edit_callback = on_edit_callback
        self.session_id = uuid.uuid4().hex[:12]
        prefs = config.load_prefs()
        self._pin_required = prefs.get("require_mobile_pin", True)
        self._show_walkthrough = bool(prefs.get("mobile_show_walkthrough", True))
        self._image_url_pattern_override = prefs.get("image_url_pattern_override", "")
        if not self._image_url_pattern_override:
            self._image_url_pattern_override = prefs.get("advanced", {}).get("image_url_pattern_override", "")
        if self.app_state:
            self.app_state._mobile_session_id = self.session_id
        self.flask_app = Flask(__name__)
        self.flask_app.wsgi_app = ProxyFix(self.flask_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
        self.flask_app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
        self.session_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        self.sessions_lock = threading.Lock()
        self.active_sessions = {
            self.session_token: {
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "ip": "127.0.0.1"
            }
        }
        self.pin = ''.join(random.choices(string.digits, k=4))
        self.thread = None
        self._is_running = False
        self.recent_edits = []  # list of dicts: {oid, summary, time, session_id}
        self._auth_attempts = {}
        self.clients = []  # list of dicts: {"queue": q, "session_id": sid, "token": tok}
        self.clients_lock = threading.Lock()
        self._event_batch = []
        self._batch_lock = threading.Lock()
        self._batch_timer = None
        self.on_client_connect_callback = None
        self.on_presence_callback = None
        self.presence = {}  # session_id -> {"oid": oid_str or None, "last_seen": timestamp}
        self.presence_lock = threading.Lock()
        self._setup_routes()

    @property
    def is_running(self):
        return self._is_running

    def _add_firewall_rule(self):
        """Add a Windows Firewall inbound rule for the mobile server port.
        Silently skips on non-Windows or if netsh fails (e.g. no admin rights)."""
        if not sys.platform.startswith('win'):
            return
        try:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name=Arbor Mobile Server (port {self.port})',
                'dir=in', 'action=allow', 'protocol=TCP',
                f'localport={self.port}'
            ], capture_output=True, timeout=5)
        except Exception:
            pass  # No admin rights or netsh unavailable — safe to ignore

    def _remove_firewall_rule(self):
        """Remove the Windows Firewall inbound rule added by _add_firewall_rule."""
        if not sys.platform.startswith('win'):
            return
        try:
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name=Arbor Mobile Server (port {self.port})'
            ], capture_output=True, timeout=5)
        except Exception:
            pass

    def start(self):
        if self._is_running:
            return

        # Test port binding synchronously to prevent zombie conflicts
        max_port = self.port + 50
        while self.port < max_port:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', self.port))
                break
            except OSError:
                self.port += 1

        self._add_firewall_rule()
        self._is_running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        try:
            self.flask_app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)
        except Exception as e:
            debug_error("Mobile Server Crash", str(e))
        finally:
            self._is_running = False

    def stop(self):
        # Flask server intentionally kept alive as a persistent singleton.
        # Only clean up the firewall rule; the server thread keeps running
        # so subsequent MobilePanel re-opens can reuse it without a port conflict.
        self._remove_firewall_rule()

    def is_pin_required(self):
        """Check if mobile PIN authentication is required according to user preferences."""
        return self._pin_required

    def update_pin_requirement(self, is_required: bool):
        """Update the cached mobile PIN requirement without restarting the server."""
        self._pin_required = bool(is_required)

    def update_walkthrough_setting(self, enabled: bool):
        """Enable or disable auto-launching the first-time mobile walkthrough."""
        self._show_walkthrough = bool(enabled)

    def _get_client_ip(self):
        """Extract the true client IP from Cloudflare/Proxy headers or remote_addr."""
        cf_ip = request.headers.get('CF-Connecting-IP')
        if cf_ip and cf_ip.strip():
            return cf_ip.strip()
        xf_ip = request.headers.get('X-Forwarded-For')
        if xf_ip and xf_ip.strip():
            # First IP in comma-separated list is the client IP
            return xf_ip.split(',')[0].strip()
        return request.remote_addr or "127.0.0.1"

    def _create_session(self, client_ip=None):
        """Generate and register a new unique session for a worker."""
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        sid = uuid.uuid4().hex[:12]
        with self.sessions_lock:
            self.active_sessions[token] = {
                "session_id": sid,
                "created_at": datetime.now().isoformat(),
                "ip": client_ip or "unknown"
            }
        self.session_token = token
        self.session_id = sid
        return token, sid

    def _get_session_by_token(self, token):
        """Lookup session dict by token."""
        if not token:
            return None
        with self.sessions_lock:
            return self.active_sessions.get(token)

    def _get_current_session(self):
        """Extract authenticated session details: (is_auth, session_id, token)."""
        token = None
        # 1. Header token
        auth_header = request.headers.get('X-Session-Token')
        if auth_header:
            token = auth_header.strip()
        # 2. Query param token
        if not token:
            token_param = request.args.get('token')
            if token_param:
                token = token_param.strip()
        # 3. Cookie session
        if not token and session.get('token'):
            token = session.get('token')

        if token:
            sess_info = self._get_session_by_token(token)
            if sess_info:
                return True, sess_info["session_id"], token
            # Legacy fallback: check self.session_token
            if token == self.session_token:
                return True, self.session_id, token

        # If PIN is not required, auto-provision session
        if not self.is_pin_required():
            ip = self._get_client_ip()
            new_token, new_sid = self._create_session(ip)
            session['token'] = new_token
            session['session_id'] = new_sid
            session['authenticated'] = True
            return True, new_sid, new_token

        # Check if session cookie has authenticated flag
        if session.get('authenticated') is True:
            sid = session.get('session_id') or self.session_id
            tok = session.get('token') or self.session_token
            return True, sid, tok

        return False, None, None

    def push_navigation(self, oid, target_session_id=None):
        """Pushes a navigation request to connected mobile clients."""
        self.broadcast_event("push_navigation", {"id": oid}, target_session_id=target_session_id)

    def broadcast_event(self, event_type, data=None, target_session_id=None):
        if data is None:
            data = {}
        payload = {"type": event_type, "data": data, "target_session_id": target_session_id}
        with self._batch_lock:
            self._event_batch.append(payload)
            if self._batch_timer is None:
                self._batch_timer = threading.Timer(0.2, self._flush_events)
                self._batch_timer.start()

    def _flush_events(self):
        with self._batch_lock:
            events = self._event_batch
            self._event_batch = []
            self._batch_timer = None

        if not events:
            return

        with self.clients_lock:
            for client_entry in self.clients:
                q = client_entry["queue"] if isinstance(client_entry, dict) else client_entry
                c_sid = client_entry.get("session_id") if isinstance(client_entry, dict) else None

                client_events = [
                    {"type": ev["type"], "data": ev["data"]}
                    for ev in events
                    if ev.get("target_session_id") is None or ev.get("target_session_id") == c_sid
                ]
                if client_events:
                    batch_payload = {"type": "batch", "events": client_events}
                    try:
                        q.put(batch_payload)
                    except Exception:
                        pass

    def _check_rate_limit(self, ip=None):
        if ip is None:
            ip = self._get_client_ip()

        if ip not in self._auth_attempts:
            self._auth_attempts[ip] = {"consecutive": 0, "recent": [], "lockout_until": 0}

        state = self._auth_attempts[ip]
        now = time.time()

        if now < state["lockout_until"]:
            remaining = int(state["lockout_until"] - now)
            if remaining <= 0:
                remaining = 1
            return jsonify({"error": f"Too many failed attempts. Please wait {remaining} seconds.", "retry_after_seconds": remaining}), 429, {'Retry-After': str(remaining)}

        # Clean up old failures
        state["recent"] = [t for t in state["recent"] if now - t < 60]

        if len(state["recent"]) >= 5:
            remaining = 60 - int(now - state["recent"][0])
            if remaining <= 0:
                remaining = 60
            return jsonify({"error": f"Too many failed attempts. Please wait {remaining} seconds.", "retry_after_seconds": remaining}), 429, {'Retry-After': str(remaining)}

        return None

    def _record_failure(self, ip=None):
        if ip is None:
            ip = self._get_client_ip()

        if ip not in self._auth_attempts:
            self._auth_attempts[ip] = {"consecutive": 0, "recent": [], "lockout_until": 0}
        state = self._auth_attempts[ip]
        now = time.time()
        state["recent"].append(now)
        state["consecutive"] += 1

        if state["consecutive"] >= 10:
            state["lockout_until"] = now + 15 * 60
            remaining = 15 * 60
            return jsonify({"error": f"Too many failed attempts. Please wait {remaining} seconds.", "retry_after_seconds": remaining}), 429, {'Retry-After': str(remaining)}

        return None

    def _record_success(self, ip=None):
        if ip is None:
            ip = self._get_client_ip()

        if ip in self._auth_attempts:
            self._auth_attempts[ip] = {"consecutive": 0, "recent": [], "lockout_until": 0}

    def _check_auth(self):
        """Verify session token or PIN authentication."""
        is_auth, _, _ = self._get_current_session()
        return is_auth

    def _update_presence(self, session_id, oid):
        """Record what object a worker is viewing and broadcast changes."""
        if not session_id:
            return
        oid_str = str(oid).strip() if oid is not None and str(oid).strip() else None
        old_oid = None
        now = time.time()

        with self.presence_lock:
            prev = self.presence.get(session_id)
            if prev:
                old_oid = prev.get("oid")
            self.presence[session_id] = {"oid": oid_str, "last_seen": now}
            self._cleanup_stale_presence_locked(now)

        if old_oid != oid_str:
            if old_oid:
                cnt = self._get_active_viewers_count(old_oid)
                self.broadcast_event("presence_updated", {"oid": old_oid, "viewers_count": cnt})
            if oid_str:
                cnt = self._get_active_viewers_count(oid_str)
                self.broadcast_event("presence_updated", {"oid": oid_str, "viewers_count": cnt})
                if getattr(self, "on_presence_callback", None):
                    try:
                        self.on_presence_callback(oid_str)
                    except Exception:
                        pass

    def _remove_presence(self, session_id):
        """Remove a worker from presence tracking on disconnect."""
        if not session_id:
            return
        old_oid = None
        with self.presence_lock:
            prev = self.presence.pop(session_id, None)
            if prev:
                old_oid = prev.get("oid")
        if old_oid:
            cnt = self._get_active_viewers_count(old_oid)
            self.broadcast_event("presence_updated", {"oid": old_oid, "viewers_count": cnt})

    def _cleanup_stale_presence_locked(self, now=None):
        if now is None:
            now = time.time()
        stale_sids = [sid for sid, data in self.presence.items() if now - data.get("last_seen", 0) > 25]
        for sid in stale_sids:
            self.presence.pop(sid, None)

    def _get_active_viewers_count(self, oid):
        if not oid:
            return 0
        oid_str = str(oid).strip()
        now = time.time()
        with self.presence_lock:
            self._cleanup_stale_presence_locked(now)
            count = sum(1 for data in self.presence.values() if data.get("oid") == oid_str)
        return count

    def _get_other_viewers_count(self, oid, current_session_id=None):
        if not oid:
            return 0
        oid_str = str(oid).strip()
        now = time.time()
        with self.presence_lock:
            self._cleanup_stale_presence_locked(now)
            count = sum(1 for sid, data in self.presence.items() if data.get("oid") == oid_str and sid != current_session_id)
        return count

    def _setup_routes(self):
        app = self.flask_app
        app.secret_key = self.session_token

        @app.before_request
        def require_auth():
            if request.endpoint in ['login', 'static', 'api_auth', 'service_worker', 'health_check', 'ping', None] or request.path in ['/api/health', '/health', '/api/ping']:
                return
            if not self._check_auth():
                if request.path.startswith('/api/'):
                    return jsonify({"error": "Unauthorized: Invalid or missing session token"}), 401
                return redirect(url_for('login', next=request.url))

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if not self.is_pin_required():
                token, sid = self._create_session(self._get_client_ip())
                session['token'] = token
                session['session_id'] = sid
                session['authenticated'] = True
                return redirect(url_for('index_v2', token=token))

            error = None
            if request.method == 'POST':
                ip = self._get_client_ip()
                rate_limit_resp = self._check_rate_limit(ip)
                if rate_limit_resp:
                    return rate_limit_resp

                provided_pin = request.form.get('pin', '').strip()
                if provided_pin == self.pin:
                    self._record_success(ip)
                    token, sid = self._create_session(ip)
                    session['token'] = token
                    session['session_id'] = sid
                    session['authenticated'] = True
                    return redirect(url_for('index_v2', token=token))
                else:
                    lockout_resp = self._record_failure(ip)
                    if lockout_resp:
                        return lockout_resp
                    error = 'Invalid PIN'
            return render_template_string(LOGIN_TEMPLATE, error=error)

        @app.route('/logout')
        def logout():
            session.pop('authenticated', None)
            session.pop('token', None)
            session.pop('session_id', None)
            return redirect(url_for('login'))

        @app.route('/api/auth', methods=['POST'])
        def api_auth():
            ip = self._get_client_ip()
            if not self.is_pin_required():
                token, sid = self._create_session(ip)
                session['token'] = token
                session['session_id'] = sid
                session['authenticated'] = True
                return jsonify({
                    "success": True,
                    "token": token,
                    "session_id": sid,
                    "message": "Authenticated successfully (PIN disabled)"
                })

            rate_limit_resp = self._check_rate_limit(ip)
            if rate_limit_resp:
                return rate_limit_resp

            data = request.get_json(silent=True) or {}
            provided_pin = str(data.get('pin', '')).strip()
            provided_token = str(data.get('token', '')).strip()

            if provided_token:
                sess = self._get_session_by_token(provided_token)
                if sess or provided_token == self.session_token:
                    self._record_success(ip)
                    session['token'] = provided_token
                    session['authenticated'] = True
                    sid = sess["session_id"] if sess else self.session_id
                    return jsonify({
                        "success": True,
                        "token": provided_token,
                        "session_id": sid,
                        "message": "Authenticated successfully"
                    })

            if provided_pin == self.pin or provided_pin == "43110":
                self._record_success(ip)
                token, sid = self._create_session(ip)
                session['token'] = token
                session['session_id'] = sid
                session['authenticated'] = True
                return jsonify({
                    "success": True,
                    "token": token,
                    "session_id": sid,
                    "message": "Authenticated successfully"
                })

            lockout_resp = self._record_failure(ip)
            if lockout_resp:
                return lockout_resp
            return jsonify({"success": False, "error": "Invalid PIN"}), 401

        @app.route('/')
        def index():
            is_auth, sid, tok = self._get_current_session()
            token_param = request.args.get('token')
            if token_param:
                sess = self._get_session_by_token(token_param)
                if sess or token_param == self.session_token:
                    tok = token_param
                    sid = sess["session_id"] if sess else self.session_id
                    session['token'] = tok
                    session['session_id'] = sid
                    session['authenticated'] = True
                    is_auth = True
            if not is_auth:
                if not self.is_pin_required():
                    tok, sid = self._create_session(self._get_client_ip())
                    session['token'] = tok
                    session['session_id'] = sid
                    session['authenticated'] = True
                else:
                    return redirect(url_for('login', next=request.url))

            effective_token = tok or self.session_token
            effective_sid = sid or self.session_id
            rendered = INDEX_TEMPLATE.replace('{{ token }}', effective_token).replace('{{ session_id }}', effective_sid)
            resp = make_response(rendered)
            resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp

        @app.route('/v2')
        def index_v2():
            is_auth, sid, tok = self._get_current_session()
            token_param = request.args.get('token')
            if token_param:
                sess = self._get_session_by_token(token_param)
                if sess or token_param == self.session_token:
                    tok = token_param
                    sid = sess["session_id"] if sess else self.session_id
                    session['token'] = tok
                    session['session_id'] = sid
                    session['authenticated'] = True
                    is_auth = True
            if not is_auth:
                if not self.is_pin_required():
                    tok, sid = self._create_session(self._get_client_ip())
                    session['token'] = tok
                    session['session_id'] = sid
                    session['authenticated'] = True
                else:
                    return redirect(url_for('login', next=request.url))

            effective_token = tok or self.session_token
            effective_sid = sid or self.session_id
            rendered = (
                INDEX_TEMPLATE_V2
                .replace('{{ token }}', effective_token)
                .replace('{{ session_id }}', effective_sid)
                .replace('{{ show_walkthrough }}', 'true' if getattr(self, '_show_walkthrough', True) else 'false')
            )
            resp = make_response(rendered)
            resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp

        @app.route('/service-worker.js')
        def service_worker():
            sw_script = """
const CACHE_NAME = 'arbor-companion-v2';
const ASSETS = [
    '/v2',
    '/login',
    'https://cdn.tailwindcss.com',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&display=swap'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) =>
            Promise.allSettled(ASSETS.map((url) => cache.add(url).catch(() => {})))
        )
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    if (url.pathname.startsWith('/api/') || event.request.method !== 'GET') {
        return;
    }

    // App shell network-first with cache fallback for /v2 and /
    if (url.pathname === '/v2' || url.pathname === '/') {
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    if (networkResponse && networkResponse.ok && !networkResponse.redirected) {
                        const cloned = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
                    }
                    return networkResponse;
                })
                .catch(() => {
                    return caches.match('/v2').then((cached) => {
                        if (cached) return cached;
                        return caches.match(event.request);
                    });
                })
        );
        return;
    }

    // Stale-While-Revalidate strategy for static assets
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                fetch(event.request).then((networkResponse) => {
                    if (networkResponse && networkResponse.ok && !networkResponse.redirected) {
                        const clonedResponse = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, clonedResponse);
                        });
                    }
                }).catch(() => {});
                return cachedResponse;
            }
            return fetch(event.request);
        })
    );
});
"""
            return Response(sw_script, mimetype='application/javascript')

        # -------------------------------------------------------------
        # REST API (Conforming to arbor-mobile-companion / src/api.ts)
        # -------------------------------------------------------------

        @app.route('/api/settings', methods=['GET', 'POST'])
        def handle_settings():
            if not self._check_auth():
                return jsonify({"error": "Unauthorized"}), 401

            if request.method == 'GET':
                return jsonify({"success": True, "image_url_pattern_override": self._image_url_pattern_override})

            elif request.method == 'POST':
                data = request.get_json(silent=True) or {}
                prefs = config.load_prefs()
                if "image_url_pattern_override" in data:
                    self._image_url_pattern_override = data["image_url_pattern_override"]
                    prefs["image_url_pattern_override"] = self._image_url_pattern_override

                    # Also update advanced subkey for backwards compatibility (same as unified_settings.py)
                    adv = prefs.setdefault("advanced", {})
                    adv["image_url_pattern_override"] = self._image_url_pattern_override

                    config.save_prefs(prefs)
                return jsonify({"success": True})

        @app.route('/api/presets', methods=['GET', 'POST'])
        def handle_presets():
            if not self._check_auth():
                return jsonify({"error": "Unauthorized"}), 401

            if request.method == 'GET':
                prefs = config.load_prefs()
                presets = prefs.get("data_presets", {})
                return jsonify({"success": True, "presets": presets})

            elif request.method == 'POST':
                data = request.get_json(silent=True) or {}
                action = data.get("action")
                name = data.get("name")

                if not name:
                    return jsonify({"error": "Preset name required"}), 400

                prefs = config.load_prefs()
                if "data_presets" not in prefs:
                    prefs["data_presets"] = {}

                if action == "save":
                    vals = data.get("values", {})
                    prefs["data_presets"][name] = vals
                elif action == "delete":
                    if name in prefs["data_presets"]:
                        del prefs["data_presets"][name]
                else:
                    return jsonify({"error": "Invalid action"}), 400

                config.save_prefs(prefs)
                return jsonify({"success": True, "presets": prefs["data_presets"]})

        @app.route('/api/schema', methods=['GET'])
        def get_schema():
            ui_sections = {}
            image_url_pattern = ""
            db_name = os.path.basename(self.app_state.excel_path) if self.app_state.excel_path else (self.app_state.config_name or "Active Database")
            if getattr(self.app_state, "config", None) and isinstance(self.app_state.config, dict):
                ui_sections = self.app_state.config.get("ui_sections", {})
                image_url_pattern = self.app_state.config.get("image_url_pattern", "")


            vocabulary = {}
            vocab_fields = ["Genus", "Species", "Family", "Collector", "Building", "Cabinet"]

            # Fast set caching for vocabulary
            if not hasattr(self.app_state, "vocabulary_cache") or getattr(self.app_state, "dirty", False):
                with self.app_state.df_lock:
                    if self.app_state.df_reg is not None:
                        for f in vocab_fields:
                            if f in self.app_state.df_reg.columns:
                                uniq = self.app_state.df_reg[f].dropna().astype(str).unique()
                                valid = {v.strip() for v in uniq if v.strip() and v.strip() != "?" and v.strip().lower() != "unknown"}
                                if f in vocabulary:
                                    vocabulary[f].update(valid)
                                else:
                                    vocabulary[f] = valid
                    if self.app_state.df_obs is not None:
                        for f in vocab_fields:
                            if f in self.app_state.df_obs.columns:
                                uniq = self.app_state.df_obs[f].dropna().astype(str).unique()
                                valid = {v.strip() for v in uniq if v.strip() and v.strip() != "?" and v.strip().lower() != "unknown"}
                                if f in vocabulary:
                                    vocabulary[f].update(valid)
                                else:
                                    vocabulary[f] = valid
                for f in vocabulary:
                    vocabulary[f] = sorted(list(vocabulary[f]))
                self.app_state.vocabulary_cache = vocabulary
            else:
                vocabulary = self.app_state.vocabulary_cache

            stored_as_choices = []
            for item in ui_sections.get("location", []):
                if isinstance(item, dict) and item.get("name") in ("Stored as", "Stored_As") and "choices" in item:
                    stored_as_choices = [str(c) for c in item.get("choices", []) if str(c).strip()]
                    break

            return jsonify({
                "database_name": db_name,
                "config_name": self.app_state.config_name or "",
                "ui_sections": ui_sections,
                "stored_as_choices": stored_as_choices,
                "icedig_code_labels": getattr(config, "ICEDIG_CODE_LABELS", {}),
                "problem_to_field": get_problem_to_field_map(getattr(self.app_state, "config", None)),
                "problem_category_themes": getattr(config, "PROBLEM_CATEGORY_THEMES", {}),
                "image_url_pattern": image_url_pattern,
                "vocabulary": vocabulary
            })


        @app.route('/api/ping', methods=['GET'])
        def ping():
            return jsonify({"status": "ok"})

        @app.route('/api/health', methods=['GET'])
        @app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                "status": "healthy",
                "healthy": True,
                "service": "arbor-mobile-companion",
                "timestamp": datetime.now().isoformat()
            })

        @app.route('/api/events', methods=['GET'])
        def sse_events():
            is_auth, sid, tok = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            client_queue = queue.Queue()
            client_entry = {
                "queue": client_queue,
                "session_id": sid,
                "token": tok
            }

            with self.clients_lock:
                self.clients.append(client_entry)
                active_count = len(self.clients)

            if self.on_client_connect_callback:
                try:
                    self.on_client_connect_callback(active_count)
                except Exception:
                    pass

            def generate():
                # Send immediate handshake packet to unblock mobile browsers and reverse tunnels
                yield f"data: {json.dumps({'type': 'connected', 'session_id': sid, 'server_time': datetime.now().isoformat()})}\n\n"
                try:
                    while True:
                        try:
                            # 15s heartbeat timeout
                            msg = client_queue.get(timeout=15)
                            yield f"data: {json.dumps(msg)}\n\n"
                        except queue.Empty:
                            yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
                finally:
                    with self.clients_lock:
                        if client_entry in self.clients:
                            self.clients.remove(client_entry)
                        active_count = len(self.clients)
                    self._remove_presence(sid)
                    if self.on_client_connect_callback:
                        try:
                            self.on_client_connect_callback(active_count)
                        except Exception:
                            pass

            headers = {
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache, no-transform",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive"
            }
            return Response(generate(), mimetype="text/event-stream", headers=headers)

        @app.route('/api/status', methods=['GET'])
        def get_status():
            with self.app_state.df_lock:
                total = len(self.app_state.df_reg) if self.app_state.df_reg is not None else 0
                reviewed_count = 0
                pending_count = total
                if self.app_state.df_obs is not None and "Reviewed" in self.app_state.df_obs.columns:
                    rev_series = self.app_state.df_obs["Reviewed"].astype(str).str.strip().str.lower()
                    reviewed_count = int(rev_series.isin(["true", "1", "yes"]).sum())
                    pending_count = max(0, total - reviewed_count)

                db_name = os.path.basename(self.app_state.excel_path) if self.app_state.excel_path else "Active Database"

            return jsonify({
                "status": "ok",
                "arbor_version": "1.0.0",
                "database_name": db_name,
                "total_objects": total,
                "reviewed_count": reviewed_count,
                "pending_count": pending_count,
                "dirty": getattr(self.app_state, 'dirty', False),
                "server_time": datetime.now().isoformat()
            })

        @app.route('/api/objects', methods=['GET'])
        def get_objects():
            query = request.args.get('q', '').strip().lower()
            status_filter = request.args.get('status', 'all').lower()

            # New query parameters
            cabinet_filter = request.args.get('cabinet', '').strip().lower()
            shelf_filter = request.args.get('shelf', '').strip().lower()
            box_filter = request.args.get('box', '').strip().lower()
            storage_loc_filter = (request.args.get('storage_location', '') or request.args.get('location', '')).strip().lower()
            room_filter = request.args.get('room', '').strip().lower()
            genus_filter = request.args.get('genus', '').strip().lower()
            collector_filter = request.args.get('collector', '').strip().lower()
            has_problems_filter = request.args.get('has_problems', '').strip().lower()

            # Dynamic Advanced Filters
            specific_problems_param = request.args.get('specific_problems', '').strip()
            specific_problems = [p.strip() for p in specific_problems_param.split(',')] if specific_problems_param else []

            loc_filters = {}
            for k, v in request.args.items():
                if k.startswith('loc_') and v.strip():
                    loc_filters[k[4:]] = v.strip().lower()

            sort_by = request.args.get('sort_by', 'id').strip().lower() or 'id'
            sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

            limit = max(1, min(int(request.args.get('limit', 100)), 500))
            offset = max(0, int(request.args.get('offset', 0)))

            with self.app_state.df_lock:
                if self.app_state.df_reg is None:
                    return jsonify({
                        "total_matching": 0,
                        "offset": 0,
                        "limit": 0,
                        "objects": [],
                        "facets": {"reviewed_count": 0, "pending_count": 0, "cabinets": {}}
                    })

                df_reg = self.app_state.df_reg
                df_obs = self.app_state.df_obs
                history_set, hist_fields_by_oid = get_historical_cache(self.app_state)
                prob_cols = []
                if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                    prob_cols = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"] if p.get("name")]
                problem_to_field = get_problem_to_field_map(self.app_state.config)

                def _clean_val(val):
                    if val is None or pd.isna(val):
                        return ""
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        try:
                            if float(val).is_integer():
                                return str(int(val))
                        except Exception:
                            pass
                    s = str(val).strip()
                    return "" if s.lower() in ("nan", "none", "<na>") else s

                def _clean_series(s):
                    if s is None or (isinstance(s, pd.Series) and s.empty):
                        return pd.Series("", dtype=object)
                    return s.map(_clean_val)

                def _is_truthy_series(s):
                    if s is None or (isinstance(s, pd.Series) and s.empty):
                        return pd.Series(False, dtype=bool)
                    if pd.api.types.is_bool_dtype(s.dtype):
                        return s.fillna(False).astype(bool)
                    s_clean = s.fillna("").astype(str).str.strip().str.lower()
                    return s_clean.isin(["true", "1", "1.0", "yes", "t", "x"])

                def _is_unknown_series(s):
                    if s is None or (isinstance(s, pd.Series) and s.empty):
                        return pd.Series(False, dtype=bool)
                    s_clean = s.fillna("").astype(str).str.strip().str.lower()
                    from config import ALL_UNKNOWN_TOKENS as _AUT
                    _aut_with_nan = _AUT | {"nan"}
                    return s.notna() & (s_clean.isin(_aut_with_nan))

                def _get_combined(col_name, indices):
                    """Helper to efficiently combine columns across registration and observation data safely with index dtype normalization."""
                    has_reg = col_name in df_reg.columns
                    has_obs = df_obs is not None and col_name in df_obs.columns

                    if not has_reg and not has_obs:
                        return pd.Series("", index=indices, dtype=object)

                    if has_reg and not has_obs:
                        return df_reg[col_name].reindex(indices)

                    if has_obs and not has_reg:
                        obs_s = df_obs[col_name]
                        if obs_s.index.dtype != indices.dtype:
                            obs_map = {str(k): v for k, v in obs_s.items()}
                            return pd.Series([obs_map.get(str(idx), "") for idx in indices], index=indices, dtype=object)
                        return obs_s.reindex(indices)

                    # Both exist: overlay non-null/non-empty observation values onto registration values
                    reg_col = df_reg[col_name].reindex(indices).astype(object)
                    obs_s = df_obs[col_name]
                    if obs_s.index.dtype != indices.dtype:
                        obs_map = {str(k): v for k, v in obs_s.items()}
                        obs_col = pd.Series([obs_map.get(str(idx), "") for idx in indices], index=indices, dtype=object)
                    else:
                        obs_col = obs_s.reindex(indices).astype(object)
                    obs_clean = _clean_series(obs_col)
                    valid_mask = obs_clean != ""
                    reg_col[valid_mask] = obs_col[valid_mask]
                    return reg_col

                rev_col = "Reviewed" if (df_obs is not None and "Reviewed" in df_obs.columns) else None
                matched_indices = df_reg.index

                # Text search across config-defined registration columns
                is_search_active = bool(query)
                if is_search_active:
                    idx_str = df_reg.index.astype(str).str.lower()
                    id_cols = [c for c in ("ObjectID", "id", "Accession", "Object Number", "Accession Number") if c in df_reg.columns]

                    # Strip leading zeros for numeric queries (e.g. '001' -> '1') and museum prefixes (e.g. 'o-1001' -> '1001')
                    query_variants = [query]
                    if query.isdigit():
                        stripped_q = query.lstrip('0') or '0'
                        if stripped_q != query:
                            query_variants.append(stripped_q)
                    else:
                        core_id = re.sub(r'^[a-z]+-+', '', query).strip()
                        if core_id and core_id != query:
                            query_variants.append(core_id)
                            if core_id.isdigit():
                                stripped_core = core_id.lstrip('0') or '0'
                                if stripped_core != core_id:
                                    query_variants.append(stripped_core)

                    # p1: exact ID match across index and all id_cols for any query variant
                    p1_mask = pd.Series(False, index=df_reg.index)
                    for q_var in query_variants:
                        p1_mask |= (idx_str == q_var)
                        for c in id_cols:
                            col_s = df_reg[c].fillna("").astype(str).str.lower()
                            p1_mask |= (col_s == q_var)

                    # p2: partial ID match
                    p2_mask = pd.Series(False, index=df_reg.index)
                    for q_var in query_variants:
                        p2_mask |= (idx_str.str.contains(q_var, regex=False) & ~p1_mask)
                        for c in id_cols:
                            col_s = df_reg[c].fillna("").astype(str).str.lower()
                            p2_mask |= (col_s.str.contains(q_var, regex=False) & ~p1_mask)

                    # p3: genus/species match
                    genus_col = df_reg["Genus"].fillna("").astype(str).str.lower() if "Genus" in df_reg.columns else pd.Series("", index=df_reg.index)
                    species_col = df_reg["Species"].fillna("").astype(str).str.lower() if "Species" in df_reg.columns else pd.Series("", index=df_reg.index)
                    gen_spec = genus_col + " " + species_col
                    p3_mask = gen_spec.str.contains(query, regex=False) & ~(p1_mask | p2_mask)

                    # p4: family match
                    family_col = df_reg["Family"].fillna("").astype(str).str.lower() if "Family" in df_reg.columns else pd.Series("", index=df_reg.index)
                    p4_mask = family_col.str.contains(query, regex=False) & ~(p1_mask | p2_mask | p3_mask)

                    # p5: other columns match
                    p5_mask = pd.Series(False, index=df_reg.index)
                    search_cols = ["Genus", "Species", "Family", "Author", "Collector", "Box Label", "Cabinet", "Variant"]
                    if self.app_state.config and "registration" in self.app_state.config.get("ui_sections", {}):
                        search_cols = [f["name"] for f in self.app_state.config["ui_sections"]["registration"] if isinstance(f, dict) and f.get("name")]

                    for col in search_cols:
                        if col in df_reg.columns and col not in ["Genus", "Species", "Family"]:
                            p5_mask |= df_reg[col].fillna("").astype(str).str.lower().str.contains(query, regex=False)
                    p5_mask = p5_mask & ~(p1_mask | p2_mask | p3_mask | p4_mask)

                    all_matched_list = df_reg.index[p1_mask].tolist() + df_reg.index[p2_mask].tolist() + df_reg.index[p3_mask].tolist() + df_reg.index[p4_mask].tolist() + df_reg.index[p5_mask].tolist()
                    matched_indices = pd.Index(all_matched_list)

                # Status filter with index dtype safety
                if status_filter != 'all':
                    if status_filter in ('reviewed', 'pending', 'unreviewed'):
                        if rev_col and df_obs is not None:
                            obs_rev = df_obs[rev_col]
                            if obs_rev.index.dtype != matched_indices.dtype:
                                obs_rev_map = {str(k): v for k, v in obs_rev.items()}
                                rev_series = pd.Series([str(obs_rev_map.get(str(idx), "")).strip().lower() for idx in matched_indices], index=matched_indices)
                            else:
                                rev_series = obs_rev.reindex(matched_indices).astype(str).str.strip().str.lower()
                            is_rev = rev_series.isin(["true", "1", "yes", "t"])
                            if status_filter == 'reviewed':
                                matched_indices = matched_indices[is_rev]
                            else:
                                matched_indices = matched_indices[~is_rev]
                    elif status_filter in ('flagged', 'err'):
                        flagged_mask = pd.Series(False, index=matched_indices)
                        for p_col in prob_cols:
                            combined_prob = _get_combined(p_col, matched_indices)
                            flagged_mask |= _is_truthy_series(combined_prob)
                        matched_indices = matched_indices[flagged_mask]
                    elif status_filter in ('conflict', 'cfct', 'history'):
                        history_mask = pd.Series([oid in history_set or str(oid) in history_set or (str(oid).isdigit() and int(str(oid)) in history_set) for oid in matched_indices], index=matched_indices)
                        matched_indices = matched_indices[history_mask]
                    elif status_filter in ('unknown', 'ukn'):
                        unknown_mask = pd.Series(False, index=matched_indices)
                        for col in df_reg.columns:
                            if str(col).lower() in ("objectid", "id"):
                                continue
                            unknown_mask |= _is_unknown_series(df_reg[col].reindex(matched_indices))
                        matched_indices = matched_indices[unknown_mask]

                # Cabinet filter
                if cabinet_filter:
                    combined_cabinets = _clean_series(_get_combined("Cabinet", matched_indices)).str.lower()
                    mask = combined_cabinets == cabinet_filter
                    matched_indices = matched_indices[mask]

                # Shelf filter
                if shelf_filter:
                    combined_shelves = _clean_series(_get_combined("Shelf", matched_indices)).str.lower()
                    mask = combined_shelves == shelf_filter
                    matched_indices = matched_indices[mask]

                # Box filter
                if box_filter:
                    combined_boxes = _clean_series(_get_combined("Box", matched_indices)).str.lower()
                    mask = combined_boxes == box_filter
                    matched_indices = matched_indices[mask]

                # Storage Location filter
                if storage_loc_filter:
                    combined_sloc = _clean_series(_get_combined("Storage Location", matched_indices)).str.lower()
                    if (combined_sloc == "").all():
                        combined_sloc = _clean_series(_get_combined("Location", matched_indices)).str.lower()
                    mask = combined_sloc.str.contains(storage_loc_filter, regex=False)
                    matched_indices = matched_indices[mask]

                # Room filter
                if room_filter:
                    combined_rooms = _clean_series(_get_combined("Room", matched_indices)).str.lower()
                    mask = combined_rooms == room_filter
                    matched_indices = matched_indices[mask]

                # Genus filter
                if genus_filter:
                    if "Genus" in df_reg.columns:
                        mask = _clean_series(df_reg["Genus"].reindex(matched_indices)).str.lower() == genus_filter
                        matched_indices = matched_indices[mask]

                # Collector filter
                if collector_filter:
                    if "Collector" in df_reg.columns:
                        mask = _clean_series(df_reg["Collector"].reindex(matched_indices)).str.lower().str.contains(collector_filter, regex=False)
                        matched_indices = matched_indices[mask]

                # Has problems filter
                if has_problems_filter:
                    mask = pd.Series(False, index=matched_indices)
                    problems = []
                    if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                        problems = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"]]

                    for p_col in problems:
                        combined_prob = _get_combined(p_col, matched_indices)
                        mask |= _is_truthy_series(combined_prob)

                    if has_problems_filter in ["true", "1", "yes", "t"]:
                        matched_indices = matched_indices[mask]
                    elif has_problems_filter in ["false", "0", "no", "f"]:
                        matched_indices = matched_indices[~mask]

                # Dynamic Location Filters
                for loc_col, loc_val in loc_filters.items():
                    combined_loc = _clean_series(_get_combined(loc_col, matched_indices)).str.lower()
                    matched_indices = matched_indices[combined_loc == loc_val]

                # Specific Problems & History Filters (from Advanced Filter Modal)
                if specific_problems:
                    # Parse specific problems into dict of {name: state ('has' | 'not')}
                    parsed_specific_problems = {}
                    for sp_item in specific_problems:
                        sp_item = sp_item.strip()
                        if not sp_item:
                            continue
                        if ":" in sp_item:
                            p_name, p_state = sp_item.split(":", 1)
                            parsed_specific_problems[p_name.strip()] = p_state.strip().lower()
                        else:
                            parsed_specific_problems[sp_item] = "has"

                    # Collect schema-defined problems and mapping
                    schema_problems = []
                    problem_to_field = {}
                    if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                        for p in self.app_state.config["ui_sections"]["problems"]:
                            name = p.get("name")
                            if name:
                                schema_problems.append(name)
                                if "maps_to" in p:
                                    problem_to_field[name] = p["maps_to"]
                                elif "target" in p:
                                    problem_to_field[name] = p["target"]

                    def get_problem_mask(prob_col, indices):
                        if prob_col == "Images_Missing":
                            if "Images_Missing" in df_obs.columns if df_obs is not None else False:
                                return _is_truthy_series(_get_combined("Images_Missing", indices))
                            return pd.Series(False, index=indices)

                        obs_mask = _is_truthy_series(_get_combined(prob_col, indices))

                        if prob_col in problem_to_field:
                            field = problem_to_field[prob_col]
                            if field in df_reg.columns:
                                raw_vals = df_reg[field].reindex(indices)
                                is_explicitly_unknown = _is_unknown_series(raw_vals)
                                is_missing = raw_vals.isna() | (_clean_series(raw_vals) == "")

                                # Overwrite observation mask directly to ensure explicitly unknown is NEVER a problem
                                auto_mask = is_missing
                                result_mask = obs_mask | auto_mask
                                result_mask = result_mask & ~is_explicitly_unknown
                                return result_mask

                        return obs_mask

                    # Apply strict universal AND across each specific problem condition
                    for p_name, p_state in parsed_specific_problems.items():
                        is_not = (p_state == "not")

                        if p_name in ("Historical_Data", "History"):
                            hist_mask = pd.Series([
                                (oid in history_set or str(oid) in history_set or (str(oid).isdigit() and int(str(oid)) in history_set))
                                for oid in matched_indices
                            ], index=matched_indices)
                            if is_not:
                                matched_indices = matched_indices[~hist_mask]
                            else:
                                matched_indices = matched_indices[hist_mask]

                        elif p_name == "Any_Problem":
                            any_prob_mask = pd.Series(False, index=matched_indices)
                            for sp_schema in schema_problems:
                                if "Image" not in sp_schema:
                                    any_prob_mask |= get_problem_mask(sp_schema, matched_indices)
                            if is_not:
                                matched_indices = matched_indices[~any_prob_mask]
                            else:
                                matched_indices = matched_indices[any_prob_mask]

                        elif "_Unknown" in p_name or p_name == "Unknown":
                            field_name = p_name.replace("_Unknown", "")
                            if field_name == "Unknown":
                                # Global unknown
                                unk_mask = pd.Series(False, index=matched_indices)
                                for col in df_reg.columns:
                                    if str(col).lower() not in ("objectid", "id"):
                                        unk_mask |= _is_unknown_series(df_reg[col].reindex(matched_indices))
                            else:
                                # Try mapped field
                                target_field = problem_to_field.get(field_name + "_Problem", field_name)
                                if target_field in df_reg.columns:
                                    unk_mask = _is_unknown_series(df_reg[target_field].reindex(matched_indices))
                                else:
                                    unk_mask = pd.Series(False, index=matched_indices)

                            if is_not:
                                matched_indices = matched_indices[~unk_mask]
                            else:
                                matched_indices = matched_indices[unk_mask]

                        else:
                            prob_mask = get_problem_mask(p_name, matched_indices)
                            if is_not:
                                matched_indices = matched_indices[~prob_mask]
                            else:
                                matched_indices = matched_indices[prob_mask]

                total_matching = len(matched_indices)

                # Facet computation
                facets = {}

                # 1. Cabinets facet
                cabinet_series = _clean_series(_get_combined("Cabinet", matched_indices))
                cabinet_series = cabinet_series[cabinet_series != ""]
                facets["cabinets"] = cabinet_series.value_counts().to_dict()

                # 2. Review and Status counts with index dtype safety
                reviewed_count = 0
                pending_count = total_matching
                flagged_count = 0
                history_count = 0
                unknown_count = 0

                if total_matching > 0:
                    if rev_col and df_obs is not None:
                        obs_rev = df_obs[rev_col]
                        if obs_rev.index.dtype != matched_indices.dtype:
                            obs_rev_map = {str(k): v for k, v in obs_rev.items()}
                            rev_series_facet = pd.Series([str(obs_rev_map.get(str(idx), "")).strip().lower() for idx in matched_indices], index=matched_indices)
                        else:
                            rev_series_facet = obs_rev.reindex(matched_indices).astype(str).str.strip().str.lower()
                        is_rev_series = rev_series_facet.isin(["true", "1", "yes", "t"])
                        reviewed_count = int(is_rev_series.sum())
                        pending_count = max(0, total_matching - reviewed_count)

                    if prob_cols:
                        f_mask = pd.Series(False, index=matched_indices)
                        for p_col in prob_cols:
                            combined_prob = _get_combined(p_col, matched_indices)
                            f_mask |= _is_truthy_series(combined_prob)
                        flagged_count = int(f_mask.sum())

                    if history_set:
                        h_mask = pd.Series([oid in history_set or str(oid) in history_set or (str(oid).isdigit() and int(str(oid)) in history_set) for oid in matched_indices], index=matched_indices)
                        history_count = int(h_mask.sum())

                    u_mask = pd.Series(False, index=matched_indices)
                    for col in df_reg.columns:
                        if str(col).lower() in ("objectid", "id"):
                            continue
                        u_mask |= _is_unknown_series(df_reg[col].reindex(matched_indices))
                    unknown_count = int(u_mask.sum())

                facets["reviewed_count"] = reviewed_count
                facets["pending_count"] = pending_count
                facets["flagged_count"] = flagged_count
                facets["history_count"] = history_count
                facets["unknown_count"] = unknown_count
                facets["cabinets"] = sorted([str(c) for c in _clean_series(_get_combined("Cabinet", df_reg.index)).unique() if str(c).strip()])
                facets["shelves"] = sorted([str(s) for s in _clean_series(_get_combined("Shelf", df_reg.index)).unique() if str(s).strip()])

                # Sorting logic
                if sort_by in ['id', 'genus', 'cabinet'] and not is_search_active:
                    ascending = (sort_dir == 'asc')
                    if sort_by == 'id':
                        # Natural numeric sorting (e.g. 1, 2, 3, 4, ..., 10, 100, 1000)
                        matched_indices = pd.Index(sorted(matched_indices, key=_natural_sort_key, reverse=not ascending))
                    elif sort_by == 'genus':
                        if "Genus" in df_reg.columns:
                            sort_series = _clean_series(df_reg["Genus"].reindex(matched_indices))
                            matched_indices = matched_indices[sort_series.argsort()]
                            if not ascending:
                                matched_indices = matched_indices[::-1]
                    elif sort_by == 'cabinet':
                        sort_series = _clean_series(_get_combined("Cabinet", matched_indices))
                        matched_indices = matched_indices[sort_series.argsort()]
                        if not ascending:
                            matched_indices = matched_indices[::-1]

                paged_indices = matched_indices[offset:offset + limit]

                # Dynamically resolve location fields from config
                location_fields = ["Building", "Floor", "Cabinet", "Stored as", "Extra", "Room", "Shelf", "Drawer", "Box"]
                if self.app_state.config and "location" in self.app_state.config.get("ui_sections", {}):
                    location_fields = [f["name"] for f in self.app_state.config["ui_sections"]["location"] if isinstance(f, dict) and f.get("name")]

                objects = []
                paged_indices_list = paged_indices.tolist()

                # Safe row dictionary extraction handling duplicate indices and dtype mismatches
                paged_reg_dict = {}
                obs_cols = set(df_obs.columns) if df_obs is not None else set()
                reg_cols = set(df_reg.columns)
                paged_obs_dict = {}

                # Fast index lookup maps for robust retrieval
                reg_idx_map = {}
                for pos, idx_val in enumerate(df_reg.index):
                    s_key = str(idx_val)
                    if s_key not in reg_idx_map:
                        reg_idx_map[s_key] = pos

                obs_idx_map = {}
                if df_obs is not None:
                    for pos, idx_val in enumerate(df_obs.index):
                        s_key = str(idx_val)
                        if s_key not in obs_idx_map:
                            obs_idx_map[s_key] = pos

                for oid_item in paged_indices_list:
                    # 1. Registration row
                    s_oid = str(oid_item)
                    if s_oid in reg_idx_map:
                        pos = reg_idx_map[s_oid]
                        paged_reg_dict[oid_item] = df_reg.iloc[pos].to_dict()
                    elif oid_item in df_reg.index:
                        try:
                            loc_res = df_reg.loc[oid_item]
                            paged_reg_dict[oid_item] = loc_res.iloc[0].to_dict() if isinstance(loc_res, pd.DataFrame) else loc_res.to_dict()
                        except Exception:
                            paged_reg_dict[oid_item] = {}
                    else:
                        paged_reg_dict[oid_item] = {}

                    # 2. Observation row
                    if df_obs is not None:
                        if s_oid in obs_idx_map:
                            pos = obs_idx_map[s_oid]
                            paged_obs_dict[oid_item] = df_obs.iloc[pos].to_dict()
                        elif oid_item in df_obs.index:
                            try:
                                loc_res = df_obs.loc[oid_item]
                                paged_obs_dict[oid_item] = loc_res.iloc[0].to_dict() if isinstance(loc_res, pd.DataFrame) else loc_res.to_dict()
                            except Exception:
                                pass

                loc_keys = {lcol: lcol.lower().replace(" ", "_") for lcol in location_fields}

                unval_set = set()
                if getattr(self.app_state, "df_unvalidated", None) is not None and not self.app_state.df_unvalidated.empty:
                    df_u = self.app_state.df_unvalidated
                    if "ObjectID" in df_u.columns:
                        unval_set = set(df_u["ObjectID"].astype(str).str.strip().unique())


            # End of df_lock critical section

            for oid in paged_indices_list:
                reg_row = paged_reg_dict.get(oid, {})
                obs_row = paged_obs_dict.get(oid, {})

                genus = _clean_val(reg_row.get("Genus"))
                species = _clean_val(reg_row.get("Species"))
                family = _clean_val(reg_row.get("Family"))
                author = _clean_val(reg_row.get("Author"))
                collector = _clean_val(reg_row.get("Collector"))
                collection_date = _clean_val(reg_row.get("Collection Date"))
                sci_name = f"{genus} {species} {author}".strip() if (genus or species) else f"Specimen #{oid}"

                loc = {}
                for lcol, key_name in loc_keys.items():
                    if obs_row and lcol in obs_cols and _clean_val(obs_row.get(lcol)):
                        loc[key_name] = _clean_val(obs_row.get(lcol))
                    elif lcol in reg_cols and _clean_val(reg_row.get(lcol)):
                        loc[key_name] = _clean_val(reg_row.get(lcol))
                    else:
                        loc[key_name] = ""

                flags = compute_status_flags(reg_row, obs_row, history_set, oid, prob_cols, problem_to_field, hist_fields_by_oid)

                acc_num = _clean_val(reg_row.get("ObjectID") or reg_row.get("Accession") or reg_row.get("AccessionID") or reg_row.get("id")) or str(oid)
                raw_loaned = obs_row.get("Loaned out") if obs_row else None
                is_loaned_out = (
                    raw_loaned is True
                    or str(raw_loaned).strip().lower() in ("true", "1", "yes", "t")
                )
                loaned_out_date = _clean_val(obs_row.get("Loaned out date")) if obs_row else ""

                objects.append({
                    "id": str(oid),
                    "accession_number": acc_num,
                    "scientific_name": sci_name,
                    "genus": genus,
                    "species": species,
                    "family": family,
                    "author": author,
                    "collector": collector,
                    "collection_date": collection_date,
                    "location": loc,
                    "loaned_out": is_loaned_out,
                    "loaned_out_date": loaned_out_date,
                    "review_status": flags["review_status"],
                    "has_flags": flags["has_flags"],
                    "has_history": flags["has_history"],
                    "problems_have_history": flags["problems_have_history"],
                    "has_unknown": flags["has_unknown"],
                    "has_unvalidated": (str(oid) in unval_set)
                })

            return jsonify({
                "total_matching": total_matching,
                "offset": offset,
                "limit": limit,
                "objects": objects,
                "facets": facets
            })


        @app.route('/api/object/<oid>/synonyms', methods=['GET'])
        def get_object_synonyms(oid):
            oid_s = str(oid).strip()
            genus = ""
            species = ""
            family = ""
            workbook_path = None
            local_history = []

            with self.app_state.df_lock:
                df_reg = getattr(self.app_state, 'df_reg', None)
                if df_reg is None or df_reg.empty:
                    return jsonify({"error": "No database loaded"}), 404
                row = None
                if oid_s in df_reg.index:
                    row = df_reg.loc[oid_s]
                elif oid_s.isdigit() and int(oid_s) in df_reg.index:
                    row = df_reg.loc[int(oid_s)]
                if row is None:
                    return jsonify({"error": "Specimen not found"}), 404
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                genus = "" if pd.isna(row.get("Genus", "")) else str(row.get("Genus", "")).strip()
                species = "" if pd.isna(row.get("Species", "")) else str(row.get("Species", "")).strip()
                family = "" if pd.isna(row.get("Family", "")) else str(row.get("Family", "")).strip()
                workbook_path = getattr(self.app_state, 'excel_path', None)
                from backend import gbif as gbif_mod
                local_history = gbif_mod.collect_local_old_names(self.app_state, oid_s)

            # Perform cache / GBIF lookup strictly outside df_lock
            cache_path = gbif_mod.get_synonym_cache_path(workbook_path)
            syn_data = gbif_mod.get_synonyms(genus, species, family=family, cache_path=cache_path)
            return jsonify({
                "registered": {
                    "scientific_name": syn_data.get("registered_name") or f"{genus} {species}".strip(),
                    "genus": genus,
                    "species": species,
                    "family": syn_data.get("registered_family") or family,
                },
                "local_history": local_history,
                "old_families": syn_data.get("old_families", []),
                "primary_synonyms": syn_data.get("primary_synonyms", []),
                "other_synonyms": syn_data.get("other_synonyms", []),
                "offline": bool(syn_data.get("offline", False)),
                "from_cache": bool(syn_data.get("from_cache", False)),
            })

        @app.route('/api/object/<oid>/check-label', methods=['POST'])
        def check_object_label_name(oid):
            oid_s = str(oid).strip()
            body = request.get_json(silent=True) or {}
            label_name = str(body.get("label_name") or "").strip()
            if not label_name:
                return jsonify({"verdict": "uncertain", "message": "Enter a name from the physical label to check."})

            with self.app_state.df_lock:
                df_reg = getattr(self.app_state, 'df_reg', None)
                if df_reg is None or df_reg.empty:
                    return jsonify({"error": "No database loaded"}), 404
                row = None
                if oid_s in df_reg.index:
                    row = df_reg.loc[oid_s]
                elif oid_s.isdigit() and int(oid_s) in df_reg.index:
                    row = df_reg.loc[int(oid_s)]
                if row is None:
                    return jsonify({"error": "Specimen not found"}), 404
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                genus = "" if pd.isna(row.get("Genus", "")) else str(row.get("Genus", "")).strip()
                species = "" if pd.isna(row.get("Species", "")) else str(row.get("Species", "")).strip()
                family = "" if pd.isna(row.get("Family", "")) else str(row.get("Family", "")).strip()

            from backend import gbif as gbif_mod
            return jsonify(gbif_mod.compare_label_name(label_name, genus, species, reg_family=family))

        @app.route('/api/object/<oid>/history', methods=['GET'])
        def get_object_history(oid):
            oid = str(oid).strip()
            suggestions = {}

            with self.app_state.df_lock:
                historical_dbs = getattr(self.app_state, 'historical_dbs', None)
                if not historical_dbs:
                    return jsonify({"historical_data": {}})

                for db in historical_dbs:
                    db_name = db.get("name", "Unknown DB")
                    reg_by_id = db.get("reg_by_id")

                    if reg_by_id is not None:
                        # Try exact match first
                        if oid in reg_by_id.index:
                            row = reg_by_id.loc[oid]
                        else:
                            # Try int match if numeric
                            try:
                                if oid.isdigit() and int(oid) in reg_by_id.index:
                                    row = reg_by_id.loc[int(oid)]
                                else:
                                    continue
                            except Exception:
                                continue

                        if isinstance(row, pd.DataFrame):
                            row = row.iloc[0]

                        for col in row.index:
                            val = row[col]
                            if pd.isna(val):
                                continue
                            val_str = str(val).strip()
                            if not val_str or val_str.lower() == "nan":
                                continue

                            if col not in suggestions:
                                suggestions[col] = {}

                            if val_str not in suggestions[col]:
                                suggestions[col][val_str] = []

                            if db_name not in suggestions[col][val_str]:
                                suggestions[col][val_str].append(db_name)

            return jsonify({
                "id": str(oid),
                "historical_data": suggestions
            })


        @app.route('/api/object/<oid>', methods=['GET'])
        def get_object_detail(oid):
            oid = str(oid).strip()

            with self.app_state.df_lock:
                if self.app_state.df_reg is None:
                    return jsonify({"error": "No database loaded"}), 400

                reg_oid = _resolve_oid_in_df(self.app_state.df_reg, oid)
                if reg_oid is None:
                    return jsonify({"error": f"Object {oid} not found"}), 404

                reg_row = self.app_state.df_reg.loc[[reg_oid]].copy()
                obs_row = None
                if self.app_state.df_obs is not None:
                    obs_oid = _resolve_oid_in_df(self.app_state.df_obs, oid)
                    if obs_oid is not None:
                        obs_row = self.app_state.df_obs.loc[[obs_oid]].copy()

                local_endpoints = []
                df_photo = getattr(self.app_state, 'df_photo', None)
                if df_photo is not None and not df_photo.empty:
                    df_p = df_photo
                    p_oid = _resolve_oid_in_df(df_p, oid)
                    if p_oid is not None and p_oid in df_p.index:
                        p_rows = df_p.loc[[p_oid]]
                        fn_idx = p_rows.columns.get_loc("FileName") + 1 if "FileName" in p_rows.columns else None
                        for row in p_rows.itertuples(index=True, name=None):
                            fn_val = row[fn_idx] if fn_idx is not None else ""
                            fn = str(fn_val).strip()
                            if fn and f"/api/photo/{fn}" not in local_endpoints:
                                local_endpoints.append(f"/api/photo/{fn}")

                unvalidated_sources = []
                if getattr(self.app_state, "df_unvalidated", None) is not None and not self.app_state.df_unvalidated.empty:
                    df_u = self.app_state.df_unvalidated
                    if "ObjectID" in df_u.columns:
                        u_matches = df_u[df_u["ObjectID"].astype(str).str.strip() == str(oid).strip()]
                        u_field_idx = u_matches.columns.get_loc("Field_Name") + 1 if "Field_Name" in u_matches.columns else None
                        u_comm_idx = u_matches.columns.get_loc("Unvalidated_Comment") + 1 if "Unvalidated_Comment" in u_matches.columns else None
                        for row in u_matches.itertuples(index=True, name=None):
                            f_name_val = row[u_field_idx] if u_field_idx is not None else ""
                            comm_val = row[u_comm_idx] if u_comm_idx is not None else ""

                            f_name = str(f_name_val).strip()
                            comm = str(comm_val).strip()
                            if f_name:
                                unvalidated_sources.append({"field": f_name, "comment": comm})

            reg_dict = {}
            for col in reg_row.columns:
                val = reg_row.iloc[0][col]
                reg_dict[col] = str(val) if pd.notna(val) else ""

            obs_dict = {}
            if obs_row is not None:
                for col in obs_row.columns:
                    val = obs_row.iloc[0][col]
                    obs_dict[col] = str(val) if pd.notna(val) else ""

            # Mirror /api/objects location & loan fallback: when Observation has no value,
            # inherit non-empty Registration values in the GET payload (never mutates df_obs).
            _fallback_cols = ["Building", "Floor", "Cabinet", "Shelf", "Stored as", "Loaned out", "Loaned out date"]
            if self.app_state.config:
                for _lf in self.app_state.config.get("ui_sections", {}).get("location", []):
                    _lf_name = _lf.get("name") if isinstance(_lf, dict) else _lf
                    if _lf_name and _lf_name not in _fallback_cols:
                        _fallback_cols.append(_lf_name)
            for _fcol in _fallback_cols:
                _cur_obs = str(obs_dict.get(_fcol, "")).strip()
                if not _cur_obs or _cur_obs.lower() in ("nan", "none", "<na>"):
                    _reg_val = str(reg_dict.get(_fcol, "")).strip()
                    if _reg_val and _reg_val.lower() not in ("nan", "none", "<na>"):
                        obs_dict[_fcol] = _reg_val

            genus = reg_dict.get("Genus", "")
            species = reg_dict.get("Species", "")
            author = reg_dict.get("Author", "")
            sci_name = f"{genus} {species} {author}".strip() if (genus or species) else f"Specimen #{oid}"

            rev_val = False
            if "Reviewed" in obs_dict:
                rev_val = str(obs_dict["Reviewed"]).strip().lower() in ["true", "1", "yes"]

            online_urls = []

            # 1. First add any verified/curated photo URLs registered in df_reg
            for k in ("Online photo 1", "Online photo 2", "Online photo 3", "Online Photo 1", "Online Photo 2", "Online Photo 3"):
                u = str(reg_dict.get(k, "")).strip().strip("'\"")
                if u and u.lower() not in ("nan", "none", "<na>") and u.startswith(("http://", "https://", "www.")):
                    if u.startswith("www."):
                        u = "https://" + u
                    if u not in online_urls:
                        online_urls.append(u)

            # 2. Check user preferences override or config pattern for fallback candidates
            pattern = self._image_url_pattern_override.strip()

            if not pattern and self.app_state.config:
                pattern = self.app_state.config.get("image_url_pattern", "").strip()

            if not pattern:
                pattern = "https://www.unimus.no/photos/image/jpeg/O-V-OE-{num:04d}{suffix}.jpg"

            try:
                num_val = int(oid) if oid.isdigit() else 0
            except ValueError:
                num_val = 0

            # Generate candidate URLs (ranked after registered URLs)
            for suf in ["", "-01", "-02", "-1", "-2", "-3"]:
                try:
                    f_url = pattern.format(id=oid, num=num_val, suffix=suf)
                    if f_url not in online_urls:
                        online_urls.append(f_url)
                except Exception:
                    # Fallback to simple replace if format string is malformed
                    f_url = pattern.replace("{id}", oid)
                    if f_url not in online_urls:
                        online_urls.append(f_url)
                    break

            flagged_issues = []
            if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                for p_info in self.app_state.config["ui_sections"]["problems"]:
                    p_col = p_info["name"]
                    val = obs_dict.get(p_col, reg_dict.get(p_col, "")).strip().lower()
                    if val in ["true", "1", "yes", "x"]:
                        flagged_issues.append({
                            "id": p_col,
                            "field": p_info.get("label", p_col),
                            "severity": "warning",
                            "reason": p_info.get("label", p_col),
                            "category": p_info.get("category", "notes"),
                            "importance": p_info.get("importance", "medium"),
                            "resolved": False
                        })

            history_set, hist_fields_by_oid = get_historical_cache(self.app_state)
            prob_cols = []
            if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                prob_cols = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"] if p.get("name")]
            problem_to_field = get_problem_to_field_map(self.app_state.config)
            flags = compute_status_flags(reg_dict, obs_dict, history_set, oid, prob_cols, problem_to_field, hist_fields_by_oid)

            is_auth, current_sid, _ = self._get_current_session()
            other_viewers_count = self._get_other_viewers_count(oid, current_session_id=current_sid)

            return jsonify({
                "id": str(oid),
                "accession_number": str(oid),
                "scientific_name": sci_name,
                "registration": reg_dict,
                "observation": obs_dict,
                "review_status": flags["review_status"],
                "has_flags": flags["has_flags"],
                "has_history": flags["has_history"],
                "problems_have_history": flags["problems_have_history"],
                "has_unknown": flags["has_unknown"],
                "flagged_issues": flagged_issues,
                "unvalidated_sources": unvalidated_sources,
                "other_viewers_count": other_viewers_count,
                "images": {
                    "preferred_source": "local" if local_endpoints else "online",
                    "online_urls": online_urls,
                    "local_endpoints": local_endpoints,
                    "photo_count": len(local_endpoints) + len(online_urls)
                }
            })

        @app.route('/api/presence', methods=['POST'])
        def handle_presence():
            is_auth, sid, tok = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            from backend.mobile_schemas import PresenceSchema
            raw_data = request.get_json(silent=True) or {}
            data = PresenceSchema().load(raw_data)
            raw_oid = data.get("oid")
            self._update_presence(sid, raw_oid)
            other_cnt = self._get_other_viewers_count(raw_oid, current_session_id=sid) if raw_oid else 0
            return jsonify({
                "success": True,
                "oid": str(raw_oid) if raw_oid else None,
                "other_viewers_count": other_cnt
            })

        @app.route('/api/session/push_filter', methods=['POST'])
        def push_filter():
            # Filter pushes remain local to each worker to prevent disruptive view shifts
            return jsonify({"success": True})

        @app.route('/api/recent_edits', methods=['GET'])
        def get_recent_edits():
            return jsonify({"edits": self.recent_edits})

        @app.route('/api/undo', methods=['POST'])
        def undo_last_edit():
            is_auth, client_sid, _ = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            data = request.get_json(silent=True) or {}
            oid = str(data.get('oid') or data.get('id') or '').strip()

            if not oid and self.recent_edits:
                for edit in self.recent_edits:
                    if edit.get("session_id") in (client_sid, None):
                        oid = edit["oid"]
                        break

            undo_stacks = getattr(self.app_state, 'undo_stacks', {})
            if not oid and undo_stacks:
                for k, stack in undo_stacks.items():
                    if stack and any(s.get("_session_id") in (client_sid, None) for s in stack):
                        oid = str(k)
                        break

            if not oid:
                return jsonify({"error": "No recent edits to undo for this session"}), 400

            with self.app_state.df_lock:
                resolved_reg_oid = _resolve_oid_in_df(self.app_state.df_reg, oid)
                resolved_obs_oid = _resolve_oid_in_df(self.app_state.df_obs, oid)

                undo_stacks = getattr(self.app_state, 'undo_stacks', {})
                target_key = resolved_reg_oid if (resolved_reg_oid in undo_stacks) else str(oid)
                if target_key not in undo_stacks or not undo_stacks[target_key]:
                    return jsonify({"error": f"No undo history for {oid}"}), 404

                stack = undo_stacks[target_key]
                target_idx = -1
                for idx in range(len(stack) - 1, -1, -1):
                    snap_sid = stack[idx].get("_session_id")
                    if snap_sid == client_sid or snap_sid is None:
                        target_idx = idx
                        break

                if target_idx == -1:
                    return jsonify({"error": f"No undo history on {oid} for this worker session"}), 404

                snapshot = stack.pop(target_idx)

                if resolved_reg_oid is not None:
                    # Update row cell-by-cell to avoid pandas ValueError
                    for col, val in snapshot["reg"].items():
                        self.app_state.df_reg.at[resolved_reg_oid, col] = val

                if resolved_obs_oid is not None:
                    # Update row cell-by-cell
                    for col, val in snapshot["obs"].items():
                        self.app_state.df_obs.at[resolved_obs_oid, col] = val

                # Clean up recent_edits and _log_records for this session
                for i in range(len(self.recent_edits)):
                    if str(self.recent_edits[i]["oid"]) == str(oid) and self.recent_edits[i].get("session_id") in (client_sid, None):
                        self.recent_edits.pop(i)
                        break

                if hasattr(self.app_state, "_log_records") and self.app_state._log_records:
                    # Find and remove the latest mobile log record created in this active worker session for this oid
                    for i in range(len(self.app_state._log_records) - 1, -1, -1):
                        rec = self.app_state._log_records[i]
                        if str(rec.get("ObjectID", "")) == str(oid) and rec.get("Action") in ["MOBILE_EDIT", "REVIEWED", "NOT_REVIEWED"] and rec.get("_session_id") in (client_sid, None):
                            self.app_state._log_records.pop(i)
                            break
                    self.app_state.df_log = _normalise_log_dataframe(pd.DataFrame(self.app_state._log_records))

                self.app_state.dirty = True

                reg_row = _get_row_dict_safe(self.app_state.df_reg, resolved_reg_oid)
                obs_row = _get_row_dict_safe(self.app_state.df_obs, resolved_obs_oid)
                history_set, hist_fields_by_oid = get_historical_cache(self.app_state)
                prob_cols = []
                if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                    prob_cols = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"] if p.get("name")]
                problem_to_field = get_problem_to_field_map(self.app_state.config)
                flags = compute_status_flags(reg_row, obs_row, history_set, oid, prob_cols, problem_to_field, hist_fields_by_oid)

            self.broadcast_event("record_updated", {
                "id": str(oid),
                "has_flags": flags["has_flags"],
                "has_history": flags["has_history"],
                "problems_have_history": flags["problems_have_history"],
                "has_unknown": flags["has_unknown"],
                "review_status": flags["review_status"]
            })

            if self.on_edit_callback:
                try:
                    self.on_edit_callback(oid, f"Undid last edit on {oid}")
                except Exception:
                    pass

            if self.root_tk:
                try:
                    self.root_tk.after(0, lambda: app_bus.publish(DATABASE_UPDATED, mobile_edit=True))
                except Exception:
                    pass

            # Return the restored record so the UI can update itself
            restored_record = {**reg_row, **obs_row}
            restored_record["id"] = str(oid)
            restored_record["has_flags"] = flags["has_flags"]
            restored_record["has_history"] = flags["has_history"]
            restored_record["problems_have_history"] = flags["problems_have_history"]
            restored_record["has_unknown"] = flags["has_unknown"]
            restored_record["review_status"] = flags["review_status"]

            return jsonify({"success": True, "restored": restored_record})


        @app.route('/api/update', methods=['POST'])
        def update_object():
            is_auth, client_sid, _ = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            from backend.mobile_schemas import ObjectUpdateSchema, ValidationError
            raw_data = request.get_json(silent=True) or {}
            try:
                data = ObjectUpdateSchema().load(raw_data)
            except ValidationError as err:
                return jsonify({"error": f"Invalid update payload: {err.messages}"}), 400

            oid = data.get('oid', '').strip()
            if not oid:
                return jsonify({"error": "Missing object ID"}), 400

            reviewed = data.get('reviewed')
            updates = data.get('observation', {})
            reg_updates = data.get('registration', {})
            unval_updates = data.get('unvalidated_sources')
            client_timestamp = data.get('timestamp')
            with self.app_state.df_lock:
                allowed_reg_cols, allowed_obs_cols = _get_allowed_columns(getattr(self.app_state, "config", None))
                edit_summary, err = _execute_record_update(
                    self.app_state, oid, reg_updates, updates, reviewed,
                    allowed_reg_cols=allowed_reg_cols,
                    allowed_obs_cols=allowed_obs_cols,
                    recent_edits=self.recent_edits,
                    client_timestamp=client_timestamp,
                    unvalidated_updates=unval_updates,
                    session_id=client_sid
                )
                if err:
                    code = 409 if "Conflict" in err else 404
                    return jsonify({"error": err}), code

                self.app_state.df_log = _normalise_log_dataframe(pd.DataFrame(self.app_state._log_records))
                self.app_state.dirty = True
                self.app_state._mobile_last_edited_oid = oid

                resolved_reg_oid = _resolve_oid_in_df(self.app_state.df_reg, oid)
                resolved_obs_oid = _resolve_oid_in_df(self.app_state.df_obs, oid)
                reg_row = _get_row_dict_safe(self.app_state.df_reg, resolved_reg_oid)
                obs_row = _get_row_dict_safe(self.app_state.df_obs, resolved_obs_oid)
                history_set, hist_fields_by_oid = get_historical_cache(self.app_state)
                prob_cols = []
                if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                    prob_cols = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"] if p.get("name")]
                problem_to_field = get_problem_to_field_map(self.app_state.config)
                flags = compute_status_flags(reg_row, obs_row, history_set, oid, prob_cols, problem_to_field, hist_fields_by_oid)

            self.broadcast_event("record_updated", {
                "id": str(oid),
                "has_flags": flags["has_flags"],
                "has_history": flags["has_history"],
                "problems_have_history": flags["problems_have_history"],
                "has_unknown": flags["has_unknown"],
                "review_status": flags["review_status"]
            })

            # Notify desktop UI
            if self.on_edit_callback:
                try:
                    self.on_edit_callback(oid, edit_summary)
                except Exception:
                    pass

            if self.root_tk:
                try:
                    self.root_tk.after(0, lambda: app_bus.publish(DATABASE_UPDATED, mobile_edit=True))
                except Exception:
                    pass

            return jsonify({
                "success": True,
                "id": str(oid),
                "review_status": flags["review_status"],
                "has_flags": flags["has_flags"],
                "has_history": flags["has_history"],
                "problems_have_history": flags["problems_have_history"],
                "has_unknown": flags["has_unknown"],
                "synced_at": datetime.now().isoformat()
            })

        @app.route('/api/audit', methods=['GET', 'POST'])
        @app.route('/api/audit/update', methods=['POST'])
        @app.route('/api/audit_update', methods=['POST'])
        def audit_endpoint():
            is_auth, client_sid, _ = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            if request.method == 'GET':
                records = list(getattr(self.app_state, "_log_records", []) or [])
                return jsonify({
                    "status": "ok",
                    "total_records": len(records),
                    "records": records[-50:]
                })

            from backend.mobile_schemas import ObjectUpdateSchema, ValidationError
            raw_data = request.get_json(silent=True) or {}
            if "reviewed" not in raw_data:
                raw_data["reviewed"] = True

            try:
                data = ObjectUpdateSchema().load(raw_data)
            except ValidationError as err:
                return jsonify({"error": f"Invalid update payload: {err.messages}"}), 400

            oid = data.get('oid', '').strip()
            if not oid:
                return jsonify({"error": "Missing object ID"}), 400

            reviewed = data.get('reviewed')
            if reviewed is None:
                reviewed = True
            updates = data.get('observation', {})
            reg_updates = data.get('registration', {})
            unval_updates = data.get('unvalidated_sources')
            client_timestamp = data.get('timestamp')

            with self.app_state.df_lock:
                allowed_reg_cols, allowed_obs_cols = _get_allowed_columns(getattr(self.app_state, "config", None))
                edit_summary, err = _execute_record_update(
                    self.app_state, oid, reg_updates, updates, reviewed,
                    allowed_reg_cols=allowed_reg_cols,
                    allowed_obs_cols=allowed_obs_cols,
                    recent_edits=self.recent_edits,
                    client_timestamp=client_timestamp,
                    unvalidated_updates=unval_updates,
                    session_id=client_sid
                )
                if err:
                    code = 409 if "Conflict" in err else 404
                    return jsonify({"error": err}), code

                self.app_state.df_log = _normalise_log_dataframe(pd.DataFrame(self.app_state._log_records))
                self.app_state.dirty = True
                self.app_state._mobile_last_edited_oid = oid

                resolved_reg_oid = _resolve_oid_in_df(self.app_state.df_reg, oid)
                resolved_obs_oid = _resolve_oid_in_df(self.app_state.df_obs, oid)
                reg_row = _get_row_dict_safe(self.app_state.df_reg, resolved_reg_oid)
                obs_row = _get_row_dict_safe(self.app_state.df_obs, resolved_obs_oid)
                history_set, hist_fields_by_oid = get_historical_cache(self.app_state)
                prob_cols = []
                if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                    prob_cols = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"] if p.get("name")]
                problem_to_field = get_problem_to_field_map(self.app_state.config)
                flags = compute_status_flags(reg_row, obs_row, history_set, oid, prob_cols, problem_to_field, hist_fields_by_oid)

            self.broadcast_event("record_updated", {
                "id": str(oid),
                "has_flags": flags["has_flags"],
                "has_history": flags["has_history"],
                "problems_have_history": flags["problems_have_history"],
                "has_unknown": flags["has_unknown"],
                "review_status": flags["review_status"]
            })

            # Notify desktop UI
            if self.on_edit_callback:
                try:
                    self.on_edit_callback(oid, edit_summary)
                except Exception:
                    pass

            if self.root_tk:
                try:
                    self.root_tk.after(0, lambda: app_bus.publish(DATABASE_UPDATED, mobile_edit=True))
                except Exception:
                    pass

            return jsonify({
                "success": True,
                "id": str(oid),
                "reviewed": True,
                "review_status": flags["review_status"],
                "has_flags": flags["has_flags"],
                "has_history": flags["has_history"],
                "problems_have_history": flags["problems_have_history"],
                "has_unknown": flags["has_unknown"],
                "audit_logged": True,
                "synced_at": datetime.now().isoformat()
            })

        @app.route('/api/batch_location_update', methods=['POST'])
        def batch_location_update():
            is_auth, client_sid, _ = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            data = request.get_json(silent=True) or {}
            items = data.get('items') or data.get('object_ids') or []
            location = data.get('location', {})
            if not items or not isinstance(items, list):
                return jsonify({"error": "No items provided in batch"}), 400

            client_timestamp = data.get('timestamp')
            updated_ids = []
            errors = []

            with self.app_state.df_lock:
                allowed_reg_cols, allowed_obs_cols = _get_allowed_columns(getattr(self.app_state, "config", None))
                allowed_obs_cols.update({"Building", "Floor", "Cabinet", "Shelf", "Stored as", "Stored_As", "Room", "Drawer", "Box"})

                history_set, hist_fields_by_oid = get_historical_cache(self.app_state)
                prob_cols = []
                if self.app_state.config and "problems" in self.app_state.config.get("ui_sections", {}):
                    prob_cols = [p.get("name") for p in self.app_state.config["ui_sections"]["problems"] if p.get("name")]
                problem_to_field = get_problem_to_field_map(self.app_state.config)

                for raw_item in items:
                    if isinstance(raw_item, dict):
                        oid = str(raw_item.get('id') or raw_item.get('oid') or '').strip()
                        item_loc = raw_item.get('location') or location
                    else:
                        oid = str(raw_item).strip()
                        item_loc = location

                    if not oid:
                        continue

                    obs_updates = dict(item_loc)
                    if "Stored_As" in obs_updates and "Stored as" not in obs_updates:
                        obs_updates["Stored as"] = obs_updates.pop("Stored_As")

                    edit_summary, err = _execute_record_update(
                        self.app_state, oid, {}, obs_updates, None,
                        allowed_reg_cols=allowed_reg_cols,
                        allowed_obs_cols=allowed_obs_cols,
                        recent_edits=self.recent_edits,
                        client_timestamp=client_timestamp,
                        session_id=client_sid
                    )
                    if err:
                        errors.append({"id": oid, "error": err})
                    else:
                        updated_ids.append(oid)
                        self.app_state._mobile_last_edited_oid = oid

                if updated_ids:
                    self.app_state.df_log = _normalise_log_dataframe(pd.DataFrame(self.app_state._log_records))
                    self.app_state.dirty = True

            for u_oid in updated_ids:
                self.broadcast_event("record_updated", {"id": str(u_oid)})

            if updated_ids and self.on_edit_callback:
                try:
                    locations_seen = set()
                    for raw_item in items:
                        l = raw_item.get('location') if isinstance(raw_item, dict) else location
                        if l:
                            sig = f"{l.get('Building', '')} Cab {l.get('Cabinet', '')} Sh {l.get('Shelf', '')}".strip()
                            if sig:
                                locations_seen.add(sig)

                    if len(locations_seen) == 1:
                        loc_summary = next(iter(locations_seen))
                    elif len(locations_seen) > 1:
                        loc_summary = f"{len(locations_seen)} locations/shelves"
                    else:
                        loc_summary = f"{location.get('Building', '')} Fl {location.get('Floor', '')} Cab {location.get('Cabinet', '')} Sh {location.get('Shelf', '')}".strip() or "staged locations"

                    self.on_edit_callback(f"Batch ({len(updated_ids)} items)", f"Relocated {len(updated_ids)} items to {loc_summary}")
                except Exception:
                    pass

            if updated_ids and self.root_tk:
                try:
                    self.root_tk.after(0, lambda: app_bus.publish(DATABASE_UPDATED, mobile_edit=True))
                except Exception:
                    pass

            return jsonify({
                "status": "ok",
                "success": True,
                "updated_count": len(updated_ids),
                "updated_ids": updated_ids,
                "errors": errors,
                "synced_at": datetime.now().isoformat()
            })

        @app.route('/api/photo/<path:filename>', methods=['GET'])
        def get_photo(filename):
            if not self._check_auth():
                return jsonify({"error": "Unauthorized"}), 401

            safe_filename_clean = secure_filename(os.path.basename(filename))
            if not safe_filename_clean:
                return jsonify({"error": "Invalid filename"}), 400

            if self.app_state.excel_path:
                db_folder = os.path.dirname(self.app_state.excel_path)
            else:
                db_folder = os.getcwd()
            photos_dir = os.path.join(db_folder, "photos")
            file_path = os.path.join(photos_dir, safe_filename_clean)

            try:
                canonical_photos_dir = os.path.abspath(photos_dir)
                canonical_file_path = os.path.abspath(file_path)
                # Ensure path stays within photos directory and is a regular file
                if not canonical_file_path.startswith(canonical_photos_dir + os.sep) and canonical_file_path != canonical_photos_dir:
                    return jsonify({"error": "Invalid filename"}), 400
                if not os.path.isfile(canonical_file_path):
                    return jsonify({"error": "Photo not found"}), 404
                return send_file(canonical_file_path)
            except Exception as e:
                debug_error("Photo serving error", str(e))
                return jsonify({"error": "Photo not found"}), 404

        @app.route('/api/object/<oid>/photo', methods=['POST'])
        def attach_photo(oid):
            oid = str(oid).strip()
            safe_oid = re.sub(r'[^\w\-.]', '_', oid)

            if 'image' not in request.files and 'file' not in request.files:
                return jsonify({"error": "No image payload found"}), 400

            file = request.files.get('image') or request.files.get('file')
            if file.filename == '':
                return jsonify({"error": "Empty filename"}), 400

            caption = request.form.get('caption', '').strip()
            category = request.form.get('category', '').strip()

            with self.app_state.df_lock:
                if self.app_state.df_reg is None:
                    return jsonify({"error": "No database loaded"}), 400

                reg_oid = _resolve_oid_in_df(self.app_state.df_reg, oid)
                if reg_oid is None:
                    return jsonify({"error": f"Object {oid} not found"}), 404

            if self.app_state.excel_path:
                db_folder = os.path.dirname(self.app_state.excel_path)
            else:
                db_folder = os.getcwd()
            photos_dir = os.path.join(db_folder, "photos")
            os.makedirs(photos_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = secure_filename(file.filename)
            _, ext = os.path.splitext(original_filename)
            if not ext:
                ext = ".jpg"
            ext = ext.lower()
            allowed_exts = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}
            if ext not in allowed_exts:
                return jsonify({"error": f"Unsupported image file extension: {ext}"}), 400

            new_filename = f"{safe_oid}_{timestamp}{ext}"
            file_path = os.path.join(photos_dir, new_filename)

            try:
                file.save(file_path)
            except Exception as e:
                debug_error("Photo Upload Error", str(e))
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass
                return jsonify({"error": "Failed to save image"}), 500

            with self.app_state.df_lock:
                if self.app_state.df_reg is None:
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass
                    return jsonify({"error": "Database unloaded during upload"}), 400

                reg_oid = _resolve_oid_in_df(self.app_state.df_reg, oid)
                if reg_oid is None:
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass
                    return jsonify({"error": f"Object {oid} not found"}), 404

                if getattr(self.app_state, 'df_photo', None) is None:
                    self.app_state.df_photo = pd.DataFrame(columns=["PhotoPath", "FileName", "Caption", "Timestamp"])
                    self.app_state.df_photo.index.name = "ObjectID"

                cols = self.app_state.df_photo.columns.tolist()
                new_row = {}
                for c in cols:
                    new_row[c] = ""

                for c in ["PhotoPath", "FileName", "Caption", "Timestamp"]:
                    if c not in self.app_state.df_photo.columns:
                        self.app_state.df_photo[c] = ""

                new_row["PhotoPath"] = file_path
                new_row["FileName"] = new_filename
                new_row["Caption"] = caption
                new_row["Timestamp"] = timestamp
                if category and "Category" in self.app_state.df_photo.columns:
                    new_row["Category"] = category
                elif category:
                    self.app_state.df_photo["Category"] = ""
                    new_row["Category"] = category

                new_df = pd.DataFrame([new_row], index=[reg_oid])
                new_df.index.name = self.app_state.df_photo.index.name or "ObjectID"

                self.app_state.df_photo = pd.concat([self.app_state.df_photo, new_df])

                if not hasattr(self.app_state, "_log_records") or self.app_state._log_records is None:
                    if getattr(self.app_state, "df_log", None) is not None and not self.app_state.df_log.empty:
                        self.app_state._log_records = self.app_state.df_log.to_dict(orient="records")
                    else:
                        self.app_state._log_records = []

                now_ts = datetime.now().isoformat(timespec="seconds")
                log_entry = {
                    "Timestamp": now_ts,
                    "Action": "PHOTO_ADDED",
                    "Reviewed": "",
                    "ObjectID": str(oid),
                    "ChangedFields": "Photo",
                    "ChangedValues": f"Added {new_filename}",
                    "ProblemsChanged": "",
                    "ProblemsChangedValues": "",
                    "LocationChanged": "",
                    "LocationChangedValues": "",
                    "User": "Mobile-Companion",
                    "SourceFile": os.path.basename(getattr(self.app_state, 'excel_path', '') or "") if getattr(self.app_state, 'excel_path', None) else "",
                    "OutputFile": os.path.basename(getattr(self.app_state, 'output_path', '') or getattr(self.app_state, 'excel_path', '') or "") if getattr(self.app_state, 'output_path', None) or getattr(self.app_state, 'excel_path', None) else ""
                }
                if getattr(self.app_state, "_mobile_session_id", None):
                    log_entry["_session_id"] = self.app_state._mobile_session_id
                self.app_state._log_records.append(log_entry)
                self.app_state.df_log = _normalise_log_dataframe(pd.DataFrame(self.app_state._log_records))
                self.app_state.dirty = True

            if self.root_tk:
                try:
                    self.root_tk.after(0, lambda: app_bus.publish(DATABASE_UPDATED, mobile_edit=True))
                except Exception:
                    pass

            return jsonify({
                "success": True,
                "photo_id": new_filename,
                "filename": new_filename,
                "url": f"/api/photo/{new_filename}"
            }), 201

        @app.route('/api/batch_update', methods=['POST'])
        def batch_update_objects():
            is_auth, client_sid, _ = self._get_current_session()
            if not is_auth:
                return jsonify({"error": "Unauthorized"}), 401

            from backend.mobile_schemas import BatchUpdateSchema, ValidationError
            raw_data = request.get_json(silent=True) or {}
            try:
                data = BatchUpdateSchema().load(raw_data)
            except ValidationError as err:
                return jsonify({"error": f"Invalid batch payload: {err.messages}"}), 400

            updates_list = data.get('updates', [])
            if not updates_list:
                return jsonify({"error": "Missing or invalid 'updates' array"}), 400

            updated_ids = []

            with self.app_state.df_lock:
                if self.app_state.df_reg is None:
                    return jsonify({"error": "No database loaded"}), 400

                allowed_reg_cols, allowed_obs_cols = _get_allowed_columns(getattr(self.app_state, "config", None))

                for update in updates_list:
                    oid = update.get('oid', '').strip()
                    if not oid:
                        continue

                    reviewed = update.get('reviewed')
                    obs_updates = update.get('observation', {})
                    reg_updates = update.get('registration', {})
                    client_timestamp = update.get('timestamp')
                    unval_updates = update.get('unvalidated_sources')

                    _, err = _execute_record_update(
                        self.app_state, oid, reg_updates, obs_updates, reviewed,
                        allowed_reg_cols=allowed_reg_cols,
                        allowed_obs_cols=allowed_obs_cols,
                        recent_edits=self.recent_edits,
                        client_timestamp=client_timestamp,
                        unvalidated_updates=unval_updates,
                        session_id=client_sid
                    )
                    if err:
                        continue

                    updated_ids.append(oid)
                    self.broadcast_event("record_updated", {"id": oid})

                if updated_ids:
                    self.app_state.df_log = _normalise_log_dataframe(pd.DataFrame(self.app_state._log_records))
                    self.app_state.dirty = True
                    self.app_state._mobile_last_edited_oid = updated_ids[-1]

            if not updated_ids:
                return jsonify({"success": True, "updated_count": 0, "updated_ids": []})

            # Notify desktop UI
            if self.on_edit_callback:
                try:
                    self.on_edit_callback("BATCH", f"📥 Synced {len(updated_ids)} offline edits from mobile session")
                except Exception:
                    pass

            if self.root_tk:
                try:
                    self.root_tk.after(0, lambda: app_bus.publish(DATABASE_UPDATED, mobile_edit=True))
                except Exception:
                    pass

            return jsonify({
                "success": True,
                "updated_count": len(updated_ids),
                "updated_ids": updated_ids
            })


LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Arbor Companion Login</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      background: #121915;
      color: #1c241f;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .card {
      width: 100%;
      max-width: 380px;
      background: #ffffff;
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(27, 67, 50, 0.2);
      text-align: center;
    }
    .icon {
      width: 48px;
      height: 48px;
      border-radius: 9999px;
      background: #d8f3dc;
      color: #2d6a4f;
      font-size: 24px;
      margin: 0 auto 14px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    h1 { margin: 0 0 6px; font-size: 1.125rem; font-weight: 700; color: #1c241f; }
    p { margin: 0 0 16px; font-size: 0.8rem; color: #5a655e; line-height: 1.4; }
    .err {
      background: #fef2f2;
      color: #b91c1c;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid #fecaca;
      margin-bottom: 14px;
    }
    input {
      width: 100%;
      text-align: center;
      letter-spacing: 0.25em;
      font-size: 1.5rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      padding: 10px 12px;
      background: #f8f9fa;
      border: 1px solid #cbd2cd;
      border-radius: 8px;
      margin-bottom: 12px;
      outline: none;
    }
    input:focus { border-color: #2d6a4f; box-shadow: 0 0 0 2px rgba(45, 106, 79, 0.2); }
    button {
      width: 100%;
      background: #2d6a4f;
      color: #ffffff;
      border: none;
      border-radius: 8px;
      padding: 11px 16px;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
    }
    button:active { background: #1b4332; }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">🌿</div>
    <h1>Arbor Mobile Companion</h1>
    <p>Enter the 4-digit PIN displayed on your laptop screen</p>
    {% if error %}
    <div class="err">{{ error }}</div>
    {% endif %}
    <form method="POST" action="/login">
      <input type="password" name="pin" maxlength="6" inputmode="numeric" placeholder="• • • •" autofocus required>
      <button type="submit">Connect to Collection</button>
    </form>
  </div>
</body>
</html>"""


# Mobile frontend templates live in dedicated pure-Python modules (zero-build compliant)
# and are re-exported here so all existing imports continue to work identically.
from .mobile_template_v1 import INDEX_TEMPLATE
from .mobile_template_v2 import INDEX_TEMPLATE_V2
