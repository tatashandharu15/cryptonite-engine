from domain.wallet.scoring import classify_wallet, compute_wallet_features, score_wallet_behavior


def test_wallet_scoring_flow() -> None:
    transactions = [
        {"direction": "in", "value": 2000.0, "counterparty": "0xabc"},
        {"direction": "out", "value": 500.0, "counterparty": "0xdef"},
        {"direction": "in", "value": 1200.0, "counterparty": "0x123"},
    ]
    features = compute_wallet_features(transactions)
    score = score_wallet_behavior(features)
    label = classify_wallet(score)

    assert features["tx_count"] == 3.0
    assert 0.0 <= score <= 1.0
    assert label in {"high-activity", "organic", "low-signal"}
