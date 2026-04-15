"""Caesar box transposition cipher module."""

from __future__ import annotations


def caesar_box_encrypt(plaintext: str, size: int = 4) -> str:
    if size < 2:
        raise ValueError('size must be >= 2')
    text = plaintext.replace(' ', '')
    rows = (len(text) + size - 1) // size
    padded = text.ljust(rows * size, 'X')
    grid = [padded[r * size:(r + 1) * size] for r in range(rows)]
    return ''.join(grid[r][c] for c in range(size) for r in range(rows))


def caesar_box_decrypt(ciphertext: str, size: int = 4) -> str:
    if size < 2:
        raise ValueError('size must be >= 2')
    rows = (len(ciphertext) + size - 1) // size
    padded = ciphertext.ljust(rows * size, 'X')
    grid = [[''] * size for _ in range(rows)]
    idx = 0
    for c in range(size):
        for r in range(rows):
            grid[r][c] = padded[idx]
            idx += 1
    return ''.join(''.join(row) for row in grid).rstrip('X')
