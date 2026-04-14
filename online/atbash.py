"""Atbash cipher module."""

from __future__ import annotations


def _transform_char(ch: str) -> str:
    if "A" <= ch <= "Z":
        return chr(ord("Z") - (ord(ch) - ord("A")))
    if "a" <= ch <= "z":
        return chr(ord("z") - (ord(ch) - ord("a")))
    return ch


def atbash_encrypt(plaintext: str) -> str:
    """Encrypt text using Atbash substitution."""
    return "".join(_transform_char(ch) for ch in plaintext)


def atbash_decrypt(ciphertext: str) -> str:
    """Decrypt Atbash text (same operation as encryption)."""
    return "".join(_transform_char(ch) for ch in ciphertext)
