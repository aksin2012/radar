# radar/visuals.py
import folium

SEVERITY_COLORS = {
    "Extreme": "darkred",
    "Severe": "red",
    "Moderate": "orange",
    "Minor": "yellow",
    "Unknown": "gray",
}

# Fallback location if no coordinates are in the alert
FALLBACK_LAT = 35.2271
FALLBACK_LON = -80.8431

def severity_color(severity):
    return SEVERITY_COLORS.get(severity, "gray")

def alerts_map(alerts):
    """Generate a folium map of alerts with polygons or fallback markers."""
    m = folium.Map(location=[FALLBACK_LAT, FALLBACK_LON], zoom_start=8)

    for alert in alerts:
        severity = alert.get("severity", "Unknown")
        color = severity_color(severity)
        title = alert.get("event", "Unknown Event")
        desc = alert.get("description", "No description")

        if alert.get("coordinates"):
            # Draw polygon
            folium.Polygon(
                locations=alert["coordinates"],
                color=color,
                fill=True,
                fill_opacity=0.4,
                popup=f"{title} — {severity}",
            ).add_to(m)
        else:
            # Drop a fallback marker
            folium.Marker(
                location=[FALLBACK_LAT, FALLBACK_LON],
                popup=f"{title} — {severity}",
                icon=folium.Icon(color="red"),
            ).add_to(m)

    return m
