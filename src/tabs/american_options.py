import streamlit as st
from models.binomial_tree import BinomialTreePricer

def show_american_options_tab(S, K, T, r, sigma, is_call, ticker):
    steps = st.slider("Steps", value=100, min_value=10, max_value=500, step=10)
    st.write("note: the closer the expiration date, the less steps are needed for convergence.")

    try: 
        option = BinomialTreePricer(
            S=S, K=K, T=T, r=r, sigma=sigma, steps=steps, call=is_call, ticker=ticker)
        
        type = "Call" if is_call else "Put"
        st.subheader(f"**{type} Option Price:** ${option.price:.2f}")
        st.code(option)

    except Exception as e:
        st.error(f"An error occurred: {e}")
