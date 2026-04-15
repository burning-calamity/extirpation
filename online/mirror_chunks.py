"""Chunk mirror cipher.

Reverses characters in fixed-size chunks. Operation is symmetric.
"""

from __future__ import annotations


def _mirror_chunks(text: str, chunk_size: int) -> str:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    return "".join(chunk[::-1] for chunk in chunks)


def mirror_chunks_encrypt(plaintext: str, chunk_size: int = 3) -> str:
    return _mirror_chunks(plaintext, chunk_size)


def mirror_chunks_decrypt(ciphertext: str, chunk_size: int = 3) -> str:
    return _mirror_chunks(ciphertext, chunk_size)
