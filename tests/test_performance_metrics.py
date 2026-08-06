import math

import pandas as pd
import pytest

from paper_trading_codex.analysis.performance import PerformanceTracker


def test_periods_per_year_must_be_positive():
    with pytest.raises(ValueError, match="periods_per_year"):
        PerformanceTracker(periods_per_year=0)


def test_equity_curve_contract_rejects_invalid_input():
    tracker = PerformanceTracker()
    with pytest.raises(TypeError, match="pandas Series"):
        tracker.calculate_returns([100, 101])
    with pytest.raises(ValueError, match="must be positive"):
        tracker.calculate_returns(pd.Series([100.0, 0.0]))


def test_returns_and_drawdown_have_known_values():
    tracker = PerformanceTracker(risk_free_rate=0, periods_per_year=4)
    equity = pd.Series([100.0, 110.0, 88.0, 105.6])

    assert tracker.calculate_returns(equity).tolist() == pytest.approx([0.1, -0.2, 0.2])
    assert tracker.max_drawdown(equity) == pytest.approx(0.2)


def test_sharpe_matches_explicit_formula():
    tracker = PerformanceTracker(risk_free_rate=0, periods_per_year=4)
    equity = pd.Series([100.0, 110.0, 104.5, 125.4])
    returns = pd.Series([0.1, -0.05, 0.2])
    expected = returns.mean() / returns.std() * math.sqrt(4)
    assert tracker.sharpe_ratio(equity) == pytest.approx(expected)


def test_sortino_and_calmar_edge_cases_are_explicit():
    tracker = PerformanceTracker(risk_free_rate=0, periods_per_year=3)
    rising = pd.Series([100.0, 110.0, 121.0])
    flat = pd.Series([100.0, 100.0, 100.0])

    assert math.isinf(tracker.sortino_ratio(rising))
    assert tracker.sortino_ratio(flat) == 0.0
    assert math.isinf(tracker.calmar_ratio(rising))
    assert tracker.calmar_ratio(flat) == 0.0


def test_sortino_one_loss_uses_documented_downside_deviation():
    """Oracle: sqrt((0² + (-0,2)² + 0²)/3), jamais un std à un élément."""
    tracker = PerformanceTracker(risk_free_rate=0, periods_per_year=4)
    equity = pd.Series([100.0, 110.0, 88.0, 105.6])
    mean_return = (0.1 - 0.2 + 0.2) / 3
    downside_deviation = math.sqrt(0.2**2 / 3)
    expected = mean_return / downside_deviation * math.sqrt(4)

    assert tracker.sortino_ratio(equity) == pytest.approx(expected)
    assert math.isfinite(tracker.sortino_ratio(equity))


def test_calmar_uses_compounded_annual_return():
    """Oracle: CAGR=(105,6/100)^(4/3)-1; MDD=20 %."""
    tracker = PerformanceTracker(risk_free_rate=0, periods_per_year=4)
    equity = pd.Series([100.0, 110.0, 88.0, 105.6])
    expected = ((105.6 / 100) ** (4 / 3) - 1) / 0.2

    assert tracker.calmar_ratio(equity) == pytest.approx(expected)


def test_trade_metrics_are_deterministic():
    tracker = PerformanceTracker()
    trades = [{"pnl_usd": 10}, {"pnl_usd": -4}, {"pnl_sol": 2}, {}]

    assert tracker.win_rate(trades) == 50.0
    assert tracker.profit_factor(trades) == pytest.approx(3.0)
    assert tracker.win_rate([]) == 0.0
    assert tracker.profit_factor([]) == 0.0
    assert math.isinf(tracker.profit_factor([{"pnl_usd": 1}]))


def test_calculate_all_filters_closing_trades():
    tracker = PerformanceTracker(risk_free_rate=0, periods_per_year=2)
    metrics = tracker.calculate_all(
        pd.Series([100.0, 90.0, 108.0]),
        [
            {"type": "OPEN_SHORT"},
            {"type": "CLOSE_TP", "pnl_usd": 10},
            {"type": "CLOSE_SL", "pnl_usd": -5},
            {"type": "CLOSE_MTM", "pnl_usd": 0},
            {"type": "LIQUIDATION", "pnl_usd": -20},
        ],
    )

    assert metrics["total_return_pct"] == pytest.approx(8.0)
    assert metrics["max_drawdown_pct"] == pytest.approx(10.0)
    assert metrics["win_rate_pct"] == 25.0
    assert metrics["profit_factor"] == pytest.approx(0.4)
    assert metrics["total_trades"] == 5
    assert metrics["closing_trades"] == 4
