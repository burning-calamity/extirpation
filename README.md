# extirpation

A Python plugin-style library that auto-loads encryption modules from an `online/` folder.

## Highlights
- Drop-in modules: add a `.py` file to `online/` and it loads automatically.
- Recursive discovery for nested module folders.
- Structured load reports with per-module errors.
- Built-in CLI for discovery, diagnostics, capability signatures, version checks, and direct function invocation.
- GitHub Actions CI + automated PyPI publishing on GitHub Release.

## Install
```bash
pip install extirpation
```

For local development:
```bash
pip install -e .[dev]
```

## Python API
```python
from extirpation import (
    list_online_modules,
    load_online_modules,
    load_online_modules_with_report,
    setup,
)

print(list_online_modules("online"))
modules = load_online_modules("online")
print(modules["caesar"].caesar_encrypt("HELLO", shift=3))

report = load_online_modules_with_report("online", recursive=True)
print(report.modules.keys())
print(report.errors)

setup_result = setup("online")
print(len(setup_result.copied), len(setup_result.skipped))
```

## CLI
List modules:
```bash
extirpation --online-dir online list
```

List modules as JSON:
```bash
extirpation --online-dir online list --json
```

Generate JSON load report:
```bash
extirpation --online-dir online --recursive --workers 4 report
```

Use cache for faster repeated inspection commands:
```bash
extirpation --online-dir online --cache catalog
```

Use cache for module listing too:
```bash
extirpation --online-dir online --cache list --json
```

Print installed version:
```bash
extirpation version
```

Invoke a function directly:
```bash
extirpation --online-dir online invoke --module caesar --function caesar_encrypt --kwargs "{\"plaintext\":\"HELLO\",\"shift\":3}"
```

Run a simple encrypt/decrypt flow without knowing exact function names:
```bash
extirpation --online-dir online transform --module caesar --mode encrypt --text "HELLO" --params "{\"shift\":3}"
```

Invoke multiple functions in one call:
```bash
extirpation --online-dir online invoke-batch --calls "[{\"module\":\"caesar\",\"function\":\"caesar_encrypt\",\"kwargs\":{\"plaintext\":\"ABC\",\"shift\":3}}]"
```

Continue batch execution even when one call fails (default), or stop immediately:
```bash
extirpation --online-dir online invoke-batch --stop-on-error --calls "[...]"
```

Show aggregate stats:
```bash
extirpation --online-dir online stats
```

Run a quick health check:
```bash
extirpation --online-dir online doctor
```

Fail CI when health issues are found:
```bash
extirpation --online-dir online doctor --fail-on-issues
```

Clear in-memory cache:
```bash
extirpation clear-cache
```

Benchmark load performance:
```bash
extirpation --online-dir online --cache --workers 4 benchmark --iterations 5
```

Search catalog for matching modules/functions:
```bash
extirpation --online-dir online find --query caesar
```

Inspect one module:
```bash
extirpation --online-dir online inspect --module caesar
```

Validate module contracts:
```bash
extirpation --online-dir online validate
```

Scaffold a new module template:
```bash
extirpation --online-dir online scaffold my_new_cipher
```

Provision bundled modules into your target folder:
```bash
extirpation --online-dir online setup
```

If you're installed from PyPI, `setup` now provisions modules from package-bundled files.

Export catalog to Markdown:
```bash
extirpation --online-dir online export-catalog --format markdown --output docs/catalog.md
```

## Wordlists
The repository now includes starter multilingual wordlists under `online/wordlist/`.

- Latin alphabet languages: `online/wordlist/latin/*.txt`
- Non-Latin languages are grouped by script/alphabet:
  - Cyrillic: `online/wordlist/cyrillic/*.txt`
  - Greek: `online/wordlist/greek/*.txt`
  - Arabic: `online/wordlist/arabic/*.txt`
  - Devanagari: `online/wordlist/devanagari/*.txt`

All files are UTF-8 and use one word per line.

## Included modules
(Alphabetical, 104 modules)
- `online/a1z26.py`
- `online/adfgvx.py`
- `online/adfgx.py`
- `online/affine.py`
- `online/affine_progressive.py`
- `online/alphabet_filter.py`
- `online/amsco_transposition.py`
- `online/atbash.py`
- `online/autokey.py`
- `online/baconian.py`
- `online/base32_cipher.py`
- `online/base64_cipher.py`
- `online/beaufort.py`
- `online/beaufort_autokey.py`
- `online/bifid.py`
- `online/binary_cipher.py`
- `online/braille_unicode.py`
- `online/caesar.py`
- `online/caesar_autoshift.py`
- `online/caesar_box.py`
- `online/caesar_prime.py`
- `online/caesar_progressive.py`
- `online/chaocipher.py`
- `online/checkerboard_straddling.py`
- `online/chunk_swap.py`
- `online/columnar_snake.py`
- `online/columnar_transposition.py`
- `online/diagonal_zigzag.py`
- `online/disrupted_transposition.py`
- `online/double_transposition.py`
- `online/enigma.py` (full Enigma simulation)
- `online/feistel_toy.py`
- `online/fibonacci_caesar.py`
- `online/fibonacci_shift.py`
- `online/four_square.py`
- `online/fractionated_morse.py`
- `online/general_rot_n_with_custom_alphabet.py`
- `online/gronsfeld.py`
- `online/hex_cipher.py`
- `online/hill_cipher.py`
- `online/jefferson_disk.py`
- `online/keyboard_shift.py`
- `online/keyword_caesar.py`
- `online/keyword_substitution.py`
- `online/langcheck.py`
- `online/leetspeak.py`
- `online/lfsr_toy.py`
- `online/mirror_chunks.py`
- `online/morse.py`
- `online/multiplicative_cipher.py`
- `online/myszkowski_transposition.py`
- `online/nato_phonetic.py`
- `online/nihilist_substitution.py`
- `online/null_cipher.py`
- `online/null_cipher_word_mode.py`
- `online/one_time_pad.py`
- `online/paired_caesar.py`
- `online/paired_vigenere.py`
- `online/permutation_blocks.py`
- `online/pig_latin.py`
- `online/pigpen.py`
- `online/playfair.py`
- `online/polyalpha_cycle.py`
- `online/polybius.py`
- `online/porta.py`
- `online/quagmire_i.py`
- `online/quagmire_ii.py`
- `online/quagmire_iii.py`
- `online/quagmire_iv.py`
- `online/rail_fence.py`
- `online/rail_fence_offset.py`
- `online/rail_fence_variable.py`
- `online/reverse_caesar.py`
- `online/reverse_cipher.py`
- `online/reverse_words.py`
- `online/rot13.py`
- `online/rot18.py`
- `online/rot47.py`
- `online/rot5.py`
- `online/rot_n.py`
- `online/rotating_caesar.py`
- `online/route_boustrophedon.py`
- `online/route_cipher.py`
- `online/route_columns_reverse.py`
- `online/route_diagonal.py`
- `online/running_key.py`
- `online/scytale.py`
- `online/spiral_route.py`
- `online/spn_toy.py`
- `online/substitution_monoalpha.py`
- `online/tap_code.py`
- `online/transpose_blocks.py`
- `online/trifid.py`
- `online/trinary_cipher.py`
- `online/triple_caesar.py`
- `online/trithemius.py`
- `online/two_square.py`
- `online/vernam.py`
- `online/vigenere.py`
- `online/vowel_shift.py`
- `online/word_caesar.py`
- `online/xor_base64.py`
- `online/xor_cipher.py`
- `online/zigzag_words.py`
## Automated PyPI publishing from GitHub Releases
This repo includes `.github/workflows/publish-pypi.yml` that publishes automatically when a GitHub Release is published.

### One-time setup in PyPI
1. Create the project (`extirpation`) on PyPI (or use an existing one).
2. In PyPI, configure **Trusted Publishing** and add this GitHub repo/workflow.
3. In GitHub, ensure the `publish` job can run with `id-token: write` (already configured).

### Release flow
1. Merge to your default branch.
2. Create and publish a GitHub Release (for example tag `v2.6.11`).
3. GitHub Actions runs tests (`ci.yml`), builds distributions, validates them, and publishes to PyPI.

## Local packaging checks
```bash
python -m build
python -m twine check dist/*
```
