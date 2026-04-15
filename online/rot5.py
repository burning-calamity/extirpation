"""ROT5 cipher for decimal digits."""

from __future__ import annotations


def _rot5_char(ch: str) -> str:
    if ch.isdigit():
        return str((int(ch) + 5) % 10)
    return ch


def rot5_encrypt(plaintext: str) -> str:
    return "".join(_rot5_char(ch) for ch in plaintext)


def rot5_decrypt(ciphertext: str) -> str:
    # ROT5 is involutory over decimal digits.
    return "".join(_rot5_char(ch) for ch in ciphertext)
