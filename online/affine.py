"""Affine cipher module."""

from __future__ import annotations


def _mod_inverse(a: int, m: int = 26) -> int:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("'a' must be coprime with 26")


def _transform(ch: str, a: int, b: int, decrypt: bool) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
    elif "a" <= ch <= "z":
        base = ord("a")
    else:
        return ch

    x = ord(ch) - base
    if decrypt:
        inv = _mod_inverse(a)
        y = (inv * (x - b)) % 26
    else:
        y = (a * x + b) % 26
    return chr(y + base)


def affine_encrypt(plaintext: str, a: int = 5, b: int = 8) -> str:
    """Encrypt text with the affine cipher: E(x) = (a*x + b) mod 26."""
    _mod_inverse(a)
    return "".join(_transform(ch, a, b, decrypt=False) for ch in plaintext)


def affine_decrypt(ciphertext: str, a: int = 5, b: int = 8) -> str:
    """Decrypt affine-cipher text."""
    return "".join(_transform(ch, a, b, decrypt=True) for ch in ciphertext)
