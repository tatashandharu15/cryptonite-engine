from __future__ import annotations

from domain.shared.utils import mean, pct_returns, stddev


def compute_price_momentum(prices: list[float], window: int = 5) -> float:
    if len(prices) < 2:
        return 0.0
    sampled = prices[-(window + 1) :] if len(prices) > window else prices
    returns = pct_returns(sampled)
    return round(mean(returns), 6)


def compute_volatility(prices: list[float], window: int = 10) -> float:
    if len(prices) < 2:
        return 0.0
    sampled = prices[-(window + 1) :] if len(prices) > window else prices
    returns = pct_returns(sampled)
    return round(stddev(returns), 6)


def generate_signal(momentum: float, volatility: float) -> str:
    if momentum > 0.015 and volatility < 0.08:
        return "BUY"
    if momentum < -0.015 and volatility < 0.08:
        return "SELL"
    return "HOLD"


def build_market_signal(prices: list[float]) -> dict[str, float | str]:
    momentum = compute_price_momentum(prices)
    volatility = compute_volatility(prices)
    return {
        "momentum": momentum,
        "volatility": volatility,
        "signal": generate_signal(momentum, volatility),
    }
