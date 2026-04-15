#!/usr/bin/env python3
"""Validate wordlist files for duplicates, empty lines, and Unicode NFC normalization."""
from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: read error ({exc})"]

    lines = text.splitlines()
    seen: set[str] = set()
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            errors.append(f"{path}:{idx}: empty/blank line")
            continue
        nfc = unicodedata.normalize("NFC", line)
        if nfc != line:
            errors.append(f"{path}:{idx}: not NFC-normalized")
        if line in seen:
            errors.append(f"{path}:{idx}: duplicate entry '{line}'")
        seen.add(line)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default="online/wordlist", help="wordlist root path")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 2

    files = sorted(
        p for p in root.rglob("*.txt")
        if p.is_file() and not p.name.startswith("TODO_")
    )
    all_errors: list[str] = []
    for file in files:
        all_errors.extend(validate_file(file))

    if all_errors:
        print("Wordlist validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print(f"OK: {len(files)} files validated under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
