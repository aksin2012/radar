import json
from pathlib import Path
from typing import List
from loguru import logger
from .paths import DATA_PROCESSED
from .schemas import Alert
from .sources.nws import fetch_alerts_nc, filter_charlotte

OUTPUT = DATA_PROCESSED / "alerts.json"


def run_ingest() -> List[Alert]:
    alerts_nc = fetch_alerts_nc(limit=100)
    alerts_clt = filter_charlotte(alerts_nc)
    logger.info(f"NC alerts: {len(alerts_nc)} | Charlotte-filtered: {len(alerts_clt)}")

    # Save as list of dicts
    payload = [a.model_dump(mode="json") for a in alerts_clt]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    logger.info(f"Wrote {len(payload)} alerts -> {OUTPUT}")
    return alerts_clt


if __name__ == "__main__":
    run_ingest()
