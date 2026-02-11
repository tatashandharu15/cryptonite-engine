from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.shared.utils import safe_div
from domain.wallet.scoring import compute_wallet_features


@dataclass(slots=True)
class NetworkEdge:
    source: str
    target: str
    value: float


@dataclass(slots=True)
class NetworkPipelineInput:
    root_address: str
    edges: list[NetworkEdge]


def run_network_pipeline(payload: NetworkPipelineInput) -> dict[str, Any]:
    root = payload.root_address.lower()
    connected_edges = [
        edge
        for edge in payload.edges
        if edge.source.lower() == root or edge.target.lower() == root
    ]
    transactions = [
        {
            "direction": "out" if edge.source.lower() == root else "in",
            "counterparty": edge.target if edge.source.lower() == root else edge.source,
            "value": edge.value,
        }
        for edge in connected_edges
    ]
    wallet_features = compute_wallet_features(transactions)
    strongest_edge = max((edge.value for edge in connected_edges), default=0.0)

    return {
        "root_address": root,
        "edge_count": len(connected_edges),
        "total_flow": wallet_features["total_volume"],
        "average_flow": safe_div(wallet_features["total_volume"], float(len(connected_edges))),
        "strongest_edge": strongest_edge,
        "wallet_features": wallet_features,
    }
