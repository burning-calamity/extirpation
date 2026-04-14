"""Base64 encode/decode cipher-like module."""

from __future__ import annotations

import base64


def base64_encrypt(plaintext: str, encoding: str = 'utf-8') -> str:
    return base64.b64encode(plaintext.encode(encoding)).decode('ascii')


def base64_decrypt(ciphertext: str, encoding: str = 'utf-8') -> str:
    return base64.b64decode(ciphertext.encode('ascii')).decode(encoding)
