"""Keyword substitution cipher module."""

from __future__ import annotations

import string

ALPHABET = string.ascii_uppercase


def _sub_alphabet(keyword: str) -> str:
    key = ''.join(dict.fromkeys(ch for ch in keyword.upper() if ch.isalpha()))
    return key + ''.join(ch for ch in ALPHABET if ch not in key)


def keyword_encrypt(plaintext: str, keyword: str) -> str:
    sub = _sub_alphabet(keyword)
    out = []
    for ch in plaintext:
        if ch.isalpha():
            idx = ALPHABET.index(ch.upper())
            mapped = sub[idx]
            out.append(mapped if ch.isupper() else mapped.lower())
        else:
            out.append(ch)
    return ''.join(out)


def keyword_decrypt(ciphertext: str, keyword: str) -> str:
    sub = _sub_alphabet(keyword)
    out = []
    for ch in ciphertext:
        if ch.isalpha():
            idx = sub.index(ch.upper())
            mapped = ALPHABET[idx]
            out.append(mapped if ch.isupper() else mapped.lower())
        else:
            out.append(ch)
    return ''.join(out)
