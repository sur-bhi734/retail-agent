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
    """Suggest 2 next categories based on past purchases."""
    NEXT_CATEGORY_MAP = {
        "Tops":       ["Bottoms", "Footwear"],
        "Bottoms":    ["Tops", "Footwear"],
        "Footwear":   ["Accessories", "Tops"],
        "Ethnic Wear":["Accessories", "Footwear"],
        "Accessories":["Tops", "Bottoms"],
    }
    
    if not already_bought_categories:
        return ["Tops", "Bottoms"]

    last_cat = already_bought_categories[-1]
    return NEXT_CATEGORY_MAP.get(last_cat, ["Tops", "Accessories"])