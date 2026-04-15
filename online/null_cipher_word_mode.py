"""Null cipher variant operating on words."""

from __future__ import annotations


def null_cipher_word_encrypt(plaintext: str, filler_word: str = 'lorem', step: int = 3) -> str:
    """Insert filler words between plaintext words."""
    if step < 1:
        raise ValueError('step must be >= 1')
    words = plaintext.split()
    if step == 1:
        return ' '.join(words)

    out: list[str] = []
    for w in words:
        out.append(w)
        out.extend([filler_word] * (step - 1))
    return ' '.join(out)


def null_cipher_word_decrypt(ciphertext: str, step: int = 3) -> str:
    """Recover plaintext by taking every ``step``-th word."""
    if step < 1:
        raise ValueError('step must be >= 1')
    words = ciphertext.split()
    return ' '.join(words[::step])
