import yfinance as yf


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


