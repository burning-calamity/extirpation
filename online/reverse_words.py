"""Reverse words cipher (word-order transposition)."""

from __future__ import annotations


def reverse_words_encrypt(plaintext: str) -> str:
    return " ".join(plaintext.split(" ")[::-1])


def reverse_words_decrypt(ciphertext: str) -> str:
    return " ".join(ciphertext.split(" ")[::-1])
