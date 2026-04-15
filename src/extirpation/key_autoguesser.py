"""Cipher key autoguessing helpers backed by language wordlists."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
import heapq
import inspect
import itertools
import math
from pathlib import Path
import re
from typing import Callable

from .online_loader import load_online_modules

TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
_A_ORD = ord("A")
ASCII_ALPHA_RE = re.compile(r"^[a-z]+$")
LATIN_LETTER_RE = re.compile(r"[a-z]", re.IGNORECASE)
_ENGLISH_FREQ = {
    "a": 8.17,
    "b": 1.49,
    "c": 2.78,
    "d": 4.25,
    "e": 12.70,
    "f": 2.23,
    "g": 2.02,
    "h": 6.09,
    "i": 6.97,
    "j": 0.15,
    "k": 0.77,
    "l": 4.03,
    "m": 2.41,
    "n": 6.75,
    "o": 7.51,
    "p": 1.93,
    "q": 0.10,
    "r": 5.99,
    "s": 6.33,
    "t": 9.06,
    "u": 2.76,
    "v": 0.98,
    "w": 2.36,
    "x": 0.15,
    "y": 1.97,
    "z": 0.07,
}
_COMMON_ENGLISH_BIGRAMS = {
    "th", "he", "in", "er", "an", "re", "on", "at", "en", "nd",
    "ti", "es", "or", "te", "of", "ed", "is", "it", "al", "ar",
}


@dataclass(frozen=True)
class LanguageScore:
    score: float
    best_language: str | None
    matched_tokens: int
    total_tokens: int
    language_hits: dict[str, int]


@dataclass(frozen=True)
class KeyGuess:
    cipher: str
    key: object
    plaintext: str
    score: float
    best_language: str | None
    matched_tokens: int
    total_tokens: int


ScoreFn = Callable[[str], LanguageScore]


def _default_wordlist_dir() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "online" / "wordlist"
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("unable to locate online/wordlist directory")


def _infer_language(file_path: Path, root: Path) -> str | None:
    if file_path.name.startswith("TODO_"):
        return None
    if file_path.name in {"NEAR_DUPLICATES_ALLOWLIST.txt"}:
        return None
    if file_path.parent == root:
        return None
    if file_path.parent.parent == root:
        return file_path.stem
    for parent in file_path.parents:
        if parent == root:
            break
        if parent.parent.parent == root:
            return parent.name
    return file_path.stem


@lru_cache(maxsize=8)
def _load_language_wordsets_cached(root_key: str) -> dict[str, set[str]]:
    root = Path(root_key)
    language_words: dict[str, set[str]] = {}
    for file_path in sorted(root.rglob("*.txt")):
        language = _infer_language(file_path, root)
        if not language:
            continue
        words = {
            line.strip().lower()
            for line in file_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }
        language_words.setdefault(language, set()).update(words)
    return language_words


def load_language_wordsets(wordlist_dir: str | Path | None = None) -> dict[str, set[str]]:
    root = Path(wordlist_dir).resolve() if wordlist_dir else _default_wordlist_dir()
    # Return a defensive copy so callers can mutate without poisoning the cache.
    return deepcopy(_load_language_wordsets_cached(str(root)))


def _build_token_language_index(language_words: dict[str, set[str]]) -> dict[str, tuple[str, ...]]:
    token_languages: dict[str, list[str]] = {}
    for language, words in language_words.items():
        for token in words:
            token_languages.setdefault(token, []).append(language)
    return {token: tuple(sorted(langs)) for token, langs in token_languages.items()}


def score_plaintext_language_cohesion(
    plaintext: str,
    language_words: dict[str, set[str]],
) -> LanguageScore:
    tokens = [t.lower() for t in TOKEN_RE.findall(plaintext)]
    if not tokens:
        return LanguageScore(0.0, None, 0, 0, {})

    token_index = _build_token_language_index(language_words)
    hits: dict[str, int] = {}
    matched_tokens = 0
    for token in tokens:
        token_languages = token_index.get(token, ())
        if token_languages:
            matched_tokens += 1
            for lang in token_languages:
                hits[lang] = hits.get(lang, 0) + 1

    if not matched_tokens:
        return LanguageScore(0.0, None, 0, len(tokens), {})

    best_language, best_hits = max(hits.items(), key=lambda kv: kv[1])
    coverage = matched_tokens / len(tokens)
    dominance = best_hits / matched_tokens
    mixed_language_penalty = 1.0 - (1.0 - dominance) * 0.7
    score = coverage * mixed_language_penalty
    return LanguageScore(score, best_language, matched_tokens, len(tokens), hits)


def _score_plaintext_quality(plaintext: str) -> float:
    if not plaintext:
        return 0.0
    printable = sum(1 for ch in plaintext if ch.isprintable())
    alpha = sum(1 for ch in plaintext if ch.isalpha())
    spaces = sum(1 for ch in plaintext if ch.isspace())
    printable_ratio = printable / len(plaintext)
    alpha_ratio = alpha / len(plaintext)
    space_ratio = spaces / len(plaintext)
    space_target_bonus = max(0.0, 1.0 - min(abs(space_ratio - 0.16), 0.16) / 0.16)
    return 0.45 * printable_ratio + 0.35 * alpha_ratio + 0.20 * space_target_bonus


def _score_latin_frequency(plaintext: str) -> float:
    letters = [ch.lower() for ch in plaintext if LATIN_LETTER_RE.match(ch)]
    if len(letters) < 20:
        return 0.0
    counts: dict[str, int] = {}
    for ch in letters:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(letters)
    chi2 = 0.0
    for letter, expected_pct in _ENGLISH_FREQ.items():
        observed = counts.get(letter, 0)
        expected = n * (expected_pct / 100.0)
        if expected > 0:
            chi2 += ((observed - expected) ** 2) / expected
    # map lower chi2 (better) onto 0..1
    return math.exp(-chi2 / 120.0)


def _score_common_english_bigrams(plaintext: str) -> float:
    letters_only = "".join(ch.lower() for ch in plaintext if LATIN_LETTER_RE.match(ch))
    if len(letters_only) < 8:
        return 0.0
    grams = [letters_only[i : i + 2] for i in range(len(letters_only) - 1)]
    if not grams:
        return 0.0
    hits = sum(1 for gram in grams if gram in _COMMON_ENGLISH_BIGRAMS)
    return hits / len(grams)


def _combined_guess_score(plaintext: str, lang_score: LanguageScore) -> float:
    quality_score = _score_plaintext_quality(plaintext)
    latin_freq_score = _score_latin_frequency(plaintext)
    bigram_score = _score_common_english_bigrams(plaintext)
    return 0.70 * lang_score.score + 0.15 * quality_score + 0.10 * latin_freq_score + 0.05 * bigram_score


def _make_language_scorer(language_words: dict[str, set[str]]) -> ScoreFn:
    token_index = _build_token_language_index(language_words)

    def _scorer(plaintext: str) -> LanguageScore:
        tokens = [t.lower() for t in TOKEN_RE.findall(plaintext)]
        if not tokens:
            return LanguageScore(0.0, None, 0, 0, {})

        hits: dict[str, int] = {}
        matched_tokens = 0
        for token in tokens:
            token_languages = token_index.get(token, ())
            if token_languages:
                matched_tokens += 1
                for language in token_languages:
                    hits[language] = hits.get(language, 0) + 1

        if not matched_tokens:
            return LanguageScore(0.0, None, 0, len(tokens), {})

        best_language, best_hits = max(hits.items(), key=lambda kv: kv[1])
        coverage = matched_tokens / len(tokens)
        dominance = best_hits / matched_tokens
        mixed_language_penalty = 1.0 - (1.0 - dominance) * 0.7
        score = coverage * mixed_language_penalty
        return LanguageScore(score, best_language, matched_tokens, len(tokens), hits)

    return _scorer


def _caesar_decrypt(ciphertext: str, shift: int) -> str:
    result: list[str] = []
    for ch in ciphertext:
        if "A" <= ch <= "Z":
            result.append(chr((ord(ch) - _A_ORD - shift) % 26 + _A_ORD))
        elif "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") - shift) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)


def _top_n_insert(heap: list[tuple[float, int, KeyGuess]], guess: KeyGuess, top_n: int, ordinal: int) -> None:
    item = (guess.score, ordinal, guess)
    if len(heap) < top_n:
        heapq.heappush(heap, item)
        return
    if item > heap[0]:
        heapq.heapreplace(heap, item)


def _top_n_sorted(heap: list[tuple[float, int, KeyGuess]]) -> list[KeyGuess]:
    return [item[2] for item in sorted(heap, key=lambda x: (x[0], x[1]), reverse=True)]


def _mod_inverse(a: int, m: int) -> int | None:
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def _affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    inv = _mod_inverse(a, 26)
    if inv is None:
        raise ValueError(f"no modular inverse for a={a}")
    result: list[str] = []
    for ch in ciphertext:
        if "A" <= ch <= "Z":
            v = (inv * ((ord(ch) - _A_ORD) - b)) % 26
            result.append(chr(v + _A_ORD))
        elif "a" <= ch <= "z":
            v = (inv * ((ord(ch) - ord('a')) - b)) % 26
            result.append(chr(v + ord('a')))
        else:
            result.append(ch)
    return "".join(result)


def _guess_caesar(
    ciphertext: str,
    language_words: dict[str, set[str]],
    scorer: ScoreFn,
    top_n: int,
) -> list[KeyGuess]:
    del language_words
    heap: list[tuple[float, int, KeyGuess]] = []
    for shift in range(26):
        plaintext = _caesar_decrypt(ciphertext, shift)
        lang_score = scorer(plaintext)
        guess = KeyGuess(
            cipher="caesar",
            key={"shift": shift},
            plaintext=plaintext,
            score=_combined_guess_score(plaintext, lang_score),
            best_language=lang_score.best_language,
            matched_tokens=lang_score.matched_tokens,
            total_tokens=lang_score.total_tokens,
        )
        _top_n_insert(heap, guess, top_n, shift)
    return _top_n_sorted(heap)


def _guess_affine(
    ciphertext: str,
    language_words: dict[str, set[str]],
    scorer: ScoreFn,
    top_n: int,
) -> list[KeyGuess]:
    del language_words
    heap: list[tuple[float, int, KeyGuess]] = []
    ordinal = 0
    for a in (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25):
        for b in range(26):
            plaintext = _affine_decrypt(ciphertext, a, b)
            lang_score = scorer(plaintext)
            guess = KeyGuess(
                cipher="affine",
                key={"a": a, "b": b},
                plaintext=plaintext,
                score=_combined_guess_score(plaintext, lang_score),
                best_language=lang_score.best_language,
                matched_tokens=lang_score.matched_tokens,
                total_tokens=lang_score.total_tokens,
            )
            _top_n_insert(heap, guess, top_n, ordinal)
            ordinal += 1
    return _top_n_sorted(heap)


def _vigenere_decrypt(ciphertext: str, key: str) -> str:
    shifts = [ord(ch) - ord("a") for ch in key.lower()]
    if not shifts:
        return ciphertext
    out: list[str] = []
    i = 0
    for ch in ciphertext:
        if "A" <= ch <= "Z":
            shift = shifts[i % len(shifts)]
            out.append(chr((ord(ch) - _A_ORD - shift) % 26 + _A_ORD))
            i += 1
        elif "a" <= ch <= "z":
            shift = shifts[i % len(shifts)]
            out.append(chr((ord(ch) - ord("a") - shift) % 26 + ord("a")))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def _candidate_keys(language_words: dict[str, set[str]], limit: int = 2000) -> list[str]:
    seed = {"key", "secret", "cipher", "river", "alpha", "omega"}
    keys = set(seed)
    for words in language_words.values():
        for word in words:
            w = word.strip().lower()
            if 2 <= len(w) <= 12 and ASCII_ALPHA_RE.fullmatch(w):
                keys.add(w)
                if len(keys) >= limit:
                    break
        if len(keys) >= limit:
            break
    return sorted(keys, key=lambda x: (len(x), x))


def _vigenere_statistical_keys(ciphertext: str, max_key_len: int = 12) -> list[str]:
    letters = [ch.lower() for ch in ciphertext if "a" <= ch.lower() <= "z"]
    if len(letters) < 8:
        return []

    def _best_shift(chars: list[str]) -> int:
        n = len(chars)
        if n == 0:
            return 0
        best_shift = 0
        best_chi2 = float("inf")
        for shift in range(26):
            counts = {chr(ord("a") + i): 0 for i in range(26)}
            for ch in chars:
                p = chr((ord(ch) - ord("a") - shift) % 26 + ord("a"))
                counts[p] += 1
            chi2 = 0.0
            for letter, expected_pct in _ENGLISH_FREQ.items():
                observed = counts[letter]
                expected = n * (expected_pct / 100.0)
                if expected > 0:
                    chi2 += ((observed - expected) ** 2) / expected
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_shift = shift
        return best_shift

    keys: list[str] = []
    for key_len in range(1, min(max_key_len, len(letters)) + 1):
        slices = [letters[i::key_len] for i in range(key_len)]
        shifts = [_best_shift(chars) for chars in slices]
        key = "".join(chr(ord("a") + s) for s in shifts)
        if key:
            keys.append(key)
    # prefer short keys first, then stable lexicographic order
    return sorted(set(keys), key=lambda k: (len(k), k))


def _guess_vigenere(ciphertext: str, language_words: dict[str, set[str]], scorer: ScoreFn, top_n: int) -> list[KeyGuess]:
    heap: list[tuple[float, int, KeyGuess]] = []
    perfect_hits = 0
    statistical = _vigenere_statistical_keys(ciphertext, max_key_len=12)
    keys = list(dict.fromkeys(statistical + _candidate_keys(language_words)))
    for ordinal, key in enumerate(keys):
        plaintext = _vigenere_decrypt(ciphertext, key)
        lang_score = scorer(plaintext)
        guess = KeyGuess(
            cipher="vigenere",
            key={"key": key},
            plaintext=plaintext,
            score=_combined_guess_score(plaintext, lang_score),
            best_language=lang_score.best_language,
            matched_tokens=lang_score.matched_tokens,
            total_tokens=lang_score.total_tokens,
        )
        _top_n_insert(heap, guess, top_n, ordinal)
        if guess.score >= 0.999:
            perfect_hits += 1
            if perfect_hits >= top_n:
                break
    return _top_n_sorted(heap)


_AUTOGUESSERS: dict[str, Callable[[str, dict[str, set[str]], ScoreFn, int], list[KeyGuess]]] = {
    "caesar": _guess_caesar,
    "affine": _guess_affine,
    "rot_n": _guess_caesar,
    "vigenere": _guess_vigenere,
}


def _bundled_online_dir() -> Path:
    return Path(__file__).resolve().parent / "bundled_online"


@lru_cache(maxsize=1)
def _load_bundled_modules() -> dict[str, object]:
    return load_online_modules(_bundled_online_dir())


def _find_decrypt_callable(module: object) -> Callable[..., object] | None:
    for name, fn in vars(module).items():
        if callable(fn) and "decrypt" in name and not name.startswith("_"):
            return fn
    return None


def _iter_param_candidates(
    parameter: inspect.Parameter,
    language_words: dict[str, set[str]],
    *,
    cipher: str | None = None,
    ciphertext: str | None = None,
) -> list[object]:
    if parameter.default is not inspect._empty:
        base_candidates: list[object] = [parameter.default]
    else:
        base_candidates = []

    name = parameter.name.lower()
    if name in {"text", "plaintext", "ciphertext", "ciphertext_hex", "binary_text"}:
        return []
    if cipher == "gronsfeld" and name == "key":
        return ["1", "12", "123", "314159"]
    if cipher in {"one_time_pad", "vernam"} and name in {"pad", "key"} and ciphertext:
        compact_len = max(1, len(ciphertext.replace(" ", "")))
        return [
            "A" * compact_len,
            "K" * compact_len,
            "KEY",
        ]
    if name in {"key", "keyword", "key1", "key2", "key_a", "key_b", "key_text"}:
        return (base_candidates + _candidate_keys(language_words, limit=200))[:200]
    if "key" in name or "keyword" in name or "indicator" in name:
        return (base_candidates + _candidate_keys(language_words, limit=120))[:120]
    if name in {"shift", "n", "start_shift", "seed_shift", "s1", "s2", "s3", "b", "b0", "step"}:
        return list(dict.fromkeys(base_candidates + list(range(0, 26))))
    if name in {"a"}:
        return list(dict.fromkeys(base_candidates + [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]))
    if name in {"rails", "width", "columns", "size", "period", "block_size", "chunk_size"}:
        return list(dict.fromkeys(base_candidates + list(range(2, 8))))
    if name in {"encoding"}:
        return list(dict.fromkeys(base_candidates + ["utf-8", "latin-1"]))
    if name in {"pad"}:
        return list(dict.fromkeys(base_candidates + ["X", "Q"]))
    if name in {"alphabet"}:
        return list(dict.fromkeys(base_candidates + ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]))
    if name in {"right"}:
        return [True, False]

    annotation = parameter.annotation
    annotation_text = str(annotation).lower() if annotation is not inspect._empty else ""
    if "int" in annotation_text:
        return list(dict.fromkeys(base_candidates + list(range(0, 10))))
    if "bool" in annotation_text:
        return [True, False]
    if "str" in annotation_text:
        return (base_candidates + _candidate_keys(language_words, limit=80))[:80]

    if base_candidates:
        return base_candidates
    return []


def _decrypt_call_candidates(
    decrypt_fn: Callable[..., object],
    ciphertext: str,
    language_words: dict[str, set[str]],
    *,
    cipher: str | None = None,
    max_combinations: int = 200,
) -> list[tuple[tuple[str, object], ...]]:
    signature = inspect.signature(decrypt_fn)
    positional_name: str | None = None
    kw_candidates: list[tuple[str, list[object]]] = []
    has_var_keywords = False
    for i, parameter in enumerate(signature.parameters.values()):
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            has_var_keywords = True
            continue
        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            continue
        if i == 0 and parameter.name.lower() in {
            "ciphertext",
            "text",
            "ciphertext_hex",
            "binary_text",
            "plaintext",
        }:
            positional_name = parameter.name
            continue

        candidates = _iter_param_candidates(parameter, language_words, cipher=cipher, ciphertext=ciphertext)
        if not candidates:
            return []
        kw_candidates.append((parameter.name, candidates))

    if has_var_keywords:
        if positional_name:
            return [((positional_name, ciphertext),)]
        return [(("text", ciphertext),)]

    if not kw_candidates:
        if positional_name:
            return [((positional_name, ciphertext),)]
        return [tuple()]

    names = [name for name, _ in kw_candidates]
    candidate_lists = [values for _, values in kw_candidates]
    combinations: list[tuple[tuple[str, object], ...]] = []
    for values in itertools.product(*candidate_lists):
        kwargs = tuple(zip(names, values))
        if positional_name:
            kwargs = ((positional_name, ciphertext),) + kwargs
        combinations.append(kwargs)
        if len(combinations) >= max_combinations:
            break
    return combinations


def _guess_module_generic(
    cipher: str,
    ciphertext: str,
    language_words: dict[str, set[str]],
    scorer: ScoreFn,
    top_n: int,
) -> list[KeyGuess]:
    module = _load_bundled_modules().get(cipher)
    if module is None:
        return []
    decrypt_fn = _find_decrypt_callable(module)
    if decrypt_fn is None:
        return []

    candidates = _decrypt_call_candidates(decrypt_fn, ciphertext, language_words, cipher=cipher)
    heap: list[tuple[float, int, KeyGuess]] = []
    seen: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
    perfect_hits = 0
    for ordinal, kwargs_items in enumerate(candidates):
        kwargs = dict(kwargs_items)
        try:
            plaintext = decrypt_fn(**kwargs)  # type: ignore[misc]
        except Exception:
            continue
        if not isinstance(plaintext, str):
            plaintext = str(plaintext)
        lang_score = scorer(plaintext)
        composite_score = _combined_guess_score(plaintext, lang_score)
        result_key = {k: v for k, v in kwargs.items() if k.lower() not in {"ciphertext", "text"}}
        fingerprint = (
            plaintext,
            tuple(sorted((k, str(v)) for k, v in result_key.items())),
        )
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        guess = KeyGuess(
            cipher=cipher,
            key=result_key,
            plaintext=plaintext,
            score=composite_score,
            best_language=lang_score.best_language,
            matched_tokens=lang_score.matched_tokens,
            total_tokens=lang_score.total_tokens,
        )
        _top_n_insert(heap, guess, top_n, ordinal)
        if composite_score >= 0.999:
            perfect_hits += 1
            if perfect_hits >= top_n:
                break
    if not heap:
        lang_score = scorer(ciphertext)
        return [
            KeyGuess(
                cipher=cipher,
                key={},
                plaintext=ciphertext,
                score=_combined_guess_score(ciphertext, lang_score),
                best_language=lang_score.best_language,
                matched_tokens=lang_score.matched_tokens,
                total_tokens=lang_score.total_tokens,
            )
        ]
    return _top_n_sorted(heap)


@lru_cache(maxsize=1)
def _registry() -> dict[str, Callable[[str, dict[str, set[str]], ScoreFn, int], list[KeyGuess]]]:
    registry = dict(_AUTOGUESSERS)
    for cipher_name in _load_bundled_modules():
        if cipher_name in registry:
            continue
        registry[cipher_name] = (
            lambda ciphertext, language_words, scorer, top_n, cipher_name=cipher_name: _guess_module_generic(
                cipher_name, ciphertext, language_words, scorer, top_n
            )
        )
    return registry


def list_supported_autoguessers() -> list[str]:
    """List ciphers with an available autoguesser."""
    return sorted(_registry().keys())


def autoguess_keys(
    cipher: str,
    ciphertext: str,
    wordlist_dir: str | Path | None = None,
    top_n: int = 5,
) -> list[KeyGuess]:
    """Return top-N key guesses for supported ciphers."""
    if top_n < 1:
        raise ValueError("top_n must be >= 1")
    cipher_key = cipher.strip().lower()
    registry = _registry()
    if cipher_key not in registry:
        return []
    language_words = load_language_wordsets(wordlist_dir=wordlist_dir)
    scorer = _make_language_scorer(language_words)
    return registry[cipher_key](ciphertext, language_words, scorer, top_n)


def autoguess_all_ciphers(
    ciphertext: str,
    wordlist_dir: str | Path | None = None,
    per_cipher_top_n: int = 1,
    global_top_n: int = 20,
) -> list[KeyGuess]:
    """Run autoguessing across every supported cipher and return top global candidates."""
    if per_cipher_top_n < 1:
        raise ValueError("per_cipher_top_n must be >= 1")
    if global_top_n < 1:
        raise ValueError("global_top_n must be >= 1")

    registry = _registry()
    language_words = load_language_wordsets(wordlist_dir=wordlist_dir)
    scorer = _make_language_scorer(language_words)

    all_guesses: list[KeyGuess] = []
    for _, guess_fn in registry.items():
        guesses = guess_fn(ciphertext, language_words, scorer, per_cipher_top_n)
        all_guesses.extend(guesses)
    return sorted(all_guesses, key=lambda g: g.score, reverse=True)[:global_top_n]
