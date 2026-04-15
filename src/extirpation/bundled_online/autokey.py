"""Autokey Vigenere cipher module."""

from __future__ import annotations


def _clean_alpha(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch.isalpha())


def autokey_encrypt(plaintext: str, key: str) -> str:
    clean_key = _clean_alpha(key)
    if not clean_key:
        raise ValueError("key must contain at least one alphabetic character")

    plain_alpha = _clean_alpha(plaintext)
    full_key = (clean_key + plain_alpha)[: len(plain_alpha)]

    out = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            p = ord(ch.upper()) - ord("A")
            k = ord(full_key[i]) - ord("A")
            out.append(chr(base + ((p + k) % 26)))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def autokey_decrypt(ciphertext: str, key: str) -> str:
    clean_key = _clean_alpha(key)
    if not clean_key:
        raise ValueError("key must contain at least one alphabetic character")

    recovered_plain: list[str] = []
    out: list[str] = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            c = ord(ch.upper()) - ord("A")
            if i < len(clean_key):
                k = ord(clean_key[i]) - ord("A")
            else:
                k = ord(recovered_plain[i - len(clean_key)]) - ord("A")
            p = (c - k) % 26
            plain_char = chr(ord("A") + p)
            recovered_plain.append(plain_char)
            out.append(chr(base + p))
            i += 1
        else:
            out.append(ch)
    return "".join(out)
