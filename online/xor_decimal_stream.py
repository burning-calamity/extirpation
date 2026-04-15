"""Repeating-key XOR encoded as decimal byte values."""

from __future__ import annotations


def xor_decimal_stream_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext and return comma-separated decimal bytes."""
    if not key:
        raise ValueError("key must not be empty")
    data = plaintext.encode("utf-8")
    key_bytes = key.encode("utf-8")
    xored = [byte ^ key_bytes[i % len(key_bytes)] for i, byte in enumerate(data)]
    return ",".join(str(value) for value in xored)


def xor_decimal_stream_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text produced by :func:`xor_decimal_stream_encrypt`."""
    if not key:
        raise ValueError("key must not be empty")
    parts = [part.strip() for part in ciphertext.split(",") if part.strip()]
    data = bytes(int(part) for part in parts)
    key_bytes = key.encode("utf-8")
    plain = bytes(byte ^ key_bytes[i % len(key_bytes)] for i, byte in enumerate(data))
    return plain.decode("utf-8")
