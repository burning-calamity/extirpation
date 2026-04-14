"""Simple null cipher by inserting filler characters between plaintext symbols."""

from __future__ import annotations


def null_cipher_encrypt(plaintext: str, filler: str = 'X', step: int = 3) -> str:
    """Interleave each plaintext character with filler to hide message positionally."""
    if step < 1:
        raise ValueError('step must be >= 1')
    if step == 1:
        return plaintext
    if len(filler) != 1:
        raise ValueError('filler must be exactly one character')
    pad = filler * (step - 1)
    return ''.join(ch + pad for ch in plaintext)


def null_cipher_decrypt(ciphertext: str, step: int = 3) -> str:
    """Recover plaintext by taking every ``step``-th character."""
    if step < 1:
        raise ValueError('step must be >= 1')
    return ciphertext[::step]
