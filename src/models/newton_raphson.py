from models.black_scholes import BlackScholesPricer
import numpy as np


class ImpliedVolatilityFinder:
    """
    Newton Raphson IV solver
    """

    def __init__(self, initial_sigma=0.20, tol=1e-8, max_iter=100, clamp=(0.01, 2.0)):

        self.sigma0 = initial_sigma
        self.tol = tol
        self.max_iter = max_iter
        self.low, self.high = clamp

    def find_iv(self, option_price, S, K, T, r, call=True):
        if not all(np.isfinite(x) for x in (option_price, S, K, T, r)):
            return None
        if S <= 0 or K <= 0 or T <= 0 or option_price < 0:
            return None

        low, high = self.low, self.high
        low_price = BlackScholesPricer(S, K, T, r, low, call).price
        high_price = BlackScholesPricer(S, K, T, r, high, call).price
        if option_price < low_price - self.tol or option_price > high_price + self.tol:
            return None
        if abs(option_price - low_price) < self.tol:
            return low
        if abs(option_price - high_price) < self.tol:
            return high

        sigma = float(np.clip(self.sigma0, low, high))

        for _ in range(self.max_iter):
            pricer = BlackScholesPricer(S, K, T, r, sigma, call)
            price = pricer.price
            diff = price - option_price

            if abs(diff) < self.tol:
                return sigma

            if diff > 0:
                high = sigma
            else:
                low = sigma

            candidate = sigma - diff / pricer.vega if pricer.vega > 1e-12 else np.nan
            sigma = candidate if low < candidate < high else (low + high) / 2

        return None

