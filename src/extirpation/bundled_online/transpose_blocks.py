"""Block transposition cipher with explicit permutation."""

from __future__ import annotations


def _validate_perm(block_size: int, perm: tuple[int, ...]) -> None:
    if block_size <= 0:
        raise ValueError('block_size must be > 0')
    if len(perm) != block_size:
        raise ValueError('perm length must equal block_size')
    if set(perm) != set(range(block_size)):
        raise ValueError('perm must be a permutation of 0..block_size-1')


def transpose_blocks_encrypt(plaintext: str, block_size: int = 5, perm: tuple[int, ...] = (2, 0, 4, 1, 3), pad: str = 'X') -> str:
    """Encrypt by permuting each fixed-size block."""
    _validate_perm(block_size, perm)
    if len(pad) != 1:
        raise ValueError('pad must be one character')

    rem = len(plaintext) % block_size
    if rem:
        plaintext += pad * (block_size - rem)

    out: list[str] = []
    for i in range(0, len(plaintext), block_size):
        blk = plaintext[i : i + block_size]
        out.extend(blk[p] for p in perm)
    return ''.join(out)


def transpose_blocks_decrypt(ciphertext: str, block_size: int = 5, perm: tuple[int, ...] = (2, 0, 4, 1, 3), pad: str = 'X') -> str:
    """Decrypt text produced by ``transpose_blocks_encrypt``."""
    _validate_perm(block_size, perm)
    if len(pad) != 1:
        raise ValueError('pad must be one character')
    if len(ciphertext) % block_size != 0:
        raise ValueError('ciphertext length must be divisible by block_size')

    inv = [0] * block_size
    for i, p in enumerate(perm):
        inv[p] = i

    out: list[str] = []
    for i in range(0, len(ciphertext), block_size):
        blk = ciphertext[i : i + block_size]
        plain_blk = [''] * block_size
        for j in range(block_size):
            plain_blk[j] = blk[inv[j]]
        out.extend(plain_blk)
    return ''.join(out).rstrip(pad)
