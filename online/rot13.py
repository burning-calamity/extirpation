"""ROT13 cipher for alphabetic characters."""

from __future__ import annotations


def _rot13_char(ch: str) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + 13) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + 13) % 26 + ord("a"))
    return ch


def rot13_encrypt(plaintext: str) -> str:
    return "".join(_rot13_char(ch) for ch in plaintext)


def rot13_decrypt(ciphertext: str) -> str:
    # ROT13 is involutory.
    return "".join(_rot13_char(ch) for ch in ciphertext)
