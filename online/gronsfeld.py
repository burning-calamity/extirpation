"""Gronsfeld cipher module (Vigenere with numeric key)."""

from __future__ import annotations


def _digits(key: str) -> list[int]:
    digs = [int(c) for c in key if c.isdigit()]
    if not digs:
        raise ValueError("key must contain at least one digit")
    return digs


def gronsfeld_encrypt(plaintext: str, key: str) -> str:
    ks = _digits(key)
    out = []
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            p = ord(ch) - base
            out.append(chr(base + ((p + ks[j % len(ks)]) % 26)))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def gronsfeld_decrypt(ciphertext: str, key: str) -> str:
    ks = _digits(key)
    out = []
    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            c = ord(ch) - base
            out.append(chr(base + ((c - ks[j % len(ks)]) % 26)))
            j += 1
        else:
            out.append(ch)
    return "".join(out)
