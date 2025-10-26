import math
import numpy as np
from utils import fetch_stock_price


class BinomialTreePricer:
    """
    Binomial Tree model for pricing American call and put options
    Cox-Ross-Rubinstein (CRR) formulation is used for up and down factors.
    """

    def __init__(self, S=100, K=105, T=1, r=0.05, sigma=0.2, steps=100, call=True, ticker=None):
        if ticker:
            self.S = fetch_stock_price(ticker)
        else:
            self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.steps = steps
        self.call = call
        self.ticker = ticker
        
        self.dt = T / steps
        self.u = math.exp(sigma * math.sqrt(self.dt))
        self.d = 1 / self.u
        self.disc = math.exp(-r * self.dt)
        self.p = (math.exp(r * self.dt) - self.d) / (self.u - self.d)

        if not (0 <= self.p <= 1):
            raise ValueError(
                "Invalid probabilities (increase n or check params).")

        self.price = self.compute_price()

    def compute_price(self):
        option_values = np.zeros(self.steps + 1)

        for i in range(self.steps + 1):
            S_T = self.S * (self.u ** (self.steps - i)) * (self.d ** i)
            if self.call:
                option_values[i] = max(0, S_T - self.K)
            else:
                option_values[i] = max(0, self.K - S_T)

        for i in range(self.steps - 1, -1, -1):
            for j in range(i + 1):
                continuation = self.disc * (self.p * option_values[j] +(1 - self.p) * option_values[j + 1])
                S_ij = self.S * (self.u ** (i - j)) * (self.d ** j)
                
                if self.call:
                    exercise = max(0, S_ij - self.K)
                else:
                    exercise = max(0, self.K - S_ij)
                option_values[j] = max(exercise, continuation)

        return option_values[0]
    
    def __repr__(self):
        if self.ticker:
            return (f"{self.ticker} ({self.T:<.2f}y) {self.K:<.2f} {'Call' if self.call else 'Put'}: ${self.price:.2f}")

        return (f"BinomialTreePricer(S={self.S:<.2f}, K={self.K:<.2f}, T={self.T:<.2f}, r={self.r:<.2f}, sigma={self.sigma:<.2f}, {'Call' if self.call else 'Put'}) = ${self.price:.2f}")
