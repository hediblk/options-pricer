import streamlit as st
import matplotlib.pyplot as plt
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
            for title, plot in (
                ("Histogram of Simulated Asset Prices at Maturity", option.plot_histogram),
                ("Convergence of Monte Carlo Price Estimate", option.plot_convergence),
                ("Simulated Asset Price Paths", option.plot_paths),
            ):
                st.subheader(title)
                fig = plot()
                st.pyplot(fig)
                plt.close(fig)

    except Exception as e:
        st.error(f"Error: {e}")
