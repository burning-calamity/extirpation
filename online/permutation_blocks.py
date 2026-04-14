"""Block permutation cipher."""

from __future__ import annotations


def _validate_perm(perm: tuple[int, ...]) -> None:
    if not perm:
        raise ValueError("permutation must be non-empty")
    n = len(perm)
    if set(perm) != set(range(n)):
        raise ValueError("permutation must contain each index exactly once")


def _inverse_perm(perm: tuple[int, ...]) -> tuple[int, ...]:
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p] = i
    return tuple(inv)


def _transform(text: str, perm: tuple[int, ...]) -> str:
    _validate_perm(perm)
    n = len(perm)
    pieces: list[str] = []
    for i in range(0, len(text), n):
        block = text[i : i + n]
        if len(block) < n:
            pieces.append(block)
            continue
        pieces.append("".join(block[p] for p in perm))
    return "".join(pieces)


def permutation_blocks_encrypt(plaintext: str, perm: tuple[int, ...] = (2, 0, 3, 1)) -> str:
    return _transform(plaintext, perm)


def permutation_blocks_decrypt(ciphertext: str, perm: tuple[int, ...] = (2, 0, 3, 1)) -> str:
    return _transform(ciphertext, _inverse_perm(perm))
