"""Matérialise le résultat déterministe H0003 depuis les vecteurs préenregistrés."""

from __future__ import annotations

import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess

from paper_trading_codex.domain.contracts import (
    AccountEvent,
    ContractValidationError,
    DurationNs,
    Fill,
    InstrumentSpec,
    InstantNs,
    MarketEvent,
    ReferenceSpec,
    validate_market_event_compatibility,
)


ROOT = Path(__file__).resolve().parents[3]
DOSSIER = ROOT / "docs" / "fusion" / "hypotheses" / "H0003"
TYPES = {
    "InstrumentSpec": InstrumentSpec,
    "ReferenceSpec": ReferenceSpec,
    "MarketEvent": MarketEvent,
    "Fill": Fill,
    "AccountEvent": AccountEvent,
}


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _rejected_with_code(operation, expected: str) -> bool:
    try:
        operation()
    except ContractValidationError as error:
        return error.code == expected
    return False


def run() -> dict:
    vectors = json.loads((DOSSIER / "ORACLE_VECTORS.json").read_text(encoding="utf-8"))
    results = {}
    for name, contract_type in TYPES.items():
        vector = vectors["valid_objects"][name]
        expected = vector["canonical_json"].encode()
        contract = contract_type.from_canonical_bytes(expected)
        actual = contract.canonical_bytes()
        if actual != expected:
            raise AssertionError(f"H0003_CANONICAL_BYTES_DIVERGENCE:{name}")
        digest = hashlib.sha256(actual).hexdigest()
        if digest != vector["sha256"]:
            raise AssertionError(f"H0003_SHA256_DIVERGENCE:{name}")
        restored = contract_type.from_canonical_bytes(actual)
        if restored.canonical_bytes() != actual:
            raise AssertionError(f"H0003_ROUNDTRIP_DIVERGENCE:{name}")
        results[name] = {"canonical_bytes_equal": True, "roundtrip_equal": True, "sha256": digest}

    instrument = TYPES["InstrumentSpec"].from_canonical_bytes(
        vectors["valid_objects"]["InstrumentSpec"]["canonical_json"].encode()
    )
    fill = TYPES["Fill"].from_canonical_bytes(
        vectors["valid_objects"]["Fill"]["canonical_json"].encode()
    )
    market_event = TYPES["MarketEvent"].from_canonical_bytes(
        vectors["valid_objects"]["MarketEvent"]["canonical_json"].encode()
    )
    correction_regressions = {
        "C4_INSTANT_STR": _rejected_with_code(
            lambda: InstantNs("not-an-int"), "INSTANT_NS_TYPE_INVALID"
        ),
        "C4_DURATION_BOOL": _rejected_with_code(
            lambda: DurationNs(True), "DURATION_NS_TYPE_INVALID"
        ),
        "F1_MULTIPLIER_BOOL": _rejected_with_code(
            lambda: replace(instrument, contract_multiplier=True),
            "RATIONAL_VALUE_TYPE_INVALID",
        ),
        "F1_QUANTITY_BINARY64": _rejected_with_code(
            lambda: replace(fill, quantity=0.1), "RATIONAL_VALUE_TYPE_INVALID"
        ),
        "F1_PRICE_BINARY64": _rejected_with_code(
            lambda: replace(fill, price=100.005), "RATIONAL_VALUE_TYPE_INVALID"
        ),
        "F1_FEE_BOOL": _rejected_with_code(
            lambda: replace(fill, fee_amount=False), "RATIONAL_VALUE_TYPE_INVALID"
        ),
        "F2_MARKET_PRICE_OFF_GRID": _rejected_with_code(
            lambda: validate_market_event_compatibility(
                replace(market_event, price=Fraction(20001, 200)), instrument
            ),
            "PRICE_OFF_GRID",
        ),
    }
    if not all(correction_regressions.values()):
        raise AssertionError("H0003_REJECT_FINDING_NOT_CLOSED")

    return {
        "schema_version": 1,
        "hypothesis_id": "H0003",
        "producer_code_commit": _git_head(),
        "rejected_packet_commit": "44893b0061f13e8a03c4a27f4d299b8b65b5943c",
        "human_rejection_decision_commit": "426781e",
        "previous_blocked_preregistration": "ed2731da82326cf938b3634670e7cd1f6e50445f",
        "normative_decision_commit": "0fe56109974790792eeaf39e341386164af36822",
        "normative_addendum_commit": "d817a1642f7123ac367f7b0b7c03186b2d161925",
        "ready_preregistration_commit": "be6678a562f77587af6f52ee7607d1a89fa674c1",
        "contract_results": results,
        "correction_regressions": correction_regressions,
        "all_contract_vectors_exact": all(
            result["canonical_bytes_equal"] and result["roundtrip_equal"]
            for result in results.values()
        ),
        "claims_not_proven": [
            "P1_PASS",
            "spot_ledger_valid",
            "short_ledger_p1_conformant",
            "clock_enforcement_valid",
            "replay_valid",
            "exchange_fidelity",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
