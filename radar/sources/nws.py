import requests
from typing import List, Tuple
from loguru import logger
from datetime import datetime
from ..schemas import Alert

# Charlotte: Mecklenburg County, NC
MECKLENBURG_COUNTY = "Mecklenburg"
STATE = "NC"

API = "https://api.weather.gov/alerts"  # CAP v1 JSON
HEADERS = {
    "User-Agent": "Radar/0.1 (contact: you@example.com)",
    "Accept": "application/geo+json",
}


def _centroid_from_geometry(geometry) -> Tuple[float, float] | tuple[None, None]:
    try:
        if not geometry:
            return (None, None)
        # geometry can be Polygon or MultiPolygon
        coords = []
        if geometry.get("type") == "Polygon":
            coords = geometry.get("coordinates", [[]])[0]
        elif geometry.get("type") == "MultiPolygon":
            # flatten first ring of first polygon
            coords = geometry.get("coordinates", [[[]]])[0][0]
        if not coords:
            return (None, None)
        lats = [pt[1] for pt in coords]
        lons = [pt[0] for pt in coords]
        return (sum(lats) / len(lats), sum(lons) / len(lons))
    except Exception:
        return (None, None)


def _iso(dt: str | None):
    if not dt:
        return None
    try:
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))
    except Exception:
        return None


def fetch_alerts_nc(limit: int = 50) -> List[Alert]:
    """
    Fetch current NWS alerts for North Carolina.
    We’ll filter to anything mentioning Mecklenburg/Charlotte downstream.
    """
    params = {
        "area": STATE,  # state postal code filter
        "status": "actual",
        "limit": limit,
    }
    logger.info("Fetching NWS alerts for NC …")
    r = requests.get(API, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

    alerts: List[Alert] = []
    for feat in data.get("features", []):
        props = feat.get("properties", {}) or {}
        geom = feat.get("geometry")

        counties = []
        area = props.get("areaDesc") or ""
        if area:
            # example: "Mecklenburg; Cabarrus; York"
            counties = [c.strip() for c in area.split(";") if c.strip()]

        lat, lon = _centroid_from_geometry(geom)

        alert = Alert(
            id=str(props.get("id") or props.get("identifier") or feat.get("id")),
            source="nws",
            event_type=props.get("event") or "",
            severity=props.get("severity"),
            headline=props.get("headline"),
            description=props.get("description"),
            instruction=props.get("instruction"),
            onset=_iso(props.get("onset")),
            expires=_iso(props.get("expires")),
            sent=_iso(props.get("sent")),
            updated=_iso(props.get("updated")),
            area=area,
            counties=counties,
            latitude=lat,
            longitude=lon,
            raw_url=props.get("uri") or props.get("@id"),
        )
        alerts.append(alert)
    return alerts


def filter_charlotte(alerts: List[Alert]) -> List[Alert]:
    """
    Keep alerts relevant to Charlotte / Mecklenburg County (and nearby common references).
    """
    KEYWORDS = {"charlotte", "mecklenburg", "uptown", "university city"}
    out = []
    for a in alerts:
        text = " ".join(
            [
                a.event_type or "",
                a.headline or "",
                a.description or "",
                a.area or "",
                " ".join(a.counties or []),
            ]
        ).lower()
        if any(k in text for k in KEYWORDS):
            out.append(a)
        elif any(c.lower().startswith("mecklenburg") for c in a.counties):
            out.append(a)
    return out
