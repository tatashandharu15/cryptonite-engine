from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping

from redis.asyncio import Redis

from events.event_types import EventType
from infrastructure.cache.redis_client import create_redis_client


class EventPublisher:
    def __init__(self, redis_client: Redis | None = None) -> None:
        self._redis = redis_client or create_redis_client()

    async def publish(self, event_type: EventType, payload: Mapping[str, Any]) -> None:
        envelope = {
            "event_type": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": dict(payload),
        }
        message = json.dumps(envelope, default=str)
        await self._redis.publish(event_type.value, message)
        await self._redis.xadd(
            "cryptonite-events",
            {"event": message},
            maxlen=100_000,
            approximate=True,
        )

    async def close(self) -> None:
        await self._redis.aclose()


async def publish_event(event_type: EventType, payload: Mapping[str, Any]) -> None:
    publisher = EventPublisher()
    try:
        await publisher.publish(event_type=event_type, payload=payload)
    finally:
        await publisher.close()
