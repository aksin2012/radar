import sys, pathlib, os
import json

# ensure repo root is on path (so "import radar" works from anywhere)
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
from dotenv import load_dotenv
from radar.config import load_config
from radar.paths import DATA_RAW, DATA_PROCESSED
from radar.utils_logging import setup_logging

load_dotenv()
logger = setup_logging()
cfg = load_config()

st.set_page_config(page_title=cfg.app.name, page_icon="🛰️", layout="wide")
st.title(cfg.app.name)
st.caption("See the signals before the storm.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Region", cfg.app.region_name)
with col2:
    st.metric("Hazards", ", ".join(cfg.app.hazards))
with col3:
    st.metric("Refresh (min)", cfg.data.refresh_minutes)

st.divider()
st.subheader("Project Folders")
st.code(f"RAW: {DATA_RAW}\\nPROCESSED: {DATA_PROCESSED}")

api_key = os.getenv("OPENWEATHER_API_KEY", "")
st.info("OpenWeather API not set." if not api_key else "OpenWeather API key detected.")

# --- Alerts section ---
st.divider()
st.subheader("Latest Alerts (Charlotte Area)")

alerts_file = DATA_PROCESSED / "alerts.json"
if alerts_file.exists():
    with open(alerts_file, "r", encoding="utf-8") as f:
        alerts = json.load(f)
    if not alerts:
        st.info("No active Charlotte-area alerts found.")
    else:
        for a in alerts:
            with st.container(border=True):
                st.markdown(f"**{a.get('event_type','')}**  \n{a.get('headline','') or ''}")
                meta = []
                if a.get("severity"):
                    meta.append(f"Severity: {a['severity']}")
                if a.get("area"):
                    meta.append(f"Area: {a['area']}")
                if a.get("expires"):
                    meta.append(f"Expires: {a['expires']}")
                if meta:
                    st.caption(" • ".join(meta))
                if a.get("description"):
                    st.write(a["description"][:600] + ("…" if len(a["description"]) > 600 else ""))
                if a.get("raw_url"):
                    st.link_button("View full alert", a["raw_url"])
else:
    st.info("No alerts file yet. Run the ingest step below.")

# --- Ingest helper (manual) ---
st.divider()
st.subheader("Data • Manual Ingest")
st.caption("Run this in your terminal to fetch NWS alerts for Charlotte:")
st.code("python -m radar.ingest", language="bash")
