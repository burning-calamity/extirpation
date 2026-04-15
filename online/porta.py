"""Porta cipher module (reciprocal polyalphabetic substitution)."""

from __future__ import annotations

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PAIRS = ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV", "WX", "YZ"]
TABLE = {
    0: "NOPQRSTUVWXYZABCDEFGHIJKLM",
    1: "OPQRSTUVWXYZNMABCDEFGHIJKL",
    2: "PQRSTUVWXYZNOMABCDEFGHIJKL",
    3: "QRSTUVWXYZNOPMABCDEFGHIJKL",
    4: "RSTUVWXYZNOPQMABCDEFGHIJKL",
    5: "STUVWXYZNOPQRMABCDEFGHIJKL",
    6: "TUVWXYZNOPQRSMABCDEFGHIJKL",
    7: "UVWXYZNOPQRSTMABCDEFGHIJKL",
    8: "VWXYZNOPQRSTUMABCDEFGHIJKL",
    9: "WXYZNOPQRSTUVMABCDEFGHIJKL",
    10: "XYZNOPQRSTUVWMABCDEFGHIJKL",
    11: "YZNOPQRSTUVWXMABCDEFGHIJKL",
    12: "ZNOPQRSTUVWXYMABCDEFGHIJKL",
}


def _pair_index(ch: str) -> int:
    for i, pair in enumerate(PAIRS):
        if ch in pair:
            return i
    raise ValueError("invalid key character")


def porta_encrypt(plaintext: str, key: str) -> str:
    cleaned_key = "".join(c for c in key.upper() if c.isalpha())
    if not cleaned_key:
        raise ValueError("key must contain alphabetic characters")
    out = []
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            upper = ch.upper()
            row = TABLE[_pair_index(cleaned_key[j % len(cleaned_key)])]
            idx = ALPHABET.index(upper)
            mapped = row[idx]
            out.append(mapped if ch.isupper() else mapped.lower())
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def porta_decrypt(ciphertext: str, key: str) -> str:
    """Porta is reciprocal, so decrypt is same as encrypt."""
    return porta_encrypt(ciphertext, key)
