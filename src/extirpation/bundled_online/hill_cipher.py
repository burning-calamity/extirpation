"""2x2 Hill cipher (A-Z) implementation."""

from __future__ import annotations


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _clean_letters(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch.isalpha())


def _pairwise(text: str) -> list[tuple[int, int]]:
    values = [ord(ch) - ord("A") for ch in text]
    if len(values) % 2 == 1:
        values.append(ord("X") - ord("A"))
    return [(values[i], values[i + 1]) for i in range(0, len(values), 2)]


def _det(key: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return key[0][0] * key[1][1] - key[0][1] * key[1][0]


def _mod_inverse(a: int, m: int) -> int:
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("key determinant is not invertible modulo 26")


def _invert_key(key: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    det = _det(key)
    inv_det = _mod_inverse(det, 26)
    a, b = key[0]
    c, d = key[1]
    return (
        ((d * inv_det) % 26, (-b * inv_det) % 26),
        ((-c * inv_det) % 26, (a * inv_det) % 26),
    )


def _transform(text: str, key: tuple[tuple[int, int], tuple[int, int]]) -> str:
    cleaned = _clean_letters(text)
    out: list[str] = []
    for x, y in _pairwise(cleaned):
        a, b = key[0]
        c, d = key[1]
        out.append(ALPHABET[(a * x + b * y) % 26])
        out.append(ALPHABET[(c * x + d * y) % 26])
    return "".join(out)


def hill_encrypt(plaintext: str, key: tuple[tuple[int, int], tuple[int, int]] = ((3, 3), (2, 5))) -> str:
    """Encrypt letters using a 2x2 Hill key matrix."""
    return _transform(plaintext, key)


def hill_decrypt(ciphertext: str, key: tuple[tuple[int, int], tuple[int, int]] = ((3, 3), (2, 5))) -> str:
    """Decrypt letters using inverse of the 2x2 Hill key matrix."""
    inv_key = _invert_key(key)
    return _transform(ciphertext, inv_key)
