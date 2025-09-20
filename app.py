import streamlit as st
from black_scholes import BlackScholesPricer

st.title("Options Pricer")
st.write("Calculate European option prices and Greeks using the Black-Scholes model.")

# sidebar
st.sidebar.header("Parameters")

price_method = st.sidebar.radio("Choose Price Input Method", ('Enter Price Manually', 'Fetch live ticker price'))

S = None
ticker = None

if price_method == 'Enter Price Manually':
    S = st.sidebar.number_input("Underlying Price (S)", value=100.0, step=1.0)
else:
    ticker = st.sidebar.text_input("Ticker", value="SPY")

K = st.sidebar.number_input("Strike Price (K)", value=105.0, step=1.0)
T = st.sidebar.number_input("Time to Maturity (T in years)", value=1.0, step=0.1)
r = st.sidebar.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05)
sigma = st.sidebar.slider("Volatility (sigma)", 0.01, 1.0, 0.2)
option_type = st.sidebar.selectbox("Option Type", ('Call', 'Put'))
show_details = st.sidebar.checkbox("Show Detailed Data (Greeks)")

is_call = (option_type == 'Call')



# center panel
if st.sidebar.button("Calculate"):
    try:
        if ticker:
            option = BlackScholesPricer(K=K, T=T, r=r, sigma=sigma, call=is_call, ticker=ticker)
        else:
            option = BlackScholesPricer(S=S, K=K, T=T, r=r, sigma=sigma, call=is_call)

        st.header("Results")
        st.write(f"**Option Price:** ${option.price:.2f}")

        if show_details:
            st.subheader("Greeks")
            st.write(f"**Delta:** {option.delta:.2f}")
            st.write(f"**Gamma:** {option.gamma:.2f}")
            st.write(f"**Vega:** {option.vega:.2f}")
            st.write(f"**Theta:** {option.theta:.2f}")
            st.write(f"**Rho:** {option.rho:.2f}")

        st.info(option)

    except Exception as e:
        st.error(f"An error occurred: {e}")
