"""Keyword-seeded Caesar cipher.

Shift value is derived from keyword character positions.
"""

from __future__ import annotations


def _keyword_shift(keyword: str) -> int:
    letters = [ord(ch.upper()) - ord("A") + 1 for ch in keyword if ch.isalpha()]
    if not letters:
        raise ValueError("keyword must include alphabetic characters")
    return sum(letters) % 26


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


def keyword_caesar_encrypt(plaintext: str, keyword: str = "SECRET") -> str:
    shift = _keyword_shift(keyword)
    return "".join(_shift_char(ch, shift) for ch in plaintext)


def keyword_caesar_decrypt(ciphertext: str, keyword: str = "SECRET") -> str:
    shift = _keyword_shift(keyword)
    return "".join(_shift_char(ch, -shift) for ch in ciphertext)
