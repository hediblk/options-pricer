# Options Pricer

### Goal
This is my attempt at implementing the Black-Scholes, Binomial Tree, and Monte Carlo models in Python for pricing European and American call and put options. The implementation also includes the ability to fetch current stock/ETF prices using the `yfinance` library so it is for example possible to price an SPY call option using the current SPY price.

You can also find the implied volatility given a market option price using the Newton Raphson root finding method.



### Streamlit dashboard
To run it, use the command:
```
streamlit run src/app.py
```
A new browser window should open with the dashboard at `http://localhost:8501`. If not, you can manually open this address in your browser.