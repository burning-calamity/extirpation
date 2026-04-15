"""Dynamic module loader for Python files inside an `online` folder."""

from __future__ import annotations

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from importlib import util
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, Iterable, List
import inspect


@dataclass(frozen=True)
class ModuleLoadError:
    """Represents a module that could not be imported."""

    module_name: str
    file_path: Path
    error: str


@dataclass(frozen=True)
class LoadReport:
    """Summary of a module loading run."""

    modules: Dict[str, ModuleType]
    errors: List[ModuleLoadError]


ModuleFilter = Callable[[str, Path], bool]
_REPORT_CACHE: dict[tuple[str, bool, str], tuple[tuple[tuple[str, int, int], ...], LoadReport]] = {}
_LIST_CACHE: dict[tuple[str, bool], tuple[tuple[tuple[str, int, int], ...], list[str]]] = {}


def _pick_alias_function_name(module: ModuleType, mode: str) -> str | None:
    suffix = f"_{mode}"
    candidates = sorted(
        name
        for name, obj in vars(module).items()
        if callable(obj) and not name.startswith("_") and mode in name and inspect.isfunction(obj)
    )
    if not candidates:
        return None
    for name in candidates:
        if name.endswith(suffix):
            return name
    return candidates[0]


def _attach_standard_encrypt_decrypt_aliases(module: ModuleType) -> None:
    """Attach ``encrypt`` / ``decrypt`` aliases when a module exposes mode-specific names."""
    if not hasattr(module, "encrypt"):
        encrypt_name = _pick_alias_function_name(module, "encrypt")
        if encrypt_name is not None:
            setattr(module, "encrypt", getattr(module, encrypt_name))
    if not hasattr(module, "decrypt"):
        decrypt_name = _pick_alias_function_name(module, "decrypt")
        if decrypt_name is not None:
            setattr(module, "decrypt", getattr(module, decrypt_name))


def _iter_module_files(online_dir: Path, recursive: bool = False) -> Iterable[Path]:
    """Yield importable Python module files from a directory."""
    if not online_dir.exists() or not online_dir.is_dir():
        return []

    iterator = online_dir.rglob("*.py") if recursive else online_dir.glob("*.py")
    return sorted(path for path in iterator if path.is_file() and not path.name.startswith("_"))


def _name_from_path(base: Path, module_file: Path, recursive: bool) -> str:
    return ".".join(module_file.relative_to(base).with_suffix("").parts) if recursive else module_file.stem


def list_online_modules(
    online_dir: str | Path = "online",
    recursive: bool = False,
    module_filter: ModuleFilter | None = None,
) -> List[str]:
    """List available module names without importing them."""
    base = Path(online_dir).expanduser().resolve()
    names: list[str] = []
    for module_file in _iter_module_files(base, recursive=recursive):
        module_name = _name_from_path(base, module_file, recursive)
        if module_filter and not module_filter(module_name, module_file):
            continue
        names.append(module_name)
    return names


def list_online_modules_cached(
    online_dir: str | Path = "online",
    recursive: bool = False,
    module_filter: ModuleFilter | None = None,
) -> List[str]:
    """List available module names with lightweight in-memory caching."""
    if module_filter is not None:
        return list_online_modules(online_dir, recursive=recursive, module_filter=module_filter)

    base = Path(online_dir).expanduser().resolve()
    module_files = list(_iter_module_files(base, recursive=recursive))
    fingerprint = _files_fingerprint(module_files)
    key = (str(base), recursive)
    cached = _LIST_CACHE.get(key)
    if cached and cached[0] == fingerprint:
        return list(cached[1])

    names = [_name_from_path(base, p, recursive) for p in module_files]
    _LIST_CACHE[key] = (fingerprint, list(names))
    return names


def load_online_modules(
    online_dir: str | Path = "online",
    *,
    recursive: bool = False,
    strict: bool = False,
    module_filter: ModuleFilter | None = None,
    namespace: str = "online_dynamic",
    workers: int = 1,
) -> Dict[str, ModuleType]:
    """Load every public `.py` module from the provided `online` folder."""
    report = load_online_modules_with_report(
        online_dir=online_dir,
        recursive=recursive,
        strict=strict,
        module_filter=module_filter,
        namespace=namespace,
        workers=workers,
    )
    return report.modules


def clear_online_loader_cache() -> None:
    """Clear in-memory cached load reports."""
    _REPORT_CACHE.clear()
    _LIST_CACHE.clear()


def _files_fingerprint(module_files: list[Path]) -> tuple[tuple[str, int, int], ...]:
    fp: list[tuple[str, int, int]] = []
    for path in module_files:
        stat = path.stat()
        fp.append((str(path), int(stat.st_mtime_ns), stat.st_size))
    return tuple(fp)


def load_online_modules_with_report_cached(
    online_dir: str | Path = "online",
    *,
    recursive: bool = False,
    strict: bool = False,
    module_filter: ModuleFilter | None = None,
    namespace: str = "online_dynamic",
    workers: int = 1,
) -> LoadReport:
    """Load modules using an in-memory cache keyed by directory/fingerprint."""
    if strict:
        return load_online_modules_with_report(
            online_dir=online_dir,
            recursive=recursive,
            strict=strict,
            module_filter=module_filter,
            namespace=namespace,
            workers=workers,
        )

    base = Path(online_dir).expanduser().resolve()
    module_files = list(_iter_module_files(base, recursive=recursive))
    if module_filter:
        module_files = [p for p in module_files if module_filter(_name_from_path(base, p, recursive), p)]

    key = (str(base), recursive, namespace)
    fingerprint = _files_fingerprint(module_files)
    cached = _REPORT_CACHE.get(key)
    if cached and cached[0] == fingerprint:
        return cached[1]

    report = load_online_modules_with_report(
        online_dir=online_dir,
        recursive=recursive,
        strict=False,
        module_filter=module_filter,
        namespace=namespace,
        workers=workers,
    )
    _REPORT_CACHE[key] = (fingerprint, report)
    return report


def load_online_modules_with_report(
    online_dir: str | Path = "online",
    *,
    recursive: bool = False,
    strict: bool = False,
    module_filter: ModuleFilter | None = None,
    namespace: str = "online_dynamic",
    workers: int = 1,
) -> LoadReport:
    """Load modules and return both successful imports and import errors."""
    base = Path(online_dir).expanduser().resolve()
    modules: Dict[str, ModuleType] = {}
    errors: List[ModuleLoadError] = []

    candidates: list[tuple[str, Path]] = []
    for module_file in _iter_module_files(base, recursive=recursive):
        module_name = _name_from_path(base, module_file, recursive)
        if module_filter and not module_filter(module_name, module_file):
            continue
        candidates.append((module_name, module_file))

    def _load_candidate(item: tuple[str, Path]) -> tuple[str, ModuleType | None, ModuleLoadError | None]:
        module_name, module_file = item
        import_name = f"{namespace}.{module_name}"
        spec = util.spec_from_file_location(import_name, module_file)
        if spec is None or spec.loader is None:
            return module_name, None, ModuleLoadError(module_name, module_file, "unable to create import spec")
        try:
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _attach_standard_encrypt_decrypt_aliases(module)
            return module_name, module, None
        except Exception as exc:  # noqa: BLE001 - preserve plugin import errors
            return module_name, None, ModuleLoadError(module_name, module_file, str(exc))

    if workers <= 1:
        results = map(_load_candidate, candidates)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(_load_candidate, candidates)

    for module_name, module, err in results:
        if err is not None:
            if strict:
                raise ImportError(f"Failed to load '{module_name}' from {err.file_path}: {err.error}")
            errors.append(err)
            continue
        assert module is not None
        modules[module_name] = module

    return LoadReport(modules=modules, errors=errors)


def describe_loaded_modules(modules: Dict[str, ModuleType]) -> Dict[str, dict[str, list[str]]]:
    """Return a simple capability catalog for loaded modules."""
    catalog: Dict[str, dict[str, list[str]]] = {}
    for name, module in modules.items():
        funcs = {
            fname
            for fname, obj in vars(module).items()
            if callable(obj) and not fname.startswith("_") and inspect.isfunction(obj)
        }
        entries = {
            "encrypt": sorted(f for f in funcs if "encrypt" in f),
            "decrypt": sorted(f for f in funcs if "decrypt" in f),
            "other": sorted(f for f in funcs if "encrypt" not in f and "decrypt" not in f),
        }
        signatures = {
            fname: str(inspect.signature(getattr(module, fname)))
            for group in entries.values()
            for fname in group
        }
        catalog[name] = {
            **entries,
            "signatures": signatures,
            "module_doc": (module.__doc__ or "").strip(),
        }
    return catalog


def invoke_module_function(modules: Dict[str, ModuleType], module_name: str, function_name: str, **kwargs: object) -> object:
    """Invoke a function from a loaded module by name."""
    if module_name not in modules:
        raise KeyError(f"module not loaded: {module_name}")
    module = modules[module_name]
    fn = getattr(module, function_name, None)
    if fn is None or not callable(fn):
        raise AttributeError(f"function not found: {module_name}.{function_name}")
    return fn(**kwargs)


def module_catalog_stats(catalog: Dict[str, dict[str, list[str]]]) -> dict[str, int]:
    """Compute simple stats for a module capability catalog."""
    return {
        "modules": len(catalog),
        "encrypt_functions": sum(len(v.get("encrypt", [])) for v in catalog.values()),
        "decrypt_functions": sum(len(v.get("decrypt", [])) for v in catalog.values()),
        "other_functions": sum(len(v.get("other", [])) for v in catalog.values()),
    }


def search_catalog(catalog: Dict[str, dict[str, list[str]]], query: str) -> Dict[str, dict[str, list[str]]]:
    """Filter catalog entries by module/function name substring."""
    needle = query.strip().lower()
    if not needle:
        return dict(catalog)

    matched: Dict[str, dict[str, list[str]]] = {}
    for module_name, meta in catalog.items():
        module_hit = needle in module_name.lower()
        function_hit = any(
            needle in fn.lower()
            for group in ("encrypt", "decrypt", "other")
            for fn in meta.get(group, [])
        )
        if module_hit or function_hit:
            matched[module_name] = meta
    return matched


def validate_module_contracts(catalog: Dict[str, dict[str, list[str]]]) -> Dict[str, list[str]]:
    """Validate that modules expose at least one encrypt/decrypt function."""
    issues: Dict[str, list[str]] = {}
    for name, meta in catalog.items():
        problems: list[str] = []
        if not meta.get("encrypt"):
            problems.append("missing encrypt function")
        if not meta.get("decrypt"):
            problems.append("missing decrypt function")
        if problems:
            issues[name] = problems
    return issues
