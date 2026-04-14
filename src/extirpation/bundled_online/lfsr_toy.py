"""Toy LFSR-based stream cipher (educational only)."""

from __future__ import annotations

import base64


def _lfsr_stream(seed: int, taps: tuple[int, ...], nbits: int, nbytes: int) -> bytes:
    if seed <= 0:
        raise ValueError('seed must be positive')
    state = seed & ((1 << nbits) - 1)
    if state == 0:
        state = 1

    out = bytearray()
    for _ in range(nbytes):
        b = 0
        for _ in range(8):
            bit = state & 1
            b = (b << 1) | bit
            feedback = 0
            for t in taps:
                feedback ^= (state >> t) & 1
            state = (state >> 1) | (feedback << (nbits - 1))
        out.append(b)
    return bytes(out)


def lfsr_toy_encrypt(
    plaintext: str,
    seed: int = 0b101001001011,
    taps: tuple[int, ...] = (0, 2, 3, 5),
    nbits: int = 12,
) -> str:
    """Encrypt plaintext with XOR against an LFSR keystream; return base64."""
    data = plaintext.encode('utf-8')
    key = _lfsr_stream(seed, taps, nbits, len(data))
    raw = bytes(a ^ b for a, b in zip(data, key))
    return base64.b64encode(raw).decode('ascii')


def lfsr_toy_decrypt(
    ciphertext: str,
    seed: int = 0b101001001011,
    taps: tuple[int, ...] = (0, 2, 3, 5),
    nbits: int = 12,
) -> str:
    """Decrypt text produced by ``lfsr_toy_encrypt``."""
    data = base64.b64decode(ciphertext.encode('ascii'))
    key = _lfsr_stream(seed, taps, nbits, len(data))
    raw = bytes(a ^ b for a, b in zip(data, key))
    return raw.decode('utf-8')
