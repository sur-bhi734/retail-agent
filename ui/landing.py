import streamlit as st
import base64
import os

def render_landing_page():
   
    st.markdown("""
        <style>
            .hero-bg {
                background-color: #E6D5C3; 
                border-radius: 12px;
                padding: 40px;
                margin-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.markdown("<div style='padding-top: 20px;'>", unsafe_allow_html=True)
        st.markdown("""
        <h1 style='font-size: 54px; font-weight: 500; font-family: "Playfair Display", Georgia, serif; line-height: 1.1; margin-bottom: 24px; color: #423030;'>
            Find The Best<br>Fashion Style<br>For You
        </h1>
        <p style='color: #6C5B5B; font-size: 14px; margin-bottom: 40px; max-width: 90%; line-height: 1.8;'>
            ShopSense is a long-established engine that builds a comprehensive profile, analyzes regional trends, incorporates peer insight, and adapts to future events to evaluate clothing completely. Make your next stylistic acquisition logical and intentional.
        </p>
        """, unsafe_allow_html=True)
        
        
       
        st.markdown("<p style='letter-spacing: 4px; color: #423030; opacity: 0.5; margin-bottom: 12px;'>· · · · · ·</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        img_path = r"C:\Users\SurbhiAnand\.gemini\antigravity\brain\70013dce-9c05-491f-b51d-96c4b7f111b8\hero_fashion_image_1776196654941.png"
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            
            
            st.markdown(f'''
                <div style="border-radius: 80px 0 0 0; overflow: hidden; height: 100%; min-height: 500px; box-shadow: -10px 10px 30px rgba(66,48,48,0.08);">
                    <img src="data:image/png;base64,{encoded}" style="width: 100%; height: 100%; object-fit: cover; display: block; object-position: center;">
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.error("Image asset not found. Please provide tracking image.")
            
    st.markdown("<br><br>", unsafe_allow_html=True)

    
    st.markdown("""
    <style>
    .feature-card {
        background-color: #FFFFFF;
        border-radius: 4px;
        padding: 28px 24px;
        margin-bottom: 28px;
        box-shadow: 0 4px 12px rgba(66,48,48,0.03);
        border: 1px solid #E8E0D5;
        transition: all 0.2s ease;
        height: 100%;
    }
    .feature-card:hover { border-color: #423030; }
    .feature-title {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #423030;
        margin-bottom: 8px;
    }
    .feature-desc {
        font-size: 12px;
        color: #8A817C;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    
    r1c1, r1c2, r1c3 = st.columns(3, gap="large")
    with r1c1:
        st.markdown("<div class='feature-card'><div class='feature-title'>Profile Data</div><div class='feature-desc'>Builds a 10-parameter shopper profile completely locally.</div></div>", unsafe_allow_html=True)
    with r1c2:
        st.markdown("<div class='feature-card'><div class='feature-title'>Algorithms</div><div class='feature-desc'>All products are algorithmically mapped and evaluated.</div></div>", unsafe_allow_html=True)
    with r1c3:
        st.markdown("<div class='feature-card'><div class='feature-title'>Market Trends</div><div class='feature-desc'>Analyzes local geographical market and regional data.</div></div>", unsafe_allow_html=True)

    
    r2c1, r2c2, r2c3 = st.columns(3, gap="large")
    with r2c1:
        st.markdown("<div class='feature-card'><div class='feature-title'>Explainability</div><div class='feature-desc'>Provides complete citations across specific profile vectors.</div></div>", unsafe_allow_html=True)
    with r2c2:
        st.markdown("<div class='feature-card'><div class='feature-title'>Calendar Events</div><div class='feature-desc'>Adapts styling perfectly to upcoming personal occasions.</div></div>", unsafe_allow_html=True)
    with r2c3:
        st.markdown("<div class='feature-card'><div class='feature-title'>Forecasting</div><div class='feature-desc'>Proactively predicts and roadmaps future acquisitions.</div></div>", unsafe_allow_html=True)

    st.markdown("<br><br><br><h2 style='text-align: center; font-family: \"Playfair Display\", serif;'>New Collection</h2><br>", unsafe_allow_html=True)
