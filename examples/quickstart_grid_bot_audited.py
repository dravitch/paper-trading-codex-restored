#!/usr/bin/env python3
"""
Quickstart Grid Bot v1.2 - AVEC AUDIT INTÉGRÉ V2
Méthodologie: Ground Truth or Silence (métriques exactes)

Usage:
    cd paper-trading-codex-v1.1
    python examples/quickstart_grid_bot_audited.py
    python examples/quickstart_grid_bot_audited.py --data data/SOL_2021_2022.csv
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

# Fix imports - assume script is in examples/
script_dir = Path(__file__).parent.absolute()
project_root = script_dir.parent

try:
    from paper_trading_codex.strategies.grid_bot import GridBot
    from paper_trading_codex.analysis.benchmarks import Benchmarks
    from paper_trading_codex.analysis.performance import PerformanceTracker
    from paper_trading_codex.core.data_loader import DataLoader, validate_timeframe_consistency, adapt_config_to_timeframe
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("   Assurez-vous d'exécuter depuis le répertoire du projet:")
    print("   cd paper-trading-codex-v1.1")
    print("   python examples/quickstart_grid_bot_audited.py")
    sys.exit(1)

# Import audit V2 - cherche dans examples/
try:
    from trade_auditor_v2 import audit_bot_results
    AUDIT_AVAILABLE = True
except ImportError:
    AUDIT_AVAILABLE = False
    print("⚠️  trade_auditor_v2.py non trouvé dans examples/ - audit désactivé")


def load_config(path: str) -> dict:
    """Charge la configuration depuis un fichier YAML"""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run_backtest(config: dict, data: pd.DataFrame) -> dict:
    """
    Exécute un backtest complet avec le Grid Bot
    
    Returns:
        dict avec bot, equity_sol, equity_usd, prices
    """
    bot = GridBot(config)
    prices = data["close"].values

    # Gérer les timestamps
    if isinstance(data.index, pd.DatetimeIndex):
        timestamps = data.index
    else:
        timestamps = pd.date_range("2021-10-01", periods=len(prices), freq="D")

    equity_sol, equity_usd = [], []

    # Exécuter le backtest pas à pas
    for i in range(len(prices)):
        ts = timestamps[i].to_pydatetime() if hasattr(timestamps[i], "to_pydatetime") else datetime.now()
        state = bot.step(float(prices[i]), ts)
        equity_sol.append(bot.collateral_sol)
        equity_usd.append(bot.collateral_sol * float(prices[i]))
        
        # Si liquidé, propager le dernier état
        if state["liquidated"]:
            for j in range(i + 1, len(prices)):
                equity_sol.append(bot.collateral_sol)
                equity_usd.append(bot.collateral_sol * float(prices[j]))
            break

    # Créer les séries temporelles
    idx = data.index[:len(equity_sol)] if len(data.index) >= len(equity_sol) else range(len(equity_sol))
    
    return {
        "bot": bot,
        "equity_sol": pd.Series(equity_sol, index=idx),
        "equity_usd": pd.Series(equity_usd, index=idx),
        "prices": data["close"],
    }


def audit_backtest_results(bot, config: dict, initial_price: float, output_dir: str = "results") -> dict:
    """
    Audit V2 avec métriques exactes
    """
    if not AUDIT_AVAILABLE:
        return {
            'success': False,
            'report': '⚠️  Audit V2 non disponible (scipy requis)'
        }
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Audit avec V2
    result = audit_bot_results(bot, config['initial_capital'], initial_price)
    
    if result['success']:
        # Sauvegarder rapport
        report_path = os.path.join(output_dir, 'audit_report_v2.txt')
        with open(report_path, 'w') as f:
            f.write(result['report'])
        result['report_file'] = report_path
    
    return result


def plot_results(results: dict, config: dict, output_dir: str = "results"):
    """Génère les graphiques de résultats"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠️  matplotlib non disponible - graphiques désactivés")
        return

    os.makedirs(output_dir, exist_ok=True)
    prices = results["prices"]
    equity_usd = results["equity_usd"]
    equity_sol = results["equity_sol"]

    # Calculer les benchmarks
    bench = Benchmarks(config["initial_capital"], float(prices.iloc[0]), leverage=config["leverage"])
    buyhold = bench.buy_and_hold(prices)
    sellhold = bench.sell_and_hold(prices)

    # Graphique 1: Performance USD
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

    # Graphique 2: Accumulation SOL
    fig, ax = plt.subplots(figsize=(14, 6))
    initial_sol = config["initial_capital"] / float(prices.iloc[0])
    ax.axhline(y=initial_sol, color="gray", linestyle="--", alpha=0.5, label=f"Initial: {initial_sol:.2f} SOL")
    ax.plot(equity_sol.index, equity_sol, label="SOL Holdings (Grid)", linewidth=2, color="purple")
    ax.set_ylabel("SOL Holdings")
    ax.set_title("Accumulation SOL - MÉTRIQUE PRIMAIRE (données réelles)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "backtest_sol.png"), dpi=150)
    plt.close()
    
    print(f"📊 Graphiques sauvegardés dans {output_dir}/")


def print_summary(results: dict, config: dict, data: pd.DataFrame, audit_result: dict = None):
    """Affiche résumé + AUDIT V2 en évidence"""
    bot = results["bot"]
    final_price = float(data["close"].iloc[-1])
    summary = bot.get_summary(final_price)

    # Métriques
    configured_timeframe = config.get("timeframe", "1d")
    periods_by_timeframe = {"1m": 525_600, "5m": 105_120, "15m": 35_040,
                            "1h": 8_760, "4h": 2_190, "1d": 365}
    tracker = PerformanceTracker(
        periods_per_year=periods_by_timeframe.get(configured_timeframe, 365)
    )
    perf = tracker.calculate_all(results["equity_usd"], bot.trades) if len(results["equity_usd"]) > 10 else {}

    # Benchmarks
    bench = Benchmarks(config["initial_capital"], float(data["close"].iloc[0]), leverage=config["leverage"])
    bh_final = bench.buy_and_hold(pd.Series([final_price])).iloc[0]
    sh_final = bench.sell_and_hold(pd.Series([final_price])).iloc[0]

    # Trades
    closing = [t for t in bot.trades if t.get("type") == "CLOSE_TP"]
    opens = [t for t in bot.trades if t.get("type") == "OPEN_SHORT"]
    wins = sum(1 for t in closing if t.get("pnl_sol", 0) > 0)
    win_rate = (wins / len(closing) * 100) if closing else 0

    zones = {2: "🟢 VERTE (Optimal)", 3: "🟢 VERTE", 5: "🟡 JAUNE", 8: "🔴 ROUGE"}

    print(f"\n{'='*70}")
    print("=== RÉSULTATS BACKTEST ===")
    print(f"{'='*70}")
    print("\n📊 Grid Bot:")
    print(f"   SOL: {summary['sol_return_pct']:+.1f}% ({summary['collateral_sol']:.4f} SOL)")
    print(f"   USD: {summary['usd_return_pct']:+.1f}% (${summary['usd_value']:.2f})")
    print(f"   Opens/Closes: {len(opens)}/{len(closing)} | Win Rate: {win_rate:.1f}%")
    print(f"   Liquidé: {'OUI ❌' if summary['liquidated'] else 'NON ✅'}")

    print("\n📊 Benchmarks:")
    print(f"   Buy & Hold:  ${bh_final:.2f} ({(bh_final/config['initial_capital']-1)*100:+.1f}%)")
    print(f"   Sell & Hold: ${sh_final:.2f} ({(sh_final/config['initial_capital']-1)*100:+.1f}%)")

    if perf:
        print("\n📊 Métriques:")
        print(f"   Sharpe: {perf.get('sharpe_ratio',0):.2f} | Sortino: {perf.get('sortino_ratio',0):.2f}")
        print(f"   Max DD: {perf.get('max_drawdown_pct',0):.1f}% | Calmar: {perf.get('calmar_ratio',0):.2f}")

    print(f"\n🎯 Zone: {zones.get(int(config['leverage']), '⚪')}")
    
    print(f"\n{'='*70}")
    
    # === AUDIT V2 SECTION SÉPARÉE ===
    if audit_result and audit_result.get('success'):
        print("\n\n")
        print(f"{'#'*70}")
        print("###  🔍 AUDIT V2 - MÉTRIQUES RIGOUREUSES")
        print(f"{'#'*70}")
        print(f"\n{audit_result['report']}")
        
        # Message succinct si anomalies
        if audit_result.get('has_issues'):
            print(f"\n📄 Rapport sauvegardé: {audit_result.get('report_file', 'results/audit_report_v2.txt')}")
        else:
            print("\n✅ AUDIT PASSÉ - Aucune anomalie détectée")
    elif not AUDIT_AVAILABLE:
        print("\n⚠️  Audit V2 non disponible")
        print("   Pour activer: copier trade_auditor_v2.py dans examples/")
        print("   Installer: pip install scipy")
    else:
        if audit_result:
            print(f"\n⚠️  Audit échoué: {audit_result.get('report', 'Erreur inconnue')}")
    
    print(f"\n{'='*70}")


def main():
    parser = argparse.ArgumentParser(
        description="Quickstart Grid Bot avec audit intégré",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--config", default="configs/grid_bot_optimal.yaml", help="Fichier de configuration")
    parser.add_argument("--data", default="data/SOL_2021_2022.csv", help="Fichier de données CSV")
    parser.add_argument("--start-date", default="2021-11-10", help="Date début backtest (post-ATH)")
    parser.add_argument("--output", default="results", help="Répertoire de sortie")
    parser.add_argument("--audit-only", action="store_true", help="Exécuter seulement l'audit (requiert results/trades.json)")
    parser.add_argument("--no-audit", action="store_true", help="Désactiver l'audit")
    parser.add_argument("--no-plots", action="store_true", help="Désactiver la génération de graphiques")
    args = parser.parse_args()

    # Mode audit-only
    if args.audit_only:
        if not AUDIT_AVAILABLE:
            print("❌ Module d'audit non disponible")
            sys.exit(1)
        
        trades_file = os.path.join(args.output, 'trades.json')
        if not os.path.exists(trades_file):
            print(f"❌ Fichier de trades non trouvé: {trades_file}")
            print("   Exécutez d'abord un backtest complet")
            sys.exit(1)
        
        print("Mode audit-only - analyse du fichier de trades existant")
        print(f"Utilisez: python audit_trade_results.py --trades-file {trades_file}")
        sys.exit(0)

    # Configuration
    config_path = Path(args.config)
    if config_path.exists():
        config = load_config(str(config_path))
        print(f"Configuration chargée: {config_path}")
    else:
        # Configuration par défaut (optimizer results)
        config = {
            "leverage": 2, 
            "grid_size": 3, 
            "grid_ratio": 0.015,
            "initial_capital": 1000, 
            "max_positions": 3, 
            "max_position_size": 0.30,
            "maintenance_margin": 0.08, 
            "safety_buffer": 2.0, 
            "adaptive_spacing": True,
        }
        print(f"⚠️  Config {config_path} non trouvée - utilisation config par défaut (optimizer)")

    # Données - UTILISER DataLoader du projet
    data_path = Path(args.data)
    
    # Résoudre chemin relatif depuis project root
    if not data_path.is_absolute():
        data_path = project_root / data_path
    
    if data_path.exists():
        try:
            data = DataLoader.load_csv(str(data_path), reset_index=False)
            
            # Filtrer par date de début (post-ATH = bear market pur)
            if isinstance(data.index, pd.DatetimeIndex) and args.start_date:
                pre_filter = len(data)
                data = data.loc[args.start_date:]
                if len(data) < pre_filter:
                    print(f"   Filtré: {pre_filter} → {len(data)} points (from {args.start_date})")

            quality = DataLoader.validate_data_quality(data)
            source = f"RÉELLES ({data_path.name}, qualité {quality['quality_score']:.0%})"
        except Exception as e:
            print(f"⚠️  Erreur chargement {data_path}: {e}")
            print("   Fallback synthétique")
            data = None
    else:
        print(f"⚠️  {data_path} non trouvé")
        print("   Chemins testés:")
        print(f"     - {data_path}")
        print(f"     - {project_root / 'data' / 'SOL_2021_2022.csv'}")
        print("   Fallback synthétique")
        data = None
    
    # Fallback synthétique si échec
    if data is None:
        np.random.seed(42)
        prices = [100.0]
        for i in range(419):
            t = -0.002 if i < 250 else -0.004
            v = 0.025 if i < 250 else 0.035
            prices.append(max(prices[-1] * (1 + max(min(np.random.normal(t, v), 0.06), -0.08)), 5))
        data = pd.DataFrame({"close": prices})
        source = "SYNTHÉTIQUES (fallback)"

    print(f"\n{'='*70}")
    print("=== BACKTEST GRID BOT ===")
    print(f"{'='*70}")

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

    # Exécuter le backtest
    print("\n🔄 Exécution du backtest...")
    results = run_backtest(config, data)
    print("✅ Backtest terminé")

    # Audit des résultats (si non désactivé)
    audit_result = None
    if not args.no_audit and AUDIT_AVAILABLE:
        print("\n🔍 Audit de cohérence en cours...")
        audit_result = audit_backtest_results(
            bot=results["bot"],
            config=config,
            initial_price=float(data["close"].iloc[0]),
            output_dir=args.output
        )
        
        if audit_result.get('success'):
            print("✅ Audit terminé")
            print(f"   Trades analysés: {audit_result['trades_count']}")
        else:
            print(f"⚠️  Audit échoué: {audit_result.get('error', 'Erreur inconnue')}")

    # Afficher le résumé (inclut audit)
    print_summary(results, config, data, audit_result)

    # Générer les graphiques
    if not args.no_plots:
        print("\n📊 Génération des graphiques...")
        plot_results(results, config, args.output)

    # Code de sortie basé sur l'audit
    if audit_result and audit_result.get('success') and audit_result.get('has_issues'):
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
