from __future__ import annotations

from typing import Any

from domain.shared.utils import safe_div


def analyze_distribution(transfers: list[dict[str, Any]]) -> dict[str, float]:
    balances: dict[str, float] = {}
    total_transferred = 0.0

    for transfer in transfers:
        value = float(transfer.get("value", transfer.get("amount", 0.0)) or 0.0)
        receiver = str(transfer.get("to", transfer.get("to_address", ""))).lower()
        if receiver:
            balances[receiver] = balances.get(receiver, 0.0) + value
        total_transferred += value

    holders = len(balances)
    top_holder = max(balances.values(), default=0.0)
    top_10 = sorted(balances.values(), reverse=True)[:10]

    return {
        "holder_count": float(holders),
        "total_transferred": total_transferred,
        "top_holder_share": safe_div(top_holder, total_transferred),
        "top_10_share": safe_div(sum(top_10), total_transferred),
    }


def analyze_contract_risk(contract_metadata: dict[str, Any]) -> dict[str, Any]:
    flags = {
        "is_proxy": bool(contract_metadata.get("is_proxy", False)),
        "mintable": bool(contract_metadata.get("mintable", False)),
        "blacklist_enabled": bool(contract_metadata.get("blacklist_enabled", False)),
        "owner_renounced": bool(contract_metadata.get("owner_renounced", False)),
    }

    risk_score = 0.0
    if flags["is_proxy"]:
        risk_score += 0.30
    if flags["mintable"]:
        risk_score += 0.35
    if flags["blacklist_enabled"]:
        risk_score += 0.25
    if not flags["owner_renounced"]:
        risk_score += 0.10

    return {
        "risk_score": round(min(risk_score, 1.0), 3),
        "flags": flags,
    }
