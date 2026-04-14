"""Command-line utilities for extirpation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from . import __version__
from .online_loader import (
    describe_loaded_modules,
    invoke_module_function,
    list_online_modules,
    load_online_modules_with_report,
    module_catalog_stats,
    search_catalog,
    validate_module_contracts,
)

TEMPLATE = '''"""{title} module."""

from __future__ import annotations


def {name}_encrypt(plaintext: str) -> str:
    """TODO: implement encryption."""
    return plaintext


def {name}_decrypt(ciphertext: str) -> str:
    """TODO: implement decryption."""
    return ciphertext
'''


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="extirpation", description="Load and inspect online modules")
    parser.add_argument("--online-dir", default="online", help="Directory containing modules")
    parser.add_argument("--recursive", action="store_true", help="Discover modules recursively")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List discoverable module names")

    report_parser = subparsers.add_parser("report", help="Load modules and print JSON report")
    report_parser.add_argument("--strict", action="store_true", help="Fail fast on first import error")

    subparsers.add_parser("catalog", help="Show discovered encryption/decryption function catalog")
    find_parser = subparsers.add_parser("find", help="Search catalog by module/function substring")
    find_parser.add_argument("--query", required=True, help="Substring to match in modules/functions")
    subparsers.add_parser("stats", help="Show aggregate catalog statistics")
    subparsers.add_parser("validate", help="Validate module contracts (encrypt/decrypt presence)")

    export_parser = subparsers.add_parser("export-catalog", help="Export module catalog to JSON or Markdown")
    export_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    export_parser.add_argument("--output", required=True, help="Output file path")

    invoke_parser = subparsers.add_parser("invoke", help="Invoke a module function with JSON kwargs")
    invoke_parser.add_argument("--module", required=True, help="Module name (e.g. caesar)")
    invoke_parser.add_argument("--function", required=True, help="Function name (e.g. caesar_encrypt)")
    invoke_parser.add_argument(
        "--kwargs",
        default="{}",
        help='JSON object of keyword args, e.g. {"plaintext":"HELLO","shift":3}',
    )

    scaffold_parser = subparsers.add_parser("scaffold", help="Create a new module template in online-dir")
    scaffold_parser.add_argument("name", help="New module name, e.g. my_cipher")
    scaffold_parser.add_argument("--force", action="store_true", help="Overwrite existing file")

    subparsers.add_parser("version", help="Print the installed extirpation version")

    return parser


def _load_report(online_dir: str, recursive: bool, strict: bool = False) -> dict[str, object]:
    report = load_online_modules_with_report(online_dir, recursive=recursive, strict=strict)
    return {
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


def _catalog_to_markdown(catalog: dict[str, dict[str, object]]) -> str:
    lines = ["# extirpation module catalog", ""]
    for module in sorted(catalog):
        meta = catalog[module]
        lines.append(f"## {module}")
        lines.append(f"- encrypt: {', '.join(meta.get('encrypt', [])) or '-'}")
        lines.append(f"- decrypt: {', '.join(meta.get('decrypt', [])) or '-'}")
        lines.append(f"- other: {', '.join(meta.get('other', [])) or '-'}")
        lines.append("")
    return "\n".join(lines)

def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "list":
        names = list_online_modules(args.online_dir, recursive=args.recursive)
        print("\n".join(names))
        return 0

    if args.command == "report":
        print(json.dumps(_load_report(args.online_dir, recursive=args.recursive, strict=args.strict), indent=2))
        return 0

    if args.command == "catalog":
        report = load_online_modules_with_report(args.online_dir, recursive=args.recursive)
        print(json.dumps(describe_loaded_modules(report.modules), indent=2))
        return 0

    if args.command == "find":
        report = load_online_modules_with_report(args.online_dir, recursive=args.recursive)
        catalog = describe_loaded_modules(report.modules)
        print(json.dumps(search_catalog(catalog, args.query), indent=2))
        return 0

    if args.command == "stats":
        report = load_online_modules_with_report(args.online_dir, recursive=args.recursive)
        catalog = describe_loaded_modules(report.modules)
        print(json.dumps(module_catalog_stats(catalog), indent=2))
        return 0

    if args.command == "validate":
        report = load_online_modules_with_report(args.online_dir, recursive=args.recursive)
        catalog = describe_loaded_modules(report.modules)
        print(json.dumps(validate_module_contracts(catalog), indent=2))
        return 0

    if args.command == "export-catalog":
        report = load_online_modules_with_report(args.online_dir, recursive=args.recursive)
        catalog = describe_loaded_modules(report.modules)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if args.format == "json":
            output_path.write_text(json.dumps(catalog, indent=2))
        else:
            output_path.write_text(_catalog_to_markdown(catalog))
        print(output_path)
        return 0

    if args.command == "invoke":
        report = load_online_modules_with_report(args.online_dir, recursive=args.recursive)
        try:
            kwargs = json.loads(args.kwargs)
        except json.JSONDecodeError as exc:
            parser.error(f"--kwargs must be valid JSON: {exc.msg}")
        if not isinstance(kwargs, dict):
            parser.error("--kwargs must decode to a JSON object")
        result = invoke_module_function(report.modules, args.module, args.function, **kwargs)
        print(result)
        return 0

    if args.command == "scaffold":
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", args.name):
            parser.error("module name must be a valid Python identifier")
        target = Path(args.online_dir) / f"{args.name}.py"
        if target.exists() and not args.force:
            raise FileExistsError(f"module file already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(TEMPLATE.format(title=args.name.replace('_', ' ').title(), name=args.name))
        print(target)
        return 0

    if args.command == "version":
        print(__version__)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
