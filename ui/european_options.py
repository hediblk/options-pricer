import streamlit as st
import pandas as pd
from black_scholes import BlackScholesPricer


def show_european_options_tab(S, K, T, r, sigma, is_call, ticker):

    try:
        
        option = BlackScholesPricer(
                S=S, K=K, T=T, r=r, sigma=sigma, call=is_call, ticker=ticker)
        """
        else:
            option = BlackScholesPricer(
                S=S, K=K, T=T, r=r, sigma=sigma, call=is_call)
        """

        type = "Call" if is_call else "Put"
        st.subheader(f"**{type} Option Price:** ${option.price:.2f}")

        show_details = st.checkbox("Show Greeks")

        if show_details:
            greeks_data = [
                {"Greek": "Delta", "Value": option.delta.round(4)},
                {"Greek": "Gamma", "Value": option.gamma.round(4)},
                {"Greek": "Vega", "Value": option.vega.round(4)},
                {"Greek": "Theta", "Value": option.theta.round(4)},
                {"Greek": "Rho", "Value": option.rho.round(4)}
            ]

            greeks_data = pd.DataFrame(greeks_data).set_index('Greek').T
            st.dataframe(data=greeks_data, hide_index=True)

        st.code(option)

    except Exception as e:
        st.error(f"An error occurred: {e}")
