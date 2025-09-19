import datetime
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


def get_nearest_friday_from_T(T, today=None):
    if today is None:
        today = datetime.date.today()

    target = today + datetime.timedelta(days=int(round(T * 365)))

    offset = (4 - target.weekday()) % 7  # Friday=4
    friday_after = target + datetime.timedelta(days=offset)
    friday_before = target - datetime.timedelta(days=(7 - offset) % 7)

    if abs((friday_after - target).days) < abs((friday_before - target).days):
        return friday_after
    return friday_before

