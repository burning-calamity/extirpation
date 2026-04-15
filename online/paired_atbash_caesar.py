"""Compose Atbash with Caesar shift."""

from __future__ import annotations


def _atbash(ch: str) -> str:
    if "A" <= ch <= "Z":
        return chr(ord("Z") - (ord(ch) - ord("A")))
    if "a" <= ch <= "z":
        return chr(ord("z") - (ord(ch) - ord("a")))
    return ch


def _caesar(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + shift) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + shift) % 26))
    return ch


def paired_atbash_caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    """Encrypt with Atbash followed by Caesar shift."""
    return "".join(_caesar(_atbash(ch), shift) for ch in plaintext)


def paired_atbash_caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    """Decrypt text from :func:`paired_atbash_caesar_encrypt`."""
    return "".join(_atbash(_caesar(ch, -shift)) for ch in ciphertext)
