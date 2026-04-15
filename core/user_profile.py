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
