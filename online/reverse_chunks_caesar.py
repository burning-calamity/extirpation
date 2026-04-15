"""Reverse fixed-size chunks and apply Caesar shifting."""

from __future__ import annotations


def _caesar(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + shift) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + shift) % 26))
    return ch


def _reverse_chunks(text: str, chunk_size: int) -> str:
    return "".join(text[i : i + chunk_size][::-1] for i in range(0, len(text), chunk_size))


def reverse_chunks_caesar_encrypt(plaintext: str, shift: int = 3, chunk_size: int = 4) -> str:
    """Encrypt by reversing chunks then applying Caesar shift."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    chunked = _reverse_chunks(plaintext, chunk_size)
    return "".join(_caesar(ch, shift) for ch in chunked)


def reverse_chunks_caesar_decrypt(ciphertext: str, shift: int = 3, chunk_size: int = 4) -> str:
    """Decrypt text from :func:`reverse_chunks_caesar_encrypt`."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    unshifted = "".join(_caesar(ch, -shift) for ch in ciphertext)
    return _reverse_chunks(unshifted, chunk_size)
