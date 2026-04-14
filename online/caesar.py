"""Caesar cipher module."""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr((ord(ch) - base + shift) % 26 + base)
    if "a" <= ch <= "z":
        base = ord("a")
        return chr((ord(ch) - base + shift) % 26 + base)
    return ch


def caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    """Encrypt text with a Caesar shift."""
    return "".join(_shift_char(ch, shift) for ch in plaintext)


def caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    """Decrypt text encrypted with a Caesar shift."""
    return "".join(_shift_char(ch, -shift) for ch in ciphertext)
