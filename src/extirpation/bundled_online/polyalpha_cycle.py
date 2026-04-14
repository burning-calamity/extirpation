"""Polyalphabetic cycle cipher using integer shift sequence."""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


def _transform(text: str, shifts: tuple[int, ...], direction: int) -> str:
    if not shifts:
        raise ValueError("shifts must be non-empty")
    out: list[str] = []
    idx = 0
    for ch in text:
        if ch.isalpha():
            shift = direction * shifts[idx % len(shifts)]
            idx += 1
            out.append(_shift_char(ch, shift))
        else:
            out.append(ch)
    return "".join(out)


def polyalpha_cycle_encrypt(plaintext: str, shifts: tuple[int, ...] = (3, 1, 4, 1, 5)) -> str:
    return _transform(plaintext, shifts, direction=1)


def polyalpha_cycle_decrypt(ciphertext: str, shifts: tuple[int, ...] = (3, 1, 4, 1, 5)) -> str:
    return _transform(ciphertext, shifts, direction=-1)
