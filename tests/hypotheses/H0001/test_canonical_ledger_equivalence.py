from __future__ import annotations

import ast
import json
import subprocess
from dataclasses import replace
from decimal import Decimal, localcontext
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
from tests.hypotheses.H0001.oracle import derive_expected
from tests.hypotheses.H0001.run_experiment import run


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0001"
SCENARIO_PATH = DOSSIER / "SCENARIO.json"
P0_PROJECTION_PATH = DOSSIER / "P0_OBSERVED_PROJECTION.json"
ORACLE_PATH = Path(__file__).with_name("oracle.py")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _spec() -> ShortScenarioSpec:
    scenario = _load_json(SCENARIO_PATH)
    inputs = scenario["inputs"]
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
            for event in scenario["ordered_events"]
        ),
    )


def _as_fraction(value: Fraction) -> Fraction:
    return Fraction(value)


def _as_decimal(value: Fraction) -> Decimal:
    with localcontext() as context:
        context.prec = 50
        return Decimal(value.numerator) / Decimal(value.denominator)


def _replace_event(events: tuple, event_type: type, transform):
    return tuple(transform(event) if isinstance(event, event_type) else event for event in events)


def test_oracle_has_no_production_or_historical_projection_dependency():
    tree = ast.parse(ORACLE_PATH.read_text(encoding="utf-8"))
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
    assert "P0_OBSERVED_PROJECTION.json" not in strings
    assert "grid_bot" not in ORACLE_PATH.read_text(encoding="utf-8")


def test_scenario_provenance_matches_frozen_p0_manifest():
    scenario = _load_json(SCENARIO_PATH)
    p0 = _load_json(ROOT / "REPRODUCIBILITY_MANIFEST.json")
    provenance = scenario["provenance"]

    assert provenance["experiment"] == p0["experiment"]
    assert provenance["config_sha256"] == p0["config_sha256"]
    assert provenance["input_sha256"] == p0["input_sha256"]
    assert provenance["result_sha256"] == p0["result_sha256"]
    assert [event["sequence"] for event in scenario["ordered_events"]] == list(range(1, 7))


def test_mutant_scenario_event_order_drift_is_rejected():
    spec = _spec()
    drifted_plan = tuple(
        replace(event, kind="CLOSE_MTM") if event.sequence == 2 else event
        for event in spec.ordered_events
    )
    with pytest.raises(LedgerInvariantError) as caught:
        build_short_scenario_events(replace(spec, ordered_events=drifted_plan))
    assert caught.value.code == "SCENARIO_EVENT_PLAN_MISMATCH"


def test_runner_records_the_executed_git_head():
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert run()["producer_code_commit"] == head


def test_canonical_ledger_matches_independent_exact_oracle():
    expected = derive_expected(SCENARIO_PATH)
    snapshots = replay_ledger(build_short_scenario_events(_spec()))
    expected_states = expected["states"]

    assert len(snapshots) == len(expected_states) == 6
    for actual, oracle in zip(snapshots, expected_states):
        assert actual.sequence == oracle["sequence"]
        assert _as_fraction(actual.collateral_sol) == oracle["collateral_sol"]
        assert _as_fraction(actual.fees_usd) == oracle["fees_usd"]
        assert _as_fraction(actual.realized_price_pnl_usd) == oracle["realized_price_pnl_usd"]
        assert actual.active_positions == oracle["active_positions"]
        assert _as_fraction(actual.position_quantity_sol) == oracle["position_quantity_sol"]
        assert _as_fraction(actual.position_margin_usd) == oracle["position_margin_usd"]

    assert expected["margin_usd"] == Fraction(300)
    assert expected["quantity_sol"] == Fraction(6)
    assert expected["entry_fee_usd"] == Fraction(3, 10)
    assert expected["gross_pnl_usd"] == Fraction(-30)
    assert expected["exit_fee_usd"] == Fraction(63, 100)
    assert expected["net_pnl_usd"] == Fraction(-3063, 100)
    assert expected["final_collateral_sol"] == Fraction(67937, 7000)


def test_h0001_result_matches_separate_p0_observed_projection():
    observed = _load_json(P0_PROJECTION_PATH)["projection"]
    expected = derive_expected(SCENARIO_PATH)
    snapshots = replay_ledger(build_short_scenario_events(_spec()))
    final = snapshots[-1]
    close = next(event for event in build_short_scenario_events(_spec()) if isinstance(event, CloseShort))
    opening = next(event for event in build_short_scenario_events(_spec()) if isinstance(event, OpenShort))

    assert opening.quantity_sol == Fraction(observed["open_quantity_sol"])
    assert opening.notional_usd == Fraction(observed["open_notional_usd"])
    assert opening.fee_usd == Fraction(observed["open_commission_usd"])
    assert close.fee_usd == Fraction(observed["close_commission_usd"])
    assert final.fees_usd == Fraction(observed["close_total_commission_usd"])
    assert close.net_pnl_usd == Fraction(observed["close_net_pnl_usd"])
    assert abs(_as_decimal(close.collateral_delta_sol) - Decimal(observed["close_pnl_sol"])) <= Decimal("5e-13")
    assert abs(_as_decimal(final.collateral_sol) - Decimal(observed["final_collateral_sol"])) <= Decimal("5e-13")
    assert _as_fraction(final.collateral_sol) == expected["final_collateral_sol"]
    assert observed["trade_count"] == 2


def _mutant_double_entry_fee(events: tuple) -> tuple:
    return _replace_event(
        events,
        OpenShort,
        lambda event: replace(
            event,
            fee_usd=event.fee_usd * 2,
            collateral_delta_sol=event.collateral_delta_sol * 2,
        ),
    )


def _mutant_invert_pnl_sign(events: tuple) -> tuple:
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


def _mutant_double_leverage(events: tuple) -> tuple:
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


def _mutant_omit_exit_fee(events: tuple) -> tuple:
    def mutate(event: CloseShort) -> CloseShort:
        return replace(
            event,
            fee_usd=Fraction(0),
            net_pnl_usd=event.gross_pnl_usd,
            collateral_delta_sol=event.gross_pnl_usd / event.price_usd_per_sol,
        )

    return _replace_event(events, CloseShort, mutate)


def _mutant_swap_close_and_open(events: tuple) -> tuple:
    opening = next(event for event in events if isinstance(event, OpenShort))
    closing = next(event for event in events if isinstance(event, CloseShort))
    return (events[0], replace(closing, sequence=2), replace(opening, sequence=3))


def _mutant_usd_as_sol(events: tuple) -> tuple:
    return _replace_event(
        events,
        OpenShort,
        lambda event: replace(event, collateral_delta_sol=-event.fee_usd),
    )


@pytest.mark.parametrize(
    ("mutation_id", "mutate", "expected_code"),
    [
        ("M1_DOUBLE_ENTRY_FEE", _mutant_double_entry_fee, "OPEN_FEE_MISMATCH"),
        ("M2_INVERT_PNL_SIGN", _mutant_invert_pnl_sign, "CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH"),
        ("M3_DOUBLE_LEVERAGE", _mutant_double_leverage, "CLOSE_PNL_SIGN_OR_LEVERAGE_MISMATCH"),
        ("M4_OMIT_EXIT_FEE", _mutant_omit_exit_fee, "CLOSE_FEE_MISMATCH"),
        ("M5_SWAP_CLOSE_AND_OPEN", _mutant_swap_close_and_open, "POSITION_MISSING"),
        ("M6_USD_AS_SOL", _mutant_usd_as_sol, "OPEN_FEE_CURRENCY_MISMATCH"),
    ],
)
def test_required_mutants_are_rejected(mutation_id, mutate, expected_code):
    events = build_short_scenario_events(_spec())
    with pytest.raises(LedgerInvariantError) as caught:
        replay_ledger(mutate(events))
    assert caught.value.code == expected_code, mutation_id
