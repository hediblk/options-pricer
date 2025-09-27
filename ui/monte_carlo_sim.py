import streamlit as st


def show_monte_carlo_tab(S, K, T, r, sigma, is_call, ticker):
    steps = st.slider("N", value=100, min_value=10, max_value=500, step=10)

    st.write("Coming soon...")
