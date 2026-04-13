import pandas as pd

BUDGET_RANGES = {
    "Low":  (0, 499),
    "Mid":  (500, 1499),
    "High": (1500, 99999),
}


def _load_products() -> pd.DataFrame:
    return pd.read_csv("data/products.csv")


def search_products(
    style: str,
    budget: str,
    size: str = None,
    category: str = None,
    top_n: int = 20,
) -> list:
    """Return products matching style + budget, optionally filtered by size/category."""
    df = _load_products()
    low, high = BUDGET_RANGES.get(budget, (0, 99999))

    filtered = df[
        (df["style"].str.lower() == style.lower()) &
        (df["price"] >= low) &
        (df["price"] <= high)
    ]

    if size:
        size_match = filtered[filtered["size"] == size]
        if not size_match.empty:
            filtered = size_match

    if category:
        cat_match = filtered[filtered["category"].str.lower() == category.lower()]
        if not cat_match.empty:
            filtered = cat_match

    # Fallback: budget only
    if filtered.empty:
        filtered = df[(df["price"] >= low) & (df["price"] <= high)]

    return filtered.head(top_n).to_dict(orient="records")


def search_products_for_events(
    events: list,
    budget: str,
    size: str = None,
) -> list:
    """
    Return products whose category matches any upcoming event's relevant_categories.
    Used to inject event-aware products into the scoring pool.
    """
    df = _load_products()
    low, high = BUDGET_RANGES.get(budget, (0, 99999))

    event_categories = list({
        cat
        for e in events
        for cat in e.get("relevant_categories", [])
    })

    if not event_categories:
        return []

    filtered = df[
        df["category"].isin(event_categories) &
        df["price"].between(low, high)
    ]

    if size:
        size_match = filtered[filtered["size"] == size]
        if not size_match.empty:
            filtered = size_match

    return filtered.head(10).to_dict(orient="records")


def get_already_purchased(user_id: str) -> tuple[list, list]:
    """
    Returns (product_name_list, category_list) for a user's purchase history.
    Custom profile users get empty lists.
    """
    if user_id == "CUSTOM":
        return [], []

    try:
        df = pd.read_csv("data/purchase_history.csv")
        user_df = df[df["user_id"] == user_id].sort_values("date_purchased")
        return (
            user_df["product_name"].tolist(),
            user_df["category"].tolist(),
        )
    except Exception:
        return [], []


def get_all_products_as_pool(budget: str, size: str = None) -> list:
    """
    Return ALL products within budget (used as the full scoring pool).
    """
    df = _load_products()
    low, high = BUDGET_RANGES.get(budget, (0, 99999))
    filtered = df[df["price"].between(low, high)]

    if size:
        size_match = filtered[filtered["size"] == size]
        if not size_match.empty:
            filtered = size_match

    return filtered.to_dict(orient="records")