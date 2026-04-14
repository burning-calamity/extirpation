"""ROT18 cipher (ROT13 letters + ROT5 digits)."""

from __future__ import annotations


def _rot18_char(ch: str) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + 13) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + 13) % 26 + ord("a"))
    if ch.isdigit():
        return str((int(ch) + 5) % 10)
    return ch


def rot18_encrypt(plaintext: str) -> str:
    return "".join(_rot18_char(ch) for ch in plaintext)


def rot18_decrypt(ciphertext: str) -> str:
    # ROT18 is involutory on supported characters.
    return "".join(_rot18_char(ch) for ch in ciphertext)
