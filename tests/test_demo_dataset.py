import os
import pytest
from repository import ExcelRepository
import config

def test_demo_collection_exists_and_loads():
    demo_path = os.path.join("data", "demo_collection.xlsx")
    assert os.path.exists(demo_path), "demo_collection.xlsx should exist in data/"

    cfg = config.DATABASE_CONFIGS.get("Økonomisk Botanisk")
    assert cfg is not None, "Økonomisk Botanisk config should exist"

    df_reg, df_obs, df_photo, df_log, df_unval = ExcelRepository.load_excel(demo_path, cfg)

    assert len(df_reg) == 220, f"Expected 220 specimens, got {len(df_reg)}"
    assert len(df_obs) == 220, f"Expected 220 observation rows, got {len(df_obs)}"
    assert "ObjectID" in df_reg.columns
    assert "ObjectID" in df_obs.columns
    assert "PlantPart_Problem" in df_obs.columns
    assert len(df_log) > 0, "Log rows should be preserved"
    # Check that ObjectIDs match
    assert set(df_reg["ObjectID"]) == set(df_obs["ObjectID"]), "ObjectIDs must match across Registration and Observation"


def test_frozen_demo_path_prefers_writable_exe_dir(tmp_path, monkeypatch):
    import sys
    from ui.dialogs import StartupDialog

    meipass_dir = tmp_path / "meipass"
    exe_dir = tmp_path / "dist_install"
    (meipass_dir / "data").mkdir(parents=True)
    exe_dir.mkdir(parents=True)

    bundled_demo = meipass_dir / "data" / "demo_collection.xlsx"
    bundled_demo.write_bytes(b"mock-demo-xlsx")

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(meipass_dir), raising=False)
    monkeypatch.setattr(sys, "executable", str(exe_dir / "Arbor.exe"))

    dlg = StartupDialog.__new__(StartupDialog)
    resolved = dlg._resolve_writable_demo_path()

    expected = str(exe_dir / "data" / "demo_collection.xlsx")
    assert resolved == expected
    assert os.path.exists(expected)
    assert open(expected, "rb").read() == b"mock-demo-xlsx"
