"""Rail fence cipher variant with configurable starting rail."""

from __future__ import annotations


def _pattern(length: int, rails: int, start_rail: int) -> list[int]:
    if rails < 2:
        raise ValueError('rails must be >= 2')
    if not 0 <= start_rail < rails:
        raise ValueError('start_rail must be within rail range')

    idx = start_rail
    direction = 1 if start_rail < rails - 1 else -1
    out: list[int] = []
    for _ in range(length):
        out.append(idx)
        idx += direction
        if idx == rails - 1 or idx == 0:
            direction *= -1
    return out


def rail_fence_offset_encrypt(plaintext: str, rails: int = 3, start_rail: int = 0) -> str:
    """Encrypt using zig-zag rails starting from ``start_rail``."""
    pat = _pattern(len(plaintext), rails, start_rail)
    buckets = ['' for _ in range(rails)]
    for ch, rail in zip(plaintext, pat):
        buckets[rail] += ch
    return ''.join(buckets)


def rail_fence_offset_decrypt(ciphertext: str, rails: int = 3, start_rail: int = 0) -> str:
    """Decrypt text produced by ``rail_fence_offset_encrypt``."""
    pat = _pattern(len(ciphertext), rails, start_rail)
    counts = [pat.count(r) for r in range(rails)]

    rails_data: list[list[str]] = []
    idx = 0
    for count in counts:
        rails_data.append(list(ciphertext[idx : idx + count]))
        idx += count

    pos = [0] * rails
    out: list[str] = []
    for rail in pat:
        out.append(rails_data[rail][pos[rail]])
        pos[rail] += 1
    return ''.join(out)
