import sys, pathlib, os
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
