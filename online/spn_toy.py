"""Toy substitution-permutation network (educational only)."""

from __future__ import annotations

import base64

SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
INV_SBOX = [0] * 16
for i, v in enumerate(SBOX):
    INV_SBOX[v] = i


def _sub_byte(b: int, inv: bool = False) -> int:
    box = INV_SBOX if inv else SBOX
    lo = box[b & 0x0F]
    hi = box[(b >> 4) & 0x0F]
    return (hi << 4) | lo


def _permute_byte(b: int) -> int:
    return ((b & 0x0F) << 4) | ((b >> 4) & 0x0F)


def _round_keys(seed: int, rounds: int) -> list[int]:
    x = seed & 0xFFFFFFFF
    keys: list[int] = []
    for _ in range(rounds + 1):
        x = (1664525 * x + 1013904223) & 0xFFFFFFFF
        keys.append(x & 0xFF)
    return keys


def spn_toy_encrypt(plaintext: str, rounds: int = 6, seed: int = 2026) -> str:
    """Encrypt UTF-8 plaintext and return base64."""
    data = bytearray(plaintext.encode('utf-8'))
    keys = _round_keys(seed, rounds)

    out = bytearray()
    for b in data:
        x = b
        for r in range(rounds):
            x ^= keys[r]
            x = _sub_byte(x, inv=False)
            x = _permute_byte(x)
        x ^= keys[rounds]
        out.append(x)
    return base64.b64encode(bytes(out)).decode('ascii')


def spn_toy_decrypt(ciphertext: str, rounds: int = 6, seed: int = 2026) -> str:
    """Decrypt text produced by ``spn_toy_encrypt``."""
    data = bytearray(base64.b64decode(ciphertext.encode('ascii')))
    keys = _round_keys(seed, rounds)

    out = bytearray()
    for b in data:
        x = b ^ keys[rounds]
        for r in reversed(range(rounds)):
            x = _permute_byte(x)
            x = _sub_byte(x, inv=True)
            x ^= keys[r]
        out.append(x)
    return out.decode('utf-8')
