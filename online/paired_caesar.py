"""Paired Caesar cipher (alternating shifts) module."""

from __future__ import annotations


def paired_caesar_encrypt(plaintext: str, shift_a: int = 1, shift_b: int = 3) -> str:
    out = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = shift_a if i % 2 == 0 else shift_b
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr(base + ((ord(ch) - base + shift) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)


def paired_caesar_decrypt(ciphertext: str, shift_a: int = 1, shift_b: int = 3) -> str:
    out = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = shift_a if i % 2 == 0 else shift_b
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr(base + ((ord(ch) - base - shift) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)
