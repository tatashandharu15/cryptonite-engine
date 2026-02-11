from __future__ import annotations

from typing import Any, Mapping

import numpy as np


def wallet_features_to_vector(features: Mapping[str, float]) -> np.ndarray:
    feature_order = [
        "tx_count",
        "inbound_volume",
        "outbound_volume",
        "total_volume",
        "avg_tx_value",
        "in_out_ratio",
        "counterparty_ratio",
    ]
    return np.array([float(features.get(name, 0.0)) for name in feature_order], dtype=np.float32)


def token_features_to_vector(
    distribution: Mapping[str, float],
    contract_analysis: Mapping[str, Any],
) -> np.ndarray:
    flags = contract_analysis.get("flags", {})
    return np.array(
        [
            float(distribution.get("holder_count", 0.0)),
            float(distribution.get("top_holder_share", 0.0)),
            float(distribution.get("top_10_share", 0.0)),
            float(contract_analysis.get("risk_score", 0.0)),
            float(bool(flags.get("is_proxy", False))),
            float(bool(flags.get("mintable", False))),
            float(bool(flags.get("blacklist_enabled", False))),
            float(bool(flags.get("owner_renounced", False))),
        ],
        dtype=np.float32,
    )
