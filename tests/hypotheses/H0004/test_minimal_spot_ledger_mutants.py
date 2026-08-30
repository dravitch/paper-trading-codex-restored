from __future__ import annotations

import ast
from dataclasses import fields, replace
from fractions import Fraction
from pathlib import Path

import pytest

from paper_trading_codex.domain.contracts import (
    AccountEvent, ContractValidationError, Fill, InstrumentSpec, ReferenceSpec,
    canonical_json_bytes, deduplicate_contracts, validate_fill_compatibility,
)
from paper_trading_codex.domain.spot_ledger import (
    SpotAccountState, SpotLedgerInvariantError, apply_fill, apply_initialization,
    create_spot_account, equity_quote, validate_transition_conservation,
)
from tests.hypotheses.H0004.test_minimal_spot_ledger_nominal import EXPECTED, SCENARIO, _contract


def _code(expected, operation):
    with pytest.raises((SpotLedgerInvariantError, ContractValidationError)) as caught:
        operation()
    assert caught.value.code == expected


def _context():
    instrument = _contract(InstrumentSpec, SCENARIO["instrument_spec"])
    reference = _contract(ReferenceSpec, SCENARIO["reference_spec"])
    state = create_spot_account(instrument, reference)
    for value in SCENARIO["initialization_events"]:
        state = apply_initialization(state, _contract(AccountEvent, value), instrument)
    fills = tuple(_contract(Fill, value) for value in SCENARIO["fills"])
    return instrument, reference, state, fills


def test_m1_buy_with_insufficient_quote_is_rejected():
    instrument, reference, state, fills = _context()
    _code("SPOT_INSUFFICIENT_QUOTE", lambda: apply_fill(
        replace(state, quote_balance=Fraction(99)), fills[0], instrument, reference))


def test_m2_sell_above_available_base_is_rejected():
    instrument, reference, state, fills = _context()
    _code("SPOT_INSUFFICIENT_BASE", lambda: apply_fill(state, fills[1], instrument, reference))


def test_m3_fee_sign_and_currency_rejections_are_stable():
    instrument, reference, state, fills = _context()
    _code("FEE_NEGATIVE", lambda: replace(fills[0], fee_amount=Fraction(-1)))
    _code("FILL_FEE_CURRENCY_INCOMPATIBLE", lambda: apply_fill(
        state, replace(fills[0], fee_currency="SOL"), instrument, reference))


@pytest.mark.parametrize(("field", "value", "code"), [
    ("quantity", Fraction(1, 2001), "QUANTITY_OFF_GRID"),
    ("price", Fraction(20001, 1000), "PRICE_OFF_GRID"),
])
def test_m4_off_grid_fill_is_rejected(field, value, code):
    instrument, reference, state, fills = _context()
    _code(code, lambda: apply_fill(state, replace(fills[0], **{field: value}), instrument, reference))


def test_m5_instrument_and_reference_incompatibility_is_rejected():
    instrument, reference, state, fills = _context()
    _code("FILL_INSTRUMENT_INCOMPATIBLE", lambda: apply_fill(
        state, replace(fills[0], instrument_id="BTC-USD-SPOT"), instrument, reference))
    invalid_reference = replace(reference, instrument_spec_sha256="b" * 64)
    state_for_invalid_reference = replace(
        state, reference_spec_sha256=invalid_reference.canonical_sha256())
    _code("REFERENCE_INSTRUMENT_HASH_MISMATCH", lambda: apply_fill(
        state_for_invalid_reference, fills[0], instrument, invalid_reference))


def test_m6_m11_omitted_or_doubled_event_breaks_conservation():
    instrument, reference, state, fills = _context()
    new_state, events = apply_fill(state, fills[0], instrument, reference)
    _code("SPOT_BALANCE_MOVEMENT_UNEXPLAINED", lambda: validate_transition_conservation(
        state, new_state, events[:-1]))
    _code("SPOT_BALANCE_MOVEMENT_UNEXPLAINED", lambda: validate_transition_conservation(
        state, new_state, events + (events[0],)))


def test_m7_event_signs_and_roles_match_frozen_oracle():
    instrument, reference, state, fills = _context()
    _, events = apply_fill(state, fills[0], instrument, reference)
    assert [event.to_canonical_dict() for event in events] == EXPECTED["derived_account_events"]["buy"]
    assert sum((e.delta for e in events if e.account == "BASE"), Fraction()) > 0
    assert all(e.delta <= 0 for e in events if e.account == "QUOTE")


def test_m8_valuation_does_not_mutate_state():
    instrument, reference, state, fills = _context()
    state, _ = apply_fill(state, fills[0], instrument, reference)
    before = state
    assert equity_quote(state, Fraction(20)) == Fraction(999, 10)
    assert state == before


def test_m9_collection_dedup_and_divergence_remain_h0003_semantics():
    _, _, _, fills = _context()
    assert deduplicate_contracts((fills[0], fills[0])) == (fills[0],)
    _code("DUPLICATE_DIVERGENT", lambda: deduplicate_contracts(
        (fills[0], replace(fills[0], fee_amount=Fraction(0)))))


def test_m10_short_account_model_is_rejected():
    instrument, reference, state, fills = _context()
    _code("SPOT_ACCOUNT_MODEL_REQUIRED", lambda: apply_fill(
        replace(state, account_model="ISOLATED_LINEAR_SHORT_EDU_V1"), fills[0], instrument, reference))


def test_m12_ids_are_deterministic_and_b6_sorted():
    instrument, reference, state, fills = _context()
    _, first = apply_fill(state, fills[0], instrument, reference)
    _, second = apply_fill(state, fills[0], instrument, reference)
    ids = tuple(event.account_event_id for event in first)
    assert ids == tuple(event.account_event_id for event in second) == tuple(sorted(ids))


def test_m13_all_derived_provenance_is_inherited_from_fill():
    instrument, reference, state, fills = _context()
    _, events = apply_fill(state, fills[0], instrument, reference)
    for event in events:
        assert (event.source_id, event.source_event_id, event.event_time, event.sequence) == (
            fills[0].source_id, fills[0].fill_id, fills[0].event_time, fills[0].sequence)


def test_m14_double_initialization_after_fill_is_rejected():
    instrument, reference, state, fills = _context()
    state, _ = apply_fill(state, fills[0], instrument, reference)
    event = _contract(AccountEvent, SCENARIO["initialization_events"][1])
    _code("SPOT_INITIALIZATION_AFTER_FILL", lambda: apply_initialization(state, event, instrument))


def test_m15_m16_fee_accumulator_is_positive_and_not_double_counted():
    instrument, reference, state, fills = _context()
    old = state
    state, events = apply_fill(state, fills[0], instrument, reference)
    assert dict(state.fees_by_currency) == {"USD": Fraction(1, 10)}
    validate_transition_conservation(old, state, events)
    assert state.quote_balance == 0


def test_m17_last_event_key_is_input_fill_not_derived_event():
    instrument, reference, state, fills = _context()
    state, events = apply_fill(state, fills[0], instrument, reference)
    assert state.last_event_key == ("FILL", *fills[0].local_order_key())
    assert state.last_event_key[-1] != events[-1].account_event_id


def test_m18a_equal_key_rejects_before_economic_validation():
    instrument, reference, state, fills = _context()
    state, _ = apply_fill(state, fills[0], instrument, reference)
    _code("SPOT_FILL_REAPPLICATION", lambda: apply_fill(state, fills[0], instrument, reference))


def test_m18b_old_economically_applicable_fill_is_out_of_order():
    instrument, reference, state, fills = _context()
    state, _ = apply_fill(state, fills[0], instrument, reference)
    state, _ = apply_fill(state, fills[1], instrument, reference)
    value = {**SCENARIO["fills"][0], "event_time": 2500000000, "fee_amount": "1/10",
             "fill_id": "fill-old-applicable", "order_id": "order-old-applicable",
             "price": "20/1", "quantity": "1/1", "sequence": 99}
    old_fill = _contract(Fill, value)
    assert state.quote_balance >= old_fill.quantity * old_fill.price + old_fill.fee_amount
    _code("SPOT_FILL_OUT_OF_ORDER", lambda: apply_fill(state, old_fill, instrument, reference))


def test_m18c_m18d_no_fill_sorting_or_hidden_history_surface():
    source = Path(__file__).resolve().parents[3].joinpath(
        "paper_trading_codex/domain/spot_ledger.py").read_text()
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.Attribute) and node.attr == "sort" for node in ast.walk(tree))
    assert "seen_fill" not in source and "cache" not in source and "registry" not in source
    assert {field.name for field in fields(SpotAccountState)} == {
        "account_model", "instrument_spec_sha256", "reference_spec_sha256", "base_balance",
        "quote_balance", "fees_by_currency", "last_event_key"}


def test_m18e_fill_key_survives_derived_event_generation():
    instrument, reference, state, fills = _context()
    state, _ = apply_fill(state, fills[0], instrument, reference)
    state, _ = apply_fill(state, fills[1], instrument, reference)
    assert state.last_event_key == ("FILL", *fills[1].local_order_key())


def test_m19_structurally_valid_base_fee_is_spot_unsupported():
    instrument, reference, state, fills = _context()
    base_reference = replace(reference, fee_settlement_currency="SOL")
    base_fee_fill = replace(fills[0], fee_currency="SOL")
    validate_fill_compatibility(base_fee_fill, instrument, base_reference)
    state = replace(state, reference_spec_sha256=base_reference.canonical_sha256())
    _code("SPOT_FEE_CURRENCY_UNSUPPORTED", lambda: apply_fill(
        state, base_fee_fill, instrument, base_reference))


def test_contract_inputs_are_canonical_roundtrips():
    for kind, values in ((AccountEvent, SCENARIO["initialization_events"]), (Fill, SCENARIO["fills"])):
        for value in values:
            contract = _contract(kind, value)
            assert kind.from_canonical_bytes(contract.canonical_bytes()) == contract
            assert canonical_json_bytes(contract.to_canonical_dict()) == contract.canonical_bytes()


def test_reviewer_f1a_foreign_coherent_specs_cannot_mutate_state():
    _, _, state, _ = _context()
    btc_instrument = _contract(InstrumentSpec, {
        **SCENARIO["instrument_spec"], "instrument_id": "BTC-USD-SPOT", "base": "BTC",
    })
    btc_reference = _contract(ReferenceSpec, {
        **SCENARIO["reference_spec"],
        "instrument_id": "BTC-USD-SPOT",
        "instrument_spec_sha256": btc_instrument.canonical_sha256(),
    })
    btc_fill = _contract(Fill, {
        **SCENARIO["fills"][0], "instrument_id": "BTC-USD-SPOT", "fill_id": "btc-fill",
        "order_id": "btc-order", "quantity": "1/1", "fee_amount": "0/1",
    })
    before = state
    _code("SPOT_STATE_INSTRUMENT_MISMATCH", lambda: apply_fill(
        state, btc_fill, btc_instrument, btc_reference))
    assert state == before


def test_reviewer_f1b_alternate_reference_cannot_mutate_state():
    instrument, reference, state, fills = _context()
    alternate_reference = replace(reference, numeraire="EUR")
    before = state
    _code("SPOT_STATE_REFERENCE_MISMATCH", lambda: apply_fill(
        state, fills[0], instrument, alternate_reference))
    assert state == before


def test_reviewer_f1_initialization_binds_available_instrument():
    instrument, _, state, _ = _context()
    foreign = replace(instrument, instrument_id="BTC-USD-SPOT", base="BTC")
    event = _contract(AccountEvent, SCENARIO["initialization_events"][0])
    before = state
    _code("SPOT_STATE_INSTRUMENT_MISMATCH", lambda: apply_initialization(state, event, foreign))
    assert state == before


def test_reviewer_f2_spot_multiplier_two_is_unsupported():
    instrument, reference, _, _ = _context()
    multiplier_two = replace(instrument, contract_multiplier=Fraction(2))
    matching_reference = replace(
        reference, instrument_spec_sha256=multiplier_two.canonical_sha256())
    _code("SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED", lambda: create_spot_account(
        multiplier_two, matching_reference))
