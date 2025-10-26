import streamlit as st
from time import strptime
from models.newton_raphson import ImpliedVolatilityFinder
from utils import fetch_option_price, get_nearest_friday_from_T

def show_implied_volatility_tab(S, K, T, r, is_call, ticker):
    st.header("Implied Volatility Finder")

    if ticker:
        expiry = str(get_nearest_friday_from_T(T))
        option_price = fetch_option_price(ticker, K, expiry, is_call)
        if option_price is None:
            st.error("Failed to fetch option price. Please enter it manually.")
            option_price = st.number_input("Market Option Price", value=10.0, step=0.1, min_value=0.01)
        else:
            st.success(f"Fetched market option price: ${option_price:.2f}")

    else:
        option_price = st.number_input("Market Option Price", value=10.0, step=0.1, min_value=0.01)


    iv_finder = ImpliedVolatilityFinder()
    implied_vol = iv_finder.find_iv(option_price, S, K, T, r, call=is_call)

    if implied_vol is not None:
        st.write(f"Implied Volatility: {implied_vol:.2f}")
        st.write("You can now feed this volatility back into the other tabs for pricing and Greeks calculation.")
    else:
        st.error("Implied Volatility could not be determined with the given parameters.")