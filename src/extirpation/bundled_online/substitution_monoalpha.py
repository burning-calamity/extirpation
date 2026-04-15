"""Monoalphabetic substitution cipher with custom key alphabet."""

from __future__ import annotations


ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_maps(key_alphabet: str) -> tuple[dict[str, str], dict[str, str]]:
    key = "".join(ch for ch in key_alphabet.upper() if ch.isalpha())
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("key_alphabet must contain 26 unique A-Z letters")
    enc = {plain: subst for plain, subst in zip(ALPHA_UPPER, key)}
    dec = {subst: plain for plain, subst in enc.items()}
    return enc, dec


def _translate(text: str, table: dict[str, str]) -> str:
    out: list[str] = []
    for ch in text:
        upper = ch.upper()
        if upper in table:
            repl = table[upper]
            out.append(repl if ch.isupper() else repl.lower())
        else:
            out.append(ch)
    return "".join(out)


def substitution_encrypt(
    plaintext: str,
    key_alphabet: str = "QWERTYUIOPASDFGHJKLZXCVBNM",
) -> str:
    enc, _ = _build_maps(key_alphabet)
    return _translate(plaintext, enc)


def substitution_decrypt(
    ciphertext: str,
    key_alphabet: str = "QWERTYUIOPASDFGHJKLZXCVBNM",
) -> str:
    _, dec = _build_maps(key_alphabet)
    return _translate(ciphertext, dec)
