import math


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
