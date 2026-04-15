"""Fractionated Morse cipher."""

from __future__ import annotations

MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
}
REV_MORSE = {v: k for k, v in MORSE.items()}
TRIPLETS = [a + b + c for a in '.-x' for b in '.-x' for c in '.-x']


def _keyed_alphabet(key: str = '') -> str:
    base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ?'
    seen: set[str] = set()
    out: list[str] = []
    for ch in (key.upper() + base):
        if ch in base and ch not in seen:
            seen.add(ch)
            out.append(ch)
    return ''.join(out)


def fractionated_morse_encrypt(plaintext: str, key: str = '') -> str:
    """Encrypt using fractionated Morse triplets."""
    alpha = _keyed_alphabet(key)
    enc_map = {TRIPLETS[i]: alpha[i] for i in range(27)}

    stream: list[str] = []
    words = plaintext.upper().split()
    for wi, word in enumerate(words):
        for li, ch in enumerate(word):
            code = MORSE.get(ch)
            if not code:
                continue
            stream.append(code)
            if li < len(word) - 1:
                stream.append('x')
        if wi < len(words) - 1:
            stream.append('xx')

    raw = ''.join(stream)
    while len(raw) % 3:
        raw += 'x'

    out: list[str] = []
    for i in range(0, len(raw), 3):
        out.append(enc_map[raw[i:i + 3]])
    return ''.join(out)


def fractionated_morse_decrypt(ciphertext: str, key: str = '') -> str:
    """Decrypt text produced by ``fractionated_morse_encrypt``."""
    alpha = _keyed_alphabet(key)
    dec_map = {alpha[i]: TRIPLETS[i] for i in range(27)}

    raw = ''.join(dec_map[ch] for ch in ciphertext.upper() if ch in dec_map).rstrip('x')
    out_words: list[str] = []
    for word_code in raw.split('xx'):
        letters: list[str] = []
        for token in word_code.split('x'):
            if token:
                letters.append(REV_MORSE.get(token, '?'))
        if letters:
            out_words.append(''.join(letters))
    return ' '.join(out_words)
