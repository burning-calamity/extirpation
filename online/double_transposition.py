"""Double keyed block transposition cipher."""

from __future__ import annotations


def _order_from_key(key: str) -> list[int]:
    if not key:
        raise ValueError("key must be non-empty")
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def _transpose_block_encrypt(block: str, key: str) -> str:
    order = _order_from_key(key)
    usable = [idx for idx in order if idx < len(block)]
    return "".join(block[idx] for idx in usable)


def _transpose_block_decrypt(block: str, key: str) -> str:
    order = _order_from_key(key)
    usable = [idx for idx in order if idx < len(block)]
    out = [""] * len(block)
    for src_pos, original_idx in enumerate(usable):
        out[original_idx] = block[src_pos]
    return "".join(out)


def _apply_blocks(text: str, key: str, decrypt: bool = False) -> str:
    width = len(key)
    if width == 0:
        raise ValueError("key must be non-empty")
    pieces: list[str] = []
    for i in range(0, len(text), width):
        block = text[i : i + width]
        pieces.append(_transpose_block_decrypt(block, key) if decrypt else _transpose_block_encrypt(block, key))
    return "".join(pieces)


def double_transposition_encrypt(plaintext: str, key1: str = "ZEBRA", key2: str = "CIPHER") -> str:
    once = _apply_blocks(plaintext, key1, decrypt=False)
    return _apply_blocks(once, key2, decrypt=False)


def double_transposition_decrypt(ciphertext: str, key1: str = "ZEBRA", key2: str = "CIPHER") -> str:
    once = _apply_blocks(ciphertext, key2, decrypt=True)
    return _apply_blocks(once, key1, decrypt=True)
