"""Produit un manifeste canonique pour une expérience synthétique déterministe."""

from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timedelta
from importlib.metadata import version
from pathlib import Path

from paper_trading_codex.strategies.grid_bot import GridBot


ROOT = Path(__file__).resolve().parents[1]
SEED = 42
CONFIG = {
    "adaptive_spacing": False,
    "grid_ratio": 0.02,
    "grid_size": 1,
    "initial_capital": 1_000,
    "leverage": 2,
    "liquidation_loss_fraction": 0.80,
    "maintenance_margin": 0.08,
    "max_position_size": 0.30,
    "max_positions": 1,
    "safety_buffer": 1.0,
}
PRICES = [100.0, 102.0, 99.0, 105.0]


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def run() -> dict:
    bot = GridBot(CONFIG)
    start = datetime(2024, 1, 1)
    states = []
    for offset, price in enumerate(PRICES):
        state = bot.step(price, start + timedelta(days=offset))
        states.append(
            {
                "active_positions": state.get("active_positions", 0),
                "collateral_sol": round(bot.collateral_sol, 12),
                "liquidated": state["liquidated"],
                "price": price,
            }
        )
    bot.close_open_positions(PRICES[-1], start + timedelta(days=len(PRICES)))
    result = {
        "final_collateral_sol": round(bot.collateral_sol, 12),
        "states": states,
        "trade_count": len(bot.trades),
        "trades": [
            {
                key: round(value, 12) if isinstance(value, float) else value
                for key, value in trade.items()
                if key not in {"timestamp"}
            }
            for trade in bot.trades
        ],
    }
    return result


def main() -> None:
    result = run()
    manifest = {
        "schema_version": 1,
        "experiment": "deterministic_public_grid_scenario",
        "seed": SEED,
        "config": CONFIG,
        "config_sha256": sha256(CONFIG),
        "input": {"prices": PRICES},
        "input_sha256": sha256(PRICES),
        "result": result,
        "result_sha256": sha256(result),
        "runtime": {
            "python": platform.python_version(),
            "numpy": version("numpy"),
            "pandas": version("pandas"),
            "pyyaml": version("PyYAML"),
        },
    }
    target = ROOT / "REPRODUCIBILITY_MANIFEST.json"
    target.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest["result_sha256"])


if __name__ == "__main__":
    main()
