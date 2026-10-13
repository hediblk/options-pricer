import math
import numpy as np
import matplotlib.pyplot as plt


class VerticalSpread:
    def __init__(self, long_strike=100, short_strike=105, long_premium=3, short_premium=1,
                 quantity=1, multiplier=100, call=True):
        if not all(math.isfinite(x) for x in (long_strike, short_strike, long_premium, short_premium)):
            raise ValueError("Strikes and premiums must be finite.")
        if long_strike <= 0 or short_strike <= 0 or long_strike == short_strike:
            raise ValueError("Strikes must be positive and different.")
        if long_premium < 0 or short_premium < 0:
            raise ValueError("Premiums must be nonnegative.")
        if any(not math.isfinite(x) or x < 1 or int(x) != x for x in (quantity, multiplier)):
            raise ValueError("Quantity and multiplier must be positive whole numbers.")

        self.long_strike = long_strike
        self.short_strike = short_strike
        self.long_premium = long_premium
        self.short_premium = short_premium
        self.quantity = quantity
        self.multiplier = multiplier
        self.call = call
        self.size = quantity * multiplier
        self.entry_debit = (long_premium - short_premium) * self.size
        self.width = abs(long_strike - short_strike)

        if call:
            self.strategy = "Bull Call" if long_strike < short_strike else "Bear Call"
        else:
            self.strategy = "Bull Put" if long_strike < short_strike else "Bear Put"

        low, high = sorted((long_strike, short_strike))
        low_pnl, high_pnl = self.expiration_pnl(low), self.expiration_pnl(high)
        self.min_pnl = min(low_pnl, high_pnl)
        self.max_pnl = max(low_pnl, high_pnl)
        self.max_profit = max(0, self.max_pnl)
        self.max_loss = max(0, -self.min_pnl)
        self.breakeven = None
        if self.min_pnl <= 0 <= self.max_pnl:
            self.breakeven = low - low_pnl * self.width / (high_pnl - low_pnl)

    def leg_payoffs(self, S):
        if not math.isfinite(S) or S < 0:
            raise ValueError("Expiration price must be finite and nonnegative.")

        direction = 1 if self.call else -1
        long_payoff = max(direction * (S - self.long_strike), 0) * self.size
        short_payoff = -max(direction * (S - self.short_strike), 0) * self.size
        return long_payoff, short_payoff

    def expiration_pnl(self, S):
        return sum(self.leg_payoffs(S)) - self.entry_debit

    def plot_payoff(self, show_legs=False):
        low, high = sorted((self.long_strike, self.short_strike))
        padding = max(self.width, high * 0.05)
        prices = np.unique(np.r_[np.linspace(max(0, low - padding), high + padding, 301), low, high])
        long, short = np.array([self.leg_payoffs(S) for S in prices]).T

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(prices, long + short - self.entry_debit, lw=2, label="Spread P&L")
        if show_legs:
            ax.plot(prices, long - self.long_premium * self.size, '--', label="Long Leg P&L")
            ax.plot(prices, short + self.short_premium * self.size, '--', label="Short Leg P&L")
        ax.axhline(0, color='black', lw=1)
        ax.axvline(self.long_strike, color='gray', ls=':', label=f"Long Strike (${self.long_strike:g})")
        ax.axvline(self.short_strike, color='gray', ls='--', label=f"Short Strike (${self.short_strike:g})")
        if self.breakeven is not None:
            ax.axvline(self.breakeven, color='green', ls=':', label=f"Breakeven (${self.breakeven:g})")
        ax.set_xlabel("Underlying Price at Expiration ($)")
        ax.set_ylabel("Position P&L ($)")
        ax.legend(fontsize='small')
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig
