"""Ledger canonique minimal pour H0001.

Le module ne connaît ni stratégie, ni provider, ni temps mural. Il reçoit une séquence
totale d'événements et retourne de nouveaux états immuables.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Optional, Tuple, Union


ZERO = Fraction(0)


class LedgerInvariantError(ValueError):
    """Violation comptable avec code stable utilisable par les mutants."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ShortScenarioSpec:
    initial_capital_usd: Fraction
    initial_price_usd_per_sol: Fraction
    margin_fraction: Fraction
    leverage: Fraction
    maker_fee_rate: Fraction
    taker_fee_rate: Fraction
    prices_usd_per_sol: Tuple[Fraction, ...]


@dataclass(frozen=True)
class InitializeCollateral:
    sequence: int
    price_usd_per_sol: Fraction
    collateral_credit_sol: Fraction
    kind: str = "INITIALIZE_COLLATERAL"


@dataclass(frozen=True)
class OpenShort:
    sequence: int
    price_usd_per_sol: Fraction
    quantity_sol: Fraction
    notional_usd: Fraction
    margin_usd: Fraction
    leverage: Fraction
    fee_rate: Fraction
    fee_usd: Fraction
    collateral_delta_sol: Fraction
    kind: str = "OPEN_SHORT"


@dataclass(frozen=True)
class ObservePrice:
    sequence: int
    price_usd_per_sol: Fraction
    kind: str = "OBSERVE"


@dataclass(frozen=True)
class CloseShort:
    sequence: int
    price_usd_per_sol: Fraction
    quantity_sol: Fraction
    fee_rate: Fraction
    gross_pnl_usd: Fraction
    fee_usd: Fraction
    net_pnl_usd: Fraction
    collateral_delta_sol: Fraction
    kind: str = "CLOSE_MTM"


LedgerEvent = Union[InitializeCollateral, OpenShort, ObservePrice, CloseShort]


@dataclass(frozen=True)
class ShortPosition:
    quantity_sol: Fraction
    entry_price_usd_per_sol: Fraction
    notional_usd: Fraction
    margin_usd: Fraction
    leverage: Fraction


@dataclass(frozen=True)
class LedgerState:
    collateral_sol: Fraction = ZERO
    fees_usd: Fraction = ZERO
    realized_price_pnl_usd: Fraction = ZERO
    position: Optional[ShortPosition] = None
    initialized: bool = False
    last_sequence: int = 0


@dataclass(frozen=True)
class LedgerSnapshot:
    sequence: int
    event_kind: str
    price_usd_per_sol: Fraction
    collateral_sol: Fraction
    fees_usd: Fraction
    realized_price_pnl_usd: Fraction
    active_positions: int
    position_quantity_sol: Fraction
    position_margin_usd: Fraction


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise LedgerInvariantError(code)


def _validate_common(state: LedgerState, event: LedgerEvent) -> None:
    _require(event.sequence == state.last_sequence + 1, "EVENT_SEQUENCE_INVALID")
    _require(event.price_usd_per_sol > ZERO, "PRICE_NOT_POSITIVE")


def apply_event(state: LedgerState, event: LedgerEvent) -> LedgerState:
    """Applique un événement et retourne un nouvel état sans muter l'ancien."""

    _validate_common(state, event)

    if isinstance(event, InitializeCollateral):
        _require(not state.initialized, "COLLATERAL_ALREADY_INITIALIZED")
        _require(event.sequence == 1, "INITIALIZATION_NOT_FIRST")
        _require(event.collateral_credit_sol > ZERO, "INITIAL_COLLATERAL_NOT_POSITIVE")
        return replace(
            state,
            collateral_sol=event.collateral_credit_sol,
            initialized=True,
            last_sequence=event.sequence,
        )

    _require(state.initialized, "LEDGER_NOT_INITIALIZED")

    if isinstance(event, OpenShort):
        _require(state.position is None, "POSITION_ALREADY_OPEN")
        _require(event.quantity_sol > ZERO, "QUANTITY_NOT_POSITIVE")
        _require(event.margin_usd > ZERO, "MARGIN_NOT_POSITIVE")
        _require(event.leverage > ZERO, "LEVERAGE_NOT_POSITIVE")
        _require(ZERO <= event.fee_rate < Fraction(1), "FEE_RATE_INVALID")
        _require(
            event.notional_usd == event.quantity_sol * event.price_usd_per_sol,
            "OPEN_NOTIONAL_MISMATCH",
        )
        _require(
            event.notional_usd == event.margin_usd * event.leverage,
            "OPEN_LEVERAGE_MISMATCH",
        )
        _require(event.fee_usd == event.notional_usd * event.fee_rate, "OPEN_FEE_MISMATCH")
        _require(
            event.collateral_delta_sol == -(event.fee_usd / event.price_usd_per_sol),
            "OPEN_FEE_CURRENCY_MISMATCH",
        )
        return replace(
            state,
            collateral_sol=state.collateral_sol + event.collateral_delta_sol,
            fees_usd=state.fees_usd + event.fee_usd,
            position=ShortPosition(
                quantity_sol=event.quantity_sol,
                entry_price_usd_per_sol=event.price_usd_per_sol,
                notional_usd=event.notional_usd,
                margin_usd=event.margin_usd,
                leverage=event.leverage,
            ),
            last_sequence=event.sequence,
        )

    if isinstance(event, ObservePrice):
        return replace(state, last_sequence=event.sequence)

    _require(state.position is not None, "POSITION_MISSING")
    position = state.position
    _require(event.quantity_sol == position.quantity_sol, "CLOSE_QUANTITY_MISMATCH")
    _require(ZERO <= event.fee_rate < Fraction(1), "FEE_RATE_INVALID")
    expected_gross = position.quantity_sol * (
        position.entry_price_usd_per_sol - event.price_usd_per_sol
    )
    expected_fee = position.quantity_sol * event.price_usd_per_sol * event.fee_rate
    _require(event.gross_pnl_usd == expected_gross, "CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH")
    _require(event.fee_usd == expected_fee, "CLOSE_FEE_MISMATCH")
    _require(event.net_pnl_usd == event.gross_pnl_usd - event.fee_usd, "CLOSE_NET_MISMATCH")
    _require(
        event.collateral_delta_sol == event.net_pnl_usd / event.price_usd_per_sol,
        "CLOSE_SETTLEMENT_CURRENCY_MISMATCH",
    )
    return replace(
        state,
        collateral_sol=state.collateral_sol + event.collateral_delta_sol,
        fees_usd=state.fees_usd + event.fee_usd,
        realized_price_pnl_usd=state.realized_price_pnl_usd + event.gross_pnl_usd,
        position=None,
        last_sequence=event.sequence,
    )


def build_short_scenario_events(spec: ShortScenarioSpec) -> Tuple[LedgerEvent, ...]:
    """Construit les événements H0001 depuis les seules conventions préenregistrées."""

    _require(len(spec.prices_usd_per_sol) >= 2, "PRICE_SEQUENCE_TOO_SHORT")
    entry_price = spec.prices_usd_per_sol[0]
    exit_price = spec.prices_usd_per_sol[-1]
    _require(spec.initial_capital_usd > ZERO, "INITIAL_CAPITAL_NOT_POSITIVE")
    _require(spec.initial_price_usd_per_sol > ZERO, "INITIAL_PRICE_NOT_POSITIVE")
    _require(ZERO < spec.margin_fraction <= Fraction(1), "MARGIN_FRACTION_INVALID")

    collateral = spec.initial_capital_usd / spec.initial_price_usd_per_sol
    equity_entry = collateral * entry_price
    margin = equity_entry * spec.margin_fraction
    notional = margin * spec.leverage
    quantity = notional / entry_price
    entry_fee = notional * spec.maker_fee_rate

    events: Tuple[LedgerEvent, ...] = (
        InitializeCollateral(1, spec.initial_price_usd_per_sol, collateral),
        OpenShort(
            2,
            entry_price,
            quantity,
            notional,
            margin,
            spec.leverage,
            spec.maker_fee_rate,
            entry_fee,
            -(entry_fee / entry_price),
        ),
    )
    sequence = 3
    for price in spec.prices_usd_per_sol[1:]:
        events += (ObservePrice(sequence, price),)
        sequence += 1

    gross_pnl = quantity * (entry_price - exit_price)
    exit_fee = quantity * exit_price * spec.taker_fee_rate
    net_pnl = gross_pnl - exit_fee
    events += (
        CloseShort(
            sequence,
            exit_price,
            quantity,
            spec.taker_fee_rate,
            gross_pnl,
            exit_fee,
            net_pnl,
            net_pnl / exit_price,
        ),
    )
    return events


def replay_ledger(events: Tuple[LedgerEvent, ...]) -> Tuple[LedgerSnapshot, ...]:
    """Rejoue une séquence totale et retourne chaque projection observable."""

    state = LedgerState()
    snapshots = []
    for event in events:
        state = apply_event(state, event)
        snapshots.append(
            LedgerSnapshot(
                sequence=event.sequence,
                event_kind=event.kind,
                price_usd_per_sol=event.price_usd_per_sol,
                collateral_sol=state.collateral_sol,
                fees_usd=state.fees_usd,
                realized_price_pnl_usd=state.realized_price_pnl_usd,
                active_positions=1 if state.position is not None else 0,
                position_quantity_sol=(
                    state.position.quantity_sol if state.position is not None else ZERO
                ),
                position_margin_usd=(
                    state.position.margin_usd if state.position is not None else ZERO
                ),
            )
        )
    return tuple(snapshots)
