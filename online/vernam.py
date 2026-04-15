"""Vernam XOR cipher module (hex representation)."""

from __future__ import annotations


def vernam_encrypt(plaintext: str, key: str, encoding: str = 'utf-8') -> str:
    p = plaintext.encode(encoding)
    k = key.encode(encoding)
    if len(k) < len(p):
        raise ValueError('key must be at least as long as plaintext bytes')
    return bytes(a ^ b for a, b in zip(p, k)).hex()


def vernam_decrypt(ciphertext_hex: str, key: str, encoding: str = 'utf-8') -> str:
    c = bytes.fromhex(ciphertext_hex)
    k = key.encode(encoding)
    if len(k) < len(c):
        raise ValueError('key must be at least as long as ciphertext bytes')
    return bytes(a ^ b for a, b in zip(c, k)).decode(encoding)
