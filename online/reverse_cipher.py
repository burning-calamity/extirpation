"""Simple reverse cipher module."""

from __future__ import annotations


def reverse_encrypt(plaintext: str) -> str:
    return plaintext[::-1]


def reverse_decrypt(ciphertext: str) -> str:
    return ciphertext[::-1]
