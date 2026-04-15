"""Quagmire I cipher variant."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def _keyed_alphabet(keyword: str) -> str:
    seen: set[str] = set()
    chars: list[str] = []
    for ch in (keyword.upper() + ALPHABET):
        if ch in ALPHABET and ch not in seen:
            seen.add(ch)
            chars.append(ch)
    return ''.join(chars)


def quagmire_i_encrypt(
    plaintext: str,
    plaintext_keyword: str,
    key: str,
    indicator: str = 'A',
) -> str:
    """Encrypt using Quagmire I style alphabets."""
    pt_alpha = _keyed_alphabet(plaintext_keyword)
    ct_alpha = ALPHABET
    indicator_shift = ALPHABET.index(indicator.upper()[0])

    out: list[str] = []
    key_stream = [c for c in key.upper() if c in ALPHABET] or ['A']
    j = 0
    for ch in plaintext:
        up = ch.upper()
        if up not in ALPHABET:
            out.append(ch)
            continue
        k = key_stream[j % len(key_stream)]
        j += 1
        shift = (ALPHABET.index(k) + indicator_shift) % 26
        p = pt_alpha.index(up)
        c = ct_alpha[(p + shift) % 26]
        out.append(c if ch.isupper() else c.lower())
    return ''.join(out)


def quagmire_i_decrypt(
    ciphertext: str,
    plaintext_keyword: str,
    key: str,
    indicator: str = 'A',
) -> str:
    """Decrypt text produced by ``quagmire_i_encrypt``."""
    pt_alpha = _keyed_alphabet(plaintext_keyword)
    ct_alpha = ALPHABET
    indicator_shift = ALPHABET.index(indicator.upper()[0])

    out: list[str] = []
    key_stream = [c for c in key.upper() if c in ALPHABET] or ['A']
    j = 0
    for ch in ciphertext:
        up = ch.upper()
        if up not in ALPHABET:
            out.append(ch)
            continue
        k = key_stream[j % len(key_stream)]
        j += 1
        shift = (ALPHABET.index(k) + indicator_shift) % 26
        p = (ct_alpha.index(up) - shift) % 26
        plain = pt_alpha[p]
        out.append(plain if ch.isupper() else plain.lower())
    return ''.join(out)
