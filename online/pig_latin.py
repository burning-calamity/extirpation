"""Pig Latin transform module (reversible for simple words)."""

from __future__ import annotations

VOWELS = set('AEIOUaeiou')


def pig_latin_encrypt(plaintext: str) -> str:
    out = []
    for word in plaintext.split():
        if not word.isalpha():
            out.append(word)
            continue
        if word[0] in VOWELS:
            out.append(word + 'yay')
        else:
            out.append(word[1:] + word[0] + 'ay')
    return ' '.join(out)


def pig_latin_decrypt(ciphertext: str) -> str:
    out = []
    for word in ciphertext.split():
        if word.endswith('yay'):
            out.append(word[:-3])
        elif word.endswith('ay') and len(word) >= 3:
            core = word[:-2]
            out.append(core[-1] + core[:-1])
        else:
            out.append(word)
    return ' '.join(out)
