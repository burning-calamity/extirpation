"""Chaocipher implementation."""

from __future__ import annotations

LEFT_DEFAULT = "HXUCZVAMDSLKPEFJRIGTWOBNYQ"
RIGHT_DEFAULT = "PTLNBQDEOYSFAVZKGJRIHWXUMC"


def _permute(left: list[str], right: list[str], idx: int) -> tuple[list[str], list[str]]:
    left = left[idx:] + left[:idx]
    pivot_left = left.pop(1)
    left.insert(13, pivot_left)

    right = right[idx:] + right[:idx]
    pivot_right = right.pop(2)
    right.insert(13, pivot_right)
    return left, right


def chaocipher_encrypt(
    plaintext: str,
    left_alphabet: str = LEFT_DEFAULT,
    right_alphabet: str = RIGHT_DEFAULT,
) -> str:
    """Encrypt with Chaocipher dynamic alphabets."""
    left = list(left_alphabet.upper())
    right = list(right_alphabet.upper())

    out: list[str] = []
    for ch in plaintext:
        up = ch.upper()
        if up not in right:
            out.append(ch)
            continue
        idx = right.index(up)
        cipher = left[idx]
        out.append(cipher if ch.isupper() else cipher.lower())
        left, right = _permute(left, right, idx)
    return ''.join(out)


def chaocipher_decrypt(
    ciphertext: str,
    left_alphabet: str = LEFT_DEFAULT,
    right_alphabet: str = RIGHT_DEFAULT,
) -> str:
    """Decrypt text produced by ``chaocipher_encrypt``."""
    left = list(left_alphabet.upper())
    right = list(right_alphabet.upper())

    out: list[str] = []
    for ch in ciphertext:
        up = ch.upper()
        if up not in left:
            out.append(ch)
            continue
        idx = left.index(up)
        plain = right[idx]
        out.append(plain if ch.isupper() else plain.lower())
        left, right = _permute(left, right, idx)
    return ''.join(out)
