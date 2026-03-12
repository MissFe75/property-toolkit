import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math

# ─────────────────────────────────────────────
# PAGE CONFIG & THEME
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="MF Property Toolkit",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Warm parchment theme via custom CSS
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

    /* Global background */
    .stApp { background-color: #f7f2ea; }
    [data-testid="stSidebar"] { background-color: #1a1410 !important; }
    [data-testid="stSidebar"] * { color: #e8dcc8 !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #b5863a !important; }

    /* Main font */
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* Headings */
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1a1410 !important; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #faf7f2, #f3ece0);
        border: 1px solid #e8dcc8;
        border-left: 4px solid #b5863a;
        border-radius: 4px;
        padding: 1rem !important;
    }
    [data-testid="metric-container"] label { color: #8a7e6e !important; font-size: 0.72rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #1a1410 !important; font-family: 'Playfair Display', serif !important; font-size: 1.4rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

    /* Inputs */
    .stNumberInput input, .stSelectbox select {
        background: #fff !important;
        border: 1px solid #e0d0b8 !important;
        border-radius: 3px !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stNumberInput input:focus { border-color: #b5863a !important; box-shadow: 0 0 0 2px rgba(181,134,58,0.15) !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #b5863a, #d4a853) !important;
        color: white !important;
        border: none !important;
        border-radius: 3px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        padding: 0.5rem 1.5rem !important;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #a07530, #c49843) !important; }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #f3ece0 !important;
        border: 1px solid #e8dcc8 !important;
        border-radius: 3px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        color: #1a1410 !important;
    }

    /* Divider */
    hr { border-color: #e8dcc8 !important; }

    /* Success/error/info boxes */
    .stSuccess { background-color: rgba(74,140,92,0.1) !important; border-left-color: #4a8c5c !important; }
    .stError { background-color: rgba(192,73,58,0.1) !important; border-left-color: #c0493a !important; }
    .stInfo { background-color: rgba(181,134,58,0.1) !important; border-left-color: #b5863a !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] { border: 1px solid #e8dcc8 !important; border-radius: 4px !important; }

    /* Sidebar logo area */
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 1rem 1rem;
        border-bottom: 1px solid #3a2e22;
        margin-bottom: 1rem;
    }
    .sidebar-logo h2 {
        font-family: 'Playfair Display', serif !important;
        color: #d4a853 !important;
        font-size: 1.3rem !important;
        margin: 0.5rem 0 0.2rem !important;
    }
    .sidebar-logo p { color: #8a7e6e !important; font-size: 0.72rem !important; letter-spacing: 0.1em; margin: 0; }

    /* Page header banner */
    .page-header {
        background: linear-gradient(135deg, #1a1410 0%, #2d2018 100%);
        border-radius: 6px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .page-header h1 { color: #d4a853 !important; margin: 0 !important; font-size: 1.6rem !important; }
    .page-header p { color: #8a7e6e !important; margin: 0.25rem 0 0 !important; font-size: 0.8rem !important; }

    /* Section labels */
    .section-label {
        font-size: 0.65rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #b5863a;
        font-weight: 500;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #e8dcc8;
    }

    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #faf7f2, #f3ece0);
        border: 1px solid #e8dcc8;
        border-left: 4px solid #b5863a;
        border-radius: 4px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
    }
    .insight-box strong { color: #1a1410; }
    .insight-box span { color: #6b5d4a; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2rem">🏡</div>
        <h2>MF Property Toolkit</h2>
        <p>PROPERTY INVESTMENT ANALYSIS</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "Navigate",
        ["🏠 Property Analyzer", "📐 Mortgage Calculator", "📊 Yield Calculator"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<p style='font-size:0.65rem;color:#3a2e22;letter-spacing:0.1em;text-transform:uppercase;'>DISCLAIMER</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem;color:#5a4e3e;'>Figures are indicative only and do not constitute financial or tax advice. Consult a qualified adviser.</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────

COLORS = {
    "gold": "#b5863a",
    "gold_light": "#d4a853",
    "dark": "#1a1410",
    "parchment": "#f7f2ea",
    "parchment_mid": "#f3ece0",
    "border": "#e8dcc8",
    "green": "#4a8c5c",
    "red": "#c0493a",
    "blue": "#3a7ab5",
    "text_muted": "#8a7e6e",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#faf7f2",
    font=dict(family="DM Sans", color=COLORS["dark"]),
    margin=dict(l=20, r=20, t=
