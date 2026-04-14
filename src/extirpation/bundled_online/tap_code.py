"""Tap code cipher module (Polybius-style I/J combined)."""

from __future__ import annotations

SQUARE = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
POS = {ch: divmod(i, 5) for i, ch in enumerate(SQUARE)}
REV = {(r, c): ch for ch, (r, c) in POS.items()}


def tap_encrypt(plaintext: str) -> str:
    out = []
    for ch in plaintext.upper():
        if ch == 'J':
            ch = 'I'
        if ch in POS:
            r, c = POS[ch]
            out.append('.' * (r + 1) + ' ' + '.' * (c + 1))
    return ' / '.join(out)


def tap_decrypt(ciphertext: str) -> str:
    out = []
    for token in ciphertext.split('/'):
        token = token.strip()
        if not token:
            continue
        parts = token.split()
        if len(parts) != 2:
            raise ValueError('invalid tap code token')
        r = len(parts[0]) - 1
        c = len(parts[1]) - 1
        out.append(REV[(r, c)])
    return ''.join(out)
