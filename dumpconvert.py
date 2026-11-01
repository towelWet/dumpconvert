#!/usr/bin/env python3
# dumpconvert.py — CLI: dumpboth .jsonl exports → one training dataset for Unsloth Studio.
# Why: dumpboth keeps each agent's raw format; trainers need {"messages": [...]} rows.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "lib"))            # lib/ holds one function per file
from discover import discover
from convert import convert


def main():
    parser = argparse.ArgumentParser(description="Convert dumpboth .jsonl exports to a messages dataset.")
    parser.add_argument("exports", nargs="+", type=Path, help="dumpboth .jsonl files (Claude, Cursor, Devin)")
    parser.add_argument("-o", "--output", type=Path, required=True, help="dataset .jsonl to write")
    args = parser.parse_args()
    adapters = discover()                                          # every file in lib/adapters/
    rows = []
    for path in args.exports:
        row = convert(path, adapters) if path.is_file() else None
        if row:
            rows.append(row)
        else:                                                      # report, never silently drop
            print(f"skipped: {path} (missing or no user/assistant exchange)", file=sys.stderr)
    args.output.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    shown = str(args.output).replace(str(Path.home()), "~", 1)     # ~ keeps home folder name out of shared screenshots
    print(f"wrote {len(rows)} conversation(s) → {shown}", file=sys.stderr)
    return 0 if rows else 1                                        # non-zero when dataset is empty


if __name__ == "__main__":
    raise SystemExit(main())
