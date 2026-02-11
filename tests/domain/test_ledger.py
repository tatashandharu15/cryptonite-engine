from domain.ledger.mapping import to_block_record, to_token_transfer_record, to_transaction_record
from domain.ledger.normalization import normalize_address, normalize_block, normalize_transaction


def test_normalize_block() -> None:
    normalized = normalize_block(
        {"number": "100", "hash": "0xABC", "parent_hash": "0xDEF", "timestamp": "2025-01-01T00:00:00Z"}
    )
    assert normalized["number"] == 100
    assert normalized["hash"] == "0xabc"


def test_normalize_transaction() -> None:
    normalized = normalize_transaction(
        {
            "hash": "0xTx",
            "from": "0xA",
            "to": "0xB",
            "value": "12345",
            "gas_used": 21000,
        }
    )
    assert normalized["tx_hash"] == "0xtx"
    assert normalized["from_address"] == "0xa"
    assert normalized["to_address"] == "0xb"


def test_mapping_outputs() -> None:
    block_record = to_block_record({"number": 7, "hash": "0x1", "timestamp": "2025-01-01T00:00:00Z"})
    tx_record = to_transaction_record({"hash": "0x2", "from": "0x1", "to": "0x2"})
    transfer_record = to_token_transfer_record({"tx_hash": "0x3", "to_address": "0x9"})
    address = normalize_address({"address": "0xAbC"})

    assert block_record["block_number"] == 7
    assert tx_record["tx_hash"] == "0x2"
    assert transfer_record["tx_hash"] == "0x3"
    assert address["address"] == "0xabc"
