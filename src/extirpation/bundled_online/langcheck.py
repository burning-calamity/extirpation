"""Language checker backed by wordlists in ``online/wordlist``."""

from __future__ import annotations

import json
from pathlib import Path

SKIP_FILENAMES = {"FREQUENCY_NOTES.txt", "NEAR_DUPLICATES_ALLOWLIST.txt"}


def _default_wordlist_dir() -> Path:
    local = Path(__file__).resolve().parent / 'wordlist'
    if local.is_dir():
        return local

    for parent in Path(__file__).resolve().parents:
        candidate = parent / 'online' / 'wordlist'
        if candidate.is_dir():
            return candidate

    raise FileNotFoundError('wordlist directory not found')


def _normalize(value: str) -> str:
    return value.strip().lower()


def _infer_language(file_path: Path, root: Path) -> str | None:
    if file_path.name.startswith("TODO_") or file_path.name in SKIP_FILENAMES:
        return None
    if file_path.parent == root:
        return None
    if file_path.parent.parent == root:
        return file_path.stem
    for parent in file_path.parents:
        if parent == root:
            break
        if parent.parent.parent == root:
            return parent.name
    return file_path.stem


def langcheck_check(text: str, wordlist_dir: str | Path | None = None) -> tuple[bool, str | None]:
    """Return ``(found, language)`` for a given word."""
    needle = _normalize(text)
    if not needle:
        return False, None

    root = Path(wordlist_dir).resolve() if wordlist_dir else _default_wordlist_dir()
    for file_path in sorted(root.rglob('*.txt')):
        language = _infer_language(file_path, root)
        if not language:
            continue
        words = {_normalize(line) for line in file_path.read_text(encoding='utf-8').splitlines() if line.strip()}
        if needle in words:
            return True, language
    return False, None


def langcheck_encrypt(plaintext: str, wordlist_dir: str | Path | None = None) -> str:
    """Serialize the langcheck result as JSON."""
    found, language = langcheck_check(plaintext, wordlist_dir=wordlist_dir)
    return json.dumps({'found': found, 'language': language}, ensure_ascii=False)


def langcheck_decrypt(ciphertext: str) -> tuple[bool, str | None]:
    """Parse JSON produced by ``langcheck_encrypt``."""
    payload = json.loads(ciphertext)
    return bool(payload.get('found')), payload.get('language')
