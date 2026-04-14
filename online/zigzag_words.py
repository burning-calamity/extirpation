"""Zigzag word transposition cipher."""

from __future__ import annotations


def zigzag_words_encrypt(plaintext: str) -> str:
    words = plaintext.split(" ")
    evens = words[::2]
    odds = words[1::2]
    return " ".join(evens + odds)


def zigzag_words_decrypt(ciphertext: str) -> str:
    words = ciphertext.split(" ")
    even_count = (len(words) + 1) // 2
    evens = words[:even_count]
    odds = words[even_count:]
    out: list[str] = []
    for i in range(even_count):
        out.append(evens[i])
        if i < len(odds):
            out.append(odds[i])
    return " ".join(out)
