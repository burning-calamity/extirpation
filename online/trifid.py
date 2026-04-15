"""Trifid cipher implementation using a 3x3x3 polybius cube."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ.'


def _normalize(text: str) -> str:
    out: list[str] = []
    for ch in text.upper():
        if ch == ' ':
            out.append('.')
        elif ch in ALPHABET:
            out.append(ch)
    return ''.join(out)


def _coord_map(key: str = '') -> tuple[str, dict[str, tuple[int, int, int]]]:
    seen: set[str] = set()
    ordered: list[str] = []
    for ch in (_normalize(key) + ALPHABET):
        if ch in ALPHABET and ch not in seen:
            seen.add(ch)
            ordered.append(ch)
    cube = ''.join(ordered)
    mapping: dict[str, tuple[int, int, int]] = {}
    for i, ch in enumerate(cube):
        a = i // 9
        b = (i % 9) // 3
        c = i % 3
        mapping[ch] = (a, b, c)
    return cube, mapping


def trifid_encrypt(plaintext: str, key: str = '') -> str:
    """Encrypt text with the Trifid fractionation process."""
    text = _normalize(plaintext)
    cube, mapping = _coord_map(key)
    if not text:
        return ''

    rows1: list[int] = []
    rows2: list[int] = []
    rows3: list[int] = []
    for ch in text:
        a, b, c = mapping[ch]
        rows1.append(a)
        rows2.append(b)
        rows3.append(c)

    merged = rows1 + rows2 + rows3
    out: list[str] = []
    for i in range(0, len(merged), 3):
        a, b, c = merged[i:i + 3]
        idx = a * 9 + b * 3 + c
        out.append(cube[idx])
    return ''.join(out)


def trifid_decrypt(ciphertext: str, key: str = '') -> str:
    """Decrypt text produced by ``trifid_encrypt``."""
    text = _normalize(ciphertext)
    cube, mapping = _coord_map(key)
    if not text:
        return ''

    coords: list[int] = []
    for ch in text:
        a, b, c = mapping[ch]
        coords.extend((a, b, c))

    n = len(text)
    row1 = coords[:n]
    row2 = coords[n:2 * n]
    row3 = coords[2 * n:]

    out: list[str] = []
    for i in range(n):
        idx = row1[i] * 9 + row2[i] * 3 + row3[i]
        out.append(cube[idx])
    return ''.join(out)
