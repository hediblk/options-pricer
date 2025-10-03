import streamlit as st
from models.monte_carlo import MonteCarloPricer

def show_monte_carlo_tab(S, K, T, r, sigma, is_call, ticker):
    N = st.slider("Number of Simulations", value=200, min_value=100, max_value=1000, step=10)

    try: 
        option = MonteCarloPricer(
            S=S, K=K, T=T, r=r, sigma=sigma, N=N, call=is_call, ticker=ticker, seed=42)
        
        type = "Call" if is_call else "Put"
        st.subheader(f"**{type} Option Price:** ${option.price:.2f}")
        st.write(f"**Standard Error:** ${option.SE:.2f}")
        st.code(option)

        show_plots = st.checkbox("Show Plots")
        if show_plots:
            st.subheader("Histogram of Simulated Asset Prices at Maturity")
            st.pyplot(option.plot_histogram())

            st.subheader("Convergence of Monte Carlo Price Estimate")
            st.pyplot(option.plot_convergence())

            st.subheader("Simulated Asset Price Paths")
            st.pyplot(option.plot_paths())

    except Exception as e:
        st.error(f"Error: {e}")
