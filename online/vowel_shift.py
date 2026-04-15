"""Vowel-shift substitution cipher."""

from __future__ import annotations


VOWELS_LOWER = "aeiou"
VOWELS_UPPER = "AEIOU"


def _shift_vowel(ch: str, offset: int) -> str:
    if ch in VOWELS_LOWER:
        idx = VOWELS_LOWER.index(ch)
        return VOWELS_LOWER[(idx + offset) % len(VOWELS_LOWER)]
    if ch in VOWELS_UPPER:
        idx = VOWELS_UPPER.index(ch)
        return VOWELS_UPPER[(idx + offset) % len(VOWELS_UPPER)]
    return ch


def vowel_shift_encrypt(plaintext: str, shift: int = 1) -> str:
    return "".join(_shift_vowel(ch, shift) for ch in plaintext)


def vowel_shift_decrypt(ciphertext: str, shift: int = 1) -> str:
    return "".join(_shift_vowel(ch, -shift) for ch in ciphertext)
