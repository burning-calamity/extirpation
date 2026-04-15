"""Diagonal route transposition cipher."""

from __future__ import annotations


def route_diagonal_encrypt(plaintext: str, columns: int = 5, pad: str = 'X') -> str:
    """Encrypt by reading row-filled grid along diagonals."""
    if columns <= 0:
        raise ValueError('columns must be > 0')
    if len(pad) != 1:
        raise ValueError('pad must be a single character')

    rows = (len(plaintext) + columns - 1) // columns
    padded = plaintext + pad * (rows * columns - len(plaintext))
    grid = [list(padded[r * columns : (r + 1) * columns]) for r in range(rows)]

    out: list[str] = []
    for s in range(rows + columns - 1):
        for r in range(rows):
            c = s - r
            if 0 <= c < columns:
                out.append(grid[r][c])
    return ''.join(out)


def route_diagonal_decrypt(ciphertext: str, columns: int = 5, pad: str = 'X') -> str:
    """Decrypt text produced by ``route_diagonal_encrypt``."""
    if columns <= 0:
        raise ValueError('columns must be > 0')
    if len(pad) != 1:
        raise ValueError('pad must be a single character')
    if len(ciphertext) % columns != 0:
        raise ValueError('ciphertext length must be divisible by columns')

    rows = len(ciphertext) // columns
    grid = [['' for _ in range(columns)] for _ in range(rows)]

    idx = 0
    for s in range(rows + columns - 1):
        for r in range(rows):
            c = s - r
            if 0 <= c < columns:
                grid[r][c] = ciphertext[idx]
                idx += 1

    plain = ''.join(''.join(row) for row in grid)
    return plain.rstrip(pad)
