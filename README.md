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
)

print(list_online_modules("online"))
modules = load_online_modules("online")
print(modules["caesar"].caesar_encrypt("HELLO", shift=3))

report = load_online_modules_with_report("online", recursive=True)
print(report.modules.keys())
print(report.errors)
```

## CLI
List modules:
```bash
extirpation --online-dir online list
```

Generate JSON load report:
```bash
extirpation --online-dir online --recursive report
```

Print installed version:
```bash
extirpation version
```

Invoke a function directly:
```bash
extirpation --online-dir online invoke --module caesar --function caesar_encrypt --kwargs "{\"plaintext\":\"HELLO\",\"shift\":3}"
```

Show aggregate stats:
```bash
extirpation --online-dir online stats
```

Search catalog for matching modules/functions:
```bash
extirpation --online-dir online find --query caesar
```

Validate module contracts:
```bash
extirpation --online-dir online validate
```

Scaffold a new module template:
```bash
extirpation --online-dir online scaffold my_new_cipher
```

Export catalog to Markdown:
```bash
extirpation --online-dir online export-catalog --format markdown --output docs/catalog.md
```

## Included modules
- `online/quagmire_iv.py`
- `online/enigma.py` (full Enigma simulation)
- `online/vigenere.py`
- `online/autokey.py`
- `online/beaufort.py`
- `online/caesar.py`
- `online/baconian.py`
- `online/binary_cipher.py`
- `online/atbash.py`
- `online/affine.py`
- `online/columnar_transposition.py`
- `online/xor_cipher.py`
- `online/rail_fence.py`
- `online/rot47.py`
- `online/morse.py`
- `online/polybius.py`
- `online/bifid.py`
- `online/gronsfeld.py`
- `online/porta.py`
- `online/trithemius.py`
- `online/scytale.py`
- `online/keyword_substitution.py`
- `online/running_key.py`
- `online/route_cipher.py`
- `online/a1z26.py`
- `online/one_time_pad.py`
- `online/tap_code.py`
- `online/reverse_cipher.py`
- `online/caesar_box.py`
- `online/base64_cipher.py`
- `online/pig_latin.py`
- `online/playfair.py`
- `online/vernam.py`
- `online/spiral_route.py`
- `online/paired_caesar.py`
- `online/caesar_progressive.py`
- `online/mirror_chunks.py`
- `online/hex_cipher.py`
- `online/rot5.py`
- `online/rot13.py`
- `online/reverse_words.py`
- `online/leetspeak.py`
- `online/word_caesar.py`
- `online/rot18.py`
- `online/chunk_swap.py`
- `online/vowel_shift.py`
- `online/hill_cipher.py`
- `online/double_transposition.py`

## Automated PyPI publishing from GitHub Releases
This repo includes `.github/workflows/publish-pypi.yml` that publishes automatically when a GitHub Release is published.

### One-time setup in PyPI
1. Create the project (`extirpation`) on PyPI (or use an existing one).
2. In PyPI, configure **Trusted Publishing** and add this GitHub repo/workflow.
3. In GitHub, ensure the `publish` job can run with `id-token: write` (already configured).

### Release flow
1. Merge to your default branch.
2. Create and publish a GitHub Release (for example tag `v1.7.0`).
3. GitHub Actions runs tests (`ci.yml`), builds distributions, validates them, and publishes to PyPI.

## Local packaging checks
```bash
python -m build
python -m twine check dist/*
```
