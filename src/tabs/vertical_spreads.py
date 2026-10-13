import streamlit as st
import matplotlib.pyplot as plt
from models.vertical_spread import VerticalSpread


def show_vertical_spreads_tab():
    st.header("Vertical Spread Analyzer")
    st.caption("Both legs share one expiry. Premiums are per share; P&L is for the entire position, before fees.")

    with st.form("vertical_spread_form"):
        option_type = st.selectbox("Spread Option Type", ('Call', 'Put'), key="spread_option_type")
        long, short = st.columns(2)
        with long:
            long_strike = st.number_input("Long Strike", value=100.0, min_value=0.01, step=1.0, key="spread_long_strike")
            long_premium = st.number_input("Premium Paid", value=3.0, min_value=0.0, step=0.1, key="spread_long_premium")
        with short:
            short_strike = st.number_input("Short Strike", value=105.0, min_value=0.01, step=1.0, key="spread_short_strike")
            short_premium = st.number_input("Premium Received", value=1.0, min_value=0.0, step=0.1, key="spread_short_premium")
        quantity = st.number_input("Number of Spreads", value=1, min_value=1, step=1, key="spread_quantity")
        multiplier = st.number_input("Contract Multiplier", value=100, min_value=1, step=1, key="spread_multiplier")
        submitted = st.form_submit_button("Analyze Spread")

    if submitted:
        try:
            st.session_state["vertical_spread"] = VerticalSpread(
                long_strike, short_strike, long_premium, short_premium, quantity, multiplier, option_type == 'Call')
        except ValueError as e:
            st.session_state.pop("vertical_spread", None)
            st.error(str(e))
            return

    spread = st.session_state.get("vertical_spread")
    if spread is None:
        return

    st.subheader(f"{spread.strategy} Spread")
    entry = "Debit" if spread.entry_debit > 0 else ("Credit" if spread.entry_debit < 0 else "Even")
    first, second, third = st.columns(3)
    first.metric(f"Entry {entry}", f"${abs(spread.entry_debit):,.2f}")
    second.metric("Spread Width", f"${spread.width:,.2f}")
    third.metric("Expiration Breakeven", f"${spread.breakeven:,.2f}" if spread.breakeven is not None else "None")
    first, second = st.columns(2)
    first.metric("Maximum Expiration Profit", f"${spread.max_profit:,.2f}")
    second.metric("Maximum Expiration Loss", f"${spread.max_loss:,.2f}")
    st.caption(f"Submitted position: {spread.quantity} spread(s), multiplier {spread.multiplier}.")
    if spread.breakeven is None:
        st.warning(f"These entry premiums give expiration P&L between ${spread.min_pnl:,.2f} and ${spread.max_pnl:,.2f}, with no breakeven.")
    elif spread.min_pnl == 0 or spread.max_pnl == 0:
        st.caption("Breakeven marks the edge of a zero-P&L price range.")

    st.subheader("Expiration P&L")
    show_legs = st.checkbox("Show Individual Legs", key="spread_show_legs")
    fig = spread.plot_payoff(show_legs)
    st.pyplot(fig)
    plt.close(fig)
