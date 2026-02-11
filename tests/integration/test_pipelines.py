from pipelines.network_pipeline import NetworkEdge, NetworkPipelineInput, run_network_pipeline
from pipelines.signal_pipeline import SignalPipelineInput, run_signal_pipeline
from pipelines.token_pipeline import TokenPipelineInput, run_token_pipeline
from pipelines.wallet_pipeline import WalletPipelineInput, run_wallet_pipeline


def test_wallet_pipeline_integration() -> None:
    output = run_wallet_pipeline(
        WalletPipelineInput(
            address="0xABC",
            transactions=[
                {"direction": "in", "value": 200, "counterparty": "0x1"},
                {"direction": "out", "value": 50, "counterparty": "0x2"},
            ],
        )
    )
    assert output["address"] == "0xabc"
    assert "score" in output


def test_token_pipeline_integration() -> None:
    output = run_token_pipeline(
        TokenPipelineInput(
            token_address="0xTOKEN",
            transfers=[{"to_address": "0x1", "amount": 50}, {"to_address": "0x2", "amount": 10}],
            contract_metadata={"is_proxy": False, "mintable": True},
        )
    )
    assert output["token_address"] == "0xtoken"
    assert "distribution" in output
    assert "contract_analysis" in output


def test_signal_pipeline_integration() -> None:
    output = run_signal_pipeline(SignalPipelineInput(symbol="btc", prices=[1.0, 1.2, 1.3, 1.1]))
    assert output["symbol"] == "BTC"
    assert output["signal"] in {"BUY", "SELL", "HOLD"}


def test_network_pipeline_integration() -> None:
    output = run_network_pipeline(
        NetworkPipelineInput(
            root_address="0xA",
            edges=[
                NetworkEdge(source="0xA", target="0xB", value=25.0),
                NetworkEdge(source="0xC", target="0xA", value=30.0),
            ],
        )
    )
    assert output["root_address"] == "0xa"
    assert output["edge_count"] == 2
    assert "wallet_features" in output
