import streamlit as st
from models.newton_raphson import ImpliedVolatilityFinder
from utils import fetch_option_price, get_nearest_friday_from_T, get_T_from_datetime

fetch_option_price = st.cache_data(ttl=300, show_spinner=False)(fetch_option_price)

def show_implied_volatility_tab(S, K, T, r, is_call, ticker):
    st.header("Implied Volatility Finder")

    option_price = None
    if ticker:
        expiry_date = get_nearest_friday_from_T(T)
        expiry = expiry_date.isoformat()
        try:
            option_price = fetch_option_price(ticker, K, expiry, is_call)
        except Exception:
            option_price = None
        if option_price is None:
            st.warning("No valid option quote for this strike and expiry. Enter a market price below.")
        else:
            T = get_T_from_datetime(expiry_date)
            st.success(f"Option bid/ask midpoint ({expiry}): ${option_price:.2f}")

    if option_price is None:
        option_price = st.number_input("Market Option Price", value=10.0, step=0.1, min_value=0.01)


    iv_finder = ImpliedVolatilityFinder()
    implied_vol = iv_finder.find_iv(option_price, S, K, T, r, call=is_call)

    if implied_vol is not None:
        st.write(f"Implied Volatility: {implied_vol:.2%}")
        st.write("You can now feed this volatility back into the other tabs for pricing and Greeks calculation.")
    else:
        st.warning("No implied volatility between 1% and 200% matches this price and these inputs.")
