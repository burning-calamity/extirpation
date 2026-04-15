"""Word-wise Caesar cipher.

Applies Caesar shifts per word, incrementing shift by one per word.
"""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


def _transform(text: str, start_shift: int, direction: int) -> str:
    words = text.split(" ")
    out_words: list[str] = []
    for idx, word in enumerate(words):
        shift = direction * (start_shift + idx)
        out_words.append("".join(_shift_char(ch, shift) for ch in word))
    return " ".join(out_words)


def word_caesar_encrypt(plaintext: str, start_shift: int = 1) -> str:
    return _transform(plaintext, start_shift, direction=1)


def word_caesar_decrypt(ciphertext: str, start_shift: int = 1) -> str:
    return _transform(ciphertext, start_shift, direction=-1)
