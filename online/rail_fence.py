"""Rail fence cipher module."""

from __future__ import annotations


def rail_fence_encrypt(plaintext: str, rails: int = 3) -> str:
    """Encrypt text with the rail fence transposition cipher."""
    if rails < 2:
        raise ValueError("rails must be >= 2")
    if len(plaintext) <= 1:
        return plaintext

    fence = ["" for _ in range(rails)]
    row = 0
    direction = 1

    for ch in plaintext:
        fence[row] += ch
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction

    return "".join(fence)


def rail_fence_decrypt(ciphertext: str, rails: int = 3) -> str:
    """Decrypt rail fence ciphertext."""
    if rails < 2:
        raise ValueError("rails must be >= 2")
    n = len(ciphertext)
    if n <= 1:
        return ciphertext

    pattern = []
    row = 0
    direction = 1
    for _ in range(n):
        pattern.append(row)
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
        row += direction

    counts = [pattern.count(r) for r in range(rails)]
    rails_data = []
    idx = 0
    for c in counts:
        rails_data.append(list(ciphertext[idx : idx + c]))
        idx += c

    positions = [0] * rails
    out = []
    for r in pattern:
        out.append(rails_data[r][positions[r]])
        positions[r] += 1

    return "".join(out)
