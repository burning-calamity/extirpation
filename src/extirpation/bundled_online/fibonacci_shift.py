"""Fibonacci-based shift cipher."""

from __future__ import annotations


def _shift_char(ch: str, shift: int) -> str:
    if "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    return ch


def _fib_sequence(n: int) -> list[int]:
    if n <= 0:
        return []
    if n == 1:
        return [1]
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def fibonacci_shift_encrypt(plaintext: str, seed_shift: int = 0) -> str:
    letters = [ch for ch in plaintext if ch.isalpha()]
    fib = _fib_sequence(len(letters))
    out: list[str] = []
    idx = 0
    for ch in plaintext:
        if ch.isalpha():
            out.append(_shift_char(ch, seed_shift + fib[idx]))
            idx += 1
        else:
            out.append(ch)
    return "".join(out)


def fibonacci_shift_decrypt(ciphertext: str, seed_shift: int = 0) -> str:
    letters = [ch for ch in ciphertext if ch.isalpha()]
    fib = _fib_sequence(len(letters))
    out: list[str] = []
    idx = 0
    for ch in ciphertext:
        if ch.isalpha():
            out.append(_shift_char(ch, -(seed_shift + fib[idx])))
            idx += 1
        else:
            out.append(ch)
    return "".join(out)
