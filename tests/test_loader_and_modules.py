from pathlib import Path
import subprocess
import sys
import os

from extirpation import list_online_modules, load_online_modules, load_online_modules_with_report


ONLINE_DIR = Path(__file__).resolve().parents[1] / "online"
SRC_DIR = Path(__file__).resolve().parents[1] / "src"


def _cli_env() -> dict[str, str]:
    env = os.environ.copy()
    current = env.get("PYTHONPATH", "")
    extra = str(SRC_DIR)
    env["PYTHONPATH"] = f"{extra}{os.pathsep}{current}" if current else extra
    return env


def test_list_modules_contains_expected_entries():
    names = set(list_online_modules(ONLINE_DIR))
    assert "caesar" in names
    assert "vigenere" in names
    assert "quagmire_iv" in names
    assert "rot47" in names
    assert "morse" in names
    assert "enigma" in names
    assert "autokey" in names
    assert "beaufort" in names
    assert "columnar_transposition" in names
    assert "xor_cipher" in names
    assert "polybius" in names
    assert "bifid" in names
    assert "gronsfeld" in names
    assert "porta" in names
    assert "trithemius" in names
    assert "scytale" in names
    assert "keyword_substitution" in names
    assert "running_key" in names
    assert "route_cipher" in names
    assert "a1z26" in names
    assert "one_time_pad" in names
    assert "tap_code" in names
    assert "reverse_cipher" in names
    assert "caesar_box" in names
    assert "base64_cipher" in names
    assert "pig_latin" in names
    assert "playfair" in names
    assert "vernam" in names
    assert "spiral_route" in names
    assert "paired_caesar" in names
    assert "caesar_progressive" in names
    assert "mirror_chunks" in names
    assert "hex_cipher" in names
    assert "rot5" in names
    assert "rot13" in names
    assert "reverse_words" in names
    assert "leetspeak" in names
    assert "word_caesar" in names
    assert "rot18" in names
    assert "chunk_swap" in names
    assert "vowel_shift" in names
    assert "hill_cipher" in names
    assert "double_transposition" in names


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
    assert set(report.modules) == {"baconian", "binary_cipher", "beaufort", "bifid", "base64_cipher"}


def test_cipher_round_trips():
    modules = load_online_modules(ONLINE_DIR)

    c = modules["caesar"].caesar_encrypt("Hello, World!", shift=5)
    assert modules["caesar"].caesar_decrypt(c, shift=5) == "Hello, World!"

    v = modules["vigenere"].vigenere_encrypt("Attack at dawn!", "LEMON")
    assert modules["vigenere"].vigenere_decrypt(v, "LEMON") == "Attack at dawn!"

    akey = modules["autokey"].autokey_encrypt("Attack at dawn!", "QUEEN")
    assert modules["autokey"].autokey_decrypt(akey, "QUEEN") == "Attack at dawn!"

    beau = modules["beaufort"].beaufort_encrypt("Attack at dawn!", "FORT")
    assert modules["beaufort"].beaufort_decrypt(beau, "FORT") == "Attack at dawn!"

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

    col = modules["columnar_transposition"].columnar_encrypt("WEAREDISCOVERED", "ZEBRA")
    assert modules["columnar_transposition"].columnar_decrypt(col, "ZEBRA") == "WEAREDISCOVERED"

    x = modules["xor_cipher"].xor_encrypt("secret message", "key")
    assert modules["xor_cipher"].xor_decrypt(x, "key") == "secret message"

    poly = modules["polybius"].polybius_encrypt("JIG")
    assert modules["polybius"].polybius_decrypt(poly) == "IIG"

    bif = modules["bifid"].bifid_encrypt("DEFENDTHEEASTWALLOFTHECASTLE", 5)
    assert modules["bifid"].bifid_decrypt(bif, 5) == "DEFENDTHEEASTWALLOFTHECASTLE"

    gr = modules["gronsfeld"].gronsfeld_encrypt("Attack at dawn!", "31415")
    assert modules["gronsfeld"].gronsfeld_decrypt(gr, "31415") == "Attack at dawn!"

    tri = modules["trithemius"].trithemius_encrypt("Attack at dawn!")
    assert modules["trithemius"].trithemius_decrypt(tri) == "Attack at dawn!"

    scy = modules["scytale"].scytale_encrypt("WEAREDISCOVERED", 4)
    assert modules["scytale"].scytale_decrypt(scy, 4) == "WEAREDISCOVERED"

    kw = modules["keyword_substitution"].keyword_encrypt("HELLO", "SECRET")
    assert modules["keyword_substitution"].keyword_decrypt(kw, "SECRET") == "HELLO"

    rk = modules["running_key"].running_key_encrypt("HELLO", "XMCKLQWERTY")
    assert modules["running_key"].running_key_decrypt(rk, "XMCKLQWERTY") == "HELLO"

    route = modules["route_cipher"].route_encrypt("WEAREDISCOVERED", 5)
    assert modules["route_cipher"].route_decrypt(route, 5) == "WEAREDISCOVERED"

    code = modules["a1z26"].a1z26_encrypt("HELLO")
    assert modules["a1z26"].a1z26_decrypt(code) == "HELLO"

    otp = modules["one_time_pad"].otp_encrypt("HELLO", "XMCKL")
    assert modules["one_time_pad"].otp_decrypt(otp, "XMCKL") == "HELLO"

    tap = modules["tap_code"].tap_encrypt("TEST")
    assert modules["tap_code"].tap_decrypt(tap) == "TEST"

    rev = modules["reverse_cipher"].reverse_encrypt("abc123")
    assert modules["reverse_cipher"].reverse_decrypt(rev) == "abc123"

    box = modules["caesar_box"].caesar_box_encrypt("WEAREDISCOVERED", 4)
    assert modules["caesar_box"].caesar_box_decrypt(box, 4) == "WEAREDISCOVERED"

    b64 = modules["base64_cipher"].base64_encrypt("hello")
    assert modules["base64_cipher"].base64_decrypt(b64) == "hello"

    pig = modules["pig_latin"].pig_latin_encrypt("hello world")
    assert modules["pig_latin"].pig_latin_decrypt(pig) == "hello world"

    pf = modules["playfair"].playfair_encrypt("HIDETHEGOLD", "MONARCHY")
    assert modules["playfair"].playfair_decrypt(pf, "MONARCHY").startswith("HIDETHEGOLD")

    ve = modules["vernam"].vernam_encrypt("HELLO", "XMCKL")
    assert modules["vernam"].vernam_decrypt(ve, "XMCKL") == "HELLO"

    sp = modules["spiral_route"].spiral_route_encrypt("WEAREDISCOVERED", 5)
    assert modules["spiral_route"].spiral_route_decrypt(sp, 5) == "WEAREDISCOVERED"

    pc = modules["paired_caesar"].paired_caesar_encrypt("Attack at dawn!", 1, 3)
    assert modules["paired_caesar"].paired_caesar_decrypt(pc, 1, 3) == "Attack at dawn!"

    prog = modules["caesar_progressive"].caesar_progressive_encrypt("Attack at dawn!", start_shift=1, step=2)
    assert modules["caesar_progressive"].caesar_progressive_decrypt(prog, start_shift=1, step=2) == "Attack at dawn!"

    mirrored = modules["mirror_chunks"].mirror_chunks_encrypt("abcdefghij", chunk_size=4)
    assert modules["mirror_chunks"].mirror_chunks_decrypt(mirrored, chunk_size=4) == "abcdefghij"

    hx = modules["hex_cipher"].hex_encrypt("hello 🌍")
    assert modules["hex_cipher"].hex_decrypt(hx) == "hello 🌍"

    r5 = modules["rot5"].rot5_encrypt("Phone: 123-909")
    assert modules["rot5"].rot5_decrypt(r5) == "Phone: 123-909"

    r13 = modules["rot13"].rot13_encrypt("Attack at Dawn")
    assert modules["rot13"].rot13_decrypt(r13) == "Attack at Dawn"

    rw = modules["reverse_words"].reverse_words_encrypt("one two three")
    assert modules["reverse_words"].reverse_words_decrypt(rw) == "one two three"

    leet = modules["leetspeak"].leetspeak_encrypt("state")
    assert modules["leetspeak"].leetspeak_decrypt(leet) == "STATE"

    wc = modules["word_caesar"].word_caesar_encrypt("alpha beta gamma", start_shift=2)
    assert modules["word_caesar"].word_caesar_decrypt(wc, start_shift=2) == "alpha beta gamma"

    r18 = modules["rot18"].rot18_encrypt("Attack 1234")
    assert modules["rot18"].rot18_decrypt(r18) == "Attack 1234"

    cs = modules["chunk_swap"].chunk_swap_encrypt("abcdefg")
    assert modules["chunk_swap"].chunk_swap_decrypt(cs) == "abcdefg"

    vs = modules["vowel_shift"].vowel_shift_encrypt("Education", shift=2)
    assert modules["vowel_shift"].vowel_shift_decrypt(vs, shift=2) == "Education"

    hill = modules["hill_cipher"].hill_encrypt("HELLO")
    assert modules["hill_cipher"].hill_decrypt(hill).startswith("HELLO")

    dtr = modules["double_transposition"].double_transposition_encrypt(
        "WEAREDISCOVEREDFLEEATONCE",
        key1="ZEBRA",
        key2="CIPHER",
    )
    assert modules["double_transposition"].double_transposition_decrypt(
        dtr,
        key1="ZEBRA",
        key2="CIPHER",
    ) == "WEAREDISCOVEREDFLEEATONCE"

    enigma_cipher = modules["enigma"].enigma_encrypt(
        text="HELLO WORLD",
        rotors=("I", "II", "III"),
        reflector="B",
        ring_settings=(1, 1, 1),
        positions="AAA",
        plugboard_pairs="AV BS CG DL FU HZ IN KM OW RX",
    )
    enigma_plain = modules["enigma"].enigma_encrypt(
        text=enigma_cipher,
        rotors=("I", "II", "III"),
        reflector="B",
        ring_settings=(1, 1, 1),
        positions="AAA",
        plugboard_pairs="AV BS CG DL FU HZ IN KM OW RX",
    )
    assert enigma_plain == "HELLO WORLD"


def test_cli_list_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "list"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "caesar" in out


def test_cli_version_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "version"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert out == "1.7.0"


def test_cli_catalog_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "catalog"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "caesar_encrypt" in out
    assert "signatures" in out


def test_cli_find_command():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "find",
        "--query",
        "progressive",
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "caesar_progressive" in out


def test_cli_invoke_command():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "invoke",
        "--module",
        "caesar",
        "--function",
        "caesar_encrypt",
        "--kwargs",
        "{\"plaintext\":\"ABC\",\"shift\":3}",
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert out == "DEF"


def test_cli_stats_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "stats"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "encrypt_functions" in out


def test_cli_validate_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "validate"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert out == "{}"


def test_cli_scaffold_command(tmp_path):
    target_dir = tmp_path / "plugins"
    cmd = [
        sys.executable, "-m", "extirpation.cli", "--online-dir", str(target_dir), "scaffold", "demo_cipher"
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    created = Path(out)
    assert created.exists()
    assert "def demo_cipher_encrypt" in created.read_text()


def test_cli_export_catalog_command(tmp_path):
    target = tmp_path / "catalog.json"
    cmd = [
        sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR),
        "export-catalog", "--format", "json", "--output", str(target)
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert Path(out).exists()
    assert "caesar" in Path(out).read_text()


def test_cli_export_catalog_markdown_command(tmp_path):
    target = tmp_path / "catalog.md"
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "export-catalog",
        "--format",
        "markdown",
        "--output",
        str(target),
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert Path(out).exists()
    assert "# extirpation module catalog" in Path(out).read_text()


def test_cli_invoke_rejects_invalid_json_kwargs():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "invoke",
        "--module",
        "caesar",
        "--function",
        "caesar_encrypt",
        "--kwargs",
        "{bad json}",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, env=_cli_env())
    assert proc.returncode != 0
    assert "--kwargs must be valid JSON" in proc.stderr


def test_cli_invoke_rejects_non_object_kwargs():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "invoke",
        "--module",
        "caesar",
        "--function",
        "caesar_encrypt",
        "--kwargs",
        '["not","an","object"]',
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, env=_cli_env())
    assert proc.returncode != 0
    assert "--kwargs must decode to a JSON object" in proc.stderr


def test_cli_scaffold_rejects_invalid_module_name(tmp_path):
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(tmp_path),
        "scaffold",
        "bad-name",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, env=_cli_env())
    assert proc.returncode != 0
    assert "module name must be a valid Python identifier" in proc.stderr
