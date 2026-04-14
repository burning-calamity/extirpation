"""Polybius square cipher module (I/J combined)."""

from __future__ import annotations

SQUARE = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
POS = {ch: divmod(i, 5) for i, ch in enumerate(SQUARE)}
REV = {f"{r+1}{c+1}": ch for ch, (r, c) in POS.items()}


def polybius_encrypt(plaintext: str) -> str:
    out = []
    for ch in plaintext.upper():
        if ch == "J":
            ch = "I"
        if ch in POS:
            r, c = POS[ch]
            out.append(f"{r+1}{c+1}")
    return " ".join(out)


def polybius_decrypt(ciphertext: str) -> str:
    tokens = ciphertext.split()
    try:
        return "".join(REV[t] for t in tokens)
    except KeyError as exc:
        raise ValueError("ciphertext must contain valid Polybius tokens") from exc
