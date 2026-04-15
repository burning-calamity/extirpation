"""Columnar snake transposition cipher."""

from __future__ import annotations


def _key_order(key: str) -> list[int]:
    if not key:
        raise ValueError('key must not be empty')
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def columnar_snake_encrypt(plaintext: str, key: str, pad: str = 'X') -> str:
    """Fill rows in snake order and read columns by keyed order."""
    if len(pad) != 1:
        raise ValueError('pad must be one character')
    cols = len(key)
    rows = (len(plaintext) + cols - 1) // cols
    total = rows * cols
    text = plaintext + pad * (total - len(plaintext))

    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for r in range(rows):
        order = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        for c in order:
            grid[r][c] = text[idx]
            idx += 1

    out: list[str] = []
    for c in _key_order(key):
        for r in range(rows):
            out.append(grid[r][c])
    return ''.join(out)


def columnar_snake_decrypt(ciphertext: str, key: str, pad: str = 'X') -> str:
    """Decrypt text produced by ``columnar_snake_encrypt``."""
    if len(pad) != 1:
        raise ValueError('pad must be one character')
    cols = len(key)
    if len(ciphertext) % cols != 0:
        raise ValueError('ciphertext length must be divisible by key length')
    rows = len(ciphertext) // cols

    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for c in _key_order(key):
        for r in range(rows):
            grid[r][c] = ciphertext[idx]
            idx += 1

    out: list[str] = []
    for r in range(rows):
        order = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        for c in order:
            out.append(grid[r][c])
    return ''.join(out).rstrip(pad)
