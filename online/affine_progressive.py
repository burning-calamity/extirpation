"""Progressive affine cipher with evolving additive term."""

from __future__ import annotations


ALPHABET_LEN = 26


def _mod_inverse(a: int, m: int) -> int:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError('a must be invertible modulo 26')


def affine_progressive_encrypt(plaintext: str, a: int = 5, b0: int = 8, step: int = 1) -> str:
    """Encrypt with E_i(x) = (a*x + (b0 + i*step)) mod 26."""
    _mod_inverse(a, ALPHABET_LEN)
    out: list[str] = []
    alpha_i = 0
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            x = ord(ch.upper()) - ord('A')
            b = (b0 + alpha_i * step) % ALPHABET_LEN
            y = (a * x + b) % ALPHABET_LEN
            out.append(chr(base + y))
            alpha_i += 1
        else:
            out.append(ch)
    return ''.join(out)


def affine_progressive_decrypt(ciphertext: str, a: int = 5, b0: int = 8, step: int = 1) -> str:
    """Decrypt text produced by ``affine_progressive_encrypt``."""
    inv_a = _mod_inverse(a, ALPHABET_LEN)
    out: list[str] = []
    alpha_i = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            y = ord(ch.upper()) - ord('A')
            b = (b0 + alpha_i * step) % ALPHABET_LEN
            x = (inv_a * (y - b)) % ALPHABET_LEN
            out.append(chr(base + x))
            alpha_i += 1
        else:
            out.append(ch)
    return ''.join(out)
