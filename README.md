# Options Pricer

[Live dashboard](https://hediblk-options-pricer.streamlit.app/)

## Goal

This is my attempt at implementing the Black-Scholes, Binomial Tree, and Monte Carlo models in Python for pricing European and American call and put options. The implementation also includes the ability to fetch current stock/ETF prices using the `yfinance` library so it is for example possible to price an SPY call option using the current SPY price.

You can also find the implied volatility given a market option price using the Newton Raphson root finding method.

## Streamlit dashboard

Install the dependencies and run the dashboard:

```bash
uv sync --locked
uv run --frozen streamlit run src/app.py
```

A new browser window should open with the dashboard at `http://localhost:8501`. If not, you can manually open this address in your browser.

## Hosting a public demo

Keep Streamlit and deploy on [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud), which offers free hosting connected to GitHub:

1. Push the dashboard changes to `hediblk/options-pricer` on GitHub.
2. Sign in to [Community Cloud](https://share.streamlit.io/) with GitHub and select **Create app**.
3. Select repository `hediblk/options-pricer`, branch `main`, and entrypoint `src/app.py`.
4. In **Advanced settings**, select Python **3.11** to match the locally verified environment. No app secrets are required.
5. Choose an available `*.streamlit.app` subdomain, deploy, and set the app's sharing settings to public.
6. Open the URL in a signed-out browser to verify access, then include the demo and GitHub repository links in your CV.

Community Cloud supports the existing `uv.lock`, so a separate `requirements.txt` is unnecessary. See the official [dependency](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies) and [deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) instructions.

Apps [sleep after 12 hours without traffic](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app#app-hibernation); visitors can wake them. If an always-available demo is essential, use a paid Python web service such as Render instead. Streamlit can run there without a framework migration.

[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) serves static websites and cannot run this Python app. It can host a portfolio page that links to the dashboard.

## Model and data notes

- Pricing assumes constant volatility and interest rates, with no dividends. Black–Scholes and Monte Carlo price European options; the CRR tree allows American exercise.
- Yahoo Finance supplies the latest available daily close, rather than a streaming quote. Stock prices and option midpoints are cached for five minutes. When quotes are unavailable, the dashboard accepts manual inputs.
- Implied volatility uses a bounded Newton–Raphson solver with bisection fallback between 1% and 200%. A price outside that range produces a message instead of an invalid result. Stock option quotes may be American, so their European-model IV is an approximation.
- Greeks use annual theta and vega/rho per 1.0 change in volatility/rate. Divide vega or rho by 100 for a one percentage point change.
- Low volatility combined with high rates can require more tree steps for valid CRR probabilities; the dashboard reports the required minimum.
