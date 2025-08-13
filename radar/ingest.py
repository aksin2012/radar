import json
from pathlib import Path
from radar.sources.nws import fetch_alerts_for_city

OUTPUT_FILE = Path("data/processed/alerts.json")

# Major NC cities to check
CITIES = {
    "Charlotte": (35.2271, -80.8431),
    "Raleigh": (35.7796, -78.6382),
    "Greensboro": (36.0726, -79.7920),
    "Durham": (35.9940, -78.8986),
    "Wilmington": (34.2257, -77.9447),
}

def save_alerts(alerts):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)
    print(f"[INFO] Saved {len(alerts)} alerts to {OUTPUT_FILE}")

def main():
    all_alerts = []
    for city, (lat, lon) in CITIES.items():
        city_alerts = fetch_alerts_for_city(city, lat, lon)
        all_alerts.extend(city_alerts)

    save_alerts(all_alerts)

if __name__ == "__main__":
    main()