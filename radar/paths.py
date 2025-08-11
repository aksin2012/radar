from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
CONFIG_DIR = ROOT / "config"

for p in (DATA_RAW, DATA_PROCESSED):
    p.mkdir(parents=True, exist_ok=True)
