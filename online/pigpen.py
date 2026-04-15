"""Pigpen-style substitution cipher using symbolic glyphs."""

from __future__ import annotations

PIG = {
    'A': '⟂', 'B': '⊢', 'C': '⊣', 'D': '⊤', 'E': '□', 'F': '⌜', 'G': '⌝', 'H': '⌞', 'I': '⌟',
    'J': '◰', 'K': '◳', 'L': '◲', 'M': '◱', 'N': '◇', 'O': '◆', 'P': '◈', 'Q': '◉', 'R': '◎',
    'S': '△', 'T': '▲', 'U': '▽', 'V': '▼', 'W': '○', 'X': '●', 'Y': '◌', 'Z': '◍',
}
REV = {v: k for k, v in PIG.items()}


def pigpen_encrypt(plaintext: str) -> str:
    """Encode plaintext letters into pigpen symbols."""
    out: list[str] = []
    for ch in plaintext:
        up = ch.upper()
        out.append(PIG.get(up, ch))
    return ''.join(out)


def pigpen_decrypt(ciphertext: str) -> str:
    """Decode text produced by ``pigpen_encrypt``."""
    out: list[str] = []
    for ch in ciphertext:
        out.append(REV.get(ch, ch))
    return ''.join(out)
