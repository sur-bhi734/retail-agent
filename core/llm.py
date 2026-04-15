import json
import ollama

with open("prompts/system_prompt.txt") as f:
    SYSTEM_PROMPT = f.read()

EXPECTED_KEYS = [
    "profile_summary",
    "local_peer_insights",
    "recommended_products",
    "personalized_reasoning",
    "next_purchase_plan",
    "comparative_suggestions",
    "disclaimer",
]

def build_prompt(profile, trends, peer_data, events, top_products, comparisons, already_bought, next_hints) -> str:
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
            for t in trends.get("area_trends", [])[:3]
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

    
    import re
    parts = re.split(r'\n\s*\d+\.\s+', raw)
    parts = [p.strip() for p in parts if p.strip()]

    result = {}
    for i, key in enumerate(EXPECTED_KEYS):
        result[key] = parts[i] if i < len(parts) else "Not generated."

    return result

def call_llm(prompt: str) -> dict:
    """Calls Ollama with System Prompt, then formats response"""
    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    raw = response["message"]["content"]
    return parse_response(raw)
