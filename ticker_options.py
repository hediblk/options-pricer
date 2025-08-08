import yfinance as yf
from black_scholes import BlackScholesPricer


def fetch_latest_price(ticker):
    try:
        data = yf.download(ticker, period="1d",
                           interval="1d", auto_adjust=True, progress=False)
        if data.empty:
            raise ValueError("No data returned")
        
        latest_price = data["Close"].iloc[-1].item()
        return latest_price
    
    except Exception as e:
        raise RuntimeError(f"Error fetching price for {ticker}: {e}")


def main():
    ticker = "SPY"
    S = fetch_latest_price(ticker)
    print(f"{ticker}: ${S:.2f}")

    K = 450
    T = 0.5
    r = 0.05
    sigma = 0.2
    call = True

    pricer = BlackScholesPricer(S=S, K=K, T=T, r=r, sigma=sigma, call=call)

    option_type = "Call" if call else "Put"
    print(f"{ticker} ({T}y) {K} {option_type}: ${pricer.price:.2f}")


if __name__ == "__main__":
    main()
