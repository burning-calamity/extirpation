from pathlib import Path
import subprocess
import sys

from extirpation import list_online_modules, load_online_modules, load_online_modules_with_report


ONLINE_DIR = Path(__file__).resolve().parents[1] / "online"


def test_list_modules_contains_expected_entries():
    names = set(list_online_modules(ONLINE_DIR))
    assert "caesar" in names
    assert "vigenere" in names
    assert "quagmire_iv" in names
    assert "rot47" in names
    assert "morse" in names


def test_loader_returns_modules():
    modules = load_online_modules(ONLINE_DIR)
    assert "caesar" in modules
    assert modules["caesar"].caesar_encrypt("ABC", 3) == "DEF"


def test_loader_report_and_filter():
    report = load_online_modules_with_report(
        ONLINE_DIR,
        module_filter=lambda name, _: name.startswith("b"),
    )
    assert report.errors == []
    assert set(report.modules) == {"baconian", "binary_cipher"}


def test_cipher_round_trips():
    modules = load_online_modules(ONLINE_DIR)

    c = modules["caesar"].caesar_encrypt("Hello, World!", shift=5)
    assert modules["caesar"].caesar_decrypt(c, shift=5) == "Hello, World!"

    v = modules["vigenere"].vigenere_encrypt("Attack at dawn!", "LEMON")
    assert modules["vigenere"].vigenere_decrypt(v, "LEMON") == "Attack at dawn!"

    q = modules["quagmire_iv"].quagmire_iv_encrypt("ATTACK AT DAWN", "ALPHA", "OMEGA", "RIVER")
    assert modules["quagmire_iv"].quagmire_iv_decrypt(q, "ALPHA", "OMEGA", "RIVER") == "ATTACKATDAWN"

    b = modules["baconian"].baconian_encrypt("HELLO")
    assert modules["baconian"].baconian_decrypt(b) == "HELLO"

    z = modules["binary_cipher"].binary_encrypt("hi")
    assert modules["binary_cipher"].binary_decrypt(z) == "hi"

    a = modules["atbash"].atbash_encrypt("Hello")
    assert modules["atbash"].atbash_decrypt(a) == "Hello"

    af = modules["affine"].affine_encrypt("Affine Cipher", 5, 8)
    assert modules["affine"].affine_decrypt(af, 5, 8) == "Affine Cipher"

    rf = modules["rail_fence"].rail_fence_encrypt("WEAREDISCOVEREDFLEEATONCE", 3)
    assert modules["rail_fence"].rail_fence_decrypt(rf, 3) == "WEAREDISCOVEREDFLEEATONCE"

    r47 = modules["rot47"].rot47_encrypt("hello")
    assert modules["rot47"].rot47_decrypt(r47) == "hello"

    m = modules["morse"].morse_encrypt("SOS 123")
    assert modules["morse"].morse_decrypt(m) == "SOS 123"


def test_cli_list_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "list"]
    out = subprocess.check_output(cmd, text=True)
    assert "caesar" in out
