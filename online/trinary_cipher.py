"""Base-3 (trinary) text encoding cipher."""

from __future__ import annotations


def trinary_encrypt(plaintext: str) -> str:
    return " ".join(format(ord(ch), "b") for ch in plaintext).replace("0", "2")


def trinary_decrypt(ciphertext: str) -> str:
    if not ciphertext.strip():
        return ""
    chunks = ciphertext.split()
    chars = [chr(int(chunk.replace("2", "0"), 2)) for chunk in chunks]
    return "".join(chars)
