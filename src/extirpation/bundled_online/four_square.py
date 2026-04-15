"""Four-square cipher implementation."""

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


def four_square_encrypt(plaintext: str, key1: str = '', key2: str = '') -> str:
    """Encrypt with four-square using keyed top-right and bottom-left squares."""
    tl = ALPHABET
    br = ALPHABET
    tr = _keyed_square(key1)
    bl = _keyed_square(key2)

    out: list[str] = []
    for a, b in _pairwise(plaintext):
        ra, ca = _coords(tl, a)
        rb, cb = _coords(br, b)
        out.append(tr[ra * 5 + cb])
        out.append(bl[rb * 5 + ca])
    return ''.join(out)


def four_square_decrypt(ciphertext: str, key1: str = '', key2: str = '') -> str:
    """Decrypt text produced by ``four_square_encrypt``."""
    tl = ALPHABET
    br = ALPHABET
    tr = _keyed_square(key1)
    bl = _keyed_square(key2)

    out: list[str] = []
    for a, b in _pairwise(ciphertext):
        ra, ca = _coords(tr, a)
        rb, cb = _coords(bl, b)
        out.append(tl[ra * 5 + cb])
        out.append(br[rb * 5 + ca])
    return ''.join(out)
