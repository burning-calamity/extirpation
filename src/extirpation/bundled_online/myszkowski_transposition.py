"""Myszkowski transposition cipher."""

from __future__ import annotations


def _ranks(key: str) -> list[int]:
    order = sorted((ch, i) for i, ch in enumerate(key))
    ranks = [0] * len(key)
    rank = -1
    prev = None
    for ch, i in order:
        if ch != prev:
            rank += 1
            prev = ch
        ranks[i] = rank
    return ranks


def myszkowski_encrypt(plaintext: str, key: str) -> str:
    """Encrypt using Myszkowski transposition."""
    if not key:
        raise ValueError('key must not be empty')
    cols = len(key)
    ranks = _ranks(key)

    rows = (len(plaintext) + cols - 1) // cols
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(plaintext):
                grid[r][c] = plaintext[idx]
                idx += 1

    out: list[str] = []
    for rank in sorted(set(ranks)):
        group = [i for i, rk in enumerate(ranks) if rk == rank]
        if len(group) == 1:
            c = group[0]
            for r in range(rows):
                if grid[r][c]:
                    out.append(grid[r][c])
        else:
            for r in range(rows):
                for c in group:
                    if grid[r][c]:
                        out.append(grid[r][c])
    return ''.join(out)


def myszkowski_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text produced by ``myszkowski_encrypt``."""
    if not key:
        raise ValueError('key must not be empty')
    cols = len(key)
    ranks = _ranks(key)
    rows = (len(ciphertext) + cols - 1) // cols

    grid = [[None for _ in range(cols)] for _ in range(rows)]
    filled_positions: list[tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            if r * cols + c < len(ciphertext):
                filled_positions.append((r, c))
    filled_set = set(filled_positions)

    idx = 0
    for rank in sorted(set(ranks)):
        group = [i for i, rk in enumerate(ranks) if rk == rank]
        if len(group) == 1:
            c = group[0]
            for r in range(rows):
                if (r, c) in filled_set:
                    grid[r][c] = ciphertext[idx]
                    idx += 1
        else:
            for r in range(rows):
                for c in group:
                    if (r, c) in filled_set:
                        grid[r][c] = ciphertext[idx]
                        idx += 1

    out: list[str] = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) in filled_set:
                out.append(grid[r][c] or '')
    return ''.join(out)
