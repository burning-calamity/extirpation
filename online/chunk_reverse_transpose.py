"""Chunk-based transposition by reversing each fixed-size chunk."""

from __future__ import annotations


def chunk_reverse_transpose_encrypt(plaintext: str, chunk_size: int = 3) -> str:
    """Encrypt by reversing each chunk of ``chunk_size`` characters."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    return "".join(plaintext[i : i + chunk_size][::-1] for i in range(0, len(plaintext), chunk_size))


def chunk_reverse_transpose_decrypt(ciphertext: str, chunk_size: int = 3) -> str:
    """Decrypt text from :func:`chunk_reverse_transpose_encrypt`."""
    return chunk_reverse_transpose_encrypt(ciphertext, chunk_size=chunk_size)
