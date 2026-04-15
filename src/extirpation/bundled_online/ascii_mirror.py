"""Mirror printable ASCII characters across the printable range."""

from __future__ import annotations

_START = 32
_END = 126


def _mirror(ch: str) -> str:
    code = ord(ch)
    if _START <= code <= _END:
        return chr(_START + (_END - code))
    return ch


def ascii_mirror_encrypt(plaintext: str) -> str:
    """Encrypt by mirroring printable ASCII characters."""
    return "".join(_mirror(ch) for ch in plaintext)


def ascii_mirror_decrypt(ciphertext: str) -> str:
    """Decrypt text from :func:`ascii_mirror_encrypt` (same transform)."""
    return ascii_mirror_encrypt(ciphertext)
