from __future__ import annotations

from infrastructure.db.base import Base
from infrastructure.db.session import async_engine
from infrastructure.graphdb.neo4j_client import connect


async def bootstrap_infrastructure() -> None:
    await connect()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
