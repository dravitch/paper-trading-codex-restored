from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from paper_trading_codex.domain.contracts import AccountEvent, Fill, InstrumentSpec, ReferenceSpec
from paper_trading_codex.domain.spot_ledger import (
    apply_fill,
    apply_initialization,
    create_spot_account,
    equity_quote,
)
from tests.hypotheses.H0004.oracle import derive_spot_round_trip


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0004"
SCENARIO = json.loads((DOSSIER / "SCENARIO.json").read_text(encoding="utf-8"))
EXPECTED = json.loads((DOSSIER / "ORACLE_EXPECTATIONS.json").read_text(encoding="utf-8"))


def _contract(contract_type, value):
    from paper_trading_codex.domain.contracts import canonical_json_bytes

    return contract_type.from_canonical_bytes(canonical_json_bytes(value))


def _projection(state):
    return {
        "account_model": state.account_model,
        "instrument_spec_sha256": state.instrument_spec_sha256,
        "reference_spec_sha256": state.reference_spec_sha256,
        "base_balance": f"{state.base_balance.numerator}/{state.base_balance.denominator}",
        "quote_balance": f"{state.quote_balance.numerator}/{state.quote_balance.denominator}",
        "fees_by_currency": {
            currency: f"{amount.numerator}/{amount.denominator}"
            for currency, amount in state.fees_by_currency
        },
        "last_event_key": list(state.last_event_key) if state.last_event_key else None,
    }


def test_nominal_spot_path_matches_frozen_oracle_exactly():
    instrument = _contract(InstrumentSpec, SCENARIO["instrument_spec"])
    reference = _contract(ReferenceSpec, SCENARIO["reference_spec"])
    state = create_spot_account(instrument, reference)
    for value in SCENARIO["initialization_events"]:
        state = apply_initialization(state, _contract(AccountEvent, value), instrument)
    assert _projection(state) == EXPECTED["states"]["after_initialization"]

    produced = {}
    for name, value in zip(("buy", "sell"), SCENARIO["fills"]):
        state, events = apply_fill(state, _contract(Fill, value), instrument, reference)
        produced[name] = [event.to_canonical_dict() for event in events]
        assert _projection(state) == EXPECTED["states"][f"after_{name}"]
    assert produced == EXPECTED["derived_account_events"]

    independent = derive_spot_round_trip(SCENARIO)
    assert state.base_balance == independent["final_base"]
    assert state.quote_balance == independent["final_quote"]
    assert dict(state.fees_by_currency)["USD"] == independent["fees"]


def test_valuation_is_pure_and_exact():
    instrument = _contract(InstrumentSpec, SCENARIO["instrument_spec"])
    reference = _contract(ReferenceSpec, SCENARIO["reference_spec"])
    state = create_spot_account(instrument, reference)
    for value in SCENARIO["initialization_events"]:
        state = apply_initialization(state, _contract(AccountEvent, value), instrument)
    for name, value in zip(("buy", "sell"), SCENARIO["fills"]):
        state, _ = apply_fill(state, _contract(Fill, value), instrument, reference)
        before = state
        expected = EXPECTED["valuations"][f"after_{name}_at_20"]["equity_quote"]
        assert equity_quote(state, Fraction(20)) == Fraction(expected)
        assert state == before
