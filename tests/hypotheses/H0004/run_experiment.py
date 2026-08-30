"""Exécute H0004 et matérialise son résultat déterministe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from paper_trading_codex.domain.contracts import (
    AccountEvent,
    Fill,
    InstrumentSpec,
    ReferenceSpec,
    canonical_json_bytes,
)
from paper_trading_codex.domain.spot_ledger import (
    apply_fill,
    apply_initialization,
    create_spot_account,
    equity_quote,
)
from tests.hypotheses.H0004.oracle import derive_spot_round_trip


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0004"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _contract(contract_type, value):
    return contract_type.from_canonical_bytes(canonical_json_bytes(value))


def _fraction(value) -> str:
    return f"{value.numerator}/{value.denominator}"


def _state(state) -> dict:
    return {
        "account_model": state.account_model,
        "instrument_spec_sha256": state.instrument_spec_sha256,
        "reference_spec_sha256": state.reference_spec_sha256,
        "base_balance": _fraction(state.base_balance),
        "quote_balance": _fraction(state.quote_balance),
        "fees_by_currency": {currency: _fraction(amount) for currency, amount in state.fees_by_currency},
        "last_event_key": list(state.last_event_key) if state.last_event_key else None,
    }


def run() -> dict:
    scenario = json.loads((DOSSIER / "SCENARIO.json").read_text(encoding="utf-8"))
    expected = json.loads((DOSSIER / "ORACLE_EXPECTATIONS.json").read_text(encoding="utf-8"))
    instrument = _contract(InstrumentSpec, scenario["instrument_spec"])
    reference = _contract(ReferenceSpec, scenario["reference_spec"])
    state = create_spot_account(instrument, reference)
    for value in scenario["initialization_events"]:
        state = apply_initialization(state, _contract(AccountEvent, value), instrument)
    states = {"after_initialization": _state(state)}
    produced = {}
    valuations = {}
    for name, value in zip(("buy", "sell"), scenario["fills"]):
        state, events = apply_fill(state, _contract(Fill, value), instrument, reference)
        states[f"after_{name}"] = _state(state)
        produced[name] = [event.to_canonical_dict() for event in events]
        valuations[f"after_{name}_at_20"] = {
            "balances_unchanged": True,
            "equity_quote": _fraction(equity_quote(state, 20)),
        }
    independent = derive_spot_round_trip(scenario)
    exact = (
        states == expected["states"]
        and produced == expected["derived_account_events"]
        and valuations == expected["valuations"]
        and _fraction(independent["final_quote"]) == states["after_sell"]["quote_balance"]
    )
    if not exact:
        raise AssertionError("H0004_FROZEN_ORACLE_DIVERGENCE")
    return {
        "schema_version": 1,
        "hypothesis_id": "H0004",
        "producer_code_commit": _head(),
        "first_run_commit": "a1374912c4eb233f64566fcc2bc8a443167179ee",
        "first_run_record_commit": "ffed088f41be0954bcc4a685660dc77f6341227f",
        "normative_decision_S1_S7": "8aa05bc80416b00a0f66c30f1d3f5238c135ed96",
        "normative_decision_S8": "cef58c5ad5e81e897148e7786fe80a74eb824c85",
        "ready_preregistration_commit": "f3c68116d3c4e19c657689e473d796b8560accc8",
        "states": states,
        "derived_account_events": produced,
        "valuations": valuations,
        "independent_oracle_equal": True,
        "all_frozen_expectations_exact": True,
        "claims_not_proven": [
            "P1_PASS",
            "canonical_short_model",
            "temporal_enforcement",
            "integrated_P1_proof",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
