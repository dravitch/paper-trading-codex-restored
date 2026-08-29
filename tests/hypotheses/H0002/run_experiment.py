"""Produit le résultat déterministe final de H0002."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

from paper_trading_codex.domain.ledger import (
    PlannedEvent,
    ShortScenarioSpec,
    build_short_scenario_events,
    replay_ledger,
)
from tests.hypotheses.H0002.oracle import derive_family


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0002"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_object(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return _sha256_bytes(payload)


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _spec(case: dict) -> ShortScenarioSpec:
    inputs = case["inputs"]
    return ShortScenarioSpec(
        initial_capital_usd=Fraction(inputs["initial_capital_usd"]),
        initial_price_usd_per_sol=Fraction(inputs["initial_price_usd_per_sol"]),
        margin_fraction=Fraction(inputs["margin_fraction"]),
        leverage=Fraction(inputs["leverage"]),
        maker_fee_rate=Fraction(inputs["maker_fee_rate"]),
        taker_fee_rate=Fraction(inputs["taker_fee_rate"]),
        prices_usd_per_sol=tuple(Fraction(value) for value in inputs["prices_usd_per_sol"]),
        ordered_events=tuple(
            PlannedEvent(
                sequence=event["sequence"],
                kind=event["kind"],
                price_usd_per_sol=Fraction(event["price_usd_per_sol"]),
            )
            for event in case["ordered_events"]
        ),
    )


def run() -> dict:
    family_path = DOSSIER / "SCENARIO_FAMILY.json"
    family = _load(family_path)

    # L'oracle dérive toute la famille avant la lecture des réponses préenregistrées.
    oracle = derive_family(family_path)
    projections = {}
    all_exact = True
    for case in family["scenarios"]:
        scenario_id = case["scenario_id"]
        snapshots = replay_ledger(build_short_scenario_events(_spec(case)))
        states = oracle[scenario_id]["states"]
        exact = len(snapshots) == len(states) and all(
            actual.sequence == expected["sequence"]
            and actual.collateral_sol == expected["collateral_sol"]
            and actual.fees_usd == expected["fees_usd"]
            and actual.realized_price_pnl_usd == expected["realized_price_pnl_usd"]
            and actual.active_positions == expected["active_positions"]
            and actual.position_quantity_sol == expected["position_quantity_sol"]
            and actual.position_margin_usd == expected["position_margin_usd"]
            for actual, expected in zip(snapshots, states)
        )
        if not exact:
            raise AssertionError(f"H0002_EXACT_DIVERGENCE:{scenario_id}")
        all_exact = all_exact and exact
        projections[scenario_id] = {
            key: _fraction_text(oracle[scenario_id][key])
            for key in (
                "margin_usd",
                "quantity_sol",
                "entry_fee_usd",
                "gross_pnl_usd",
                "exit_fee_usd",
                "net_pnl_usd",
                "final_collateral_sol",
            )
        }

    registered = _load(DOSSIER / "ORACLE_EXPECTATIONS.json")["expectations"]
    registered_equal = all(
        all(_fraction_text(oracle[scenario_id][key]) == value for key, value in expected.items())
        for scenario_id, expected in registered.items()
    )
    if not registered_equal:
        raise AssertionError("H0002_PREREGISTERED_ORACLE_DIVERGENCE")

    ledger_path = ROOT / "paper_trading_codex" / "domain" / "ledger.py"
    return {
        "schema_version": 1,
        "hypothesis_id": "H0002",
        "producer_code_commit": _git_head(),
        "preregistration_commit": "1d63024aee44e56c236d5bc67b3128f03994aa92",
        "first_run_record_commit": "9eec77fb4cdeb58b16f579959c22003fa734fdf8",
        "inherited_ledger_sha256": _sha256_bytes(ledger_path.read_bytes()),
        "ledger_modified_for_h0002": False,
        "oracle_input": "SCENARIO_FAMILY.json",
        "oracle_forbidden_input": "ORACLE_EXPECTATIONS.json",
        "scenario_count": len(projections),
        "scenario_projections": projections,
        "scenario_projection_sha256": _sha256_object(projections),
        "comparisons": {
            "canonical_ledger_equals_independent_oracle_for_all_cases": all_exact,
            "executable_oracle_equals_preregistered_expectations": registered_equal,
        },
        "claims_not_proven": [
            "P1_PASS",
            "long_or_spot_accounting",
            "partial_close_accounting",
            "liquidation_or_funding",
            "multi_position_accounting",
            "exchange_fidelity",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
