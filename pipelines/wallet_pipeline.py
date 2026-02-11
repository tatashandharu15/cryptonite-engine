from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.wallet.scoring import classify_wallet, compute_wallet_features, score_wallet_behavior


@dataclass(slots=True)
class WalletPipelineInput:
    address: str
    transactions: list[dict[str, Any]]


def run_wallet_pipeline(payload: WalletPipelineInput) -> dict[str, Any]:
    features = compute_wallet_features(payload.transactions)
    score = score_wallet_behavior(features)
    label = classify_wallet(score)
    return {
        "address": payload.address.lower(),
        "features": features,
        "score": score,
        "label": label,
    }
