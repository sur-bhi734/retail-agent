import pandas as pd


def get_local_trends(area: str, school: str = None, top_n: int = 5) -> dict:
    """
    Returns:
      - area_trends:   top products/colors in the user's area (or school's areas)
      - top_categories: top trending categories in area (for scorer)
      - top_colors:    top trending colors in area (for UI display)
      - school_trends: top products/colors specific to the school's catchment areas
    Falls back to global trends if area has no data.
    """
    df = pd.read_csv("data/sales_trends.csv")

    # School-level trends: find all areas associated with users from this school,
    # then filter the sales trends to those areas.
    school_trends = []
    if school:
        try:
            users_df = pd.read_csv("data/users.csv")
            school_areas = users_df[
                users_df["school"].str.lower() == school.lower()
            ]["area"].unique().tolist()
            if school_areas:
                school_local = df[df["area"].isin(school_areas)]
                if not school_local.empty:
                    school_trends = (
                        school_local.groupby(["product_name", "color"])[["units_sold"]]
                        .sum()
                        .reset_index()
                        .sort_values("units_sold", ascending=False)
                        .head(top_n)
                        .to_dict(orient="records")
                    )
        except Exception:
            school_trends = []

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
        "school_trends":  school_trends,
    }