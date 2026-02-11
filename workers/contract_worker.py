from __future__ import annotations

from typing import Any

from pipelines.token_pipeline import TokenPipelineInput, run_token_pipeline
from workers import celery


@celery.task(name="workers.contract.analyze_contract")
def analyze_contract(
    token_address: str,
    transfers: list[dict[str, Any]],
    contract_metadata: dict[str, Any],
) -> dict[str, Any]:
    payload = TokenPipelineInput(
        token_address=token_address,
        transfers=transfers,
        contract_metadata=contract_metadata,
    )
    return run_token_pipeline(payload)
