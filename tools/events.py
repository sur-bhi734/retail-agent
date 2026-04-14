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


def get_relevant_events(profile: dict, within_days: int = 20, top_n: int = 3) -> list:
    """
    Returns top relevant events within the window based on user profile preferences.
    """
    with open("data/events_calendar.json") as f:
        events = json.load(f)

    # Filter by time window
    upcoming = [e for e in events if e["days_away"] <= within_days]

    if not upcoming:
        return []

    # Build user preferences set for matching
    user_prefs = {
        profile.get("style_pref", ""),
        profile.get("occasion", "")
    }
    
    for e in upcoming:
        cats = set(e.get("relevant_categories", []))
        e["_relevance"] = len(cats.intersection(user_prefs))
        
    # Sort by relevance (descending) and proximity (ascending)
    upcoming.sort(key=lambda x: (-x.get("_relevance", 0), x["days_away"]))
    
    return upcoming[:top_n]


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