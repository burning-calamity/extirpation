"""Triple-pass Caesar cipher with independent shifts."""

from __future__ import annotations


def _shift_text(text: str, s: int) -> str:
    out: list[str] = []
    s %= 26
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((p + s) % 26)))
        else:
            out.append(ch)
    return ''.join(out)


def triple_caesar_encrypt(plaintext: str, s1: int = 3, s2: int = 7, s3: int = 11) -> str:
    """Encrypt with three sequential Caesar shifts."""
    return _shift_text(_shift_text(_shift_text(plaintext, s1), s2), s3)


def triple_caesar_decrypt(ciphertext: str, s1: int = 3, s2: int = 7, s3: int = 11) -> str:
    """Decrypt text produced by ``triple_caesar_encrypt``."""
    return _shift_text(_shift_text(_shift_text(ciphertext, -s3), -s2), -s1)
