"""Caesar-style cipher using Fibonacci shifts per letter."""

from __future__ import annotations


def _fib(n: int) -> list[int]:
    seq = [1, 1]
    while len(seq) < n:
        seq.append((seq[-1] + seq[-2]) % 26)
    return seq[:n]


def fibonacci_caesar_encrypt(plaintext: str) -> str:
    """Encrypt with shifts 1,1,2,3,5,... applied to alphabetic chars."""
    letters = sum(1 for c in plaintext if c.isalpha())
    fib = _fib(letters)
    out: list[str] = []
    i = 0
    for ch in plaintext:
        if ch.isalpha():
            s = fib[i] % 26
            base = ord('A') if ch.isupper() else ord('a')
            p = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((p + s) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)


def fibonacci_caesar_decrypt(ciphertext: str) -> str:
    """Decrypt text produced by ``fibonacci_caesar_encrypt``."""
    letters = sum(1 for c in ciphertext if c.isalpha())
    fib = _fib(letters)
    out: list[str] = []
    i = 0
    for ch in ciphertext:
        if ch.isalpha():
            s = fib[i] % 26
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch.upper()) - ord('A')
            out.append(chr(base + ((c - s) % 26)))
            i += 1
        else:
            out.append(ch)
    return ''.join(out)
