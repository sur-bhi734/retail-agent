import json
import time
import ollama

# ✅ FIXED IMPORTS
from tools.trends import get_local_trends
from tools.social import get_peer_purchases
from tools.events import get_upcoming_events, get_event_categories, get_relevant_events
from tools.catalog import (
    search_products,
    search_products_for_events,
    get_already_purchased,
    get_all_products_as_pool,
)
from tools.scorer import (
    score_products,
    get_top_recommendations,
    get_comparisons,
    get_next_purchase_hints,
)

with open("prompts/system_prompt.txt") as f:
    SYSTEM_PROMPT = f.read()


def run_agent(profile: dict) -> dict:
    start = time.time()

    # ── 1. Gather all context ──────────────────────────────────────────────
    trends = get_local_trends(profile["area"], school=profile.get("school"))
    peer_data = get_peer_purchases(profile["user_id"])
    events = get_relevant_events(profile, within_days=20, top_n=3)
    print(f"[DEBUG] Selected events for {profile['name']}: {[e['name'] for e in events]}")
    event_cats = get_event_categories(events)
    already_bought, bought_categories = get_already_purchased(profile["user_id"])

    # ── 2. Build scoring pool ──────────────────────────────────────────────
    base_products = search_products(
        style=profile["style_pref"],
        budget=profile["budget"],
        size=profile.get("size"),
        top_n=30,
    )

    event_products = search_products_for_events(
        events=events,
        budget=profile["budget"],
        size=profile.get("size"),
    )

    # Merge & deduplicate
    seen_ids = {p["product_id"] for p in base_products}
    combined = base_products + [
        p for p in event_products if p["product_id"] not in seen_ids
    ]

    # ── 3. Multi-factor scoring ────────────────────────────────────────────
    scored = score_products(
        products=combined,
        profile=profile,
        trends=trends["area_trends"],
        peer_categories=peer_data.get("peer_categories", []),
        event_categories=event_cats,
        already_bought=already_bought,
    )

    top_recommendations = get_top_recommendations(scored, n=5)
    comparisons = get_comparisons(scored, scored[0]) if scored else []
    next_hints = get_next_purchase_hints(bought_categories)

    # ── 4. Build prompt ────────────────────────────────────────────────────
    prompt = build_prompt(
        profile=profile,
        trends=trends,
        peer_data=peer_data,
        events=events,
        top_products=top_recommendations,
        comparisons=comparisons,
        already_bought=already_bought,
        next_hints=next_hints,
    )

    # ── 5. LLM call ────────────────────────────────────────────────────────
    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    raw = response["message"]["content"]
    result = parse_response(raw)

    # ── 6. Attach structured data ──────────────────────────────────────────
    result["_structured"] = {
        "top_products": top_recommendations,
        "comparisons": comparisons,
        "trends": trends,
        "peer_data": peer_data,
        "events": events,
        "next_hints": next_hints,
        "profile_score": scored[0]["_score"] if scored else 0,
    }

    result["response_time"] = round(time.time() - start, 1)
    return result


# ── Prompt Builder ─────────────────────────────────────────────────────────

def build_prompt(profile, trends, peer_data, events, top_products, comparisons,
                 already_bought, next_hints) -> str:

    peer_products_str = (
        ", ".join(peer_data.get("peer_products", [])) or "No peer product data"
    )

    peer_styles_str = (
        "; ".join(
            f"{s['style']} ({s['friends']} friends)"
            for s in peer_data.get("peer_styles", [])
        ) or "No peer style data"
    )

    events_str = (
        "; ".join(f"{e['name']} in {e['days_away']} days" for e in events)
        or "No upcoming events"
    )

    trend_items_str = (
        ", ".join(
            f"{t['product_name']} ({t['color']}, {t['units_sold']} sold)"
            for t in trends["area_trends"][:3]
        ) or "No local trend data"
    )

    top_products_str = json.dumps(top_products, indent=2)
    comparisons_str = json.dumps(comparisons, indent=2)
    already_str = ", ".join(already_bought[:5]) if already_bought else "None"

    return f"""
SHOPPER PROFILE
---------------
Name: {profile['name']}
Age: {profile['age']} | Gender: {profile['gender']}
Area: {profile['area']} | School: {profile.get('school', 'N/A')}
Budget: {profile['budget']}
Style preference: {profile['style_pref']}
Color preference: {profile.get('color_pref', 'Not specified')}
Preferred occasion: {profile.get('occasion', 'Not specified')}
Size: {profile.get('size', 'Not specified')}
Preferred brand: {profile['preferred_brands']}
Social influence: {profile['social_influence']} | Shops: {profile['purchase_frequency']}

CONTEXT DATA
------------
Local trending items: {trend_items_str}
Trending colors: {", ".join(trends.get('top_colors', []))}

Peer network:
Products: {peer_products_str}
Styles: {peer_styles_str}

Upcoming events: {events_str}
Already owns: {already_str}

AVAILABLE PRODUCTS:
{top_products_str}

COMPARISONS:
{comparisons_str}

NEXT PURCHASE HINTS:
{", ".join(next_hints)}

Respond strictly in JSON as per instructions.
"""


# ── Response Parser ────────────────────────────────────────────────────────

EXPECTED_KEYS = [
    "profile_summary",
    "local_peer_insights",
    "recommended_products",
    "personalized_reasoning",
    "next_purchase_plan",
    "comparative_suggestions",
    "disclaimer",
]


def parse_response(raw: str) -> dict:
    cleaned = raw.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        return {k: data.get(k, "Not generated.") for k in EXPECTED_KEYS}
    except:
        pass

    # fallback
    import re
    parts = re.split(r'\n\s*\d+\.\s+', raw)
    parts = [p.strip() for p in parts if p.strip()]

    result = {}
    for i, key in enumerate(EXPECTED_KEYS):
        result[key] = parts[i] if i < len(parts) else "Not generated."

    return result


# ── Test Run ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_profile = {
        "user_id": "U001",
        "name": "Riya Sharma",
        "age": 21,
        "area": "Koramangala",
        "school": "Koramangala College",
        "budget": "Mid",
        "style_pref": "Casual",
        "gender": "Female",
        "social_influence": "High",
        "purchase_frequency": "Monthly",
        "preferred_brands": "HRX",
        "size": "S",
        "color_pref": "Navy",
        "occasion": "College",
    }

    output = run_agent(test_profile)

    for section, content in output.items():
        if section.startswith("_"):
            continue
        print(f"\n--- {section.upper()} ---")
        print(content)

    print("\n--- STRUCTURED DATA ---")
    import pprint
    pprint.pprint(output["_structured"])