"""Morse code module."""

from __future__ import annotations

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}
REV_MORSE = {v: k for k, v in MORSE.items()}


def morse_encrypt(plaintext: str) -> str:
    """Encode plaintext into morse code, separating letters with spaces and words with /."""
    out_words = []
    for word in plaintext.upper().split():
        chars = [MORSE[ch] for ch in word if ch in MORSE]
        out_words.append(" ".join(chars))
    return " / ".join(out_words)


def morse_decrypt(ciphertext: str) -> str:
    """Decode morse code where words are separated by '/' and letters by spaces."""
    out_words = []
    for word in ciphertext.strip().split("/"):
        letters = []
        for token in word.strip().split():
            if token not in REV_MORSE:
                raise ValueError(f"invalid morse token: {token}")
            letters.append(REV_MORSE[token])
        out_words.append("".join(letters))
    return " ".join(out_words)
