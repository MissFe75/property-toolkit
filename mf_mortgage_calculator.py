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

# Dark charcoal + emerald green theme
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global background */
    .stApp { background-color: #0f1117; color: #e2e8f0; }
    [data-testid="stSidebar"] { background-color: #080b0f !important; border-right: 1px solid #1e2530 !important; }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #10b981 !important; }

    /* Main font */
    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    /* Headings */
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f1f5f9 !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }

    /* Main content text */
    p, label, .stMarkdown { color: #94a3b8 !important; font-family: 'Space Grotesk', sans-serif !important; }
    .stMarkdown p { font-family: 'Space Grotesk', sans-serif !important; }
    .stMarkdown strong { font-family: 'Space Grotesk', sans-serif !important; color: #f1f5f9 !important; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #161b27 !important;
        border: 1px solid #1e2d3d !important;
        border-top: 2px solid #10b981 !important;
        border-radius: 6px !important;
        padding: 0.75rem !important;
    }
    [data-testid="metric-container"] label { color: #64748b !important; font-size: 0.62rem !important; letter-spacing: 0.08em; text-transform: uppercase; font-family: 'JetBrains Mono', monospace !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; font-weight: 600 !important; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.58rem !important; }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: #161b27 !important; border-radius: 6px !important; padding: 4px !important; gap: 2px !important; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; color: #94a3b8 !important; border-radius: 4px !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 0.8rem !important; }
    .stTabs [aria-selected="true"] { background: #10b981 !important; color: #000000 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] p { color: #000000 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] * { color: #000000 !important; }

    /* Inputs */
    .stNumberInput input, .stSelectbox select {
        background: #161b27 !important;
        border: 1px solid #1e2d3d !important;
        border-radius: 4px !important;
        color: #f1f5f9 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
    }
    .stNumberInput input:focus { border-color: #10b981 !important; box-shadow: 0 0 0 2px rgba(16,185,129,0.2) !important; }
    .stNumberInput label, .stSelectbox label { color: #64748b !important; font-size: 0.72rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

    /* Toggle */
    .stToggle label { color: #e2e8f0 !important; font-size: 0.9rem !important; font-weight: 500 !important; }
    .stToggle [data-baseweb="toggle"] { transform: scale(1.2); }
    [data-testid="stToggle"] p { color: #e2e8f0 !important; font-size: 0.9rem !important; font-weight: 500 !important; font-family: 'Space Grotesk', sans-serif !important; }
    [data-testid="stRadio"] label { color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 0.85rem !important; }
    [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: #e2e8f0 !important; font-size: 0.85rem !important; }
    [data-baseweb="radio"] div { border-color: #10b981 !important; }
    [data-baseweb="radio"] [aria-checked="true"] div { background-color: #10b981 !important; border-color: #10b981 !important; }

    /* Buttons */
    .stButton > button {
        background: #10b981 !important;
        color: #080b0f !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
    }
    .stButton > button:hover { background: #059669 !important; }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #161b27 !important;
        border: 1px solid #1e2d3d !important;
        border-radius: 4px !important;
        color: #94a3b8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
    }
    .streamlit-expanderContent { background: #0f1117 !important; border: 1px solid #1e2d3d !important; border-top: none !important; }

    /* Divider */
    hr { border-color: #1e2d3d !important; }

    /* Success/error/info boxes */
    .stSuccess { background-color: rgba(16,185,129,0.1) !important; border-left-color: #10b981 !important; color: #6ee7b7 !important; }
    .stError { background-color: rgba(239,68,68,0.1) !important; border-left-color: #ef4444 !important; color: #fca5a5 !important; }
    .stInfo { background-color: rgba(59,130,246,0.1) !important; border-left-color: #3b82f6 !important; color: #93c5fd !important; }
    .stWarning { background-color: rgba(245,158,11,0.1) !important; border-left-color: #f59e0b !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] { border: 1px solid #1e2d3d !important; border-radius: 4px !important; }
    [data-testid="stDataFrame"] * { color: #94a3b8 !important; background-color: #161b27 !important; }

    /* Selectbox dropdown */
    [data-baseweb="select"] > div { background-color: #161b27 !important; border-color: #1e2d3d !important; color: #f1f5f9 !important; }

    /* Sidebar logo area */
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 1rem 1rem;
        border-bottom: 1px solid #1e2530;
        margin-bottom: 1rem;
    }
    .sidebar-logo h2 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #10b981 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        margin: 0.5rem 0 0.2rem !important;
    }
    .sidebar-logo p { color: #334155 !important; font-size: 0.82rem !important; letter-spacing: 0.1em; margin: 0; color: #64748b !important; }

    /* Page header banner */
    .page-header {
        background: linear-gradient(135deg, #0d1f17 0%, #0a1628 100%);
        border: 1px solid #1e2d3d;
        border-left: 6px solid #10b981;
        border-radius: 6px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
    }
    .page-header h1 { color: #f1f5f9 !important; margin: 0 !important; font-size: 2.2rem !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; letter-spacing: -0.03em !important; }
    .page-header p { color: #64748b !important; margin: 0.4rem 0 0 !important; font-size: 0.9rem !important; letter-spacing: 0.12em; text-transform: uppercase; font-family: 'Space Grotesk', sans-serif !important; }

    /* Section labels */
    .section-label {
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #10b981;
        font-weight: 600;
        margin-bottom: 0.75rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #1e2d3d;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Insight box */
    .insight-box {
        background: #0d1f17;
        border: 1px solid #1e3a2a;
        border-left: 3px solid #10b981;
        border-radius: 4px;
        padding: 0.9rem 1.25rem;
        margin: 0.75rem 0;
    }
    .insight-box strong { color: #6ee7b7; }
    .insight-box span { color: #475569; font-size: 0.82rem; }

    /* Number input arrows */
    .stNumberInput button { background: #1e2d3d !important; color: #94a3b8 !important; border: none !important; }
    .stNumberInput button:hover { background: #10b981 !important; color: #080b0f !important; }
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
        ["🏠 Property Analyzer", "📐 Mortgage Calculator", "📊 Yield Calculator", "⚖️ Compare Properties"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<p style='font-size:0.62rem;color:#1e2d3d;letter-spacing:0.15em;text-transform:uppercase;font-family:JetBrains Mono,monospace;'>DISCLAIMER</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem;color:#334155;'>Figures are indicative only and do not constitute financial or tax advice. Consult a qualified adviser.</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────

COLORS = {
    "gold": "#10b981",
    "gold_light": "#34d399",
    "dark": "#0f1117",
    "parchment": "#161b27",
    "parchment_mid": "#0d1520",
    "border": "#1e2d3d",
    "green": "#10b981",
    "red": "#ef4444",
    "blue": "#3b82f6",
    "text_muted": "#64748b",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#161b27",
    font=dict(family="Space Grotesk", color="#e2e8f0", size=13),
    margin=dict(l=20, r=20, t=60, b=60),
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
        rows.append({
            "Month": month,
            "Year": math.ceil(month / 12),
            "Payment": principal + interest,
            "Principal": principal,
            "Interest": interest,
            "Balance": balance,
        })
    return pd.DataFrame(rows)

def build_amortization_io(loan, annual_rate, io_years, total_years, extra_monthly=0):
    """Interest-only for io_years, then switches to P&I for remaining term."""
    r = annual_rate / 100 / 12
    rows = []
    balance = loan
    # Interest-only phase
    for month in range(1, io_years * 12 + 1):
        interest = balance * r
        rows.append({
            "Month": month,
            "Year": math.ceil(month / 12),
            "Payment": interest,
            "Principal": 0.0,
            "Interest": interest,
            "Balance": balance,
            "Phase": "Interest Only",
        })
    # P&I phase — recalculate repayment on remaining balance over remaining term
    remaining_years = total_years - io_years
    if remaining_years > 0 and balance > 0:
        pi_payment = calc_monthly_payment(balance, annual_rate, remaining_years) + extra_monthly
        for i in range(1, remaining_years * 12 + 1):
            month = io_years * 12 + i
            interest = balance * r
            principal = min(pi_payment - interest, balance)
            balance = max(0, balance - principal)
            rows.append({
                "Month": month,
                "Year": math.ceil(month / 12),
                "Payment": principal + interest,
                "Principal": principal,
                "Interest": interest,
                "Balance": balance,
                "Phase": "Principal & Interest",
            })
            if balance <= 0.01:
                break
    return pd.DataFrame(rows)

MARGINAL_RATES = {
    "Individual": [(0,18200,0.0),(18200,45000,0.19),(45000,120000,0.325),(120000,180000,0.37),(180000,float("inf"),0.45)],
    "SMSF": [(0,float("inf"),0.15)],
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
        rows.append({"Year": yr, "Building": build_cost / 40, "Plant": plant_dep, "Total": build_cost / 40 + plant_dep})
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

def fmt(n): return f"${n:,.0f}"
def fmtp(n): return f"{n:.2f}%"


# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────

def chart_principal_interest(loan, annual_rate, years):
    df = build_amortization(loan, annual_rate, years)
    annual = df.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Principal", x=annual["Year"], y=annual["Principal"],
                         marker_color=COLORS["gold"], marker_line_width=0))
    fig.add_trace(go.Bar(name="Interest", x=annual["Year"], y=annual["Interest"],
                         marker_color="#1e3a2a", marker_line_width=0))
    fig.update_layout(**PLOTLY_LAYOUT, barmode="stack", title=dict(text="Annual Principal vs Interest", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                      legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                      xaxis_title="Year", yaxis_title="Amount ($)",
                      xaxis=dict(gridcolor="#1e2d3d"), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
    return fig

def chart_balance_over_time(loan, annual_rate, years, extra=0):
    df_base = build_amortization(loan, annual_rate, years, extra_monthly=0)
    annual_base = df_base.groupby("Year")["Balance"].last().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=annual_base["Year"], y=annual_base["Balance"], name="Standard",
                             line=dict(color="#334155", width=2), fill="tozeroy",
                             fillcolor="rgba(16,185,129,0.05)"))
    if extra > 0:
        df_extra = build_amortization(loan, annual_rate, years, extra_monthly=extra)
        annual_extra = df_extra.groupby("Year")["Balance"].last().reset_index()
        fig.add_trace(go.Scatter(x=annual_extra["Year"], y=annual_extra["Balance"], name=f"+{fmt(extra)}/mo extra",
                                 line=dict(color=COLORS["gold"], width=2.5), fill="tozeroy",
                                 fillcolor="rgba(16,185,129,0.1)"))
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text="Loan Balance Over Time", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                      xaxis_title="Year", yaxis_title="Balance ($)",
                      legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                      xaxis=dict(gridcolor="#1e2d3d"), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
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
                             line=dict(color="#334155", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=list(range(1, years+1)), y=cashflows_post, name="After-tax cashflow",
                             line=dict(color=COLORS["gold"], width=2.5), fill="tozeroy",
                             fillcolor="rgba(16,185,129,0.08)"))
    fig.add_hline(y=0, line_dash="solid", line_color=COLORS["red"], line_width=1, opacity=0.5)
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text="Annual Cashflow (10-Year Projection)", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                      xaxis_title="Year", yaxis_title="Cashflow ($)",
                      legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                      xaxis=dict(gridcolor="#1e2d3d", dtick=1), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
    return fig

def chart_payoff_comparison(loan, annual_rate, years, extra_amounts):
    fig = go.Figure()
    colors_list = ["#d9cdb8", COLORS["gold_light"], COLORS["gold"], "#8a6020", COLORS["dark"]]
    for i, extra in enumerate(extra_amounts):
        df = build_amortization(loan, annual_rate, years, extra_monthly=extra)
        annual = df.groupby("Year")["Balance"].last().reset_index()
        label = "Standard" if extra == 0 else f"+{fmt(extra)}/mo"
        fig.add_trace(go.Scatter(x=annual["Year"], y=annual["Balance"], name=label,
                                 line=dict(color=colors_list[i % len(colors_list)], width=2)))
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text="Loan Payoff Comparison", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                      xaxis_title="Year", yaxis_title="Balance ($)",
                      legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                      xaxis=dict(gridcolor="#1e2d3d"), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
    return fig


# ─────────────────────────────────────────────
# PAGE: PROPERTY ANALYZER
# ─────────────────────────────────────────────

if page == "🏠 Property Analyzer":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>🏠 Property Analyzer</h1>
            <p>Full investment analysis — cashflow, stamp duty, depreciation, amortization & CGT</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Inputs ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label">Investor Details</div>', unsafe_allow_html=True)
        entity = st.selectbox("Entity type", ["Individual", "SMSF", "Company / Trust"])
        state = st.selectbox("State", ["QLD", "NSW", "VIC", "WA", "SA", "TAS", "ACT", "NT"])
        other_income = st.number_input("Other annual income ($)", min_value=0.0, value=80000.0, step=1000.0,
                                       help="Salary / other income — used to estimate marginal tax rate")
    with col2:
        st.markdown('<div class="section-label">Property Details</div>', unsafe_allow_html=True)
        purchase_price = st.number_input("Purchase price ($)", min_value=1.0, value=500000.0, step=1000.0)
        weekly_rent = st.number_input("Weekly rent ($)", min_value=0.0, value=500.0, step=10.0)
        vacancy_rate = st.number_input("Vacancy rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.5)
        annual_expenses = st.number_input("Annual expenses ($)", min_value=0.0, value=5000.0, step=100.0,
                                          help="Rates, insurance, maintenance, management fees")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label">Loan Details</div>', unsafe_allow_html=True)
        loan_amount = st.number_input("Loan amount ($)", min_value=0.0, value=400000.0, step=1000.0)
        interest_rate = st.number_input("Interest rate (%)", min_value=0.0, value=6.0, step=0.1)
        loan_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30)
        io_enabled_pa = st.radio("Loan type", ["Principal & Interest", "Interest Only"], horizontal=True, key="io_pa") == "Interest Only"
        io_years_pa = 0
        if io_enabled_pa:
            io_years_pa = st.number_input("Interest-only period (years)", min_value=1,
                                          max_value=int(loan_term) - 1, value=min(5, int(loan_term) - 1), key="io_yrs_pa")
    with col2:
        st.markdown('<div class="section-label">Depreciation</div>', unsafe_allow_html=True)
        build_cost = st.number_input("Construction / build cost ($)", min_value=0.0, value=200000.0, step=1000.0)
        plant_cost = st.number_input("Plant & equipment value ($)", min_value=0.0, value=20000.0, step=500.0)
        dep_method = st.selectbox("Depreciation method", ["Diminishing Value", "Prime Cost"])

    st.divider()

    # ── Calculations ──
    annual_rent_gross = weekly_rent * 52
    annual_rent = annual_rent_gross * (1 - vacancy_rate / 100)
    gross_yield = (annual_rent_gross / purchase_price) * 100
    net_yield = ((annual_rent - annual_expenses) / purchase_price) * 100
    monthly_repayment = calc_monthly_payment(loan_amount, interest_rate, int(loan_term))
    if io_enabled_pa and io_years_pa > 0:
        monthly_repayment = loan_amount * (interest_rate / 100) / 12  # show IO repayment as primary
    annual_interest = loan_amount * (interest_rate / 100)
    dep_df = calc_depreciation(build_cost, plant_cost, dep_method)
    year1_dep = dep_df.iloc[0]["Total"]
    stamp_duty = calc_stamp_duty(purchase_price, state)
    equity = purchase_price - loan_amount
    lvr = (loan_amount / purchase_price) * 100 if purchase_price > 0 else 0
    cashflow_pretax = annual_rent - annual_interest - annual_expenses
    taxable_prop = annual_rent - annual_interest - annual_expenses - year1_dep
    marg = marginal_rate(entity, other_income)
    tax_benefit = abs(min(0, taxable_prop)) * marg if taxable_prop < 0 else 0
    cashflow_aftertax = cashflow_pretax + tax_benefit
    cash_on_cash = (cashflow_aftertax / equity * 100) if equity > 0 else 0

    # ── Key Metrics ──
    st.markdown('<div class="section-label">Key Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Gross Yield", fmtp(gross_yield))
    c2.metric("Net Yield", fmtp(net_yield))
    cashflow_delta = "✅ Positive" if cashflow_pretax > 0 else ("❌ Negative" if cashflow_pretax < 0 else "😌 Neutral")
    c3.metric("Cashflow (pre-tax)", f"{fmt(cashflow_pretax)}/yr", cashflow_delta)
    c1, c2, c3 = st.columns(3)
    c1.metric("Cashflow (after-tax)", f"{fmt(cashflow_aftertax)}/yr")
    c2.metric("Stamp Duty", fmt(stamp_duty))
    c3.metric("LVR", fmtp(lvr))

    # ── Charts ──
    st.divider()
    st.markdown('<div class="section-label">Visualisations</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["💰 Cashflow Projection", "📊 Principal vs Interest", "📉 Loan Balance"])
    with tab1:
        st.plotly_chart(chart_cashflow(annual_rent, annual_interest, annual_expenses, dep_df, marg), use_container_width=True)
    with tab2:
        st.plotly_chart(chart_principal_interest(loan_amount, interest_rate, int(loan_term)), use_container_width=True)
    with tab3:
        st.plotly_chart(chart_balance_over_time(loan_amount, interest_rate, int(loan_term)), use_container_width=True)

    # ── Details ──
    with st.expander("💰 Full Cashflow Breakdown"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Income**")
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Gross annual rent: {fmt(annual_rent_gross)}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Less vacancy ({vacancy_rate:.1f}%): ({fmt(annual_rent_gross - annual_rent)})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'><strong style='color:#f1f5f9;'>Effective annual rent: {fmt(annual_rent)}</strong></span>", unsafe_allow_html=True)
        with col2:
            st.markdown("**Costs**")
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Annual interest: ({fmt(annual_interest)})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Annual expenses: ({fmt(annual_expenses)})</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Year 1 depreciation: ({fmt(year1_dep)})</span>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Taxable property income: <strong style='color:#f1f5f9;'>{fmt(taxable_prop)}</strong></span>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Marginal tax rate ({entity}): <strong style='color:#f1f5f9;'>{marg*100:.0f}%</strong></span>", unsafe_allow_html=True)
        if tax_benefit > 0:
            st.markdown(f'<div class="insight-box"><strong>Negative gearing benefit: {fmt(tax_benefit)}/yr</strong><br><span>At your marginal rate of {marg*100:.0f}%, the ATO effectively subsidises your shortfall.</span></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='font-family:Space Grotesk,sans-serif;color:#f1f5f9;font-weight:600;'>After-tax cashflow (Year 1): {fmt(cashflow_aftertax)}/yr ({fmt(cashflow_aftertax/52)}/wk)</p>", unsafe_allow_html=True)

    with st.expander(f"🏛️ Stamp Duty — {state}"):
        st.metric("Stamp duty payable", fmt(stamp_duty))
        total_upfront = stamp_duty + equity
        st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Deposit: {fmt(equity)}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'><strong style='color:#f1f5f9;'>Total upfront cash required: {fmt(total_upfront)}</strong></span>", unsafe_allow_html=True)
        st.caption(f"Indicative only — confirm with your conveyancer.")

    with st.expander("📐 Break-Even Rent Finder"):
        breakeven_weekly = (annual_interest + annual_expenses) / 52
        breakeven_aftertax = ((annual_interest + annual_expenses - year1_dep) * (1 - marg) + year1_dep * (1 - marg)) / 52
        col1, col2 = st.columns(2)
        col1.metric("Break-even (pre-tax)", f"{fmt(breakeven_weekly)}/wk")
        col2.metric("Break-even (after-tax)", f"{fmt(breakeven_aftertax)}/wk")
        surplus = weekly_rent - breakeven_weekly
        st.markdown(f'<div class="insight-box"><strong>Current rent vs break-even: {surplus:+,.0f}/wk {"above ✅" if surplus >= 0 else "below ❌"}</strong><br><span>{"You are covering your costs from rent alone." if surplus >= 0 else "You need to top up from other income to cover costs."}</span></div>', unsafe_allow_html=True)

    with st.expander("🔧 Depreciation Schedule"):
        display_dep = dep_df[dep_df["Year"] <= 25].copy()
        for col in ["Building", "Plant", "Total"]:
            display_dep[col] = display_dep[col].map("${:,.0f}".format)
        st.dataframe(display_dep.set_index("Year"), use_container_width=True)

    with st.expander("📅 Amortization Schedule"):
        if io_enabled_pa and io_years_pa > 0:
            amort_df = build_amortization_io(loan_amount, interest_rate, int(io_years_pa), int(loan_term))
            st.info(f"Showing interest-only for years 1–{io_years_pa}, then P&I for years {io_years_pa+1}–{int(loan_term)}.")
        else:
            amort_df = build_amortization(loan_amount, interest_rate, int(loan_term))
        annual_summary = amort_df.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum"), Balance=("Balance","last")).reset_index()
        for col in ["Principal", "Interest", "Balance"]:
            annual_summary[col] = annual_summary[col].map("${:,.0f}".format)
        st.dataframe(annual_summary.set_index("Year"), use_container_width=True)
        st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Total interest over {int(loan_term)} years: <strong style='color:#f1f5f9;'>{fmt(amort_df['Interest'].sum())}</strong></span>", unsafe_allow_html=True)

    with st.expander("📈 CGT Estimator"):
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
            est_tax = taxable_gain * est_rate
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Gross gain", fmt(gross_gain))
            c2.metric("CGT discount", fmt(discount) if discount > 0 else "None")
            c3.metric("Taxable gain", fmt(taxable_gain))
            c4.metric("Estimated CGT", fmt(est_tax))

    with st.expander("📈 Capital Growth Projector"):
        st.markdown("Estimate how your property value and equity could grow over time.")
        col1, col2 = st.columns(2)
        with col1:
            cg_rate = st.number_input("Annual growth rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5, key="cg_rate_pa")
        with col2:
            cg_years = st.number_input("Projection (years)", min_value=1, max_value=30, value=5, key="cg_years_pa")

        cg_data = []
        cg_amort = build_amortization(loan_amount, interest_rate, int(loan_term))
        for yr in range(0, int(cg_years) + 1):
            proj_value = purchase_price * ((1 + cg_rate / 100) ** yr)
            loan_balance = cg_amort[cg_amort["Year"] == yr]["Balance"].iloc[-1] if yr > 0 and yr <= len(cg_amort.groupby("Year")) else loan_amount
            proj_equity = proj_value - loan_balance
            cg_data.append({"Year": yr, "Property Value": proj_value, "Equity": proj_equity, "Loan Balance": loan_balance})
        cg_df = pd.DataFrame(cg_data)

        # Metrics
        final = cg_df.iloc[-1]
        initial_equity = purchase_price - loan_amount
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Value in {int(cg_years)} years", fmt(final["Property Value"]), fmt(final["Property Value"] - purchase_price) + " gain")
        c2.metric("Projected equity", fmt(final["Equity"]), fmt(final["Equity"] - initial_equity) + " growth")
        c3.metric("Total return", fmtp(((final["Property Value"] - purchase_price) / purchase_price) * 100))

        # Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cg_df["Year"], y=cg_df["Property Value"], name="Property Value",
                                 line=dict(color=COLORS["gold"], width=2.5), fill="tozeroy",
                                 fillcolor="rgba(16,185,129,0.06)"))
        fig.add_trace(go.Scatter(x=cg_df["Year"], y=cg_df["Equity"], name="Your Equity",
                                 line=dict(color="#34d399", width=2, dash="dot")))
        fig.add_trace(go.Scatter(x=cg_df["Year"], y=cg_df["Loan Balance"], name="Loan Balance",
                                 line=dict(color="#334155", width=1.5)))
        fig.update_layout(**PLOTLY_LAYOUT,
                          title=dict(text="Property Value & Equity Projection", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                          legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                          xaxis_title="Year", yaxis_title="Value ($)",
                          xaxis=dict(gridcolor="#1e2d3d", dtick=1), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("⚠️ Capital growth projections are estimates only. Past growth does not guarantee future performance.")


# ─────────────────────────────────────────────
# PAGE: MORTGAGE CALCULATOR
# ─────────────────────────────────────────────

elif page == "📐 Mortgage Calculator":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>📐 Mortgage Calculator</h1>
            <p>Repayments, amortization & pay off sooner analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_amount = st.number_input("Loan amount ($)", value=500000.0, step=1000.0)
    with col2:
        interest_rate = st.number_input("Interest rate (%)", value=6.0, step=0.1)
    with col3:
        loan_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30)

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
            amort_df_full = build_amortization_io(loan_amount, interest_rate, int(io_years), int(loan_term))
            io_monthly = loan_amount * (interest_rate / 100) / 12
            pi_years = int(loan_term) - int(io_years)
            pi_monthly = calc_monthly_payment(loan_amount, interest_rate, pi_years)
            total_interest = amort_df_full["Interest"].sum()
            total_paid = amort_df_full["Payment"].sum()
            # Compare with straight P&I
            pi_only_df = build_amortization(loan_amount, interest_rate, int(loan_term))
            pi_total_interest = pi_only_df["Interest"].sum()
            extra_interest = total_interest - pi_total_interest

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("IO monthly repayment", fmt(io_monthly), f"for {io_years} yrs")
            c2.metric("P&I monthly (after IO)", fmt(pi_monthly), f"for {pi_years} yrs")
            c3.metric("Total interest", fmt(total_interest))
            c4.metric("Extra interest vs P&I", fmt(extra_interest), "cost of IO period", delta_color="inverse")

            st.markdown(f'<div class="insight-box"><strong>Interest-only for {io_years} years costs an extra {fmt(extra_interest)} in total interest</strong> compared to a standard P&I loan.<br><span>Your repayments jump from {fmt(io_monthly)}/mo to {fmt(pi_monthly)}/mo when the IO period ends — make sure you plan for this.</span></div>', unsafe_allow_html=True)
        else:
            monthly = calc_monthly_payment(loan_amount, interest_rate, int(loan_term))
            total_paid = monthly * int(loan_term) * 12
            total_interest = total_paid - loan_amount
            amort_df_full = build_amortization(loan_amount, interest_rate, int(loan_term))

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Monthly repayment", fmt(monthly))
            c2.metric("Weekly repayment", fmt(monthly * 12 / 52))
            c3.metric("Total interest", fmt(total_interest))
            c4.metric("Total paid", fmt(total_paid))

        # Charts
        tab1, tab2 = st.tabs(["📊 Principal vs Interest", "📉 Loan Balance"])
        with tab1:
            # Build chart from full amortization
            annual = amort_df_full.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum")).reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Principal", x=annual["Year"], y=annual["Principal"], marker_color=COLORS["gold"], marker_line_width=0))
            fig.add_trace(go.Bar(name="Interest", x=annual["Year"], y=annual["Interest"], marker_color="#1e3a2a", marker_line_width=0))
            if io_enabled and io_years > 0:
                fig.add_vline(x=io_years + 0.5, line_dash="dash", line_color=COLORS["red"],
                              annotation_text="IO → P&I", annotation_position="top")
            fig.update_layout(**PLOTLY_LAYOUT, barmode="stack", title=dict(text="Annual Principal vs Interest", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                              legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                              xaxis_title="Year", yaxis_title="Amount ($)",
                              xaxis=dict(gridcolor="#1e2d3d"), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            annual_bal = amort_df_full.groupby("Year")["Balance"].last().reset_index()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=annual_bal["Year"], y=annual_bal["Balance"], name="Balance",
                                      line=dict(color=COLORS["gold"], width=2.5), fill="tozeroy",
                                      fillcolor="rgba(16,185,129,0.1)"))
            if io_enabled and io_years > 0:
                fig2.add_vline(x=io_years + 0.5, line_dash="dash", line_color=COLORS["red"],
                               annotation_text="IO → P&I", annotation_position="top")
            fig2.update_layout(**PLOTLY_LAYOUT, title=dict(text="Loan Balance Over Time", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                               legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                               xaxis_title="Year", yaxis_title="Balance ($)",
                               xaxis=dict(gridcolor="#1e2d3d"), yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
            st.plotly_chart(fig2, use_container_width=True)

        # ── PAY OFF SOONER ──
        st.divider()
        st.markdown('<div class="section-label">⚡ Pay Off Sooner Calculator</div>', unsafe_allow_html=True)
        st.markdown("See how much time and interest you save by making extra repayments.")

        col1, col2 = st.columns(2)
        with col1:
            extra_monthly = st.number_input("Extra monthly repayment ($)", min_value=0.0, value=500.0, step=100.0)
        with col2:
            extra_lump = st.number_input("One-off lump sum ($)", min_value=0.0, value=0.0, step=1000.0,
                                         help="Applied immediately to the principal")

        effective_loan = loan_amount - extra_lump
        if effective_loan < 0:
            st.warning("Lump sum exceeds loan amount.")
        else:
            if io_enabled and io_years > 0:
                df_standard = build_amortization_io(loan_amount, interest_rate, int(io_years), int(loan_term), extra_monthly=0)
                df_extra = build_amortization_io(effective_loan, interest_rate, int(io_years), int(loan_term), extra_monthly=extra_monthly)
            else:
                df_standard = build_amortization(loan_amount, interest_rate, int(loan_term), extra_monthly=0)
                df_extra = build_amortization(effective_loan, interest_rate, int(loan_term), extra_monthly=extra_monthly)

            standard_months = len(df_standard)
            extra_months = len(df_extra)
            months_saved = standard_months - extra_months
            years_saved = months_saved // 12
            mo_saved = months_saved % 12
            interest_standard = df_standard["Interest"].sum()
            interest_extra = df_extra["Interest"].sum()
            interest_saved = interest_standard - interest_extra

            c1, c2, c3 = st.columns(3)
            c1.metric("New payoff time", f"{extra_months // 12}y {extra_months % 12}m",
                      f"{years_saved}y {mo_saved}m sooner" if months_saved > 0 else "No change")
            c2.metric("Interest saved", fmt(interest_saved))
            c3.metric("Total extra paid", fmt(extra_monthly * extra_months + extra_lump))

            # Payoff comparison chart with multiple scenarios
            extra_scenarios = sorted(set([0, int(extra_monthly), int(extra_monthly * 2)]))
            st.plotly_chart(chart_payoff_comparison(effective_loan, interest_rate, int(loan_term), extra_scenarios), use_container_width=True)

            if interest_saved > 0:
                st.markdown(f'<div class="insight-box"><strong>By paying an extra {fmt(extra_monthly)}/month{f" plus a {fmt(extra_lump)} lump sum" if extra_lump > 0 else ""}, you save {fmt(interest_saved)} in interest and pay off {years_saved} year{"s" if years_saved != 1 else ""} {mo_saved} month{"s" if mo_saved != 1 else ""} sooner.</strong><br><span>Your effective return on those extra payments is equivalent to earning {interest_rate:.2f}% guaranteed — often better than a savings account after tax.</span></div>', unsafe_allow_html=True)

        with st.expander("📅 Full Amortization Schedule"):
            annual_summary = amort_df_full.groupby("Year").agg(Principal=("Principal","sum"), Interest=("Interest","sum"), Balance=("Balance","last")).reset_index()
            for col in ["Principal", "Interest", "Balance"]:
                annual_summary[col] = annual_summary[col].map("${:,.0f}".format)
            st.dataframe(annual_summary.set_index("Year"), use_container_width=True)
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Total interest over loan term: <strong style='color:#f1f5f9;'>{fmt(amort_df_full['Interest'].sum())}</strong></span>", unsafe_allow_html=True)

    else:
        st.info("Enter loan details above to see results.")


# ─────────────────────────────────────────────
# PAGE: YIELD CALCULATOR
# ─────────────────────────────────────────────

elif page == "📊 Yield Calculator":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>📊 Yield Calculator</h1>
            <p>Gross and net rental yield analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        purchase_price = st.number_input("Purchase price ($)", value=500000.0, step=1000.0)
        weekly_rent = st.number_input("Weekly rent ($)", value=500.0, step=10.0)
    with col2:
        vacancy_rate = st.number_input("Vacancy rate (%)", value=4.0, step=0.5)
        annual_expenses = st.number_input("Annual expenses ($)", value=5000.0, step=100.0)

    st.markdown('<div class="section-label">Mortgage (optional)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        yld_loan = st.number_input("Loan amount ($)", value=400000.0, step=1000.0, key="yld_loan")
    with col2:
        yld_rate = st.number_input("Interest rate (%)", value=6.0, step=0.1, key="yld_rate")
    with col3:
        yld_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30, key="yld_term")

    if purchase_price > 0:
        annual_rent_gross = weekly_rent * 52
        annual_rent_net = annual_rent_gross * (1 - vacancy_rate / 100)
        gross_yield = (annual_rent_gross / purchase_price) * 100
        net_yield = ((annual_rent_net - annual_expenses) / purchase_price) * 100
        yld_monthly = calc_monthly_payment(yld_loan, yld_rate, int(yld_term))
        yld_weekly = yld_monthly * 12 / 52
        net_weekly_cashflow = (annual_rent_net - annual_expenses - yld_monthly * 12) / 52

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Gross yield", fmtp(gross_yield))
        c2.metric("Net yield", fmtp(net_yield))
        c3.metric("Monthly repayment", fmt(yld_monthly))
        c4.metric("Weekly repayment", fmt(yld_weekly))

        c1, c2, c3 = st.columns(3)
        c1.metric("Annual rent (gross)", fmt(annual_rent_gross))
        c2.metric("Annual rent (effective)", fmt(annual_rent_net))
        c3.metric("Net weekly cashflow", f"{fmt(net_weekly_cashflow)}/wk",
                  "✅ Positive" if net_weekly_cashflow >= 0 else "❌ Negative")

        # Yield gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=net_yield,
            delta={"reference": 5, "valueformat": ".2f", "suffix": "%"},
            title={"text": "Net Yield", "font": {"family": "Playfair Display", "size": 18}},
            number={"suffix": "%", "valueformat": ".2f"},
            gauge={
                "axis": {"range": [0, 12], "tickformat": ".0f", "ticksuffix": "%"},
                "bar": {"color": COLORS["gold"]},
                "bgcolor": "#161b27",
                "bordercolor": "#1e2d3d",
                "steps": [
                    {"range": [0, 3.5], "color": "rgba(192,73,58,0.15)"},
                    {"range": [3.5, 5], "color": "rgba(181,134,58,0.15)"},
                    {"range": [5, 12], "color": "rgba(74,140,92,0.15)"},
                ],
                "threshold": {"line": {"color": COLORS["green"], "width": 2}, "thickness": 0.75, "value": 5}
            }
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280)
        st.plotly_chart(fig, use_container_width=True)

        if net_yield >= 5:
            st.success(f"✅ Strong yield — this property is performing above the 5% benchmark.")
        elif net_yield >= 3.5:
            st.info(f"📊 Moderate yield — acceptable but monitor expenses to improve returns.")
        else:
            st.error(f"⚠️ Low yield — consider price negotiation or increasing rent.")

        with st.expander("📐 Break-Even Rent"):
            breakeven = annual_expenses / 52
            surplus = weekly_rent - breakeven
            st.metric("Break-even weekly rent (expenses only)", f"{fmt(breakeven)}/wk")
            st.markdown(f"<span style='font-family:Space Grotesk,sans-serif;color:#94a3b8;'>Your rent vs break-even: <strong style='color:#f1f5f9;'>{surplus:+,.0f}/wk</strong> {'✅' if surplus >= 0 else '❌'}</span>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: COMPARE PROPERTIES
# ─────────────────────────────────────────────

elif page == "⚖️ Compare Properties":
    st.markdown("""
    <div class="page-header">
        <div>
            <h1>⚖️ Compare Properties</h1>
            <p>SIDE-BY-SIDE ANALYSIS OF UP TO 3 PROPERTIES</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Shared assumptions ──
    st.markdown('<div class="section-label">Shared Assumptions</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        cmp_entity = st.selectbox("Entity type", ["Individual", "SMSF", "Company / Trust"], key="cmp_entity")
    with col2:
        cmp_state = st.selectbox("State", ["QLD", "NSW", "VIC", "WA", "SA", "TAS", "ACT", "NT"], key="cmp_state")
    with col3:
        cmp_income = st.number_input("Other annual income ($)", min_value=0.0, value=80000.0, step=1000.0, key="cmp_income")

    st.divider()

    # ── Property inputs ──
    props = []
    cols = st.columns(3)
    default_names = ["Property A", "Property B", "Property C"]
    default_prices = [500000.0, 650000.0, 450000.0]
    default_rents = [500.0, 620.0, 440.0]
    default_loans = [400000.0, 520000.0, 360000.0]
    default_rates = [6.0, 6.0, 6.5]
    default_expenses = [5000.0, 6500.0, 4500.0]

    for i, col in enumerate(cols):
        with col:
            st.markdown(f'<div class="section-label">{default_names[i]}</div>', unsafe_allow_html=True)
            name = st.text_input("Label", value=default_names[i], key=f"cmp_name_{i}")
            price = st.number_input("Purchase price ($)", min_value=1.0, value=default_prices[i], step=1000.0, key=f"cmp_price_{i}")
            rent = st.number_input("Weekly rent ($)", min_value=0.0, value=default_rents[i], step=10.0, key=f"cmp_rent_{i}")
            loan = st.number_input("Loan amount ($)", min_value=0.0, value=default_loans[i], step=1000.0, key=f"cmp_loan_{i}")
            rate = st.number_input("Interest rate (%)", min_value=0.0, value=default_rates[i], step=0.1, key=f"cmp_rate_{i}")
            expenses = st.number_input("Annual expenses ($)", min_value=0.0, value=default_expenses[i], step=100.0, key=f"cmp_exp_{i}")
            loan_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30, key=f"cmp_term_{i}")
            props.append({
                "name": name, "price": price, "rent": rent,
                "loan": loan, "rate": rate, "expenses": expenses, "term": loan_term
            })

    st.divider()

    # ── Calculations ──
    results = []
    marg = marginal_rate(cmp_entity, cmp_income)
    for p in props:
        annual_rent = p["rent"] * 52
        gross_yield = (annual_rent / p["price"]) * 100
        net_yield = ((annual_rent - p["expenses"]) / p["price"]) * 100
        annual_interest = p["loan"] * (p["rate"] / 100)
        monthly = calc_monthly_payment(p["loan"], p["rate"], p["term"])
        equity = p["price"] - p["loan"]
        lvr = (p["loan"] / p["price"]) * 100
        cashflow_pre = annual_rent - annual_interest - p["expenses"]
        tax_benefit = abs(min(0, cashflow_pre)) * marg if cashflow_pre < 0 else 0
        cashflow_post = cashflow_pre + tax_benefit
        stamp = calc_stamp_duty(p["price"], cmp_state)
        results.append({
            "name": p["name"],
            "gross_yield": gross_yield,
            "net_yield": net_yield,
            "cashflow_pre": cashflow_pre,
            "cashflow_post": cashflow_post,
            "monthly": monthly,
            "weekly": monthly * 12 / 52,
            "equity": equity,
            "lvr": lvr,
            "stamp": stamp,
            "price": p["price"],
        })

    # ── Winner highlighting helper ──
    def winner(vals, higher_is_better=True):
        if higher_is_better:
            best = max(vals)
        else:
            best = min(vals)
        return [i for i, v in enumerate(vals) if v == best]

    # ── Comparison table ──
    st.markdown('<div class="section-label">Results Comparison</div>', unsafe_allow_html=True)

    metrics = [
        ("Gross Yield", "gross_yield", True, lambda v: fmtp(v)),
        ("Net Yield", "net_yield", True, lambda v: fmtp(v)),
        ("Cashflow (pre-tax)", "cashflow_pre", True, lambda v: f"{fmt(v)}/yr"),
        ("Cashflow (after-tax)", "cashflow_post", True, lambda v: f"{fmt(v)}/yr"),
        ("Monthly Repayment", "monthly", False, lambda v: fmt(v)),
        ("Weekly Repayment", "weekly", False, lambda v: fmt(v)),
        ("Equity", "equity", True, lambda v: fmt(v)),
        ("Stamp Duty", "stamp", False, lambda v: fmt(v)),
    ]

    # Header row
    hcols = st.columns([2, 1, 1, 1])
    hcols[0].markdown("<p style='color:#64748b;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;font-family:JetBrains Mono,monospace;'>METRIC</p>", unsafe_allow_html=True)
    for i, r in enumerate(results):
        hcols[i+1].markdown(f"<p style='color:#10b981;font-size:0.9rem;font-weight:700;font-family:Space Grotesk,sans-serif;'>{r['name']}</p>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e2d3d;margin:0.5rem 0;'>", unsafe_allow_html=True)

    for label, key, higher_better, fmt_fn in metrics:
        vals = [r[key] for r in results]
        winners = winner(vals, higher_better)
        row = st.columns([2, 1, 1, 1])
        row[0].markdown(f"<span style='color:#64748b;font-size:0.78rem;font-family:Space Grotesk,sans-serif;'>{label}</span>", unsafe_allow_html=True)
        for i, r in enumerate(results):
            is_winner = i in winners
            color = "#10b981" if is_winner else "#94a3b8"
            prefix = "🏆 " if is_winner else ""
            row[i+1].markdown(f"<span style='color:{color};font-size:0.85rem;font-weight:{'700' if is_winner else '400'};font-family:JetBrains Mono,monospace;'>{prefix}{fmt_fn(r[key])}</span>", unsafe_allow_html=True)

    # ── Bar charts ──
    st.divider()
    st.markdown('<div class="section-label">Visual Comparison</div>', unsafe_allow_html=True)

    names = [r["name"] for r in results]
    tab1, tab2, tab3 = st.tabs(["📊 Yield", "💰 Cashflow", "🏦 LVR & Equity"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Gross Yield", x=names, y=[r["gross_yield"] for r in results],
                             marker_color=COLORS["gold"], marker_line_width=0))
        fig.add_trace(go.Bar(name="Net Yield", x=names, y=[r["net_yield"] for r in results],
                             marker_color="#064e3b", marker_line_width=0))
        fig.update_layout(**PLOTLY_LAYOUT, barmode="group",
                          title=dict(text="Gross vs Net Yield", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                          legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                          yaxis=dict(gridcolor="#1e2d3d", ticksuffix="%"), xaxis=dict(gridcolor="#1e2d3d"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Pre-tax cashflow", x=names, y=[r["cashflow_pre"] for r in results],
                             marker_color="#334155", marker_line_width=0))
        fig.add_trace(go.Bar(name="After-tax cashflow", x=names, y=[r["cashflow_post"] for r in results],
                             marker_color=COLORS["gold"], marker_line_width=0))
        fig.add_hline(y=0, line_color=COLORS["red"], line_width=1, opacity=0.5)
        fig.update_layout(**PLOTLY_LAYOUT, barmode="group",
                          title=dict(text="Annual Cashflow Comparison", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                          legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                          yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"), xaxis=dict(gridcolor="#1e2d3d"))
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Equity", x=names, y=[r["equity"] for r in results],
                             marker_color=COLORS["gold"], marker_line_width=0))
        fig.add_trace(go.Bar(name="Loan", x=names, y=[r["price"] - r["equity"] for r in results],
                             marker_color="#1e3a2a", marker_line_width=0))
        fig.update_layout(**PLOTLY_LAYOUT, barmode="stack",
                          title=dict(text="Equity vs Loan", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                          legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                          yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"), xaxis=dict(gridcolor="#1e2d3d"))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    best_yield = results[winner([r["net_yield"] for r in results])[0]]["name"]
    best_cashflow = results[winner([r["cashflow_post"] for r in results])[0]]["name"]
    best_repayment = results[winner([r["monthly"] for r in results], higher_is_better=False)[0]]["name"]
    st.markdown('<div class="section-label">Quick Summary</div>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    sc1.markdown(f"""
    <div style='background:#0d1f17;border:1px solid #1e3a2a;border-top:3px solid #10b981;border-radius:6px;padding:1.25rem;text-align:center;'>
        <div style='font-size:0.65rem;letter-spacing:0.15em;color:#64748b;font-family:JetBrains Mono,monospace;text-transform:uppercase;margin-bottom:0.5rem;'>Best Net Yield</div>
        <div style='font-size:1.5rem;font-weight:700;color:#10b981;font-family:Space Grotesk,sans-serif;'>🏆 {best_yield}</div>
        <div style='font-size:0.8rem;color:#475569;margin-top:0.3rem;font-family:Space Grotesk,sans-serif;'>{fmtp(max(r["net_yield"] for r in results))}</div>
    </div>
    """, unsafe_allow_html=True)
    sc2.markdown(f"""
    <div style='background:#0d1f17;border:1px solid #1e3a2a;border-top:3px solid #10b981;border-radius:6px;padding:1.25rem;text-align:center;'>
        <div style='font-size:0.65rem;letter-spacing:0.15em;color:#64748b;font-family:JetBrains Mono,monospace;text-transform:uppercase;margin-bottom:0.5rem;'>Best Cashflow</div>
        <div style='font-size:1.5rem;font-weight:700;color:#10b981;font-family:Space Grotesk,sans-serif;'>🏆 {best_cashflow}</div>
        <div style='font-size:0.8rem;color:#475569;margin-top:0.3rem;font-family:Space Grotesk,sans-serif;'>{fmt(max(r["cashflow_post"] for r in results))}/yr</div>
    </div>
    """, unsafe_allow_html=True)
    sc3.markdown(f"""
    <div style='background:#0d1f17;border:1px solid #1e3a2a;border-top:3px solid #10b981;border-radius:6px;padding:1.25rem;text-align:center;'>
        <div style='font-size:0.65rem;letter-spacing:0.15em;color:#64748b;font-family:JetBrains Mono,monospace;text-transform:uppercase;margin-bottom:0.5rem;'>Lowest Repayment</div>
        <div style='font-size:1.5rem;font-weight:700;color:#10b981;font-family:Space Grotesk,sans-serif;'>🏆 {best_repayment}</div>
        <div style='font-size:0.8rem;color:#475569;margin-top:0.3rem;font-family:Space Grotesk,sans-serif;'>{fmt(min(r["monthly"] for r in results))}/mo</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Capital Growth Projector ──
    st.divider()
    st.markdown('<div class="section-label">Capital Growth Projector</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        cg_rate_cmp = st.number_input("Annual growth rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5, key="cg_rate_cmp")
    with col2:
        cg_years_cmp = st.number_input("Projection (years)", min_value=1, max_value=30, value=5, key="cg_years_cmp")

    fig = go.Figure()
    colors_cmp = [COLORS["gold"], "#3b82f6", "#f59e0b"]
    for i, r in enumerate(results):
        vals = [r["price"] * ((1 + cg_rate_cmp / 100) ** yr) for yr in range(0, int(cg_years_cmp) + 1)]
        fig.add_trace(go.Scatter(
            x=list(range(0, int(cg_years_cmp) + 1)),
            y=vals,
            name=r["name"],
            line=dict(color=colors_cmp[i], width=2.5),
        ))

    fig.update_layout(**PLOTLY_LAYOUT,
                      title=dict(text="Projected Property Value", font=dict(size=15, color="#10b981", family="Space Grotesk")),
                      legend=dict(orientation="h", y=-0.2, yanchor="top", font=dict(color="#e2e8f0", size=13, family="Space Grotesk")),
                      xaxis_title="Year", yaxis_title="Value ($)",
                      xaxis=dict(gridcolor="#1e2d3d", dtick=1),
                      yaxis=dict(gridcolor="#1e2d3d", tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig, use_container_width=True)

    # Summary metrics per property
    gcols = st.columns(3)
    for i, r in enumerate(results):
        proj_val = r["price"] * ((1 + cg_rate_cmp / 100) ** int(cg_years_cmp))
        gain = proj_val - r["price"]
        gcols[i].markdown(f"""
        <div style='background:#0d1f17;border:1px solid #1e3a2a;border-top:3px solid {colors_cmp[i]};border-radius:6px;padding:1rem;text-align:center;'>
            <div style='font-size:0.65rem;letter-spacing:0.15em;color:#64748b;font-family:JetBrains Mono,monospace;text-transform:uppercase;margin-bottom:0.4rem;'>{r["name"]}</div>
            <div style='font-size:1.3rem;font-weight:700;color:{colors_cmp[i]};font-family:Space Grotesk,sans-serif;'>{fmt(proj_val)}</div>
            <div style='font-size:0.8rem;color:#10b981;margin-top:0.3rem;font-family:Space Grotesk,sans-serif;'>+{fmt(gain)} gain</div>
        </div>
        """, unsafe_allow_html=True)
    st.caption("⚠️ Capital growth projections are estimates only. Past growth does not guarantee future performance.")
