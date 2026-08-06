"""
Tests spécifiques Grid Bot et composants.

Tests complémentaires aux 5 critiques.
"""

from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from paper_trading_codex.core.exchange_simulator import ExchangeSimulator
from paper_trading_codex.strategies.grid_bot import GridBot
from paper_trading_codex.analysis.benchmarks import Benchmarks
from paper_trading_codex.analysis.performance import PerformanceTracker


# =========================================================================
# Tests ExchangeSimulator
# =========================================================================


class TestExchangeSimulator:
    def test_slippage_always_unfavorable(self):
        """Slippage TOUJOURS défavorable (dégrade le prix)."""
        sim = ExchangeSimulator({"mean": 0.001, "std": 0.0005})

        # Buy: prix exécuté > prix demandé
        for _ in range(50):
            result = sim.place_market_order("SOL", "buy", 100, 100.0)
            assert result["executed_price"] >= 100.0, (
                "Buy: prix exécuté doit être >= prix demandé"
            )

        # Sell: prix exécuté < prix demandé
        for _ in range(50):
            result = sim.place_market_order("SOL", "sell", 100, 100.0)
            assert result["executed_price"] <= 100.0, (
                "Sell: prix exécuté doit être <= prix demandé"
            )

    def test_commission_always_charged(self):
        """Commission toujours > 0."""
        sim = ExchangeSimulator({"mean": 0, "std": 0})
        result = sim.place_market_order("SOL", "buy", 1000, 100.0)
        assert result["commission"] == pytest.approx(1.0, abs=0.01)  # 0.1% de 1000

    def test_invalid_side_raises(self):
        """Side invalide lève ValueError."""
        sim = ExchangeSimulator({"mean": 0, "std": 0})
        with pytest.raises(ValueError):
            sim.place_market_order("SOL", "long", 100, 100.0)


# =========================================================================
# Tests Benchmarks
# =========================================================================


class TestBenchmarks:
    def test_buy_hold_stable_price(self):
        """Buy&Hold avec prix stable = valeur constante."""
        bench = Benchmarks(1000, 100)
        prices = pd.Series([100, 100, 100, 100, 100])
        bh = bench.buy_and_hold(prices)
        assert all(abs(bh - 1000) < 0.01)

    def test_buy_hold_price_drops_50_percent(self):
        """Buy&Hold perd exactement 50% si prix baisse 50%."""
        bench = Benchmarks(1000, 100)
        prices = pd.Series([100, 90, 80, 70, 60, 50])
        bh = bench.buy_and_hold(prices)
        # 10 SOL × $50 = $500
        assert abs(bh.iloc[-1] - 500) < 0.01

    def test_buy_hold_preserves_units_on_hand_computed_path(self):
        """Oracle externe: 1 000/100 = 10 unités, puis 10×prix."""
        bench = Benchmarks(1000, 100)
        prices = pd.Series([100, 120, 80, 100])
        bh = bench.buy_and_hold(prices)
        assert bh.tolist() == [1000, 1200, 800, 1000]

    def test_sell_hold_profit_on_drop(self):
        """Sell&Hold profite quand prix baisse."""
        bench = Benchmarks(1000, 100, leverage=2.0)
        prices = pd.Series([100, 60])  # -40%
        sh = bench.sell_and_hold(prices)
        # PnL: (100-60)/60 * 2 = 1.333 → value = 1000 * (1 + 1.333 - 0.002) = 2331
        assert sh.iloc[-1] > 1000, "Sell&Hold doit profiter d'une baisse"

    def test_sell_hold_loss_on_rise(self):
        """Sell&Hold perd quand prix monte."""
        bench = Benchmarks(1000, 100, leverage=2.0)
        prices = pd.Series([100, 150])  # +50%
        sh = bench.sell_and_hold(prices)
        assert sh.iloc[-1] < 1000, "Sell&Hold doit perdre sur une hausse"


# =========================================================================
# Tests GridBot
# =========================================================================


class TestGridBot:
    def test_grid_levels_progressive_spacing(self):
        """Espacement géométrique (pas linéaire) — SHORT ascendant."""
        bot = GridBot({"leverage": 5, "grid_size": 7, "grid_ratio": 0.02, "initial_capital": 1000,
                       "adaptive_spacing": True})
        levels = bot.calculate_grid_levels(100.0)

        # Ascending pour SHORT
        assert levels == sorted(levels)

        # Vérifier que les gaps s'élargissent (progressif)
        gaps = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
        for i in range(len(gaps) - 1):
            assert gaps[i + 1] >= gaps[i] * 0.95, (
                "Espacement doit être progressif (croissant)"
            )

    def test_grid_levels_ascending_for_short(self):
        """SHORT: Niveaux triés du plus bas au plus haut (ascendants)."""
        bot = GridBot({"leverage": 5, "grid_size": 5, "grid_ratio": 0.02, "initial_capital": 1000})
        levels = bot.calculate_grid_levels(100.0)
        assert levels == sorted(levels)  # Ascending pour SHORT
        assert all(level > 100.0 for level in levels)  # Au-dessus du prix

    def test_liquidation_price_formula(self):
        """Modèle isolé simplifié: E × (1 + 1/L) / (1 + MMR)."""
        bot = GridBot({
            "leverage": 3,
            "grid_size": 7,
            "grid_ratio": 0.02,
            "initial_capital": 1000,
            "maintenance_margin": 0.05,
            "safety_buffer": 1.5,
        })
        liq = bot.calculate_liquidation_price(100)
        expected = 100 * (1 + 1 / 3) / (1 + 0.05)
        assert abs(liq - expected) < 0.01

    def test_no_open_when_max_positions(self):
        """Ne pas ouvrir si max positions atteint."""
        bot = GridBot({"leverage": 5, "grid_size": 7, "grid_ratio": 0.02, "initial_capital": 1000, "max_positions": 2})
        should_open, _ = bot.should_open_position(50.0, active_positions=2)
        assert should_open is False

    def test_initialize_converts_usd_to_sol(self):
        """Initialize convertit correctement USD → SOL."""
        bot = GridBot({"leverage": 5, "grid_size": 7, "grid_ratio": 0.02, "initial_capital": 1000})
        bot.initialize(100.0)
        assert abs(bot.collateral_sol - 10.0) < 0.01  # 1000 / 100

    def test_full_bear_market_backtest(self):
        """Backtest sur données bear market synthétiques."""
        bot = GridBot({
            "leverage": 5,
            "grid_size": 7,
            "grid_ratio": 0.02,
            "initial_capital": 1000,
            "max_positions": 5,
        })

        # Simuler chute claire 100 → 50 avec oscillations
        np.random.seed(42)
        n_steps = 500
        prices = [100.0]
        for _ in range(n_steps - 1):
            change = np.random.normal(-0.005, 0.015)
            prices.append(max(prices[-1] * (1 + change), 10))

        for i, price in enumerate(prices):
            ts = datetime(2024, 1, 1, i // 24, i % 24)
            state = bot.step(price, ts)
            if state["liquidated"]:
                break

        # Le bot doit avoir fait des trades ou être liquidé
        assert len(bot.trades) > 0 or bot.liquidated, (
            "Bot doit avoir fait au moins 1 trade ou être liquidé"
        )


# =========================================================================
# Tests PerformanceTracker
# =========================================================================


class TestPerformanceTracker:
    def test_sharpe_positive_uptrend(self):
        """Sharpe positif pour equity montante."""
        tracker = PerformanceTracker()
        equity = pd.Series(np.linspace(1000, 2000, 100))
        assert tracker.sharpe_ratio(equity) > 0

    def test_max_drawdown_known(self):
        """Max drawdown sur séquence connue."""
        tracker = PerformanceTracker()
        equity = pd.Series([100, 120, 90, 110, 80, 100])
        # Pic=120, creux=80 → DD = (120-80)/120 = 33.3%
        mdd = tracker.max_drawdown(equity)
        assert abs(mdd - 0.333) < 0.01
