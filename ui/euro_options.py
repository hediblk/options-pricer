import streamlit as st
import pandas as pd
from black_scholes import BlackScholesPricer


def show_euro_options_tab(S, K, T, r, sigma, is_call, ticker, show_details):

    try:
        #if ticker:
        option = BlackScholesPricer(
                K=K, T=T, r=r, sigma=sigma, call=is_call, ticker=ticker)
        """
        else:
            option = BlackScholesPricer(
                S=S, K=K, T=T, r=r, sigma=sigma, call=is_call)
        """

        type = "Call" if is_call else "Put"
        st.subheader(f"**{type} Option Price:** ${option.price:.2f}")

        if show_details:
            st.subheader("Greeks")
            # display greeks in a table/df format instead of individual lines
            greeks_data = {
                "Delta": option.delta.round(4),
                "Gamma": option.gamma.round(4),
                "Vega": option.vega.round(4),
                "Theta": option.theta.round(4),
                "Rho": option.rho.round(4)
            }
            df = pd.DataFrame(data=greeks_data, index=[0])
            st.write(df, use_container_width=True)

        st.info(option)

    except Exception as e:
        st.error(f"An error occurred: {e}")
