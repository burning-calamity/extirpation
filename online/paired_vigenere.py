"""Vigenere variant alternating between two keys."""

from __future__ import annotations


def _norm_key(key: str) -> list[int]:
    vals = [ord(c.upper()) - ord('A') for c in key if c.isalpha()]
    if not vals:
        raise ValueError('keys must contain alphabetic characters')
    return vals


def paired_vigenere_encrypt(plaintext: str, key_a: str = 'ALPHA', key_b: str = 'OMEGA') -> str:
    """Encrypt, alternating key streams for each alphabetic character."""
    ka = _norm_key(key_a)
    kb = _norm_key(key_b)
    ia = ib = 0
    out: list[str] = []
    letter_index = 0
    for ch in plaintext:
        if ch.isalpha():
            key = ka if letter_index % 2 == 0 else kb
            idx = ia if letter_index % 2 == 0 else ib
            shift = key[idx % len(key)]
            if letter_index % 2 == 0:
                ia += 1
            else:
                ib += 1
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((p + shift) % 26)))
            letter_index += 1
        else:
            out.append(ch)
    return ''.join(out)


def paired_vigenere_decrypt(ciphertext: str, key_a: str = 'ALPHA', key_b: str = 'OMEGA') -> str:
    """Decrypt text produced by ``paired_vigenere_encrypt``."""
    ka = _norm_key(key_a)
    kb = _norm_key(key_b)
    ia = ib = 0
    out: list[str] = []
    letter_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            key = ka if letter_index % 2 == 0 else kb
            idx = ia if letter_index % 2 == 0 else ib
            shift = key[idx % len(key)]
            if letter_index % 2 == 0:
                ia += 1
            else:
                ib += 1
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((c - shift) % 26)))
            letter_index += 1
        else:
            out.append(ch)
    return ''.join(out)
