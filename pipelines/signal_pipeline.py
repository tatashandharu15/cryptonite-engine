from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.market.signals import build_market_signal


@dataclass(slots=True)
class SignalPipelineInput:
    symbol: str
    prices: list[float]


def run_signal_pipeline(payload: SignalPipelineInput) -> dict[str, Any]:
    signal = build_market_signal(payload.prices)
    return {
        "symbol": payload.symbol.upper(),
        **signal,
    }
