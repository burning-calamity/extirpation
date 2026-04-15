"""XOR stream cipher module (hex output)."""

from __future__ import annotations


def xor_encrypt(plaintext: str, key: str, encoding: str = "utf-8") -> str:
    """Encrypt plaintext with repeating-key XOR and return hex string."""
    if not key:
        raise ValueError("key must not be empty")
    data = plaintext.encode(encoding)
    k = key.encode(encoding)
    out = bytes(b ^ k[i % len(k)] for i, b in enumerate(data))
    return out.hex()


def xor_decrypt(ciphertext_hex: str, key: str, encoding: str = "utf-8") -> str:
    """Decrypt repeating-key XOR hex string back to plaintext."""
    if not key:
        raise ValueError("key must not be empty")
    data = bytes.fromhex(ciphertext_hex)
    k = key.encode(encoding)
    out = bytes(b ^ k[i % len(k)] for i, b in enumerate(data))
    return out.decode(encoding)
