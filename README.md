# Options Pricer

### Goal
This is my attempt at implementing the Black-Scholes, Binomial Tree, and Monte Carlo models in Python for pricing European and American call and put options. The implementation also includes the ability to fetch current stock/ETF prices using the `yfinance` library so it is for example possible to price an SPY call option using the current SPY price.


### Next steps
Next step is to add some form of implied volatility calculation and feed it to all models. 

### Streamlit dashboard
You can currently interactively price European options with the Black Scholes model (Monte Carlo and Binomial Tree coming soon) using the Streamlit dashboard. To run it, use the command:
```
streamlit run src/app.py
```
A new browser window should open with the dashboard at `http://localhost:8501`. If not, you can manually open this address in your browser.