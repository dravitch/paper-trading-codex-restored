from __future__ import annotations

import ast
import json
from fractions import Fraction
from pathlib import Path

import pytest

from paper_trading_codex.domain.ledger import (
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
