"""Spiral route transposition cipher module."""

from __future__ import annotations


def _spiral_indices(rows: int, cols: int) -> list[tuple[int, int]]:
    top, left, bottom, right = 0, 0, rows - 1, cols - 1
    order = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            order.append((top, c))
        top += 1
        for r in range(top, bottom + 1):
            order.append((r, right))
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                order.append((bottom, c))
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                order.append((r, left))
            left += 1
    return order


def spiral_route_encrypt(plaintext: str, width: int = 5) -> str:
    if width < 2:
        raise ValueError('width must be >= 2')
    rows = (len(plaintext) + width - 1) // width
    padded = plaintext.ljust(rows * width)
    grid = [list(padded[r * width:(r + 1) * width]) for r in range(rows)]
    return ''.join(grid[r][c] for r, c in _spiral_indices(rows, width)).rstrip()


def spiral_route_decrypt(ciphertext: str, width: int = 5) -> str:
    if width < 2:
        raise ValueError('width must be >= 2')
    rows = (len(ciphertext) + width - 1) // width
    padded = ciphertext.ljust(rows * width)
    grid = [[''] * width for _ in range(rows)]
    for ch, (r, c) in zip(padded, _spiral_indices(rows, width)):
        grid[r][c] = ch
    return ''.join(''.join(row) for row in grid).rstrip()
