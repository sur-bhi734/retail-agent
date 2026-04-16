"""
scorer.py — Multi-factor product scoring engine.
"""

BUDGET_RANGES = {
    "Low":  (0, 499),
    "Mid":  (500, 1499),
    "High": (1500, 99999),
}

def score_products(
    products: list[dict],
    profile: dict,
    trends: list[dict],
    peer_categories: list[str],
    event_categories: list[str],
    already_bought: list[str],
) -> list[dict]:
    """Score and rank a list of product dicts."""
    trending_names = {t.get("product_name", "").lower() for t in trends}
    
    user_style = profile.get("style_pref", "").lower()
    user_color = profile.get("color_pref", "").lower()
    low_budget, high_budget = BUDGET_RANGES.get(profile.get("budget", ""), (0, 99999))
    
    for p in products:
        score = 0
        name = p.get("name", "")
        category = p.get("category", "")
        
        if p.get("style", "").lower() == user_style:
            score += 3
        if low_budget <= p.get("price", 0) <= high_budget:
            score += 2
        if user_color and p.get("color", "").lower() == user_color:
            score += 2
        if category in event_categories:
            score += 2
        if category in peer_categories:
            score += 1
        if name.lower() in trending_names:
            score += 1
        if name in already_bought:
            score -= 5
            
        p["_score"] = score

    return sorted(products, key=lambda x: x["_score"], reverse=True)


def get_top_recommendations(scored: list[dict], n: int = 5) -> list[dict]:
    """Return top-n products, stripping the internal _score key for display."""
    return [{k: v for k, v in p.items() if k != "_score"} for p in scored[:n]]


def get_comparisons(scored: list[dict], anchor: dict) -> list[dict]:
    """Return up to 2 alternative products based on category, brand, and price."""
    anchor_price = anchor.get("price", 0)
    anchor_brand = anchor.get("brand", "")
    anchor_category = anchor.get("category", "")
    anchor_name = anchor.get("name", "")

    alternatives = [
        p for p in scored
        if p.get("category") == anchor_category
        and p.get("brand") != anchor_brand
        and abs(p.get("price", 0) - anchor_price) <= anchor_price * 0.4
        and p.get("name") != anchor_name
    ]
    return alternatives[:2]


def get_next_purchase_hints(already_bought_categories: list[str]) -> list[str]:
    """
    Suggest next categories based on frequency gaps in purchase history.
    Finds which categories the user has bought least and surfaces those first,
    so the plan reflects actual gaps rather than a fixed lookup table.
    Falls back to sensible defaults when history is empty.
    """
    ALL_CATEGORIES = ["Tops", "Bottoms", "Footwear", "Ethnic Wear", "Accessories"]

    if not already_bought_categories:
        return ["Tops", "Bottoms"]

    # Count how many times the user has bought each category
    from collections import Counter
    bought_counts = Counter(already_bought_categories)

    # Score each category: categories never bought score 0, bought ones score their count
    # We want to surface the most under-represented categories
    category_scores = {cat: bought_counts.get(cat, 0) for cat in ALL_CATEGORIES}

    # Sort ascending — least purchased categories come first
    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1])

    # Return the 2 least-bought categories that the user hasn't already bought most recently
    last_bought = already_bought_categories[-1] if already_bought_categories else ""
    hints = [cat for cat, _ in sorted_cats if cat != last_bought][:2]

    # If filtering removed everything, fall back gracefully
    if not hints:
        hints = [cat for cat, _ in sorted_cats][:2]

    return hints