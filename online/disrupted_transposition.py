"""Disrupted transposition (columnar with row disruption)."""

from __future__ import annotations


def _key_order(key: str) -> list[int]:
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def disrupted_transposition_encrypt(plaintext: str, key: str) -> str:
    """Encrypt by reversing every other row before column readout."""
    if not key:
        raise ValueError('key must not be empty')

    cols = len(key)
    rows = (len(plaintext) + cols - 1) // cols
    grid = [['' for _ in range(cols)] for _ in range(rows)]

    idx = 0
    for r in range(rows):
        order = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        for c in order:
            if idx < len(plaintext):
                grid[r][c] = plaintext[idx]
                idx += 1

    out: list[str] = []
    for c in _key_order(key):
        for r in range(rows):
            if grid[r][c]:
                out.append(grid[r][c])
    return ''.join(out)


def disrupted_transposition_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text produced by ``disrupted_transposition_encrypt``."""
    if not key:
        raise ValueError('key must not be empty')

    cols = len(key)
    rows = (len(ciphertext) + cols - 1) // cols
    short_cols = rows * cols - len(ciphertext)

    col_lens = [rows - 1 if c >= cols - short_cols and short_cols > 0 else rows for c in range(cols)]
    grid = [['' for _ in range(cols)] for _ in range(rows)]

    idx = 0
    for c in _key_order(key):
        for r in range(col_lens[c]):
            grid[r][c] = ciphertext[idx]
            idx += 1

    out: list[str] = []
    for r in range(rows):
        order = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        for c in order:
            if grid[r][c]:
                out.append(grid[r][c])
    return ''.join(out)
