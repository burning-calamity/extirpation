"""Two-square cipher implementation (digraph substitution)."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'


def _normalize(text: str) -> str:
    return ''.join(('I' if ch == 'J' else ch) for ch in text.upper() if ch.isalpha())


def _keyed_square(keyword: str = '') -> str:
    seen: set[str] = set()
    ordered: list[str] = []
    for ch in _normalize(keyword) + ALPHABET:
        if ch not in seen:
            seen.add(ch)
            ordered.append(ch)
    return ''.join(ordered)


def _coords(square: str, ch: str) -> tuple[int, int]:
    idx = square.index(ch)
    return divmod(idx, 5)


def _pairwise(text: str) -> list[tuple[str, str]]:
    text = _normalize(text)
    if len(text) % 2:
        text += 'X'
    return [(text[i], text[i + 1]) for i in range(0, len(text), 2)]


def two_square_encrypt(plaintext: str, key1: str = '', key2: str = '') -> str:
    """Encrypt using the two-square cipher with two keyed squares."""
    left = _keyed_square(key1)
    right = _keyed_square(key2)

    out: list[str] = []
    for a, b in _pairwise(plaintext):
        ra, ca = _coords(left, a)
        rb, cb = _coords(right, b)
        if ra == rb:
            out.extend((a, b))
        else:
            out.append(left[ra * 5 + cb])
            out.append(right[rb * 5 + ca])
    return ''.join(out)


def two_square_decrypt(ciphertext: str, key1: str = '', key2: str = '') -> str:
    """Decrypt text produced by ``two_square_encrypt``."""
    left = _keyed_square(key1)
    right = _keyed_square(key2)

    out: list[str] = []
    for a, b in _pairwise(ciphertext):
        ra, ca = _coords(left, a)
        rb, cb = _coords(right, b)
        if ra == rb:
            out.extend((a, b))
        else:
            out.append(left[ra * 5 + cb])
            out.append(right[rb * 5 + ca])
    return ''.join(out)
