import streamlit as st
from core.user_profile import AREAS, STYLES, BRANDS, SIZES, BUDGETS, COLORS, OCCASIONS

def render_sidebar(users_df):
    with st.sidebar:
        st.markdown("### PROFILE")
        mode = st.radio("Mode", ["Select existing shopper", "Enter my own profile"], horizontal=False)
        st.divider()

        if mode == "Select existing shopper":
            selected_name = st.selectbox("Select shopper", users_df["name"].tolist())
            row = users_df[users_df["name"] == selected_name].iloc[0]
            profile = row.to_dict()

            
            st.markdown(f"**Name:** {profile['name']}")
            cols = st.columns(2)
            cols[0].markdown(f"**Age:** {profile['age']}")
            cols[1].markdown(f"**Gender:** {profile['gender']}")
            st.markdown(f"**Area:** {profile['area']}")
            st.markdown(f"**School:** {profile['school']}")

            st.markdown("---")
            cols2 = st.columns(2)
            cols2[0].markdown(f"**Budget:** {profile['budget']}")
            cols2[1].markdown(f"**Size:** {profile['size']}")
            st.markdown(f"**Style:** {profile['style_pref']}")
            st.markdown(f"**Color pref:** {profile.get('color_pref', 'N/A')}")
            st.markdown(f"**Occasion:** {profile.get('occasion', 'N/A')}")
            st.markdown(f"**Brand:** {profile['preferred_brands']}")
            st.markdown(f"**Social influence:** {profile['social_influence']}")
            st.markdown(f"**Shops:** {profile['purchase_frequency']}")

        else:
            name      = st.text_input("Your name", placeholder="e.g. Arjun Mehta")
            age       = st.slider("Age", 15, 45, 21)
            gender    = st.selectbox("Gender", ["Male", "Female", "Other"])
            area      = st.selectbox("Area", AREAS)
            school    = st.text_input("School / College", placeholder="e.g. Indiranagar College")
            budget    = st.selectbox("Budget", BUDGETS)
            style     = st.selectbox("Style preference", STYLES)
            size      = st.selectbox("Size", SIZES)
            color_pref= st.selectbox("Favourite color", COLORS)
            occasion  = st.selectbox("Main occasion", OCCASIONS)
            brand     = st.selectbox("Preferred brand", BRANDS)
            influence = st.selectbox("Social influence", ["High", "Medium", "Low"])
            frequency = st.selectbox("Shopping frequency", ["Weekly", "Monthly", "Rarely"])

            profile = {
                "user_id":            "CUSTOM",
                "name":               name if name else "Shopper",
                "age":                age,
                "gender":             gender,
                "area":               area,
                "school":             school if school else f"{area} College",
                "budget":             budget,
                "style_pref":         style,
                "size":               size,
                "color_pref":         color_pref,
                "occasion":           occasion,
                "preferred_brands":   brand,
                "social_influence":   influence,
                "purchase_frequency": frequency,
            }

        st.divider()
        go = st.button("FIND YOUR STYLE", type="primary", use_container_width=True)

    if mode == "Enter my own profile" and go and not profile["name"].strip():
        st.warning("Please enter your name before continuing.")
        st.stop()

    return profile, go
