"""Rail fence variant with repeating rail schedule."""

from __future__ import annotations


def _schedule_pattern(length: int, schedule: tuple[int, ...]) -> list[int]:
    if not schedule:
        raise ValueError('schedule must not be empty')
    if min(schedule) < 0:
        raise ValueError('schedule values must be >= 0')
    return [schedule[i % len(schedule)] for i in range(length)]


def rail_fence_variable_encrypt(plaintext: str, rails: int = 4, schedule: tuple[int, ...] = (0, 1, 2, 3, 2, 1)) -> str:
    """Encrypt using a configurable repeating rail assignment schedule."""
    if rails <= 0:
        raise ValueError('rails must be > 0')
    if max(schedule) >= rails:
        raise ValueError('schedule references rail index outside rails')

    pattern = _schedule_pattern(len(plaintext), schedule)
    buckets = ['' for _ in range(rails)]
    for ch, r in zip(plaintext, pattern):
        buckets[r] += ch
    return ''.join(buckets)


def rail_fence_variable_decrypt(ciphertext: str, rails: int = 4, schedule: tuple[int, ...] = (0, 1, 2, 3, 2, 1)) -> str:
    """Decrypt text produced by ``rail_fence_variable_encrypt``."""
    if rails <= 0:
        raise ValueError('rails must be > 0')
    if max(schedule) >= rails:
        raise ValueError('schedule references rail index outside rails')

    pattern = _schedule_pattern(len(ciphertext), schedule)
    counts = [pattern.count(r) for r in range(rails)]

    rails_data: list[list[str]] = []
    idx = 0
    for cnt in counts:
        rails_data.append(list(ciphertext[idx : idx + cnt]))
        idx += cnt

    pos = [0] * rails
    out: list[str] = []
    for r in pattern:
        out.append(rails_data[r][pos[r]])
        pos[r] += 1
    return ''.join(out)
