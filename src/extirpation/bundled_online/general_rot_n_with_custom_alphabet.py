"""General ROT-N with configurable alphabet."""

from __future__ import annotations


def _translate(text: str, n: int, alphabet: str) -> str:
    if not alphabet:
        raise ValueError('alphabet must not be empty')
    idx = {ch: i for i, ch in enumerate(alphabet)}
    m = len(alphabet)

    out: list[str] = []
    for ch in text:
        if ch in idx:
            out.append(alphabet[(idx[ch] + n) % m])
        else:
            out.append(ch)
    return ''.join(out)


def general_rot_encrypt(plaintext: str, n: int = 13, alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') -> str:
    """Encrypt text using arbitrary alphabet rotation."""
    return _translate(plaintext, n, alphabet)


def general_rot_decrypt(ciphertext: str, n: int = 13, alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') -> str:
    """Decrypt text produced by ``general_rot_encrypt``."""
    return _translate(ciphertext, -n, alphabet)
