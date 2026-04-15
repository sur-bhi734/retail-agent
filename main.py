import streamlit as st
from core.user_profile import load_users
from agent import run_agent
from ui.styles import apply_custom_css
from ui.sidebar import render_sidebar
from ui.landing import render_landing_page
from ui.dashboard import render_dashboard

st.set_page_config(page_title="ShopSense", layout="wide")
apply_custom_css()

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>ShopSense</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A39B92; text-transform: uppercase; font-size: 11px; letter-spacing: 2px; margin-bottom: 24px;'>Curated Fashion Engine</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; border-top: 1px solid #E8E0D5;'>", unsafe_allow_html=True)

# ── Load users ─────────────────────────────────────────────────────────────
users_df = load_users()

# ── Sidebar — Profile ──────────────────────────────────────────────────────
profile, go = render_sidebar(users_df)

# ── Main content ───────────────────────────────────────────────────────────
if not go:
    render_landing_page()
else:
    with st.spinner("Compiling styling profile..."):
        result = run_agent(profile)
    
    render_dashboard(profile, result)