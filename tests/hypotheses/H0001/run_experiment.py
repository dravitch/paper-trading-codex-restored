"""Matérialise la chaîne probatoire H0001 dans un JSON déterministe."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from paper_trading_codex.domain.ledger import (
    CloseShort,
    OpenShort,
    PlannedEvent,
    ShortScenarioSpec,
    build_short_scenario_events,
    replay_ledger,
)
from tests.hypotheses.H0001.oracle import derive_expected


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0001"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _decimal(value: Fraction) -> Decimal:
    with localcontext() as context:
        context.prec = 50
        return Decimal(value.numerator) / Decimal(value.denominator)


def _sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def run() -> dict:
    scenario_path = DOSSIER / "SCENARIO.json"
    observed_path = DOSSIER / "P0_OBSERVED_PROJECTION.json"

    # L'oracle est calculé avant toute lecture de la projection historique.
    expected = derive_expected(scenario_path)
    scenario = _load(scenario_path)
    inputs = scenario["inputs"]
    spec = ShortScenarioSpec(
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
            for event in scenario["ordered_events"]
        ),
    )
    events = build_short_scenario_events(spec)
    snapshots = replay_ledger(events)

    oracle_states = expected["states"]
    exact_equal = len(snapshots) == len(oracle_states) and all(
        snapshot.sequence == oracle["sequence"]
        and snapshot.collateral_sol == oracle["collateral_sol"]
        and snapshot.fees_usd == oracle["fees_usd"]
        and snapshot.realized_price_pnl_usd == oracle["realized_price_pnl_usd"]
        and snapshot.active_positions == oracle["active_positions"]
        and snapshot.position_quantity_sol == oracle["position_quantity_sol"]
        and snapshot.position_margin_usd == oracle["position_margin_usd"]
        for snapshot, oracle in zip(snapshots, oracle_states)
    )
    if not exact_equal:
        raise AssertionError("H0001_EXACT_ACCOUNTING_DIVERGENCE")

    # La projection P0 est ouverte seulement après le calcul et la comparaison comptables.
    observed = _load(observed_path)["projection"]
    opening = next(event for event in events if isinstance(event, OpenShort))
    closing = next(event for event in events if isinstance(event, CloseShort))
    final = snapshots[-1]
    tolerance = Decimal("5e-13")
    p0_equal = all(
        (
            opening.quantity_sol == Fraction(observed["open_quantity_sol"]),
            opening.notional_usd == Fraction(observed["open_notional_usd"]),
            opening.fee_usd == Fraction(observed["open_commission_usd"]),
            closing.fee_usd == Fraction(observed["close_commission_usd"]),
            final.fees_usd == Fraction(observed["close_total_commission_usd"]),
            closing.net_pnl_usd == Fraction(observed["close_net_pnl_usd"]),
            abs(_decimal(closing.collateral_delta_sol) - Decimal(observed["close_pnl_sol"]))
            <= tolerance,
            abs(_decimal(final.collateral_sol) - Decimal(observed["final_collateral_sol"]))
            <= tolerance,
        )
    )
    if not p0_equal:
        raise AssertionError("H0001_P0_PROJECTION_DIVERGENCE")

    exact_projection = {
        "entry_fee_usd": _fraction_text(expected["entry_fee_usd"]),
        "exit_fee_usd": _fraction_text(expected["exit_fee_usd"]),
        "final_collateral_sol": _fraction_text(expected["final_collateral_sol"]),
        "gross_pnl_usd": _fraction_text(expected["gross_pnl_usd"]),
        "margin_usd": _fraction_text(expected["margin_usd"]),
        "net_pnl_usd": _fraction_text(expected["net_pnl_usd"]),
        "quantity_sol": _fraction_text(expected["quantity_sol"]),
        "total_fees_usd": _fraction_text(final.fees_usd),
    }
    state_projection = [
        {
            "active_positions": snapshot.active_positions,
            "collateral_sol": _fraction_text(snapshot.collateral_sol),
            "event_kind": snapshot.event_kind,
            "fees_usd": _fraction_text(snapshot.fees_usd),
            "position_margin_usd": _fraction_text(snapshot.position_margin_usd),
            "position_quantity_sol": _fraction_text(snapshot.position_quantity_sol),
            "realized_price_pnl_usd": _fraction_text(snapshot.realized_price_pnl_usd),
            "sequence": snapshot.sequence,
        }
        for snapshot in snapshots
    ]
    return {
        "schema_version": 1,
        "hypothesis_id": "H0001",
        "producer_code_commit": _git_head(),
        "chain": [
            "independent_fraction_oracle",
            "pre_registered_expectations",
            "canonical_ledger",
            "exact_comparison",
            "separate_p0_projection_comparison",
        ],
        "oracle_input": "SCENARIO.json",
        "oracle_forbidden_input": "P0_OBSERVED_PROJECTION.json",
        "exact_projection": exact_projection,
        "state_projection": state_projection,
        "state_projection_sha256": _sha256(state_projection),
        "comparisons": {
            "canonical_ledger_equals_independent_oracle": exact_equal,
            "h0001_projection_matches_p0_observation": p0_equal,
            "p0_projection_abs_tol": "5e-13",
        },
        "claims_not_proven": [
            "P1_PASS",
            "strategy_equivalence",
            "exchange_fidelity",
            "multi_period_replay",
            "financial_performance",
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
