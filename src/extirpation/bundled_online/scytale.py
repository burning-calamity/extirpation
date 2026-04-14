"""Scytale transposition cipher module."""

from __future__ import annotations


def scytale_encrypt(plaintext: str, rails: int = 3) -> str:
    if rails < 2:
        raise ValueError('rails must be >= 2')
    rows = [plaintext[i::rails] for i in range(rails)]
    return ''.join(rows)


def scytale_decrypt(ciphertext: str, rails: int = 3) -> str:
    if rails < 2:
        raise ValueError('rails must be >= 2')
    n = len(ciphertext)
    lens = [n // rails + (1 if i < n % rails else 0) for i in range(rails)]
    rows = []
    idx = 0
    for ln in lens:
        rows.append(ciphertext[idx:idx+ln])
        idx += ln
    out = []
    for i in range(max(lens)):
        for r in range(rails):
            if i < len(rows[r]):
                out.append(rows[r][i])
    return ''.join(out)
