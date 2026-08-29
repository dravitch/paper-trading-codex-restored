"""Régénère la section de comptage de STATUS.md depuis la collecte Pytest."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
START = "<!-- TEST_STATUS_START -->"
END = "<!-- TEST_STATUS_END -->"


def collect() -> tuple[int, str]:
    result = subprocess.run(
        ["python", "-m", "pytest", "tests", "--collect-only", "-q"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.search(r"(\d+) tests? collected", result.stdout)
    if not match:
        raise RuntimeError("Pytest collection count not found")
    count = int(match.group(1))
    files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("test_*.py")
    )
    body = (
        f"{START}\n"
        f"- Tests collectés : **{count}** dans **{len(files)}** fichiers.\n"
        f"- Commande canonique : `python -m pytest tests -q`.\n"
        f"- Fichiers : {', '.join(f'`{name}`' for name in files)}.\n"
        f"{END}"
    )
    return count, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    _, body = collect()
    current = STATUS.read_text(encoding="utf-8")
    updated = re.sub(
        rf"{re.escape(START)}.*?{re.escape(END)}",
        body,
        current,
        flags=re.DOTALL,
    )
    if args.check:
        if updated != current:
            print("STATUS.md is stale")
            return 1
        print("STATUS.md is current")
        return 0
    STATUS.write_text(updated, encoding="utf-8")
    print(f"Updated {STATUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
