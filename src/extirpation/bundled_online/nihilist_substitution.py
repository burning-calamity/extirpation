"""Nihilist substitution cipher (Polybius + additive key)."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'


def _normalize(text: str) -> str:
    return ''.join(('I' if ch == 'J' else ch) for ch in text.upper() if ch.isalpha())


def _keyed_square(keyword: str = '') -> str:
    seen: set[str] = set()
    out: list[str] = []
    for ch in _normalize(keyword) + ALPHABET:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return ''.join(out)


def _polybius_num(square: str, ch: str) -> int:
    idx = square.index(ch)
    r, c = divmod(idx, 5)
    return (r + 1) * 10 + (c + 1)


def nihilist_substitution_encrypt(plaintext: str, square_keyword: str = '', key: str = 'KEY') -> str:
    """Encrypt into space-separated integers."""
    square = _keyed_square(square_keyword)
    p = _normalize(plaintext)
    k = _normalize(key) or 'A'

    key_nums = [_polybius_num(square, ch) for ch in k]
    out: list[str] = []
    for i, ch in enumerate(p):
        n = _polybius_num(square, ch) + key_nums[i % len(key_nums)]
        out.append(str(n))
    return ' '.join(out)


def nihilist_substitution_decrypt(ciphertext: str, square_keyword: str = '', key: str = 'KEY') -> str:
    """Decrypt text produced by ``nihilist_substitution_encrypt``."""
    square = _keyed_square(square_keyword)
    k = _normalize(key) or 'A'
    key_nums = [_polybius_num(square, ch) for ch in k]

    nums = [int(tok) for tok in ciphertext.split() if tok.strip()]
    out: list[str] = []
    for i, n in enumerate(nums):
        base = n - key_nums[i % len(key_nums)]
        r = base // 10 - 1
        c = base % 10 - 1
        out.append(square[r * 5 + c])
    return ''.join(out)
