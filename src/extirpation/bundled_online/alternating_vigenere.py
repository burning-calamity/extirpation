"""Vigenere-like cipher that alternates add/subtract key shifts."""

from __future__ import annotations


def _shift(ch: str, amount: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + amount) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + amount) % 26))
    return ch


def _key_shifts(key: str) -> list[int]:
    shifts = [ord(ch.upper()) - ord("A") for ch in key if ch.isalpha()]
    if not shifts:
        raise ValueError("key must contain at least one alphabetic character")
    return shifts


def alternating_vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt alphabetic characters using alternating +/- key shifts."""
    shifts = _key_shifts(key)
    out: list[str] = []
    key_idx = 0
    direction = 1
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift(ch, direction * shifts[key_idx % len(shifts)]))
            key_idx += 1
            direction *= -1
        else:
            out.append(ch)
    return "".join(out)


def alternating_vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text from :func:`alternating_vigenere_encrypt`."""
    shifts = _key_shifts(key)
    out: list[str] = []
    key_idx = 0
    direction = 1
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift(ch, -direction * shifts[key_idx % len(shifts)]))
            key_idx += 1
            direction *= -1
        else:
            out.append(ch)
    return "".join(out)
