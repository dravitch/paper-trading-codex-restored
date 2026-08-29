"""Matérialise le résultat déterministe H0003 depuis les vecteurs préenregistrés."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from paper_trading_codex.domain.contracts import (
    AccountEvent,
    Fill,
    InstrumentSpec,
    MarketEvent,
    ReferenceSpec,
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

    return {
        "schema_version": 1,
        "hypothesis_id": "H0003",
        "producer_code_commit": _git_head(),
        "previous_blocked_preregistration": "ed2731da82326cf938b3634670e7cd1f6e50445f",
        "normative_decision_commit": "0fe56109974790792eeaf39e341386164af36822",
        "normative_addendum_commit": "d817a1642f7123ac367f7b0b7c03186b2d161925",
        "ready_preregistration_commit": "be6678a562f77587af6f52ee7607d1a89fa674c1",
        "contract_results": results,
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
