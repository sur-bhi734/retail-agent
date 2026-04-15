import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

/* Global Overrides */
* {
    font-family: 'Inter', sans-serif;
}
div[data-testid="stAlert"] {
    background-color: #F5F2EB !important;
    color: #423030 !important;
    border: 1px solid #E8E0D5 !important;
}
div[data-testid="stAlert"] * {
    color: #423030 !important;
}
h1, h2, h3, h4, h5, h6 {
    font-weight: 600 !important;
    letter-spacing: -0.5px;
}

/* Product cards */
.product-card {
    background: #FFFFFF;
    border: 1px solid #E8E0D5;
    border-radius: 0px;
    padding: 0;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(66,48,48,0.03);
    overflow: hidden;
    transition: transform 0.2s ease;
}
.product-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(66,48,48,0.06);
}
.product-img {
    width: 100%;
    aspect-ratio: 4/5;
    object-fit: cover;
    background-color: #E8E0D5;
}
.product-info {
    padding: 16px;
}
.product-card .brand-badge {
    display: inline-block;
    color: #A39B92;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 6px;
}
.product-card .style-badge {
    display: inline-block;
    background: #F5F2EB;
    color: #423030;
    padding: 2px 6px;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-left: 8px;
    margin-bottom: 6px;
}
.product-card .price {
    font-size: 16px;
    font-weight: 600;
    color: #423030;
    margin-top: 8px;
}
.product-card .product-name {
    font-size: 14px;
    font-weight: 400;
    color: #423030;
    margin: 0;
    line-height: 1.4;
}
.product-card .product-meta {
    font-size: 12px;
    color: #8A817C;
    margin-top: 10px;
}
/* Section headers */
.section-header {
    font-size: 12px;
    font-weight: 600;
    color: #423030;
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #E8E0D5;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
/* Event form */
.event-pill {
    background: #FFFFFF;
    color: #423030;
    padding: 12px;
    border: 1px solid #E8E0D5;
    margin-bottom: 8px;
}
.event-pill-title {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 12px;
    margin-bottom: 4px;
}
/* Comparison table */
.comp-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 8px;
}
.comp-table th {
    background: #F5F2EB;
    color: #423030;
    padding: 12px 10px;
    text-align: left;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 10px;
    letter-spacing: 1px;
}
.comp-table td {
    padding: 12px 10px;
    border-bottom: 1px solid #E8E0D5;
    color: #423030;
}
/* Removed hardcoded button tracking */
</style>
""", unsafe_allow_html=True)
