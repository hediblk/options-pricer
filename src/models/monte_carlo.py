import numpy as np
import matplotlib.pyplot as plt
from utils import fetch_latest_price, get_num_days_from_T


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

        return price, float(SE)
    
    def plot_histogram(self, bins=50):
        fig, ax = plt.subplots()
        ax.hist(self.S_T, bins=bins, edgecolor='black', alpha=0.7)
        ax.set_title(f'Histogram of Simulated Asset Prices at Maturity T={self.T:.2f}y')
        ax.set_xlabel('Asset Price at Maturity')
        ax.set_ylabel('Frequency')
        ax.grid(True)
        fig.tight_layout()
        return fig

    def plot_convergence(self):
        cumulative_payoff = np.cumsum(np.maximum(self.S_T - self.K, 0) if self.call else np.maximum(self.K - self.S_T, 0))
        cumulative_average = np.exp(-self.r * self.T) * cumulative_payoff / np.arange(1, self.N + 1)

        fig, ax = plt.subplots()
        ax.plot(cumulative_average)
        ax.set_title('Convergence of Monte Carlo Price Estimate')
        ax.set_xlabel('Number of Simulations')
        ax.set_ylabel('Estimated Option Price')
        ax.grid(True)
        fig.tight_layout()
        return fig

    def plot_paths(self, num_paths=50):
        time_steps = get_num_days_from_T(self.T)
        dt = self.T / time_steps
        paths = np.zeros((num_paths, time_steps + 1))
        paths[:, 0] = self.S

        for t in range(1, time_steps + 1):
            Z = np.random.randn(num_paths)
            paths[:, t] = paths[:, t - 1] * np.exp((self.r - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * Z)

        fig, ax = plt.subplots()

        for i in range(num_paths):
            ax.plot(paths[i], lw=1)
        
        ax.plot(paths.mean(axis=0), color='red', lw=3, label='Average Path')
        ax.legend()

        ax.set_title(f'Simulated Asset Price Paths ({num_paths} shown)')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Asset Price')
        ax.grid(True)
        fig.tight_layout()
        return fig

    def __repr__(self):
        if self.ticker:
            return (f"{self.ticker} ({self.T:<.2f}y) {self.K:<.2f} {'Call' if self.call else 'Put'} (MC): ${self.price:.2f}, SE: {self.SE:.2f}")

        return (f"MonteCarloPricer(S={self.S:<.2f}, K={self.K:<.2f}, T={self.T:<.2f}, r={self.r:<.2f}, sigma={self.sigma:<.2f}, N={self.N}, {'Call' if self.call else 'Put'}) --> "
                f"${self.price:.2f}, SE: {self.SE:.2f}")
