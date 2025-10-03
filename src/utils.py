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

def get_T_from_datetime(date, today=None):
    if today is None:
        today = datetime.date.today()

    if date < today:
        raise ValueError("Date must be in the future")

    delta = date - today
    return delta.days / 365.0


def get_next_fridays(n=52, today=None):
    if today is None:
        today = datetime.date.today()

    days_ahead = 4 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7

    next_fridays = {}

    # no 0dte if today is friday
    # it will break black scholes

    for i in range(n):
        next_friday = today + datetime.timedelta(days=days_ahead + i * 7)
        T = (next_friday - today).days / 365.0
        key = f"{next_friday.strftime('%d-%m-%Y')} ({(next_friday - today).days} days)"
        next_fridays[key] = T

    return next_fridays

def get_num_days_from_T(T, today=None):
    if today is None:
        today = datetime.date.today()
    target = today + datetime.timedelta(days=int(round(T * 365)))
    return (target - today).days


if __name__ == "__main__":
    print(get_next_fridays(3))