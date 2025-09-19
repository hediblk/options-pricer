# Options Pricer

### Goal
This is my attempt at implementing the Black-Scholes model and Monte Carlo simulations in Python for pricing European call and put options. The implementation also includes the ability to fetch current stock/ETF prices using the `yfinance` library so it is for example possible to price an SPY call option using the current SPY price.


### Next steps
Next step is to add support for American options using the Binomial tree model as well as some form of implied volatility estimation.
The end goal is to then integrate these models into a user interface for easier interaction and visualization of option pricing scenarios.