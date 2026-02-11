from __future__ import annotations

import asyncio
from typing import Any

from infrastructure.graphdb.neo4j_client import get_neighbors, upsert_wallet_edge
from pipelines.network_pipeline import NetworkEdge, NetworkPipelineInput, run_network_pipeline
from workers import celery


async def _persist_edges(edges: list[NetworkEdge]) -> None:
    for edge in edges:
        await upsert_wallet_edge(edge.source, edge.target, edge.value)


@celery.task(name="workers.graph.build_network")
def build_network(root_address: str, edges: list[dict[str, Any]]) -> dict[str, Any]:
    parsed_edges = [
        NetworkEdge(
            source=str(edge.get("source", "")).lower(),
            target=str(edge.get("target", "")).lower(),
            value=float(edge.get("value", 0.0)),
        )
        for edge in edges
    ]
    asyncio.run(_persist_edges(parsed_edges))
    pipeline_output = run_network_pipeline(
        NetworkPipelineInput(root_address=root_address, edges=parsed_edges)
    )
    pipeline_output["neighbors"] = asyncio.run(get_neighbors(root_address, depth=2))
    return pipeline_output
