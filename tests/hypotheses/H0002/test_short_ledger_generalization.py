from __future__ import annotations

import ast
from copy import deepcopy
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from paper_trading_codex.domain.ledger import (
    CloseShort,
    LedgerInvariantError,
    OpenShort,
    PlannedEvent,
    ShortScenarioSpec,
    build_short_scenario_events,
    replay_ledger,
)
from tests.hypotheses.H0002.oracle import derive_family


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0002"
FAMILY_PATH = DOSSIER / "SCENARIO_FAMILY.json"
EXPECTATIONS_PATH = DOSSIER / "ORACLE_EXPECTATIONS.json"
ORACLE_PATH = Path(__file__).with_name("oracle.py")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


FAMILY = _load(FAMILY_PATH)
CASES = FAMILY["scenarios"]
CASE_IDS = tuple(case["scenario_id"] for case in CASES)


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


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def test_oracle_cannot_import_production_or_read_registered_answers():
    source = ORACLE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = []
    strings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            strings.append(node.value)

    assert not any(name.startswith("paper_trading_codex") for name in imports)
    assert "ORACLE_EXPECTATIONS.json" not in strings
    assert "grid_bot" not in source


def test_executable_oracle_reproduces_preregistered_expectations():
    derived = derive_family(FAMILY_PATH)
    registered = _load(EXPECTATIONS_PATH)["expectations"]

    assert tuple(derived) == CASE_IDS
    for scenario_id, expected in registered.items():
        actual = derived[scenario_id]
        assert {
            key: _fraction_text(actual[key])
            for key in expected
        } == expected


@pytest.mark.parametrize("case", CASES, ids=CASE_IDS)
def test_unchanged_h0001_ledger_matches_family_oracle(case):
    expected = derive_family(FAMILY_PATH)[case["scenario_id"]]
    snapshots = replay_ledger(build_short_scenario_events(_spec(case)))

    assert len(snapshots) == len(expected["states"])
    for actual, oracle in zip(snapshots, expected["states"]):
        assert actual.sequence == oracle["sequence"]
        assert actual.collateral_sol == oracle["collateral_sol"]
        assert actual.fees_usd == oracle["fees_usd"]
        assert actual.realized_price_pnl_usd == oracle["realized_price_pnl_usd"]
        assert actual.active_positions == oracle["active_positions"]
        assert actual.position_quantity_sol == oracle["position_quantity_sol"]
        assert actual.position_margin_usd == oracle["position_margin_usd"]

    assert snapshots[-1].collateral_sol == expected["final_collateral_sol"]


def test_scenario_identity_and_family_order_do_not_affect_calculation():
    expected = derive_family(FAMILY_PATH)
    for case in reversed(CASES):
        anonymous = deepcopy(case)
        scenario_id = anonymous.pop("scenario_id")
        snapshots = replay_ledger(build_short_scenario_events(_spec(anonymous)))
        assert snapshots[-1].collateral_sol == expected[scenario_id]["final_collateral_sol"]

    production_source = (ROOT / "paper_trading_codex" / "domain" / "ledger.py").read_text(
        encoding="utf-8"
    )
    assert "scenario_id" not in production_source


def _replace_event(events: tuple, event_type: type, transform) -> tuple:
    return tuple(transform(event) if isinstance(event, event_type) else event for event in events)


def _double_entry_fee(events: tuple) -> tuple:
    return _replace_event(
        events,
        OpenShort,
        lambda event: replace(
            event,
            fee_usd=event.fee_usd * 2,
            collateral_delta_sol=event.collateral_delta_sol * 2,
        ),
    )


def _invert_pnl(events: tuple) -> tuple:
    def mutate(event: CloseShort) -> CloseShort:
        gross = -event.gross_pnl_usd
        net = gross - event.fee_usd
        return replace(
            event,
            gross_pnl_usd=gross,
            net_pnl_usd=net,
            collateral_delta_sol=net / event.price_usd_per_sol,
        )

    return _replace_event(events, CloseShort, mutate)


def _double_leverage(events: tuple) -> tuple:
    def mutate(event: CloseShort) -> CloseShort:
        gross = event.gross_pnl_usd * 2
        net = gross - event.fee_usd
        return replace(
            event,
            gross_pnl_usd=gross,
            net_pnl_usd=net,
            collateral_delta_sol=net / event.price_usd_per_sol,
        )

    return _replace_event(events, CloseShort, mutate)


def _omit_exit_fee(events: tuple) -> tuple:
    def mutate(event: CloseShort) -> CloseShort:
        return replace(
            event,
            fee_usd=Fraction(0),
            net_pnl_usd=event.gross_pnl_usd,
            collateral_delta_sol=event.gross_pnl_usd / event.price_usd_per_sol,
        )

    return _replace_event(events, CloseShort, mutate)


def _usd_as_sol(events: tuple) -> tuple:
    return _replace_event(
        events,
        OpenShort,
        lambda event: replace(event, collateral_delta_sol=-event.fee_usd),
    )


@pytest.mark.parametrize(
    ("scenario_id", "mutate", "expected_code"),
    [
        ("WIN_STANDARD", _invert_pnl, "CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH"),
        ("LOSS_STANDARD", _double_entry_fee, "OPEN_FEE_MISMATCH"),
        ("FLAT_HIGH_FEES", _omit_exit_fee, "CLOSE_FEE_MISMATCH"),
        ("SMALL_FRACTIONAL", _double_leverage, "CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH"),
        ("LARGE_WIN", _usd_as_sol, "OPEN_FEE_CURRENCY_MISMATCH"),
    ],
)
def test_accounting_mutants_are_rejected(scenario_id, mutate, expected_code):
    case = next(case for case in CASES if case["scenario_id"] == scenario_id)
    events = build_short_scenario_events(_spec(case))
    with pytest.raises(LedgerInvariantError) as caught:
        replay_ledger(mutate(events))
    assert caught.value.code == expected_code


@pytest.mark.parametrize("drift", ["kind", "price", "order"])
def test_preregistered_event_plan_drift_is_rejected(drift):
    case = deepcopy(CASES[0])
    if drift == "kind":
        case["ordered_events"][1]["kind"] = "CLOSE_MTM"
    elif drift == "price":
        case["ordered_events"][2]["price_usd_per_sol"] = "96"
    else:
        case["ordered_events"][2], case["ordered_events"][3] = (
            case["ordered_events"][3],
            case["ordered_events"][2],
        )

    with pytest.raises(LedgerInvariantError) as caught:
        build_short_scenario_events(_spec(case))
    assert caught.value.code == "SCENARIO_EVENT_PLAN_MISMATCH"
