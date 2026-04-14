# extirpation

A Python plugin-style library that auto-loads encryption modules from an `online/` folder.

## Highlights
- Drop-in modules: add a `.py` file to `online/` and it loads automatically.
- Recursive discovery for nested module folders.
- Structured load reports with per-module errors.
- Built-in CLI for discovery, diagnostics, and version checks.
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

## Automated PyPI publishing from GitHub Releases
This repo includes `.github/workflows/publish-pypi.yml` that publishes automatically when a GitHub Release is published.

### One-time setup in PyPI
1. Create the project (`extirpation`) on PyPI (or use an existing one).
2. In PyPI, configure **Trusted Publishing** and add this GitHub repo/workflow.
3. In GitHub, ensure the `publish` job can run with `id-token: write` (already configured).

### Release flow
1. Merge to your default branch.
2. Create and publish a GitHub Release (for example tag `v0.5.0`).
3. GitHub Actions runs tests (`ci.yml`), builds distributions, validates them, and publishes to PyPI.

## Local packaging checks
```bash
python -m build
python -m twine check dist/*
```
