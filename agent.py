import time


from core.llm import build_prompt, call_llm
from tools.trends import get_local_trends
from tools.social import get_peer_purchases
from tools.events import get_event_categories, get_relevant_events
from tools.catalog import (
    search_products,
    search_products_for_events,
    get_already_purchased,
)
from tools.scorer import (
    score_products,
    get_top_recommendations,
    get_comparisons,
    get_next_purchase_hints,
)


def run_agent(profile: dict) -> dict:
    start = time.time()

   
    trends = get_local_trends(profile["area"], school=profile.get("school"))
    peer_data = get_peer_purchases(profile["user_id"], profile=profile)
    events = get_relevant_events(profile, within_days=20, top_n=3)
    print(f"[DEBUG] Selected events for {profile['name']}: {[e['name'] for e in events]}")
    event_cats = get_event_categories(events)
    already_bought, bought_categories = get_already_purchased(profile["user_id"])

   
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

    
    seen_ids = {p["product_id"] for p in base_products}
    combined = base_products + [
        p for p in event_products if p["product_id"] not in seen_ids
    ]

    
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
    
    
    import json
    
    profile_summary = json.dumps({
        "Style": profile.get("style_pref", ""),
        "Budget": profile.get("budget", ""),
        "Color": profile.get("color_pref", ""),
        "Brand": profile.get("preferred_brands", "")
    })

    peer_products = ", ".join(peer_data.get("peer_products", [])[:3])
    peer_styles = ", ".join([f"{s['style']}" for s in peer_data.get("peer_styles", [])])
    local_peer_insights = f"Your peers are buying {peer_products if peer_products else 'similar items'}. Top styles in your network: {peer_styles if peer_styles else 'Diverse'}."

    top_names = [p.get('name', 'Item') for p in top_recommendations]
    recommended_products = f"We highly recommend looking into: {', '.join(top_names)}."

    next_purchase_plan = f"Based on your profile, you might want to look into {', '.join(next_hints)} next to complete your wardrobe."

    if comparisons:
        comparative_suggestions = f"Alternatively consider {comparisons[0].get('name')} ({comparisons[0].get('brand')}) as a strong comparison."
    else:
        comparative_suggestions = "No direct comparisons available."

    disclaimer = "AI-generated recommendations. Prices may vary."

   
    prompt = build_prompt(profile, events, top_recommendations)
    personalized_reasoning = call_llm(prompt)

    
    result = {
        "profile_summary": profile_summary,
        "local_peer_insights": local_peer_insights,
        "recommended_products": recommended_products,
        "personalized_reasoning": personalized_reasoning,
        "next_purchase_plan": next_purchase_plan,
        "comparative_suggestions": comparative_suggestions,
        "disclaimer": disclaimer,
    }

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