"""Shift printable ASCII characters by a configurable offset."""

from __future__ import annotations

_ASCII_START = 32
_ASCII_END = 126
_ASCII_SPAN = _ASCII_END - _ASCII_START + 1


def _shift_printable_ascii(text: str, shift: int) -> str:
    out: list[str] = []
    for ch in text:
        code = ord(ch)
        if _ASCII_START <= code <= _ASCII_END:
            out.append(chr(_ASCII_START + ((code - _ASCII_START + shift) % _ASCII_SPAN)))
        else:
            out.append(ch)
    return "".join(out)


def ascii_shift_encrypt(plaintext: str, shift: int = 1) -> str:
    """Encrypt by rotating printable ASCII codepoints."""
    return _shift_printable_ascii(plaintext, shift)


def ascii_shift_decrypt(ciphertext: str, shift: int = 1) -> str:
    """Decrypt printable ASCII-shifted text."""
    return _shift_printable_ascii(ciphertext, -shift)
