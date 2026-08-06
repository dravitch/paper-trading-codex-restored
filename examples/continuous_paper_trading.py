#!/usr/bin/env python3
"""
Paper Trading Continu - 24h/48h/7j.

Usage:
    python examples/continuous_paper_trading.py --duration 24
    python examples/continuous_paper_trading.py --duration 168 --config configs/grid_bot_green.yaml

Sans API Bitget, utilise simulation de prix.
"""

import argparse
import logging
import os
import signal
import time
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import yaml

from paper_trading_codex.strategies.grid_bot import GridBot

_running = True


def signal_handler(sig, frame):
    global _running
    print("\n⚠️  Arrêt demandé...")
    _running = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def simulate_price(current: float, dt_seconds: float = 60) -> float:
    """Simule prix avec random walk (fallback sans API)."""
    hourly_vol = 0.02
    per_step_vol = hourly_vol * np.sqrt(dt_seconds / 3600)
    change = np.random.normal(-0.0001, per_step_vol)
    return max(current * (1 + change), 1.0)


def main():
    parser = argparse.ArgumentParser(description="Paper Trading Continu")
    parser.add_argument("--duration", type=int, default=24, help="Durée en heures")
    parser.add_argument("--config", default="configs/grid_bot_optimal.yaml")
    parser.add_argument("--interval", type=int, default=60, help="Intervalle en secondes")
    parser.add_argument("--initial-price", type=float, default=100.0)
    args = parser.parse_args()

    # Setup
    os.makedirs("reports", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f"reports/paper_trading_{args.duration}h.log"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)

    # Config
    config_path = Path(args.config)
    if config_path.exists():
        config = load_config(str(config_path))
    else:
        config = {
            "leverage": 2, "grid_size": 3, "grid_ratio": 0.015,
            "initial_capital": 1000, "max_positions": 3,
            "max_position_size": 0.30,
            "maintenance_margin": 0.08, "safety_buffer": 1.5,
            "adaptive_spacing": True,
        }

    bot = GridBot(config)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=args.duration)
    current_price = args.initial_price

    # Essayer API Bitget
    use_api = False
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("BITGET_API_KEY", "")
        if api_key and api_key != "your_api_key_here":
            from paper_trading_codex.core.data_fetcher import BitgetDataFetcher
            fetcher = BitgetDataFetcher(
                api_key, os.getenv("BITGET_API_SECRET", ""),
                os.getenv("BITGET_PASSPHRASE", ""),
            )
            symbol = fetcher.get_symbol("SOL")
            ticker = fetcher.get_ticker(symbol)
            current_price = float(ticker["last"])
            use_api = True
            logger.info("API Bitget connectée. Prix live: $%.2f", current_price)
    except Exception as e:
        logger.info("API non disponible (%s). Mode simulation.", e)

    logger.info("=" * 60)
    logger.info("PAPER TRADING DÉMARRÉ")
    logger.info("Durée: %dh | Intervalle: %ds | Leverage: %dx",
                args.duration, args.interval, config["leverage"])
    logger.info("Prix initial: $%.2f | Mode: %s",
                current_price, "API Live" if use_api else "Simulation")
    logger.info("=" * 60)

    # Boucle principale
    iteration = 0
    price_history = []

    while _running and datetime.now() < end_time:
        now = datetime.now()

        # Obtenir prix
        if use_api:
            try:
                ticker = fetcher.get_ticker(symbol)
                current_price = float(ticker["last"])
            except Exception:
                current_price = simulate_price(current_price, args.interval)
        else:
            current_price = simulate_price(current_price, args.interval)

        # Step
        state = bot.step(current_price, now)
        price_history.append({"time": now, "price": current_price})

        # Log périodique (toutes les 10 itérations)
        iteration += 1
        if iteration % 10 == 0:
            elapsed = (now - start_time).total_seconds() / 3600
            logger.info(
                "[%.1fh/%.0fh] Prix=$%.2f | SOL=%.4f (%+.1f%%) | Pos=%d | Trades=%d%s",
                elapsed, args.duration, current_price,
                bot.collateral_sol, bot.get_sol_return_pct(),
                len(bot.positions), len(bot.trades),
                " | LIQUIDÉ" if state["liquidated"] else "",
            )

        if state["liquidated"]:
            logger.warning("LIQUIDÉ. Trading arrêté.")
            break

        time.sleep(args.interval)

    # Rapport final
    actual_end = datetime.now()
    duration_actual = (actual_end - start_time).total_seconds() / 3600
    summary = bot.get_summary(current_price)

    report = f"""
{'='*60}
RAPPORT PAPER TRADING - {args.duration}h
{'='*60}

Période:     {start_time.strftime('%Y-%m-%d %H:%M')} → {actual_end.strftime('%Y-%m-%d %H:%M')}
Durée:       {duration_actual:.1f}h / {args.duration}h
Mode:        {"API Live" if use_api else "Simulation"}
Leverage:    {config['leverage']}x

SOL Return:  {summary['sol_return_pct']:+.2f}%
USD Return:  {summary['usd_return_pct']:+.2f}%
SOL Final:   {summary['collateral_sol']:.4f}
USD Final:   ${summary['usd_value']:.2f}

Trades:      {summary['total_trades']}
Positions:   {summary['active_positions']}
Liquidé:     {'OUI' if summary['liquidated'] else 'NON'}

Prix début:  ${price_history[0]['price']:.2f}
Prix fin:    ${current_price:.2f}
Variation:   {(current_price - price_history[0]['price']) / price_history[0]['price'] * 100:+.1f}%
"""

    logger.info(report)

    report_path = f"reports/paper_trading_{args.duration}h.txt"
    with open(report_path, "w") as f:
        f.write(report)
    logger.info("Rapport sauvegardé: %s", report_path)


if __name__ == "__main__":
    main()
