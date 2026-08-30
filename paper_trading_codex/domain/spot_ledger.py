"""Ledger spot cash minimal préenregistré par H0004."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple

from .contracts import (
    AccountEvent,
    Fill,
    InstrumentSpec,
    ReferenceSpec,
    canonical_sha256,
    validate_account_event_compatibility,
    validate_fill_compatibility,
    validate_instrument_reference,
)


class SpotLedgerInvariantError(ValueError):
    """Rejet spot avec code stable."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise SpotLedgerInvariantError(code)


TypedEventKey = Tuple[str, int, int, str, str]


@dataclass(frozen=True)
class SpotAccountState:
    account_model: str
    instrument_spec_sha256: str
    reference_spec_sha256: str
    base_balance: Fraction
    quote_balance: Fraction
    fees_by_currency: Tuple[Tuple[str, Fraction], ...]
    last_event_key: TypedEventKey | None


def create_spot_account(
    instrument: InstrumentSpec, reference: ReferenceSpec
) -> SpotAccountState:
    validate_instrument_reference(instrument, reference)
    _require(instrument.instrument_type == "SPOT", "SPOT_INSTRUMENT_TYPE_REQUIRED")
    _require(
        instrument.contract_multiplier == 1,
        "SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED",
    )
    return SpotAccountState(
        account_model="SPOT_CASH_V1",
        instrument_spec_sha256=instrument.canonical_sha256(),
        reference_spec_sha256=reference.canonical_sha256(),
        base_balance=Fraction(0),
        quote_balance=Fraction(0),
        fees_by_currency=(),
        last_event_key=None,
    )


def _account_event_key(event: AccountEvent) -> TypedEventKey:
    return (
        "ACCOUNT_EVENT",
        event.event_time,
        event.sequence,
        event.source_id,
        event.account_event_id,
    )


def _fill_key(fill: Fill) -> TypedEventKey:
    return ("FILL", fill.event_time, fill.sequence, fill.source_id, fill.fill_id)


def apply_initialization(
    state: SpotAccountState, event: AccountEvent, instrument: InstrumentSpec
) -> SpotAccountState:
    _require(state.account_model == "SPOT_CASH_V1", "SPOT_ACCOUNT_MODEL_REQUIRED")
    _require(
        state.instrument_spec_sha256 == instrument.canonical_sha256(),
        "SPOT_STATE_INSTRUMENT_MISMATCH",
    )
    _require(event.account_model == "SPOT_CASH_V1", "SPOT_ACCOUNT_MODEL_REQUIRED")
    _require(event.kind == "INITIALIZE", "SPOT_INITIALIZATION_EVENT_REQUIRED")
    _require(
        state.last_event_key is None or state.last_event_key[0] == "ACCOUNT_EVENT",
        "SPOT_INITIALIZATION_AFTER_FILL",
    )
    validate_account_event_compatibility(event, instrument)
    _require(event.account in {"BASE", "QUOTE"}, "SPOT_INITIALIZATION_ACCOUNT_UNSUPPORTED")
    new_base = state.base_balance + (event.delta if event.account == "BASE" else 0)
    new_quote = state.quote_balance + (event.delta if event.account == "QUOTE" else 0)
    _require(new_base >= 0 and new_quote >= 0, "SPOT_NEGATIVE_BALANCE")
    return SpotAccountState(
        account_model=state.account_model,
        instrument_spec_sha256=state.instrument_spec_sha256,
        reference_spec_sha256=state.reference_spec_sha256,
        base_balance=new_base,
        quote_balance=new_quote,
        fees_by_currency=state.fees_by_currency,
        last_event_key=_account_event_key(event),
    )


def _derived_event_id(fill: Fill, kind: str, account: str) -> str:
    identity = {
        "account_model": "SPOT_CASH_V1",
        "source_id": fill.source_id,
        "source_event_id": fill.fill_id,
        "kind": kind,
        "account": account,
    }
    return f"ae:{canonical_sha256(identity)}"


def _derived_event(
    fill: Fill, *, kind: str, account: str, delta: Fraction, currency: str
) -> AccountEvent:
    return AccountEvent(
        account_event_id=_derived_event_id(fill, kind, account),
        source_id=fill.source_id,
        source_event_id=fill.fill_id,
        account_model="SPOT_CASH_V1",
        instrument_id=fill.instrument_id,
        kind=kind,
        account=account,
        delta=delta,
        currency=currency,
        event_time=fill.event_time,
        sequence=fill.sequence,
    )


def _validate_fill_progression(state: SpotAccountState, fill: Fill) -> None:
    if state.last_event_key is None or state.last_event_key[0] == "ACCOUNT_EVENT":
        return
    current = fill.local_order_key()
    previous = state.last_event_key[1:]
    _require(current != previous, "SPOT_FILL_REAPPLICATION")
    _require(current > previous, "SPOT_FILL_OUT_OF_ORDER")


def apply_fill(
    state: SpotAccountState,
    fill: Fill,
    instrument: InstrumentSpec,
    reference: ReferenceSpec,
) -> tuple[SpotAccountState, tuple[AccountEvent, ...]]:
    _validate_fill_progression(state, fill)
    _require(state.account_model == "SPOT_CASH_V1", "SPOT_ACCOUNT_MODEL_REQUIRED")
    _require(
        state.instrument_spec_sha256 == instrument.canonical_sha256(),
        "SPOT_STATE_INSTRUMENT_MISMATCH",
    )
    _require(
        state.reference_spec_sha256 == reference.canonical_sha256(),
        "SPOT_STATE_REFERENCE_MISMATCH",
    )
    _require(
        instrument.contract_multiplier == 1,
        "SPOT_CONTRACT_MULTIPLIER_UNSUPPORTED",
    )
    validate_fill_compatibility(fill, instrument, reference)
    _require(
        fill.fee_currency == instrument.quote,
        "SPOT_FEE_CURRENCY_UNSUPPORTED",
    )

    trade_quote = fill.quantity * fill.price
    if fill.side == "BUY":
        base_delta = fill.quantity
        quote_trade_delta = -trade_quote
        _require(
            state.quote_balance >= trade_quote + fill.fee_amount,
            "SPOT_INSUFFICIENT_QUOTE",
        )
    else:
        base_delta = -fill.quantity
        quote_trade_delta = trade_quote
        _require(state.base_balance >= fill.quantity, "SPOT_INSUFFICIENT_BASE")

    events = tuple(
        sorted(
            (
                _derived_event(
                    fill,
                    kind="TRADE",
                    account="BASE",
                    delta=base_delta,
                    currency=instrument.base,
                ),
                _derived_event(
                    fill,
                    kind="TRADE",
                    account="QUOTE",
                    delta=quote_trade_delta,
                    currency=instrument.quote,
                ),
                _derived_event(
                    fill,
                    kind="FEE",
                    account="QUOTE",
                    delta=-fill.fee_amount,
                    currency=instrument.quote,
                ),
            ),
            key=lambda event: event.local_order_key(),
        )
    )
    for event in events:
        validate_account_event_compatibility(event, instrument)

    base_change = sum(
        (event.delta for event in events if event.account == "BASE"), Fraction(0)
    )
    quote_change = sum(
        (event.delta for event in events if event.account == "QUOTE"), Fraction(0)
    )
    new_base = state.base_balance + base_change
    new_quote = state.quote_balance + quote_change
    _require(new_base >= 0 and new_quote >= 0, "SPOT_NEGATIVE_BALANCE")

    fees = dict(state.fees_by_currency)
    fees[fill.fee_currency] = fees.get(fill.fee_currency, Fraction(0)) + fill.fee_amount
    new_state = SpotAccountState(
            account_model=state.account_model,
            instrument_spec_sha256=state.instrument_spec_sha256,
            reference_spec_sha256=state.reference_spec_sha256,
            base_balance=new_base,
            quote_balance=new_quote,
            fees_by_currency=tuple(sorted(fees.items())),
            last_event_key=_fill_key(fill),
    )
    validate_transition_conservation(state, new_state, events)
    return new_state, events


def validate_transition_conservation(
    old_state: SpotAccountState,
    new_state: SpotAccountState,
    events: tuple[AccountEvent, ...],
) -> None:
    base_delta = sum((event.delta for event in events if event.account == "BASE"), Fraction())
    quote_delta = sum((event.delta for event in events if event.account == "QUOTE"), Fraction())
    _require(
        new_state.base_balance == old_state.base_balance + base_delta
        and new_state.quote_balance == old_state.quote_balance + quote_delta,
        "SPOT_BALANCE_MOVEMENT_UNEXPLAINED",
    )


def equity_quote(state: SpotAccountState, valuation_price: Fraction) -> Fraction:
    _require(valuation_price > 0, "SPOT_VALUATION_PRICE_NOT_POSITIVE")
    return state.quote_balance + state.base_balance * valuation_price
