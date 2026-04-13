"""
scorer.py — Multi-factor product scoring engine.

Each product is scored on 5 dimensions:
  +3  style matches shopper preference
  +2  budget tier matches shopper budget
  +2  color matches shopper color preference
  +2  product category is relevant to an upcoming event
  +1  a peer has purchased a product in the same category
  +1  product is trending in the shopper's area
  -5  shopper already owns this product (heavy penalty)

Returns products sorted by score descending.
"""

import pandas as pd


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
    """
    Score and rank a list of product dicts.
    Returns the same dicts with an added '_score' key, sorted descending.
    """
    trending_names = {t.get("product_name", "").lower() for t in trends}

    for p in products:
        score = 0

        # 1. Style match
        if p.get("style", "").lower() == profile.get("style_pref", "").lower():
            score += 3

        # 2. Budget tier match
        user_budget = profile.get("budget", "")
        low, high   = BUDGET_RANGES.get(user_budget, (0, 99999))
        if low <= p.get("price", 0) <= high:
            score += 2

        # 3. Color preference match
        user_color = profile.get("color_pref", "").lower()
        if user_color and p.get("color", "").lower() == user_color:
            score += 2

        # 4. Event relevance
        if p.get("category", "") in event_categories:
            score += 2

        # 5. Peer category match
        if p.get("category", "") in peer_categories:
            score += 1

        # 6. Area trending
        if p.get("name", "").lower() in trending_names:
            score += 1

        # 7. Already owned penalty
        if p.get("name", "") in already_bought:
            score -= 5

        p["_score"] = score

    return sorted(products, key=lambda x: x["_score"], reverse=True)


def get_top_recommendations(scored: list[dict], n: int = 5) -> list[dict]:
    """Return top-n products, stripping the internal _score key for display."""
    top = scored[:n]
    return [{k: v for k, v in p.items() if k != "_score"} for p in top]


def get_comparisons(scored: list[dict], anchor: dict) -> list[dict]:
    """
    Given an anchor product (the top recommendation), find 2 alternatives:
      - Same category
      - Different brand
      - Price within ±40% of anchor price
    Returns up to 2 alternatives with style/price/brand metadata.
    """
    anchor_price    = anchor.get("price", 0)
    anchor_brand    = anchor.get("brand", "")
    anchor_category = anchor.get("category", "")

    alternatives = [
        p for p in scored
        if p.get("category") == anchor_category
        and p.get("brand") != anchor_brand
        and abs(p.get("price", 0) - anchor_price) <= anchor_price * 0.4
        and p.get("name") != anchor.get("name")
    ]
    return alternatives[:2]


def get_next_purchase_hints(already_bought_categories: list[str]) -> list[str]:
    """
    Simple category-transition rules derived from typical fashion purchase sequences.
    Returns 2 suggested next categories.
    """
    NEXT_CATEGORY = {
        "Tops":       ["Bottoms", "Footwear"],
        "Bottoms":    ["Tops", "Footwear"],
        "Footwear":   ["Accessories", "Tops"],
        "Ethnic Wear":["Accessories", "Footwear"],
        "Accessories":["Tops", "Bottoms"],
    }
    # Use the most recently purchased category as the anchor
    if not already_bought_categories:
        return ["Tops", "Bottoms"]

    last_cat = already_bought_categories[-1]
    return NEXT_CATEGORY.get(last_cat, ["Tops", "Accessories"])