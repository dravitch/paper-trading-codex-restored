import sys
import types

import pandas as pd
import pytest

from paper_trading_codex.core import data_fetcher as module
from paper_trading_codex.core.data_fetcher import BitgetDataFetcher


class FakeClient:
    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=100):
        assert symbol == "SOL/USDT:USDT"
        assert timeframe == "1h"
        assert since == 123
        assert limit == 2
        return [
            [1_704_067_200_000, "100", "110", "90", "105", "12"],
            [1_704_070_800_000, "105", "112", "101", "108", "15"],
        ]

    def fetch_ticker(self, symbol):
        return {"symbol": symbol, "last": 108.0}


def test_symbol_is_deterministic_by_mode():
    assert BitgetDataFetcher(mode="demo").get_symbol("SOL") == "SSOL/SUSDT:SUSDT"
    assert BitgetDataFetcher(mode="live").get_symbol("SOL") == "SOL/USDT:USDT"


def test_market_data_uses_injected_client_without_network(monkeypatch):
    fetcher = BitgetDataFetcher(mode="live")
    fetcher._client = FakeClient()
    monkeypatch.setattr(fetcher, "_rate_limit", lambda: None)

    frame = fetcher.get_ohlcv("SOL/USDT:USDT", limit=2, since=123)
    ticker = fetcher.get_ticker("SOL/USDT:USDT")

    assert isinstance(frame.index, pd.DatetimeIndex)
    assert frame["close"].tolist() == [105, 108]
    assert ticker == {"symbol": "SOL/USDT:USDT", "last": 108.0}


def test_lazy_client_receives_credentials(monkeypatch):
    captured = {}

    class FakeExchange:
        def __init__(self, config):
            captured.update(config)

    monkeypatch.setitem(sys.modules, "ccxt", types.SimpleNamespace(bitget=FakeExchange))
    fetcher = BitgetDataFetcher("key", "secret", "phrase")

    assert fetcher._get_client() is fetcher._get_client()
    assert captured == {
        "apiKey": "key",
        "secret": "secret",
        "password": "phrase",
        "options": {"defaultType": "swap"},
    }


def test_rate_limit_sleeps_only_for_remaining_interval(monkeypatch):
    fetcher = BitgetDataFetcher()
    fetcher._last_call_time = 10.0
    times = iter([10.1, 10.2])
    sleeps = []
    monkeypatch.setattr(module.time, "time", lambda: next(times))
    monkeypatch.setattr(module.time, "sleep", sleeps.append)

    fetcher._rate_limit()

    assert sleeps == [pytest.approx(0.1)]
    assert fetcher._last_call_time == 10.2


@pytest.mark.parametrize("method", ["get_balance", "create_order", "fetch_positions"])
def test_private_endpoints_are_explicitly_blocked(method):
    with pytest.raises(NotImplementedError, match="PortfolioManager|ExchangeSimulator"):
        getattr(BitgetDataFetcher(), method)()
