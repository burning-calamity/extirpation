"""Baconian cipher module."""

from __future__ import annotations

import string

ALPHABET = string.ascii_uppercase
ENCODE_TABLE = {ch: format(i, "05b").replace("0", "A").replace("1", "B") for i, ch in enumerate(ALPHABET)}
DECODE_TABLE = {value: key for key, value in ENCODE_TABLE.items()}


def baconian_encrypt(plaintext: str) -> str:
    """Encrypt letters as 5-symbol A/B groups; non-letters are ignored."""
    letters = [ch for ch in plaintext.upper() if ch in ALPHABET]
    return " ".join(ENCODE_TABLE[ch] for ch in letters)


def baconian_decrypt(ciphertext: str) -> str:
    """Decrypt whitespace-separated Baconian A/B groups to uppercase letters."""
    tokens = ["".join(ch for ch in token.upper() if ch in {"A", "B"}) for token in ciphertext.split()]
    if any(len(token) != 5 for token in tokens):
        raise ValueError("each Baconian token must contain exactly 5 A/B symbols")

    try:
        return "".join(DECODE_TABLE[token] for token in tokens)
    except KeyError as exc:
        raise ValueError("ciphertext contains an invalid Baconian token") from exc
