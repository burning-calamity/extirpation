"""Column-route transposition with alternating column direction."""

from __future__ import annotations


def route_columns_reverse_encrypt(plaintext: str, columns: int = 5, pad: str = 'X') -> str:
    """Fill rows left-to-right; read columns alternating top-down/bottom-up."""
    if columns <= 0:
        raise ValueError('columns must be > 0')
    if len(pad) != 1:
        raise ValueError('pad must be one character')

    rows = (len(plaintext) + columns - 1) // columns
    text = plaintext + pad * (rows * columns - len(plaintext))
    grid = [list(text[r * columns : (r + 1) * columns]) for r in range(rows)]

    out: list[str] = []
    for c in range(columns):
        rng = range(rows) if c % 2 == 0 else range(rows - 1, -1, -1)
        for r in rng:
            out.append(grid[r][c])
    return ''.join(out)


def route_columns_reverse_decrypt(ciphertext: str, columns: int = 5, pad: str = 'X') -> str:
    """Decrypt text produced by ``route_columns_reverse_encrypt``."""
    if columns <= 0:
        raise ValueError('columns must be > 0')
    if len(pad) != 1:
        raise ValueError('pad must be one character')
    if len(ciphertext) % columns != 0:
        raise ValueError('ciphertext length must be divisible by columns')

    rows = len(ciphertext) // columns
    grid = [['' for _ in range(columns)] for _ in range(rows)]

    idx = 0
    for c in range(columns):
        rng = range(rows) if c % 2 == 0 else range(rows - 1, -1, -1)
        for r in rng:
            grid[r][c] = ciphertext[idx]
            idx += 1

    plain = ''.join(''.join(row) for row in grid)
    return plain.rstrip(pad)
