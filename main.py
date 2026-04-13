import streamlit as st
import pandas as pd
import plotly.express as px
from agent import run_agent

st.set_page_config(page_title="ShopSense AI", layout="wide", page_icon="🛍️")

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Product cards */
.product-card {
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    position: relative;
}
.product-card .brand-badge {
    display: inline-block;
    background: #e8f4f8;
    color: #1a6a8a;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 4px;
}
.product-card .style-badge {
    display: inline-block;
    background: #f0e8f8;
    color: #6a1a8a;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 4px;
    margin-bottom: 4px;
}
.product-card .price {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
}
.product-card .product-name {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a2e;
    margin: 4px 0 2px;
}
.product-card .product-meta {
    font-size: 12px;
    color: #666;
}
/* Section headers */
.section-header {
    font-size: 16px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 18px 0 10px;
    padding-bottom: 4px;
    border-bottom: 2px solid #e0e0e0;
}
/* Score bar */
.score-bar-bg {
    background: #e0e0e0;
    border-radius: 8px;
    height: 10px;
    margin-top: 4px;
}
.score-bar-fill {
    background: linear-gradient(90deg, #1a6a8a, #6a1a8a);
    border-radius: 8px;
    height: 10px;
}
/* Event pill */
.event-pill {
    display: inline-block;
    background: #fff3cd;
    color: #856404;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px 3px;
}
/* Comparison table */
.comp-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 8px;
}
.comp-table th {
    background: #f0f2f5;
    padding: 6px 10px;
    text-align: left;
    font-weight: 600;
}
.comp-table td {
    padding: 6px 10px;
    border-bottom: 1px solid #eee;
}
.comp-table tr:hover td { background: #fafafa; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("## 🛍️ ShopSense — Personalized Shopping Assistant")
st.caption("Powered by local AI · Multi-factor recommendations · No data leaves your machine")
st.divider()

# ── Load users ─────────────────────────────────────────────────────────────
@st.cache_data
def load_users():
    return pd.read_csv("data/users.csv")

users_df = load_users()

AREAS   = ["Koramangala", "Indiranagar", "Whitefield", "Jayanagar", "HSR Layout"]
STYLES  = ["Casual", "Ethnic", "Streetwear", "Formal"]
BRANDS  = ["Roadster", "HRX", "W", "Biba", "Puma", "Campus", "Van Heusen"]
SIZES   = ["XS", "S", "M", "L", "XL"]
BUDGETS = ["Low", "Mid", "High"]
COLORS  = ["Black", "White", "Navy", "Olive", "Maroon", "Beige", "Mustard", "Pastel", "Blue"]
OCCASIONS = ["College", "Festive", "Casual Outing", "Work", "Party"]

# ── Sidebar — Profile ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    mode = st.radio("Mode", ["Select existing shopper", "Enter my own profile"], horizontal=False)
    st.divider()

    if mode == "Select existing shopper":
        selected_name = st.selectbox("Select shopper", users_df["name"].tolist())
        row = users_df[users_df["name"] == selected_name].iloc[0]
        profile = row.to_dict()

        # Display profile card
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
    go = st.button("✨ Get Recommendations", type="primary", use_container_width=True)

# ── Main content ───────────────────────────────────────────────────────────
if not go:
    # Landing state
    st.markdown("#### How ShopSense works")
    c1, c2, c3, c4 = st.columns(4)
    c1.info("**👤 Profile**\nBuilds a 10-parameter shopper profile")
    c2.info("**📍 Local trends**\nChecks what's selling in your area")
    c3.info("**👥 Peer insights**\nLooks at what your friends are buying")
    c4.info("**📅 Events**\nAdapts to upcoming festivals & occasions")

    st.markdown("---")
    c5, c6, c7 = st.columns(3)
    c5.success("**⚡ Multi-factor scoring**\nEvery product gets a relevance score across 5 dimensions")
    c6.success("**💡 Explainability**\nEach recommendation cites your profile data specifically")
    c7.success("**🗺️ Purchase planning**\nPredicts your next 2 logical purchases")

else:
    # Validate custom profile
    if mode == "Enter my own profile" and not profile["name"].strip():
        st.warning("Please enter your name before continuing.")
        st.stop()

    with st.spinner("ShopSense is thinking — scoring products and consulting the AI..."):
        result = run_agent(profile)

    structured = result.get("_structured", {})
    elapsed    = result.get("response_time", 0)

    # ── Top KPI bar ───────────────────────────────────────────────────────
    st.markdown(f"### Recommendations for **{profile['name']}**")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("⏱️ Response time", f"{elapsed}s", delta=None)
    k2.metric("🏆 Match score", f"{structured.get('profile_score', 0)} / 10")
    k3.metric("👥 Peer connections", structured.get("peer_data", {}).get("friend_count", 0))
    k4.metric("📅 Upcoming events", len(structured.get("events", [])))

    if elapsed > 5:
        st.warning(f"Response took {elapsed}s — model is running slow. Consider using a faster Ollama model.")
    else:
        st.success(f"Generated in {elapsed}s")

    st.divider()

    # ── Row 1: Events + Peer insights (side by side) ───────────────────────
    col_ev, col_peer = st.columns([1, 1])

    with col_ev:
        st.markdown('<div class="section-header">📅 Upcoming Events</div>', unsafe_allow_html=True)
        events = structured.get("events", [])
        if events:
            for e in events:
                cats = ", ".join(e.get("relevant_categories", []))
                badge_color = "#fff3cd" if e["days_away"] > 10 else "#ffe0b2"
                st.markdown(
                    f'<span class="event-pill" style="background:{badge_color}">'
                    f'📌 {e["name"]} — in {e["days_away"]} days</span>'
                    f'<br><span style="font-size:11px;color:#888;margin-left:6px">'
                    f'Relevant: {cats}</span><br>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No major events in the next 30 days.")

    with col_peer:
        st.markdown('<div class="section-header">👥 Peer & Social Insights</div>', unsafe_allow_html=True)
        peer = structured.get("peer_data", {})
        peer_products = peer.get("peer_products", [])
        peer_styles   = peer.get("peer_styles", [])

        if peer_products:
            st.markdown(f"**What your friends bought:** {', '.join(peer_products[:3])}")
        if peer_styles:
            for s in peer_styles:
                pct = int(s["friends"] / max(peer.get("friend_count", 1), 1) * 100)
                st.markdown(f"**{s['style']}** style — {s['friends']} friend(s)")
                st.progress(min(pct, 100))
        if not peer_products and not peer_styles:
            st.info(peer.get("note", "No peer data available."))

    st.divider()

    # ── Row 2: Local trends chart ──────────────────────────────────────────
    trends = structured.get("trends", {})
    area_trends = trends.get("area_trends", [])

    if area_trends:
        st.markdown('<div class="section-header">📍 Local Trend Insights</div>', unsafe_allow_html=True)
        trend_df = pd.DataFrame(area_trends).head(5)
        trend_df["label"] = trend_df["product_name"] + " (" + trend_df["color"] + ")"
        fig = px.bar(
            trend_df,
            x="units_sold",
            y="label",
            orientation="h",
            color="units_sold",
            color_continuous_scale=["#c8e6fa", "#1a6a8a"],
            labels={"units_sold": "Units Sold", "label": "Product"},
            title=f"Top trending items in {profile['area']}",
        )
        fig.update_layout(
            height=240,
            margin=dict(l=0, r=20, t=40, b=0),
            showlegend=False,
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed"),
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

        top_colors = trends.get("top_colors", [])
        if top_colors:
            st.markdown(f"**Trending colors in your area:** {' · '.join(top_colors)}")

        st.divider()

    # ── Row 3: Recommended products (cards) ───────────────────────────────
    st.markdown('<div class="section-header">🛍️ Recommended Products</div>', unsafe_allow_html=True)

    top_products = structured.get("top_products", [])
    if top_products:
        cols = st.columns(min(len(top_products), 3))
        for i, p in enumerate(top_products[:3]):
            with cols[i]:
                budget_badge = {"Low": "🟢 Budget-friendly", "Mid": "🟡 Mid-range", "High": "🔴 Premium"}.get(
                    p.get("budget_tier", ""), ""
                )
                st.markdown(f"""
<div class="product-card">
  <span class="brand-badge">{p.get('brand','')}</span>
  <span class="style-badge">{p.get('style','')}</span>
  <div class="product-name">{p.get('name','')}</div>
  <div class="price">₹{p.get('price',''):,}</div>
  <div class="product-meta">
    {p.get('category','')} · {p.get('color','')} · Size {p.get('size','')}
    <br>{budget_badge}
  </div>
</div>
""", unsafe_allow_html=True)

        # Show remaining 2 in a smaller row
        if len(top_products) > 3:
            extra_cols = st.columns(2)
            for i, p in enumerate(top_products[3:5]):
                with extra_cols[i]:
                    st.markdown(f"""
<div class="product-card">
  <span class="brand-badge">{p.get('brand','')}</span>
  <span class="style-badge">{p.get('style','')}</span>
  <div class="product-name">{p.get('name','')}</div>
  <div class="price">₹{p.get('price',''):,}</div>
  <div class="product-meta">{p.get('category','')} · {p.get('color','')} · Size {p.get('size','')}</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.info("No products scored above threshold.")

    # Also show LLM's recommendation text
    with st.expander("💬 AI recommendation narrative", expanded=False):
        st.write(result.get("recommended_products", "—"))

    st.divider()

    # ── Row 4: Personalized reasoning + Profile summary ───────────────────
    col_reason, col_profile = st.columns([3, 2])

    with col_reason:
        st.markdown('<div class="section-header">💡 Personalized Reasoning</div>', unsafe_allow_html=True)
        st.info(result.get("personalized_reasoning", "—"))

        st.markdown('<div class="section-header">📍 Local & Peer Insights (AI)</div>', unsafe_allow_html=True)
        st.write(result.get("local_peer_insights", "—"))

    with col_profile:
        st.markdown('<div class="section-header">👤 Profile Summary</div>', unsafe_allow_html=True)
        st.write(result.get("profile_summary", "—"))

        st.markdown("**Profile parameters:**")
        params = {
            "Style":     profile["style_pref"],
            "Budget":    profile["budget"],
            "Color":     profile.get("color_pref", "—"),
            "Occasion":  profile.get("occasion", "—"),
            "Size":      profile.get("size", "—"),
            "Brand":     profile["preferred_brands"],
        }
        param_df = pd.DataFrame(params.items(), columns=["Parameter", "Value"])
        st.dataframe(param_df, hide_index=True, use_container_width=True)

    st.divider()

    # ── Row 5: Next purchase plan + Comparisons ───────────────────────────
    col_plan, col_comp = st.columns([1, 2])

    with col_plan:
        st.markdown('<div class="section-header">📅 Next Purchase Plan</div>', unsafe_allow_html=True)
        next_hints = structured.get("next_hints", [])
        if next_hints:
            st.markdown("**Suggested next categories:**")
            for cat in next_hints:
                st.markdown(f"→ **{cat}**")
        st.write(result.get("next_purchase_plan", "—"))

    with col_comp:
        st.markdown('<div class="section-header">⚖️ Comparative Suggestions</div>', unsafe_allow_html=True)
        comps = structured.get("comparisons", [])

        if comps:
            # Build comparison table from catalog data
            comp_rows = [
                {
                    "Product":  p.get("name", ""),
                    "Brand":    p.get("brand", ""),
                    "Price":    f"₹{p.get('price', 0):,}",
                    "Style":    p.get("style", ""),
                    "Category": p.get("category", ""),
                    "Color":    p.get("color", ""),
                }
                for p in comps
            ]
            st.dataframe(pd.DataFrame(comp_rows), hide_index=True, use_container_width=True)
        else:
            st.info("Not enough catalog variety for comparison in this budget/style.")

        with st.expander("💬 AI comparison narrative", expanded=False):
            st.write(result.get("comparative_suggestions", "—"))

    st.divider()

    # ── Disclaimer ────────────────────────────────────────────────────────
    st.caption(f"⚠️ {result.get('disclaimer', 'These are AI-generated suggestions only.')}")