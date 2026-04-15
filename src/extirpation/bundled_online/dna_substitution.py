"""Toy DNA substitution cipher using fixed 2-bit encoding."""

from __future__ import annotations

_BITS_TO_BASE = {"00": "A", "01": "C", "10": "G", "11": "T"}
_BASE_TO_BITS = {v: k for k, v in _BITS_TO_BASE.items()}


def dna_substitution_encrypt(plaintext: str) -> str:
    """Encode UTF-8 bytes into a DNA alphabet (A/C/G/T)."""
    bits = "".join(f"{byte:08b}" for byte in plaintext.encode("utf-8"))
    return "".join(_BITS_TO_BASE[bits[i : i + 2]] for i in range(0, len(bits), 2))


def dna_substitution_decrypt(ciphertext: str) -> str:
    """Decode DNA alphabet text created by :func:`dna_substitution_encrypt`."""
    normalized = "".join(ch for ch in ciphertext.upper() if not ch.isspace())
    if any(ch not in _BASE_TO_BITS for ch in normalized):
        raise ValueError("ciphertext must contain only A/C/G/T (whitespace allowed)")
    if len(normalized) % 4 != 0:
        raise ValueError("ciphertext length must be a multiple of 4 bases")
    bits = "".join(_BASE_TO_BITS[ch] for ch in normalized)
    raw = bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))
    return raw.decode("utf-8")
