import streamlit as st
import pandas as pd
from models.black_scholes import BlackScholesPricer


def show_european_options_tab(S, K, T, r, sigma, is_call, ticker):

    try:
        
        option = BlackScholesPricer(
                S=S, K=K, T=T, r=r, sigma=sigma, call=is_call, ticker=ticker)

        type = "Call" if is_call else "Put"
        st.subheader(f"**{type} Option Price:** ${option.price:.2f}")

        show_details = st.checkbox("Show Greeks")

        if show_details:
            greeks_data = [
                {"Greek": "Delta", "Value": round(option.delta, 4)},
                {"Greek": "Gamma", "Value": round(option.gamma, 4)},
                {"Greek": "Vega", "Value": round(option.vega, 4)},
                {"Greek": "Theta", "Value": round(option.theta, 4)},
                {"Greek": "Rho", "Value": round(option.rho, 4)}
            ]

            greeks_data = pd.DataFrame(greeks_data).set_index('Greek').T
            st.dataframe(data=greeks_data, hide_index=True)
            st.caption("Theta is per year. Vega and rho are per 1.0 change; divide by 100 for a one percentage point change.")

        st.code(option)

    except Exception as e:
        st.error(f"An error occurred: {e}")
