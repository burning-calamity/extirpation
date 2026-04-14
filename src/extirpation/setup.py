"""Convenience setup helpers for provisioning bundled online modules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from .online_loader import LoadReport, load_online_modules_with_report


@dataclass(frozen=True)
class SetupResult:
    target_dir: Path
    copied: list[Path]
    skipped: list[Path]
    report: LoadReport | None


def _default_bundled_online_dir() -> Path:
    # Repository layout: src/extirpation/setup.py -> ../../online
    return Path(__file__).resolve().parents[2] / "online"


def populate_online_directory(
    target_dir: str | Path = "online",
    *,
    overwrite: bool = False,
    bundled_online_dir: str | Path | None = None,
) -> tuple[Path, list[Path], list[Path]]:
    """Copy bundled `online/*.py` modules to `target_dir`."""
    source_dir = Path(bundled_online_dir).resolve() if bundled_online_dir else _default_bundled_online_dir()
    destination = Path(target_dir).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    if not source_dir.exists() or not source_dir.is_dir():
        return destination, [], []

    copied: list[Path] = []
    skipped: list[Path] = []
    for source in sorted(source_dir.glob("*.py")):
        if source.name.startswith("_") or not source.is_file():
            continue
        target = destination / source.name
        if target.exists() and not overwrite:
            skipped.append(target)
            continue
        shutil.copy2(source, target)
        copied.append(target)
    return destination, copied, skipped


def setup(
    online_dir: str | Path = "online",
    *,
    overwrite: bool = False,
    load: bool = True,
    recursive: bool = False,
    workers: int = 1,
    bundled_online_dir: str | Path | None = None,
) -> SetupResult:
    """Provision bundled modules into `online_dir` and optionally load them."""
    target_dir, copied, skipped = populate_online_directory(
        online_dir,
        overwrite=overwrite,
        bundled_online_dir=bundled_online_dir,
    )
    report = None
    if load:
        report = load_online_modules_with_report(target_dir, recursive=recursive, workers=workers)
    return SetupResult(target_dir=target_dir, copied=copied, skipped=skipped, report=report)
