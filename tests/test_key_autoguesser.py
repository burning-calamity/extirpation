from __future__ import annotations

from pathlib import Path

from extirpation.key_autoguesser import (
    autoguess_keys,
    list_supported_autoguessers,
    load_language_wordsets,
    score_plaintext_language_cohesion,
)
from extirpation.online_loader import list_online_modules


ROOT = Path(__file__).resolve().parents[1]
WORDLIST = ROOT / "online" / "wordlist"


def test_language_cohesion_penalizes_mixed_language_tokens() -> None:
    wordsets = load_language_wordsets(WORDLIST)
    single = score_plaintext_language_cohesion("hello world", wordsets)
    mixed = score_plaintext_language_cohesion("hello mundo", wordsets)
    assert single.score > mixed.score


def test_autoguess_caesar_finds_expected_shift() -> None:
    guesses = autoguess_keys("caesar", "Khoor Zruog", wordlist_dir=WORDLIST, top_n=3)
    assert guesses
    top = guesses[0]
    assert top.key == {"shift": 3}
    assert top.plaintext == "Hello World"
    assert top.best_language == "english"


def test_autoguess_affine_returns_candidates() -> None:
    guesses = autoguess_keys("affine", "Ihhwvc Swfrcp", wordlist_dir=WORDLIST, top_n=3)
    assert len(guesses) == 3
    assert all(g.cipher == "affine" for g in guesses)


def test_autoguess_vigenere_finds_key_with_seeded_wordlist(tmp_path: Path) -> None:
    root = tmp_path / "wordlist"
    (root / "latin").mkdir(parents=True)
    (root / "latin" / "english.txt").write_text("hello\nworld\nkey\n", encoding="utf-8")
    guesses = autoguess_keys("vigenere", "Rijvs Uyvjn", wordlist_dir=root, top_n=3)
    assert guesses
    top = guesses[0]
    assert top.key == {"key": "key"}
    assert top.plaintext == "Hello World"
    assert top.best_language == "english"


def test_autoguess_vigenere_uses_statistical_key_recovery(tmp_path: Path) -> None:
    root = tmp_path / "wordlist"
    (root / "latin").mkdir(parents=True)
    # Deliberately omit the true key from the wordlist to force statistical recovery.
    (root / "latin" / "english.txt").write_text("hello\nworld\n", encoding="utf-8")
    guesses = autoguess_keys("vigenere", "Rijvs Uyvjn", wordlist_dir=root, top_n=3)
    assert guesses
    assert guesses[0].key == {"key": "key"}
    assert guesses[0].plaintext == "Hello World"


def test_autoguess_unknown_cipher_returns_empty() -> None:
    guesses = autoguess_keys("definitely_unknown_cipher", "abc", wordlist_dir=WORDLIST, top_n=3)
    assert guesses == []


def test_autoguesser_registry_covers_all_online_modules() -> None:
    supported = set(list_supported_autoguessers())
    modules = set(list_online_modules(ROOT / "online"))
    assert modules.issubset(supported)


def test_autoguess_generic_fallback_for_atbash() -> None:
    guesses = autoguess_keys("atbash", "Svool Dliow", wordlist_dir=WORDLIST, top_n=3)
    assert guesses
    assert guesses[0].plaintext == "Hello World"


def test_autoguess_generic_handles_required_keyword_ciphers() -> None:
    guesses = autoguess_keys("quagmire_i", "NLZLT UZVZQ", wordlist_dir=WORDLIST, top_n=3)
    assert guesses
    assert all(g.cipher == "quagmire_i" for g in guesses)


def test_autoguess_generic_finds_autokey_key_with_seeded_wordlist(tmp_path: Path) -> None:
    root = tmp_path / "wordlist"
    (root / "latin").mkdir(parents=True)
    (root / "latin" / "english.txt").write_text("hello\nworld\nkey\n", encoding="utf-8")
    guesses = autoguess_keys("autokey", "Rijss Hzfhr", wordlist_dir=root, top_n=3)
    assert guesses
    top = guesses[0]
    assert top.key == {"key": "key"}
    assert top.plaintext == "Hello World"


def test_load_language_wordsets_returns_defensive_copy() -> None:
    a = load_language_wordsets(WORDLIST)
    a["english"].add("__tmp_mutation__")
    b = load_language_wordsets(WORDLIST)
    assert "__tmp_mutation__" not in b["english"]


def test_autoguess_special_key_shapes_return_candidates() -> None:
    assert autoguess_keys("gronsfeld", "Khoor Zruog", wordlist_dir=WORDLIST, top_n=1)
    assert autoguess_keys("one_time_pad", "Khoor Zruog", wordlist_dir=WORDLIST, top_n=1)
    assert autoguess_keys("vernam", "48656c6c6f", wordlist_dir=WORDLIST, top_n=1)


def test_autoguess_langcheck_tuple_output_is_handled() -> None:
    guesses = autoguess_keys("langcheck", "hello world", wordlist_dir=WORDLIST, top_n=1)
    assert guesses
