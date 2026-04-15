"""Vigenere variant with per-position key rotation."""

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


def vigenere_autorotate_encrypt(plaintext: str, key: str) -> str:
    """Encrypt with Vigenere where each key use adds the character index."""
    key_vals = _key_shifts(key)
    out: list[str] = []
    idx = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = key_vals[idx % len(key_vals)] + idx
            out.append(_shift(ch, shift))
            idx += 1
        else:
            out.append(ch)
    return "".join(out)


def vigenere_autorotate_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text from :func:`vigenere_autorotate_encrypt`."""
    key_vals = _key_shifts(key)
    out: list[str] = []
    idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = key_vals[idx % len(key_vals)] + idx
            out.append(_shift(ch, -shift))
            idx += 1
        else:
            out.append(ch)
    return "".join(out)
