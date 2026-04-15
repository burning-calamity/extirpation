"""Columnar transposition cipher module."""

from __future__ import annotations


def _key_order(key: str) -> list[int]:
    key = "".join(ch for ch in key.upper() if ch.isalnum())
    if not key:
        raise ValueError("key must contain at least one alphanumeric character")
    indexed = sorted(range(len(key)), key=lambda i: (key[i], i))
    return indexed


def columnar_encrypt(plaintext: str, key: str) -> str:
    order = _key_order(key)
    cols = len(order)
    rows = (len(plaintext) + cols - 1) // cols
    padded = plaintext.ljust(rows * cols)
    grid = [padded[r * cols : (r + 1) * cols] for r in range(rows)]
    return "".join("".join(grid[r][c] for r in range(rows)) for c in order)


def columnar_decrypt(ciphertext: str, key: str) -> str:
    order = _key_order(key)
    cols = len(order)
    rows = (len(ciphertext) + cols - 1) // cols
    padded = ciphertext.ljust(rows * cols)

    col_data = {}
    idx = 0
    for c in order:
        col_data[c] = list(padded[idx : idx + rows])
        idx += rows

    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(col_data[c][r])
    return "".join(out).rstrip()
