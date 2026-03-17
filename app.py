import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math
import base64
import os
import io
from datetime import date as _date

# ─────────────────────────────────────────────
# PAGE CONFIG & THEME
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Property Compass",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@media (max-width: 600px) {
    .pc-banner { padding: 0 1rem !important; height: 84px !important; }
    .pc-name { font-size: 18px !important; }
    .pc-tagline { font-size: 10.5px !important; line-height: 1.4 !important; white-space: normal !important; }
}
</style>
<div class="pc-banner" style="
    width:100%; background:#F5F0E8;
    border-bottom:1px solid rgba(61,90,128,0.12);
    display:flex; align-items:center; justify-content:space-between;
    padding:0 2rem; height:72px;
    position:fixed; top:0; left:0; right:0; z-index:999999;
    margin:0; box-sizing:border-box;
">
    <div style="display:flex;flex-direction:row;align-items:center;gap:0.6rem;text-decoration:none;min-width:0;">
        <svg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='#3D5A80' stroke-width='1.75' stroke-linecap='round' stroke-linejoin='round' style="flex-shrink:0;"><circle cx='12' cy='12' r='10'/><polygon points='16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76'/></svg>
        <div style="display:flex;flex-direction:column;line-height:1.2;gap:1px;min-width:0;">
            <span class="pc-name" style="font-family:'Inter',sans-serif;font-weight:700;font-size:24px;color:#3D5A80;letter-spacing:-0.025em;">Property Compass</span>
            <span class="pc-tagline" style="font-family:'Inter',sans-serif;font-size:13px;font-weight:300;color:#3D5A80;letter-spacing:0.04em;">by Sextant Digital &nbsp;·&nbsp; Calculators for buying and investing in Aussie property</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    /* ── Hide Streamlit header ── */
    header[data-testid="stHeader"] { display: none !important; }

    /* ── Offset app body for fixed banner ── */
    .stApp { margin-top: 72px !important; }

    /* ── Base ── */
    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; font-weight: 300 !important; }
    .stApp {
        background: linear-gradient(180deg, #F5F0E8 0%, #FAF7F2 35%, #FFFFFF 100%) !important;
        background-attachment: fixed !important;
        color: #1A1A2E;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #FAF7F2 !important;
        border-right: 1px solid rgba(61,90,128,0.12) !important;
    }
    [data-testid="stSidebar"] * { color: #1A1A2E !important; }

    /* ── Main padding ── */
    .main .block-container { padding: 0 2rem 2rem !important; max-width: 1400px; }
    [data-testid="stMainBlockContainer"] { padding-top: 0 !important; margin-top: 0 !important; }
    .main > div:first-child { padding-top: 0 !important; margin-top: 0 !important; }
    [data-testid="stVerticalBlock"] > div:first-child { margin-top: 0 !important; padding-top: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }

    /* ── Sidebar top gap ── */
    [data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
    section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
    [data-testid="stSidebarContent"] { padding-top: 0 !important; }
    [data-testid="stSidebarUserContent"] { padding-top: 0 !important; margin-top: 0 !important; }
    [data-testid="stSidebar"] .sidebar-logo { margin-top: -2rem !important; }

    /* ── Headings ── */
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; letter-spacing: -0.03em !important; color: #1A1A2E !important; }

    /* ── Metric tiles ── */
    .tile-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0 1.5rem;
    }
    .tile {
        flex: 1 1 160px;
        background: #FFFFFF;
        border: 1px solid #EAE4DC;
        border-radius: 14px;
        padding: 1.25rem 1.5rem 1.1rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        min-width: 140px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .tile:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }
    .tile::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--accent, #3D5A80);
        border-radius: 14px 14px 0 0;
    }
    .tile::after {
        content: '';
        position: absolute;
        top: -30px; right: -20px;
        width: 90px; height: 90px;
        background: radial-gradient(circle, var(--accent-glow, rgba(61,90,128,0.08)) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .tile-icon { font-size: 1.3rem; margin-bottom: 0.6rem; opacity: 0.85; }
    .tile-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #1A1A2E;
        letter-spacing: -0.03em;
        line-height: 1.1;
        font-family: 'Inter', sans-serif;
    }
    .tile-value-sm { font-size: 1.15rem; }
    .tile-label {
        font-size: 0.625rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-top: 0.35rem;
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    .tile-delta {
        font-size: 0.72rem;
        font-weight: 600;
        margin-top: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }
    .tile-delta.pos { color: #3D5A80; }
    .tile-delta.neg { color: #ef4444; }
    .tile-delta.neu { color: #9CA3AF; }

    /* ── Input card ── */
    .input-card {
        background: #FFFFFF;
        border: 1px solid #EAE4DC;
        border-radius: 14px;
        padding: 1.25rem 1.5rem 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 6px rgba(61,90,128,0.06);
    }

    /* ── Section label ── */
    .section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        text-transform: none;
        color: #1A1A2E;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid rgba(61,90,128,0.15);
        font-family: 'Inter', sans-serif;
        width: 100%;
    }
    .section-label .sl-icon { font-size: 1.1rem; flex-shrink: 0; line-height: 0; }

    /* ── Page header ── */
    .page-header {
        display: flex;
        align-items: center;
        gap: 2rem;
        background: transparent;
        border: none;
        border-bottom: 1px solid #E8E2D9;
        border-radius: 0;
        padding: 0.5rem 0 1.25rem;
        margin-bottom: 1.75rem;
    }
    .page-header .header-content { flex: 1; min-width: 0; }
    .page-header h1 {
        color: #1A1A2E !important;
        margin: 0 !important;
        font-size: 1.75rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.03em !important;
    }
    .page-header .sub {
        color: #9CA3AF !important;
        margin: 0.25rem 0 0 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.06em;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
        text-transform: none;
    }
    /* ── Full-width hero banner (piggybank etc.) ── */
    .page-hero-banner {
        width: 100%;
        height: 400px;
        border-radius: 14px;
        overflow: hidden;
        position: relative;
        box-shadow: 0 6px 28px rgba(61,90,128,0.16);
    }
    .page-hero-banner > img {
        width: 100%; height: 100%;
        object-fit: cover;
        object-position: center center;
        display: block;
    }
    .page-hero-banner > img.hero-top {
        object-position: top center !important;
    }
    .page-hero-banner.hero-contain {
        height: 500px !important;
        background-color: #F5F0E8;
    }
    .page-hero-banner.hero-contain > img {
        object-fit: contain !important;
        object-position: center top !important;
        background-color: #F5F0E8;
    }
    .page-hero-overlay {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        padding: 1.75rem 2rem 1.5rem;
        background: linear-gradient(to top, rgba(10,15,30,0.82) 0%, rgba(10,15,30,0.45) 55%, transparent 100%);
    }
    .page-hero-overlay h1 {
        color: #FFFFFF !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.6rem !important;
        margin: 0 !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.03em !important;
    }
    .page-hero-overlay .sub {
        color: rgba(255,255,255,0.72) !important;
        margin: 0.3rem 0 0 !important;
        font-size: 0.75rem !important;
        font-weight: 300 !important;
        letter-spacing: 0.04em;
    }

    /* ── Small rounded thumbnail icon ── */
    .icon-thumb {
        width: 40px; height: 40px;
        border-radius: 8px;
        object-fit: cover;
        object-position: center center;
        display: inline-block;
        vertical-align: middle;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(61,90,128,0.18);
    }
    /* ── Sidebar banner ── */
    .sidebar-banner {
        width: 100%;
        height: 220px;
        display: block;
        object-fit: cover;
        object-position: center center;
    }
    .sidebar-logo-text {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        background: linear-gradient(to top, rgba(10,15,30,0.88) 0%, rgba(10,15,30,0.6) 55%, transparent 100%);
        padding: 1.4rem 1rem 0.25rem;
    }
    .sidebar-logo-text h2 {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: 300 !important;
        margin: 0 0 2px 0 !important;
        padding: 0 !important;
        letter-spacing: 0.02em !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
        font-family: 'Inter', sans-serif !important;
        text-align: left !important;
    }
    /* Zero out any Streamlit / browser default p margins inside the lockup */
    .sidebar-logo-text p,
    .sidebar-logo-text .stMarkdown p {
        margin: 0 !important;
        padding: 0 !important;
    }
    .domain-text {
        color: #FFFFFF !important;
        font-size: 11px !important;
        font-weight: 300 !important;
        letter-spacing: 0.08em !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
        opacity: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: block !important;
        line-height: 1.2 !important;
        text-align: left !important;
    }
    .sidebar-tagline {
        text-align: center !important;
        display: block !important;
        font-size: 0.69rem;
        color: #3D5A80;
        letter-spacing: 0.06em;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        margin: 0 0 0.1rem;
        white-space: normal;
        padding: 0.45rem 0.5rem;
        line-height: 1.5;
        border-top: 1px solid rgba(61,90,128,0.2);
        border-bottom: 1px solid rgba(61,90,128,0.2);
        width: 100%;
        box-sizing: border-box;
    }

    /* ── Decorative image strip ── */
    .deco-strip {
        width: 100%;
        height: 220px;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1.5rem;
        box-shadow: 0 3px 16px rgba(61,90,128,0.12);
    }
    .deco-strip img {
        width: 100%; height: 100%;
        object-fit: cover;
        object-position: center center;
        display: block;
    }

    /* ── Insight box ── */
    .insight-box {
        background: rgba(61,90,128,0.05);
        border: 1px solid rgba(61,90,128,0.2);
        border-left: 3px solid #3D5A80;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #4B5563;
        line-height: 1.6;
    }
    .insight-box strong { color: #1D3A60; font-weight: 600; }

    /* ── Sidebar logo ── */
    .sidebar-logo {
        position: relative;
        padding: 0;
        border-bottom: 1px solid #E8E2D9;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    .sidebar-logo .icon { display: none; }

    /* ── Property comparison card thumbnail ── */
    .prop-thumb {
        display: block !important;
        width: 60px !important; height: 60px !important;
        min-width: 60px !important; min-height: 60px !important;
        max-width: 60px !important; max-height: 60px !important;
        border-radius: 8px !important;
        object-fit: cover !important;
        object-position: center center !important;
        flex-shrink: 0 !important;
        box-shadow: 0 2px 8px rgba(61,90,128,0.18);
    }

    /* ── Help tooltip (? icon) ── */
    .help-wrap {
        position: relative;
        display: inline-block;
        margin-bottom: 0.75rem;
    }
    .help-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px; height: 22px;
        border-radius: 50%;
        background: #3D5A80;
        color: #fff;
        font-size: 0.72rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        cursor: help;
        user-select: none;
        box-shadow: 0 1px 4px rgba(61,90,128,0.25);
    }
    .help-tip {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        left: 30px;
        top: -8px;
        width: 340px;
        background: #FFFFFF;
        color: #1A1A2E;
        border: 1px solid #EAE4DC;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        font-size: 0.78rem;
        line-height: 1.65;
        z-index: 9999;
        box-shadow: 0 4px 16px rgba(61,90,128,0.12);
        transition: opacity 0.18s ease;
        pointer-events: none;
    }
    .help-tip strong {
        font-weight: 700 !important;
        color: #1A1A2E !important;
    }
    .help-wrap:hover .help-tip {
        visibility: visible;
        opacity: 1;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #F0EBE3 !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: 1px solid #E8E2D9 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #6B7280 !important;
        border-radius: 7px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2D4A70, #3D5A80) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(61,90,128,0.25) !important;
    }
    .stTabs [aria-selected="true"] * { color: #FFFFFF !important; }

    /* ── Inputs ── */
    .stNumberInput input, .stSelectbox select {
        background: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        color: #1A1A2E !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
    }
    textarea, [contenteditable] {
        font-family: 'Space Grotesk', sans-serif !important;
        caret-color: #3D5A80 !important;
    }
    .stNumberInput input:focus { border-color: #3D5A80 !important; box-shadow: 0 0 0 3px rgba(61,90,128,0.15) !important; }
    .stNumberInput label, .stSelectbox label {
        color: #6B7280 !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    .stNumberInput button { background: #F0EBE3 !important; color: #6B7280 !important; border: none !important; border-radius: 6px !important; }
    .stNumberInput button:hover { background: #3D5A80 !important; color: #FFFFFF !important; }

    /* ── Radio / Toggle ── */
    .stToggle label, [data-testid="stToggle"] p { color: #1A1A2E !important; font-size: 0.88rem !important; font-weight: 500 !important; }
    [data-testid="stRadio"] label, [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: #374151 !important; font-size: 0.85rem !important; }
    [data-baseweb="radio"] div { border-color: #3D5A80 !important; }
    [data-baseweb="radio"] [aria-checked="true"] div { background: #3D5A80 !important; border-color: #3D5A80 !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #2D4A70, #3D5A80) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        box-shadow: 0 4px 12px rgba(61,90,128,0.25) !important;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #1D3A60, #2D4A70) !important; box-shadow: 0 6px 20px rgba(61,90,128,0.35) !important; }
    .stDownloadButton > button {
        background: rgba(61,90,128,0.08) !important;
        color: #3D5A80 !important;
        border: 1px solid rgba(61,90,128,0.3) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: #F5F0E8 !important;
        border: 1px solid #EAE4DC !important;
        border-radius: 10px !important;
        color: #4B5563 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent {
        background: #FDFAF7 !important;
        border: 1px solid #EAE4DC !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* ── Divider ── */
    hr { border-color: #E8E2D9 !important; }

    /* ── Alert boxes ── */
    .stSuccess { background: rgba(61,90,128,0.06) !important; border-left-color: #3D5A80 !important; border-radius: 8px !important; }
    .stError   { background: rgba(239,68,68,0.06) !important;  border-left-color: #ef4444 !important; border-radius: 8px !important; }
    .stInfo    { background: rgba(59,130,246,0.06) !important;  border-left-color: #3b82f6 !important; border-radius: 8px !important; }
    .stWarning { background: rgba(245,158,11,0.06) !important;  border-left-color: #f59e0b !important; border-radius: 8px !important; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] { border: 1px solid #EAE4DC !important; border-radius: 10px !important; overflow: hidden; }
    [data-testid="stDataFrame"] * { color: #374151 !important; background-color: #FFFFFF !important; }

    /* ── Selectbox dropdown ── */
    [data-baseweb="select"] > div { background: #FFFFFF !important; border-color: #D6CECC !important; color: #1A1A2E !important; border-radius: 8px !important; }

    /* ── Summary winner card ── */
    .winner-card {
        background: #FFFFFF;
        border: 1px solid #EAE4DC;
        border-top: 3px solid #3D5A80;
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .winner-card .wc-label { font-size: 0.62rem; letter-spacing: 0.16em; color: #9CA3AF; font-family: 'Space Grotesk', sans-serif; text-transform: uppercase; margin-bottom: 0.5rem; font-weight: 700; }
    .winner-card .wc-name  { font-size: 1.4rem; font-weight: 600; color: #3D5A80; font-family: 'Inter', sans-serif; letter-spacing: -0.02em; }
    .winner-card .wc-val   { font-size: 0.78rem; color: #6B7280; margin-top: 0.3rem; }

    /* ── CG card ── */
    .cg-card {
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border-top: 3px solid;
        background: #FFFFFF;
        border: 1px solid #EAE4DC;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .cg-card .cg-label { font-size: 0.62rem; letter-spacing: 0.15em; color: #9CA3AF; font-family: 'Space Grotesk', sans-serif; text-transform: uppercase; margin-bottom: 0.4rem; font-weight: 700; }
    .cg-card .cg-val   { font-size: 1.25rem; font-weight: 800; font-family: 'Inter', sans-serif; letter-spacing: -0.03em; }
    .cg-card .cg-gain  { font-size: 0.78rem; color: #3D5A80; margin-top: 0.3rem; }

    /* ── Report Details section ── */
    .report-details-wrap {
        background: #FAF7F2;
        border: 1px solid #EAE4DC;
        border-left: 3px solid #3D5A80;
        border-radius: 10px;
        padding: 0.9rem 1.25rem 0.5rem;
        margin-bottom: 1.25rem;
    }
    .report-details-title {
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        color: #9CA3AF;
        text-transform: uppercase;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 0.6rem;
    }

    /* ── Mobile ── */
    @media (max-width: 768px) {
        .page-header { padding: 1rem 1.25rem; }
        .page-header h1 { font-size: 1.35rem !important; }
        .tile { flex: 1 1 130px; padding: 1rem; }
        .tile-value { font-size: 1.15rem; }
        .main .block-container { padding: 0.75rem !important; }

        /* Tabs: allow wrapping so labels don't get squished */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap !important;
            gap: 0.25rem !important;
            padding: 0.25rem !important;
        }
        .stTabs [data-baseweb="tab"] {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            font-size: 0.7rem !important;
            padding: 0.35rem 0.5rem !important;
            white-space: normal !important;
            text-align: center !important;
        }

        /* Plotly: hide the modebar toolbar on mobile to stop it overlapping the title */
        .modebar-container { display: none !important; }

        /* Taller header on mobile — adjust app body offset to match */
        .stApp { margin-top: 84px !important; }

        /* Sidebar toggle arrows: push below the fixed header so they're visible */
        [data-testid="collapsedControl"] {
            top: 92px !important;
            z-index: 99998 !important;
        }
        [data-testid="stSidebar"] {
            top: 84px !important;
            height: calc(100vh - 84px) !important;
        }
        /* Close button inside open sidebar */
        [data-testid="stSidebarCollapseButton"] {
            top: 92px !important;
        }
    }

    /* ── p & label text ── */
    p, label, .stMarkdown { color: #4B5563 !important; font-family: 'Inter', sans-serif !important; font-weight: 300 !important; }
    .stMarkdown strong { color: #1A1A2E !important; font-weight: 600 !important; }

    /* ── Kill dotted zeros: high-specificity input override ── */
    div[data-testid="stAppViewContainer"] input,
    div[data-testid="stAppViewContainer"] input[type="number"],
    div[data-testid="stAppViewContainer"] input[type="text"],
    div[data-testid="stAppViewContainer"] [data-baseweb="base-input"] input,
    div[data-testid="stAppViewContainer"] [data-baseweb="input"] input {
        font-family: 'Space Grotesk', sans-serif !important;
        font-variant-numeric: normal !important;
        font-variant: normal !important;
        font-feature-settings: normal !important;
        caret-color: #3D5A80 !important;
    }

    /* ── FINAL OVERRIDE: clean zeros in all inputs ── */
    input,
    .stNumberInput input,
    [data-testid="stNumberInput"] input {
        font-family: 'Space Grotesk', sans-serif !important;
        font-variant-numeric: normal !important;
        font-feature-settings: normal !important;
    }
</style>""", unsafe_allow_html=True)


# Inject JS to force Space Grotesk on inputs at runtime — overrides Streamlit's own bundled CSS
st.components.v1.html("""
<script>
function fixInputFonts() {
    const style = document.createElement('style');
    style.textContent = `
        input, input[type="number"], input[type="text"],
        [data-testid="stNumberInput"] input,
        [data-baseweb="input"] input,
        [data-baseweb="base-input"] input {
            font-family: 'Space Grotesk', sans-serif !important;
            font-variant-numeric: normal !important;
            font-feature-settings: normal !important;
        }
    `;
    document.head.appendChild(style);
}
fixInputFonts();
// Re-apply after Streamlit re-renders
const observer = new MutationObserver(fixInputFonts);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", height=0)

# ─────────────────────────────────────────────
# HOLD-TO-ACCELERATE on number input +/- buttons
# Single click → 1× step.  Hold 1-2 s → 5× step.  Hold 2+ s → 20× step.
# Uses window.parent to reach the Streamlit page DOM from the component frame.
# ─────────────────────────────────────────────
st.components.v1.html("""
<script>
(function () {
    'use strict';

    // The component runs inside a same-origin iframe; the real Streamlit DOM
    // lives one level up in window.parent.
    var pd = (window.parent || window).document;

    var TICK_MS = 150;   // interval between accelerated steps (ms)

    var intervalId = null;
    var holdStart  = null;

    // Returns how many normal steps to jump per tick based on hold duration.
    function multiplier() {
        if (!holdStart) return 1;
        var ms = Date.now() - holdStart;
        if (ms >= 2000) return 20;
        if (ms >= 1000) return 5;
        return 1;
    }

    function doStep(btn) {
        // Walk up to the container that holds the <input type="number">
        var container = btn.closest('[data-testid="stNumberInputContainer"]')
                     || btn.closest('[data-testid="stNumberInput"]')
                     || btn.parentElement;
        if (!container) return;

        var input = container.querySelector('input[type="number"]');
        if (!input) return;

        // Determine direction from the button's data-testid or its visible text
        var tid  = btn.getAttribute('data-testid') || '';
        var isUp = tid === 'stNumberInputStepUp'
                || (!tid && (btn.textContent || '').trim() === '+');

        var step    = parseFloat(input.step)  || 1;
        var minVal  = input.min !== '' ? parseFloat(input.min) : -Infinity;
        var maxVal  = input.max !== '' ? parseFloat(input.max) :  Infinity;
        var current = parseFloat(input.value) || 0;

        var delta    = step * multiplier();
        var newValue = isUp ? current + delta : current - delta;

        // Clamp to declared min/max
        newValue = Math.max(minVal, Math.min(maxVal, newValue));

        // Round to the same decimal precision as the step to prevent float drift
        var decimals = (step.toString().split('.')[1] || '').length;
        newValue = parseFloat(newValue.toFixed(decimals));

        // React tracks input state via the native property descriptor; we must
        // go through it (not just set .value) to fire a proper onChange event.
        var win = (window.parent || window);
        var setter = Object.getOwnPropertyDescriptor(
            win.HTMLInputElement.prototype, 'value'
        ).set;
        setter.call(input, String(newValue));
        input.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function startHold(btn) {
        holdStart = Date.now();
        if (intervalId) clearInterval(intervalId);
        // Begin ticking; the multiplier() function gates speed by elapsed time.
        intervalId = setInterval(function () {
            if (Date.now() - holdStart >= 1000) doStep(btn);
        }, TICK_MS);
    }

    function stopHold() {
        if (intervalId) { clearInterval(intervalId); intervalId = null; }
        holdStart = null;
    }

    function attach(btn) {
        if (btn._holdAttached) return;
        btn._holdAttached = true;
        btn.addEventListener('mousedown',   function () { startHold(btn); });
        btn.addEventListener('mouseup',     stopHold);
        btn.addEventListener('mouseleave',  stopHold);
        btn.addEventListener('touchstart',  function () { startHold(btn); }, { passive: true });
        btn.addEventListener('touchend',    stopHold);
        btn.addEventListener('touchcancel', stopHold);
    }

    function scan() {
        pd.querySelectorAll(
            '[data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"]'
        ).forEach(attach);
    }

    // Re-scan whenever Streamlit re-renders widgets into the DOM
    new MutationObserver(scan).observe(pd.body, { childList: true, subtree: true });
    scan();
})();
</script>
""", height=0)

# ─────────────────────────────────────────────
# TILE HELPERS
# ─────────────────────────────────────────────

ACCENT_COLORS = {
    "green":  ("#3D5A80", "rgba(61,90,128,0.08)"),
    "blue":   ("#3b82f6", "rgba(59,130,246,0.08)"),
    "amber":  ("#f59e0b", "rgba(245,158,11,0.08)"),
    "red":    ("#ef4444", "rgba(239,68,68,0.08)"),
    "purple": ("#8b5cf6", "rgba(139,92,246,0.08)"),
    "teal":   ("#06b6d4", "rgba(6,182,212,0.08)"),
}

def tile(label, value, delta=None, delta_positive=None, icon="", accent="green", small=False):
    color, glow = ACCENT_COLORS.get(accent, ACCENT_COLORS["green"])
    delta_html = ""
    if delta:
        if delta_positive is True:
            cls, arrow = "pos", "▲"
        elif delta_positive is False:
            cls, arrow = "neg", "▼"
        else:
            cls, arrow = "neu", "—"
        delta_html = f"<div class='tile-delta {cls}'>{arrow} {delta}</div>"
    val_cls = "tile-value tile-value-sm" if small else "tile-value"
    return (
        f"<div class='tile' style='--accent:{color};--accent-glow:{glow};'>"
        f"<div class='tile-icon'>{icon}</div>"
        f"<div class='{val_cls}'>{value}</div>"
        f"<div class='tile-label'>{label}</div>"
        f"{delta_html}"
        f"</div>"
    )

def tile_row(tiles):
    return st.markdown(f"<div class='tile-row'>{''.join(tiles)}</div>", unsafe_allow_html=True)

def section(label, icon=""):
    inner = f"<span class='sl-icon'>{icon}</span> {label}" if icon else label
    st.markdown(f"<div class='section-label'>{inner}</div>", unsafe_allow_html=True)

def insight(html):
    st.markdown(f'<div class="insight-box">{html}</div>', unsafe_allow_html=True)


def _img_b64(filename):
    # Loads image from /images folder and returns base64 string for embedding in HTML
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _svg(key, size=18):
    s = str(size)
    _p = {
        "house":      f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H4a1 1 0 01-1-1V9.5z"/><path d="M9 21V12h6v9"/></svg>',
        "person":     f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>',
        "bank":       f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><line x1="3" y1="21" x2="21" y2="21"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="5" y1="10" x2="5" y2="21"/><line x1="9" y1="10" x2="9" y2="21"/><line x1="15" y1="10" x2="15" y2="21"/><line x1="19" y1="10" x2="19" y2="21"/><path d="M12 3L3 10h18L12 3z"/></svg>',
        "chart-bar":  f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="12" width="4" height="9" rx="0.5"/><rect x="10" y="6" width="4" height="15" rx="0.5"/><rect x="17" y="3" width="4" height="18" rx="0.5"/></svg>',
        "chart-up":   f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "chart-down": f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>',
        "sliders":    f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/><circle cx="8" cy="6" r="2" fill="#FAF7F2"/><circle cx="16" cy="12" r="2" fill="#FAF7F2"/><circle cx="10" cy="18" r="2" fill="#FAF7F2"/></svg>',
        "lightning":  f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "scales":     f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="3" x2="12" y2="21"/><line x1="6" y1="21" x2="18" y2="21"/><line x1="12" y1="3" x2="3" y2="6"/><line x1="12" y1="3" x2="21" y2="6"/><path d="M3 6l3 8H0L3 6z"/><path d="M21 6l3 8h-6L21 6z"/></svg>',
        "trophy":     f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><path d="M17 4h2a2 2 0 010 4c0 2.5-2 4.5-4 5.5"/><path d="M7 4H5a2 2 0 000 4c0 2.5 2 4.5 4 5.5"/><rect x="7" y="4" width="10" height="9" rx="1"/></svg>',
        "clipboard":  f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><rect x="9" y="2" width="6" height="4" rx="1"/><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><line x1="8" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="13" y2="15"/></svg>',
        "gear":       f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
        "card":       f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
        "coins":      f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><circle cx="8" cy="8" r="6"/><path d="M18.09 10A6 6 0 0122 16a6 6 0 01-6 6c-2.3 0-4.3-1.3-5.4-3.2"/></svg>',
        "receipt":    f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1z"/><line x1="8" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="13" y2="14"/></svg>',
        "building":   f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><rect x="2" y="7" width="20" height="15"/><path d="M2 7l10-5 10 5"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="8" y1="7" x2="8" y2="22"/><line x1="16" y1="7" x2="16" y2="22"/></svg>',
        "gem":        f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9z"/><path d="M2 9h20"/><line x1="12" y1="22" x2="12" y2="9"/></svg>',
        "calendar":   f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        "scissors":   f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
        "clock":      f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "heart":      f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>',
        "pin":        f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>',
        "wrench":     f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>',
        "document":   f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="12" y2="17"/></svg>',
        "calculator": f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><rect x="4" y="2" width="16" height="20" rx="2"/><rect x="7" y="5" width="10" height="4" rx="0.5"/><circle cx="8.5" cy="14" r="1" fill="#3D5A80"/><circle cx="12" cy="14" r="1" fill="#3D5A80"/><circle cx="15.5" cy="14" r="1" fill="#3D5A80"/><circle cx="8.5" cy="18" r="1" fill="#3D5A80"/><circle cx="12" cy="18" r="1" fill="#3D5A80"/><circle cx="15.5" cy="18" r="1" fill="#3D5A80"/></svg>',
        "compare":    f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><path d="M9 3H5a2 2 0 00-2 2v4"/><path d="M9 3h10a2 2 0 012 2v4"/><path d="M9 3v18"/><path d="M3 9h18"/><path d="M3 9v10a2 2 0 002 2h4"/><path d="M21 9v10a2 2 0 01-2 2h-4"/></svg>',
        "piggybank":  f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#3D5A80" stroke-width="1.5" stroke-linecap="round"><path d="M19 12a7 7 0 10-14 0c0 2 .8 3.8 2 5.1V19a2 2 0 002 2h6a2 2 0 002-2v-1.9A7 7 0 0019 12z"/><path d="M19 12h2a1 1 0 010 2h-2"/><path d="M12 6V4"/><circle cx="9.5" cy="11.5" r="0.5" fill="#3D5A80"/></svg>',
    }
    return _p.get(key, "")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    _house_b64 = _img_b64("house.jpg")
    st.markdown(f"""
    <div class="sidebar-logo">
        <img src="data:image/jpeg;base64,{_house_b64}" class="sidebar-banner" alt="House">
    </div>
    <p class="sidebar-tagline">Navigate your next property move</p>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "Navigate",
        ["Property Analyser", "Mortgage Calculator", "Yield Calculator", "Compare Properties"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<p style='font-size:0.6rem;color:#9CA3AF;letter-spacing:0.18em;text-transform:uppercase;font-family:Space Grotesk,sans-serif;font-weight:700;'>DISCLAIMER</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.72rem;color:#6B7280;line-height:1.6;'>Figures are indicative only and do not constitute financial or tax advice. Consult a qualified adviser.</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────

COLORS = {
    "gold":         "#3D5A80",
    "gold_light":   "#6A8FAF",
    "dark":         "#1A1A2E",
    "parchment":    "#F5F5F5",
    "parchment_mid":"#FAFAFA",
    "border":       "#E5E7EB",
    "green":        "#3D5A80",
    "red":          "#ef4444",
    "blue":         "#3b82f6",
    "text_muted":   "#6B7280",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FDFAF7",
    font=dict(family="Inter", color="#374151", size=12),
    margin=dict(l=20, r=20, t=55, b=60),
)

STAMP_DUTY = {
    "NSW": [(0,14000,0,1.25),(14000,32000,175,1.50),(32000,85000,445,1.75),(85000,319000,1372,3.50),(319000,1064000,9618,4.50),(1064000,3131000,43231,5.50),(3131000,float("inf"),157581,7.00)],
    "VIC": [(0,25000,0,1.40),(25000,130000,350,2.40),(130000,960000,2870,6.00),(960000,float("inf"),52670,6.50)],
    "QLD": [(0,5000,0,0.00),(5000,75000,0,1.50),(75000,540000,1050,3.50),(540000,1000000,17325,4.50),(1000000,float("inf"),38025,5.75)],
    "WA":  [(0,120000,0,1.90),(120000,150000,2280,2.85),(150000,360000,3135,3.80),(360000,725000,11115,4.75),(725000,float("inf"),28453,5.15)],
    "SA":  [(0,12000,0,1.00),(12000,30000,120,2.00),(30000,50000,480,3.00),(50000,100000,1080,3.50),(100000,200000,2830,4.00),(200000,250000,6830,4.25),(250000,300000,8955,4.75),(300000,500000,11330,5.00),(500000,float("inf"),21330,5.50)],
    "TAS": [(0,3000,50,0.00),(3000,25000,50,1.75),(25000,75000,435,2.25),(75000,200000,1560,3.50),(200000,375000,5935,4.00),(375000,725000,12935,4.25),(725000,float("inf"),27810,4.50)],
    "ACT": [(0,260000,0,0.60),(260000,300000,1560,2.20),(300000,500000,2440,3.40),(500000,750000,9240,4.32),(750000,1000000,20040,5.90),(1000000,1455000,34790,6.40),(1455000,float("inf"),63910,6.90)],
    "NT":  [(0,525000,0,None),(525000,float("inf"),0,4.95)],
}

def calc_stamp_duty(price, state):
    if state == "NT":
        if price <= 525000:
            v = price / 1000
            return round((0.06571441 * v * v) + 15 * v)
        return round((price - 525000) * 4.95 / 100)
    for low, high, base, rate in STAMP_DUTY[state]:
        if low <= price < high:
            return round(base + (price - low) * rate / 100)
    return 0

def calc_monthly_payment(loan, annual_rate, years):
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return loan / n
    return loan * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def build_amortization(loan, annual_rate, years, extra_monthly=0):
    r = annual_rate / 100 / 12
    base_payment = calc_monthly_payment(loan, annual_rate, years)
    payment = base_payment + extra_monthly
    balance = loan
    rows = []
    month = 0
    while balance > 0.01 and month < years * 12:
        month += 1
        interest = balance * r
        principal = min(payment - interest, balance)
        balance = max(0, balance - principal)
        rows.append({"Month": month, "Year": math.ceil(month / 12),
                     "Payment": principal + interest, "Principal": principal,
                     "Interest": interest, "Balance": balance})
    return pd.DataFrame(rows)

def build_amortization_io(loan, annual_rate, io_years, total_years, extra_monthly=0):
    r = annual_rate / 100 / 12
    rows = []
    balance = loan
    for month in range(1, io_years * 12 + 1):
        interest = balance * r
        rows.append({"Month": month, "Year": math.ceil(month / 12),
                     "Payment": interest, "Principal": 0.0,
                     "Interest": interest, "Balance": balance, "Phase": "Interest Only"})
    remaining_years = total_years - io_years
    if remaining_years > 0 and balance > 0:
        pi_payment = calc_monthly_payment(balance, annual_rate, remaining_years) + extra_monthly
        for i in range(1, remaining_years * 12 + 1):
            month = io_years * 12 + i
            interest = balance * r
            principal = min(pi_payment - interest, balance)
            balance = max(0, balance - principal)
            rows.append({"Month": month, "Year": math.ceil(month / 12),
                         "Payment": principal + interest, "Principal": principal,
                         "Interest": interest, "Balance": balance, "Phase": "Principal & Interest"})
            if balance <= 0.01:
                break
    return pd.DataFrame(rows)

MARGINAL_RATES = {
    "Individual":      [(0,18200,0.0),(18200,45000,0.19),(45000,120000,0.325),(120000,180000,0.37),(180000,float("inf"),0.45)],
    "SMSF":            [(0,float("inf"),0.15)],
    "Company / Trust": [(0,float("inf"),0.30)],
}

def marginal_rate(entity, income):
    for low, high, rate in MARGINAL_RATES[entity]:
        if low <= income < high:
            return rate
    return 0.45

def calc_depreciation(build_cost, plant_cost, method, years=40):
    rows = []
    dv_balance = plant_cost
    for yr in range(1, years + 1):
        if method == "Diminishing Value":
            plant_dep = dv_balance * 0.2
            dv_balance = max(0, dv_balance - plant_dep)
        else:
            plant_dep = plant_cost / 25 if yr <= 25 else 0
        rows.append({"Year": yr, "Building": build_cost / 40, "Plant": plant_dep,
                     "Total": build_cost / 40 + plant_dep})
    return pd.DataFrame(rows)

def calc_cgt(purchase_price, sale_price, purchase_costs, sale_costs, entity, held_over_12m):
    cost_base = purchase_price + purchase_costs + sale_costs
    gross_gain = sale_price - cost_base
    if gross_gain <= 0:
        return gross_gain, gross_gain, 0.0
    if entity == "Individual" and held_over_12m:
        return gross_gain, gross_gain * 0.5, gross_gain * 0.5
    elif entity == "SMSF" and held_over_12m:
        return gross_gain, gross_gain * (2/3), gross_gain / 3
    return gross_gain, gross_gain, 0.0

def fmt(n):  return f"${n:,.0f}"
def fmtp(n): return f"{n:.2f}%"

_today = _date.today().strftime("%d %B %Y").lstrip("0")

# ── Report Details session state ─────────────────────────────────────────────
if "rpt_prepared_for" not in st.session_state: st.session_state.rpt_prepared_for = ""
if "rpt_prepared_by"  not in st.session_state: st.session_state.rpt_prepared_by  = ""
if "rpt_date"         not in st.session_state: st.session_state.rpt_date         = _today
if "rpt_notes"        not in st.session_state: st.session_state.rpt_notes        = ""

# ── PDF generation ──────────────────────────────────────────────────────────

def _make_pdf(page_title, rows, today_str, report_details=None):
    """rows: list of ("label","value") tuples, or ("__section__","Section Name") for headings."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib import colors as C
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import ParagraphStyle
    except ImportError:
        raise RuntimeError("reportlab not installed — run: pip install reportlab")

    cream = C.HexColor("#F5F0E8"); navy = C.HexColor("#1A1A2E")
    slate = C.HexColor("#3D5A80"); grey = C.HexColor("#6B7280")
    light = C.HexColor("#EAE4DC"); faint = C.HexColor("#FAF7F2")

    def ps(name, font="Helvetica", size=9, color=navy, leading=14, **kw):
        return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color, leading=leading, **kw)

    brand_s   = ps("brand", font="Helvetica-Bold", size=8,  color=slate, leading=11)
    date_s    = ps("date",  size=8, color=grey, leading=11)
    title_s   = ps("title", font="Helvetica-Bold", size=20, color=navy,  leading=24)
    section_s = ps("sec",   font="Helvetica-Bold", size=7,  color=slate, leading=10, spaceAfter=1)
    label_s   = ps("lbl",   size=9,  color=grey, leading=13)
    value_s   = ps("val",   font="Helvetica-Bold", size=9, color=navy, leading=13)
    disc_s    = ps("disc",  size=7,  color=grey, leading=10)
    rd_key_s  = ps("rdkey", size=8,  color=grey, leading=12)
    rd_val_s  = ps("rdval", font="Helvetica-Bold", size=8, color=navy, leading=12)

    rd = report_details or {}
    hdr_date = rd.get("date") or today_str

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=22*mm, rightMargin=22*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    elems = []

    # Header bar
    hdr = Table([[Paragraph("Property Compass  ·  sextantdigital.com.au", brand_s),
                  Paragraph(hdr_date, date_s)]],
                colWidths=[120*mm, 46*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), cream),
        ("TOPPADDING",    (0,0),(-1,-1), 7), ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(0,-1),  10), ("RIGHTPADDING", (-1,0),(-1,-1), 10),
        ("ALIGN",         (1,0),(1,-1), "RIGHT"), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ROUNDEDCORNERS",[6]),
    ]))
    elems.append(hdr)

    # Report details block (prepared for / by / notes)
    _rd_rows = []
    if rd.get("prepared_for"): _rd_rows.append([Paragraph("Prepared for", rd_key_s), Paragraph(rd["prepared_for"], rd_val_s)])
    if rd.get("prepared_by"):  _rd_rows.append([Paragraph("Prepared by",  rd_key_s), Paragraph(rd["prepared_by"],  rd_val_s)])
    if rd.get("notes"):        _rd_rows.append([Paragraph("Notes",        rd_key_s), Paragraph(rd["notes"],        rd_key_s)])
    if _rd_rows:
        rd_tbl = Table(_rd_rows, colWidths=[32*mm, 134*mm])
        rd_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), faint),
            ("TOPPADDING",    (0,0),(-1,-1), 4), ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(0,-1),  10), ("RIGHTPADDING", (-1,0),(-1,-1), 10),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        elems += [Spacer(1, 3*mm), rd_tbl]

    elems += [Spacer(1, 5*mm), Paragraph(page_title, title_s),
              Spacer(1, 2*mm), HRFlowable(width="100%", thickness=1, color=light, spaceAfter=5*mm)]

    # Metric rows
    tbl_rows = []
    def _flush(tbl_rows):
        if not tbl_rows: return []
        t = Table(tbl_rows, colWidths=[90*mm, 76*mm])
        t.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0,0),(-1,-1), [C.white, faint]),
            ("TOPPADDING",     (0,0),(-1,-1), 6), ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",    (0,0),(0,-1),  2), ("RIGHTPADDING", (-1,0),(-1,-1), 2),
            ("ALIGN",          (1,0),(1,-1), "RIGHT"), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LINEBELOW",      (0,-1),(-1,-1), 0.4, light),
        ]))
        return [t]

    for item in rows:
        if item[0] == "__section__":
            elems += _flush(tbl_rows); tbl_rows = []
            elems += [Spacer(1, 4*mm), Paragraph(item[1].upper(), section_s),
                      HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=2*mm)]
        else:
            tbl_rows.append([Paragraph(item[0], label_s), Paragraph(item[1], value_s)])
    elems += _flush(tbl_rows)

    # Disclaimer
    elems += [Spacer(1, 8*mm), HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=3*mm),
              Paragraph("Figures are indicative only and do not constitute financial or tax advice. "
                        "Consult a qualified adviser.", disc_s)]
    doc.build(elems)
    buf.seek(0)
    return buf.read()


def _make_compare_pdf(results, metrics, today_str, report_details=None):
    """Side-by-side PDF for Compare Properties."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib import colors as C
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.styles import ParagraphStyle
    except ImportError:
        raise RuntimeError("reportlab not installed — run: pip install reportlab")

    cream = C.HexColor("#F5F0E8"); navy = C.HexColor("#1A1A2E")
    slate = C.HexColor("#3D5A80"); grey = C.HexColor("#6B7280")
    light = C.HexColor("#EAE4DC"); faint = C.HexColor("#FAF7F2")
    gold  = C.HexColor("#B45309")

    def ps(name, font="Helvetica", size=9, color=navy, leading=14, **kw):
        return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color, leading=leading, **kw)

    brand_s  = ps("brand", font="Helvetica-Bold", size=8,  color=slate, leading=11)
    date_s   = ps("date",  size=8, color=grey, leading=11)
    title_s  = ps("title", font="Helvetica-Bold", size=20, color=navy,  leading=24)
    hdr_s    = ps("hdr",   font="Helvetica-Bold", size=9,  color=slate, leading=12)
    met_s    = ps("met",   size=8,  color=grey, leading=12)
    val_s    = ps("val",   font="Helvetica-Bold", size=8,  color=navy,  leading=12)
    win_s    = ps("win",   font="Helvetica-Bold", size=8,  color=slate, leading=12)
    disc_s   = ps("disc",  size=7,  color=grey, leading=10)
    rd_key_s = ps("rdkey", size=8,  color=grey, leading=12)
    rd_val_s = ps("rdval", font="Helvetica-Bold", size=8, color=navy, leading=12)

    rd = report_details or {}
    hdr_date = rd.get("date") or today_str

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    elems = []

    # Header
    hdr = Table([[Paragraph("Property Compass  ·  sextantdigital.com.au", brand_s),
                  Paragraph(hdr_date, date_s)]],
                colWidths=[120*mm, 46*mm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),cream), ("ROUNDEDCORNERS",[6]),
        ("TOPPADDING",(0,0),(-1,-1),7),     ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(0,-1),10),    ("RIGHTPADDING",(-1,0),(-1,-1),10),
        ("ALIGN",(1,0),(1,-1),"RIGHT"),     ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    elems.append(hdr)

    # Report details block (prepared for / by / notes)
    _rd_rows = []
    if rd.get("prepared_for"): _rd_rows.append([Paragraph("Prepared for", rd_key_s), Paragraph(rd["prepared_for"], rd_val_s)])
    if rd.get("prepared_by"):  _rd_rows.append([Paragraph("Prepared by",  rd_key_s), Paragraph(rd["prepared_by"],  rd_val_s)])
    if rd.get("notes"):        _rd_rows.append([Paragraph("Notes",        rd_key_s), Paragraph(rd["notes"],        rd_key_s)])
    if _rd_rows:
        rd_tbl = Table(_rd_rows, colWidths=[32*mm, 138*mm])
        rd_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), faint),
            ("TOPPADDING",    (0,0),(-1,-1), 4), ("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(0,-1),  10), ("RIGHTPADDING", (-1,0),(-1,-1), 10),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        elems += [Spacer(1, 3*mm), rd_tbl]

    elems += [Spacer(1,5*mm), Paragraph("Compare Properties", title_s),
              Spacer(1,2*mm), HRFlowable(width="100%",thickness=1,color=light,spaceAfter=5*mm)]

    # Determine winners
    def winner_idx(vals, higher_is_better):
        best = max(vals) if higher_is_better else min(vals)
        return [i for i, v in enumerate(vals) if v == best]

    col_w = [52*mm, 43*mm, 43*mm, 43*mm]

    # Table header row
    tbl = [[Paragraph("Metric", met_s)] + [Paragraph(r["name"], hdr_s) for r in results]]
    bg_row = [cream, cream, cream, cream]

    for idx, (label, key, higher_better, fmt_fn) in enumerate(metrics):
        vals = [r[key] for r in results]
        winners = winner_idx(vals, higher_better)
        bg = C.white if idx % 2 == 0 else faint
        row = [Paragraph(label, met_s)]
        for i, r in enumerate(results):
            style = win_s if i in winners else val_s
            prefix = "★ " if i in winners else ""
            row.append(Paragraph(f"{prefix}{fmt_fn(r[key])}", style))
        tbl.append(row)

    t = Table(tbl, colWidths=col_w)
    row_bgs = [cream] + [C.white if i % 2 == 0 else faint for i in range(len(metrics))]
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS",  (0,0), (-1,-1), row_bgs),
        ("TOPPADDING",      (0,0), (-1,-1), 6),  ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",     (0,0), (-1,-1), 4),  ("RIGHTPADDING", (0,0),(-1,-1),4),
        ("ALIGN",           (1,0), (-1,-1), "RIGHT"),
        ("VALIGN",          (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",       (0,0), (-1,0),  1, slate),
        ("FONTNAME",        (0,0), (-1,0),  "Helvetica-Bold"),
    ]))
    elems.append(t)

    # Winner highlights
    elems += [Spacer(1,6*mm), HRFlowable(width="100%",thickness=0.5,color=light,spaceAfter=3*mm)]
    best_yield_i  = winner_idx([r["net_yield"]      for r in results], True)[0]
    best_cf_i     = winner_idx([r["cashflow_post"]  for r in results], True)[0]
    lowest_rep_i  = winner_idx([r["monthly"]        for r in results], False)[0]

    highlights = [
        [Paragraph("Best Net Yield",       ps("h1",font="Helvetica-Bold",size=8,color=slate,leading=11)),
         Paragraph(results[best_yield_i]["name"], ps("h2",font="Helvetica-Bold",size=9,color=navy,leading=12)),
         Paragraph(fmtp(results[best_yield_i]["net_yield"]), ps("h3",font="Helvetica-Bold",size=9,color=slate,leading=12))],
        [Paragraph("Best After-Tax Cashflow", ps("h4",font="Helvetica-Bold",size=8,color=slate,leading=11)),
         Paragraph(results[best_cf_i]["name"],  ps("h5",font="Helvetica-Bold",size=9,color=navy,leading=12)),
         Paragraph(fmt(results[best_cf_i]["cashflow_post"]) + "/yr", ps("h6",font="Helvetica-Bold",size=9,color=slate,leading=12))],
        [Paragraph("Lowest Repayment",     ps("h7",font="Helvetica-Bold",size=8,color=slate,leading=11)),
         Paragraph(results[lowest_rep_i]["name"], ps("h8",font="Helvetica-Bold",size=9,color=navy,leading=12)),
         Paragraph(fmt(results[lowest_rep_i]["monthly"]) + "/mo", ps("h9",font="Helvetica-Bold",size=9,color=slate,leading=12))],
    ]
    ht = Table(highlights, colWidths=[58*mm, 60*mm, 57*mm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), cream),
        ("TOPPADDING",    (0,0),(-1,-1), 7), ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",   (0,0),(-1,-1), 8), ("RIGHTPADDING", (0,0),(-1,-1),8),
        ("ALIGN",         (2,0),(2,-1),  "RIGHT"), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LINEBELOW",     (0,0),(-1,-2), 0.4, light),
    ]))
    elems.append(ht)

    elems += [Spacer(1,8*mm), HRFlowable(width="100%",thickness=0.5,color=light,spaceAfter=3*mm),
              Paragraph("Figures are indicative only and do not constitute financial or tax advice. "
                        "Consult a qualified adviser.", disc_s)]
    doc.build(elems)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────

def _chart_layout(**kw):
    d = dict(**PLOTLY_LAYOUT)
    d.update(kw)
    return d

def chart_principal_interest(loan, annual_rate, years):
    df = build_amortization(loan, annual_rate, years)
    annual = df.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Principal", x=annual["Year"], y=annual["Principal"],
                         marker_color="#3D5A80", marker_line_width=0))
    fig.add_trace(go.Bar(name="Interest", x=annual["Year"], y=annual["Interest"],
                         marker_color="#B0C4D8", marker_line_width=0))
    fig.update_layout(**_chart_layout(
        barmode="stack",
        title=dict(text="Annual Principal vs Interest", font=dict(size=14, color="#3D5A80", family="Inter")),
        legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
        xaxis_title="Year", yaxis_title="Amount ($)",
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
    ))
    return fig

def chart_balance_over_time(loan, annual_rate, years, extra=0):
    df_base = build_amortization(loan, annual_rate, years)
    annual_base = df_base.groupby("Year")["Balance"].last().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=annual_base["Year"], y=annual_base["Balance"], name="Standard",
                             line=dict(color="#B0C4D8", width=2), fill="tozeroy",
                             fillcolor="rgba(61,90,128,0.06)"))
    if extra > 0:
        df_extra = build_amortization(loan, annual_rate, years, extra_monthly=extra)
        annual_extra = df_extra.groupby("Year")["Balance"].last().reset_index()
        fig.add_trace(go.Scatter(x=annual_extra["Year"], y=annual_extra["Balance"],
                                 name=f"+{fmt(extra)}/mo extra",
                                 line=dict(color="#3D5A80", width=2.5), fill="tozeroy",
                                 fillcolor="rgba(61,90,128,0.10)"))
    fig.update_layout(**_chart_layout(
        title=dict(text="Loan Balance Over Time", font=dict(size=14, color="#3D5A80", family="Inter")),
        xaxis_title="Year", yaxis_title="Balance ($)",
        legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
    ))
    return fig

def chart_cashflow(annual_rent, annual_interest, annual_expenses, dep_df, marg_rate_val, years=10):
    cashflows_pre, cashflows_post = [], []
    for yr in range(1, years + 1):
        dep = dep_df.iloc[yr-1]["Total"] if yr <= len(dep_df) else 0
        pre = annual_rent - annual_interest - annual_expenses
        taxable = pre - dep
        benefit = abs(min(0, taxable)) * marg_rate_val
        cashflows_pre.append(pre)
        cashflows_post.append(pre + benefit)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, years+1)), y=cashflows_pre, name="Pre-tax cashflow",
                             line=dict(color="#9CA3AF", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=list(range(1, years+1)), y=cashflows_post, name="After-tax cashflow",
                             line=dict(color="#3D5A80", width=2.5), fill="tozeroy",
                             fillcolor="rgba(61,90,128,0.08)"))
    fig.add_hline(y=0, line_dash="solid", line_color="#ef4444", line_width=1, opacity=0.4)
    fig.update_layout(**_chart_layout(
        title=dict(text="10-Year Cashflow Estimate (based on your inputs)", font=dict(size=14, color="#3D5A80", family="Inter")),
        xaxis_title="Year", yaxis_title="Cashflow ($)",
        legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)", dtick=1),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
    ))
    return fig

def chart_payoff_comparison(loan, annual_rate, years, extra_amounts):
    fig = go.Figure()
    colors_list = ["#9CA3AF", "#6A8FAF", "#3D5A80", "#2D4A70", "#1D3A60"]
    for i, extra in enumerate(extra_amounts):
        df = build_amortization(loan, annual_rate, years, extra_monthly=extra)
        annual = df.groupby("Year")["Balance"].last().reset_index()
        label = "Standard" if extra == 0 else f"+{fmt(extra)}/mo"
        fig.add_trace(go.Scatter(x=annual["Year"], y=annual["Balance"], name=label,
                                 line=dict(color=colors_list[i % len(colors_list)], width=2.5)))
    fig.update_layout(**_chart_layout(
        title=dict(text="Loan Payoff Comparison", font=dict(size=14, color="#3D5A80", family="Inter")),
        xaxis_title="Year", yaxis_title="Balance ($)",
        legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
    ))
    return fig


# ─────────────────────────────────────────────
# PAGE: PROPERTY ANALYZER
# ─────────────────────────────────────────────

if page == "Property Analyser":
    _piggybank = _img_b64("piggybank.jpg")
    st.markdown(f"""
    <div class="page-header" style="display:block;padding:0 0 0.5rem;border-bottom:1px solid #E8E2D9;margin-top:-1.2rem;">
        <div class="page-hero-banner">
            <img src="data:image/jpeg;base64,{_piggybank}" alt="Property Investment" class="hero-top">
            <div class="page-hero-overlay">
                <h1>Property Analyser</h1>
                <p class="sub">Property investment analysis — cashflow · stamp duty · depreciation · CGT · capital growth · break-even</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Report Details ──
    st.markdown('<div class="report-details-wrap"><div class="report-details-title">Report Details</div></div>', unsafe_allow_html=True)
    _rd1, _rd2, _rd3 = st.columns([2, 2, 1])
    with _rd1:
        st.text_input("Prepared for", key="rpt_prepared_for")
    with _rd2:
        st.text_input("Prepared by", key="rpt_prepared_by")
    with _rd3:
        st.text_input("Date", key="rpt_date")
    st.text_area("Notes", placeholder="Any additional notes for this report...", key="rpt_notes", height=70, label_visibility="visible")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        section("Investor Details", _svg("person"))
        entity = st.selectbox("Entity type", ["Individual", "SMSF", "Company / Trust"])
        state  = st.selectbox("State", ["QLD", "NSW", "VIC", "WA", "SA", "TAS", "ACT", "NT"])
        other_income = st.number_input("Other annual income ($)", min_value=0.0, value=80000.0, step=1000.0,
                                       help="Salary / other income — used to estimate marginal tax rate")

        section("Property Details", _svg("house"))
        purchase_price  = st.number_input("Purchase price ($)", min_value=1.0, value=500000.0, step=1000.0)
        weekly_rent     = st.number_input("Weekly rent ($)", min_value=0.0, value=500.0, step=10.0)
        vacancy_rate    = st.number_input("Vacancy rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.5)

        section("Loan Details", _svg("bank"))
        loan_amount   = st.number_input("Loan amount ($)", min_value=0.0, value=400000.0, step=1000.0)
        interest_rate = st.number_input("Interest rate (%)", min_value=0.0, value=6.0, step=0.1)
        loan_term     = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30)
        io_enabled_pa = st.radio("Loan type", ["Principal & Interest", "Interest Only"], horizontal=True, key="io_pa") == "Interest Only"
        io_years_pa   = 0
        if io_enabled_pa:
            io_years_pa = st.number_input("Interest-only period (years)", min_value=1,
                                          max_value=int(loan_term) - 1, value=min(5, int(loan_term) - 1), key="io_yrs_pa")

    with col2:
        section("Annual Expenses", _svg("coins"))
        exp_council   = st.number_input("Council Rates ($)",          min_value=0.0, value=1500.0, step=50.0,             key="pa_exp_council")
        exp_insurance = st.number_input("Landlord Insurance ($)",     min_value=0.0, value=1200.0, step=50.0,             key="pa_exp_insurance")
        exp_water     = st.number_input("Water ($)",                  min_value=0.0, value=600.0,  step=50.0,             key="pa_exp_water")
        pa_pm_pct     = st.number_input("Property Management (%)",    min_value=0.0, max_value=20.0, value=8.0, step=0.5, key="pa_exp_pm_pct")
        exp_pm        = (pa_pm_pct / 100) * (weekly_rent * 52)
        st.caption(f"Calculated: ${exp_pm:,.0f}/yr")
        exp_bc        = st.number_input("Body Corporate ($)",         min_value=0.0, value=0.0,    step=100.0,            key="pa_exp_bc")
        exp_maint     = st.number_input("Maintenance & Repairs ($)",  min_value=0.0, value=800.0,  step=50.0,             key="pa_exp_maint")
        exp_other_lbl = st.text_input("Other description", value="", placeholder="e.g. Pest inspection",                 key="pa_exp_other_lbl")
        exp_other     = st.number_input("Other ($)",                  min_value=0.0, value=0.0,    step=50.0,             key="pa_exp_other")
        annual_expenses = exp_council + exp_insurance + exp_water + exp_pm + exp_bc + exp_maint + exp_other
        st.markdown(f"<p style='font-size:0.8rem;font-weight:600;color:#3D5A80;margin:0.4rem 0 0.8rem;'>Total: ${annual_expenses:,.0f}/yr</p>", unsafe_allow_html=True)

        section("Depreciation", _svg("chart-down"))
        build_cost  = st.number_input("Construction / build cost ($)", min_value=0.0, value=200000.0, step=1000.0)
        plant_cost  = st.number_input("Plant & equipment value ($)", min_value=0.0, value=20000.0, step=500.0)
        dep_method  = st.selectbox("Depreciation method", ["Diminishing Value", "Prime Cost"])

    st.divider()

    # ── Calculations ──
    annual_rent_gross  = weekly_rent * 52
    annual_rent        = annual_rent_gross * (1 - vacancy_rate / 100)
    gross_yield        = (annual_rent_gross / purchase_price) * 100
    net_yield          = ((annual_rent - annual_expenses) / purchase_price) * 100
    monthly_repayment  = calc_monthly_payment(loan_amount, interest_rate, int(loan_term))
    if io_enabled_pa and io_years_pa > 0:
        monthly_repayment = loan_amount * (interest_rate / 100) / 12
    annual_interest    = loan_amount * (interest_rate / 100)
    dep_df             = calc_depreciation(build_cost, plant_cost, dep_method)
    year1_dep          = dep_df.iloc[0]["Total"]
    stamp_duty         = calc_stamp_duty(purchase_price, state)
    equity             = purchase_price - loan_amount
    lvr                = (loan_amount / purchase_price) * 100 if purchase_price > 0 else 0
    cashflow_pretax    = annual_rent - annual_interest - annual_expenses
    taxable_prop       = annual_rent - annual_interest - annual_expenses - year1_dep
    marg               = marginal_rate(entity, other_income)
    tax_benefit        = abs(min(0, taxable_prop)) * marg if taxable_prop < 0 else 0
    cashflow_aftertax  = cashflow_pretax + tax_benefit
    cash_on_cash       = (cashflow_aftertax / equity * 100) if equity > 0 else 0

    # ── Key Metric Tiles ──
    section("Key Metrics", _svg("chart-bar"))
    cf_pos = cashflow_pretax >= 0
    tile_row([
        tile("Gross Yield",         fmtp(gross_yield),        icon=_svg("chart-up"), accent="green"),
        tile("Net Yield",           fmtp(net_yield),           icon=_svg("chart-bar"), accent="teal"),
        tile("Monthly Repayment",   fmt(monthly_repayment),    icon=_svg("card"), accent="blue"),
        tile("Cashflow (pre-tax)",  f"{fmt(cashflow_pretax)}/yr",
             delta="Positive" if cf_pos else "Negative",
             delta_positive=cf_pos, icon=_svg("coins"), accent="green" if cf_pos else "red"),
        tile("Cashflow (after-tax)", f"{fmt(cashflow_aftertax)}/yr", icon=_svg("receipt"), accent="green"),
        tile("Stamp Duty",          fmt(stamp_duty),            icon=_svg("building"), accent="amber"),
        tile("LVR",                 fmtp(lvr),                 icon=_svg("scales"), accent="purple"),
        tile("Equity",              fmt(equity),               icon=_svg("house"), accent="teal"),
    ])

    # ── Charts ──
    st.divider()
    section("Visualisations", _svg("chart-bar"))
    tab1, tab2, tab3 = st.tabs(["Cashflow Projection", "Principal vs Interest", "Loan Balance"])
    with tab1:
        st.plotly_chart(chart_cashflow(annual_rent, annual_interest, annual_expenses, dep_df, marg), use_container_width=True)
        st.caption("Estimates use your entered rent, expenses and interest rate held constant. Actual cashflow will vary with market conditions, rate changes and vacancy.")
    with tab2:
        st.plotly_chart(chart_principal_interest(loan_amount, interest_rate, int(loan_term)), use_container_width=True)
    with tab3:
        st.plotly_chart(chart_balance_over_time(loan_amount, interest_rate, int(loan_term)), use_container_width=True)

    # ── Expanders ──
    with st.expander("Full Cashflow Breakdown"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Income**")
            st.markdown(f"<span style='color:#4B5563;'>Gross annual rent: {fmt(annual_rent_gross)}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#4B5563;'>Less vacancy ({vacancy_rate:.1f}%): ({fmt(annual_rent_gross - annual_rent)})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#4B5563;'><strong style='color:#1A1A2E;'>Effective annual rent: {fmt(annual_rent)}</strong></span>", unsafe_allow_html=True)
        with col2:
            st.markdown("**Costs**")
            st.markdown(f"<span style='color:#4B5563;'>Annual interest: ({fmt(annual_interest)})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#4B5563;'>Annual expenses: ({fmt(annual_expenses)})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#4B5563;'>Year 1 depreciation: ({fmt(year1_dep)})</span>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<span style='color:#4B5563;'>Taxable property income: <strong style='color:#1A1A2E;'>{fmt(taxable_prop)}</strong></span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#4B5563;'>Marginal tax rate ({entity}): <strong style='color:#1A1A2E;'>{marg*100:.0f}%</strong></span>", unsafe_allow_html=True)
        if tax_benefit > 0:
            insight(f"<strong>Negative gearing benefit: {fmt(tax_benefit)}/yr</strong><br><span>At your marginal rate of {marg*100:.0f}%, the ATO effectively subsidises your shortfall.</span>")
        st.markdown(f"<p style='color:#1A1A2E;font-weight:700;'>After-tax cashflow (Year 1): {fmt(cashflow_aftertax)}/yr ({fmt(cashflow_aftertax/52)}/wk)</p>", unsafe_allow_html=True)

    with st.expander(f"Stamp Duty — {state}"):
        tile_row([tile("Stamp Duty Payable", fmt(stamp_duty), icon=_svg("building"), accent="amber")])
        total_upfront = stamp_duty + equity
        st.markdown(f"<span style='color:#4B5563;'>Deposit: {fmt(equity)}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#4B5563;'><strong style='color:#1A1A2E;'>Total upfront cash required: {fmt(total_upfront)}</strong></span>", unsafe_allow_html=True)
        st.caption("Indicative only — confirm with your conveyancer.")

    with st.expander("Break-Even Rent Finder"):
        st.markdown("""
        <div class="help-wrap">
            <span class="help-icon">?</span>
            <div class="help-tip">
                Break-even rent is the minimum weekly rent needed to cover your property costs.<br><br>
                Pre-tax: The rent needed to cover your costs before any tax considerations.<br><br>
                After-tax: If your property costs more than it earns, that loss reduces your taxable income — meaning the ATO taxes you less. This effectively lowers your real break-even point.<br><br>
                The gap between the two figures shows how much your tax position improves your cashflow as a property investor.<br><br>
                Always speak to your accountant for advice tailored to your situation.
            </div>
        </div>
        """, unsafe_allow_html=True)
        breakeven_weekly     = (annual_interest + annual_expenses) / 52
        breakeven_aftertax   = ((annual_interest + annual_expenses - year1_dep) * (1 - marg) + year1_dep * (1 - marg)) / 52
        surplus              = weekly_rent - breakeven_weekly
        tile_row([
            tile("Break-even (pre-tax)",   f"{fmt(breakeven_weekly)}/wk",   icon=_svg("scales"), accent="amber"),
            tile("Break-even (after-tax)", f"{fmt(breakeven_aftertax)}/wk", icon=_svg("receipt"), accent="teal"),
        ])
        insight(f"<strong>Current rent vs break-even: {surplus:+,.0f}/wk {'above' if surplus >= 0 else 'below'}</strong><br>"
                f"{'You are covering your costs from rent alone.' if surplus >= 0 else 'You need to top up from other income to cover costs.'}")

    with st.expander("Depreciation Schedule"):
        display_dep = dep_df[dep_df["Year"] <= 25].copy()
        for _c in ["Building", "Plant", "Total"]:
            display_dep[_c] = display_dep[_c].apply(lambda x: f"${x:,.0f}")
        st.table(display_dep.set_index("Year"))

    # with st.expander("📅 Amortization Schedule"):
    #     if io_enabled_pa and io_years_pa > 0:
    #         amort_df = build_amortization_io(loan_amount, interest_rate, int(io_years_pa), int(loan_term))
    #         st.info(f"Showing interest-only for years 1–{io_years_pa}, then P&I for years {io_years_pa+1}–{int(loan_term)}.")
    #     else:
    #         amort_df = build_amortization(loan_amount, interest_rate, int(loan_term))
    #     annual_summary = amort_df.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum"), Balance=("Balance","last")).reset_index()
    #     for col in ["Principal", "Interest", "Balance"]:
    #         annual_summary[col] = annual_summary[col].map("${:,.0f}".format)
    #     st.dataframe(annual_summary.set_index("Year"), use_container_width=True)
    #     st.markdown(f"<span style='color:#4B5563;'>Total interest over {int(loan_term)} years: <strong style='color:#1A1A2E;'>{fmt(amort_df['Interest'].sum())}</strong></span>", unsafe_allow_html=True)

    with st.expander("CGT Estimator"):
        col1, col2, col3 = st.columns(3)
        with col1:
            sale_price = st.number_input("Expected sale price ($)", min_value=0.0,
                                         value=float(round(purchase_price * 1.3 / 1000) * 1000), step=10000.0)
        with col2:
            purchase_costs_cgt = st.number_input("Purchase costs ($)", min_value=0.0, value=float(stamp_duty), step=500.0)
        with col3:
            sale_costs_cgt = st.number_input("Sale costs ($)", min_value=0.0, value=15000.0, step=500.0)
        held = st.toggle("Held 12+ months (CGT discount eligible)", value=True)
        gross_gain, taxable_gain, discount = calc_cgt(purchase_price, sale_price, purchase_costs_cgt, sale_costs_cgt, entity, held)
        if gross_gain <= 0:
            st.warning(f"Capital loss of {fmt(abs(gross_gain))} — no CGT payable.")
        else:
            est_rate = marginal_rate(entity, other_income + taxable_gain)
            est_tax  = taxable_gain * est_rate
            tile_row([
                tile("Gross Gain",    fmt(gross_gain),                                    icon=_svg("chart-up"), accent="green"),
                tile("CGT Discount",  fmt(discount) if discount > 0 else "None",          icon=_svg("scissors"), accent="teal"),
                tile("Taxable Gain",  fmt(taxable_gain),                                  icon=_svg("receipt"), accent="amber"),
                tile("Estimated CGT", fmt(est_tax),                                       icon=_svg("building"), accent="red"),
            ])

    with st.expander("Capital Growth Projector"):
        st.markdown("Estimate how your property value and equity could grow over time.")
        col1, col2 = st.columns(2)
        with col1:
            cg_rate  = st.number_input("Annual growth rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5, key="cg_rate_pa")
        with col2:
            cg_years = st.number_input("Projection (years)", min_value=1, max_value=30, value=5, key="cg_years_pa")

        cg_data  = []
        cg_amort = build_amortization(loan_amount, interest_rate, int(loan_term))
        for yr in range(0, int(cg_years) + 1):
            proj_value   = purchase_price * ((1 + cg_rate / 100) ** yr)
            loan_balance = cg_amort[cg_amort["Year"] == yr]["Balance"].iloc[-1] if yr > 0 and yr <= len(cg_amort.groupby("Year")) else loan_amount
            proj_equity  = proj_value - loan_balance
            cg_data.append({"Year": yr, "Property Value": proj_value, "Equity": proj_equity, "Loan Balance": loan_balance})
        cg_df = pd.DataFrame(cg_data)

        final          = cg_df.iloc[-1]
        initial_equity = purchase_price - loan_amount
        tile_row([
            tile(f"Value in {int(cg_years)} years", fmt(final["Property Value"]),
                 delta=fmt(final["Property Value"] - purchase_price) + " gain", delta_positive=True, icon=_svg("house"), accent="green"),
            tile("Projected Equity", fmt(final["Equity"]),
                 delta=fmt(final["Equity"] - initial_equity) + " growth", delta_positive=True, icon=_svg("gem"), accent="teal"),
            tile("Total Return", fmtp(((final["Property Value"] - purchase_price) / purchase_price) * 100), icon=_svg("chart-up"), accent="blue"),
        ])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cg_df["Year"], y=cg_df["Property Value"], name="Property Value",
                                 line=dict(color="#3D5A80", width=2.5), fill="tozeroy", fillcolor="rgba(61,90,128,0.06)"))
        fig.add_trace(go.Scatter(x=cg_df["Year"], y=cg_df["Equity"], name="Your Equity",
                                 line=dict(color="#6A8FAF", width=2, dash="dot")))
        fig.add_trace(go.Scatter(x=cg_df["Year"], y=cg_df["Loan Balance"], name="Loan Balance",
                                 line=dict(color="#9CA3AF", width=1.5)))
        fig.update_layout(**_chart_layout(
            title=dict(text="Property Value & Equity Projection", font=dict(size=14, color="#3D5A80", family="Inter")),
            legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
            xaxis_title="Year", yaxis_title="Value ($)",
            xaxis=dict(gridcolor="rgba(0,0,0,0.06)", dtick=1),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.warning("Capital growth projections are estimates only. Past growth does not guarantee future performance.")

    # ── Save as PDF ──
    st.divider()
    _pdf_rows_pa = [
        ("__section__", "Property Details"),
        ("Purchase Price", fmt(purchase_price)),
        ("State", state),
        ("Weekly Rent", fmt(weekly_rent)),
        ("__section__", "Key Results"),
        ("Gross Yield",            fmtp(gross_yield)),
        ("Net Yield",              fmtp(net_yield)),
        ("Monthly Repayment",      fmt(monthly_repayment)),
        ("Cashflow (pre-tax)",     f"{fmt(cashflow_pretax)}/yr"),
        ("Cashflow (after-tax)",   f"{fmt(cashflow_aftertax)}/yr"),
        ("__section__", "Upfront Costs"),
        ("Stamp Duty",             fmt(stamp_duty)),
        ("LVR",                    fmtp(lvr)),
        ("__section__", "Break-Even Rent"),
        ("Break-even (pre-tax)",   f"{fmt(breakeven_weekly)}/wk"),
        ("Break-even (after-tax)", f"{fmt(breakeven_aftertax)}/wk"),
    ]
    _rpt_details = {"prepared_for": st.session_state.rpt_prepared_for, "prepared_by": st.session_state.rpt_prepared_by,
                    "date": st.session_state.rpt_date, "notes": st.session_state.rpt_notes}
    try:
        _pdf_bytes_pa = _make_pdf("Property Analyser", _pdf_rows_pa, _today, _rpt_details)
        st.download_button("Save as PDF", data=_pdf_bytes_pa, file_name="property_analysis.pdf", mime="application/pdf")
    except RuntimeError as e:
        st.warning(str(e))


# ─────────────────────────────────────────────
# PAGE: MORTGAGE CALCULATOR
# ─────────────────────────────────────────────

elif page == "Mortgage Calculator":
    _coins = _img_b64("coins.jpg")
    st.markdown(f"""
    <div class="page-header" style="display:block;padding:0 0 1.25rem;border-bottom:1px solid #E8E2D9;">
        <div class="page-hero-banner">
            <img src="data:image/jpeg;base64,{_coins}" alt="Mortgage">
            <div class="page-hero-overlay">
                <h1>Mortgage Calculator</h1>
                <p class="sub">Repayments · pay off sooner analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section("Loan Parameters", _svg("bank"))
    col1, col2, col3 = st.columns(3)
    with col1:
        loan_amount   = st.number_input("Loan amount ($)", value=500000.0, step=1000.0)
    with col2:
        interest_rate = st.number_input("Interest rate (%)", value=6.0, step=0.1)
    with col3:
        loan_term     = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30)
    col1, col2 = st.columns(2)
    with col1:
        io_enabled = st.radio("Loan type", ["Principal & Interest", "Interest Only"], horizontal=True) == "Interest Only"
    with col2:
        io_years = 0
        if io_enabled:
            io_years = st.number_input("Interest-only period (years)", min_value=1,
                                       max_value=int(loan_term) - 1, value=min(5, int(loan_term) - 1))

    if loan_amount > 0 and interest_rate >= 0 and loan_term > 0:
        if io_enabled and io_years > 0:
            amort_df_full   = build_amortization_io(loan_amount, interest_rate, int(io_years), int(loan_term))
            io_monthly      = loan_amount * (interest_rate / 100) / 12
            pi_years        = int(loan_term) - int(io_years)
            pi_monthly      = calc_monthly_payment(loan_amount, interest_rate, pi_years)
            total_interest  = amort_df_full["Interest"].sum()
            total_paid      = amort_df_full["Payment"].sum()
            pi_only_df      = build_amortization(loan_amount, interest_rate, int(loan_term))
            pi_total_int    = pi_only_df["Interest"].sum()
            extra_interest  = total_interest - pi_total_int

            tile_row([
                tile(f"IO Repayment (first {io_years}y)", fmt(io_monthly),          icon=_svg("card"),      accent="blue"),
                tile("IO Fortnightly",                    fmt(io_monthly*12/26),    icon=_svg("calendar"),  accent="purple"),
                tile(f"P&I Repayment (after IO)",         fmt(pi_monthly),          icon=_svg("card"),      accent="green"),
                tile("Total Interest",                    fmt(total_interest),      icon=_svg("chart-bar"), accent="amber"),
                tile("Extra Interest vs P&I",             fmt(extra_interest),      icon=_svg("lightning"), accent="red"),
            ])
            insight(f"<strong>Interest-only for {io_years} years costs an extra {fmt(extra_interest)} in total interest</strong> compared to a standard P&I loan.<br>"
                    f"Your repayments jump from {fmt(io_monthly)}/mo to {fmt(pi_monthly)}/mo when the IO period ends — plan for this.")
        else:
            monthly        = calc_monthly_payment(loan_amount, interest_rate, int(loan_term))
            total_paid     = monthly * int(loan_term) * 12
            total_interest = total_paid - loan_amount
            amort_df_full  = build_amortization(loan_amount, interest_rate, int(loan_term))

            tile_row([
                tile("Monthly Repayment",     fmt(monthly),           icon=_svg("card"),      accent="green"),
                tile("Fortnightly Repayment", fmt(monthly*12/26),     icon=_svg("calendar"),  accent="purple"),
                tile("Weekly Repayment",      fmt(monthly*12/52),     icon=_svg("calendar"),  accent="teal"),
                tile("Total Interest",        fmt(total_interest),    icon=_svg("chart-bar"), accent="amber"),
                tile("Total Paid",            fmt(total_paid),        icon=_svg("coins"),     accent="blue"),
            ])

        tab1, tab2 = st.tabs(["Principal vs Interest", "Loan Balance"])
        with tab1:
            annual = amort_df_full.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum")).reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Principal", x=annual["Year"], y=annual["Principal"],
                                 marker_color="#3D5A80", marker_line_width=0))
            fig.add_trace(go.Bar(name="Interest",  x=annual["Year"], y=annual["Interest"],
                                 marker_color="#B0C4D8", marker_line_width=0))
            if io_enabled and io_years > 0:
                fig.add_vline(x=io_years + 0.5, line_dash="dash", line_color="#ef4444",
                              annotation_text="IO → P&I", annotation_position="top")
            fig.update_layout(**_chart_layout(
                barmode="stack",
                title=dict(text="Annual Principal vs Interest", font=dict(size=14, color="#3D5A80", family="Inter")),
                legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
                xaxis_title="Year", yaxis_title="Amount ($)",
                xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
                yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
            ))
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            annual_bal = amort_df_full.groupby("Year")["Balance"].last().reset_index()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=annual_bal["Year"], y=annual_bal["Balance"], name="Balance",
                                      line=dict(color="#3D5A80", width=2.5), fill="tozeroy",
                                      fillcolor="rgba(61,90,128,0.10)"))
            if io_enabled and io_years > 0:
                fig2.add_vline(x=io_years + 0.5, line_dash="dash", line_color="#ef4444",
                               annotation_text="IO → P&I", annotation_position="top")
            fig2.update_layout(**_chart_layout(
                title=dict(text="Loan Balance Over Time", font=dict(size=14, color="#3D5A80", family="Inter")),
                legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
                xaxis_title="Year", yaxis_title="Balance ($)",
                xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
                yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
            ))
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        section("Pay Off Sooner", _svg("lightning"))
        st.markdown("<p style='color:#6B7280;font-size:0.85rem;margin-bottom:1rem;'>See how much time and interest you save by making extra repayments.</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            extra_monthly = st.number_input("Extra monthly repayment ($)", min_value=0.0, value=500.0, step=100.0)
        with col2:
            extra_lump    = st.number_input("One-off lump sum ($)", min_value=0.0, value=0.0, step=1000.0,
                                            help="Applied immediately to the principal")

        months_saved = 0; interest_saved = 0; years_saved = 0; mo_saved = 0; extra_months = 0
        effective_loan = loan_amount - extra_lump
        if effective_loan < 0:
            st.warning("Lump sum exceeds loan amount.")
        else:
            if io_enabled and io_years > 0:
                df_standard = build_amortization_io(loan_amount,     interest_rate, int(io_years), int(loan_term), extra_monthly=0)
                df_extra    = build_amortization_io(effective_loan,  interest_rate, int(io_years), int(loan_term), extra_monthly=extra_monthly)
            else:
                df_standard = build_amortization(loan_amount,    interest_rate, int(loan_term), extra_monthly=0)
                df_extra    = build_amortization(effective_loan, interest_rate, int(loan_term), extra_monthly=extra_monthly)

            standard_months  = len(df_standard)
            extra_months     = len(df_extra)
            months_saved     = standard_months - extra_months
            years_saved      = months_saved // 12
            mo_saved         = months_saved % 12
            interest_standard = df_standard["Interest"].sum()
            interest_extra    = df_extra["Interest"].sum()
            interest_saved    = interest_standard - interest_extra

            tile_row([
                tile("New Payoff Time",  f"{extra_months//12}y {extra_months%12}m",
                     delta=f"{years_saved}y {mo_saved}m sooner" if months_saved > 0 else "No change",
                     delta_positive=months_saved > 0, icon=_svg("clock"), accent="green"),
                tile("Interest Saved",   fmt(interest_saved),                                icon=_svg("heart"), accent="teal"),
                tile("Total Extra Paid", fmt(extra_monthly * extra_months + extra_lump),     icon=_svg("card"), accent="blue"),
            ])

            extra_scenarios = sorted(set([0, int(extra_monthly), int(extra_monthly * 2)]))
            st.plotly_chart(chart_payoff_comparison(effective_loan, interest_rate, int(loan_term), extra_scenarios), use_container_width=True)

            if interest_saved > 0:
                insight(f"<strong>By paying an extra {fmt(extra_monthly)}/month"
                        f"{f' plus a {fmt(extra_lump)} lump sum' if extra_lump > 0 else ''}, "
                        f"you save {fmt(interest_saved)} in interest and pay off {years_saved} year{'s' if years_saved != 1 else ''} "
                        f"{mo_saved} month{'s' if mo_saved != 1 else ''} sooner.</strong><br>"
                        f"Your effective return on those extra payments is equivalent to earning {interest_rate:.2f}% guaranteed.")

        # with st.expander("📅 Full Amortization Schedule"):
        #     annual_summary = amort_df_full.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum"), Balance=("Balance","last")).reset_index()
        #     for col in ["Principal", "Interest", "Balance"]:
        #         annual_summary[col] = annual_summary[col].map("${:,.0f}".format)
        #     st.dataframe(annual_summary.set_index("Year"), use_container_width=True)
        #     st.markdown(f"<span style='color:#4B5563;'>Total interest over loan term: <strong style='color:#1A1A2E;'>{fmt(amort_df_full['Interest'].sum())}</strong></span>", unsafe_allow_html=True)

        # ── Save as PDF ──
        st.divider()
        if io_enabled and io_years > 0:
            _pdf_rows_mc = [
                ("__section__", "Loan Details"),
                ("Loan Amount", fmt(loan_amount)),
                ("Interest Rate", fmtp(interest_rate)),
                ("Loan Term", f"{int(loan_term)} years"),
                ("__section__", "Repayments (Interest Only)"),
                ("IO Monthly Repayment", fmt(io_monthly)),
                ("P&I Repayment (after IO)", fmt(pi_monthly)),
                ("Total Interest", fmt(total_interest)),
                ("Total Amount Paid", fmt(total_paid)),
            ]
        else:
            _pdf_rows_mc = [
                ("__section__", "Loan Details"),
                ("Loan Amount", fmt(loan_amount)),
                ("Interest Rate", fmtp(interest_rate)),
                ("Loan Term", f"{int(loan_term)} years"),
                ("__section__", "Repayments"),
                ("Monthly Repayment", fmt(monthly)),
                ("Weekly Repayment", fmt(monthly * 12 / 52)),
                ("Total Interest", fmt(total_interest)),
                ("Total Amount Paid", fmt(total_paid)),
            ]
        if months_saved > 0:
            _pdf_rows_mc += [
                ("__section__", "Pay Off Sooner"),
                ("Time Saved", f"{years_saved}y {mo_saved}m"),
                ("Interest Saved", fmt(interest_saved)),
                ("New Payoff Time", f"{extra_months//12}y {extra_months%12}m"),
            ]
        _rpt_details = {"prepared_for": st.session_state.rpt_prepared_for, "prepared_by": st.session_state.rpt_prepared_by,
                        "date": st.session_state.rpt_date, "notes": st.session_state.rpt_notes}
        try:
            _pdf_bytes_mc = _make_pdf("Mortgage Calculator", _pdf_rows_mc, _today, _rpt_details)
            st.download_button("Save as PDF", data=_pdf_bytes_mc, file_name="mortgage_summary.pdf", mime="application/pdf")
        except RuntimeError as e:
            st.warning(str(e))
    else:
        st.info("Enter loan details above to see results.")


# ─────────────────────────────────────────────
# PAGE: YIELD CALCULATOR
# ─────────────────────────────────────────────

elif page == "Yield Calculator":
    _room = _img_b64("room.jpg")
    st.markdown(f"""
    <div class="page-header" style="display:block;padding:0 0 1.25rem;border-bottom:1px solid #E8E2D9;">
        <div class="page-hero-banner">
            <img src="data:image/jpeg;base64,{_room}" alt="Property interior">
            <div class="page-hero-overlay">
                <h1>Yield Calculator</h1>
                <p class="sub">Gross and net rental yield analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section("Property & Rent", _svg("house"))
    col1, col2 = st.columns(2)
    with col1:
        purchase_price  = st.number_input("Purchase price ($)", value=500000.0, step=1000.0)
        weekly_rent     = st.number_input("Weekly rent ($)", value=500.0, step=10.0)
    with col2:
        vacancy_rate    = st.number_input("Vacancy rate (%)", value=4.0, step=0.5)
        annual_expenses = st.number_input("Annual expenses ($)", value=5000.0, step=100.0,
                                          help="Include all ongoing property costs such as council rates, landlord insurance, property management fees, maintenance and repairs.")

    section("Mortgage (optional)", _svg("bank"))
    col1, col2, col3 = st.columns(3)
    with col1:
        yld_loan = st.number_input("Loan amount ($)", value=400000.0, step=1000.0, key="yld_loan")
    with col2:
        yld_rate = st.number_input("Interest rate (%)", value=6.0, step=0.1, key="yld_rate")
    with col3:
        yld_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30, key="yld_term")
    col1, col2 = st.columns(2)
    with col1:
        yld_io_enabled = st.radio("Loan type", ["Principal & Interest", "Interest Only"], horizontal=True, key="yld_io") == "Interest Only"
    with col2:
        yld_io_years = 0
        if yld_io_enabled:
            yld_io_years = st.number_input("Interest-only period (years)", min_value=1,
                                           max_value=int(yld_term) - 1, value=min(5, int(yld_term) - 1), key="yld_io_yrs")

    if purchase_price > 0:
        annual_rent_gross   = weekly_rent * 52
        annual_rent_net     = annual_rent_gross * (1 - vacancy_rate / 100)
        gross_yield         = (annual_rent_gross / purchase_price) * 100
        net_yield           = ((annual_rent_net - annual_expenses) / purchase_price) * 100
        if yld_io_enabled and yld_io_years > 0:
            yld_monthly = yld_loan * (yld_rate / 100) / 12   # interest-only repayment
        else:
            yld_monthly = calc_monthly_payment(yld_loan, yld_rate, int(yld_term))
        yld_weekly          = yld_monthly * 12 / 52
        net_weekly_cashflow = (annual_rent_net - annual_expenses - yld_monthly * 12) / 52
        cf_pos              = net_weekly_cashflow >= 0

        tile_row([
            tile("Gross Yield",            fmtp(gross_yield),        icon=_svg("chart-up"), accent="green"),
            tile("Net Yield",              fmtp(net_yield),           icon=_svg("chart-bar"), accent="teal"),
            tile("Monthly Repayment",      fmt(yld_monthly),          icon=_svg("card"), accent="blue"),
            tile("Weekly Repayment",       fmt(yld_weekly),           icon=_svg("calendar"), accent="purple"),
            tile("Annual Rent (gross)",    fmt(annual_rent_gross),    icon=_svg("coins"), accent="green"),
            tile("Annual Rent (effective)", fmt(annual_rent_net),     icon=_svg("house"), accent="teal"),
            tile("Net Weekly Cashflow",    f"{fmt(net_weekly_cashflow)}/wk",
                 delta="Positive" if cf_pos else "Negative",
                 delta_positive=cf_pos, icon=_svg("lightning"), accent="green" if cf_pos else "red"),
        ])

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=net_yield,
            delta={"reference": 5, "valueformat": ".2f", "suffix": "%"},
            title={"text": "Net Yield", "font": {"family": "Inter", "size": 16, "color": "#6B7280"}},
            number={"suffix": "%", "valueformat": ".2f", "font": {"color": "#1A1A2E", "size": 36}},
            gauge={
                "axis": {"range": [0, 12], "tickformat": ".0f", "ticksuffix": "%",
                         "tickcolor": "#9CA3AF", "tickwidth": 1},
                "bar": {"color": "#3D5A80"},
                "bgcolor": "#F5F0E8",
                "bordercolor": "#EAE4DC",
                "steps": [
                    {"range": [0,   3.5], "color": "rgba(239,68,68,0.08)"},
                    {"range": [3.5, 5.0], "color": "rgba(245,158,11,0.08)"},
                    {"range": [5.0, 12],  "color": "rgba(61,90,128,0.10)"},
                ],
                "threshold": {"line": {"color": "#3D5A80", "width": 2}, "thickness": 0.75, "value": 5},
            }
        ))
        fig.update_layout(**_chart_layout(height=280))
        st.plotly_chart(fig, use_container_width=True)

        if net_yield >= 5:
            st.success("Strong yield — this property is performing above the 5% benchmark.")
        elif net_yield >= 3.5:
            st.info("Moderate yield — acceptable but monitor expenses to improve returns.")
        else:
            st.error("Low yield — consider price negotiation or increasing rent.")

        with st.expander("Break-Even Rent"):
            st.markdown("""
            <div class="help-wrap">
                <span class="help-icon">?</span>
                <div class="help-tip">
                    Break-even rent is the minimum weekly rent needed to cover your property costs.<br><br>
                    Pre-tax: The rent needed to cover your costs before any tax considerations.<br><br>
                    After-tax: If your property costs more than it earns, that loss reduces your taxable income — meaning the ATO taxes you less. This effectively lowers your real break-even point.<br><br>
                    The gap between the two figures shows how much your tax position improves your cashflow as a property investor.<br><br>
                    Always speak to your accountant for advice tailored to your situation.
                </div>
            </div>
            """, unsafe_allow_html=True)
            breakeven = annual_expenses / 52
            surplus   = weekly_rent - breakeven
            tile_row([tile("Break-even weekly rent (expenses only)", f"{fmt(breakeven)}/wk", icon=_svg("scales"), accent="amber")])
            st.markdown(f"<span style='color:#4B5563;'>Your rent vs break-even: <strong style='color:#1A1A2E;'>{surplus:+,.0f}/wk</strong> {'above' if surplus >= 0 else 'below'}</span>", unsafe_allow_html=True)

        # ── Save as PDF ──
        st.divider()
        _pdf_rows_yc = [
            ("__section__", "Property Details"),
            ("Purchase Price", fmt(purchase_price)),
            ("Weekly Rent", fmt(weekly_rent)),
            ("__section__", "Yield"),
            ("Gross Yield", fmtp(gross_yield)),
            ("Net Yield", fmtp(net_yield)),
            ("__section__", "Repayments"),
            ("Monthly Repayment", fmt(yld_monthly)),
            ("Weekly Repayment", fmt(yld_weekly)),
            ("__section__", "Cashflow"),
            ("Net Weekly Cashflow", f"{fmt(net_weekly_cashflow)}/wk"),
            ("Annual Gross Rent", fmt(annual_rent_gross)),
            ("Annual Effective Rent", fmt(annual_rent_net)),
            ("__section__", "Break-Even"),
            ("Break-Even Weekly Rent", f"{fmt(breakeven)}/wk"),
        ]
        _rpt_details = {"prepared_for": st.session_state.rpt_prepared_for, "prepared_by": st.session_state.rpt_prepared_by,
                        "date": st.session_state.rpt_date, "notes": st.session_state.rpt_notes}
        try:
            _pdf_bytes_yc = _make_pdf("Yield Calculator", _pdf_rows_yc, _today, _rpt_details)
            st.download_button("Save as PDF", data=_pdf_bytes_yc, file_name="yield_summary.pdf", mime="application/pdf")
        except RuntimeError as e:
            st.warning(str(e))


# ─────────────────────────────────────────────
# PAGE: COMPARE PROPERTIES
# ─────────────────────────────────────────────

elif page == "Compare Properties":
    _magnify = _img_b64("magnify.jpg")
    st.markdown(f"""
    <div class="page-header" style="display:block;padding:0 0 1.25rem;border-bottom:1px solid #E8E2D9;">
        <div class="page-hero-banner">
            <img src="data:image/jpeg;base64,{_magnify}" alt="Property comparison">
            <div class="page-hero-overlay">
                <h1>Compare Properties</h1>
                <p class="sub">Side-by-side analysis of up to 3 properties</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section("Shared Assumptions", _svg("gear"))
    col1, col2, col3 = st.columns(3)
    with col1:
        cmp_entity = st.selectbox("Entity type", ["Individual", "SMSF", "Company / Trust"], key="cmp_entity")
    with col2:
        cmp_state  = st.selectbox("State", ["QLD", "NSW", "VIC", "WA", "SA", "TAS", "ACT", "NT"], key="cmp_state")
    with col3:
        cmp_income = st.number_input("Other annual income ($)", min_value=0.0, value=80000.0, step=1000.0, key="cmp_income")

    st.divider()

    _img_a = _img_b64("house in hand.jpg")
    _img_b = _img_b64("house in hands.jpg")
    _img_c = _img_b64("house with love heart.jpg")
    _thumb_style = "width:60px;height:60px;min-width:60px;min-height:60px;max-width:60px;max-height:60px;object-fit:cover;border-radius:8px;flex-shrink:0;display:block;"
    _prop_icons = [
        f'<img src="data:image/jpeg;base64,{_img_a}" class="prop-thumb" style="{_thumb_style}" alt="Property A">',
        f'<img src="data:image/jpeg;base64,{_img_b}" class="prop-thumb" style="{_thumb_style}" alt="Property B">',
        f'<img src="data:image/jpeg;base64,{_img_c}" class="prop-thumb" style="{_thumb_style}" alt="Property C">',
    ]

    props = []
    cols  = st.columns(3)
    default_names    = ["Property A", "Property B", "Property C"]
    default_prices   = [500000.0, 650000.0, 450000.0]
    default_rents    = [500.0, 620.0, 440.0]
    default_loans    = [400000.0, 520000.0, 360000.0]
    default_rates    = [6.0, 6.0, 6.5]
    default_expenses = [5000.0, 6500.0, 4500.0]
    prop_accents     = ["green", "blue", "amber"]

    for i in range(3):
        if f"cmp_name_{i}" not in st.session_state:
            st.session_state[f"cmp_name_{i}"] = default_names[i]

    for i, col in enumerate(cols):
        with col:
            heading = st.session_state.get(f"cmp_name_{i}") or default_names[i]
            section(heading, _prop_icons[i])
            name     = st.text_input("Enter property address or nickname", placeholder="e.g. 123 Smith St", key=f"cmp_name_{i}")
            price    = st.number_input("Purchase price ($)", min_value=1.0, value=default_prices[i], step=1000.0, key=f"cmp_price_{i}")
            rent     = st.number_input("Weekly rent ($)", min_value=0.0, value=default_rents[i], step=10.0, key=f"cmp_rent_{i}")
            loan     = st.number_input("Loan amount ($)", min_value=0.0, value=default_loans[i], step=1000.0, key=f"cmp_loan_{i}")
            rate     = st.number_input("Interest rate (%)", min_value=0.0, value=default_rates[i], step=0.1, key=f"cmp_rate_{i}")
            st.markdown("<p style='font-size:0.68rem;font-weight:700;letter-spacing:0.12em;color:#9CA3AF;margin:1rem 0 0.4rem;font-family:Space Grotesk,sans-serif;'>ANNUAL EXPENSES</p>", unsafe_allow_html=True)
            cmp_council   = st.number_input("Council Rates ($)",         min_value=0.0, value=1500.0, step=50.0,             key=f"cmp_exp_council_{i}")
            cmp_insurance = st.number_input("Landlord Insurance ($)",    min_value=0.0, value=1200.0, step=50.0,             key=f"cmp_exp_ins_{i}")
            cmp_water     = st.number_input("Water ($)",                 min_value=0.0, value=600.0,  step=50.0,             key=f"cmp_exp_water_{i}")
            cmp_pm_pct    = st.number_input("Property Management (%)",   min_value=0.0, max_value=20.0, value=8.0, step=0.5, key=f"cmp_exp_pm_pct_{i}")
            cmp_pm        = (cmp_pm_pct / 100) * (rent * 52)
            st.caption(f"Calculated: ${cmp_pm:,.0f}/yr")
            cmp_bc        = st.number_input("Body Corporate ($)",        min_value=0.0, value=0.0,    step=100.0,            key=f"cmp_exp_bc_{i}")
            cmp_maint     = st.number_input("Maintenance & Repairs ($)", min_value=0.0, value=800.0,  step=50.0,             key=f"cmp_exp_maint_{i}")
            cmp_other_lbl = st.text_input("Other description", value="", placeholder="e.g. Pest inspection",                key=f"cmp_exp_other_lbl_{i}")
            cmp_other     = st.number_input("Other ($)",                 min_value=0.0, value=0.0,    step=50.0,             key=f"cmp_exp_other_{i}")
            expenses      = cmp_council + cmp_insurance + cmp_water + cmp_pm + cmp_bc + cmp_maint + cmp_other
            st.markdown(f"<p style='font-size:0.8rem;font-weight:600;color:#3D5A80;margin:0.4rem 0 0.2rem;'>Total: ${expenses:,.0f}/yr</p>", unsafe_allow_html=True)
            loan_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30, key=f"cmp_term_{i}")
            props.append({"name": name, "price": price, "rent": rent,
                          "loan": loan, "rate": rate, "expenses": expenses, "term": loan_term})

    st.divider()

    # ── Calculations ──
    results = []
    marg = marginal_rate(cmp_entity, cmp_income)
    for p in props:
        annual_rent    = p["rent"] * 52
        gross_yield    = (annual_rent / p["price"]) * 100
        net_yield      = ((annual_rent - p["expenses"]) / p["price"]) * 100
        annual_interest = p["loan"] * (p["rate"] / 100)
        monthly        = calc_monthly_payment(p["loan"], p["rate"], p["term"])
        equity         = p["price"] - p["loan"]
        lvr            = (p["loan"] / p["price"]) * 100
        cashflow_pre   = annual_rent - annual_interest - p["expenses"]
        tax_benefit    = abs(min(0, cashflow_pre)) * marg if cashflow_pre < 0 else 0
        cashflow_post  = cashflow_pre + tax_benefit
        stamp          = calc_stamp_duty(p["price"], cmp_state)
        results.append({"name": p["name"], "gross_yield": gross_yield, "net_yield": net_yield,
                        "cashflow_pre": cashflow_pre, "cashflow_post": cashflow_post,
                        "monthly": monthly, "fortnightly": monthly * 12 / 26, "weekly": monthly * 12 / 52,
                        "equity": equity, "lvr": lvr, "stamp": stamp, "price": p["price"]})

    def winner(vals, higher_is_better=True):
        best = max(vals) if higher_is_better else min(vals)
        return [i for i, v in enumerate(vals) if v == best]

    # ── Comparison table ──
    section("Results Comparison", _svg("clipboard"))
    metrics = [
        ("Gross Yield",         "gross_yield",    True,  lambda v: fmtp(v)),
        ("Net Yield",           "net_yield",       True,  lambda v: fmtp(v)),
        ("Cashflow (pre-tax)",  "cashflow_pre",    True,  lambda v: f"{fmt(v)}/yr"),
        ("Cashflow (after-tax)","cashflow_post",   True,  lambda v: f"{fmt(v)}/yr"),
        ("Monthly Repayment",   "monthly",         False, lambda v: fmt(v)),
        ("Fortnightly Repayment", "fortnightly",   False, lambda v: fmt(v)),
        ("Weekly Repayment",    "weekly",          False, lambda v: fmt(v)),
        ("Equity",              "equity",          True,  lambda v: fmt(v)),
        ("Stamp Duty",          "stamp",           False, lambda v: fmt(v)),
    ]

    header_cells = "<th style='text-align:left;padding:0.7rem 1rem;color:#9CA3AF;font-size:0.62rem;letter-spacing:0.14em;font-family:Space Grotesk,sans-serif;font-weight:700;border-bottom:1px solid #EAE4DC;'>METRIC</th>"
    for r in results:
        header_cells += f"<th style='text-align:right;padding:0.7rem 1rem;color:#3D5A80;font-size:0.88rem;font-weight:600;font-family:Inter,sans-serif;letter-spacing:-0.02em;border-bottom:1px solid #EAE4DC;'>{r['name']}</th>"

    body_rows = ""
    for idx, (label, key, higher_better, fmt_fn) in enumerate(metrics):
        vals    = [r[key] for r in results]
        winners = winner(vals, higher_better)
        bg      = "#FFFFFF" if idx % 2 == 0 else "#FAF7F2"
        row_html = f"<tr style='background:{bg};'>"
        row_html += f"<td style='padding:0.65rem 1rem;color:#6B7280;font-size:0.75rem;font-family:Inter,sans-serif;white-space:nowrap;font-weight:500;'>{label}</td>"
        for i, r in enumerate(results):
            is_win = i in winners
            color  = "#3D5A80" if is_win else "#9CA3AF"
            weight = "700" if is_win else "400"
            trophy = "★ " if is_win else ""
            row_html += f"<td style='text-align:right;padding:0.65rem 1rem;color:{color};font-size:0.82rem;font-weight:{weight};font-family:Space Grotesk,sans-serif;white-space:nowrap;'>{trophy}{fmt_fn(r[key])}</td>"
        row_html += "</tr>"
        body_rows += row_html

    st.markdown(f"""
    <div style='overflow-x:auto;border-radius:12px;border:1px solid #EAE4DC;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(61,90,128,0.06);'>
        <table style='width:100%;border-collapse:collapse;'>
            <thead><tr style='background:#F5F0E8;'>{header_cells}</tr></thead>
            <tbody>{body_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    section("Visual Comparison", _svg("chart-bar"))
    names  = [r["name"] for r in results]
    colors_cmp = ["#3D5A80", "#3b82f6", "#f59e0b"]

    tab1, tab2, tab3 = st.tabs(["Yield", "Cashflow", "LVR & Equity"])
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Gross Yield", x=names, y=[r["gross_yield"] for r in results],
                             marker_color="#3D5A80", marker_line_width=0))
        fig.add_trace(go.Bar(name="Net Yield",   x=names, y=[r["net_yield"]   for r in results],
                             marker_color="#B0C4D8", marker_line_width=0))
        fig.update_layout(**_chart_layout(
            barmode="group",
            title=dict(text="Gross vs Net Yield", font=dict(size=14, color="#3D5A80", family="Inter")),
            legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)", ticksuffix="%"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        ))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Pre-tax cashflow",  x=names, y=[r["cashflow_pre"]  for r in results],
                             marker_color="#B0C4D8", marker_line_width=0))
        fig.add_trace(go.Bar(name="After-tax cashflow", x=names, y=[r["cashflow_post"] for r in results],
                             marker_color="#3D5A80", marker_line_width=0))
        fig.add_hline(y=0, line_color="#ef4444", line_width=1, opacity=0.4)
        fig.update_layout(**_chart_layout(
            barmode="group",
            title=dict(text="Annual Cashflow Comparison", font=dict(size=14, color="#3D5A80", family="Inter")),
            legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        ))
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Equity", x=names, y=[r["equity"]           for r in results],
                             marker_color="#3D5A80", marker_line_width=0))
        fig.add_trace(go.Bar(name="Loan",   x=names, y=[r["price"] - r["equity"] for r in results],
                             marker_color="#B0C4D8", marker_line_width=0))
        fig.update_layout(**_chart_layout(
            barmode="stack",
            title=dict(text="Equity vs Loan", font=dict(size=14, color="#3D5A80", family="Inter")),
            legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        ))
        st.plotly_chart(fig, use_container_width=True)

    # ── Quick Summary winner tiles ──
    st.divider()
    section("Quick Summary", _svg("trophy"))
    best_yield      = results[winner([r["net_yield"]      for r in results])[0]]["name"]
    best_cashflow   = results[winner([r["cashflow_post"]  for r in results])[0]]["name"]
    best_repayment  = results[winner([r["monthly"]        for r in results], higher_is_better=False)[0]]["name"]

    _qs_data = [
        ("Best Net Yield",    fmtp(max(r["net_yield"]      for r in results)), best_yield,      _svg("chart-up"), "green"),
        ("Best Cashflow",     f"{fmt(max(r['cashflow_post'] for r in results))}/yr", best_cashflow, _svg("coins"),   "teal"),
        ("Lowest Repayment",  f"{fmt(min(r['monthly']       for r in results))}/mo", best_repayment, _svg("card"),   "blue"),
    ]
    _qs_tiles = []
    for _lbl, _val, _name, _icon, _acc in _qs_data:
        _c, _g = ACCENT_COLORS[_acc]
        _qs_tiles.append(
            f"<div class='tile' style='--accent:{_c};--accent-glow:{_g};'>"
            f"<div class='tile-icon'>{_icon}</div>"
            f"<div class='tile-value tile-value-sm'>{_val}</div>"
            f"<div class='tile-label'>{_lbl}</div>"
            f"<div style='font-size:0.8rem;color:{_c};font-weight:600;margin-top:0.35rem;font-family:Inter,sans-serif;'>{_name}</div>"
            f"</div>"
        )
    st.markdown(f"<div class='tile-row'>{''.join(_qs_tiles)}</div>", unsafe_allow_html=True)

    # ── Capital Growth Projector ──
    st.divider()
    section("Capital Growth Projector", _svg("chart-up"))
    col1, col2 = st.columns(2)
    with col1:
        cg_rate_cmp  = st.number_input("Annual growth rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5, key="cg_rate_cmp")
    with col2:
        cg_years_cmp = st.number_input("Projection (years)", min_value=1, max_value=30, value=5, key="cg_years_cmp")

    fig = go.Figure()
    for i, r in enumerate(results):
        vals = [r["price"] * ((1 + cg_rate_cmp / 100) ** yr) for yr in range(0, int(cg_years_cmp) + 1)]
        fig.add_trace(go.Scatter(
            x=list(range(0, int(cg_years_cmp) + 1)), y=vals,
            name=r["name"], line=dict(color=colors_cmp[i], width=2.5),
        ))
    fig.update_layout(**_chart_layout(
        title=dict(text="Projected Property Value", font=dict(size=14, color="#3D5A80", family="Inter")),
        legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#374151", size=12, family="Inter")),
        xaxis_title="Year", yaxis_title="Value ($)",
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)", dtick=1),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", tickprefix="$", tickformat=",.0f"),
    ))
    st.plotly_chart(fig, use_container_width=True)

    _cg_accents = ["green", "blue", "amber"]
    _cg_tiles = []
    for i, r in enumerate(results):
        proj_val = r["price"] * ((1 + cg_rate_cmp / 100) ** int(cg_years_cmp))
        gain     = proj_val - r["price"]
        _c, _g   = ACCENT_COLORS[_cg_accents[i]]
        _cg_tiles.append(
            f"<div class='tile' style='--accent:{_c};--accent-glow:{_g};'>"
            f"<div class='tile-icon'>{_svg('chart-up')}</div>"
            f"<div class='tile-value tile-value-sm'>{fmt(proj_val)}</div>"
            f"<div class='tile-label'>{r['name']}</div>"
            f"<div style='font-size:0.8rem;color:{_c};font-weight:600;margin-top:0.35rem;font-family:Inter,sans-serif;'>+{fmt(gain)} gain</div>"
            f"</div>"
        )
    st.markdown(f"<div class='tile-row'>{''.join(_cg_tiles)}</div>", unsafe_allow_html=True)

    st.warning("Capital growth projections are estimates only. Past growth does not guarantee future performance.")

    # ── Save as PDF ──
    st.divider()
    _cmp_metrics = [
        ("Gross Yield",          "gross_yield",  True,  lambda v: fmtp(v)),
        ("Net Yield",            "net_yield",    True,  lambda v: fmtp(v)),
        ("Cashflow (pre-tax)",   "cashflow_pre", True,  lambda v: f"{fmt(v)}/yr"),
        ("Cashflow (after-tax)", "cashflow_post",True,  lambda v: f"{fmt(v)}/yr"),
        ("Monthly Repayment",      "monthly",      False, lambda v: fmt(v)),
        ("Fortnightly Repayment",  "fortnightly",  False, lambda v: fmt(v)),
        ("Weekly Repayment",       "weekly",       False, lambda v: fmt(v)),
        ("Equity",                 "equity",       True,  lambda v: fmt(v)),
        ("Stamp Duty",             "stamp",        False, lambda v: fmt(v)),
    ]
    _rpt_details = {"prepared_for": st.session_state.rpt_prepared_for, "prepared_by": st.session_state.rpt_prepared_by,
                    "date": st.session_state.rpt_date, "notes": st.session_state.rpt_notes}
    try:
        _pdf_bytes_cmp = _make_compare_pdf(results, _cmp_metrics, _today, _rpt_details)
        st.download_button("Save as PDF", data=_pdf_bytes_cmp, file_name="property_comparison.pdf", mime="application/pdf")
    except RuntimeError as e:
        st.warning(str(e))
