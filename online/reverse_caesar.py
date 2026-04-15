"""Reverse text and apply Caesar shift."""

from __future__ import annotations


def _caesar(text: str, shift: int) -> str:
    out: list[str] = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return ''.join(out)


def reverse_caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    """Reverse plaintext then apply Caesar shift."""
    return _caesar(plaintext[::-1], shift)


def reverse_caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    """Undo Caesar shift then reverse back."""
    return _caesar(ciphertext, -shift)[::-1]
