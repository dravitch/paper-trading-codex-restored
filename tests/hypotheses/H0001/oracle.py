"""Oracle rationnel indépendant de H0001.

Ce module lit uniquement les inputs du scénario. Il n'importe ni code de production, ni
projection historique P0.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, List


def _fraction(value: str) -> Fraction:
    return Fraction(value)


def derive_expected(scenario_path: Path) -> Dict[str, object]:
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    inputs = scenario["inputs"]
    prices = [_fraction(value) for value in inputs["prices_usd_per_sol"]]

    capital = _fraction(inputs["initial_capital_usd"])
    initial_price = _fraction(inputs["initial_price_usd_per_sol"])
    margin_fraction = _fraction(inputs["margin_fraction"])
    leverage = _fraction(inputs["leverage"])
    maker_fee_rate = _fraction(inputs["maker_fee_rate"])
    taker_fee_rate = _fraction(inputs["taker_fee_rate"])

    collateral_initial = capital / initial_price
    equity_entry = collateral_initial * prices[0]
    margin = equity_entry * margin_fraction
    notional = margin * leverage
    quantity = notional / prices[0]
    entry_fee_usd = notional * maker_fee_rate
    entry_fee_sol = entry_fee_usd / prices[0]
    collateral_open = collateral_initial - entry_fee_sol

    gross_pnl = quantity * (prices[0] - prices[-1])
    exit_notional = quantity * prices[-1]
    exit_fee_usd = exit_notional * taker_fee_rate
    net_pnl = gross_pnl - exit_fee_usd
    collateral_delta = net_pnl / prices[-1]
    collateral_final = collateral_open + collateral_delta

    states: List[Dict[str, object]] = [
        {
            "sequence": 1,
            "collateral_sol": collateral_initial,
            "fees_usd": Fraction(0),
            "realized_price_pnl_usd": Fraction(0),
            "active_positions": 0,
            "position_quantity_sol": Fraction(0),
            "position_margin_usd": Fraction(0),
        },
        {
            "sequence": 2,
            "collateral_sol": collateral_open,
            "fees_usd": entry_fee_usd,
            "realized_price_pnl_usd": Fraction(0),
            "active_positions": 1,
            "position_quantity_sol": quantity,
            "position_margin_usd": margin,
        },
    ]
    for sequence in range(3, 3 + len(prices) - 1):
        states.append(
            {
                "sequence": sequence,
                "collateral_sol": collateral_open,
                "fees_usd": entry_fee_usd,
                "realized_price_pnl_usd": Fraction(0),
                "active_positions": 1,
                "position_quantity_sol": quantity,
                "position_margin_usd": margin,
            }
        )
    states.append(
        {
            "sequence": states[-1]["sequence"] + 1,
            "collateral_sol": collateral_final,
            "fees_usd": entry_fee_usd + exit_fee_usd,
            "realized_price_pnl_usd": gross_pnl,
            "active_positions": 0,
            "position_quantity_sol": Fraction(0),
            "position_margin_usd": Fraction(0),
        }
    )

    return {
        "collateral_initial_sol": collateral_initial,
        "margin_usd": margin,
        "notional_usd": notional,
        "quantity_sol": quantity,
        "entry_fee_usd": entry_fee_usd,
        "entry_fee_sol": entry_fee_sol,
        "gross_pnl_usd": gross_pnl,
        "exit_fee_usd": exit_fee_usd,
        "net_pnl_usd": net_pnl,
        "collateral_delta_sol": collateral_delta,
        "final_collateral_sol": collateral_final,
        "states": states,
    }
