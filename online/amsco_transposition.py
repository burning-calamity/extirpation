"""AMSCO transposition cipher (simplified classical variant)."""

from __future__ import annotations


def _key_order(key: str) -> list[int]:
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def _cell_lengths(text_len: int, cols: int) -> list[list[int]]:
    lengths: list[list[int]] = []
    used = 0
    row_start_two = False
    while used < text_len:
        row: list[int] = []
        take_two = row_start_two
        for _ in range(cols):
            if used >= text_len:
                break
            ln = 2 if take_two else 1
            ln = min(ln, text_len - used)
            row.append(ln)
            used += ln
            take_two = not take_two
        lengths.append(row)
        row_start_two = not row_start_two
    return lengths


def amsco_encrypt(plaintext: str, key: str) -> str:
    """Encrypt using AMSCO transposition with alternating 1/2-letter cells."""
    if not key:
        raise ValueError('key must not be empty')

    cols = len(key)
    lengths = _cell_lengths(len(plaintext), cols)

    grid: list[list[str]] = []
    idx = 0
    for row in lengths:
        row_cells: list[str] = []
        for ln in row:
            row_cells.append(plaintext[idx:idx + ln])
            idx += ln
        grid.append(row_cells)

    out: list[str] = []
    for c in _key_order(key):
        for r, row in enumerate(grid):
            if c < len(row):
                out.append(grid[r][c])
    return ''.join(out)


def amsco_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text produced by ``amsco_encrypt``."""
    if not key:
        raise ValueError('key must not be empty')

    cols = len(key)
    lengths = _cell_lengths(len(ciphertext), cols)
    grid: list[list[str]] = [['' for _ in row] for row in lengths]

    idx = 0
    for c in _key_order(key):
        for r, row in enumerate(lengths):
            if c < len(row):
                ln = row[c]
                grid[r][c] = ciphertext[idx:idx + ln]
                idx += ln

    out: list[str] = []
    for r, row in enumerate(lengths):
        for c in range(len(row)):
            out.append(grid[r][c])
    return ''.join(out)
