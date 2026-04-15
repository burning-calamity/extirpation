"""Beginner-friendly helpers for common extirpation workflows."""

from __future__ import annotations

import inspect
from pathlib import Path
from types import ModuleType
from typing import Any

from .online_loader import load_online_modules_with_report_cached
from .setup import setup


def _pick_transform_function(module: ModuleType, mode: str) -> str:
    suffix = f"_{mode}"
    candidates = sorted(
        name
        for name, fn in vars(module).items()
        if callable(fn) and not name.startswith("_") and mode in name and inspect.isfunction(fn)
    )
    if not candidates:
        raise AttributeError(f"no '{mode}' function found for module '{module.__name__}'")
    for name in candidates:
        if name.endswith(suffix):
            return name
    return candidates[0]


def _inject_text_argument(fn: object, text: str, kwargs: dict[str, Any]) -> dict[str, Any]:
    sig = inspect.signature(fn)
    for preferred in ("plaintext", "ciphertext", "text", "input_text"):
        if preferred in sig.parameters and preferred not in kwargs:
            return {**kwargs, preferred: text}
    for name, param in sig.parameters.items():
        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY) and name not in kwargs:
            return {**kwargs, name: text}
    return kwargs


def ensure_online_modules(
    online_dir: str | Path = "online",
    *,
    recursive: bool = False,
    workers: int = 1,
) -> dict[str, ModuleType]:
    """Provision bundled modules into ``online_dir`` (if needed) and load them."""
    setup(online_dir)
    report = load_online_modules_with_report_cached(
        online_dir=online_dir,
        recursive=recursive,
        strict=False,
        workers=workers,
    )
    return report.modules


def quick_transform(
    module_name: str,
    mode: str,
    text: str,
    *,
    params: dict[str, Any] | None = None,
    online_dir: str | Path = "online",
    recursive: bool = False,
    workers: int = 1,
) -> Any:
    """Encrypt/decrypt text without manually loading modules and function names."""
    normalized_mode = mode.strip().lower()
    if normalized_mode not in {"encrypt", "decrypt"}:
        raise ValueError("mode must be 'encrypt' or 'decrypt'")

    modules = ensure_online_modules(online_dir=online_dir, recursive=recursive, workers=workers)
    module = modules.get(module_name)
    if module is None:
        raise KeyError(f"module not found: {module_name}")

    function_name = _pick_transform_function(module, normalized_mode)
    fn = getattr(module, function_name)
    kwargs = _inject_text_argument(fn, text, dict(params or {}))
    return fn(**kwargs)
