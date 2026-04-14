"""Route transposition using boustrophedon row ordering."""

from __future__ import annotations


def route_boustrophedon_encrypt(plaintext: str, columns: int = 5) -> str:
    """Write row-wise zigzag and read column-wise."""
    if columns < 1:
        raise ValueError('columns must be >= 1')

    rows = (len(plaintext) + columns - 1) // columns
    grid = [['' for _ in range(columns)] for _ in range(rows)]

    idx = 0
    for r in range(rows):
        cols = range(columns) if r % 2 == 0 else range(columns - 1, -1, -1)
        for c in cols:
            if idx < len(plaintext):
                grid[r][c] = plaintext[idx]
                idx += 1

    out: list[str] = []
    for c in range(columns):
        for r in range(rows):
            if grid[r][c]:
                out.append(grid[r][c])
    return ''.join(out)


def route_boustrophedon_decrypt(ciphertext: str, columns: int = 5) -> str:
    """Decrypt text produced by ``route_boustrophedon_encrypt``."""
    if columns < 1:
        raise ValueError('columns must be >= 1')

    rows = (len(ciphertext) + columns - 1) // columns
    short_cols = rows * columns - len(ciphertext)

    col_lens = [rows - 1 if c >= columns - short_cols and short_cols > 0 else rows for c in range(columns)]
    grid = [['' for _ in range(columns)] for _ in range(rows)]

    idx = 0
    for c in range(columns):
        for r in range(col_lens[c]):
            grid[r][c] = ciphertext[idx]
            idx += 1

    out: list[str] = []
    for r in range(rows):
        cols = range(columns) if r % 2 == 0 else range(columns - 1, -1, -1)
        for c in cols:
            if grid[r][c]:
                out.append(grid[r][c])
    return ''.join(out)
