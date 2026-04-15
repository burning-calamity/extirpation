"""Chunk-swap transposition cipher.

Swaps each adjacent pair of characters, preserving trailing odd character.
"""

from __future__ import annotations


def _chunk_swap(text: str) -> str:
    chars = list(text)
    for i in range(0, len(chars) - 1, 2):
        chars[i], chars[i + 1] = chars[i + 1], chars[i]
    return "".join(chars)


def chunk_swap_encrypt(plaintext: str) -> str:
    return _chunk_swap(plaintext)


def chunk_swap_decrypt(ciphertext: str) -> str:
    return _chunk_swap(ciphertext)
