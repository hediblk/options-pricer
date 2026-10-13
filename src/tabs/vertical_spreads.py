import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from models.vertical_spread import VerticalSpread


EXAMPLES = {
    "Bull Call": ('Call', 100.0, 105.0, 3.0, 1.0),
    "Bear Call": ('Call', 105.0, 100.0, 1.0, 3.0),
    "Bull Put": ('Put', 95.0, 100.0, 1.0, 2.5),
    "Bear Put": ('Put', 100.0, 95.0, 2.5, 1.0),
}
INPUT_KEYS = ("option_type", "long_strike", "short_strike", "long_premium", "short_premium")


def load_spread_example():
    example = EXAMPLES.get(st.session_state["spread_example"])
    if example is not None:
        for key, value in zip(INPUT_KEYS, example):
            st.session_state[f"spread_{key}"] = value
        st.session_state["spread_quantity"] = 1
        st.session_state["spread_multiplier"] = 100
        st.session_state.pop("vertical_spread", None)


def show_vertical_spreads_tab():
    st.header("Vertical Spread Analyzer")
    st.caption("Both legs share one expiry. Premiums are per share; P&L is for the entire position, before fees.")
    for key, value in zip(INPUT_KEYS, EXAMPLES["Bull Call"]):
        st.session_state.setdefault(f"spread_{key}", value)
    st.session_state.setdefault("spread_multiplier", 100)
    st.selectbox("Example Preset", ("Custom", *EXAMPLES), key="spread_example", on_change=load_spread_example)

    with st.form("vertical_spread_form"):
        option_type = st.selectbox("Spread Option Type", ('Call', 'Put'), key="spread_option_type")
        long, short = st.columns(2)
        with long:
            long_strike = st.number_input("Long Strike", min_value=0.01, step=1.0, key="spread_long_strike")
            long_premium = st.number_input("Premium Paid", min_value=0.0, step=0.1, key="spread_long_premium")
        with short:
            short_strike = st.number_input("Short Strike", min_value=0.01, step=1.0, key="spread_short_strike")
            short_premium = st.number_input("Premium Received", min_value=0.0, step=0.1, key="spread_short_premium")
        quantity = st.number_input("Number of Spreads", min_value=1, step=1, key="spread_quantity")
        multiplier = st.number_input("Contract Multiplier", min_value=1, step=1, key="spread_multiplier")
        submitted = st.form_submit_button("Analyze Spread")

    if submitted:
        try:
            st.session_state["vertical_spread"] = VerticalSpread(
                long_strike, short_strike, long_premium, short_premium, quantity, multiplier, option_type == 'Call')
            st.session_state.pop("spread_expiration_price", None)
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

    st.subheader("Inspect Expiration P&L")
    default_price = spread.breakeven if spread.breakeven is not None else (spread.long_strike + spread.short_strike) / 2
    S = st.number_input("Underlying Price at Expiration", value=float(default_price), min_value=0.0, step=1.0, key="spread_expiration_price")
    long_payoff, short_payoff = spread.leg_payoffs(S)
    long_cash = -spread.long_premium * spread.size
    short_cash = spread.short_premium * spread.size
    option_type = "Call" if spread.call else "Put"
    rows = [
        {"Leg": f"Long {option_type}", "Strike": spread.long_strike, "Payoff ($)": long_payoff,
         "Entry Cash Flow ($)": long_cash, "P&L ($)": long_payoff + long_cash},
        {"Leg": f"Short {option_type}", "Strike": spread.short_strike, "Payoff ($)": short_payoff,
         "Entry Cash Flow ($)": short_cash, "P&L ($)": short_payoff + short_cash},
        {"Leg": "Spread", "Strike": None, "Payoff ($)": long_payoff + short_payoff,
         "Entry Cash Flow ($)": -spread.entry_debit, "P&L ($)": spread.expiration_pnl(S)},
    ]
    st.dataframe(pd.DataFrame(rows).round(2), hide_index=True)
    st.caption("Positive cash flow is received; negative cash flow is paid.")
