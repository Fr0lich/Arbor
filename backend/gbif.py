import difflib
import requests
import concurrent.futures
import functools
import re
import threading
from typing import List, Dict, Optional, Any
from cachetools import LRUCache

_thread_local = threading.local()
_session = requests.Session()  # Kept for backward-compat / test mocking


def _get_session() -> requests.Session:
    """Return a thread-local requests.Session, or module _session if patched in tests."""
    if not isinstance(_session, requests.Session) or getattr(_session.get, "__self__", None) is not _session:
        return _session
    sess = getattr(_thread_local, "session", None)
    if sess is None:
        sess = requests.Session()
        _thread_local.session = sess
    return sess


_gbif_cache_lock = threading.Lock()
_check_gbif_cache: LRUCache = LRUCache(maxsize=1024)
_accepted_name_cache: LRUCache = LRUCache(maxsize=1024)
_synonyms_cache: LRUCache = LRUCache(maxsize=1024)

CLASSICAL_FAMILY_NAMES = {
    "compositae", "cruciferae", "gramineae", "guttiferae",
    "labiatae", "leguminosae", "palmae", "umbelliferae"
}


def is_likely_family_name(name: Any) -> bool:
    """Returns True if string matches botanical family patterns (-aceae, classic names)."""
    if not name:
        return False
    s = str(name).strip().lower()
    if s.endswith("aceae") or s.endswith("oideae") or s.endswith("ineae") or s.endswith("phyta"):
        return True
    return s in CLASSICAL_FAMILY_NAMES

UNDETERMINED_SPECIES_EXACT = {
    "", "sp", "sp.", "spp", "spp.", "spec", "spec.", "species",
    "indet", "indet.", "undet", "undet.", "unknown", "?", "-", "--",
    "none", "n/a", "na", "null"
}

_MORPHOSPECIES_PATTERN = re.compile(
    r"^(sp\.?|spec\.?|indet\.?|species)\s*([0-9]+|[a-zA-Z]|nov\.?|nr\.?|aff\.?|cf\.?.*)?$",
    re.IGNORECASE
)


def is_undetermined_species(species: Any) -> bool:
    """
    Returns True if species string indicates an undetermined taxon, open nomenclature,
    morphospecies, or unassigned species (e.g. 'sp.', 'spp.', 'indet.', 'sp. 1', 'sp. nov.', '?').
    """
    if species is None:
        return True
    s = str(species).strip().lower()
    if s in UNDETERMINED_SPECIES_EXACT:
        return True
    s_clean = s.rstrip(".").strip()
    if s_clean in UNDETERMINED_SPECIES_EXACT:
        return True
    if _MORPHOSPECIES_PATTERN.match(s):
        return True
    return False


def check_gbif(genus: str, species: str):
    genus = (genus or "").strip()
    species = (species or "").strip()
    name = f"{genus} {species}".strip()
    if not name or not genus:
        return None
    cache_key = (genus, species)
    with _gbif_cache_lock:
        cached = _check_gbif_cache.get(cache_key)
        if cached is not None:
            return cached.copy()
    url = "https://api.gbif.org/v1/species/match"
    params = {"name": name}
    if genus:
        params["genus"] = genus
    try:
        response = _get_session().get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        scientific_name = data.get("scientificName", "")
        canonical_name = data.get("canonicalName", "")

        # get authorship directly if available, otherwise fallback to parsing
        author = data.get("authorship", "")
        if not author:
             author = scientific_name.replace(canonical_name, "").strip() if canonical_name and scientific_name.startswith(canonical_name) else ""

        rank = (data.get("rank") or "").upper()
        # The gbif API sometimes returns exact matches for genus only if species is not found.
        if rank == "GENUS" and species:
            match_type = "HIGHERRANK"
        else:
            match_type = data.get("matchType")

        new_genus = data.get("genus", "")

        # Guard: Higher ranks (e.g. FAMILY Pinaceae) must NEVER be assigned as species!
        if rank in ("FAMILY", "ORDER", "CLASS", "PHYLUM", "KINGDOM") or match_type == "HIGHERRANK":
            new_species = ""
        else:
            new_species = data.get("species", "")
            if not new_species and rank == "SPECIES":
                new_species = canonical_name
            if new_genus and new_species and new_species.startswith(new_genus + " "):
                new_species = new_species[len(new_genus):].strip()

        family = data.get("family", "")
        if not family and rank == "FAMILY":
            family = canonical_name

        higher_classification = " | ".join(filter(None, [
            (data.get("kingdom") or "").strip(),
            (data.get("phylum") or "").strip(),
            (data.get("class") or "").strip(),
            (data.get("order") or "").strip()
        ]))

        result = {
            "matchType": match_type,
            "status": data.get("status"),
            "canonicalName": data.get("canonicalName"),
            "scientificName": data.get("scientificName"),
            "genus": new_genus,
            "species": new_species,
            "author": author,
            "family": family,
            "higherClassification": higher_classification,
            "rank": rank,
            "confidence": data.get("confidence", 0),
            "usageKey": data.get("usageKey"),
            "taxonKey": data.get("usageKey"),
            "synonym": data.get("status") == "SYNONYM",
            "acceptedUsageKey": data.get("acceptedUsageKey"),
        }
        with _gbif_cache_lock:
            _check_gbif_cache[cache_key] = result
        return result.copy()
    except Exception as e:
        print(f"Error checking GBIF: {e}")
        # Never cache transient/offline errors so reconnecting works immediately
        return {"error": str(e)}


def _clear_gbif_caches():
    with _gbif_cache_lock:
        _check_gbif_cache.clear()
        _accepted_name_cache.clear()
        _synonyms_cache.clear()


check_gbif.cache_clear = _clear_gbif_caches


def get_accepted_name(usage_key: int):
    with _gbif_cache_lock:
        cached = _accepted_name_cache.get(usage_key)
        if cached is not None:
            return cached.copy()
    url = f"https://api.gbif.org/v1/species/{usage_key}"
    try:
        response = _get_session().get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        scientific_name = data.get("scientificName", "")
        canonical_name = data.get("canonicalName", "")

        author = data.get("authorship", "")
        if not author:
             author = scientific_name.replace(canonical_name, "").strip() if canonical_name and scientific_name.startswith(canonical_name) else ""

        new_genus = data.get("genus", "")
        rank = (data.get("rank") or "").upper()
        if rank in ("FAMILY", "ORDER", "CLASS", "PHYLUM", "KINGDOM"):
            new_species = ""
        else:
            new_species = data.get("species", "")
            if not new_species and rank == "SPECIES":
                new_species = canonical_name
            if new_genus and new_species and new_species.startswith(new_genus + " "):
                new_species = new_species[len(new_genus):].strip()

        family = data.get("family", "")
        if not family and rank == "FAMILY":
            family = canonical_name

        higher_classification = " | ".join(filter(None, [
            (data.get("kingdom") or "").strip(),
            (data.get("phylum") or "").strip(),
            (data.get("class") or "").strip(),
            (data.get("order") or "").strip()
        ]))

        result = {
            "canonicalName": data.get("canonicalName"),
            "scientificName": data.get("scientificName"),
            "genus": new_genus,
            "species": new_species,
            "author": author,
            "family": family,
            "higherClassification": higher_classification,
            "rank": rank,
            "status": data.get("status", "ACCEPTED"),
            "usageKey": usage_key,
            "taxonKey": usage_key,
        }
        with _gbif_cache_lock:
            _accepted_name_cache[usage_key] = result
        return result.copy()
    except Exception as e:
        print(f"Error checking GBIF accepted name: {e}")
        return {"error": str(e)}


get_accepted_name.cache_clear = _clear_gbif_caches


def is_author_equivalent(a1: Any, a2: Any) -> bool:
    """Compare two author strings taking into account abbreviations, spacing, and punctuation."""
    s1 = str(a1 or "").strip()
    s2 = str(a2 or "").strip()
    if not s1 and not s2:
        return True
    if not s1 or not s2:
        return False
    if s1 == s2:
        return True
    norm1 = s1.replace(".", "").replace(",", "").replace("(", "").replace(")", "").replace(" ", "").lower()
    norm2 = s2.replace(".", "").replace(",", "").replace("(", "").replace(")", "").replace(" ", "").lower()
    return norm1 == norm2


def is_classification_equivalent(existing_val: Any, gbif_val: Any) -> bool:
    """Compare existing higher classification against GBIF considering rank depth, formatting, and division synonyms."""
    if existing_val is None or gbif_val is None:
        return False
    e_str = str(existing_val).strip()
    g_str = str(gbif_val).strip()
    if not e_str and not g_str:
        return True
    if not e_str or not g_str:
        return False
    if e_str == g_str:
        return True

    import re
    def tokenize(s):
        raw_tokens = re.split(r"[|/;,]+", s)
        tokens = []
        for t in raw_tokens:
            cleaned = t.strip().lower()
            if cleaned:
                if cleaned in ("magnoliophyta", "angiospermae", "spermatophyta", "anthophyta"):
                    cleaned = "tracheophyta"
                elif cleaned in ("pinophyta", "coniferophyta", "gymnospermae"):
                    cleaned = "tracheophyta"
                tokens.append(cleaned)
        return tokens

    e_tokens = tokenize(e_str)
    g_tokens = tokenize(g_str)

    if not e_tokens or not g_tokens:
        return False

    if e_tokens == g_tokens:
        return True

    set_e = set(e_tokens)
    set_g = set(g_tokens)

    if set_e == set_g:
        return True

    # If existing has all GBIF ranks plus extras (e.g. family or subranks), it is equivalent
    if set_g.issubset(set_e):
        return True

    # If existing has at least 3 ranks (e.g. Class+Order+Kingdom) and matches GBIF ranks, it is equivalent
    if len(e_tokens) >= 3 and set_e.issubset(set_g):
        return True

    return False


def _process_single_item(item: Dict[str, Any], cancel_event=None) -> Optional[Dict[str, Any]]:
    """Process a single item against GBIF and return proposed changes if any."""
    if cancel_event and cancel_event.is_set():
        return None

    oid = str(item.get("oid", ""))
    genus = str(item.get("genus", "") or "").strip()
    species = str(item.get("species", "") or "").strip()
    author = str(item.get("author", "") or "").strip()
    family = str(item.get("family", "") or "").strip()

    if not genus:
        return None

    gbif_data = check_gbif(genus, species)
    if not gbif_data or "error" in gbif_data:
        return None

    # If synonym, optionally fetch accepted name
    if gbif_data.get("synonym") and gbif_data.get("acceptedUsageKey"):
        if cancel_event and cancel_event.is_set():
            return None
        acc_data = get_accepted_name(gbif_data["acceptedUsageKey"])
        if acc_data and "error" not in acc_data:
            if acc_data.get("genus"):
                gbif_data["genus"] = acc_data["genus"]
            if acc_data.get("species"):
                gbif_data["species"] = acc_data["species"]
            if acc_data.get("author"):
                gbif_data["author"] = acc_data["author"]
            if acc_data.get("family"):
                gbif_data["family"] = acc_data["family"]

    prop_genus = gbif_data.get("genus") or ""
    prop_species = gbif_data.get("species") or ""
    prop_author = gbif_data.get("author") or ""
    prop_family = gbif_data.get("family") or ""

    current_map = {
        "Genus": genus,
        "Species": species,
        "Author": author,
        "Family": family,
    }
    proposed_map = {
        "Genus": prop_genus,
        "Species": prop_species,
        "Author": prop_author,
        "Family": prop_family,
    }

    changes = []
    for k in ["Genus", "Species", "Author", "Family"]:
        c_val = current_map[k]
        p_val = proposed_map[k]
        if k == "Author":
            if p_val and not is_author_equivalent(c_val, p_val):
                changes.append({"field": k, "old": c_val, "new": p_val})
        elif k == "Family":
            if p_val and p_val.lower() != c_val.lower():
                changes.append({"field": k, "old": c_val, "new": p_val})
        else:
            if p_val and p_val != c_val:
                changes.append({"field": k, "old": c_val, "new": p_val})

    if changes:
        return {
            "oid": oid,
            "current": current_map,
            "proposed": proposed_map,
            "changes": changes,
            "match_type": gbif_data.get("matchType") or "MATCH",
            "status": gbif_data.get("status") or "ACCEPTED",
            "rank": gbif_data.get("rank") or "SPECIES"
        }
    return None


def _query_single_taxon(genus: str, species: str, cancel_event=None) -> Optional[Dict[str, Any]]:
    """
    Query GBIF for a single genus/species taxon combination, resolving synonyms and family hierarchy.
    If species is undetermined ('sp.', 'indet.', blank), queries at genus rank.
    """
    if cancel_event and cancel_event.is_set():
        return None
    if not genus:
        return None

    is_undet = is_undetermined_species(species)
    # If undetermined, query genus only
    query_species = "" if is_undet else species

    gbif_data = check_gbif(genus, query_species)
    if not gbif_data or "error" in gbif_data:
        return None

    original_scientific_name = gbif_data.get("scientificName") or f"{genus} {query_species}".strip()
    is_synonym = bool(gbif_data.get("synonym"))
    accepted_scientific_name = ""

    if is_synonym and gbif_data.get("acceptedUsageKey"):
        if cancel_event and cancel_event.is_set():
            return None
        acc_data = get_accepted_name(gbif_data["acceptedUsageKey"])
        if acc_data and "error" not in acc_data:
            accepted_scientific_name = acc_data.get("scientificName") or ""
            if acc_data.get("genus"):
                gbif_data["genus"] = acc_data["genus"]
            if not is_undet and acc_data.get("species"):
                gbif_data["species"] = acc_data["species"]
            if not is_undet and acc_data.get("author"):
                gbif_data["author"] = acc_data["author"]
            if acc_data.get("family"):
                gbif_data["family"] = acc_data["family"]

    gbif_data["is_undetermined"] = is_undet
    gbif_data["is_synonym"] = is_synonym
    gbif_data["original_scientific_name"] = original_scientific_name
    gbif_data["accepted_scientific_name"] = accepted_scientific_name
    if is_undet:
        gbif_data["species"] = species
        gbif_data["rank"] = "GENUS"

    return gbif_data


def _evaluate_item_diff(item: Dict[str, Any], gbif_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Compare an individual item against resolved GBIF data and produce diffs with taxonomic reasons."""
    if not gbif_data or "error" in gbif_data:
        return None

    oid = str(item.get("oid", ""))
    genus = str(item.get("genus", "") or "").strip()
    species = str(item.get("species", "") or "").strip()
    author = str(item.get("author", "") or "").strip()
    family = str(item.get("family", "") or "").strip()

    is_undet = is_undetermined_species(species) or gbif_data.get("is_undetermined", False)
    is_synonym = gbif_data.get("is_synonym", False)

    prop_genus = gbif_data.get("genus") or ""
    # If undetermined, NEVER change species name, but check Genus Author
    if is_undet:
        prop_species = species
        prop_author = gbif_data.get("author") or ""
    else:
        prop_species = gbif_data.get("species") or ""
        prop_author = gbif_data.get("author") or ""

    prop_family = gbif_data.get("family") or ""

    current_map = {
        "Genus": genus,
        "Species": species,
        "Author": author,
        "Family": family,
    }
    proposed_map = {
        "Genus": prop_genus,
        "Species": prop_species,
        "Author": prop_author,
        "Family": prop_family,
    }

    changes = []
    for k in ["Genus", "Species", "Author", "Family"]:
        c_val = current_map[k]
        p_val = proposed_map[k]

        if k == "Author":
            if p_val and not is_author_equivalent(c_val, p_val):
                if not c_val:
                    r_code = "MISSING_AUTHOR"
                    r_lbl = "+ Missing Author"
                    expl = f"Populated {'Genus' if is_undet else 'Species'} author '{p_val}' from GBIF."
                else:
                    r_code = "AUTHOR_STANDARDIZED"
                    r_lbl = "Author Standardized"
                    expl = f"Standardized author from '{c_val}' to '{p_val}'."
                changes.append({
                    "field": k, "old": c_val, "new": p_val,
                    "reason_code": r_code, "reason_label": r_lbl, "explanation": expl,
                    "has_rank_discrepancy": False, "auto_resolve_eligible": True
                })
        elif k == "Family":
            if p_val and p_val.lower() != c_val.lower():
                if not c_val:
                    r_code = "MISSING_FAMILY"
                    r_lbl = "+ Missing Family"
                    expl = f"Assigned family '{p_val}' from GBIF classification for genus '{prop_genus}'."
                else:
                    r_code = "FAMILY_UPDATE"
                    r_lbl = "Family Reclassified"
                    expl = f"Updated family classification from '{c_val}' to '{p_val}'."
                changes.append({
                    "field": k, "old": c_val, "new": p_val,
                    "reason_code": r_code, "reason_label": r_lbl, "explanation": expl,
                    "has_rank_discrepancy": False, "auto_resolve_eligible": True
                })
        elif k == "Species":
            if not is_undet and p_val and p_val != c_val:
                is_c_family = is_likely_family_name(c_val) or (c_val and family and c_val.lower() == family.lower())
                is_p_family = is_likely_family_name(p_val) or (p_val and prop_family and p_val.lower() == prop_family.lower())
                sim = difflib.SequenceMatcher(None, c_val.lower(), p_val.lower()).ratio() if c_val and p_val else 0.0

                if is_c_family or is_p_family:
                    r_code = "RANK_DISCREPANCY"
                    r_lbl = "⚠️ Rank Discrepancy (Species / Family)"
                    expl = f"Species '{c_val}' detected as a family-level rank or inversion. Replacement: '{p_val}'."
                    has_rank_disc = True
                    auto_res = False
                elif is_synonym:
                    r_code = "SYNONYM_SPECIES"
                    r_lbl = "Accepted Species (Synonym)"
                    expl = f"'{species}' is an older synonym for accepted species '{p_val}'."
                    has_rank_disc = False
                    auto_res = True
                elif sim >= 0.70 or gbif_data.get("matchType") == "FUZZY":
                    r_code = "SPELLING"
                    r_lbl = "Spelling / Typo Fix"
                    expl = f"Corrected species spelling from '{c_val}' to '{p_val}'."
                    has_rank_disc = False
                    auto_res = True
                else:
                    r_code = "RECLASSIFICATION"
                    r_lbl = "⚠️ Taxonomic Reclassification"
                    expl = f"GBIF proposes changing species from '{c_val}' to '{p_val}' (similarity {int(sim*100)}%)."
                    has_rank_disc = False
                    auto_res = False

                changes.append({
                    "field": k, "old": c_val, "new": p_val,
                    "reason_code": r_code, "reason_label": r_lbl, "explanation": expl,
                    "has_rank_discrepancy": has_rank_disc,
                    "auto_resolve_eligible": auto_res
                })
        else:  # Genus
            if p_val and p_val != c_val:
                is_c_family = is_likely_family_name(c_val)
                is_p_family = is_likely_family_name(p_val)
                sim = difflib.SequenceMatcher(None, c_val.lower(), p_val.lower()).ratio() if c_val and p_val else 0.0

                if is_c_family or is_p_family:
                    r_code = "RANK_DISCREPANCY"
                    r_lbl = "⚠️ Rank Discrepancy (Genus / Family)"
                    expl = f"Genus '{c_val}' detected as a family-level rank. Replacement: '{p_val}'."
                    has_rank_disc = True
                    auto_res = False
                elif is_synonym:
                    r_code = "SYNONYM_GENUS"
                    r_lbl = "⚠️ Reclassified Genus (Synonym)"
                    expl = f"'{genus} {species}'.strip() is cataloged as a synonym for modern combination '{prop_genus} {prop_species}'.strip() in GBIF."
                    has_rank_disc = False
                    auto_res = True
                elif sim >= 0.70 or gbif_data.get("matchType") == "FUZZY":
                    r_code = "SPELLING"
                    r_lbl = "🔤 Spelling / Typo Fix"
                    expl = f"Corrected genus spelling from '{c_val}' to '{p_val}'."
                    has_rank_disc = False
                    auto_res = True
                else:
                    r_code = "RECLASSIFICATION"
                    r_lbl = "⚠️ Reclassified Genus"
                    expl = f"GBIF proposes changing genus from '{c_val}' to '{p_val}'."
                    has_rank_disc = False
                    auto_res = False

                changes.append({
                    "field": k, "old": c_val, "new": p_val,
                    "reason_code": r_code, "reason_label": r_lbl, "explanation": expl,
                    "has_rank_discrepancy": has_rank_disc,
                    "auto_resolve_eligible": auto_res
                })

    item_has_inversion = is_likely_family_name(species) or (species and family and species.lower() == family.lower())
    has_rank_discrepancy = any(c.get("has_rank_discrepancy") for c in changes) or item_has_inversion
    rank_disc_str = "⚠️ Species → Family" if (item_has_inversion or any(c.get("reason_code") == "RANK_DISCREPANCY" for c in changes)) else ""
    auto_resolve_eligible = not has_rank_discrepancy and all(c.get("auto_resolve_eligible", True) for c in changes)

    if changes:
        missing_family = (not bool(family)) and bool(prop_family)
        missing_author = (not bool(author)) and bool(prop_author)
        return {
            "oid": oid,
            "current": current_map,
            "proposed": proposed_map,
            "changes": changes,
            "match_type": gbif_data.get("matchType") or "MATCH",
            "status": "SYNONYM" if is_synonym else (gbif_data.get("status") or "ACCEPTED"),
            "rank": gbif_data.get("rank") or ("GENUS" if is_undet else "SPECIES"),
            "is_undetermined": is_undet,
            "is_synonym": is_synonym,
            "missing_family": missing_family,
            "missing_author": missing_author,
            "original_scientific_name": gbif_data.get("original_scientific_name", ""),
            "accepted_scientific_name": gbif_data.get("accepted_scientific_name", ""),
            "has_rank_discrepancy": has_rank_discrepancy,
            "rank_discrepancy": rank_disc_str,
            "auto_resolve_eligible": auto_resolve_eligible
        }
    return None


def batch_gbif_match(
    items: List[Dict[str, Any]],
    progress_callback=None,
    cancel_event=None,
    max_workers: Optional[int] = None,
    exclude_undetermined: bool = False,
    stats_out: Optional[Dict[str, int]] = None
) -> List[Dict[str, Any]]:
    """
    Query GBIF concurrently for unique taxa and return proposed taxonomic changes across all items.
    Supports excluding undetermined ('sp.') specimens or validating their Family/Genus safely.
    """
    if not items:
        return []

    if exclude_undetermined:
        items = [item for item in items if not is_undetermined_species(item.get("species"))]
        if not items:
            return []

    if max_workers is None:
        try:
            import config
            prefs = config.load_prefs()
            max_workers = int(prefs.get("gbif_max_workers", 5))
        except Exception:
            max_workers = 5
    max_workers = max(1, min(10, max_workers))

    # 1. Deduplicate unique taxa:
    # Binomials map to (genus_lower, species_lower) -> (genus, species)
    # Undetermined taxa map to (genus_lower, "__undetermined__") -> (genus, "")
    unique_taxa = {}
    for item in items:
        g = str(item.get("genus", "") or "").strip()
        s = str(item.get("species", "") or "").strip()
        if g:
            if is_undetermined_species(s):
                key = (g.lower(), "__undetermined__")
                if key not in unique_taxa:
                    unique_taxa[key] = (g, s)
            else:
                key = (g.lower(), s.lower())
                if key not in unique_taxa:
                    unique_taxa[key] = (g, s)

    if not unique_taxa:
        return []

    total_taxa = len(unique_taxa)
    taxon_cache = {}
    completed_taxa = 0
    error_count = 0

    # 2. Query GBIF concurrently only for distinct taxa
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_key = {
            executor.submit(_query_single_taxon, g, s, cancel_event): key
            for key, (g, s) in unique_taxa.items()
        }

        for future in concurrent.futures.as_completed(future_to_key):
            if cancel_event and cancel_event.is_set():
                break

            key = future_to_key[future]
            completed_taxa += 1

            if progress_callback:
                try:
                    display_name = f"{unique_taxa[key][0]} {unique_taxa[key][1]}".strip()
                    progress_callback(completed_taxa, total_taxa, display_name)
                except Exception:
                    pass

            try:
                gbif_res = future.result()
                taxon_cache[key] = gbif_res
                if isinstance(gbif_res, dict) and gbif_res.get("error"):
                    error_count += 1
            except Exception as e:
                print(f"Error querying taxon {key}: {e}")
                taxon_cache[key] = None
                error_count += 1

    if stats_out is not None:
        stats_out["total_taxa"] = total_taxa
        stats_out["error_count"] = error_count

    if cancel_event and cancel_event.is_set():
        return []

    # 3. Evaluate diffs for each item against the resolved taxon cache
    results = []
    for item in items:
        g = str(item.get("genus", "") or "").strip()
        s = str(item.get("species", "") or "").strip()
        if is_undetermined_species(s):
            key = (g.lower(), "__undetermined__")
        else:
            key = (g.lower(), s.lower())
        gbif_data = taxon_cache.get(key)
        diff = _evaluate_item_diff(item, gbif_data)
        if diff:
            results.append(diff)

    return results


# ── Old Names / Synonyms & Offline Family Aliases ─────────────────────────────

# Classical botanical family pairs (modern -> classical)
_CLASSICAL_FAMILY_PAIRS = [
    ("Asteraceae", "Compositae"),
    ("Fabaceae", "Leguminosae"),
    ("Poaceae", "Gramineae"),
    ("Lamiaceae", "Labiatae"),
    ("Apiaceae", "Umbelliferae"),
    ("Brassicaceae", "Cruciferae"),
    ("Arecaceae", "Palmae"),
    ("Clusiaceae", "Guttiferae"),
]

# Common APG family merges/splits (modern -> list of older family names frequently seen on museum labels)
_APG_OLD_FAMILIES: Dict[str, List[str]] = {
    "Malvaceae": ["Tiliaceae", "Sterculiaceae", "Bombacaceae"],
    "Plantaginaceae": ["Scrophulariaceae", "Callitrichaceae", "Hippuridaceae"],
    "Orobanchaceae": ["Scrophulariaceae"],
    "Asparagaceae": ["Liliaceae", "Agavaceae", "Convallariaceae", "Hyacinthaceae", "Ruscaceae"],
    "Amaryllidaceae": ["Alliaceae", "Liliaceae"],
    "Sapindaceae": ["Aceraceae", "Hippocastanaceae"],
    "Amaranthaceae": ["Chenopodiaceae"],
    "Apocynaceae": ["Asclepiadaceae"],
    "Fabaceae": ["Caesalpiniaceae", "Mimosaceae", "Papilionaceae"],
    "Cupressaceae": ["Taxodiaceae"],
    "Papaveraceae": ["Fumariaceae"],
    "Adoxaceae": ["Caprifoliaceae"],
    "Viburnaceae": ["Caprifoliaceae", "Adoxaceae"],
    "Salicaceae": ["Flacourtiaceae"],
    "Phyllanthaceae": ["Euphorbiaceae"],
    "Hypericaceae": ["Guttiferae", "Clusiaceae"],
    "Primulaceae": ["Myrsinaceae"],
    "Ericaceae": ["Pyrolaceae", "Monotropaceae", "Empetraceae"],
    "Rosaceae": ["Amygdalaceae", "Pomaceae"],
    "Cannabaceae": ["Ulmaceae", "Celtidaceae"],
}


def get_old_family_names(family: Any) -> List[Dict[str, str]]:
    """Return known classical and major APG older family names for a given family (100% offline)."""
    fam = str(family or "").strip()
    if not fam:
        return []
    fam_low = fam.lower()
    seen = {fam_low}
    out: List[Dict[str, str]] = []

    def _add(name: str, note: str):
        nl = name.lower()
        if nl not in seen:
            seen.add(nl)
            out.append({"name": name, "note": note})

    for modern, classical in _CLASSICAL_FAMILY_PAIRS:
        if fam_low == modern.lower():
            _add(classical, f"Classical name for {modern}")
        elif fam_low == classical.lower():
            _add(modern, f"Modern name for {classical}")

    for modern, olds in _APG_OLD_FAMILIES.items():
        if fam_low == modern.lower():
            for old in olds:
                _add(old, f"Earlier family placement (now {modern})")
        else:
            for old in olds:
                if fam_low == old.lower():
                    _add(modern, f"Modern APG family (includes {old})")
    return out


def get_synonym_cache_path(workbook_path: Optional[str]) -> Optional[str]:
    """Return path to the silent per-workbook synonym cache JSON file."""
    if not workbook_path:
        return None
    import os
    try:
        folder = os.path.dirname(os.path.abspath(str(workbook_path)))
        if folder and os.path.isdir(folder):
            return os.path.join(folder, ".arbor_synonyms_cache.json")
    except Exception:
        pass
    return None


def _load_disk_synonym_cache(cache_path: Optional[str]) -> Dict[str, Any]:
    if not cache_path:
        return {}
    import json
    import os
    try:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _save_disk_synonym_cache_entry(cache_path: Optional[str], key: str, payload: Dict[str, Any]) -> None:
    if not cache_path:
        return
    import json
    import os
    import tempfile
    try:
        with _gbif_cache_lock:
            existing = _load_disk_synonym_cache(cache_path)
            existing[key] = payload
            # Keep cache compact (cap at 2000 taxa)
            if len(existing) > 2000:
                for k in list(existing.keys())[:-2000]:
                    existing.pop(k, None)
            folder = os.path.dirname(cache_path)
            fd, tmp_path = tempfile.mkstemp(prefix=".arbor_syn_", suffix=".tmp", dir=folder)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(existing, f, ensure_ascii=False)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, cache_path)
            except Exception:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
    except Exception:
        pass


def get_synonyms(
    genus: str,
    species: str = "",
    family: str = "",
    cache_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch known old names (basionym, homotypic, heterotypic synonyms) and offline old family names
    for a registered taxon. Uses in-memory LRU + silent disk cache for offline vault reliability.
    """
    g = str(genus or "").strip()
    s = str(species or "").strip()
    fam = str(family or "").strip()
    if is_undetermined_species(s):
        s = ""

    old_families = get_old_family_names(fam)
    reg_canonical = f"{g} {s}".strip()
    cache_key = f"{g.lower()}|{s.lower()}"

    base_empty = {
        "registered_name": reg_canonical,
        "registered_family": fam,
        "old_families": old_families,
        "primary_synonyms": [],
        "other_synonyms": [],
        "offline": False,
        "from_cache": False,
    }

    if not g:
        return base_empty

    # 1. Check in-memory LRU cache
    with _gbif_cache_lock:
        mem_hit = _synonyms_cache.get(cache_key)
        if mem_hit is not None:
            res = dict(mem_hit)
            res["old_families"] = get_old_family_names(fam or res.get("registered_family", ""))
            res["from_cache"] = True
            return res

    # 2. Check silent disk cache (fast offline vault path)
    disk_data = _load_disk_synonym_cache(cache_path)
    if cache_key in disk_data and isinstance(disk_data[cache_key], dict):
        res = dict(disk_data[cache_key])
        res["old_families"] = get_old_family_names(fam or res.get("registered_family", ""))
        res["offline"] = False
        res["from_cache"] = True
        with _gbif_cache_lock:
            _synonyms_cache[cache_key] = res
        return res

    # 3. Live GBIF lookup
    match = check_gbif(g, s)
    if not match or (isinstance(match, dict) and match.get("error")):
        base_empty["offline"] = True
        return base_empty

    accepted_key = match.get("acceptedUsageKey") or match.get("usageKey")
    resolved_family = fam or (match.get("family") or "")
    old_families = get_old_family_names(resolved_family)

    if not accepted_key:
        base_empty["old_families"] = old_families
        return base_empty

    basionym_name = ""
    raw_synonyms: List[Dict[str, Any]] = []
    try:
        sess = _get_session()
        sp_resp = sess.get(f"https://api.gbif.org/v1/species/{accepted_key}", timeout=5)
        if sp_resp.ok:
            sp_json = sp_resp.json() or {}
            basionym_name = str(sp_json.get("basionym") or "").strip()

        syn_resp = sess.get(
            f"https://api.gbif.org/v1/species/{accepted_key}/synonyms",
            params={"limit": 100},
            timeout=6,
        )
        syn_resp.raise_for_status()
        raw_synonyms = (syn_resp.json() or {}).get("results") or []
    except Exception:
        base_empty["old_families"] = old_families
        base_empty["offline"] = True
        return base_empty

    reg_low = reg_canonical.lower()
    seen_canon = {reg_low}
    if match.get("canonicalName"):
        seen_canon.add(str(match["canonicalName"]).strip().lower())

    primary: List[Dict[str, str]] = []
    other_species: List[Dict[str, str]] = []
    other_infra: List[Dict[str, str]] = []

    basionym_low = basionym_name.lower()

    for rec in raw_synonyms:
        canon = str(rec.get("canonicalName") or "").strip()
        sci = str(rec.get("scientificName") or "").strip()
        if not canon:
            continue
        cl = canon.lower()
        if cl in seen_canon:
            continue
        seen_canon.add(cl)

        author = str(rec.get("authorship") or "").strip()
        if not author and sci.startswith(canon):
            author = sci[len(canon):].strip()

        status = str(rec.get("taxonomicStatus") or "").upper()
        rank = str(rec.get("rank") or "").upper()

        is_basionym = bool(basionym_low and (basionym_low.startswith(cl) or cl in basionym_low))
        if is_basionym:
            primary.insert(0, {"name": canon, "author": author, "kind": "Basionym"})
        elif status == "HOMOTYPIC_SYNONYM" and rank in ("SPECIES", "GENUS", ""):
            primary.append({"name": canon, "author": author, "kind": "Homotypic"})
        elif rank in ("SPECIES", "GENUS", ""):
            other_species.append({"name": canon, "author": author, "kind": "Synonym"})
        else:
            other_infra.append({"name": canon, "author": author, "kind": rank.title() or "Variant"})

    # If basionym wasn't in the first 100 synonyms, still surface its canonical form
    if basionym_name:
        bas_short = " ".join(basionym_name.split()[:2]).strip()
        if bas_short and bas_short.lower() not in seen_canon:
            seen_canon.add(bas_short.lower())
            bas_author = basionym_name[len(bas_short):].strip() if basionym_name.startswith(bas_short) else ""
            primary.insert(0, {"name": bas_short, "author": bas_author, "kind": "Basionym"})

    result = {
        "registered_name": reg_canonical,
        "registered_family": resolved_family,
        "old_families": old_families,
        "primary_synonyms": primary,
        "other_synonyms": other_species + other_infra,
        "accepted_usage_key": accepted_key,
        "offline": False,
        "from_cache": False,
    }

    with _gbif_cache_lock:
        _synonyms_cache[cache_key] = result
    _save_disk_synonym_cache_entry(cache_path, cache_key, result)
    return dict(result)


def compare_label_name(
    label_name: str,
    reg_genus: str,
    reg_species: str = "",
    reg_family: str = "",
) -> Dict[str, Any]:
    """
    Compare a physical label name/family against a specimen's registered taxon.
    Returns a calibrated, trainee-safe verdict:
      - 'synonym_match': high-confidence known old name / family alias
      - 'different_species': exact match to a different accepted species
      - 'uncertain': offline, low-confidence, higher-rank only, or unlisted
    """
    label = str(label_name or "").strip()
    if not label:
        return {"verdict": "uncertain", "message": "Enter a name from the physical label to check."}

    # 1. Offline family alias check first (instant, zero network)
    label_low = label.lower()
    if reg_family:
        if label_low == str(reg_family).strip().lower():
            return {
                "verdict": "synonym_match",
                "message": f"Matches the registered family ({reg_family}).",
                "matched_name": reg_family,
            }
        for fam_entry in get_old_family_names(reg_family):
            if label_low == fam_entry["name"].lower():
                return {
                    "verdict": "synonym_match",
                    "message": f"Known old family name: {fam_entry['note']}. Keep the modern name.",
                    "matched_name": fam_entry["name"],
                }

    # 2. Live GBIF comparison via acceptedUsageKey
    parts = label.split()
    lbl_g = parts[0]
    lbl_s = parts[1] if len(parts) > 1 else ""

    reg_match = check_gbif(reg_genus, "" if is_undetermined_species(reg_species) else reg_species)
    lbl_match = check_gbif(lbl_g, lbl_s)

    if (
        not reg_match
        or not lbl_match
        or (isinstance(reg_match, dict) and reg_match.get("error"))
        or (isinstance(lbl_match, dict) and lbl_match.get("error"))
    ):
        return {
            "verdict": "uncertain",
            "offline": True,
            "message": "Offline or GBIF unreachable — if unsure, leave a quick note in Comment for desk review.",
        }

    reg_key = reg_match.get("acceptedUsageKey") or reg_match.get("usageKey")
    lbl_key = lbl_match.get("acceptedUsageKey") or lbl_match.get("usageKey")
    lbl_conf = int(lbl_match.get("confidence") or 0)
    lbl_mtype = str(lbl_match.get("matchType") or "").upper()
    lbl_canon = str(lbl_match.get("canonicalName") or label).strip()

    if reg_key and lbl_key and reg_key == lbl_key and lbl_conf >= 85 and lbl_mtype != "HIGHERRANK":
        return {
            "verdict": "synonym_match",
            "message": f"Known old name for {reg_match.get('canonicalName') or reg_genus} (GBIF). Keep the modern name — no edit needed.",
            "matched_name": lbl_canon,
            "matched_author": lbl_match.get("author") or "",
        }

    if lbl_mtype == "EXACT" and lbl_conf >= 90 and lbl_key and reg_key and lbl_key != reg_key:
        # Resolve accepted name for clearer message if label itself is a synonym of another species
        target_name = lbl_canon
        if lbl_match.get("synonym") and lbl_match.get("acceptedUsageKey"):
            acc = get_accepted_name(lbl_match["acceptedUsageKey"])
            if acc and not acc.get("error") and acc.get("canonicalName"):
                target_name = acc["canonicalName"]
        return {
            "verdict": "different_species",
            "message": f"Resolves to a different species ({target_name}), not {reg_match.get('canonicalName') or reg_genus}.",
            "matched_name": target_name,
        }

    return {
        "verdict": "uncertain",
        "message": "Not listed as a known synonym in GBIF — could be an old spelling or unlisted name. If unsure, leave a note in Comment for desk review.",
    }


def record_batch_diffs_to_synonym_cache(
    diff_results: List[Dict[str, Any]],
    cache_path: Optional[str],
) -> int:
    """
    Silently persist old->accepted synonym & family pairs discovered during Batch GBIF
    into the per-workbook `.arbor_synonyms_cache.json` (zero extra network calls).
    Returns the number of unique accepted taxa updated in the cache.
    """
    if not cache_path or not diff_results:
        return 0
    import json
    import os
    import tempfile

    updates: Dict[str, Dict[str, Any]] = {}
    for diff in diff_results:
        if not isinstance(diff, dict):
            continue
        cur = diff.get("current") or {}
        prop = diff.get("proposed") or {}
        cur_g = str(cur.get("Genus") or "").strip()
        cur_s = str(cur.get("Species") or "").strip()
        cur_f = str(cur.get("Family") or "").strip()
        prop_g = str(prop.get("Genus") or cur_g).strip()
        prop_s = str(prop.get("Species") or cur_s).strip()
        prop_f = str(prop.get("Family") or cur_f).strip()
        if not prop_g:
            continue
        if is_undetermined_species(prop_s):
            prop_s = ""
        if is_undetermined_species(cur_s):
            cur_s = ""

        old_canon = f"{cur_g} {cur_s}".strip()
        new_canon = f"{prop_g} {prop_s}".strip()
        has_name_change = bool(old_canon and new_canon and old_canon.lower() != new_canon.lower())
        has_fam_change = bool(cur_f and prop_f and cur_f.lower() != prop_f.lower())
        if not (has_name_change or has_fam_change):
            continue

        key = f"{prop_g.lower()}|{prop_s.lower()}"
        bucket = updates.setdefault(key, {
            "registered_name": new_canon,
            "registered_family": prop_f,
            "names": [],
            "families": [],
        })
        if has_name_change and old_canon not in bucket["names"]:
            bucket["names"].append(old_canon)
        if has_fam_change and cur_f not in bucket["families"]:
            bucket["families"].append(cur_f)

    if not updates:
        return 0

    try:
        with _gbif_cache_lock:
            existing = _load_disk_synonym_cache(cache_path)
            for key, upd in updates.items():
                entry = dict(existing.get(key) or {})
                entry.setdefault("registered_name", upd["registered_name"])
                entry.setdefault("registered_family", upd["registered_family"])
                entry.setdefault("primary_synonyms", [])
                entry.setdefault("other_synonyms", [])
                entry.setdefault("old_families", get_old_family_names(upd["registered_family"]))
                entry["offline"] = False

                seen_names = {
                    str(x.get("name") or "").strip().lower()
                    for x in (entry["primary_synonyms"] + entry["other_synonyms"])
                }
                for old_n in upd["names"]:
                    if old_n.lower() not in seen_names:
                        seen_names.add(old_n.lower())
                        entry["primary_synonyms"].insert(0, {
                            "name": old_n,
                            "author": "",
                            "kind": "Previous name (GBIF)",
                        })

                seen_fams = {str(x.get("name") or "").strip().lower() for x in entry["old_families"]}
                for old_f in upd["families"]:
                    if old_f.lower() not in seen_fams:
                        seen_fams.add(old_f.lower())
                        entry["old_families"].insert(0, {
                            "name": old_f,
                            "note": f"Earlier family in this collection (updated to {upd['registered_family']})",
                        })

                existing[key] = entry
                _synonyms_cache[key] = entry

            if len(existing) > 2000:
                for k in list(existing.keys())[:-2000]:
                    existing.pop(k, None)

            folder = os.path.dirname(cache_path)
            fd, tmp_path = tempfile.mkstemp(prefix=".arbor_syn_", suffix=".tmp", dir=folder)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(existing, f, ensure_ascii=False)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, cache_path)
            except Exception:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
        return len(updates)
    except Exception:
        return 0


def collect_local_old_names(app_state, oid: str) -> List[Dict[str, str]]:
    """Collect any prior Genus/Species/Family for this specimen from local Log & historical ledgers (100% offline)."""
    if app_state is None or not oid:
        return []
    s_oid = str(oid).strip()
    out: List[Dict[str, str]] = []
    seen = set()

    def _add(name: str, source: str):
        n = str(name or "").strip()
        if not n or n.lower() in ("nan", "none", "ukjent", "unknown"):
            return
        key = (n.lower(), source.lower())
        if key not in seen:
            seen.add(key)
            out.append({"name": n, "source": source})

    # 1. Previous GBIF updates recorded on the Log sheet
    df_log = getattr(app_state, "df_log", None)
    if df_log is not None and not df_log.empty and "ObjectID" in df_log.columns:
        try:
            sub = df_log[df_log["ObjectID"].astype(str) == s_oid]
            for _, row in sub.iterrows():
                details = str(row.get("Details") or "")
                for field in ("Genus", "Species", "Family", "Taxon"):
                    m = re.search(rf"{field}:\s*([^\->\n;,]+?)\s*->\s*([^\n;,]+)", details)
                    if m:
                        old_val = m.group(1).strip()
                        if old_val:
                            _add(f"{field}: {old_val}", "Previous update in Log")
        except Exception:
            pass

    # 2. Loaded historical databases & ledger books
    for db in (getattr(app_state, "historical_dbs", None) or []):
        try:
            df_h = db.get("reg_by_id") if db.get("reg_by_id") is not None else db.get("df_reg")
            if df_h is None or df_h.empty:
                continue
            if "ObjectID" in df_h.columns and df_h.index.name != "ObjectID":
                matches = df_h[df_h["ObjectID"].astype(str) == s_oid]
                if matches.empty:
                    continue
                row = matches.iloc[0]
            elif s_oid in df_h.index:
                row = df_h.loc[s_oid]
                if hasattr(row, "iloc") and getattr(row, "ndim", 1) > 1:
                    row = row.iloc[0]
            else:
                continue
            src_name = str(db.get("name") or "Historical DB")
            g = str(row.get("Genus", "") or "").strip()
            s = str(row.get("Species", "") or "").strip()
            f = str(row.get("Family", "") or "").strip()
            if g and g.lower() != "nan":
                _add(f"{g} {s}".strip() if s and s.lower() != "nan" else g, src_name)
            if f and f.lower() != "nan":
                _add(f"Family: {f}", src_name)
        except Exception:
            pass

    return out



