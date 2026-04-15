"""Route cipher module (row fill, reverse row read)."""

from __future__ import annotations


def route_encrypt(plaintext: str, width: int = 5) -> str:
    if width < 2:
        raise ValueError('width must be >= 2')
    rows = (len(plaintext) + width - 1) // width
    padded = plaintext.ljust(rows * width)
    grid = [padded[i * width:(i + 1) * width] for i in range(rows)]
    out = []
    for r, row in enumerate(grid):
        out.append(row[::-1] if r % 2 else row)
    return ''.join(out)


def route_decrypt(ciphertext: str, width: int = 5) -> str:
    if width < 2:
        raise ValueError('width must be >= 2')
    rows = (len(ciphertext) + width - 1) // width
    padded = ciphertext.ljust(rows * width)
    grid = [padded[i * width:(i + 1) * width] for i in range(rows)]
    out = []
    for r, row in enumerate(grid):
        out.append(row[::-1] if r % 2 else row)
    return ''.join(out).rstrip()
