from __future__ import annotations

from typing import Any

from domain.ledger.mapping import (
    to_address_record,
    to_block_record,
    to_token_transfer_record,
    to_transaction_record,
)
from pipelines.wallet_pipeline import WalletPipelineInput, run_wallet_pipeline
from workers import celery


@celery.task(name="workers.ingestion.ingest_wallet_activity")
def ingest_wallet_activity(address: str, transactions: list[dict[str, Any]]) -> dict[str, Any]:
    payload = WalletPipelineInput(address=address, transactions=transactions)
    return run_wallet_pipeline(payload)


@celery.task(name="workers.ingestion.normalize_ledger_payload")
def normalize_ledger_payload(
    block: dict[str, Any],
    transactions: list[dict[str, Any]],
    transfers: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "block": to_block_record(block),
        "transactions": [to_transaction_record(tx) for tx in transactions],
        "addresses": [
            to_address_record({"address": tx.get("from_address"), "tx_count": 1})
            for tx in transactions
            if tx.get("from_address")
        ],
        "token_transfers": [to_token_transfer_record(transfer) for transfer in transfers],
    }
