"""Simple reversible leetspeak substitution."""

from __future__ import annotations


ENC_MAP = str.maketrans({"A": "4", "E": "3", "I": "1", "O": "0", "S": "5", "T": "7"})
DEC_MAP = str.maketrans({"4": "A", "3": "E", "1": "I", "0": "O", "5": "S", "7": "T"})


def leetspeak_encrypt(plaintext: str) -> str:
    return plaintext.upper().translate(ENC_MAP)


def leetspeak_decrypt(ciphertext: str) -> str:
    return ciphertext.upper().translate(DEC_MAP)
