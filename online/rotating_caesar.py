"""Caesar cipher with per-letter rotating shift."""

from __future__ import annotations


def rotating_caesar_encrypt(plaintext: str, start_shift: int = 1, step: int = 1) -> str:
    """Encrypt by increasing shift for each alphabetic character."""
    out: list[str] = []
    idx = 0
    for ch in plaintext:
        if ch.isalpha():
            s = (start_shift + idx * step) % 26
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((p + s) % 26)))
            idx += 1
        else:
            out.append(ch)
    return ''.join(out)


def rotating_caesar_decrypt(ciphertext: str, start_shift: int = 1, step: int = 1) -> str:
    """Decrypt text produced by ``rotating_caesar_encrypt``."""
    out: list[str] = []
    idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            s = (start_shift + idx * step) % 26
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((c - s) % 26)))
            idx += 1
        else:
            out.append(ch)
    return ''.join(out)
