#!/usr/bin/env python3
"""Detect likely near-duplicate wordlist entries using accent/punctuation folding."""
from __future__ import annotations

import argparse
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


SKIP_FILENAMES = {"NEAR_DUPLICATES_ALLOWLIST.txt"}


def load_allowlist(path: Path) -> set[tuple[str, str]]:
    if not path.exists():
        return set()
    entries: set[tuple[str, str]] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        relpath, sep, key = stripped.partition("|")
        if not sep or not relpath or not key:
            raise ValueError(f"invalid allowlist entry: {stripped!r}")
        entries.add((relpath, key))
    return entries


def fold_token(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    no_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    cleaned = "".join(ch for ch in no_marks.lower() if ch.isalnum())
    return cleaned


def scan_file(path: Path, root: Path, allowlist: set[tuple[str, str]]) -> tuple[list[str], int]:
    groups: dict[str, set[str]] = defaultdict(set)
    for raw in path.read_text(encoding="utf-8").splitlines():
        token = raw.strip()
        if not token:
            continue
        groups[fold_token(token)].add(token)

    warnings: list[str] = []
    ignored = 0
    relpath = path.relative_to(root).as_posix()
    for key, variants in groups.items():
        if len(variants) > 1 and key:
            if (relpath, key) in allowlist:
                ignored += 1
                continue
            sample = ", ".join(sorted(variants))
            warnings.append(f"{path}: near-duplicate variants for key '{key}': {sample}")
    return warnings, ignored


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default="online/wordlist")
    parser.add_argument("--strict", action="store_true", help="return non-zero when near-duplicates are found")
    parser.add_argument(
        "--allowlist",
        default="online/wordlist/NEAR_DUPLICATES_ALLOWLIST.txt",
        help="optional file with '<relative-path>|<folded-key>' entries to suppress known pairs",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 2
    allowlist_path = Path(args.allowlist)
    try:
        allowlist = load_allowlist(allowlist_path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    warnings: list[str] = []
    ignored = 0
    for file in sorted(
        p
        for p in root.rglob("*.txt")
        if p.is_file() and not p.name.startswith("TODO_") and p.name not in SKIP_FILENAMES
    ):
        file_warnings, file_ignored = scan_file(file, root, allowlist)
        warnings.extend(file_warnings)
        ignored += file_ignored

    if warnings:
        print(f"Near-duplicate candidates found: {len(warnings)} (ignored by allowlist: {ignored})")
        for item in warnings[:200]:
            print(f"- {item}")
        if len(warnings) > 200:
            print(f"... truncated {len(warnings) - 200} additional entries")
        return 1 if args.strict else 0

    print(f"OK: no unsuppressed near-duplicate variants detected under {root} (ignored by allowlist: {ignored})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
