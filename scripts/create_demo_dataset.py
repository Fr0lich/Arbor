import os
from datetime import datetime, timezone
import openpyxl
import pandas as pd


_DEMO_TAXA = [
    ("Betula", "pendula", "Roth", "Betulaceae", "Fagales", "Bark", "Bark"),
    ("Pinus", "sylvestris", "L.", "Pinaceae", "Pinales", "Kongle", "Cone"),
    ("Coffea", "arabica", "L.", "Rubiaceae", "Gentianales", "Frø", "Seed"),
    ("Theobroma", "cacao", "L.", "Malvaceae", "Malvales", "Frukt", "Fruit"),
    ("Gossypium", "hirsutum", "L.", "Malvaceae", "Malvales", "Fiber", "Fiber"),
    ("Quercus", "robur", "L.", "Fagaceae", "Fagales", "Nøtt", "Acorn"),
    ("Picea", "abies", "(L.) H.Karst.", "Pinaceae", "Pinales", "Ved", "Wood"),
    ("Salix", "caprea", "L.", "Salicaceae", "Malpighiales", "Bark", "Bark"),
    ("Juniperus", "communis", "L.", "Cupressaceae", "Pinales", "Bærkongle", "Seed cone"),
    ("Cinchona", "officinalis", "L.", "Rubiaceae", "Gentianales", "Bark", "Bark"),
    ("Piper", "nigrum", "L.", "Piperaceae", "Piperales", "Frukt", "Fruit"),
    ("Linum", "usitatissimum", "L.", "Linaceae", "Malpighiales", "Stengel", "Stem fiber"),
]

_DEMO_COLLECTORS = [
    "N. Moe", "M. N. Blytt", "J. Lid", "O. Dahl", "R. Nordhagen",
    "F. C. Schübeler", "A. Blytt", "I. Jørstad",
]

_DEMO_PLACES = [
    "Oslo, Tøyen", "Bergen, Hordaland", "Trondheim, Sør-Trøndelag",
    "Tromsø, Troms", "Lillehammer, Oppland", "Kristiansand, Vest-Agder",
    "Java (Botanical Exchange)", "Ceylon (Historical Trade)",
]

_STORED_AS = [
    "in paper box",
    "in plastic box",
    "Mounted on wooded platform",
    "Petridish",
    "in plastic bag",
    "Free standing",
]


def _build_synthetic_demo_frames(count: int = 220):
    """Build a deterministic, realistic 220-specimen Økonomisk Botanisk dataset."""
    reg_rows = []
    obs_rows = []
    unval_rows = []

    for i in range(1, count + 1):
        oid = str(i)
        genus, species, author, family, higher, n_part, part = _DEMO_TAXA[(i - 1) % len(_DEMO_TAXA)]
        collector = _DEMO_COLLECTORS[(i - 1) % len(_DEMO_COLLECTORS)]
        place = _DEMO_PLACES[(i - 1) % len(_DEMO_PLACES)]
        year = str(1885 + (i % 120))
        stored = _STORED_AS[(i - 1) % len(_STORED_AS)]

        # Leave every 10th specimen unplaced for Armed Target Shelf hallway testing
        if i % 10 == 0:
            building, floor, cabinet, shelf = "", "", "", ""
        else:
            building = "Lid's hus" if i % 3 != 0 else "Økern"
            floor = ["-1", "-2", "1", "2"][i % 4]
            cabinet = f"{((i - 1) % 24) + 1:02d}"
            shelf = f"{((i - 1) % 6) + 1:02d}"

        reg_rows.append({
            "ObjectID": oid,
            "Variant": "",
            "Genus": genus,
            "Species": species,
            "Author": author,
            "Family": family,
            "Higher Classification": higher,
            "(N) Plant Part": n_part,
            "Plant Part": part,
            "Collector": collector,
            "Innsammling Nr.": f"OB-{i:04d}",
            "Collection Date": year,
            "Collection Place": place,
            "Box Label": f"{genus} {species} ({year})",
            "Observation": "",
            "Conservation Status": "Good" if i % 7 != 0 else "Fragile label",
            "Comment": "",
            "UID": f"O-V-OE-{i:04d}",
            "ProblemDescription": "Faded handwritten label" if i % 15 == 0 else "",
            "Online photo 1": "",
            "Online photo 2": "",
            "Online photo 3": "",
            "Stored as": stored,
            "Floor": floor,
            "Cabinet": cabinet,
            "Shelf": shelf,
            "Extra": "",
            "Building": building,
            "Loaned out": False,
            "Loaned out date": "",
        })

        reviewed = (i <= 45)
        box_prob = (i % 15 == 0)
        plant_prob = (i % 22 == 0)
        date_prob = (i % 19 == 0)
        genus_prob = (i % 35 == 0)

        obs_rows.append({
            "ObjectID": oid,
            "Reviewed": reviewed,
            "Genus_Problem": genus_prob,
            "Species_Problem": False,
            "Family_Problem": False,
            "Author_Problem": False,
            "PlantPart_Problem": plant_prob,
            "Collector_Problem": False,
            "Collection_Date_Problem": date_prob,
            "Collection_Place_Problem": False,
            "Box_Label_Problem": box_prob,
            "Images_Problem": False,
            "Other_problem": False,
            "Unknown_Collector": False,
            "Unknown_Collection_Date": False,
            "Unknown_Collection_Place": False,
        })

        if i % 25 == 0:
            unval_rows.append({
                "ObjectID": oid,
                "Field_Name": "Collection Date",
                "Unvalidated_Comment": f"Historical ledger reads {int(year) - 2}",
            })

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    df_log = pd.DataFrame([
        {
            "Timestamp": now_iso,
            "User": "Arbor Demo",
            "ObjectID": "ALL",
            "Action": "DEMO_INIT",
            "Details": f"Initialized {count}-specimen offline demo collection",
        }
    ])

    return (
        pd.DataFrame(reg_rows),
        pd.DataFrame(obs_rows),
        df_log,
        pd.DataFrame(unval_rows, columns=["ObjectID", "Field_Name", "Unvalidated_Comment"]),
    )


def create_demo_subset(dest_path: str = None):
    src_path = "excel_temporary_example/24.10.OBCJDF.xlsx"
    if dest_path is None:
        dest_dir = "data"
        dest_path = os.path.join(dest_dir, "demo_collection.xlsx")
    else:
        dest_dir = os.path.dirname(os.path.abspath(dest_path))
    os.makedirs(dest_dir, exist_ok=True)

    if os.path.exists(src_path):
        print(f"Reading source: {src_path}")
        xls = pd.ExcelFile(src_path)

        # 1. Registration
        df_reg = pd.read_excel(xls, sheet_name="Registration")
        # Take first 220 specimens (~11%)
        df_reg_sub = df_reg.iloc[:220].copy()
        valid_oids = set(df_reg_sub["ObjectID"].astype(str))
        print(f"Registration rows: {len(df_reg_sub)}, Unique ObjectIDs: {len(valid_oids)}")

        # 2. Observation
        df_obs = pd.read_excel(xls, sheet_name="Observation")
        df_obs_sub = df_obs[df_obs["ObjectID"].astype(str).isin(valid_oids)].copy()
        print(f"Observation rows: {len(df_obs_sub)}")

        # 3. Log
        df_log = pd.read_excel(xls, sheet_name="Log")
        # Keep logs that match valid_oids or are initial setup/ALL
        df_log_sub = df_log[df_log["ObjectID"].astype(str).isin(valid_oids) | (df_log["ObjectID"].astype(str) == "ALL")].copy()
        print(f"Log rows: {len(df_log_sub)}")

        # 4. Unvalidated_source
        if "Unvalidated_source" in xls.sheet_names:
            df_unval = pd.read_excel(xls, sheet_name="Unvalidated_source")
            df_unval_sub = df_unval[df_unval["ObjectID"].astype(str).isin(valid_oids)].copy()
            print(f"Unvalidated_source rows: {len(df_unval_sub)}")
        else:
            df_unval_sub = pd.DataFrame(columns=["ObjectID", "Field_Name", "Unvalidated_Comment"])
    else:
        print(f"Source workbook not found ({src_path}); generating synthetic 220-specimen demo dataset...")
        df_reg_sub, df_obs_sub, df_log_sub, df_unval_sub = _build_synthetic_demo_frames(220)

    print(f"Writing demo collection to: {dest_path}")
    with pd.ExcelWriter(dest_path, engine="openpyxl") as writer:
        df_reg_sub.to_excel(writer, sheet_name="Registration", index=False)
        df_obs_sub.to_excel(writer, sheet_name="Observation", index=False)
        df_log_sub.to_excel(writer, sheet_name="Log", index=False)
        df_unval_sub.to_excel(writer, sheet_name="Unvalidated_source", index=False)

    print(f"Success! File size: {os.path.getsize(dest_path)} bytes")
    return dest_path


if __name__ == "__main__":
    create_demo_subset()
