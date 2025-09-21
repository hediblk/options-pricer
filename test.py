import math
from black_scholes import BlackScholesPricer
from monte_carlo import MonteCarloPricer
import datetime
from utils import fetch_latest_price, get_nearest_friday_from_T, get_T_from_datetime


def test_spy_option():
    option = BlackScholesPricer(ticker="SPY", K=700)

    print(option)

    print(f"Delta: {option.delta:.2f}")
    print(f"Gamma: {option.gamma:.2f}")
    print(f"Theta: {option.theta:.2f}")
    print(f"Vega: {option.vega:.2f}")
    print(f"Rho: {option.rho:.2f}")


def test_price_fetch():
    print(fetch_latest_price("SPY"))


def test_fridays():
    print(get_nearest_friday_from_T(0.0))
    print(get_nearest_friday_from_T(0.1))
    print(get_nearest_friday_from_T(0.5))
    print(get_nearest_friday_from_T(1.0))

def test_BS_vs_MC():
    bs_call = BlackScholesPricer()
    bs_put = BlackScholesPricer(call=False)
    mc_call = MonteCarloPricer(call=True, seed=42)
    mc_put = MonteCarloPricer(call=False, seed=42)

    print(f"Call BS: {bs_call.price:.4f}")
    print(f"Call MC: {mc_call.price:.4f}, SE: {mc_call.SE:.4f}")

    print(f"Put BS : {bs_put.price:.4f}")
    print(f"Put MC : {mc_put.price:.4f}, SE: {mc_put.SE:.4f}")

def test_MC_plots():
    mc_call = MonteCarloPricer(call=True, seed=42, num_paths=1000, num_steps=100)
    mc_call.plot_histogram()
    mc_call.plot_convergence()
    mc_call.plot_paths()


def test_get_T_from_datetime():
    print(get_T_from_datetime(datetime.date(2025, 9, 26)))
    print(BlackScholesPricer(T=get_T_from_datetime(datetime.date(2025, 9, 26))))