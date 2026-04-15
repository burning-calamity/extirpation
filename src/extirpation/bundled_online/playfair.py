"""Playfair cipher module (I/J combined)."""

from __future__ import annotations


def _square(keyword: str) -> str:
    alpha = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key = ''.join(dict.fromkeys(ch for ch in keyword.upper().replace('J', 'I') if ch.isalpha()))
    return key + ''.join(ch for ch in alpha if ch not in key)


def _prep(text: str) -> list[str]:
    t = ''.join(ch for ch in text.upper() if ch.isalpha()).replace('J', 'I')
    pairs = []
    i = 0
    while i < len(t):
        a = t[i]
        b = t[i + 1] if i + 1 < len(t) else 'X'
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    if pairs and len(pairs[-1]) == 1:
        pairs[-1] += 'X'
    return pairs


def _pos(square: str, ch: str) -> tuple[int, int]:
    i = square.index(ch)
    return divmod(i, 5)


def playfair_encrypt(plaintext: str, keyword: str = 'MONARCHY') -> str:
    sq = _square(keyword)
    out = []
    for a, b in _prep(plaintext):
        ra, ca = _pos(sq, a)
        rb, cb = _pos(sq, b)
        if ra == rb:
            out.append(sq[ra * 5 + (ca + 1) % 5])
            out.append(sq[rb * 5 + (cb + 1) % 5])
        elif ca == cb:
            out.append(sq[((ra + 1) % 5) * 5 + ca])
            out.append(sq[((rb + 1) % 5) * 5 + cb])
        else:
            out.append(sq[ra * 5 + cb])
            out.append(sq[rb * 5 + ca])
    return ''.join(out)


def playfair_decrypt(ciphertext: str, keyword: str = 'MONARCHY') -> str:
    sq = _square(keyword)
    text = ''.join(ch for ch in ciphertext.upper() if ch.isalpha())
    if len(text) % 2:
        raise ValueError('ciphertext must contain an even number of letters')
    out = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        ra, ca = _pos(sq, a)
        rb, cb = _pos(sq, b)
        if ra == rb:
            out.append(sq[ra * 5 + (ca - 1) % 5])
            out.append(sq[rb * 5 + (cb - 1) % 5])
        elif ca == cb:
            out.append(sq[((ra - 1) % 5) * 5 + ca])
            out.append(sq[((rb - 1) % 5) * 5 + cb])
        else:
            out.append(sq[ra * 5 + cb])
            out.append(sq[rb * 5 + ca])
    return ''.join(out)
