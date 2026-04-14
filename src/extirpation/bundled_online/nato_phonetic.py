"""NATO phonetic alphabet transform."""

from __future__ import annotations

NATO = {
    'A': 'ALFA', 'B': 'BRAVO', 'C': 'CHARLIE', 'D': 'DELTA', 'E': 'ECHO', 'F': 'FOXTROT',
    'G': 'GOLF', 'H': 'HOTEL', 'I': 'INDIA', 'J': 'JULIETT', 'K': 'KILO', 'L': 'LIMA',
    'M': 'MIKE', 'N': 'NOVEMBER', 'O': 'OSCAR', 'P': 'PAPA', 'Q': 'QUEBEC', 'R': 'ROMEO',
    'S': 'SIERRA', 'T': 'TANGO', 'U': 'UNIFORM', 'V': 'VICTOR', 'W': 'WHISKEY',
    'X': 'XRAY', 'Y': 'YANKEE', 'Z': 'ZULU',
}
REV = {v: k for k, v in NATO.items()}


def nato_phonetic_encrypt(plaintext: str) -> str:
    """Encode letters as NATO words; preserve unknown chars as-is."""
    out: list[str] = []
    for ch in plaintext:
        if ch.upper() in NATO:
            out.append(NATO[ch.upper()])
        elif ch == ' ':
            out.append('/')
        else:
            out.append(ch)
    return ' '.join(out)


def nato_phonetic_decrypt(ciphertext: str) -> str:
    """Decode text produced by ``nato_phonetic_encrypt``."""
    out: list[str] = []
    for tok in ciphertext.split():
        up = tok.upper()
        if up == '/':
            out.append(' ')
        elif up in REV:
            out.append(REV[up])
        else:
            out.append(tok)
    return ''.join(out)
