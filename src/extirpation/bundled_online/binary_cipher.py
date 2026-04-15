"""Binary text encoding/decoding module."""

from __future__ import annotations


def binary_encrypt(plaintext: str, encoding: str = "utf-8") -> str:
    """Encode plaintext bytes as space-separated 8-bit binary values."""
    data = plaintext.encode(encoding)
    return " ".join(format(byte, "08b") for byte in data)


def binary_decrypt(binary_text: str, encoding: str = "utf-8") -> str:
    """Decode space-separated 8-bit binary values back to text."""
    tokens = [token for token in binary_text.split() if token]
    if any(len(token) != 8 or set(token) - {"0", "1"} for token in tokens):
        raise ValueError("binary_text must be whitespace-separated 8-bit binary tokens")
    data = bytes(int(token, 2) for token in tokens)
    return data.decode(encoding)
