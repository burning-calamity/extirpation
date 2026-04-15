"""A1Z26 substitution module."""

from __future__ import annotations


def a1z26_encrypt(plaintext: str) -> str:
    nums = [str(ord(ch.upper()) - 64) for ch in plaintext if ch.isalpha()]
    return '-'.join(nums)


def a1z26_decrypt(ciphertext: str) -> str:
    if not ciphertext.strip():
        return ''
    out = []
    for token in ciphertext.replace(' ', '-').split('-'):
        if not token:
            continue
        n = int(token)
        if not 1 <= n <= 26:
            raise ValueError('A1Z26 values must be 1..26')
        out.append(chr(64 + n))
    return ''.join(out)
