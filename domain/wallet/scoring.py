from __future__ import annotations

from typing import Any

from domain.shared.utils import clamp, safe_div


def compute_wallet_features(transactions: list[dict[str, Any]]) -> dict[str, float]:
    inbound = 0.0
    outbound = 0.0
    counterparties: set[str] = set()

    for tx in transactions:
        value = float(tx.get("value", 0.0) or 0.0)
        direction = str(tx.get("direction", "out")).lower()
        counterparty = str(tx.get("counterparty", "")).lower()
        if counterparty:
            counterparties.add(counterparty)
        if direction == "in":
            inbound += value
        else:
            outbound += value

    tx_count = float(len(transactions))
    total_volume = inbound + outbound
    avg_tx_value = safe_div(total_volume, tx_count)
    in_out_ratio = safe_div(inbound, outbound, default=inbound)
    counterparty_ratio = safe_div(float(len(counterparties)), tx_count)

    return {
        "tx_count": tx_count,
        "inbound_volume": inbound,
        "outbound_volume": outbound,
        "total_volume": total_volume,
        "avg_tx_value": avg_tx_value,
        "in_out_ratio": in_out_ratio,
        "counterparty_ratio": counterparty_ratio,
    }


def score_wallet_behavior(features: dict[str, float]) -> float:
    score = 0.0
    score += 0.35 * (clamp(features.get("in_out_ratio", 0.0), 0.0, 2.0) / 2.0)
    score += 0.25 * clamp(features.get("counterparty_ratio", 0.0), 0.0, 1.0)
    score += 0.20 * clamp(safe_div(features.get("avg_tx_value", 0.0), 10_000.0), 0.0, 1.0)
    score += 0.20 * clamp(safe_div(features.get("tx_count", 0.0), 100.0), 0.0, 1.0)
    return round(clamp(score, 0.0, 1.0), 4)


def classify_wallet(score: float) -> str:
    if score >= 0.75:
        return "high-activity"
    if score >= 0.45:
        return "organic"
    return "low-signal"
