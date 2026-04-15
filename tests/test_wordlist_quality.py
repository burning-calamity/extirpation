from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORDLIST = ROOT / "online" / "wordlist"
VALIDATOR = ROOT / "tools" / "wordlist_validate.py"
NEAR_DUPES = ROOT / "tools" / "wordlist_near_duplicates.py"
NEAR_DUPES_ALLOWLIST = WORDLIST / "NEAR_DUPLICATES_ALLOWLIST.txt"


def test_wordlist_validator_passes() -> None:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(WORDLIST)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_frequency_seed_files_exist() -> None:
    expected = [
        WORDLIST / "latin" / "english" / "frequency_top_100.txt",
        WORDLIST / "latin" / "spanish" / "frequency_top_100.txt",
        WORDLIST / "latin" / "french" / "frequency_top_100.txt",
        WORDLIST / "latin" / "german" / "frequency_top_100.txt",
        WORDLIST / "latin" / "italian" / "frequency_top_100.txt",
        WORDLIST / "latin" / "portuguese" / "frequency_top_100.txt",
        WORDLIST / "latin" / "dutch" / "frequency_top_100.txt",
    ]
    for path in expected:
        assert path.exists(), f"missing {path}"
        lines = [x for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        assert len(lines) == 100


def test_thematic_seed_files_exist() -> None:
    thematic_files = [
        WORDLIST / "latin" / "english" / "themes" / "technology.txt",
        WORDLIST / "latin" / "spanish" / "themes" / "geography.txt",
        WORDLIST / "latin" / "french" / "themes" / "daily_life.txt",
        WORDLIST / "latin" / "german" / "themes" / "technology.txt",
        WORDLIST / "latin" / "italian" / "themes" / "geography.txt",
        WORDLIST / "latin" / "portuguese" / "themes" / "daily_life.txt",
        WORDLIST / "latin" / "dutch" / "themes" / "technology.txt",
    ]
    for path in thematic_files:
        assert path.exists(), f"missing {path}"
        lines = [x for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        assert len(lines) >= 10


def test_near_duplicate_scan_runs() -> None:
    proc = subprocess.run(
        [sys.executable, str(NEAR_DUPES), str(WORDLIST), "--strict", "--allowlist", str(NEAR_DUPES_ALLOWLIST)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_near_duplicate_scan_skips_allowlist_file(tmp_path: Path) -> None:
    root = tmp_path / "wordlist"
    root.mkdir()
    (root / "NEAR_DUPLICATES_ALLOWLIST.txt").write_text("x.txt|dup\nx.txt|dup\n", encoding="utf-8")
    data = root / "sample.txt"
    data.write_text("café\ncafe\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(NEAR_DUPES), str(root), "--strict", "--allowlist", str(root / "NEAR_DUPLICATES_ALLOWLIST.txt")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "sample.txt" in proc.stdout


def test_near_duplicate_scan_rejects_invalid_allowlist(tmp_path: Path) -> None:
    root = tmp_path / "wordlist"
    root.mkdir()
    (root / "sample.txt").write_text("alpha\nbeta\n", encoding="utf-8")
    allowlist = root / "bad_allowlist.txt"
    allowlist.write_text("not-valid\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(NEAR_DUPES), str(root), "--allowlist", str(allowlist)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "invalid allowlist entry" in proc.stderr
