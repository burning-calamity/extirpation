"""Alphabetic one-time pad module (A-Z only)."""

from __future__ import annotations


def _clean_alpha(s: str) -> str:
    return ''.join(ch for ch in s.upper() if ch.isalpha())


def otp_encrypt(plaintext: str, pad: str) -> str:
    text = _clean_alpha(plaintext)
    key = _clean_alpha(pad)
    if len(key) < len(text):
        raise ValueError('pad must be at least as long as plaintext letters')
    return ''.join(chr(65 + ((ord(p) - 65 + ord(k) - 65) % 26)) for p, k in zip(text, key))


def otp_decrypt(ciphertext: str, pad: str) -> str:
    text = _clean_alpha(ciphertext)
    key = _clean_alpha(pad)
    if len(key) < len(text):
        raise ValueError('pad must be at least as long as ciphertext letters')
    return ''.join(chr(65 + ((ord(c) - 65 - (ord(k) - 65)) % 26)) for c, k in zip(text, key))
