"""Running key cipher module."""

from __future__ import annotations


def _clean_key(key_text: str) -> str:
    k = ''.join(ch for ch in key_text.upper() if ch.isalpha())
    if not k:
        raise ValueError('key_text must contain alphabetic characters')
    return k


def running_key_encrypt(plaintext: str, key_text: str) -> str:
    key = _clean_key(key_text)
    out = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            if i >= len(key):
                raise ValueError('key_text must be at least as long as alphabetic plaintext')
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch.upper()) - ord('A')
            k = ord(key[i]) - ord('A')
            out.append(chr(base + ((p + k) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)


def running_key_decrypt(ciphertext: str, key_text: str) -> str:
    key = _clean_key(key_text)
    out = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            if i >= len(key):
                raise ValueError('key_text must be at least as long as alphabetic ciphertext')
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch.upper()) - ord('A')
            k = ord(key[i]) - ord('A')
            out.append(chr(base + ((c - k) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)
