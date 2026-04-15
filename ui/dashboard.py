import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

CATEGORY_IMAGE_MAP = {
    "tops": "https://img105.savana.com/goods-pic/219ee7bc5c4a4df9b51d65d8a436c245_w540_h720_q85.webp",
    "bottoms": "https://assets.myntassets.com/w_200,q_50,,dpr_3,fl_progressive,f_webp/assets/images/2025/DECEMBER/5/5PRuNmTV_81289dcc65434608bad49d38f5230906.jpg",
    "footwear": "https://assets.myntassets.com/dpr_1.5,q_30,w_400,c_limit,fl_progressive/assets/images/2026/MARCH/7/Tpu96GgH_0478750fcc354af18f0a87a338849dc2.jpg",
    "accessories": "https://images.pexels.com/photos/2986445/pexels-photo-2986445.jpeg?cs=srgb&dl=pexels-harper-sunday-2986445.jpg&fm=jpg",
    "ethnic wear": "https://i.pinimg.com/474x/08/2a/62/082a622cb06e8dcfd11e6865fc3fadfb.jpg",
    "default": "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=400&q=80"
}

def get_image_src(img_val: str, fallback_url: str) -> str:
    
    if not img_val or str(img_val).lower() == "nan":
        return fallback_url
    if img_val.startswith("http"):
        return img_val
    if os.path.exists(img_val):
        try:
            with open(img_val, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            ext = img_val.split('.')[-1].lower()
            mime = f"image/{ext}" if ext in ["png", "jpg", "jpeg", "webp"] else "image/jpeg"
            return f"data:{mime};base64,{encoded}"
        except:
            pass
    return fallback_url

def render_dashboard(profile: dict, result: dict):
    structured = result.get("_structured", {})
    elapsed    = result.get("response_time", 0)

    
    st.markdown(f"<div class='section-header'>Curations for {profile['name']}</div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Response Time", f"{elapsed}s", delta=None)
    k2.metric("Match Score", f"{structured.get('profile_score', 0)} / 10")
    k3.metric("Peer Connections", structured.get("peer_data", {}).get("friend_count", 0))
    k4.metric("Upcoming Events", len(structured.get("events", [])))

    if elapsed > 5:
        st.warning(f"Engine processed in {elapsed}s — model is running slow.")
    else:
        st.success(f"Generated securely in {elapsed}s")

    st.markdown("<br>", unsafe_allow_html=True)

    
    col_ev, col_peer = st.columns([1, 1])

    with col_ev:
        st.markdown('<div class="section-header">Upcoming Events</div>', unsafe_allow_html=True)
        events = structured.get("events", [])
        if events:
            for e in events:
                cats = ", ".join(e.get("relevant_categories", []))
                st.markdown(
                    f'<div class="event-pill">'
                    f'<div class="event-pill-title">{e["name"]} — {e["days_away"]} Days</div>'
                    f'<span style="font-size:11px;color:#A39B92">Curated for: {cats}</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No major events in the near future.")

    with col_peer:
        st.markdown('<div class="section-header">Social Insights</div>', unsafe_allow_html=True)
        peer = structured.get("peer_data", {})
        peer_products = peer.get("peer_products", [])
        peer_styles   = peer.get("peer_styles", [])

        if peer_products:
            st.markdown(f"<div style='font-size:13px; margin-bottom:8px;'><b>Peer Acquisitions:</b> {', '.join(peer_products[:3])}</div>", unsafe_allow_html=True)
        if peer_styles:
            for s in peer_styles:
                pct = int(s["friends"] / max(peer.get("friend_count", 1), 1) * 100)
                st.markdown(f"<div style='font-size:12px; margin-bottom:2px; font-weight:600;'>{s['style'].upper()} — {s['friends']} Connection(s)</div>", unsafe_allow_html=True)
                st.progress(min(pct, 100))
        if not peer_products and not peer_styles:
            st.info(peer.get("note", "No peer data available."))

    st.markdown("<br>", unsafe_allow_html=True)

    
    trends = structured.get("trends", {})
    area_trends = trends.get("area_trends", [])

    if area_trends:
        st.markdown('<div class="section-header">Local Trend Analysis</div>', unsafe_allow_html=True)
        trend_df = pd.DataFrame(area_trends).head(5)
        trend_df["label"] = trend_df["product_name"] + " (" + trend_df["color"] + ")"
        fig = px.bar(
            trend_df,
            x="units_sold",
            y="label",
            orientation="h",
            color="units_sold",
            color_continuous_scale=["#E8E0D5", "#423030"],
            labels={"units_sold": "Units Sold", "label": "Product"},
            title=f"Trending in {profile['area']}",
        )
        fig.update_layout(
            height=240,
            margin=dict(l=0, r=20, t=40, b=0),
            showlegend=False,
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed"),
            font=dict(family="Inter", color="#423030")
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

        top_colors = trends.get("top_colors", [])
        if top_colors:
            st.markdown(f"<div style='font-size:13px; color:#A39B92; text-transform:uppercase; letter-spacing:1px;'>Trending Palettes: {' · '.join(top_colors)}</div>", unsafe_allow_html=True)


    
    st.markdown('<div class="section-header">Curated Collection</div>', unsafe_allow_html=True)

    top_products = structured.get("top_products", [])
    if top_products:
        cols = st.columns(min(len(top_products), 3))
        for i, p in enumerate(top_products[:3]):
            with cols[i]:
                budget_badge = {"Low": "Budget", "Mid": "Standard", "High": "Premium"}.get(
                    p.get("budget_tier", ""), ""
                )
                cat_img = CATEGORY_IMAGE_MAP.get(p.get("category", "").lower(), CATEGORY_IMAGE_MAP["default"])
                final_img = get_image_src(p.get("image_url", ""), cat_img)
                    
                st.markdown(f"""
<div class="product-card">
  <img src="{final_img}" class="product-img" alt="{p.get('category','')}">
  <div class="product-info">
      <span class="brand-badge">{p.get('brand','')}</span>
      <span class="style-badge">{p.get('style','')}</span>
      <div class="product-name">{p.get('name','')}</div>
      <div class="price">₹{p.get('price',''):,}</div>
      <div class="product-meta">
        {p.get('color','')} · Size {p.get('size','')} <br>{budget_badge} Tier
      </div>
  </div>
</div>
""", unsafe_allow_html=True)

        
        if len(top_products) > 3:
            extra_cols = st.columns(2)
            for i, p in enumerate(top_products[3:5]):
                with extra_cols[i]:
                    budget_badge = {"Low": "Budget", "Mid": "Standard", "High": "Premium"}.get(
                        p.get("budget_tier", ""), ""
                    )
                    cat_img = CATEGORY_IMAGE_MAP.get(p.get("category", "").lower(), CATEGORY_IMAGE_MAP["default"])
                    final_img = get_image_src(p.get("image_url", ""), cat_img)
                        
                    st.markdown(f"""
<div class="product-card">
  <img src="{final_img}" class="product-img" alt="{p.get('category','')}">
  <div class="product-info">
      <span class="brand-badge">{p.get('brand','')}</span>
      <span class="style-badge">{p.get('style','')}</span>
      <div class="product-name">{p.get('name','')}</div>
      <div class="price">₹{p.get('price',''):,}</div>
      <div class="product-meta">{p.get('color','')} · Size {p.get('size','')} <br>{budget_badge} Tier</div>
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.info("No products aligned with current criteria.")

    
    with st.expander("AI Narrative Strategy", expanded=False):
        st.write(result.get("recommended_products", "—"))


    
    col_reason, col_profile = st.columns([3, 2])

    with col_reason:
        st.markdown('<div class="section-header">Strategic Alignment</div>', unsafe_allow_html=True)
        st.info(result.get("personalized_reasoning", "—"))

        st.markdown('<div class="section-header">Environmental Factors</div>', unsafe_allow_html=True)
        st.write(result.get("local_peer_insights", "—"))

    with col_profile:
        st.markdown('<div class="section-header">Profile Vector</div>', unsafe_allow_html=True)
        st.write(result.get("profile_summary", "—"))

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

    
    col_plan, col_comp = st.columns([1, 2])

    with col_plan:
        st.markdown('<div class="section-header">Acquisition Roadmap</div>', unsafe_allow_html=True)
        next_hints = structured.get("next_hints", [])
        if next_hints:
            st.markdown("<div style='font-size:12px; color:#A39B92; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>Suggested Progression:</div>", unsafe_allow_html=True)
            for cat in next_hints:
                st.markdown(f"<div style='font-size:13px; font-weight:600; margin-bottom:4px;'>→ {cat}</div>", unsafe_allow_html=True)
        st.write(result.get("next_purchase_plan", "—"))

    with col_comp:
        st.markdown('<div class="section-header">Market Comparison</div>', unsafe_allow_html=True)
        comps = structured.get("comparisons", [])

        if comps:
            
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
            st.info("Insufficient variance for matrix generation.")

        with st.expander("Comparative Deep Dive", expanded=False):
            st.write(result.get("comparative_suggestions", "—"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"Disclaimer: {result.get('disclaimer', 'AI-generated curation. Please verify styling accuracy.')}")
