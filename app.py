import streamlit as st
from ui.european_options import show_european_options_tab
from ui.american_options import show_american_options_tab
from ui.monte_carlo_sim import show_monte_carlo_tab

st.title("Options Pricer")

# Sidebar for user inputs (shared across tabs)
st.sidebar.header("Parameters")

price_method = st.sidebar.radio(
    "Choose Price Input Method", ('Enter Price Manually', 'Fetch live ticker price'))
S = None
ticker = None

if price_method == 'Enter Price Manually':
    S = st.sidebar.number_input("Underlying Price (S)", value=100.0, step=1.0, min_value=0.01)
else:
    ticker = st.sidebar.text_input("Ticker", value="SPY")

option_type = st.sidebar.selectbox("Option Type", ('Call', 'Put'))
is_call = (option_type == 'Call')

K = st.sidebar.number_input("Strike Price (K)", value=105.0, step=1.0, min_value=0.01)
T = st.sidebar.number_input(
    "Time to Maturity (T in years)", value=1.0, step=0.05, min_value=0.01, max_value=2.0)
r = st.sidebar.slider("Risk-Free Rate (r)", value=0.05, min_value=0.01, max_value=0.25)
sigma = st.sidebar.slider("Volatility (sigma)", value=0.2, min_value=0.01, max_value=2.0)
show_details = st.sidebar.checkbox("Show Greeks (only for Euro Options)")

# Top menu bar with tabs
tab1, tab2, tab3 = st.tabs(["European Options", "American Options", "Monte Carlo Sim"])

with tab1:
    show_european_options_tab(S, K, T, r, sigma, is_call, ticker, show_details)

with tab2:
    show_american_options_tab()

with tab3:
    show_monte_carlo_tab()
