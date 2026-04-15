"""Enigma machine simulation (rotors I-V + reflectors B/C)."""

from __future__ import annotations

import string

ALPHABET = string.ascii_uppercase

ROTOR_SPECS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}

REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}


def _i(ch: str) -> int:
    return ord(ch) - 65


def _clean(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


def _parse_plugboard(pairs: str | None) -> dict[str, str]:
    mapping = {ch: ch for ch in ALPHABET}
    if not pairs:
        return mapping
    used = set()
    for pair in pairs.upper().split():
        if len(pair) != 2 or any(c not in ALPHABET for c in pair):
            raise ValueError(f"invalid plugboard pair: {pair}")
        a, b = pair[0], pair[1]
        if a == b or a in used or b in used:
            raise ValueError(f"invalid or duplicate plugboard assignment: {pair}")
        mapping[a], mapping[b] = b, a
        used.add(a)
        used.add(b)
    return mapping


class _Rotor:
    def __init__(self, name: str, ring_setting: int = 1, position: str = "A") -> None:
        wiring, notch = ROTOR_SPECS[name]
        self.name = name
        self.forward = [_i(c) for c in wiring]
        self.backward = [0] * 26
        for idx, out in enumerate(self.forward):
            self.backward[out] = idx
        self.notch = _i(notch)
        self.ring = (ring_setting - 1) % 26
        self.pos = _i(position.upper())

    def at_notch(self) -> bool:
        return self.pos == self.notch

    def step(self) -> None:
        self.pos = (self.pos + 1) % 26

    def enc_fwd(self, c: int) -> int:
        shifted = (c + self.pos - self.ring) % 26
        out = self.forward[shifted]
        return (out - self.pos + self.ring) % 26

    def enc_back(self, c: int) -> int:
        shifted = (c + self.pos - self.ring) % 26
        out = self.backward[shifted]
        return (out - self.pos + self.ring) % 26


class EnigmaMachine:
    """Three-rotor Enigma machine with reflector and optional plugboard."""

    def __init__(
        self,
        rotors: tuple[str, str, str] = ("I", "II", "III"),
        reflector: str = "B",
        ring_settings: tuple[int, int, int] = (1, 1, 1),
        positions: str = "AAA",
        plugboard_pairs: str | None = None,
    ) -> None:
        if len(positions) != 3:
            raise ValueError("positions must be a 3-letter string")
        if reflector not in REFLECTORS:
            raise ValueError("reflector must be 'B' or 'C'")

        self.left = _Rotor(rotors[0], ring_settings[0], positions[0])
        self.middle = _Rotor(rotors[1], ring_settings[1], positions[1])
        self.right = _Rotor(rotors[2], ring_settings[2], positions[2])
        self.reflector = [_i(c) for c in REFLECTORS[reflector]]
        self.plugboard = _parse_plugboard(plugboard_pairs)

    def _step_rotors(self) -> None:
        # Double-stepping behavior
        if self.middle.at_notch():
            self.left.step()
            self.middle.step()
        elif self.right.at_notch():
            self.middle.step()
        self.right.step()

    def encrypt_char(self, ch: str) -> str:
        if ch.upper() not in ALPHABET:
            return ch

        self._step_rotors()
        c = self.plugboard[ch.upper()]
        idx = _i(c)

        idx = self.right.enc_fwd(idx)
        idx = self.middle.enc_fwd(idx)
        idx = self.left.enc_fwd(idx)

        idx = self.reflector[idx]

        idx = self.left.enc_back(idx)
        idx = self.middle.enc_back(idx)
        idx = self.right.enc_back(idx)

        out = self.plugboard[ALPHABET[idx]]
        return out if ch.isupper() else out.lower()

    def encrypt_text(self, text: str) -> str:
        return "".join(self.encrypt_char(ch) for ch in text)


def enigma_encrypt(
    text: str,
    rotors: tuple[str, str, str] = ("I", "II", "III"),
    reflector: str = "B",
    ring_settings: tuple[int, int, int] = (1, 1, 1),
    positions: str = "AAA",
    plugboard_pairs: str | None = None,
) -> str:
    """Encrypt/decrypt text with Enigma (same function for both directions)."""
    machine = EnigmaMachine(
        rotors=rotors,
        reflector=reflector,
        ring_settings=ring_settings,
        positions=positions,
        plugboard_pairs=plugboard_pairs,
    )
    return machine.encrypt_text(text)


def enigma_decrypt(**kwargs: object) -> str:
    """Alias for `enigma_encrypt` (Enigma is symmetric)."""
    return enigma_encrypt(**kwargs)
