"""Jefferson-disk inspired wheel-shift cipher."""

from __future__ import annotations

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def _sanitize_wheels(wheels: tuple[int, ...] | list[int] | None) -> list[int]:
    if not wheels:
        return [3, 1, 4, 1, 5]
    vals = [int(x) % 26 for x in wheels]
    return vals or [0]


def _shift(ch: str, amount: int) -> str:
    if ch.upper() not in ALPHABET:
        return ch
    idx = ALPHABET.index(ch.upper())
    out = ALPHABET[(idx + amount) % 26]
    return out if ch.isupper() else out.lower()


def jefferson_disk_encrypt(plaintext: str, wheels: tuple[int, ...] | list[int] | None = None) -> str:
    """Encrypt text using repeating wheel shifts."""
    wheel = _sanitize_wheels(wheels)
    out: list[str] = []
    i = 0
    for ch in plaintext:
        if ch.upper() in ALPHABET:
            out.append(_shift(ch, wheel[i % len(wheel)]))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)


def jefferson_disk_decrypt(ciphertext: str, wheels: tuple[int, ...] | list[int] | None = None) -> str:
    """Decrypt text produced by ``jefferson_disk_encrypt``."""
    wheel = _sanitize_wheels(wheels)
    out: list[str] = []
    i = 0
    for ch in ciphertext:
        if ch.upper() in ALPHABET:
            out.append(_shift(ch, -wheel[i % len(wheel)]))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)
