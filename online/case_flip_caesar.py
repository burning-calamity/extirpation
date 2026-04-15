"""Caesar cipher variant that flips case on transformed letters."""

from __future__ import annotations


def _caesar(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + shift) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + shift) % 26))
    return ch


def _flip_case(ch: str) -> str:
    if ch.islower():
        return ch.upper()
    if ch.isupper():
        return ch.lower()
    return ch


def case_flip_caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    """Encrypt letters with Caesar and flip letter case."""
    return "".join(_flip_case(_caesar(ch, shift)) for ch in plaintext)


def case_flip_caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    """Decrypt text produced by :func:`case_flip_caesar_encrypt`."""
    return "".join(_caesar(_flip_case(ch), -shift) for ch in ciphertext)
