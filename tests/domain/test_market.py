from domain.market.signals import (
    build_market_signal,
    compute_price_momentum,
    compute_volatility,
    generate_signal,
)


def test_market_signals() -> None:
    prices = [10.0, 10.5, 11.0, 11.5, 12.0]
    momentum = compute_price_momentum(prices)
    volatility = compute_volatility(prices)
    signal = generate_signal(momentum, volatility)

    assert momentum > 0.0
    assert volatility >= 0.0
    assert signal in {"BUY", "SELL", "HOLD"}


def test_build_market_signal() -> None:
    payload = build_market_signal([10.0, 9.9, 10.1, 10.2])
    assert set(payload) == {"momentum", "volatility", "signal"}
