"""Alternating Caesar cipher."""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + shift) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + shift) % 26))
    return ch


def alternating_caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    """Encrypt by alternating +shift and -shift for each alphabetic character."""
    out: list[str] = []
    direction = 1
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift_char(ch, direction * shift))
            direction *= -1
        else:
            out.append(ch)
    return "".join(out)


def alternating_caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    """Decrypt alternating Caesar text."""
    out: list[str] = []
    direction = 1
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift_char(ch, -direction * shift))
            direction *= -1
        else:
            out.append(ch)
    return "".join(out)
