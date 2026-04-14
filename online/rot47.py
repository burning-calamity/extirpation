"""ROT47 cipher module."""

from __future__ import annotations


def _rot47_char(ch: str) -> str:
    o = ord(ch)
    if 33 <= o <= 126:
        return chr(33 + ((o - 33 + 47) % 94))
    return ch


def rot47_encrypt(plaintext: str) -> str:
    """Encrypt text using ROT47."""
    return "".join(_rot47_char(ch) for ch in plaintext)


def rot47_decrypt(ciphertext: str) -> str:
    """Decrypt ROT47 text (same transform as encryption)."""
    return "".join(_rot47_char(ch) for ch in ciphertext)
