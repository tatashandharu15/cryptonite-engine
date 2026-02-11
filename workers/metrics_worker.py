from __future__ import annotations

from typing import Any

from pipelines.signal_pipeline import SignalPipelineInput, run_signal_pipeline
from workers import celery


@celery.task(name="workers.metrics.compute_market_metrics")
def compute_market_metrics(symbol: str, prices: list[float]) -> dict[str, Any]:
    payload = SignalPipelineInput(symbol=symbol, prices=prices)
    return run_signal_pipeline(payload)
