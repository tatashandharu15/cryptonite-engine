from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from domain.token.analysis import analyze_contract_risk, analyze_distribution


@dataclass(slots=True)
class TokenPipelineInput:
    token_address: str
    transfers: list[dict[str, Any]]
    contract_metadata: dict[str, Any] = field(default_factory=dict)


def run_token_pipeline(payload: TokenPipelineInput) -> dict[str, Any]:
    distribution = analyze_distribution(payload.transfers)
    contract_analysis = analyze_contract_risk(payload.contract_metadata)
    return {
        "token_address": payload.token_address.lower(),
        "distribution": distribution,
        "contract_analysis": contract_analysis,
    }
