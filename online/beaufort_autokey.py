"""Autokey Beaufort cipher."""

from __future__ import annotations


def _shift(ch: str) -> int:
    return ord(ch.upper()) - ord('A')


def beaufort_autokey_encrypt(plaintext: str, key: str = 'KEY') -> str:
    """Encrypt using Beaufort with running key seeded by ``key`` then plaintext."""
    seed = [c for c in key.upper() if c.isalpha()]
    if not seed:
        raise ValueError('key must contain alphabetic characters')

    out: list[str] = []
    plain_letters: list[str] = []
    idx = 0
    for ch in plaintext:
        if ch.isalpha():
            kch = seed[idx] if idx < len(seed) else plain_letters[idx - len(seed)]
            p = _shift(ch)
            k = _shift(kch)
            c = (k - p) % 26
            out.append(chr((ord('A') if ch.isupper() else ord('a')) + c))
            plain_letters.append(ch.upper())
            idx += 1
        else:
            out.append(ch)
    return ''.join(out)


def beaufort_autokey_decrypt(ciphertext: str, key: str = 'KEY') -> str:
    """Decrypt text produced by ``beaufort_autokey_encrypt``."""
    seed = [c for c in key.upper() if c.isalpha()]
    if not seed:
        raise ValueError('key must contain alphabetic characters')

    out: list[str] = []
    plain_letters: list[str] = []
    idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            kch = seed[idx] if idx < len(seed) else plain_letters[idx - len(seed)]
            c = _shift(ch)
            k = _shift(kch)
            p = (k - c) % 26
            plain_ch = chr((ord('A') if ch.isupper() else ord('a')) + p)
            out.append(plain_ch)
            plain_letters.append(plain_ch.upper())
            idx += 1
        else:
            out.append(ch)
    return ''.join(out)
