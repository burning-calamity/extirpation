"""Beaufort cipher module."""

from __future__ import annotations


def _clean_key(key: str) -> str:
    cleaned = "".join(ch for ch in key.upper() if ch.isalpha())
    if not cleaned:
        raise ValueError("key must contain at least one alphabetic character")
    return cleaned


def beaufort_encrypt(plaintext: str, key: str) -> str:
    """Encrypt/decrypt text with Beaufort cipher (self-inverse)."""
    key = _clean_key(key)
    out: list[str] = []
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            p = ord(ch.upper()) - ord("A")
            k = ord(key[j % len(key)]) - ord("A")
            c = (k - p) % 26
            out.append(chr(base + c))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def beaufort_decrypt(ciphertext: str, key: str) -> str:
    """Beaufort is reciprocal, so decrypt is the same operation."""
    return beaufort_encrypt(ciphertext, key)
