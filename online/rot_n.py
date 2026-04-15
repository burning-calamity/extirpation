"""Generic ROT-N Caesar variant."""

from __future__ import annotations


def _shift_char(ch: str, n: int) -> str:
    if not ch.isalpha():
        return ch
    base = ord('A') if ch.isupper() else ord('a')
    return chr((ord(ch) - base + n) % 26 + base)


def rot_n_encrypt(plaintext: str, n: int = 13) -> str:
    """Encrypt text with a Caesar shift of ``n``."""
    return ''.join(_shift_char(ch, n) for ch in plaintext)


def rot_n_decrypt(ciphertext: str, n: int = 13) -> str:
    """Decrypt text produced by ``rot_n_encrypt``."""
    return ''.join(_shift_char(ch, -n) for ch in ciphertext)
