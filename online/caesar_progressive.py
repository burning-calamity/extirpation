"""Progressive Caesar cipher.

Shift increases by `step` after each alphabetic character.
"""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


def caesar_progressive_encrypt(plaintext: str, start_shift: int = 1, step: int = 1) -> str:
    out: list[str] = []
    shift = start_shift
    for ch in plaintext:
        out.append(_shift_char(ch, shift))
        if ch.isalpha():
            shift += step
    return "".join(out)


def caesar_progressive_decrypt(ciphertext: str, start_shift: int = 1, step: int = 1) -> str:
    out: list[str] = []
    shift = start_shift
    for ch in ciphertext:
        out.append(_shift_char(ch, -shift))
        if ch.isalpha():
            shift += step
    return "".join(out)
