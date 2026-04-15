"""XOR stream cipher encoded as base64 text."""

from __future__ import annotations

import base64


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError('key must not be empty')
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def xor_base64_encrypt(plaintext: str, key: str) -> str:
    """Encrypt UTF-8 plaintext using repeating-key XOR and return base64."""
    raw = _xor_bytes(plaintext.encode('utf-8'), key.encode('utf-8'))
    return base64.b64encode(raw).decode('ascii')


def xor_base64_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt base64-wrapped XOR ciphertext."""
    raw = base64.b64decode(ciphertext.encode('ascii'))
    return _xor_bytes(raw, key.encode('utf-8')).decode('utf-8')
