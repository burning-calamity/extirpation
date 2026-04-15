"""Toy Feistel network over byte pairs (educational only)."""

from __future__ import annotations

import base64


def _f(r: int, k: int) -> int:
    return ((r + k) & 0xFF) ^ ((r << 1) & 0xFF)


def _round_keys(seed: int, rounds: int) -> list[int]:
    x = seed & 0xFFFFFFFF
    keys: list[int] = []
    for _ in range(rounds):
        x = (1103515245 * x + 12345) & 0x7FFFFFFF
        keys.append(x & 0xFF)
    return keys


def feistel_toy_encrypt(plaintext: str, rounds: int = 8, seed: int = 1337) -> str:
    """Encrypt UTF-8 plaintext into base64 ciphertext."""
    data = bytearray(plaintext.encode('utf-8'))
    if len(data) % 2:
        data.append(0)

    keys = _round_keys(seed, rounds)
    out = bytearray()
    for i in range(0, len(data), 2):
        l, r = data[i], data[i + 1]
        for k in keys:
            l, r = r, l ^ _f(r, k)
        out.extend((l, r))
    return base64.b64encode(bytes(out)).decode('ascii')


def feistel_toy_decrypt(ciphertext: str, rounds: int = 8, seed: int = 1337) -> str:
    """Decrypt text produced by ``feistel_toy_encrypt``."""
    data = bytearray(base64.b64decode(ciphertext.encode('ascii')))
    keys = _round_keys(seed, rounds)

    out = bytearray()
    for i in range(0, len(data), 2):
        l, r = data[i], data[i + 1]
        for k in reversed(keys):
            l, r = r ^ _f(l, k), l
        out.extend((l, r))

    while out and out[-1] == 0:
        out.pop()
    return out.decode('utf-8')
