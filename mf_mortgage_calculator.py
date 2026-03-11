import streamlit as st

st.title("MF Mortgage Calculator")

loan_amount = st.number_input("Loan amount ($)", min_value=1.0, value=500000.0, step=1000.0)
interest_rate = st.number_input("Interest rate (%)", min_value=0.0, value=6.0, step=0.1)
loan_term_years = st.number_input("Loan term (years)", min_value=1, value=30, step=1)

monthly_rate = (interest_rate / 100) / 12
number_of_payments = loan_term_years * 12

if monthly_rate > 0:
    monthly_repayment = loan_amount * (
    monthly_rate * (1 + monthly_rate) ** number_of_payments
    ) / (
(1 + monthly_rate) ** number_of_payments - 1
)
else:
    monthly_repayment = loan_amount / number_of_payments

yearly_repayment = monthly_repayment * 12
total_paid = monthly_repayment * number_of_payments
total_interest = total_paid - loan_amount

st.subheader("Results")
st.write(f"Monthly repayment: ${monthly_repayment:,.2f}")
st.write(f"Yearly repayment: ${yearly_repayment:,.2f}")
st.write(f"Total paid over loan term: ${total_paid:,.2f}")
st.write(f"Total interest paid: ${total_interest:,.2f}")
