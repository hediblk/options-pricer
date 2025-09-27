import numpy as np
import matplotlib.pyplot as plt
from utils import fetch_latest_price


class MonteCarloPricer:
    """
    Monte Carlo simulation for pricing European call and put options
    """

    def __init__(self, S=100, K=105, T=1, r=0.05, sigma=0.2, N=1000, call=True, ticker=None, seed=None):
        if ticker:
            self.S = fetch_latest_price(ticker)
        else:
            self.S = S

        if seed is not None:
            np.random.seed(seed)

        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.N = N
        self.call = call
        self.ticker = ticker

        self.price, self.SE = self.run_simulation()

    def run_simulation(self):
        Z = np.random.randn(self.N)

        self.S_T = self.S * np.exp((self.r - 0.5 * self.sigma**2) * self.T + self.sigma * np.sqrt(self.T) * Z)

        if self.call:
            payoff = np.maximum(self.S_T - self.K, 0)
        else:
            payoff = np.maximum(self.K - self.S_T, 0)

        price = np.exp(-self.r * self.T) * payoff.mean()

        SE = np.exp(-self.r * self.T) * payoff.std(ddof=1) / np.sqrt(self.N)

        return price, SE
    
    def plot_histogram(self, bins=50):
        plt.hist(self.S_T, bins=bins, edgecolor='black', alpha=0.7)
        plt.title('Histogram of Simulated Asset Prices at Maturity')
        plt.xlabel('Asset Price at Maturity')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

    def plot_convergence(self):
        cumulative_payoff = np.cumsum(np.maximum(self.S_T - self.K, 0) if self.call else np.maximum(self.K - self.S_T, 0))
        cumulative_average = np.exp(-self.r * self.T) * cumulative_payoff / np.arange(1, self.N + 1)

        plt.plot(cumulative_average)
        plt.title('Convergence of Monte Carlo Price Estimate')
        plt.xlabel('Number of Simulations')
        plt.ylabel('Estimated Option Price')
        plt.grid(True)
        plt.show()

    def plot_paths(self, num_paths=20, time_steps=100):
        dt = self.T / time_steps
        paths = np.zeros((num_paths, time_steps + 1))
        paths[:, 0] = self.S

        for t in range(1, time_steps + 1):
            Z = np.random.randn(num_paths)
            paths[:, t] = paths[:, t - 1] * np.exp((self.r - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * Z)

        for i in range(num_paths):
            plt.plot(paths[i], lw=1)

        plt.title('Simulated Asset Price Paths')
        plt.xlabel('Time Steps')
        plt.ylabel('Asset Price')
        plt.grid(True)
        plt.show()

    def __repr__(self):
        if self.ticker:
            return (f"{self.ticker} ({self.T:<.2f}y) {self.K:<.2f} {'Call' if self.call else 'Put'} (MC): ${self.price:.2f}, SE: {self.SE:.2f}")

        return (f"MonteCarloPricer(S={self.S:<.2f}, K={self.K:<.2f}, T={self.T:<.2f}, r={self.r:<.2f}, sigma={self.sigma:<.2f}, N={self.N}, {'Call' if self.call else 'Put'}) --> "
                f"${self.price:.2f}, SE: {self.SE:.2f}")
