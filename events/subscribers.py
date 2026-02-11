from __future__ import annotations

import json
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from redis.asyncio import Redis

from events.event_types import EventType
from infrastructure.cache.redis_client import create_redis_client

EventHandler = Callable[[dict[str, Any]], Awaitable[None]]


class EventSubscriber:
    def __init__(
        self,
        event_types: Sequence[EventType] | None = None,
        redis_client: Redis | None = None,
    ) -> None:
        self._event_types = list(event_types or list(EventType))
        self._redis = redis_client or create_redis_client()

    async def listen(self, handler: EventHandler, stop_after: int | None = None) -> None:
        pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
        await pubsub.subscribe(*[event.value for event in self._event_types])

        processed = 0
        async for message in pubsub.listen():
            if message.get("type") != "message":
                continue
            data = message.get("data")
            if not isinstance(data, str):
                continue
            await handler(json.loads(data))
            processed += 1
            if stop_after is not None and processed >= stop_after:
                break

        await pubsub.aclose()

    async def close(self) -> None:
        await self._redis.aclose()
