# radar/nlp.py
import json
from pathlib import Path

ALERTS_FILE = Path("data/processed/alerts.json")

def load_alerts():
    with open(ALERTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def find_alerts_by_event(alerts, event_query):
    """Return alerts matching the event name or type."""
    event_query_lower = event_query.lower()
    return [a for a in alerts if event_query_lower in (a["event"] or "").lower()]

def find_alerts_by_city(alerts, city_query):
    """Return alerts for a specific city."""
    city_query_lower = city_query.lower()
    return [a for a in alerts if city_query_lower == a["city"].lower()]

def answer_question(question):
    """Very basic Q&A logic — keyword + city detection."""
    alerts = load_alerts()

    # Try to detect a city from the question
    cities = {a["city"] for a in alerts}
    mentioned_cities = [c for c in cities if c.lower() in question.lower()]

    # Try to detect event keyword
    keywords = [
    "thunderstorm", "extreme heat", "severe weather", "flood", "tornado",
    "hail", "wind advisory", "heat advisory", "winter storm", "hurricane"]
    mentioned_events = [k for k in keywords if k in question.lower()]

    results = alerts
    if mentioned_cities:
        results = [a for a in results if a["city"] in mentioned_cities]
    if mentioned_events:
        filtered = []
        for ev in mentioned_events:
            filtered.extend(find_alerts_by_event(results, ev))
        results = filtered

    if not results:
        return "No matching alerts found."

    # Build answer
    answer_parts = []
    for alert in results:
        answer_parts.append(
            f"{alert['event']} in {alert['city']} — Severity: {alert['severity']}"
        )

    return "\n".join(answer_parts)
