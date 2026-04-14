"""Diagonal zigzag transposition cipher."""

from __future__ import annotations


def diagonal_zigzag_encrypt(plaintext: str, width: int = 6, pad: str = 'X') -> str:
    """Write row-wise and read diagonals, alternating diagonal direction."""
    if width <= 0:
        raise ValueError('width must be > 0')
    if len(pad) != 1:
        raise ValueError('pad must be one character')

    rows = (len(plaintext) + width - 1) // width
    text = plaintext + pad * (rows * width - len(plaintext))
    grid = [list(text[r * width : (r + 1) * width]) for r in range(rows)]

    out: list[str] = []
    for d in range(rows + width - 1):
        cells: list[str] = []
        for r in range(rows):
            c = d - r
            if 0 <= c < width:
                cells.append(grid[r][c])
        if d % 2 == 1:
            cells.reverse()
        out.extend(cells)
    return ''.join(out)


def diagonal_zigzag_decrypt(ciphertext: str, width: int = 6, pad: str = 'X') -> str:
    """Decrypt text produced by ``diagonal_zigzag_encrypt``."""
    if width <= 0:
        raise ValueError('width must be > 0')
    if len(pad) != 1:
        raise ValueError('pad must be one character')
    if len(ciphertext) % width != 0:
        raise ValueError('ciphertext length must be divisible by width')

    rows = len(ciphertext) // width
    grid = [['' for _ in range(width)] for _ in range(rows)]

    idx = 0
    for d in range(rows + width - 1):
        coords: list[tuple[int, int]] = []
        for r in range(rows):
            c = d - r
            if 0 <= c < width:
                coords.append((r, c))
        if d % 2 == 1:
            coords.reverse()
        for r, c in coords:
            grid[r][c] = ciphertext[idx]
            idx += 1

    plain = ''.join(''.join(row) for row in grid)
    return plain.rstrip(pad)
