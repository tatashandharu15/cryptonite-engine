from domain.shared.utils import clamp, mean, pct_returns, safe_div, stddev


def test_safe_div_handles_zero_denominator() -> None:
    assert safe_div(10.0, 0.0) == 0.0


def test_mean_and_stddev() -> None:
    values = [1.0, 2.0, 3.0]
    assert mean(values) == 2.0
    assert round(stddev(values), 6) == 1.0


def test_pct_returns_and_clamp() -> None:
    assert pct_returns([100.0, 110.0, 121.0]) == [0.1, 0.1]
    assert clamp(10.0, 0.0, 1.0) == 1.0
