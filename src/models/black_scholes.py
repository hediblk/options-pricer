from utils import fetch_stock_price
import math
from scipy.stats import norm


class BlackScholesPricer:
    """
    Black-Scholes model for pricing European call and put options
    """

    def __init__(self, S=None, K=105, T=1, r=0.05, sigma=0.2, call=True, ticker=None):
        self.S = S if S is not None else (fetch_stock_price(ticker) if ticker else 100)
        if not all(math.isfinite(x) for x in (self.S, K, T, r, sigma)):
            raise ValueError("Parameters must be finite.")
        if self.S <= 0 or K <= 0 or T < 0 or sigma < 0:
            raise ValueError("Prices must be positive; maturity and volatility must be nonnegative.")

        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.call = call
        self.ticker = ticker

        if T == 0 or sigma == 0:
            forward_payoff = self.S - K * math.exp(-r * T)
            self.d1 = self.d2 = math.inf if forward_payoff > 0 else (-math.inf if forward_payoff < 0 else 0.0)
        else:
            self.d1 = (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
            self.d2 = self.d1 - self.sigma * math.sqrt(self.T)

        self.price = self.compute_price()
        self.delta = self.compute_delta()
        self.gamma = self.compute_gamma()
        self.vega = self.compute_vega()
        self.theta = self.compute_theta()
        self.rho = self.compute_rho()

    def compute_price(self):
        if self.call:
            return self.S * norm.cdf(self.d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2)
        else:
            return self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def compute_delta(self):
        if self.call:
            return norm.cdf(self.d1)
        else:
            return norm.cdf(self.d1) - 1

    def compute_gamma(self):
        if self.T <= 0 or self.sigma <= 0:
            return 0.0

        return norm.pdf(self.d1) / (self.S * self.sigma * math.sqrt(self.T))

    def compute_vega(self):
        if self.T <= 0 or self.sigma <= 0:
            return 0.0

        return self.S * norm.pdf(self.d1) * math.sqrt(self.T)

    def compute_theta(self):
        if self.T <= 0:
            return 0.0

        if self.call:
            return (-self.S * norm.pdf(self.d1) * self.sigma / (2 * math.sqrt(self.T)) -
                    self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2))
        else:
            return (-self.S * norm.pdf(self.d1) * self.sigma / (2 * math.sqrt(self.T)) +
                    self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2))

    def compute_rho(self):
        if self.call:
            return self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(self.d2)
        else:
            return -self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(-self.d2)

    def __repr__(self):
        if self.ticker:
            return (f"{self.ticker} ({self.T:<.2f}y) {self.K:<.2f} {'Call' if self.call else 'Put'}: ${self.price:.2f}")

        return (f"BlackScholesPricer(S={self.S:<.2f}, K={self.K:<.2f}, T={self.T:<.2f}, r={self.r:<.2f}, sigma={self.sigma:<.2f}, {'Call' if self.call else 'Put'}) = ${self.price:.2f}")
