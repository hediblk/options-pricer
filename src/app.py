import streamlit as st
from utils import get_next_fridays, fetch_latest_price
from tabs.european_options import show_european_options_tab
from tabs.american_options import show_american_options_tab
from tabs.monte_carlo_sim import show_monte_carlo_tab

st.title("Options Pricer")

# Sidebar for user inputs (shared across tabs)
st.sidebar.header("Parameters")

price_method = st.sidebar.radio("Choose Price Input Method", ('Enter Price Manually', 'Fetch live ticker price'))
S = None
ticker = None
default_K = 105.0

if price_method == 'Enter Price Manually':
    S = st.sidebar.number_input("Underlying Price (S)", value=100.0, step=1.0, min_value=0.01)
else:
    ticker = st.sidebar.text_input("Ticker", value="SPY")
    if ticker:
        S = fetch_latest_price(ticker)
        if S is None:
            st.sidebar.error("Failed to fetch price. Please check the ticker symbol.")
            S = st.sidebar.number_input("Underlying Price (S)", value=100.0, step=1.0, min_value=0.01)
        else:
            st.sidebar.success(f"Fetched live price for {ticker}: ${S:.2f}")
            default_K = S

date_method = st.sidebar.radio("Choose Maturity Input Method", ('Enter T in years', 'Use calendar'))

if date_method == 'Enter T in years':
    T = st.sidebar.number_input(
        "Time to Maturity (T in years)", value=1.0, step=0.05, min_value=0.01, max_value=2.0)
else:
    next_fridays = get_next_fridays(n=53)
    selected_date = st.sidebar.selectbox("Select Expiration Date", list(next_fridays.keys()))
    T = next_fridays[selected_date]

option_type = st.sidebar.selectbox("Option Type", ('Call', 'Put'))
is_call = (option_type == 'Call')

K = st.sidebar.number_input("Strike Price (K)", value=default_K, step=1.0, min_value=0.01)
r = st.sidebar.slider("Risk-Free Rate (r)", value=0.05, min_value=0.01, max_value=0.25)
sigma = st.sidebar.slider("Volatility (sigma)", value=0.2, min_value=0.01, max_value=2.0)


# Top menu bar with tabs
tab1, tab2, tab3 = st.tabs(["European Options", "American Options", "Monte Carlo Sim"])

with tab1:
    show_european_options_tab(S, K, T, r, sigma, is_call, ticker)

with tab2:
    show_american_options_tab(S, K, T, r, sigma, is_call, ticker)

with tab3:
    show_monte_carlo_tab(S, K, T, r, sigma, is_call, ticker)
