import json


def get_upcoming_events(within_days: int = 30) -> list:
    """
    Returns events within the window, sorted by proximity.
    Each event: {name, days_away, relevant_categories}
    """
    with open("data/events_calendar.json") as f:
        events = json.load(f)

    upcoming = [e for e in events if e["days_away"] <= within_days]

    if not upcoming:
        return []

    return sorted(upcoming, key=lambda x: x["days_away"])


def get_event_categories(events: list) -> list:
    """Flatten all relevant_categories from a list of events (deduped)."""
    seen = set()
    result = []
    for e in events:
        for cat in e.get("relevant_categories", []):
            if cat not in seen:
                seen.add(cat)
                result.append(cat)
    return result