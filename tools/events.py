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

    
    upcoming = [e for e in events if e["days_away"] <= within_days]

    if not upcoming:
        return []

    
    user_prefs_str = " ".join([
        str(profile.get("style_pref", "")),
        str(profile.get("occasion", "")),
        str(profile.get("preferred_brands", "")),
        str(profile.get("color_pref", ""))
    ]).lower()
    
    for e in upcoming:
        
        e["_relevance"] = sum(
            1 for cat in e.get("relevant_categories", [])
            if cat.lower() in user_prefs_str or user_prefs_str.find(cat.lower().split()[0]) != -1
        )
        

    user_hash = hash(profile.get("user_id", "default")) % 100
    upcoming.sort(key=lambda x: (-x.get("_relevance", 0), x["days_away"] + (user_hash % (x["days_away"] + 1))))
    
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