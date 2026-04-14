"""Base32 encoding cipher."""

from __future__ import annotations

import base64


def base32_encrypt(plaintext: str) -> str:
    return base64.b32encode(plaintext.encode("utf-8")).decode("ascii")


def base32_decrypt(ciphertext: str) -> str:
    return base64.b32decode(ciphertext.encode("ascii")).decode("utf-8")
