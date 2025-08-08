import math
from scipy.stats import norm


class BlackScholesPricer:
    """
    Black-Scholes model for pricing European call or put options
    """

    def __init__(self, S, K, T, r=0.05, sigma=0.2, call=True):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.call = call

        self.price = self.compute_price()

        # to add later: self.delta, self.gamma, self.vega, self.theta, self.rho

    def compute_price(self):

        if self.T <= 0 or self.sigma <= 0:
            if self.call:
                return max(0.0, self.S - self.K)
            else:
                return max(0.0, self.K - self.S)

        d1 = (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
        d2 = d1 - self.sigma * math.sqrt(self.T)

        if self.call:
            return self.S * norm.cdf(d1) - self.K * math.exp(-self.r * self.T) * norm.cdf(d2)
        else:
            return self.K * math.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)


