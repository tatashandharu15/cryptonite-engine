from __future__ import annotations

from typing import Any

from pipelines.network_pipeline import NetworkEdge, NetworkPipelineInput, run_network_pipeline
from workers import celery


@celery.task(name="workers.orchestrator.dispatch_batch")
def dispatch_batch(
    address: str,
    transactions: list[dict[str, Any]],
    token_address: str,
    transfers: list[dict[str, Any]],
    contract_metadata: dict[str, Any],
    symbol: str,
    prices: list[float],
) -> dict[str, Any]:
    edges = [
        NetworkEdge(
            source=str(tx.get("from_address", address)).lower(),
            target=str(tx.get("to_address", "")).lower(),
            value=float(tx.get("value", 0.0)),
        )
        for tx in transactions
    ]
    network_preview = run_network_pipeline(NetworkPipelineInput(root_address=address, edges=edges))

    ingestion_async = celery.send_task(
        "workers.ingestion.ingest_wallet_activity",
        args=[address, transactions],
    )
    contract_async = celery.send_task(
        "workers.contract.analyze_contract",
        args=[token_address, transfers, contract_metadata],
    )
    market_async = celery.send_task("workers.market.evaluate_market", args=[symbol, prices])
    graph_async = celery.send_task(
        "workers.graph.build_network",
        args=[
            address,
            [
                {"source": edge.source, "target": edge.target, "value": edge.value}
                for edge in edges
            ],
        ],
    )

    return {
        "network_preview": network_preview,
        "task_ids": {
            "ingestion": ingestion_async.id,
            "contract": contract_async.id,
            "market": market_async.id,
            "graph": graph_async.id,
        },
    }
