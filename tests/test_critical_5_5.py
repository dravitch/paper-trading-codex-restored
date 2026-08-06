"""Invariants métier calculés depuis l'API publique et des oracles indépendants."""

from datetime import datetime

import pandas as pd
import pytest

from paper_trading_codex.analysis.benchmarks import Benchmarks
from paper_trading_codex.core.exchange_simulator import ExchangeSimulator
from paper_trading_codex.core.portfolio_manager import PortfolioManager
from paper_trading_codex.strategies.grid_bot import GridBot


DEFAULT_CONFIG = {
    "leverage": 5,
    "grid_size": 1,
    "grid_ratio": 0.02,
    "initial_capital": 1_000,
    "maintenance_margin": 0.08,
    "safety_buffer": 1.3,
    "max_positions": 1,
    "liquidation_loss_fraction": 0.80,
}
T0 = datetime(2024, 1, 1)
T1 = datetime(2024, 1, 2)


def initialized_bot() -> GridBot:
    bot = GridBot(DEFAULT_CONFIG)
    bot.initialize(100.0)
    assert bot.open_position(100.0, 102.0, T0)
    return bot


def test_declared_liquidation_loss_is_applied_through_public_api():
    """Oracle: le collatéral net conserve exactement 20 %."""
    bot = initialized_bot()
    threshold = bot.calculate_liquidation_price(100.0)

    state = bot.step(threshold, T1)

    assert state["liquidated"] is True
    # Marge 300 USD, notionnel 1 500 USD; frais maker 0,75 USD = 0,0075 SOL.
    collateral_before_liquidation = 10.0 - 0.0075
    assert bot.collateral_sol == pytest.approx(collateral_before_liquidation * 0.20)
    assert bot.trades[-1]["loss_pct"] == 80.0


def test_liquidation_is_terminal_for_identical_future_inputs():
    bot = initialized_bot()
    threshold = bot.calculate_liquidation_price(100.0)
    bot.step(threshold, T1)
    collateral_after = bot.collateral_sol
    trade_count_after = len(bot.trades)

    state = bot.step(50.0, datetime(2024, 1, 3))

    assert state["liquidated"] is True
    assert bot.collateral_sol == collateral_after
    assert len(bot.trades) == trade_count_after
    assert bot.positions == []


def test_round_trip_fee_conservation_at_constant_price():
    """Oracle: coût = 100×0,1 % + 99,9×0,1 % = 0,1999 USD."""
    portfolio = PortfolioManager(1_000)
    simulator = ExchangeSimulator({"mean": 0, "std": 0}, seed=7)
    portfolio.place_market_order("SOL", "buy", 100, 20, simulator, T0)
    portfolio.place_market_order("SOL", "sell", 100, 20, simulator, T1)

    assert portfolio.get_total_fees_paid() == pytest.approx(0.1999)
    assert portfolio.balance == pytest.approx(999.8001)
    assert 1_000 - portfolio.balance == pytest.approx(
        portfolio.get_total_fees_paid()
    )


def test_benchmark_formulas_are_exact():
    prices = pd.Series([100.0, 50.0])
    bench = Benchmarks(1_000, 100, leverage=2, trading_fee=0)

    assert bench.buy_and_hold(prices).tolist() == [1_000.0, 500.0]
    assert bench.sell_and_hold(prices).tolist() == [1_000.0, 2_000.0]
