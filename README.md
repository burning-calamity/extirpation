# extirpation

A Python plugin-style library that auto-loads encryption modules from an `online/` folder.

## Highlights
- Drop-in modules: add a `.py` file to `online/` and it loads automatically.
- Recursive discovery for nested module folders.
- Structured load reports with per-module errors.
- Built-in CLI for discovery and diagnostics.

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

## Included modules
- `online/quagmire_iv.py`
- `online/vigenere.py`
- `online/caesar.py`
- `online/baconian.py`
- `online/binary_cipher.py`
- `online/atbash.py`
- `online/affine.py`
- `online/rail_fence.py`
- `online/rot47.py`
- `online/morse.py`

## Publish to PyPI
1. Build:
   ```bash
   python -m build
   ```
2. Validate:
   ```bash
   twine check dist/*
   ```
3. Upload to TestPyPI:
   ```bash
   twine upload --repository testpypi dist/*
   ```
4. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```
