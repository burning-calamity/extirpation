"""Vigenère cipher module."""

from __future__ import annotations


def _alpha_index(ch: str) -> int:
    return ord(ch.upper()) - ord("A")


def _shift_char(ch: str, key_shift: int, encrypt: bool) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
    elif "a" <= ch <= "z":
        base = ord("a")
    else:
        return ch

    delta = key_shift if encrypt else -key_shift
    return chr((ord(ch) - base + delta) % 26 + base)


def _clean_key(key: str) -> str:
    cleaned = "".join(ch for ch in key.upper() if "A" <= ch <= "Z")
    if not cleaned:
        raise ValueError("key must contain at least one alphabetic character")
    return cleaned


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt text with the Vigenère cipher."""
    cleaned_key = _clean_key(key)
    out: list[str] = []
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = _alpha_index(cleaned_key[j % len(cleaned_key)])
            out.append(_shift_char(ch, shift, encrypt=True))
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt text encrypted with the Vigenère cipher."""
    cleaned_key = _clean_key(key)
    out: list[str] = []
    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = _alpha_index(cleaned_key[j % len(cleaned_key)])
            out.append(_shift_char(ch, shift, encrypt=False))
            j += 1
        else:
            out.append(ch)
    return "".join(out)
