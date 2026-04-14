"""ADFGX cipher (5x5 Polybius + optional columnar transposition)."""

from __future__ import annotations

SYMBOLS = 'ADFGX'
ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # J merged into I


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


def _columnar_encrypt(text: str, key: str) -> str:
    if not key:
        return text
    key = key.upper()
    cols = len(key)
    rows = (len(text) + cols - 1) // cols
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    order = sorted(range(cols), key=lambda i: (key[i], i))
    return ''.join(grid[r][c] for c in order for r in range(rows) if grid[r][c])


def _columnar_decrypt(text: str, key: str) -> str:
    if not key:
        return text
    key = key.upper()
    cols = len(key)
    rows = (len(text) + cols - 1) // cols
    long_cols = len(text) % cols
    if long_cols == 0:
        long_cols = cols

    order = sorted(range(cols), key=lambda i: (key[i], i))
    lengths = {c: rows if c < long_cols else rows - 1 for c in range(cols)}

    columns: dict[int, str] = {}
    idx = 0
    for c in order:
        ln = lengths[c]
        columns[c] = text[idx:idx + ln]
        idx += ln

    out: list[str] = []
    for r in range(rows):
        for c in range(cols):
            col = columns[c]
            if r < len(col):
                out.append(col[r])
    return ''.join(out)


def adfgx_encrypt(plaintext: str, square_keyword: str = '', transposition_key: str = '') -> str:
    """Encrypt alphabetic plaintext (J merged to I)."""
    square = _keyed_square(square_keyword)
    encoded: list[str] = []
    for ch in _normalize(plaintext):
        idx = square.index(ch)
        r, c = divmod(idx, 5)
        encoded.append(SYMBOLS[r])
        encoded.append(SYMBOLS[c])
    return _columnar_encrypt(''.join(encoded), transposition_key)


def adfgx_decrypt(ciphertext: str, square_keyword: str = '', transposition_key: str = '') -> str:
    """Decrypt text produced by ``adfgx_encrypt``."""
    square = _keyed_square(square_keyword)
    pairs = _columnar_decrypt(''.join(ch for ch in ciphertext.upper() if ch in SYMBOLS), transposition_key)
    out: list[str] = []
    for i in range(0, len(pairs) - 1, 2):
        r = SYMBOLS.index(pairs[i])
        c = SYMBOLS.index(pairs[i + 1])
        out.append(square[r * 5 + c])
    return ''.join(out)
