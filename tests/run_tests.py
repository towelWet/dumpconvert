#!/usr/bin/env python3
# run_tests.py — convert each fixture and compare with tests/expected/<name>.json.
# Why: proves every adapter on synthetic data; never runs on real user chats.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import json, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "lib"))
from discover import discover
from convert import convert


def run_tests():
    adapters, failed = discover(), 0
    for fixture in sorted((HERE / "fixtures").glob("*.jsonl")):
        expected = json.loads((HERE / "expected" / f"{fixture.stem}.json").read_text())
        got = convert(fixture, adapters)
        ok = got == expected                                       # exact match, incl. None for empty
        failed += not ok
        print(("PASS " if ok else "FAIL ") + fixture.stem + ("" if ok else f"\n  got {got}"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_tests())
