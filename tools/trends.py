import pandas as pd


def get_local_trends(area: str, school: str = None, top_n: int = 5) -> dict:
    """
    Returns:
      - area_trends:   top products/colors in the user's area
      - top_categories: top trending categories in area (for scorer)
      - top_colors:    top trending colors in area (for UI display)
    Falls back to global trends if area has no data.
    """
    df = pd.read_csv("data/sales_trends.csv")

    local = df[df["area"].str.lower() == area.lower()]

    if local.empty:
        local = df  

    
    product_trends = (
        local.groupby(["product_name", "color"])["units_sold"]
        .sum()
        .reset_index()
        .sort_values("units_sold", ascending=False)
        .head(top_n)
        .to_dict(orient="records")
    )

    
    cat_trends = (
        local.groupby("category")["units_sold"]
        .sum()
        .reset_index()
        .sort_values("units_sold", ascending=False)
        .head(3)
    )
    top_categories = cat_trends["category"].tolist()

    
    color_trends = (
        local.groupby("color")["units_sold"]
        .sum()
        .reset_index()
        .sort_values("units_sold", ascending=False)
        .head(3)
    )
    top_colors = color_trends["color"].tolist()

    return {
        "area_trends":    product_trends,
        "top_categories": top_categories,
        "top_colors":     top_colors,
    }