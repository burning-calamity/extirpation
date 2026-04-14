"""Trithemius cipher module (progressive Caesar)."""

from __future__ import annotations


def trithemius_encrypt(plaintext: str) -> str:
    out = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr(base + ((ord(ch) - base + i) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)


def trithemius_decrypt(ciphertext: str) -> str:
    out = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr(base + ((ord(ch) - base - i) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)
