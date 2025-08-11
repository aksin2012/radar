# Radar
AI-powered local hazard intelligence — real-time, location-aware, and signal-driven.

**Region (default):** Charlotte, NC, USA

## Vision
Aggregate official signals (gov feeds, weather) and answer localized safety questions fast.

## Status
Day 1: repo + env + hello-world Streamlit.

## Quickstart
```bash
python -m venv .venv
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/ui_app.py
```

## Config
- Edit `config/defaults.yaml` for region/hazards.
- Copy `.env.example` to `.env` and add `OPENWEATHER_API_KEY` (optional).

## Project Structure
```
radar/
  app/
    ui_app.py
  radar/
    config.py
    paths.py
    utils_logging.py
  data/
    raw/
    processed/
  config/
    defaults.yaml
  .env.example
  .gitignore
  README.md
  requirements.txt
  requirements-nlp.txt
  pyproject.toml
  .pre-commit-config.yaml
  LICENSE
```

## Notes
- No paid services required. OpenWeather API is optional (free tier) for weather signals.
- Next steps (Day 2+): Add data sources (FEMA/USGS/OpenWeather), normalize schema, and build Q&A.