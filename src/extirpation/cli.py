"""Command-line utilities for extirpation."""

from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path
import re
import time

from . import __version__
from .online_loader import (
    clear_online_loader_cache,
    describe_loaded_modules,
    invoke_module_function,
    list_online_modules,
    list_online_modules_cached,
    load_online_modules_with_report,
    load_online_modules_with_report_cached,
    module_catalog_stats,
    search_catalog,
    validate_module_contracts,
)
from .setup import setup as setup_online
from .key_autoguesser import autoguess_keys

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
    parser.add_argument("--workers", type=int, default=1, help="Number of worker threads for module imports")
    parser.add_argument("--cache", action="store_true", help="Use in-memory load cache for faster repeated commands")

    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="List discoverable module names")
    list_parser.add_argument("--json", action="store_true", help="Output module list as JSON array")

    report_parser = subparsers.add_parser("report", help="Load modules and print JSON report")
    report_parser.add_argument("--strict", action="store_true", help="Fail fast on first import error")

    subparsers.add_parser("catalog", help="Show discovered encryption/decryption function catalog")
    inspect_parser = subparsers.add_parser("inspect", help="Show details for a single module")
    inspect_parser.add_argument("--module", required=True, help="Module name to inspect")
    find_parser = subparsers.add_parser("find", help="Search catalog by module/function substring")
    find_parser.add_argument("--query", required=True, help="Substring to match in modules/functions")
    subparsers.add_parser("stats", help="Show aggregate catalog statistics")
    subparsers.add_parser("validate", help="Validate module contracts (encrypt/decrypt presence)")
    doctor_parser = subparsers.add_parser("doctor", help="Show health summary with load errors and contract issues")
    doctor_parser.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero if errors/issues are found")
    subparsers.add_parser("clear-cache", help="Clear in-memory loader cache")

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
    batch_parser = subparsers.add_parser("invoke-batch", help="Invoke multiple module functions from JSON")
    batch_parser.add_argument(
        "--calls",
        required=True,
        help='JSON array: [{"module":"...","function":"...","kwargs":{...}}, ...]',
    )
    batch_parser.add_argument("--stop-on-error", action="store_true", help="Stop immediately on first call error")
    transform_parser = subparsers.add_parser("transform", help="Run module encrypt/decrypt using auto-selected function")
    transform_parser.add_argument("--module", required=True, help="Module name")
    transform_parser.add_argument("--mode", choices=["encrypt", "decrypt"], required=True)
    transform_parser.add_argument("--text", required=True, help="Input text")
    transform_parser.add_argument("--params", default="{}", help="Extra JSON kwargs for the selected function")
    autoguess_parser = subparsers.add_parser("autoguess-key", help="Attempt key autoguessing for supported ciphers")
    autoguess_parser.add_argument("--cipher", required=True, help="Cipher name, e.g. caesar")
    autoguess_parser.add_argument("--ciphertext", required=True, help="Ciphertext to analyze")
    autoguess_parser.add_argument("--top", type=int, default=5, help="Number of top guesses to return")
    autoguess_parser.add_argument("--wordlist-dir", default=None, help="Optional override for wordlist directory")

    scaffold_parser = subparsers.add_parser("scaffold", help="Create a new module template in online-dir")
    scaffold_parser.add_argument("name", help="New module name, e.g. my_cipher")
    scaffold_parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    setup_parser = subparsers.add_parser("setup", help="Populate online-dir with bundled modules")
    setup_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing module files")
    setup_parser.add_argument("--no-load", action="store_true", help="Skip loading after provisioning")

    subparsers.add_parser("version", help="Print the installed extirpation version")
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark module load performance")
    benchmark_parser.add_argument("--iterations", type=int, default=3, help="Number of benchmark iterations")

    return parser


def _load_report(online_dir: str, recursive: bool, strict: bool = False, workers: int = 1) -> dict[str, object]:
    report = load_online_modules_with_report(online_dir, recursive=recursive, strict=strict, workers=workers)
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


def _load_modules_report(args: argparse.Namespace, strict: bool = False):
    if args.cache and not strict:
        return load_online_modules_with_report_cached(
            args.online_dir,
            recursive=args.recursive,
            strict=False,
            workers=args.workers,
        )
    return load_online_modules_with_report(
        args.online_dir,
        recursive=args.recursive,
        strict=strict,
        workers=args.workers,
    )


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


def _pick_transform_function(module: object, mode: str) -> str:
    suffix = f"_{mode}"
    candidates = sorted(
        name
        for name, fn in vars(module).items()
        if callable(fn) and not name.startswith("_") and mode in name and inspect.isfunction(fn)
    )
    if not candidates:
        raise AttributeError(f"no '{mode}' function found")
    for name in candidates:
        if name.endswith(suffix):
            return name
    return candidates[0]


def _inject_text_argument(fn: object, text: str, kwargs: dict[str, object]) -> dict[str, object]:
    sig = inspect.signature(fn)
    for preferred in ("plaintext", "ciphertext", "text", "input_text"):
        if preferred in sig.parameters and preferred not in kwargs:
            return {**kwargs, preferred: text}
    for name, param in sig.parameters.items():
        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY) and name not in kwargs:
            return {**kwargs, name: text}
    return kwargs

def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "list":
        names = (
            list_online_modules_cached(args.online_dir, recursive=args.recursive)
            if args.cache
            else list_online_modules(args.online_dir, recursive=args.recursive)
        )
        if args.json:
            print(json.dumps(names, indent=2))
        else:
            print("\n".join(names))
        return 0

    if args.command == "report":
        print(
            json.dumps(
                _load_report(args.online_dir, recursive=args.recursive, strict=args.strict, workers=args.workers),
                indent=2,
            )
        )
        return 0

    if args.command == "catalog":
        report = _load_modules_report(args)
        print(json.dumps(describe_loaded_modules(report.modules), indent=2))
        return 0

    if args.command == "find":
        report = _load_modules_report(args)
        catalog = describe_loaded_modules(report.modules)
        print(json.dumps(search_catalog(catalog, args.query), indent=2))
        return 0

    if args.command == "inspect":
        report = _load_modules_report(args)
        catalog = describe_loaded_modules(report.modules)
        module_meta = catalog.get(args.module)
        if module_meta is None:
            raise KeyError(f"module not found: {args.module}")
        print(json.dumps(module_meta, indent=2))
        return 0

    if args.command == "stats":
        report = _load_modules_report(args)
        catalog = describe_loaded_modules(report.modules)
        print(json.dumps(module_catalog_stats(catalog), indent=2))
        return 0

    if args.command == "validate":
        report = _load_modules_report(args)
        catalog = describe_loaded_modules(report.modules)
        print(json.dumps(validate_module_contracts(catalog), indent=2))
        return 0

    if args.command == "doctor":
        report = _load_modules_report(args)
        catalog = describe_loaded_modules(report.modules)
        issues = validate_module_contracts(catalog)
        payload = {
            "module_count": len(report.modules),
            "load_error_count": len(report.errors),
            "contract_issue_count": len(issues),
            "issues": issues,
        }
        print(json.dumps(payload, indent=2))
        if args.fail_on_issues and (report.errors or issues):
            return 1
        return 0

    if args.command == "clear-cache":
        clear_online_loader_cache()
        print("cache cleared")
        return 0

    if args.command == "export-catalog":
        report = _load_modules_report(args)
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
        report = _load_modules_report(args)
        try:
            kwargs = json.loads(args.kwargs)
        except json.JSONDecodeError as exc:
            parser.error(f"--kwargs must be valid JSON: {exc.msg}")
        if not isinstance(kwargs, dict):
            parser.error("--kwargs must decode to a JSON object")
        result = invoke_module_function(report.modules, args.module, args.function, **kwargs)
        print(result)
        return 0

    if args.command == "invoke-batch":
        report = _load_modules_report(args)
        try:
            calls = json.loads(args.calls)
        except json.JSONDecodeError as exc:
            parser.error(f"--calls must be valid JSON: {exc.msg}")
        if not isinstance(calls, list):
            parser.error("--calls must decode to a JSON array")

        results: list[object] = []
        for item in calls:
            if not isinstance(item, dict):
                parser.error("each call item must be a JSON object")
            module_name = item.get("module")
            function_name = item.get("function")
            kwargs = item.get("kwargs", {})
            if not isinstance(module_name, str) or not isinstance(function_name, str):
                parser.error("each call requires string 'module' and 'function'")
            if not isinstance(kwargs, dict):
                parser.error("each call 'kwargs' must be a JSON object")
            try:
                result = invoke_module_function(report.modules, module_name, function_name, **kwargs)
                results.append({"ok": True, "result": result})
            except Exception as exc:  # noqa: BLE001
                payload = {"ok": False, "error": str(exc), "module": module_name, "function": function_name}
                results.append(payload)
                if args.stop_on_error:
                    print(json.dumps(results, indent=2))
                    return 1
        print(json.dumps(results, indent=2))
        return 0

    if args.command == "transform":
        report = _load_modules_report(args)
        module = report.modules.get(args.module)
        if module is None:
            raise KeyError(f"module not found: {args.module}")
        fn_name = _pick_transform_function(module, args.mode)
        fn = getattr(module, fn_name)
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as exc:
            parser.error(f"--params must be valid JSON: {exc.msg}")
        if not isinstance(params, dict):
            parser.error("--params must decode to a JSON object")
        kwargs = _inject_text_argument(fn, args.text, params)
        result = fn(**kwargs)
        print(result)
        return 0

    if args.command == "autoguess-key":
        guesses = autoguess_keys(
            cipher=args.cipher,
            ciphertext=args.ciphertext,
            wordlist_dir=args.wordlist_dir,
            top_n=args.top,
        )
        print(
            json.dumps(
                [
                    {
                        "cipher": g.cipher,
                        "key": g.key,
                        "score": g.score,
                        "best_language": g.best_language,
                        "matched_tokens": g.matched_tokens,
                        "total_tokens": g.total_tokens,
                        "plaintext": g.plaintext,
                    }
                    for g in guesses
                ],
                indent=2,
                ensure_ascii=False,
            )
        )
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

    if args.command == "setup":
        result = setup_online(
            online_dir=args.online_dir,
            overwrite=args.overwrite,
            load=not args.no_load,
            recursive=args.recursive,
            workers=args.workers,
        )
        payload = {
            "target_dir": str(result.target_dir),
            "copied": [str(p) for p in result.copied],
            "skipped": [str(p) for p in result.skipped],
            "loaded_modules": len(result.report.modules) if result.report else None,
            "load_errors": len(result.report.errors) if result.report else None,
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.command == "version":
        print(__version__)
        return 0

    if args.command == "benchmark":
        if args.iterations <= 0:
            parser.error("--iterations must be positive")
        timings: list[float] = []
        clear_online_loader_cache()
        for _ in range(args.iterations):
            start = time.perf_counter()
            _load_modules_report(args)
            timings.append((time.perf_counter() - start) * 1000.0)
        result = {
            "iterations": args.iterations,
            "min_ms": min(timings),
            "max_ms": max(timings),
            "avg_ms": sum(timings) / len(timings),
            "cache_enabled": bool(args.cache),
            "workers": args.workers,
        }
        print(json.dumps(result, indent=2))
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
