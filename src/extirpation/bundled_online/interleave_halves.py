"""Transposition cipher that interleaves two halves of the text."""

from __future__ import annotations


def interleave_halves_encrypt(plaintext: str) -> str:
    """Encrypt by interleaving the left and right halves of the string."""
    mid = (len(plaintext) + 1) // 2
    left = plaintext[:mid]
    right = plaintext[mid:]
    out: list[str] = []
    for i in range(max(len(left), len(right))):
        if i < len(left):
            out.append(left[i])
        if i < len(right):
            out.append(right[i])
    return "".join(out)


def interleave_halves_decrypt(ciphertext: str) -> str:
    """Decrypt text produced by :func:`interleave_halves_encrypt`."""
    left_len = (len(ciphertext) + 1) // 2
    left = ciphertext[::2][:left_len]
    right = ciphertext[1::2]
    return left + right
