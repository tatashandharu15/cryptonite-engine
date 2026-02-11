from __future__ import annotations

from typing import Any

from neo4j import AsyncDriver, AsyncGraphDatabase

from infrastructure.config.settings import get_settings


class Neo4jClient:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._driver: AsyncDriver | None = None

    async def connect(self) -> None:
        if self._driver is None:
            self._driver = AsyncGraphDatabase.driver(self._dsn)
        await self._driver.verify_connectivity()

    async def close(self) -> None:
        if self._driver is not None:
            await self._driver.close()
            self._driver = None

    async def upsert_wallet_edge(self, w1: str, w2: str, value: float) -> None:
        if self._driver is None:
            await self.connect()
        assert self._driver is not None

        query = """
        MERGE (a:Wallet {address: $w1})
        MERGE (b:Wallet {address: $w2})
        MERGE (a)-[r:TRANSFER]->(b)
        SET r.value = coalesce(r.value, 0.0) + $value,
            r.updated_at = datetime()
        """
        async with self._driver.session() as session:
            await session.run(query, w1=w1.lower(), w2=w2.lower(), value=float(value))

    async def get_neighbors(self, address: str, depth: int = 1) -> list[dict[str, Any]]:
        if self._driver is None:
            await self.connect()
        assert self._driver is not None

        safe_depth = max(1, min(depth, 6))
        query = f"""
        MATCH (start:Wallet {{address: $address}})-[rels:TRANSFER*1..{safe_depth}]->(neighbor:Wallet)
        WITH neighbor, reduce(total = 0.0, rel in rels | total + coalesce(rel.value, 0.0)) AS flow
        RETURN neighbor.address AS address, max(flow) AS flow
        ORDER BY flow DESC
        LIMIT 250
        """
        async with self._driver.session() as session:
            cursor = await session.run(query, address=address.lower())
            rows = await cursor.data()
            return [{"address": row["address"], "flow": float(row["flow"])} for row in rows]


_client: Neo4jClient | None = None


async def connect() -> Neo4jClient:
    global _client
    if _client is None:
        _client = Neo4jClient(get_settings().NEO4J_DSN)
    await _client.connect()
    return _client


async def upsert_wallet_edge(w1: str, w2: str, value: float) -> None:
    client = await connect()
    await client.upsert_wallet_edge(w1=w1, w2=w2, value=value)


async def get_neighbors(address: str, depth: int) -> list[dict[str, Any]]:
    client = await connect()
    return await client.get_neighbors(address=address, depth=depth)
