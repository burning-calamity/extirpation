"""Progressive ROT cipher with per-character shift growth."""

from __future__ import annotations


def _shift_letter(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + shift) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + shift) % 26))
    return ch


def chained_rot_encrypt(plaintext: str, base_shift: int = 1) -> str:
    """Encrypt by shifting letters with ``base_shift + index`` progression."""
    out: list[str] = []
    letter_index = 0
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift_letter(ch, base_shift + letter_index))
            letter_index += 1
        else:
            out.append(ch)
    return "".join(out)


def chained_rot_decrypt(ciphertext: str, base_shift: int = 1) -> str:
    """Decrypt text encrypted by :func:`chained_rot_encrypt`."""
    out: list[str] = []
    letter_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift_letter(ch, -(base_shift + letter_index)))
            letter_index += 1
        else:
            out.append(ch)
    return "".join(out)
