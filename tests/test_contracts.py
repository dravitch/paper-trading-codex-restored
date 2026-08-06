from datetime import datetime

import pytest
import yaml

from paper_trading_codex.core.exchange_simulator import ExchangeSimulator
from paper_trading_codex.core.portfolio_manager import PortfolioManager
from paper_trading_codex.strategies.grid_bot import GridBot


def simulator(slippage=0.0, fee=0.001):
    return ExchangeSimulator({"mean": slippage, "std": 0.0}, commission_rate=fee)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"slippage_config": {"mean": -0.1}},
        {"slippage_config": {"std": -0.1}},
        {"slippage_config": {}, "commission_rate": 1.0},
    ],
)
def test_simulator_rejects_impossible_friction(kwargs):
    with pytest.raises(ValueError):
        ExchangeSimulator(**kwargs)


@pytest.mark.parametrize("side", ["buy", "sell"])
def test_zero_slippage_execution_has_closed_form(side):
    execution = simulator().place_market_order(
        "SOL/USDT", side, 100.0, 20.0, datetime(2024, 1, 1)
    )
    assert execution["executed_price"] == 20.0
    assert execution["commission"] == 0.1
    expected_quantity = 99.9 / 20 if side == "buy" else 100 / 20
    assert execution["quantity"] == pytest.approx(expected_quantity)


def test_portfolio_round_trip_matches_known_accounting():
    portfolio = PortfolioManager(1_000.0)
    exchange = simulator()
    portfolio.place_market_order("SOL/USDT", "buy", 100.0, 20.0, exchange)
    portfolio.place_market_order("SOL/USDT", "sell", 100.0, 22.0, exchange)

    assert portfolio.get_trade_count() == 2
    assert portfolio.get_positions() == {}
    assert portfolio.get_total_fees_paid() == pytest.approx(0.20989)
    assert portfolio.balance == pytest.approx(1_009.78011)
    summary = portfolio.get_summary({})
    assert summary["pnl_usd"] == pytest.approx(9.78011)
    assert summary["open_positions"] == 0


def test_portfolio_rejects_unfunded_buy_and_missing_position_sell():
    portfolio = PortfolioManager(100.0)
    exchange = simulator()
    with pytest.raises(ValueError, match="Balance insuffisante"):
        portfolio.place_market_order("SOL/USDT", "buy", 101, 20, exchange)
    with pytest.raises(ValueError, match="Aucune position"):
        portfolio.place_market_order("SOL/USDT", "sell", 10, 20, exchange)


def test_all_shipped_configs_parse_and_construct_a_bot():
    for path in sorted(__import__("pathlib").Path("configs").glob("*.yaml")):
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
        bot = GridBot(config)
        bot.initialize(100.0)
        assert len(bot.grid_levels) == config["grid_size"]
        assert all(level > 100 for level in bot.grid_levels)


@pytest.mark.parametrize(
    "override",
    [
        {"leverage": 0},
        {"initial_capital": 0},
        {"grid_size": 0},
        {"max_positions": 0},
        {"safety_buffer": 0},
    ],
)
def test_grid_bot_rejects_invalid_config(override):
    config = {"leverage": 2, "initial_capital": 1_000, **override}
    with pytest.raises(ValueError):
        GridBot(config)


def test_grid_bot_rejects_non_positive_initial_price():
    bot = GridBot({"leverage": 2, "initial_capital": 1_000})
    with pytest.raises(ValueError, match="initial_price"):
        bot.initialize(0)


def test_take_profit_uses_the_public_close_event_name():
    bot = GridBot(
        {
            "leverage": 2,
            "initial_capital": 1_000,
            "grid_ratio": 0.02,
            "grid_size": 1,
        }
    )
    bot.initialize(100)
    bot.open_position(102, 102, datetime(2024, 1, 1))
    bot.step(99, datetime(2024, 1, 2))

    assert [trade["type"] for trade in bot.trades] == ["OPEN_SHORT", "CLOSE_TP"]
    assert bot.trades[0]["position_id"] == bot.trades[1]["position_id"]


def test_grid_short_pnl_uses_contract_quantity_once():
    """Marge 300, notionnel 600, quantité 6; PnL brut (100-90)×6=60."""
    bot = GridBot(
        {
            "leverage": 2,
            "initial_capital": 1_000,
            "grid_size": 1,
            "max_position_size": 0.30,
            "maker_fee": 0.0005,
            "trading_fee": 0.001,
        }
    )
    bot.initialize(100)
    assert bot.open_position(100, 102, datetime(2024, 1, 1))
    bot.close_open_positions(90, datetime(2024, 1, 2))

    opened, closed = bot.trades
    assert opened["quantity"] == pytest.approx(6.0)
    assert opened["commission"] == pytest.approx(0.30)
    assert closed["pnl_usd"] == pytest.approx(59.46)
    assert closed["commission"] == pytest.approx(0.54)
    assert closed["total_commission"] == pytest.approx(0.84)
