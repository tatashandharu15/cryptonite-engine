from __future__ import annotations

from math import sqrt
from typing import Iterable


def safe_div(numerator: float, denominator: float, default: float = 0.0) -> float:
    return default if denominator == 0 else numerator / denominator


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def mean(values: Iterable[float]) -> float:
    data = list(values)
    if not data:
        return 0.0
    return sum(data) / len(data)


def stddev(values: Iterable[float]) -> float:
    data = list(values)
    if len(data) < 2:
        return 0.0
    average = mean(data)
    variance = sum((item - average) ** 2 for item in data) / (len(data) - 1)
    return sqrt(variance)


def pct_returns(values: list[float]) -> list[float]:
    if len(values) < 2:
        return []
    returns: list[float] = []
    for previous, current in zip(values, values[1:]):
        returns.append(safe_div(current - previous, previous))
    return returns
