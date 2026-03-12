import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="MF Property Toolkit", page_icon="🏡", layout="wide")

st.sidebar.title("🏡 MF Property Toolkit")
st.sidebar.caption("Comprehensive property analysis")

page = st.sidebar.selectbox(
    "Choose calculator",
    ["Property Analyzer", "Mortgage Calculator", "Yield Calculator"]
)

# ─────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────

STAMP_DUTY = {
    "NSW": [
        (0,      14000,   0,       1.25),
        (14000,  32000,   175,     1.50),
        (32000,  85000,   445,     1.75),
        (85000,  319000,  1372,    3.50),
        (319000, 1064000, 9618,    4.50),
        (1064000,3131000, 43231,   5.50),
        (3131000,float("inf"), 157581, 7.00),
    ],
    "VIC": [
        (0,      25000,   0,       1.40),
        (25000,  130000,  350,     2.40),
        (130000, 960000,  2870,    6.00),
        (960000, float("inf"), 52670, 6.50),
    ],
    "QLD": [
        (0,      5000,    0,       0.00),
        (5000,   75000,   0,       1.50),
        (75000,  540000,  1050,    3.50),
        (540000, 1000000, 17325,   4.50),
        (1000000,float("inf"), 38025, 5.75),
    ],
    "WA": [
        (0,      120000,  0,       1.90),
        (120000, 150000,  2280,    2.85),
        (150000, 360000,  3135,    3.80),
        (360000, 725000,  11115,   4.75),
        (725000, float("inf"), 28453, 5.15),
    ],
    "SA": [
        (0,      12000,   0,       1.00),
        (12000,  30000,   120,     2.00),
        (30000,  50000,   480,     3.00),
        (50000,  100000,  1080,    3.50),
        (100000, 200000,  2830,    4.00),
        (200000, 250000,  6830,    4.25),
        (250000, 300000,  8955,    4.75),
        (300000, 500000,  11330,   5.00),
        (500000, float("inf"), 21330, 5.50),
    ],
    "TAS": [
        (0,      3000,    50,      0.00),
        (3000,   25000,   50,      1.75),
        (25000,  75000,   435,     2.25),
        (75000,  200000,  1560,    3.50),
        (200000, 375000,  5935,    4.00),
        (375000, 725000,  12935,   4.25),
        (725000, float("inf"), 27810, 4.50),
    ],
    "ACT": [
        (0,      260000,  0,       0.60),
        (260000, 300000,  1560,    2.20),
        (300000, 500000,  2440,    3.40),
        (500000, 750000,  9240,    4.32),
        (750000, 1000000, 20040,   5.90),
        (1000000,1455000, 34790,   6.40),
        (1455000,float("inf"), 63910, 6.90),
    ],
    "NT": [
        (0,      525000,  0,       None),  # formula-based
        (525000, float("inf"), 0, 4.95),
    ],
}

def calc_stamp_duty(price, state):
    if state == "NT":
        if price <= 525000:
            v = price / 1000
            duty = (0.06571441 * v * v) + 15 * v
            return round(duty)
        else:
            brackets = STAMP_DUTY["NT"]
            base = 0
            rate = 4.95
            return round(base + (price - 525000) * rate / 100)
    brackets = STAMP_DUTY[state]
    for low, high, base, rate in brackets:
        if low <= price < high:
            return round(base + (price - low) * rate / 100)
    return 0

def calc_mortgage(loan, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    if monthly_rate == 0:
        return loan / n
    return loan * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)

def build_amortization(loan, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    n = years * 12
    monthly = calc_mortgage(loan, annual_rate, years)
    balance = loan
    rows = []
    for i in range(1, n + 1):
        interest = balance * monthly_rate
        principal = monthly - interest
        balance = max(0, balance - principal)
        rows.append({
            "Month": i,
            "Year": math.ceil(i / 12),
            "Payment": monthly,
            "Principal": principal,
            "Interest": interest,
            "Balance": balance,
        })
    return pd.DataFrame(rows)

def calc_depreciation(build_cost, plant_cost, method, years=40):
    rows = []
    dv_balance = plant_cost
    for yr in range(1, years + 1):
        if method == "Diminishing Value":
            plant_dep = dv_balance * 0.2
            dv_balance = max(0, dv_balance - plant_dep)
        else:
            plant_dep = plant_cost / 25 if yr <= 25 else 0
        building_dep = build_cost / 40
        total = building_dep + plant_dep
        rows.append({"Year": yr, "Building (2.5%)": building_dep, "Plant & Equipment": plant_dep, "Total": total})
    return pd.DataFrame(rows)

def calc_cgt(purchase_price, sale_price, purchase_costs, sale_costs, entity, held_over_12m):
    cost_base = purchase_price + purchase_costs + sale_costs
    gross_gain = sale_price - cost_base
    if gross_gain <= 0:
        return gross_gain, gross_gain, 0.0

    if entity == "Individual" and held_over_12m:
        taxable_gain = gross_gain * 0.5
        discount = gross_gain * 0.5
    elif entity == "SMSF" and held_over_12m:
        taxable_gain = gross_gain * (1 - 1/3)
        discount = gross_gain / 3
    else:
        taxable_gain = gross_gain
        discount = 0.0

    return gross_gain, taxable_gain, discount

MARGINAL_RATES = {
    "Individual": [
        (0,      18200,  0.0),
        (18200,  45000,  0.19),
        (45000,  120000, 0.325),
        (120000, 180000, 0.37),
        (180000, float("inf"), 0.45),
    ],
    "SMSF":            [(0, float("inf"), 0.15)],
    "Company / Trust": [(0, float("inf"), 0.30)],
}

def marginal_rate(entity, income):
    for low, high, rate in MARGINAL_RATES[entity]:
        if low <= income < high:
            return rate
    return 0.45


# ─────────────────────────────────────────────
# PAGE: PROPERTY ANALYZER
# ─────────────────────────────────────────────

if page == "Property Analyzer":
    st.title("🏡 MF Property Analyzer")
    st.caption("Full investment analysis — cashflow, stamp duty, depreciation, amortization & CGT")

    # ── Entity & State ──
    col1, col2 = st.columns(2)
    with col1:
        entity = st.selectbox("Investor entity", ["Individual", "SMSF", "Company / Trust"])
    with col2:
        state = st.selectbox("State", ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"])

    st.divider()

    # ── Property Details ──
    st.subheader("Property Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        purchase_price = st.number_input("Purchase price ($)", min_value=1.0, value=500000.0, step=1000.0)
    with col2:
        weekly_rent = st.number_input("Weekly rent ($)", min_value=0.0, value=500.0, step=10.0)
    with col3:
        annual_expenses = st.number_input("Annual expenses ($)", min_value=0.0, value=5000.0, step=100.0,
                                          help="Rates, insurance, maintenance, management fees etc.")

    # ── Loan Details ──
    st.subheader("Loan Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        loan_amount = st.number_input("Loan amount ($)", min_value=0.0, value=400000.0, step=1000.0)
    with col2:
        interest_rate = st.number_input("Interest rate (%)", min_value=0.0, value=6.0, step=0.1)
    with col3:
        loan_term = st.number_input("Loan term (years)", min_value=1, max_value=30, value=30)

    # ── Depreciation Inputs ──
    st.subheader("Depreciation")
    col1, col2, col3 = st.columns(3)
    with col1:
        build_cost = st.number_input("Construction / build cost ($)", min_value=0.0, value=200000.0, step=1000.0,
                                     help="Used for 2.5% building depreciation")
    with col2:
        plant_cost = st.number_input("Plant & equipment value ($)", min_value=0.0, value=20000.0, step=500.0,
                                     help="Carpets, appliances, blinds etc.")
    with col3:
        dep_method = st.selectbox("Depreciation method", ["Diminishing Value", "Prime Cost"])

    # ── Income ──
    col1, col2 = st.columns(2)
    with col1:
        other_income = st.number_input("Other annual income ($, for tax calc)", min_value=0.0, value=80000.0, step=1000.0,
                                       help="Your salary / other income — used to estimate marginal tax rate")
    with col2:
        vacancy_rate = st.number_input("Vacancy rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.5)

    st.divider()

    # ─── CALCULATIONS ───
    annual_rent_gross = weekly_rent * 52
    annual_rent = annual_rent_gross * (1 - vacancy_rate / 100)
    gross_yield = (annual_rent_gross / purchase_price) * 100
    net_yield = ((annual_rent - annual_expenses) / purchase_price) * 100

    monthly_repayment = calc_mortgage(loan_amount, interest_rate, loan_term)
    annual_repayment = monthly_repayment * 12
    annual_interest = loan_amount * (interest_rate / 100)  # simple interest for cashflow

    dep_df = calc_depreciation(build_cost, plant_cost, dep_method)
    year1_depreciation = dep_df.iloc[0]["Total"]

    stamp_duty = calc_stamp_duty(purchase_price, state)
    equity = purchase_price - loan_amount
    lvr = (loan_amount / purchase_price) * 100 if purchase_price > 0 else 0

    cashflow_pretax = annual_rent - annual_interest - annual_expenses
    taxable_property_income = annual_rent - annual_interest - annual_expenses - year1_depreciation
    marg_rate = marginal_rate(entity, other_income)
    tax_benefit = abs(min(0, taxable_property_income)) * marg_rate if taxable_property_income < 0 else 0
    cashflow_aftertax = cashflow_pretax + tax_benefit

    # ─── RESULTS ───
    st.subheader("📊 Results")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gross Yield", f"{gross_yield:.2f}%")
    col2.metric("Net Yield", f"{net_yield:.2f}%")
    cashflow_label = "✅ Positive" if cashflow_pretax > 0 else ("❌ Negative" if cashflow_pretax < 0 else "😌 Neutral")
    col3.metric("Cashflow (pre-tax)", f"${cashflow_pretax:,.0f}/yr", cashflow_label)
    col4.metric("Cashflow (after-tax)", f"${cashflow_aftertax:,.0f}/yr")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Repayment", f"${monthly_repayment:,.0f}")
    col2.metric("Stamp Duty", f"${stamp_duty:,.0f}")
    col3.metric("LVR", f"{lvr:.1f}%")
    col4.metric("Equity", f"${equity:,.0f}")

    # Cashflow breakdown
    with st.expander("💰 Cashflow Breakdown", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Income**")
            st.write(f"Gross annual rent: ${annual_rent_gross:,.0f}")
            st.write(f"Less vacancy ({vacancy_rate:.1f}%): (${annual_rent_gross - annual_rent:,.0f})")
            st.write(f"**Effective annual rent: ${annual_rent:,.0f}**")
        with col2:
            st.markdown("**Costs**")
            st.write(f"Annual interest: (${annual_interest:,.0f})")
            st.write(f"Annual expenses: (${annual_expenses:,.0f})")
            st.write(f"Year 1 depreciation: (${year1_depreciation:,.0f})")
        st.divider()
        st.write(f"**Taxable property income: ${taxable_property_income:,.0f}**")
        st.write(f"Marginal tax rate ({entity}): {marg_rate*100:.0f}%")
        if tax_benefit > 0:
            st.write(f"Tax benefit (negative gearing): ${tax_benefit:,.0f}")
        st.write(f"**After-tax cashflow (Year 1): ${cashflow_aftertax:,.0f}**")

    # Stamp Duty
    with st.expander(f"🏛️ Stamp Duty — {state}"):
        st.metric("Stamp duty payable", f"${stamp_duty:,.0f}")
        st.caption(f"Based on purchase price of ${purchase_price:,.0f} in {state}. "
                   "Figures are indicative — confirm with your conveyancer.")
        total_upfront = stamp_duty + (purchase_price - loan_amount)
        st.write(f"Total upfront cash required (deposit + stamp duty): **${total_upfront:,.0f}**")

    # Break-even rent
    with st.expander("📐 Break-Even Rent Finder"):
        breakeven_annual = annual_interest + annual_expenses
        breakeven_weekly = breakeven_annual / 52
        breakeven_aftertax_annual = (annual_interest + annual_expenses - year1_depreciation) * (1 - marg_rate)
        breakeven_aftertax_weekly = (breakeven_aftertax_annual + year1_depreciation * (1 - marg_rate)) / 52
        col1, col2 = st.columns(2)
        col1.metric("Break-even rent (pre-tax)", f"${breakeven_weekly:,.0f}/wk",
                    help="Rent needed to cover interest + expenses")
        col2.metric("Break-even rent (after-tax)", f"${breakeven_aftertax_weekly:,.0f}/wk",
                    help="Includes depreciation tax shield")
        current_surplus = weekly_rent - breakeven_weekly
        st.write(f"Your current rent vs break-even: **${current_surplus:+,.0f}/wk** {'above ✅' if current_surplus >= 0 else 'below ❌'}")

    # Depreciation schedule
    with st.expander("🔧 Depreciation Schedule (25 years)"):
        st.write(f"Method: **{dep_method}**")
        display_dep = dep_df[dep_df["Year"] <= 25].copy()
        display_dep["Building (2.5%)"] = display_dep["Building (2.5%)"].map("${:,.0f}".format)
        display_dep["Plant & Equipment"] = display_dep["Plant & Equipment"].map("${:,.0f}".format)
        display_dep["Total"] = display_dep["Total"].map("${:,.0f}".format)
        st.dataframe(display_dep.set_index("Year"), use_container_width=True)

    # Amortization schedule
    with st.expander("📅 Amortization Schedule"):
        amort_df = build_amortization(loan_amount, interest_rate, loan_term)

        # Annual summary
        annual_summary = amort_df.groupby("Year").agg(
            Principal=("Principal", "sum"),
            Interest=("Interest", "sum"),
            Balance=("Balance", "last"),
        ).reset_index()
        annual_summary["Principal"] = annual_summary["Principal"].map("${:,.0f}".format)
        annual_summary["Interest"] = annual_summary["Interest"].map("${:,.0f}".format)
        annual_summary["Balance"] = annual_summary["Balance"].map("${:,.0f}".format)
        st.write("**Annual summary**")
        st.dataframe(annual_summary.set_index("Year"), use_container_width=True)

        total_interest_paid = amort_df["Interest"].sum()
        total_paid = amort_df["Payment"].sum()
        st.write(f"Total interest over {loan_term} years: **${total_interest_paid:,.0f}**")
        st.write(f"Total paid over {loan_term} years: **${total_paid:,.0f}**")

    # CGT
    with st.expander("📈 Capital Gains Tax (CGT) Estimator"):
        st.write("Estimate the CGT liability on a future sale.")
        col1, col2, col3 = st.columns(3)
        with col1:
            sale_price = st.number_input("Expected sale price ($)", min_value=0.0,
                                         value=float(round(purchase_price * 1.3 / 1000) * 1000), step=10000.0)
        with col2:
            purchase_costs = st.number_input("Purchase costs ($)", min_value=0.0,
                                             value=float(stamp_duty), step=500.0,
                                             help="Stamp duty, legal, inspection fees")
        with col3:
            sale_costs = st.number_input("Sale costs ($)", min_value=0.0, value=15000.0, step=500.0,
                                         help="Agent commission, legal fees")

        held_over_12m = st.toggle("Held for 12+ months (CGT discount eligible)", value=True)

        gross_gain, taxable_gain, discount = calc_cgt(
            purchase_price, sale_price, purchase_costs, sale_costs, entity, held_over_12m
        )

        if gross_gain <= 0:
            st.warning(f"Capital loss of ${abs(gross_gain):,.0f} — no CGT payable.")
        else:
            est_cgt_rate = marginal_rate(entity, other_income + taxable_gain)
            est_tax = taxable_gain * est_cgt_rate

            col1, col2, col3 = st.columns(3)
            col1.metric("Gross capital gain", f"${gross_gain:,.0f}")
            col2.metric("CGT discount", f"${discount:,.0f}" if discount > 0 else "None")
            col3.metric("Taxable gain", f"${taxable_gain:,.0f}")

            col1, col2 = st.columns(2)
            col1.metric("Estimated tax rate", f"{est_cgt_rate*100:.0f}%")
            col2.metric("Estimated CGT payable", f"${est_tax:,.0f}")

            if entity == "Individual" and not held_over_12m:
                st.info("💡 Holding for 12+ months would reduce taxable gain by 50%.")
            if entity == "SMSF":
                st.info("💡 SMSF receives a 1/3 CGT discount after 12 months (effective 10% tax on gains).")

    st.caption("⚠️ All figures are indicative only and do not constitute financial or tax advice. Consult a qualified adviser.")


# ─────────────────────────────────────────────
# PAGE: MORTGAGE CALCULATOR
# ─────────────────────────────────────────────

elif page == "Mortgage Calculator":
    st.title("🏡 MF Property Toolkit")
    st.caption("Quick property analysis")
    st.header("Mortgage Calculator")
    st.write("Enter your loan details below")

    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("Loan amount ($)", value=500000.0)
    with col2:
        interest_rate = st.number_input("Interest rate (%)", value=6.0)

    loan_term = st.number_input("Loan term (years)", value=30)

    if loan_amount > 0 and interest_rate >= 0 and loan_term > 0:
        monthly_repayment = calc_mortgage(loan_amount, interest_rate, int(loan_term))
        yearly_repayment = monthly_repayment * 12
        total_paid = monthly_repayment * int(loan_term) * 12
        total_interest = total_paid - loan_amount

        st.subheader("Results")
        col1, col2 = st.columns(2)
        col1.metric("Monthly repayment", f"${monthly_repayment:,.2f}")
        col2.metric("Total interest", f"${total_interest:,.2f}")
        st.write(f"Yearly repayment: ${yearly_repayment:,.2f}")
        st.write(f"Total paid over loan term: ${total_paid:,.2f}")

        with st.expander("📅 Amortization Schedule"):
            amort_df = build_amortization(loan_amount, interest_rate, int(loan_term))
            annual_summary = amort_df.groupby("Year").agg(
                Principal=("Principal", "sum"),
                Interest=("Interest", "sum"),
                Balance=("Balance", "last"),
            ).reset_index()
            annual_summary["Principal"] = annual_summary["Principal"].map("${:,.0f}".format)
            annual_summary["Interest"] = annual_summary["Interest"].map("${:,.0f}".format)
            annual_summary["Balance"] = annual_summary["Balance"].map("${:,.0f}".format)
            st.dataframe(annual_summary.set_index("Year"), use_container_width=True)
    else:
        st.info("Enter loan details to calculate repayment")


# ─────────────────────────────────────────────
# PAGE: YIELD CALCULATOR
# ─────────────────────────────────────────────

elif page == "Yield Calculator":
    st.title("🏡 MF Property Toolkit")
    st.caption("Quick property analysis")
    st.header("Rental Yield Calculator")
    st.write("Enter property details below")

    col1, col2 = st.columns(2)
    with col1:
        purchase_price = st.number_input("Purchase price ($)", value=500000.0)
    with col2:
        weekly_rent = st.number_input("Weekly rent ($)", value=500.0)

    col1, col2 = st.columns(2)
    with col1:
        vacancy_rate = st.number_input("Vacancy rate (%)", value=4.0, step=0.5)
    with col2:
        annual_expenses = st.number_input("Annual expenses ($)", value=5000.0, step=100.0)

    if purchase_price > 0 and weekly_rent >= 0:
        annual_rent_gross = weekly_rent * 52
        annual_rent_net = annual_rent_gross * (1 - vacancy_rate / 100)
        gross_yield = (annual_rent_gross / purchase_price) * 100
        net_yield = ((annual_rent_net - annual_expenses) / purchase_price) * 100

        st.subheader("Results")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Annual rent (gross)", f"${annual_rent_gross:,.0f}")
        col2.metric("Annual rent (effective)", f"${annual_rent_net:,.0f}")
        col3.metric("Gross yield", f"{gross_yield:.2f}%")
        col4.metric("Net yield", f"{net_yield:.2f}%")

        # Break-even
        with st.expander("📐 Break-Even Rent"):
            breakeven_weekly = annual_expenses / 52
            st.write(f"Break-even rent (expenses only): **${breakeven_weekly:,.0f}/wk**")
            surplus = weekly_rent - breakeven_weekly
            st.write(f"Surplus above expenses: **${surplus:+,.0f}/wk**")
    else:
        st.info("Enter property details to calculate yield")

    st.caption("⚠️ Indicative only. Not financial advice.")
