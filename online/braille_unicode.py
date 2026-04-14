"""Braille unicode substitution cipher for basic Latin letters."""

from __future__ import annotations

LETTER_TO_BRAILLE = {
    'A': '⠁', 'B': '⠃', 'C': '⠉', 'D': '⠙', 'E': '⠑', 'F': '⠋', 'G': '⠛', 'H': '⠓',
    'I': '⠊', 'J': '⠚', 'K': '⠅', 'L': '⠇', 'M': '⠍', 'N': '⠝', 'O': '⠕', 'P': '⠏',
    'Q': '⠟', 'R': '⠗', 'S': '⠎', 'T': '⠞', 'U': '⠥', 'V': '⠧', 'W': '⠺', 'X': '⠭',
    'Y': '⠽', 'Z': '⠵',
}
BRAILLE_TO_LETTER = {v: k for k, v in LETTER_TO_BRAILLE.items()}


def braille_unicode_encrypt(plaintext: str) -> str:
    """Encode letters into Unicode Braille characters."""
    out: list[str] = []
    for ch in plaintext:
        up = ch.upper()
        if up in LETTER_TO_BRAILLE:
            out.append(LETTER_TO_BRAILLE[up])
        else:
            out.append(ch)
    return ''.join(out)


def braille_unicode_decrypt(ciphertext: str) -> str:
    """Decode text produced by ``braille_unicode_encrypt``."""
    out: list[str] = []
    for ch in ciphertext:
        out.append(BRAILLE_TO_LETTER.get(ch, ch))
    return ''.join(out)
