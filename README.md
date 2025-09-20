# Options Pricer

### Goal
This is my attempt at implementing the Black-Scholes model and Monte Carlo simulations in Python for pricing European call and put options. The implementation also includes the ability to fetch current stock/ETF prices using the `yfinance` library so it is for example possible to price an SPY call option using the current SPY price.


### Next steps
Next step is to add support for American options using the Binomial tree model as well as some form of implied volatility estimation.

### Streamlit dashboard
You can currently interactively price European options with the Black Scholes model (Monte Carlo coming soon) using the Streamlit dashboard. To run it, use the command:
```
streamlit run app.py
```
A new browser window should open with the dashboard at `http://localhost:8501`. If not, you can manually open this address in your browser.