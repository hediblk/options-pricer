import math
from scipy.stats import norm
from ticker_options import fetch_latest_price


class BlackScholesPricer:
    """
    Black-Scholes model for pricing European call or put options
    """

    def __init__(self, S=100, K=100, T=1, r=0.05, sigma=0.2, call=True, ticker=None):
        if ticker:
            self.S = fetch_latest_price(ticker)
        else:
            self.S = S
            
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.call = call
        self.ticker = ticker
        
        self.d1 = (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * math.sqrt(self.T)

        self.price = self.compute_price()
        self.delta = self.compute_delta()
        self.gamma = self.compute_gamma()
        self.vega = self.compute_vega()
        self.theta = self.compute_theta()
        self.rho = self.compute_rho()


    def compute_price(self):
        if self.T <= 0 or self.sigma <= 0:
            if self.call:
                return max(0.0, self.S - self.K)
            else:
                return max(0.0, self.K - self.S)

        if self.call:
            return self.S * norm.cdf(self.d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2)
        else:
            return self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def compute_delta(self):
        if self.T <= 0 or self.sigma <= 0:
            if self.call:
                return 1.0 if self.S > self.K else 0.0
            else:
                return -1.0 if self.S < self.K else 0.0

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
        if self.T <= 0 or self.sigma <= 0:
            if self.call:
                return -self.K * math.exp(-self.r * self.T) if self.S > self.K else 0.0
            else:
                return self.K * math.exp(-self.r * self.T) if self.S < self.K else 0.0

        if self.call:
            return (-self.S * norm.pdf(self.d1) * self.sigma / (2 * math.sqrt(self.T)) -
                    self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2))
        else:
            return (-self.S * norm.pdf(self.d1) * self.sigma / (2 * math.sqrt(self.T)) +
                    self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2))

    def compute_rho(self):
        if self.T <= 0 or self.sigma <= 0:
            if self.call:
                return self.K * self.T * math.exp(-self.r * self.T) if self.S > self.K else 0.0
            else:
                return -self.K * self.T * math.exp(-self.r * self.T) if self.S < self.K else 0.0

        d2 = (math.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
        if self.call:
            return self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(self.d2)
        else:
            return -self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(-self.d2)

    def __repr__(self):
        if self.ticker:
            return (f"{self.ticker} ({self.T}y) {self.K} {'Call' if self.call else 'Put'}: ${self.price:.2f}")
        
        return (f"BlackScholesPricer(S={self.S}, K={self.K}, T={self.T}, r={self.r}, sigma={self.sigma}, {'Call' if self.call else 'Put'}) --> ${self.price:.2f}")
