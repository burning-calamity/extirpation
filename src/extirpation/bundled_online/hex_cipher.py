"""Hex encoding cipher."""

from __future__ import annotations


def hex_encrypt(plaintext: str) -> str:
    return plaintext.encode("utf-8").hex()


def hex_decrypt(ciphertext: str) -> str:
    return bytes.fromhex(ciphertext).decode("utf-8")
