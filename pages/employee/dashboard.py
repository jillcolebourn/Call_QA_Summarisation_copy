"""
Employee Portal - Dashboard Page
Shows full account details, payment history, and account management options
"""
import streamlit as st
import pandas as pd
from utils.api_client import get_account_data, get_customer_data, get_payment_history
from utils.styles import COLORS
from utils.sidebar import render_employee_sidebar

# Render sidebar
render_employee_sidebar()

st.title("📊 Employee Dashboard")

# Get client ID from session state
client_id = st.session_state.get('client_id', 31567)

# Header
st.markdown(f"""
<div class="dashboard-header">
    <h1>Mortgage Account Dashboard</h1>
    <p style="color: #666;">Client ID: <strong>{client_id}</strong> | Account Status: <span style="color: {COLORS['red']}"><strong>Arrears</strong></span></p>
</div>
""", unsafe_allow_html=True)

# Fetch data
account = get_account_data(client_id)
customer = get_customer_data(client_id)

if not account:
    st.error("Unable to load account data")
    st.stop()

# Summary cards grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="summary-card">
        <h3>Outstanding Balance</h3>
        <div class="value">£{account.get('principal', 0):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="summary-card">
        <h3>Monthly Payment</h3>
        <div class="value">£{account.get('monthly_payments', 0):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="summary-card">
        <h3>Interest Rate</h3>
        <div class="value">{account.get('interest_rate_pa', 0)}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    months_remaining = account.get('term_months', 0) - account.get('loan_age_months', 0)
    years_remaining = months_remaining / 12
    st.markdown(f"""
    <div class="summary-card">
        <h3>Remaining Term</h3>
        <div class="value">{years_remaining:.1f} years</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content - two columns
col_left, col_right = st.columns([2, 1])

with col_left:
    # Payment history table
    st.markdown("### 📅 Payment History")

    payment_history = get_payment_history(client_id)

    if payment_history is not None:
        # Display summary stats
        total_payments = len(payment_history)
        paid_payments = len(payment_history[payment_history['status'] == 'Paid'])
        missed_payments = len(payment_history[payment_history['status'] == 'Missed'])

        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Total Payments", total_payments)
        with col_stat2:
            st.metric("Paid", paid_payments)
        with col_stat3:
            st.metric("Missed", missed_payments)

        st.markdown("---")

        # Display payment history table (most recent first)
        display_df = payment_history.sort_values('payment_date', ascending=False).copy()
        display_df['payment_date'] = display_df['payment_date'].dt.strftime('%Y-%m-%d')
        display_df['amount'] = display_df['amount'].apply(lambda x: f"£{x:,.2f}")

        # Style the dataframe
        def highlight_missed(row):
            if row['status'] == 'Missed':
                return ['background-color: #FFCDD2; color: #B71C1C; font-weight: 500'] * len(row)
            elif row['status'] == 'Paid':
                return ['background-color: #C8E6C9; color: #1B5E20; font-weight: 500'] * len(row)
            return [''] * len(row)

        styled_df = display_df.style.apply(highlight_missed, axis=1)

        st.dataframe(
            styled_df,
            column_config={
                "payment_date": st.column_config.TextColumn("Payment Date", width="medium"),
                "amount": st.column_config.TextColumn("Amount", width="medium"),
                "status": st.column_config.TextColumn("Status", width="small")
            },
            hide_index=True,
            width='stretch',
            height=400
        )
    else:
        st.info(f"ℹ️ No payment history file found for client {client_id}")

with col_right:
    # Customer Information Card
    st.markdown("### 👤 Customer Information")

    if customer:
        st.markdown(f"""
        <div class="support-card">
            <p><strong>Name:</strong> {customer.get('given_name(s)', '')} {customer.get('surname', '')}</p>
            <p><strong>Income:</strong> £{customer.get('income_gross_pa', 0):,.2f}/year</p>
            <p><strong>Expenses:</strong> £{customer.get('essential_expenditure', 0):,.2f}/month</p>
            <p><strong>Consent:</strong> {'✅ Given' if customer.get('consent') == 1 else '❌ Not Given'}</p>
        </div>
        """, unsafe_allow_html=True)

    # Arrears notice (if in arrears)
    if account.get('payment_status') == 'Arrears':
        days_in_arrears = account.get('days_in_arrears', 0)
        months_in_arrears = days_in_arrears // 30
        arrears_amount = months_in_arrears * account.get('monthly_payments', 0)

        st.markdown(f"""
        <div class="urgent-notice">
            <h3>⚠️ Payment Arrears</h3>
            <p><strong>Arrears: £{arrears_amount:,.2f}</strong></p>
            <p>{days_in_arrears} days ({months_in_arrears} months)</p>
        </div>
        """, unsafe_allow_html=True)

