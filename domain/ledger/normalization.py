from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


def _to_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    return datetime.now(tz=timezone.utc)


def _to_decimal(value: Any) -> Decimal:
    return Decimal(str(value or "0"))


def normalize_block(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": int(raw.get("number", 0)),
        "hash": str(raw.get("hash", "")).lower(),
        "parent_hash": str(raw.get("parent_hash", "")).lower(),
        "mined_at": _to_datetime(raw.get("timestamp") or raw.get("mined_at")),
    }


def normalize_transaction(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "tx_hash": str(raw.get("tx_hash") or raw.get("hash", "")).lower(),
        "block_number": int(raw.get("block_number", 0)),
        "from_address": str(raw.get("from_address") or raw.get("from", "")).lower(),
        "to_address": str(raw.get("to_address") or raw.get("to", "")).lower(),
        "value": _to_decimal(raw.get("value", 0)),
        "gas_used": int(raw.get("gas_used", 0)),
        "status": str(raw.get("status", "confirmed")),
        "created_at": _to_datetime(raw.get("timestamp") or raw.get("created_at")),
    }


def normalize_address(raw: dict[str, Any]) -> dict[str, Any]:
    first_seen = _to_datetime(raw.get("first_seen_at") or raw.get("created_at"))
    last_seen = _to_datetime(raw.get("last_seen_at") or raw.get("updated_at") or first_seen)
    return {
        "address": str(raw.get("address", "")).lower(),
        "chain_id": int(raw.get("chain_id", 1)),
        "first_seen_at": first_seen,
        "last_seen_at": last_seen,
        "tx_count": int(raw.get("tx_count", 0)),
    }


def normalize_token_transfer(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "tx_hash": str(raw.get("tx_hash") or raw.get("hash", "")).lower(),
        "token_address": str(raw.get("token_address") or raw.get("contract", "")).lower(),
        "from_address": str(raw.get("from_address") or raw.get("from", "")).lower(),
        "to_address": str(raw.get("to_address") or raw.get("to", "")).lower(),
        "amount": _to_decimal(raw.get("amount") or raw.get("value", 0)),
        "raw_log": str(raw.get("raw_log", "")),
        "created_at": _to_datetime(raw.get("timestamp") or raw.get("created_at")),
    }
