from domain.token.analysis import analyze_contract_risk, analyze_distribution


def test_token_distribution() -> None:
    transfers = [
        {"to": "0x1", "value": 50},
        {"to": "0x2", "value": 40},
        {"to": "0x1", "value": 10},
    ]
    result = analyze_distribution(transfers)
    assert result["holder_count"] == 2.0
    assert result["top_holder_share"] == 0.6


def test_contract_risk() -> None:
    result = analyze_contract_risk(
        {"is_proxy": True, "mintable": True, "blacklist_enabled": False, "owner_renounced": False}
    )
    assert result["risk_score"] > 0.0
    assert result["flags"]["is_proxy"] is True
