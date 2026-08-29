"""Contrats canoniques minimaux préenregistrés par H0003."""

from __future__ import annotations

from dataclasses import dataclass, fields
from fractions import Fraction
import hashlib
import json
import unicodedata
from typing import Any, Dict, Iterable, Protocol, Tuple, Type, TypeVar


class InstantNs(int):
    """Instant nanoseconde signé dont la frontière est validée à l'exécution."""

    def __new__(cls, value: int) -> "InstantNs":
        _require(type(value) is int, "INSTANT_NS_TYPE_INVALID")
        return int.__new__(cls, value)


class DurationNs(int):
    """Durée nanoseconde signée dont la frontière est validée à l'exécution."""

    def __new__(cls, value: int) -> "DurationNs":
        _require(type(value) is int, "DURATION_NS_TYPE_INVALID")
        return int.__new__(cls, value)


class Clock(Protocol):
    """Port temporel pur; aucune source temporelle n'est construite ici."""

    def now_ns(self) -> InstantNs: ...


class ContractValidationError(ValueError):
    """Rejet d'un contrat avec code stable."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ContractValidationError(code)


def _nfc(value: str, code: str = "STRING_REQUIRED") -> str:
    _require(isinstance(value, str) and bool(value), code)
    _require(
        not any(0xD800 <= ord(character) <= 0xDFFF for character in value),
        "UNICODE_SURROGATE_INVALID",
    )
    return unicodedata.normalize("NFC", value)


def _integer(value: int, code: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool), code)
    return value


def _hash_text(value: str, code: str) -> str:
    value = _nfc(value, code)
    _require(len(value) == 64 and all(char in "0123456789abcdef" for char in value), code)
    return value


def _exact_fraction(value: Any) -> Fraction:
    _require(type(value) in {int, Fraction}, "RATIONAL_VALUE_TYPE_INVALID")
    return value if isinstance(value, Fraction) else Fraction(value)


def rational_text(value: Fraction) -> str:
    value = _exact_fraction(value)
    return f"{value.numerator}/{value.denominator}"


def parse_canonical_rational(value: str) -> Fraction:
    _require(isinstance(value, str), "RATIONAL_TEXT_INVALID")
    parts = value.split("/")
    _require(len(parts) == 2 and all(parts), "RATIONAL_TEXT_INVALID")
    numerator_text, denominator_text = parts
    _require(not numerator_text.startswith("+") and not denominator_text.startswith("+"), "RATIONAL_TEXT_INVALID")
    _require(not denominator_text.startswith("-"), "RATIONAL_DENOMINATOR_INVALID")
    try:
        numerator = int(numerator_text)
        denominator = int(denominator_text)
    except ValueError as error:
        raise ContractValidationError("RATIONAL_TEXT_INVALID") from error
    _require(str(numerator) == numerator_text, "RATIONAL_TEXT_NON_CANONICAL")
    _require(str(denominator) == denominator_text, "RATIONAL_TEXT_NON_CANONICAL")
    _require(denominator > 0, "RATIONAL_DENOMINATOR_INVALID")
    parsed = Fraction(numerator, denominator)
    _require(rational_text(parsed) == value, "RATIONAL_TEXT_NON_CANONICAL")
    return parsed


def _normalize_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return rational_text(value)
    if isinstance(value, str):
        return _nfc(value)
    if isinstance(value, bool) or value is None or isinstance(value, int):
        return value
    if isinstance(value, (tuple, list)):
        return [_normalize_json(item) for item in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            normalized_key = _nfc(key)
            _require(normalized_key not in result, "CANONICAL_JSON_DUPLICATE_KEY")
            result[normalized_key] = _normalize_json(item)
        return result
    raise ContractValidationError("CANONICAL_JSON_TYPE_UNSUPPORTED")


def canonical_json_bytes(value: Any) -> bytes:
    normalized = _normalize_json(value)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _pairs_without_duplicates(pairs: Iterable[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, "CANONICAL_JSON_DUPLICATE_KEY")
        result[key] = value
    return result


def _canonical_payload(payload: bytes) -> Dict[str, Any]:
    _require(isinstance(payload, bytes), "CANONICAL_BYTES_REQUIRED")
    try:
        decoded = payload.decode("utf-8")
        value = json.loads(decoded, object_pairs_hook=_pairs_without_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractValidationError("CANONICAL_JSON_INVALID") from error
    _require(isinstance(value, dict), "CANONICAL_JSON_OBJECT_REQUIRED")
    _require(canonical_json_bytes(value) == payload, "CANONICAL_BYTES_MISMATCH")
    return value


T = TypeVar("T", bound="CanonicalContract")


class CanonicalContract:
    def to_canonical_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for field in fields(self):
            value = getattr(self, field.name)
            result[field.name] = rational_text(value) if isinstance(value, Fraction) else value
        return result

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_canonical_dict())

    def canonical_sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    @classmethod
    def from_canonical_bytes(cls: Type[T], payload: bytes) -> T:
        return cls._from_dict(_canonical_payload(payload))

    @classmethod
    def _from_dict(cls: Type[T], value: Dict[str, Any]) -> T:
        raise NotImplementedError


def _exact_keys(value: Dict[str, Any], expected: Tuple[str, ...]) -> None:
    _require(set(value) == set(expected), "CONTRACT_FIELDS_INVALID")


@dataclass(frozen=True)
class InstrumentSpec(CanonicalContract):
    instrument_id: str
    instrument_type: str
    base: str
    quote: str
    settlement: str
    contract_multiplier: Fraction
    tick_size: Fraction
    lot_size: Fraction
    rounding_policy: str

    def __post_init__(self) -> None:
        for name in ("instrument_id", "base", "quote", "settlement"):
            object.__setattr__(self, name, _nfc(getattr(self, name), "INSTRUMENT_FIELD_REQUIRED"))
        _require(self.instrument_type in {"SPOT", "LINEAR_PERPETUAL"}, "INSTRUMENT_TYPE_INVALID")
        _require(self.rounding_policy == "REJECT_OFF_GRID", "ROUNDING_POLICY_INVALID")
        for name, code in (
            ("contract_multiplier", "CONTRACT_MULTIPLIER_NOT_POSITIVE"),
            ("tick_size", "TICK_SIZE_NOT_POSITIVE"),
            ("lot_size", "LOT_SIZE_NOT_POSITIVE"),
        ):
            value = _exact_fraction(getattr(self, name))
            object.__setattr__(self, name, value)
            _require(value > 0, code)

    @classmethod
    def _from_dict(cls, value: Dict[str, Any]) -> "InstrumentSpec":
        names = tuple(field.name for field in fields(cls))
        _exact_keys(value, names)
        return cls(
            **{
                **value,
                "contract_multiplier": parse_canonical_rational(value["contract_multiplier"]),
                "tick_size": parse_canonical_rational(value["tick_size"]),
                "lot_size": parse_canonical_rational(value["lot_size"]),
            }
        )


@dataclass(frozen=True)
class ReferenceSpec(CanonicalContract):
    instrument_id: str
    instrument_spec_sha256: str
    numeraire: str
    valuation_price: str
    fee_settlement_currency: str
    numeric_policy: str
    rounding_policy: str

    def __post_init__(self) -> None:
        for name in ("instrument_id", "numeraire", "fee_settlement_currency"):
            object.__setattr__(self, name, _nfc(getattr(self, name), "REFERENCE_FIELD_REQUIRED"))
        object.__setattr__(
            self,
            "instrument_spec_sha256",
            _hash_text(self.instrument_spec_sha256, "INSTRUMENT_SPEC_HASH_INVALID"),
        )
        _require(self.valuation_price == "EVENT_PRICE", "VALUATION_PRICE_INVALID")
        _require(self.numeric_policy == "EXACT_RATIONAL", "NUMERIC_POLICY_INVALID")
        _require(self.rounding_policy == "REJECT_OFF_GRID", "ROUNDING_POLICY_INVALID")

    @classmethod
    def _from_dict(cls, value: Dict[str, Any]) -> "ReferenceSpec":
        _exact_keys(value, tuple(field.name for field in fields(cls)))
        return cls(**value)


def validate_instrument_reference(instrument: InstrumentSpec, reference: ReferenceSpec) -> None:
    _require(reference.instrument_id == instrument.instrument_id, "REFERENCE_INSTRUMENT_ID_MISMATCH")
    _require(
        reference.instrument_spec_sha256 == instrument.canonical_sha256(),
        "REFERENCE_INSTRUMENT_HASH_MISMATCH",
    )
    _require(
        reference.fee_settlement_currency
        in {instrument.base, instrument.quote, instrument.settlement},
        "REFERENCE_FEE_CURRENCY_INCOMPATIBLE",
    )


def _event_common(instance: Any, object_id_name: str) -> None:
    for name in (object_id_name, "source_id", "instrument_id"):
        object.__setattr__(instance, name, _nfc(getattr(instance, name), "EVENT_FIELD_REQUIRED"))
    event_time = instance.event_time
    if type(event_time) is int:
        event_time = InstantNs(event_time)
    else:
        _require(type(event_time) is InstantNs, "EVENT_TIME_INVALID")
    object.__setattr__(instance, "event_time", event_time)
    object.__setattr__(instance, "sequence", _integer(instance.sequence, "EVENT_SEQUENCE_REQUIRED"))


@dataclass(frozen=True)
class MarketEvent(CanonicalContract):
    event_id: str
    source_id: str
    instrument_id: str
    event_type: str
    event_time: InstantNs
    sequence: int
    price: Fraction
    raw_hash: str
    fidelity_level: str

    def __post_init__(self) -> None:
        _event_common(self, "event_id")
        _require(self.event_type == "PRICE", "MARKET_EVENT_TYPE_INVALID")
        price = _exact_fraction(self.price)
        object.__setattr__(self, "price", price)
        _require(price > 0, "PRICE_NOT_POSITIVE")
        object.__setattr__(self, "raw_hash", _hash_text(self.raw_hash, "RAW_HASH_INVALID"))
        _require(self.fidelity_level in {"F0", "F1", "F2", "F3", "F4"}, "FIDELITY_LEVEL_INVALID")

    def local_order_key(self) -> Tuple[int, int, str, str]:
        return (self.event_time, self.sequence, self.source_id, self.event_id)

    def identity_key(self) -> Tuple[str, str, str]:
        return (type(self).__name__, self.source_id, self.event_id)

    @classmethod
    def _from_dict(cls, value: Dict[str, Any]) -> "MarketEvent":
        _exact_keys(value, tuple(field.name for field in fields(cls)))
        return cls(**{**value, "price": parse_canonical_rational(value["price"])})


def validate_market_event_compatibility(
    event: MarketEvent, instrument: InstrumentSpec
) -> None:
    _require(
        event.instrument_id == instrument.instrument_id,
        "MARKET_EVENT_INSTRUMENT_INCOMPATIBLE",
    )
    _require(event.price % instrument.tick_size == 0, "PRICE_OFF_GRID")


@dataclass(frozen=True)
class Fill(CanonicalContract):
    fill_id: str
    order_id: str
    source_id: str
    instrument_id: str
    side: str
    quantity: Fraction
    price: Fraction
    fee_amount: Fraction
    fee_currency: str
    liquidity_role: str
    event_time: InstantNs
    sequence: int

    def __post_init__(self) -> None:
        _event_common(self, "fill_id")
        object.__setattr__(self, "order_id", _nfc(self.order_id, "ORDER_ID_REQUIRED"))
        object.__setattr__(self, "fee_currency", _nfc(self.fee_currency, "CURRENCY_REQUIRED"))
        _require(self.side in {"BUY", "SELL"}, "FILL_SIDE_INVALID")
        _require(self.liquidity_role in {"MAKER", "TAKER"}, "LIQUIDITY_ROLE_INVALID")
        for name, code, allow_zero in (
            ("quantity", "QUANTITY_NOT_POSITIVE", False),
            ("price", "PRICE_NOT_POSITIVE", False),
            ("fee_amount", "FEE_NEGATIVE", True),
        ):
            value = _exact_fraction(getattr(self, name))
            object.__setattr__(self, name, value)
            _require(value >= 0 if allow_zero else value > 0, code)

    def local_order_key(self) -> Tuple[int, int, str, str]:
        return (self.event_time, self.sequence, self.source_id, self.fill_id)

    def identity_key(self) -> Tuple[str, str, str]:
        return (type(self).__name__, self.source_id, self.fill_id)

    @classmethod
    def _from_dict(cls, value: Dict[str, Any]) -> "Fill":
        _exact_keys(value, tuple(field.name for field in fields(cls)))
        return cls(
            **{
                **value,
                "quantity": parse_canonical_rational(value["quantity"]),
                "price": parse_canonical_rational(value["price"]),
                "fee_amount": parse_canonical_rational(value["fee_amount"]),
            }
        )


def validate_fill_compatibility(
    fill: Fill, instrument: InstrumentSpec, reference: ReferenceSpec
) -> None:
    validate_instrument_reference(instrument, reference)
    _require(fill.instrument_id == instrument.instrument_id, "FILL_INSTRUMENT_INCOMPATIBLE")
    _require(
        fill.fee_currency == reference.fee_settlement_currency,
        "FILL_FEE_CURRENCY_INCOMPATIBLE",
    )
    _require(fill.quantity % instrument.lot_size == 0, "QUANTITY_OFF_GRID")
    _require(fill.price % instrument.tick_size == 0, "PRICE_OFF_GRID")


@dataclass(frozen=True)
class AccountEvent(CanonicalContract):
    account_event_id: str
    source_id: str
    source_event_id: str
    account_model: str
    instrument_id: str
    kind: str
    account: str
    delta: Fraction
    currency: str
    event_time: InstantNs
    sequence: int

    def __post_init__(self) -> None:
        _event_common(self, "account_event_id")
        object.__setattr__(self, "source_event_id", _nfc(self.source_event_id, "SOURCE_EVENT_ID_REQUIRED"))
        object.__setattr__(self, "currency", _nfc(self.currency, "CURRENCY_REQUIRED"))
        _require(
            self.account_model in {"SPOT_CASH_V1", "ISOLATED_LINEAR_SHORT_EDU_V1"},
            "ACCOUNT_MODEL_INVALID",
        )
        _require(self.kind in {"INITIALIZE", "TRADE", "FEE", "REALIZED_PNL"}, "ACCOUNT_EVENT_KIND_INVALID")
        _require(self.account in {"BASE", "QUOTE", "COLLATERAL"}, "ACCOUNT_INVALID")
        delta = _exact_fraction(self.delta)
        object.__setattr__(self, "delta", delta)
        _require(not (self.kind == "INITIALIZE" and delta < 0), "ACCOUNT_EVENT_SIGN_MISMATCH")
        _require(not (self.kind == "FEE" and delta > 0), "ACCOUNT_EVENT_SIGN_MISMATCH")

    def local_order_key(self) -> Tuple[int, int, str, str]:
        return (self.event_time, self.sequence, self.source_id, self.account_event_id)

    def identity_key(self) -> Tuple[str, str, str]:
        return (type(self).__name__, self.source_id, self.account_event_id)

    @classmethod
    def _from_dict(cls, value: Dict[str, Any]) -> "AccountEvent":
        _exact_keys(value, tuple(field.name for field in fields(cls)))
        return cls(**{**value, "delta": parse_canonical_rational(value["delta"])})


def validate_account_event_compatibility(event: AccountEvent, instrument: InstrumentSpec) -> None:
    _require(event.instrument_id == instrument.instrument_id, "ACCOUNT_EVENT_INSTRUMENT_INCOMPATIBLE")
    expected = {
        "BASE": instrument.base,
        "QUOTE": instrument.quote,
        "COLLATERAL": instrument.settlement,
    }[event.account]
    _require(event.currency == expected, "ACCOUNT_EVENT_CURRENCY_INCOMPATIBLE")


EventContract = TypeVar("EventContract", MarketEvent, Fill, AccountEvent)


def deduplicate_contracts(items: Iterable[EventContract]) -> Tuple[EventContract, ...]:
    values = tuple(items)
    if not values:
        return ()
    expected_type = type(values[0])
    _require(all(type(item) is expected_type for item in values), "CROSS_TYPE_ORDER_UNDEFINED")
    unique: Dict[Tuple[str, str, str], EventContract] = {}
    for item in values:
        key = item.identity_key()
        previous = unique.get(key)
        if previous is None:
            unique[key] = item
        else:
            _require(previous.canonical_bytes() == item.canonical_bytes(), "DUPLICATE_DIVERGENT")
    return tuple(sorted(unique.values(), key=lambda item: item.local_order_key()))
