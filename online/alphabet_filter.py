"""Filter text to characters belonging to a named alphabet/script."""

from __future__ import annotations

ALPHABETS: dict[str, tuple[int, int]] = {
    'latin': (0x0041, 0x024F),
    'cyrillic': (0x0400, 0x04FF),
    'greek': (0x0370, 0x03FF),
    'arabic': (0x0600, 0x06FF),
    'devanagari': (0x0900, 0x097F),
}


def _in_alphabet(ch: str, alphabet: str) -> bool:
    if alphabet not in ALPHABETS:
        raise ValueError(f'unknown alphabet: {alphabet}')
    start, end = ALPHABETS[alphabet]
    cp = ord(ch)
    return start <= cp <= end and ch.isalpha()


def alphabet_filter_encrypt(plaintext: str, alphabet: str = 'latin') -> str:
    """Return only letters belonging to the selected alphabet."""
    alphabet = alphabet.strip().lower()
    return ''.join(ch for ch in plaintext if _in_alphabet(ch, alphabet))


def alphabet_filter_decrypt(ciphertext: str, alphabet: str = 'latin') -> str:
    """Idempotent decode for filtered text (same behavior as encrypt)."""
    return alphabet_filter_encrypt(ciphertext, alphabet=alphabet)
