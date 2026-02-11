from __future__ import annotations

from typing import Any

from domain.ledger.normalization import (
    normalize_address,
    normalize_block,
    normalize_token_transfer,
    normalize_transaction,
)


def to_block_record(raw: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_block(raw)
    return {
        "block_number": normalized["number"],
        "block_hash": normalized["hash"],
        "parent_hash": normalized["parent_hash"],
        "mined_at": normalized["mined_at"],
    }


def to_transaction_record(raw: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_transaction(raw)
    return {
        "tx_hash": normalized["tx_hash"],
        "from_address": normalized["from_address"],
        "to_address": normalized["to_address"],
        "value": normalized["value"],
        "gas_used": normalized["gas_used"],
        "status": normalized["status"],
        "created_at": normalized["created_at"],
    }


def to_address_record(raw: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_address(raw)
    return {
        "address": normalized["address"],
        "chain_id": normalized["chain_id"],
        "first_seen_at": normalized["first_seen_at"],
        "last_seen_at": normalized["last_seen_at"],
        "tx_count": normalized["tx_count"],
    }


def to_token_transfer_record(raw: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_token_transfer(raw)
    return {
        "tx_hash": normalized["tx_hash"],
        "token_address": normalized["token_address"],
        "from_address": normalized["from_address"],
        "to_address": normalized["to_address"],
        "amount": normalized["amount"],
        "raw_log": normalized["raw_log"],
        "created_at": normalized["created_at"],
    }
