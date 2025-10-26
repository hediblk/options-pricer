from models.black_scholes import BlackScholesPricer
import numpy as np


class ImpliedVolatilityFinder:
    """
    Newton Raphson IV solver
    """

    def __init__(self, initial_sigma=0.20, tol=0.01, max_iter=100, clamp=(0.01, 2.0)):

        self.sigma0 = initial_sigma
        self.tol = tol
        self.max_iter = max_iter
        self.low, self.high = clamp

    def find_iv(self, option_price, S, K, T, r, call=True):
        sigma = self.sigma0

        for _ in range(self.max_iter):
            pricer = BlackScholesPricer(S, K, T, r, sigma, call)
            price = pricer.price
            diff = price - option_price

            if abs(diff) < self.tol:
                return sigma

            v = pricer.vega
            if not np.isfinite(v) or abs(v) < 1e-12:
                eps = 1e-4
                up = BlackScholesPricer(S, K, T, r, sigma + eps, call).price
                down = BlackScholesPricer(S, K, T, r, sigma - eps, call).price
                v = (up - down) / (2 * eps)

            if not np.isfinite(v) or v == 0.0:
                break

            sigma -= diff / v
            if sigma <= self.low:
                sigma = (self.low + sigma) / 2.0
            if sigma >= self.high:
                sigma = (self.high + sigma) / 2.0

        return None

