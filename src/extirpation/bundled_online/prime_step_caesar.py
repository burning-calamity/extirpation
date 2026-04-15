"""Caesar-style cipher with prime-number step progression."""

from __future__ import annotations


def _shift(ch: str, amount: int) -> str:
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + amount) % 26))
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + amount) % 26))
    return ch


def _first_primes(n: int) -> list[int]:
    primes: list[int] = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


def prime_step_caesar_encrypt(plaintext: str) -> str:
    """Encrypt each alphabetic character using successive prime shifts."""
    letters = sum(1 for ch in plaintext if ch.isalpha())
    primes = _first_primes(letters)
    out: list[str] = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift(ch, primes[i]))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def prime_step_caesar_decrypt(ciphertext: str) -> str:
    """Decrypt text from :func:`prime_step_caesar_encrypt`."""
    letters = sum(1 for ch in ciphertext if ch.isalpha())
    primes = _first_primes(letters)
    out: list[str] = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift(ch, -primes[i]))
            i += 1
        else:
            out.append(ch)
    return "".join(out)
