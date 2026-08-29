from __future__ import annotations

import ast
from dataclasses import replace
from datetime import datetime
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import pytest

from paper_trading_codex.domain.contracts import (
    AccountEvent,
    ContractValidationError,
    Fill,
    DurationNs,
    InstantNs,
    InstrumentSpec,
    MarketEvent,
    ReferenceSpec,
    canonical_json_bytes,
    deduplicate_contracts,
    parse_canonical_rational,
    rational_text,
    validate_account_event_compatibility,
    validate_fill_compatibility,
    validate_instrument_reference,
    validate_market_event_compatibility,
)


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0003"
VECTORS_PATH = DOSSIER / "ORACLE_VECTORS.json"
CONTRACTS_PATH = ROOT / "paper_trading_codex" / "domain" / "contracts.py"
VECTORS = json.loads(VECTORS_PATH.read_text(encoding="utf-8"))

CONTRACT_TYPES = {
    "InstrumentSpec": InstrumentSpec,
    "ReferenceSpec": ReferenceSpec,
    "MarketEvent": MarketEvent,
    "Fill": Fill,
    "AccountEvent": AccountEvent,
}


def _object(name: str):
    vector = VECTORS["valid_objects"][name]
    return CONTRACT_TYPES[name].from_canonical_bytes(vector["canonical_json"].encode())


def _assert_code(expected: str, operation) -> None:
    with pytest.raises(ContractValidationError) as caught:
        operation()
    assert caught.value.code == expected


def test_contract_module_has_no_forbidden_domain_dependencies_or_time_source():
    source = CONTRACTS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

    assert not any(
        name.startswith(prefix)
        for name in imports
        for prefix in ("paper_trading_codex.core", "paper_trading_codex.strategies")
    )
    assert not any(name in {"time", "datetime", "os", "pathlib", "socket"} for name in imports)
    assert "SpotAccountModel" not in source
    assert "IsolatedLinearShortAccountModel" not in source


def test_preregistered_rational_vectors_and_noncanonical_rejections():
    for vector in VECTORS["rational_vectors"]:
        semantic = Fraction(vector["semantic_input"])
        assert rational_text(semantic) == vector["canonical"]
        assert parse_canonical_rational(vector["canonical"]) == semantic

    for value in VECTORS["noncanonical_rational_text_rejections"]:
        with pytest.raises(ContractValidationError):
            parse_canonical_rational(value)


@pytest.mark.parametrize("contract_name", tuple(CONTRACT_TYPES))
def test_preregistered_contract_bytes_and_hashes(contract_name):
    vector = VECTORS["valid_objects"][contract_name]
    contract = _object(contract_name)
    payload = contract.canonical_bytes()

    assert payload.decode() == vector["canonical_json"]
    assert hashlib.sha256(payload).hexdigest() == vector["sha256"]
    if "canonical_utf8_hex" in vector:
        assert payload.hex() == vector["canonical_utf8_hex"]


def test_unicode_nfc_and_escape_vector_bytes_are_exact():
    vector = VECTORS["unicode_and_escape_vector"]
    payload = canonical_json_bytes(vector["semantic_value"])
    assert payload.decode() == vector["canonical_json"]
    assert payload.hex() == vector["canonical_utf8_hex"]
    assert hashlib.sha256(payload).hexdigest() == vector["sha256"]


def test_unicode_surrogate_and_nfc_key_collision_are_rejected():
    _assert_code(
        "UNICODE_SURROGATE_INVALID",
        lambda: canonical_json_bytes({"value": "\ud800"}),
    )
    _assert_code(
        "CANONICAL_JSON_DUPLICATE_KEY",
        lambda: canonical_json_bytes({"é": 1, "e\u0301": 2}),
    )


@pytest.mark.parametrize("contract_name", tuple(CONTRACT_TYPES))
def test_serialize_deserialize_serialize_is_bit_exact(contract_name):
    contract_type = CONTRACT_TYPES[contract_name]
    original = _object(contract_name).canonical_bytes()
    restored = contract_type.from_canonical_bytes(original)
    assert restored.canonical_bytes() == original
    assert restored.canonical_sha256() == hashlib.sha256(original).hexdigest()


def test_m1_nonpositive_contract_multiplier_is_rejected():
    instrument = _object("InstrumentSpec")
    _assert_code(
        "CONTRACT_MULTIPLIER_NOT_POSITIVE",
        lambda: replace(instrument, contract_multiplier=Fraction(0)),
    )


@pytest.mark.parametrize(
    ("field", "code"),
    [("tick_size", "TICK_SIZE_NOT_POSITIVE"), ("lot_size", "LOT_SIZE_NOT_POSITIVE")],
)
def test_m2_nonpositive_grid_is_rejected(field, code):
    instrument = _object("InstrumentSpec")
    _assert_code(code, lambda: replace(instrument, **{field: Fraction(0)}))


def test_m3_missing_or_incompatible_currency_is_rejected():
    instrument = _object("InstrumentSpec")
    reference = _object("ReferenceSpec")
    fill = _object("Fill")
    _assert_code("CURRENCY_REQUIRED", lambda: replace(fill, fee_currency=""))
    _assert_code(
        "REFERENCE_FEE_CURRENCY_INCOMPATIBLE",
        lambda: validate_instrument_reference(
            instrument, replace(reference, fee_settlement_currency="BTC")
        ),
    )
    _assert_code(
        "FILL_FEE_CURRENCY_INCOMPATIBLE",
        lambda: validate_fill_compatibility(
            replace(fill, fee_currency="SOL"), instrument, reference
        ),
    )


def test_m4_rational_normalization_has_one_serialization():
    assert rational_text(Fraction(1, 2)) == rational_text(Fraction(2, 4)) == "1/2"
    _assert_code(
        "RATIONAL_TEXT_NON_CANONICAL",
        lambda: parse_canonical_rational("2/4"),
    )


def test_m5_incompatible_reference_is_rejected():
    instrument = _object("InstrumentSpec")
    reference = _object("ReferenceSpec")
    _assert_code(
        "REFERENCE_INSTRUMENT_ID_MISMATCH",
        lambda: validate_instrument_reference(
            instrument, replace(reference, instrument_id="BTC-USD-SPOT")
        ),
    )
    _assert_code(
        "REFERENCE_INSTRUMENT_HASH_MISMATCH",
        lambda: validate_instrument_reference(
            instrument, replace(reference, instrument_spec_sha256="b" * 64)
        ),
    )


def test_m6_event_without_sequence_is_rejected():
    vector = VECTORS["valid_objects"]["MarketEvent"]
    value = dict(vector["semantic_value"])
    value.pop("sequence")
    payload = canonical_json_bytes(value)
    _assert_code(
        "CONTRACT_FIELDS_INVALID",
        lambda: MarketEvent.from_canonical_bytes(payload),
    )


def test_m7_duplicate_identity_with_divergent_content_is_rejected():
    event = _object("MarketEvent")
    assert deduplicate_contracts((event, event)) == (event,)
    _assert_code(
        "DUPLICATE_DIVERGENT",
        lambda: deduplicate_contracts((event, replace(event, price=Fraction(101)))),
    )


def test_m8_negative_or_missing_fill_fee_is_rejected():
    fill = _object("Fill")
    _assert_code("FEE_NEGATIVE", lambda: replace(fill, fee_amount=Fraction(-1, 20)))
    _assert_code("CURRENCY_REQUIRED", lambda: replace(fill, fee_currency=""))


@pytest.mark.parametrize(
    ("kind", "delta"),
    [("FEE", Fraction(1, 20)), ("INITIALIZE", Fraction(-1))],
)
def test_m9_account_event_sign_kind_mismatch_is_rejected(kind, delta):
    event = _object("AccountEvent")
    _assert_code(
        "ACCOUNT_EVENT_SIGN_MISMATCH",
        lambda: replace(event, kind=kind, delta=delta),
    )


def test_account_event_currency_matches_target_account():
    instrument = _object("InstrumentSpec")
    event = _object("AccountEvent")
    validate_account_event_compatibility(event, instrument)
    _assert_code(
        "ACCOUNT_EVENT_CURRENCY_INCOMPATIBLE",
        lambda: validate_account_event_compatibility(
            replace(event, currency="SOL"), instrument
        ),
    )


def test_m10_construction_order_does_not_change_canonical_bytes_or_hash():
    vector = VECTORS["valid_objects"]["InstrumentSpec"]
    items = list(vector["semantic_value"].items())
    first = InstrumentSpec.from_canonical_bytes(canonical_json_bytes(dict(items)))
    second = InstrumentSpec.from_canonical_bytes(canonical_json_bytes(dict(reversed(items))))
    assert first.canonical_bytes() == second.canonical_bytes()
    assert first.canonical_sha256() == second.canonical_sha256()


def test_local_order_and_cross_type_order_boundary():
    market = _object("MarketEvent")
    fill = _object("Fill")
    account = _object("AccountEvent")
    ordering = VECTORS["ordering_vectors"]
    assert list(market.local_order_key()) == ordering["MarketEvent"]
    assert list(fill.local_order_key()) == ordering["Fill"]
    assert list(account.local_order_key()) == ordering["AccountEvent"]
    _assert_code(
        "CROSS_TYPE_ORDER_UNDEFINED",
        lambda: deduplicate_contracts((market, fill)),
    )


def test_reject_off_grid_is_mechanical():
    instrument = _object("InstrumentSpec")
    reference = _object("ReferenceSpec")
    fill = _object("Fill")
    validate_fill_compatibility(fill, instrument, reference)
    _assert_code(
        "QUANTITY_OFF_GRID",
        lambda: validate_fill_compatibility(
            replace(fill, quantity=Fraction(1, 2001)), instrument, reference
        ),
    )
    _assert_code(
        "PRICE_OFF_GRID",
        lambda: validate_fill_compatibility(
            replace(fill, price=Fraction(10001, 1000)), instrument, reference
        ),
    )


@pytest.mark.parametrize("value", ["not-an-int", True, 0.1, datetime(2026, 8, 29)])
def test_reviewer_c4_instant_ns_rejects_non_exact_int(value):
    _assert_code("INSTANT_NS_TYPE_INVALID", lambda: InstantNs(value))


@pytest.mark.parametrize("value", ["not-an-int", True, 0.1, datetime(2026, 8, 29)])
def test_reviewer_c4_duration_ns_rejects_non_exact_int(value):
    _assert_code("DURATION_NS_TYPE_INVALID", lambda: DurationNs(value))


def test_reviewer_f1_rejects_bool_and_binary64_rationals():
    instrument = _object("InstrumentSpec")
    fill = _object("Fill")
    _assert_code(
        "RATIONAL_VALUE_TYPE_INVALID",
        lambda: replace(instrument, contract_multiplier=True),
    )
    _assert_code(
        "RATIONAL_VALUE_TYPE_INVALID",
        lambda: replace(fill, quantity=0.1),
    )
    _assert_code(
        "RATIONAL_VALUE_TYPE_INVALID",
        lambda: replace(fill, price=100.005),
    )
    _assert_code(
        "RATIONAL_VALUE_TYPE_INVALID",
        lambda: replace(fill, fee_amount=False),
    )


def test_reviewer_f2_market_event_rejects_incompatible_instrument_and_off_grid_price():
    instrument = _object("InstrumentSpec")
    event = _object("MarketEvent")
    validate_market_event_compatibility(event, instrument)
    _assert_code(
        "MARKET_EVENT_INSTRUMENT_INCOMPATIBLE",
        lambda: validate_market_event_compatibility(
            replace(event, instrument_id="BTC-USD-SPOT"), instrument
        ),
    )
    _assert_code(
        "PRICE_OFF_GRID",
        lambda: validate_market_event_compatibility(
            replace(event, price=Fraction(20001, 200)), instrument
        ),
    )
