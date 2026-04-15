"""Keyboard-shift substitution using QWERTY row neighbors."""

from __future__ import annotations

ROWS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']


def _build_shift(right: bool = True) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in ROWS:
        n = len(row)
        for i, ch in enumerate(row):
            j = (i + 1) % n if right else (i - 1) % n
            mapping[ch] = row[j]
    return mapping


def keyboard_shift_encrypt(plaintext: str, right: bool = True) -> str:
    """Shift letters to neighboring QWERTY keys."""
    m = _build_shift(right=right)
    out: list[str] = []
    for ch in plaintext:
        low = ch.lower()
        if low in m:
            rep = m[low]
            out.append(rep.upper() if ch.isupper() else rep)
        else:
            out.append(ch)
    return ''.join(out)


def keyboard_shift_decrypt(ciphertext: str, right: bool = True) -> str:
    """Decrypt text produced by ``keyboard_shift_encrypt``."""
    return keyboard_shift_encrypt(ciphertext, right=not right)
