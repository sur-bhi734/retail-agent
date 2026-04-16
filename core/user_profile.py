import pandas as pd
import streamlit as st

@st.cache_data
def load_users():
    return pd.read_csv("data/users.csv")

AREAS   = ["Koramangala", "Indiranagar", "Whitefield", "Jayanagar", "HSR Layout"]
STYLES  = ["Casual", "Ethnic", "Streetwear", "Formal"]
BRANDS  = ["Roadster", "HRX", "W", "Biba", "Puma", "Campus", "Van Heusen"]
SIZES   = ["XS", "S", "M", "L", "XL"]
BUDGETS = ["Low", "Mid", "High"]
COLORS  = ["Black", "White", "Navy", "Olive", "Maroon", "Beige", "Mustard", "Pastel", "Blue"]
OCCASIONS = ["College", "Festive", "Casual Outing", "Work", "Party"]


def build_profile_from_inputs(raw_inputs: dict) -> dict:
    """
    Constructs a complete shopper profile from questionnaire inputs.
    Infers social_influence from age + occasion, and purchase_frequency
    from budget tier — so even custom users get a fully populated profile
    rather than hardcoded defaults.
    """
    age = raw_inputs.get("age", 21)
    occasion = raw_inputs.get("occasion", "College")
    budget = raw_inputs.get("budget", "Mid")

    # Infer social_influence: younger shoppers in social occasions tend to be highly influenced
    if age <= 22 and occasion in ("College", "Party", "Festive"):
        social_influence = "High"
    elif age <= 28:
        social_influence = "Medium"
    else:
        social_influence = "Low"

    # Infer purchase_frequency: higher budget → more frequent shopping
    frequency_map = {"Low": "Rarely", "Mid": "Monthly", "High": "Weekly"}
    purchase_frequency = frequency_map.get(budget, "Monthly")

    profile = {
        "user_id":            raw_inputs.get("user_id", "CUSTOM"),
        "name":               raw_inputs.get("name", "Shopper"),
        "age":                age,
        "gender":             raw_inputs.get("gender", "Other"),
        "area":               raw_inputs.get("area", AREAS[0]),
        "school":             raw_inputs.get("school", f"{raw_inputs.get('area', AREAS[0])} College"),
        "budget":             budget,
        "style_pref":         raw_inputs.get("style_pref", STYLES[0]),
        "size":               raw_inputs.get("size", "M"),
        "color_pref":         raw_inputs.get("color_pref", COLORS[0]),
        "occasion":           occasion,
        "preferred_brands":   raw_inputs.get("preferred_brands", BRANDS[0]),
        "social_influence":   social_influence,
        "purchase_frequency": purchase_frequency,
    }
    return profile