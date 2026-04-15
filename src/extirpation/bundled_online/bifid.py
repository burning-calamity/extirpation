"""Bifid cipher module (period-based Polybius fractionation)."""

from __future__ import annotations

SQUARE = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
POS = {ch: divmod(i, 5) for i, ch in enumerate(SQUARE)}
REV = {(r, c): ch for ch, (r, c) in POS.items()}


def _normalize(text: str) -> str:
    t = "".join(ch for ch in text.upper() if ch.isalpha())
    return t.replace("J", "I")


def bifid_encrypt(plaintext: str, period: int = 5) -> str:
    text = _normalize(plaintext)
    out = []
    for i in range(0, len(text), period):
        chunk = text[i : i + period]
        rows = [POS[ch][0] for ch in chunk]
        cols = [POS[ch][1] for ch in chunk]
        merged = rows + cols
        for j in range(0, len(merged), 2):
            out.append(REV[(merged[j], merged[j + 1])])
    return "".join(out)


def bifid_decrypt(ciphertext: str, period: int = 5) -> str:
    text = _normalize(ciphertext)
    out = []
    for i in range(0, len(text), period):
        chunk = text[i : i + period]
        pairs = [POS[ch] for ch in chunk]
        coords = [n for pair in pairs for n in pair]
        half = len(coords) // 2
        rows = coords[:half]
        cols = coords[half:]
        for r, c in zip(rows, cols):
            out.append(REV[(r, c)])
    return "".join(out)
