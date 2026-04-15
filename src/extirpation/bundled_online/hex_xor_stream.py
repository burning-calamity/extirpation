"""XOR stream cipher with hex encoding output."""

from __future__ import annotations


def hex_xor_stream_encrypt(plaintext: str, key: str) -> str:
    """Encrypt UTF-8 plaintext with repeating-key XOR and return hex."""
    if not key:
        raise ValueError("key must not be empty")
    data = plaintext.encode("utf-8")
    key_bytes = key.encode("utf-8")
    out = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))
    return out.hex()


def hex_xor_stream_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt repeating-key XOR hex ciphertext back to UTF-8 plaintext."""
    if not key:
        raise ValueError("key must not be empty")
    data = bytes.fromhex(ciphertext.strip())
    key_bytes = key.encode("utf-8")
    out = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))
    return out.decode("utf-8")
