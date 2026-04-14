"""Command-line utilities for extirpation."""

from __future__ import annotations

import argparse
import json

from . import __version__
from .online_loader import list_online_modules, load_online_modules_with_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="extirpation", description="Load and inspect online modules")
    parser.add_argument("--online-dir", default="online", help="Directory containing modules")
    parser.add_argument("--recursive", action="store_true", help="Discover modules recursively")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List discoverable module names")

    report_parser = subparsers.add_parser("report", help="Load modules and print JSON report")
    report_parser.add_argument("--strict", action="store_true", help="Fail fast on first import error")

    subparsers.add_parser("version", help="Print the installed extirpation version")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "list":
        names = list_online_modules(args.online_dir, recursive=args.recursive)
        print("\n".join(names))
        return 0

    if args.command == "report":
        report = load_online_modules_with_report(
            args.online_dir,
            recursive=args.recursive,
            strict=args.strict,
        )
        payload = {
            "module_count": len(report.modules),
            "modules": sorted(report.modules.keys()),
            "errors": [
                {
                    "module": err.module_name,
                    "file": str(err.file_path),
                    "error": err.error,
                }
                for err in report.errors
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.command == "version":
        print(__version__)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
