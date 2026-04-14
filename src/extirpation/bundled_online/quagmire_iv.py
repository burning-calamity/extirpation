"""Quagmire IV cipher module.

This module is designed to be discovered automatically by
`extirpation.load_online_modules("online")`.
"""

from __future__ import annotations

import string

ALPHABET = string.ascii_uppercase


def _clean(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


def keyed_alphabet(keyword: str) -> str:
    """Build a keyed alphabet by prepending unique letters from `keyword`."""
    cleaned = _clean(keyword)
    unique_key = "".join(dict.fromkeys(cleaned))
    tail = "".join(ch for ch in ALPHABET if ch not in unique_key)
    return unique_key + tail


def quagmire_iv_encrypt(
    plaintext: str,
    plain_keyword: str,
    cipher_keyword: str,
    indicator_key: str,
) -> str:
    """Encrypt plaintext with a Quagmire IV-style polyalphabetic substitution.

    This implementation uses:
    - a keyed plaintext alphabet (`plain_keyword`)
    - a keyed ciphertext alphabet (`cipher_keyword`)
    - a repeating indicator key to choose the alphabet shift at each position
    """
    clean_plain = _clean(plaintext)
    indicator = _clean(indicator_key)
    if not indicator:
        raise ValueError("indicator_key must contain at least one A-Z letter")

    plain_alpha = keyed_alphabet(plain_keyword)
    cipher_alpha = keyed_alphabet(cipher_keyword)
    out: list[str] = []

    for i, ch in enumerate(clean_plain):
        shift = ALPHABET.index(indicator[i % len(indicator)])
        p_index = plain_alpha.index(ch)
        out.append(cipher_alpha[(p_index + shift) % 26])

    return "".join(out)


def quagmire_iv_decrypt(
    ciphertext: str,
    plain_keyword: str,
    cipher_keyword: str,
    indicator_key: str,
) -> str:
    """Decrypt ciphertext produced by :func:`quagmire_iv_encrypt`."""
    clean_cipher = _clean(ciphertext)
    indicator = _clean(indicator_key)
    if not indicator:
        raise ValueError("indicator_key must contain at least one A-Z letter")

    plain_alpha = keyed_alphabet(plain_keyword)
    cipher_alpha = keyed_alphabet(cipher_keyword)
    out: list[str] = []

    for i, ch in enumerate(clean_cipher):
        shift = ALPHABET.index(indicator[i % len(indicator)])
        c_index = cipher_alpha.index(ch)
        out.append(plain_alpha[(c_index - shift) % 26])

    return "".join(out)
