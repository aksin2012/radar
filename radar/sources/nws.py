import requests

NWS_BASE_URL = "https://api.weather.gov/alerts/active"

def fetch_alerts_for_city(city, lat, lon):
    """Fetch and return parsed alerts for a given city."""
    url = f"{NWS_BASE_URL}?point={lat},{lon}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    alerts = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        geom = feature.get("geometry")
        coords = None
        if geom and geom.get("type") == "Polygon":
            coords = [(lat, lon) for lon, lat in geom["coordinates"][0]]

        alerts.append({
            "city": city,
            "event": props.get("event"),
            "severity": props.get("severity", "Unknown"),
            "areaDesc": props.get("areaDesc", ""),
            "description": props.get("description", ""),
            "coordinates": coords
        })

    return alerts
