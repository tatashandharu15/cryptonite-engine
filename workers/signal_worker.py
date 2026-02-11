from __future__ import annotations

import asyncio
from typing import Any

from events.event_types import EventType
from events.publishers import publish_event
from pipelines.signal_pipeline import SignalPipelineInput, run_signal_pipeline
from workers import celery


async def _publish_market_event(payload: dict[str, Any]) -> None:
    await publish_event(EventType.PRICE_UPDATED, payload)


@celery.task(name="workers.signal.generate_signal")
def generate_signal(symbol: str, prices: list[float]) -> dict[str, Any]:
    result = run_signal_pipeline(SignalPipelineInput(symbol=symbol, prices=prices))
    asyncio.run(_publish_market_event(result))
    return result
