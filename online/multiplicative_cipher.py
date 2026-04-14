"""Multiplicative cipher over A-Z."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
M = len(ALPHABET)


def _mod_inverse(a: int, m: int) -> int:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError('key has no modular inverse modulo 26')


def multiplicative_encrypt(plaintext: str, key: int = 5) -> str:
    """Encrypt using E(x) = (key * x) mod 26."""
    _mod_inverse(key, M)
    out: list[str] = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            idx = ord(ch.upper()) - ord('A')
            enc = (key * idx) % M
            out.append(chr(base + enc))
        else:
            out.append(ch)
    return ''.join(out)


def multiplicative_decrypt(ciphertext: str, key: int = 5) -> str:
    """Decrypt text produced by ``multiplicative_encrypt``."""
    inv = _mod_inverse(key, M)
    out: list[str] = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            idx = ord(ch.upper()) - ord('A')
            dec = (inv * idx) % M
            out.append(chr(base + dec))
        else:
            out.append(ch)
    return ''.join(out)
