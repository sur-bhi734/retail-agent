import json
import pandas as pd


def _load_connections() -> dict:
    with open("data/social_connections.json") as f:
        return json.load(f)


def get_peer_purchases(user_id: str, top_n: int = 5, profile: dict = None) -> dict:
    """
    Returns a dict with:
      - peer_products: top product names bought by friends
      - peer_categories: top categories bought by friends  (used by scorer)
      - peer_styles: style distribution among friends
      - friend_count: number of connected peers
    """
    friend_ids = []
    if user_id == "CUSTOM" and profile is not None:
        try:
            users_df = pd.read_csv("data/users.csv")
            
            style_pref = profile.get("style_pref")
            area = profile.get("area")
            similar_users = users_df[
                (users_df["area"] == area) | (users_df["style_pref"] == style_pref)
            ]
            friend_ids = similar_users["user_id"].head(5).tolist()
        except Exception:
            friend_ids = []
    else:
        connections  = _load_connections()
        friend_ids   = connections.get(user_id, [])

    if not friend_ids:
        return {
            "peer_products":   [],
            "peer_categories": [],
            "peer_styles":     [],
            "friend_count":    0,
            "note": "No peer connections found.",
        }

    
    try:
        history   = pd.read_csv("data/purchase_history.csv")
        peer_hist = history[history["user_id"].isin(friend_ids)]

        top_products   = peer_hist["product_name"].value_counts().head(top_n).index.tolist()
        top_categories = peer_hist["category"].value_counts().head(top_n).index.tolist()
    except Exception:
        top_products   = []
        top_categories = []

    
    try:
        users_df   = pd.read_csv("data/users.csv")
        friends_df = users_df[users_df["user_id"].isin(friend_ids)]
        peer_styles = friends_df["style_pref"].value_counts().head(3).to_dict()
        peer_styles = [{"style": k, "friends": int(v)} for k, v in peer_styles.items()]
    except Exception:
        peer_styles = []

    return {
        "peer_products":   top_products,
        "peer_categories": top_categories,
        "peer_styles":     peer_styles,
        "friend_count":    len(friend_ids),
    }