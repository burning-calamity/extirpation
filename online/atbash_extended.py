"""Atbash variant that mirrors letters and digits."""

from __future__ import annotations


def _map_char(ch: str) -> str:
    if "A" <= ch <= "Z":
        return chr(ord("Z") - (ord(ch) - ord("A")))
    if "a" <= ch <= "z":
        return chr(ord("z") - (ord(ch) - ord("a")))
    if "0" <= ch <= "9":
        return chr(ord("9") - (ord(ch) - ord("0")))
    return ch


def atbash_extended_encrypt(plaintext: str) -> str:
    """Apply Atbash to alphabetic characters and mirror digits."""
    return "".join(_map_char(ch) for ch in plaintext)


def atbash_extended_decrypt(ciphertext: str) -> str:
    """Decrypt Atbash-extended text (same transform as encrypt)."""
    return atbash_extended_encrypt(ciphertext)
