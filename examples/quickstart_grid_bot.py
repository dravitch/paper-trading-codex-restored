#!/usr/bin/env python3
"""
Quickstart Grid Bot v1.1 - Backtest avec données RÉELLES.

Usage:
    python examples/quickstart_grid_bot.py
    python examples/quickstart_grid_bot.py --data data/SOL_2021_2022.csv
    python examples/quickstart_grid_bot.py --config configs/grid_bot_green.yaml
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from paper_trading_codex.strategies.grid_bot import GridBot
from paper_trading_codex.analysis.benchmarks import Benchmarks
from paper_trading_codex.analysis.performance import PerformanceTracker
from paper_trading_codex.core.data_loader import DataLoader, validate_timeframe_consistency, adapt_config_to_timeframe


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_backtest(config: dict, data: pd.DataFrame) -> dict:
    bot = GridBot(config)
    prices = data["close"].values

    if isinstance(data.index, pd.DatetimeIndex):
        timestamps = data.index
    else:
        timestamps = pd.date_range("2021-10-01", periods=len(prices), freq="D")

    equity_sol, equity_usd = [], []

    for i in range(len(prices)):
        ts = timestamps[i].to_pydatetime() if hasattr(timestamps[i], "to_pydatetime") else datetime.now()
        state = bot.step(float(prices[i]), ts)
        equity_sol.append(bot.collateral_sol)
        equity_usd.append(bot.collateral_sol * float(prices[i]))
        if state["liquidated"]:
            for j in range(i + 1, len(prices)):
                equity_sol.append(bot.collateral_sol)
                equity_usd.append(bot.collateral_sol * float(prices[j]))
            break

    idx = data.index[:len(equity_sol)] if len(data.index) >= len(equity_sol) else range(len(equity_sol))

    # Mark-to-market: fermer positions ouvertes restantes (audit honnête)
    if bot.positions:
        mtm_closed = bot.close_open_positions(float(prices[-1]))
        if mtm_closed > 0:
            # Recalculer dernière equity
            equity_sol[-1] = bot.collateral_sol
            equity_usd[-1] = bot.collateral_sol * float(prices[-1])

    return {
        "bot": bot,
        "equity_sol": pd.Series(equity_sol, index=idx),
        "equity_usd": pd.Series(equity_usd, index=idx),
        "prices": data["close"],
    }


def plot_results(results: dict, config: dict, output_dir: str = "results"):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return

    os.makedirs(output_dir, exist_ok=True)
    prices = results["prices"]
    equity_usd = results["equity_usd"]
    equity_sol = results["equity_sol"]

    bench = Benchmarks(config["initial_capital"], float(prices.iloc[0]), leverage=config["leverage"])
    buyhold = bench.buy_and_hold(prices)
    sellhold = bench.sell_and_hold(prices)

    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    axes[0].plot(buyhold.index, buyhold, label="Buy & Hold", alpha=0.7, color="blue")
    axes[0].plot(sellhold.index, sellhold, label=f"Sell & Hold ({config['leverage']}x)", alpha=0.7, color="orange")
    axes[0].plot(equity_usd.index, equity_usd, label="Grid Bot", linewidth=2, color="green")
    axes[0].axhline(y=config["initial_capital"], color="gray", linestyle="--", alpha=0.5)
    axes[0].set_ylabel("Valeur USD")
    axes[0].set_title(f"Grid Bot - SOL Bear Market 2021-2022 - Leverage {config['leverage']}x")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(prices.index, prices, color="red", alpha=0.7)
    axes[1].set_ylabel("Prix SOL ($)")
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "backtest_usd.png"), dpi=150)
    plt.close()

    fig, ax = plt.subplots(figsize=(14, 6))
    initial_sol = config["initial_capital"] / float(prices.iloc[0])
    ax.axhline(y=initial_sol, color="gray", linestyle="--", alpha=0.5, label=f"Initial: {initial_sol:.2f} SOL")
    ax.plot(equity_sol.index, equity_sol, label="SOL Holdings (Grid)", linewidth=2, color="purple")
    ax.set_ylabel("SOL Holdings")
    ax.set_title("Accumulation SOL - Métrique PRIMAIRE (données réelles)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "backtest_sol.png"), dpi=150)
    plt.close()
    print(f"📊 Graphiques sauvegardés dans {output_dir}/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/grid_bot_optimal.yaml")
    parser.add_argument("--data", default="data/SOL_2021_2022.csv")
    parser.add_argument("--start-date", default="2021-11-10", help="Date début backtest (post-ATH)")
    parser.add_argument("--output", default="results")
    args = parser.parse_args()

    # Config
    config_path = Path(args.config)
    config = load_config(str(config_path)) if config_path.exists() else {
        "leverage": 2, "grid_size": 3, "grid_ratio": 0.015,
        "initial_capital": 1000, "max_positions": 3, "max_position_size": 0.30,
        "maintenance_margin": 0.08, "safety_buffer": 2.0, "adaptive_spacing": True,
    }

    # Données
    data_path = Path(args.data)
    if data_path.exists():
        data = DataLoader.load_csv(str(data_path), reset_index=False)

        # Filtrer par date de début (post-ATH = bear market pur)
        if isinstance(data.index, pd.DatetimeIndex) and args.start_date:
            pre_filter = len(data)
            data = data.loc[args.start_date:]
            if len(data) < pre_filter:
                print(f"   Filtré: {pre_filter} → {len(data)} points (from {args.start_date})")

        quality = DataLoader.validate_data_quality(data)
        source = f"RÉELLES ({data_path.name}, qualité {quality['quality_score']:.0%})"
    else:
        print(f"⚠️  {data_path} non trouvé. Fallback synthétique.")
        np.random.seed(42)
        prices = [100.0]
        for i in range(419):
            t = -0.002 if i < 250 else -0.004
            v = 0.025 if i < 250 else 0.035
            prices.append(max(prices[-1] * (1 + max(min(np.random.normal(t, v), 0.06), -0.08)), 5))
        data = pd.DataFrame({"close": prices})
        source = "SYNTHÉTIQUES (fallback)"

    print(f"\n{'='*60}")
    print("=== BACKTEST GRID BOT ===")
    print(f"{'='*60}")

    # Inférer timeframe et valider cohérence
    timeframe = DataLoader.infer_timeframe(data) if isinstance(data.index, pd.DatetimeIndex) else "unknown"
    if timeframe != "unknown":
        warnings = validate_timeframe_consistency(config, timeframe)
        if warnings:
            print(f"\n⚠️  Incohérence config/timeframe ({timeframe}):")
            for w in warnings:
                print(f"   → {w}")
            print("   Auto-adaptation appliquée.")
            config = adapt_config_to_timeframe(config, "1h", timeframe)
        print(f"Timeframe: {timeframe}")

    print(f"Config:  Leverage {config['leverage']}x, Grid {config.get('grid_size',3)}, Ratio {config.get('grid_ratio',0.015)*100:.1f}%")
    print(f"Capital: ${config['initial_capital']}")
    print(f"Données: {source}")
    print(f"Points:  {len(data)} | ${data['close'].iloc[0]:.2f} → ${data['close'].iloc[-1]:.2f} ({(data['close'].iloc[-1]/data['close'].iloc[0]-1)*100:+.1f}%)")

    # Backtest
    results = run_backtest(config, data)
    bot = results["bot"]
    final_price = float(data["close"].iloc[-1])
    summary = bot.get_summary(final_price)

    # Métriques
    periods_by_timeframe = {"1m": 525_600, "5m": 105_120, "15m": 35_040,
                            "1h": 8_760, "4h": 2_190, "1d": 365}
    periods_per_year = periods_by_timeframe.get(timeframe, 365)
    tracker = PerformanceTracker(periods_per_year=periods_per_year)
    perf = tracker.calculate_all(results["equity_usd"], bot.trades) if len(results["equity_usd"]) > 10 else {}

    bench = Benchmarks(config["initial_capital"], float(data["close"].iloc[0]), leverage=config["leverage"])
    bh_final = bench.buy_and_hold(pd.Series([final_price])).iloc[0]
    sh_final = bench.sell_and_hold(pd.Series([final_price])).iloc[0]

    closing = [
        t
        for t in bot.trades
        if t.get("type") in ("CLOSE_TP", "CLOSE_SL", "CLOSE_MTM", "LIQUIDATION")
    ]
    opens = [t for t in bot.trades if t.get("type") == "OPEN_SHORT"]
    wins = sum(1 for t in closing if t.get("pnl_sol", 0) > 0)
    losses = sum(1 for t in closing if t.get("pnl_sol", 0) <= 0)
    win_rate = (wins / len(closing) * 100) if closing else 0

    zones = {2: "🟢 VERTE (Optimal)", 3: "🟢 VERTE", 5: "🟡 JAUNE", 8: "🔴 ROUGE"}

    print(f"\n{'='*60}")
    print("=== RÉSULTATS ===")
    print(f"{'='*60}")
    print("\n📊 Grid Bot:")
    print(f"   SOL: {summary['sol_return_pct']:+.1f}% ({summary['collateral_sol']:.4f} SOL)")
    print(f"   USD: {summary['usd_return_pct']:+.1f}% (${summary['usd_value']:.2f})")
    print(f"   Opens/Closes: {len(opens)}/{len(closing)} (W:{wins} L:{losses}) | Win Rate: {win_rate:.1f}%")
    print(f"   Liquidé: {'OUI ❌' if summary['liquidated'] else 'NON ✅'}")

    print("\n📊 Benchmarks:")
    print(f"   Buy & Hold:  ${bh_final:.2f} ({(bh_final/config['initial_capital']-1)*100:+.1f}%)")
    print(f"   Sell & Hold: ${sh_final:.2f} ({(sh_final/config['initial_capital']-1)*100:+.1f}%)")

    if perf:
        print("\n📊 Métriques:")
        print(f"   Sharpe: {perf.get('sharpe_ratio',0):.2f} | Sortino: {perf.get('sortino_ratio',0):.2f}")
        print(f"   Max DD: {perf.get('max_drawdown_pct',0):.1f}% | Calmar: {perf.get('calmar_ratio',0):.2f}")

    print(f"\n🎯 Zone: {zones.get(int(config['leverage']), '⚪')}")
    difference = summary["usd_value"] - sh_final
    print(f"Écart Grid vs Sell&Hold statique: ${difference:+.2f}")
    print(f"{'='*60}")

    plot_results(results, config, args.output)


if __name__ == "__main__":
    main()
