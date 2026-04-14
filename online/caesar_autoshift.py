"""Caesar cipher variant with an automatically increasing shift per letter."""

from __future__ import annotations


def _shift_char(ch: str, amount: int) -> str:
    if not ch.isalpha():
        return ch
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + amount) % 26 + base)


def caesar_autoshift_encrypt(plaintext: str, start_shift: int = 1) -> str:
    """Encrypt by applying a Caesar shift that increments for each alphabetic character."""
    out: list[str] = []
    shift = start_shift
    for ch in plaintext:
        out.append(_shift_char(ch, shift))
        if ch.isalpha():
            shift += 1
    return ''.join(out)


def caesar_autoshift_decrypt(ciphertext: str, start_shift: int = 1) -> str:
    """Decrypt text encrypted with ``caesar_autoshift_encrypt``."""
    out: list[str] = []
    shift = start_shift
    for ch in ciphertext:
        out.append(_shift_char(ch, -shift))
        if ch.isalpha():
            shift += 1
    return ''.join(out)
