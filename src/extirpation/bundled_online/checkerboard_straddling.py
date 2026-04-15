"""Straddling checkerboard substitution cipher."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def _dedupe(text: str) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for ch in text:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return ''.join(out)


def _build_checkerboard(keyword: str, row_digits: tuple[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    if len(row_digits) != 2 or row_digits[0] == row_digits[1]:
        raise ValueError('row_digits must contain exactly two distinct digits')

    top_digits = [d for d in '0123456789' if d not in row_digits]
    ordered = _dedupe(''.join(ch for ch in keyword.upper() if ch.isalpha()) + ALPHABET + ' ')

    enc: dict[str, str] = {}
    dec: dict[str, str] = {}

    first_row = ordered[: len(top_digits)]
    rest = ordered[len(top_digits) :]

    for d, ch in zip(top_digits, first_row):
        enc[ch] = d
        dec[d] = ch

    for row_idx, row_digit in enumerate(row_digits):
        row_chars = rest[row_idx * 10 : (row_idx + 1) * 10]
        for col_digit, ch in enumerate(row_chars):
            code = f'{row_digit}{col_digit}'
            enc[ch] = code
            dec[code] = ch

    return enc, dec


def checkerboard_straddling_encrypt(plaintext: str, keyword: str = 'CIPHER', row_digits: tuple[str, str] = ('3', '7')) -> str:
    """Encrypt text into checkerboard digits."""
    enc, _ = _build_checkerboard(keyword, row_digits)
    out: list[str] = []
    for ch in plaintext.upper():
        if ch.isalpha() or ch == ' ':
            out.append(enc[ch])
    return ' '.join(out)


def checkerboard_straddling_decrypt(ciphertext: str, keyword: str = 'CIPHER', row_digits: tuple[str, str] = ('3', '7')) -> str:
    """Decrypt text produced by ``checkerboard_straddling_encrypt``."""
    _, dec = _build_checkerboard(keyword, row_digits)
    tokens = [t for t in ciphertext.split() if t]

    out: list[str] = []
    for tok in tokens:
        if tok in dec:
            out.append(dec[tok])
            continue
        raise ValueError(f'invalid checkerboard token: {tok}')
    return ''.join(out)
