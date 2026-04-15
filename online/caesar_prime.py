"""Prime-step Caesar cipher."""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


def _primes(n: int) -> list[int]:
    out: list[int] = []
    x = 2
    while len(out) < n:
        for p in out:
            if x % p == 0:
                break
        else:
            out.append(x)
        x += 1
    return out


def caesar_prime_encrypt(plaintext: str, base_shift: int = 0) -> str:
    letters = [c for c in plaintext if c.isalpha()]
    primes = _primes(len(letters))
    out: list[str] = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift_char(ch, base_shift + primes[i]))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def caesar_prime_decrypt(ciphertext: str, base_shift: int = 0) -> str:
    letters = [c for c in ciphertext if c.isalpha()]
    primes = _primes(len(letters))
    out: list[str] = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift_char(ch, -(base_shift + primes[i])))
            i += 1
        else:
            out.append(ch)
    return "".join(out)
