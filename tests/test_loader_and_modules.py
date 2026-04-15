from pathlib import Path
import subprocess
import sys
import os

from extirpation import (
    clear_online_loader_cache,
    list_online_modules,
    list_online_modules_cached,
    load_online_modules,
    load_online_modules_with_report,
    load_online_modules_with_report_cached,
    setup,
)


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
    assert "quagmire_i" in names
    assert "quagmire_ii" in names
    assert "quagmire_iii" in names
    assert "rot47" in names
    assert "morse" in names
    assert "fractionated_morse" in names
    assert "enigma" in names
    assert "chaocipher" in names
    assert "jefferson_disk" in names
    assert "autokey" in names
    assert "amsco_transposition" in names
    assert "beaufort" in names
    assert "columnar_transposition" in names
    assert "xor_cipher" in names
    assert "xor_base64" in names
    assert "polybius" in names
    assert "bifid" in names
    assert "gronsfeld" in names
    assert "porta" in names
    assert "trithemius" in names
    assert "scytale" in names
    assert "keyword_substitution" in names
    assert "myszkowski_transposition" in names
    assert "running_key" in names
    assert "route_cipher" in names
    assert "route_boustrophedon" in names
    assert "rot_n" in names
    assert "a1z26" in names
    assert "adfgvx" in names
    assert "adfgx" in names
    assert "one_time_pad" in names
    assert "tap_code" in names
    assert "two_square" in names
    assert "reverse_cipher" in names
    assert "caesar_box" in names
    assert "base64_cipher" in names
    assert "pig_latin" in names
    assert "playfair" in names
    assert "four_square" in names
    assert "vernam" in names
    assert "spiral_route" in names
    assert "paired_caesar" in names
    assert "caesar_progressive" in names
    assert "caesar_autoshift" in names
    assert "mirror_chunks" in names
    assert "hex_cipher" in names
    assert "rot5" in names
    assert "rot13" in names
    assert "reverse_words" in names
    assert "reverse_caesar" in names
    assert "leetspeak" in names
    assert "word_caesar" in names
    assert "rot18" in names
    assert "chunk_swap" in names
    assert "vowel_shift" in names
    assert "hill_cipher" in names
    assert "double_transposition" in names
    assert "substitution_monoalpha" in names
    assert "polyalpha_cycle" in names
    assert "permutation_blocks" in names
    assert "fibonacci_shift" in names
    assert "trinary_cipher" in names
    assert "trifid" in names
    assert "zigzag_words" in names
    assert "caesar_prime" in names
    assert "base32_cipher" in names
    assert "nato_phonetic" in names
    assert "braille_unicode" in names
    assert "keyboard_shift" in names
    assert "general_rot_n_with_custom_alphabet" in names
    assert "pigpen" in names
    assert "keyword_caesar" in names
    assert "null_cipher" in names
    assert "null_cipher_word_mode" in names
    assert "lfsr_toy" in names
    assert "feistel_toy" in names
    assert "spn_toy" in names
    assert "nihilist_substitution" in names
    assert "disrupted_transposition" in names
    assert "checkerboard_straddling" in names
    assert "multiplicative_cipher" in names
    assert "route_diagonal" in names
    assert "affine_progressive" in names
    assert "rail_fence_offset" in names
    assert "transpose_blocks" in names
    assert "beaufort_autokey" in names
    assert "rotating_caesar" in names
    assert "columnar_snake" in names
    assert "fibonacci_caesar" in names
    assert "diagonal_zigzag" in names
    assert "paired_vigenere" in names
    assert "route_columns_reverse" in names
    assert "triple_caesar" in names
    assert "rail_fence_variable" in names
    assert "langcheck" in names
    assert "alphabet_filter" in names


def test_loader_returns_modules():
    modules = load_online_modules(ONLINE_DIR, workers=4)
    assert "caesar" in modules
    assert modules["caesar"].caesar_encrypt("ABC", 3) == "DEF"


def test_cached_list_modules():
    first = list_online_modules_cached(ONLINE_DIR)
    second = list_online_modules_cached(ONLINE_DIR)
    assert first == second


def test_loader_report_and_filter():
    report = load_online_modules_with_report(
        ONLINE_DIR,
        module_filter=lambda name, _: name.startswith("b"),
    )
    assert report.errors == []
    assert set(report.modules) == {
        "baconian",
        "binary_cipher",
        "beaufort",
        "bifid",
        "base64_cipher",
        "base32_cipher",
        "braille_unicode",
        "beaufort_autokey",
    }


def test_cached_loader_report():
    clear_online_loader_cache()
    first = load_online_modules_with_report_cached(ONLINE_DIR)
    second = load_online_modules_with_report_cached(ONLINE_DIR)
    assert first.modules.keys() == second.modules.keys()
    assert first.errors == second.errors


def test_setup_provisions_modules(tmp_path):
    target = tmp_path / "seeded_online"
    result = setup(target, load=True)
    assert result.target_dir == target.resolve()
    assert len(result.copied) > 0
    assert result.report is not None
    assert "caesar" in result.report.modules


def test_setup_raises_on_missing_bundled_source(tmp_path):
    missing = tmp_path / "does_not_exist"
    try:
        setup(tmp_path / "target", bundled_online_dir=missing)
    except FileNotFoundError as exc:
        assert "bundled online module directory not found" in str(exc)
    else:
        raise AssertionError("expected FileNotFoundError")


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
    q1 = modules["quagmire_i"].quagmire_i_encrypt("Attack at dawn", plaintext_keyword="ALPHA", key="RIVER", indicator="D")
    assert modules["quagmire_i"].quagmire_i_decrypt(q1, plaintext_keyword="ALPHA", key="RIVER", indicator="D") == "Attack at dawn"
    q2 = modules["quagmire_ii"].quagmire_ii_encrypt("Attack at dawn", ciphertext_keyword="OMEGA", key="RIVER", indicator="D")
    assert modules["quagmire_ii"].quagmire_ii_decrypt(q2, ciphertext_keyword="OMEGA", key="RIVER", indicator="D") == "Attack at dawn"
    q3 = modules["quagmire_iii"].quagmire_iii_encrypt(
        "Attack at dawn",
        plaintext_keyword="ALPHA",
        ciphertext_keyword="OMEGA",
        key="RIVER",
        indicator="D",
    )
    assert modules["quagmire_iii"].quagmire_iii_decrypt(
        q3,
        plaintext_keyword="ALPHA",
        ciphertext_keyword="OMEGA",
        key="RIVER",
        indicator="D",
    ) == "Attack at dawn"

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
    chao = modules["chaocipher"].chaocipher_encrypt("WELL DONE IS BETTER THAN WELL SAID")
    assert modules["chaocipher"].chaocipher_decrypt(chao) == "WELL DONE IS BETTER THAN WELL SAID"

    m = modules["morse"].morse_encrypt("SOS 123")
    assert modules["morse"].morse_decrypt(m) == "SOS 123"
    fm = modules["fractionated_morse"].fractionated_morse_encrypt("ATTACK AT 0900", key="SECRET")
    assert modules["fractionated_morse"].fractionated_morse_decrypt(fm, key="SECRET") == "ATTACK AT 0900"
    nc = modules["null_cipher"].null_cipher_encrypt("HIDDEN", filler="Q", step=4)
    assert modules["null_cipher"].null_cipher_decrypt(nc, step=4) == "HIDDEN"
    ncw = modules["null_cipher_word_mode"].null_cipher_word_encrypt("hide this message", filler_word="zz", step=3)
    assert modules["null_cipher_word_mode"].null_cipher_word_decrypt(ncw, step=3) == "hide this message"
    lfsr = modules["lfsr_toy"].lfsr_toy_encrypt("stream cipher test", seed=0b110101010111)
    assert modules["lfsr_toy"].lfsr_toy_decrypt(lfsr, seed=0b110101010111) == "stream cipher test"
    ftl = modules["feistel_toy"].feistel_toy_encrypt("hello feistel", rounds=6, seed=77)
    assert modules["feistel_toy"].feistel_toy_decrypt(ftl, rounds=6, seed=77) == "hello feistel"
    spn = modules["spn_toy"].spn_toy_encrypt("hello spn", rounds=5, seed=123)
    assert modules["spn_toy"].spn_toy_decrypt(spn, rounds=5, seed=123) == "hello spn"

    ns = modules["nihilist_substitution"].nihilist_substitution_encrypt("ATTACKATDAWN", square_keyword="ALPHA", key="RIVER")
    assert modules["nihilist_substitution"].nihilist_substitution_decrypt(ns, square_keyword="ALPHA", key="RIVER") == "ATTACKATDAWN"

    dt = modules["disrupted_transposition"].disrupted_transposition_encrypt("MEETATNOON", "ZEBRA")
    assert modules["disrupted_transposition"].disrupted_transposition_decrypt(dt, "ZEBRA") == "MEETATNOON"

    cs = modules["checkerboard_straddling"].checkerboard_straddling_encrypt("HIDE MESSAGE", keyword="SECRET")
    assert modules["checkerboard_straddling"].checkerboard_straddling_decrypt(cs, keyword="SECRET") == "HIDE MESSAGE"

    mc = modules["multiplicative_cipher"].multiplicative_encrypt("Attack at Dawn", key=7)
    assert modules["multiplicative_cipher"].multiplicative_decrypt(mc, key=7) == "Attack at Dawn"

    rd = modules["route_diagonal"].route_diagonal_encrypt("WEAREDISCOVERED", columns=4, pad="_")
    assert modules["route_diagonal"].route_diagonal_decrypt(rd, columns=4, pad="_") == "WEAREDISCOVERED"

    ap = modules["affine_progressive"].affine_progressive_encrypt("Attack at Dawn", a=5, b0=3, step=2)
    assert modules["affine_progressive"].affine_progressive_decrypt(ap, a=5, b0=3, step=2) == "Attack at Dawn"

    rfo = modules["rail_fence_offset"].rail_fence_offset_encrypt("WEAREDISCOVEREDFLEEATONCE", rails=4, start_rail=1)
    assert modules["rail_fence_offset"].rail_fence_offset_decrypt(rfo, rails=4, start_rail=1) == "WEAREDISCOVEREDFLEEATONCE"

    tb = modules["transpose_blocks"].transpose_blocks_encrypt("MEETATNOON", block_size=5, perm=(2, 0, 4, 1, 3), pad="_")
    assert modules["transpose_blocks"].transpose_blocks_decrypt(tb, block_size=5, perm=(2, 0, 4, 1, 3), pad="_") == "MEETATNOON"

    ba = modules["beaufort_autokey"].beaufort_autokey_encrypt("Attack at Dawn", key="QUEEN")
    assert modules["beaufort_autokey"].beaufort_autokey_decrypt(ba, key="QUEEN") == "Attack at Dawn"

    rc = modules["rotating_caesar"].rotating_caesar_encrypt("Attack at Dawn", start_shift=2, step=3)
    assert modules["rotating_caesar"].rotating_caesar_decrypt(rc, start_shift=2, step=3) == "Attack at Dawn"

    csn = modules["columnar_snake"].columnar_snake_encrypt("WEAREDISCOVERED", key="ZEBRA", pad="_")
    assert modules["columnar_snake"].columnar_snake_decrypt(csn, key="ZEBRA", pad="_") == "WEAREDISCOVERED"

    fc = modules["fibonacci_caesar"].fibonacci_caesar_encrypt("Attack at Dawn")
    assert modules["fibonacci_caesar"].fibonacci_caesar_decrypt(fc) == "Attack at Dawn"

    dz = modules["diagonal_zigzag"].diagonal_zigzag_encrypt("WEAREDISCOVERED", width=5, pad="_")
    assert modules["diagonal_zigzag"].diagonal_zigzag_decrypt(dz, width=5, pad="_") == "WEAREDISCOVERED"

    pv = modules["paired_vigenere"].paired_vigenere_encrypt("Attack at Dawn", key_a="ALPHA", key_b="OMEGA")
    assert modules["paired_vigenere"].paired_vigenere_decrypt(pv, key_a="ALPHA", key_b="OMEGA") == "Attack at Dawn"

    rcr = modules["route_columns_reverse"].route_columns_reverse_encrypt("WEAREDISCOVERED", columns=4, pad="_")
    assert modules["route_columns_reverse"].route_columns_reverse_decrypt(rcr, columns=4, pad="_") == "WEAREDISCOVERED"

    tc = modules["triple_caesar"].triple_caesar_encrypt("Attack at Dawn", s1=2, s2=5, s3=9)
    assert modules["triple_caesar"].triple_caesar_decrypt(tc, s1=2, s2=5, s3=9) == "Attack at Dawn"

    rfv = modules["rail_fence_variable"].rail_fence_variable_encrypt("WEAREDISCOVEREDFLEEATONCE", rails=4, schedule=(0,1,2,3,2,1))
    assert modules["rail_fence_variable"].rail_fence_variable_decrypt(rfv, rails=4, schedule=(0,1,2,3,2,1)) == "WEAREDISCOVEREDFLEEATONCE"

    found, language = modules["langcheck"].langcheck_check("hello", wordlist_dir=ONLINE_DIR / "wordlist")
    assert found is True and language == "english"
    payload = modules["langcheck"].langcheck_encrypt("мир", wordlist_dir=ONLINE_DIR / "wordlist")
    parsed = modules["langcheck"].langcheck_decrypt(payload)
    assert parsed == (True, "russian")

    mixed = "Hello Привет Γειά σου مرحبا नमस्ते"
    assert modules["alphabet_filter"].alphabet_filter_encrypt(mixed, alphabet="latin") == "Hello"
    assert modules["alphabet_filter"].alphabet_filter_encrypt(mixed, alphabet="cyrillic") == "Привет"

    col = modules["columnar_transposition"].columnar_encrypt("WEAREDISCOVERED", "ZEBRA")
    assert modules["columnar_transposition"].columnar_decrypt(col, "ZEBRA") == "WEAREDISCOVERED"
    ams = modules["amsco_transposition"].amsco_encrypt("WEAREDISCOVEREDFLEEATONCE", key="CARGO")
    assert modules["amsco_transposition"].amsco_decrypt(ams, key="CARGO") == "WEAREDISCOVEREDFLEEATONCE"
    mysz = modules["myszkowski_transposition"].myszkowski_encrypt("WEAREDISCOVEREDFLEEATONCE", key="BALLOON")
    assert modules["myszkowski_transposition"].myszkowski_decrypt(mysz, key="BALLOON") == "WEAREDISCOVEREDFLEEATONCE"

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
    jef = modules["jefferson_disk"].jefferson_disk_encrypt("Attack at dawn!", wheels=(4, 2, 7))
    assert modules["jefferson_disk"].jefferson_disk_decrypt(jef, wheels=(4, 2, 7)) == "Attack at dawn!"

    scy = modules["scytale"].scytale_encrypt("WEAREDISCOVERED", 4)
    assert modules["scytale"].scytale_decrypt(scy, 4) == "WEAREDISCOVERED"

    kw = modules["keyword_substitution"].keyword_encrypt("HELLO", "SECRET")
    assert modules["keyword_substitution"].keyword_decrypt(kw, "SECRET") == "HELLO"

    rk = modules["running_key"].running_key_encrypt("HELLO", "XMCKLQWERTY")
    assert modules["running_key"].running_key_decrypt(rk, "XMCKLQWERTY") == "HELLO"

    route = modules["route_cipher"].route_encrypt("WEAREDISCOVERED", 5)
    assert modules["route_cipher"].route_decrypt(route, 5) == "WEAREDISCOVERED"
    rb = modules["route_boustrophedon"].route_boustrophedon_encrypt("WEAREDISCOVEREDFLEEATONCE", columns=6)
    assert modules["route_boustrophedon"].route_boustrophedon_decrypt(rb, columns=6) == "WEAREDISCOVEREDFLEEATONCE"
    rn = modules["rot_n"].rot_n_encrypt("Attack at Dawn", n=11)
    assert modules["rot_n"].rot_n_decrypt(rn, n=11) == "Attack at Dawn"
    grot = modules["general_rot_n_with_custom_alphabet"].general_rot_encrypt("ABCD-123", n=5, alphabet="ABCD1234")
    assert modules["general_rot_n_with_custom_alphabet"].general_rot_decrypt(grot, n=5, alphabet="ABCD1234") == "ABCD-123"

    code = modules["a1z26"].a1z26_encrypt("HELLO")
    assert modules["a1z26"].a1z26_decrypt(code) == "HELLO"
    adf = modules["adfgvx"].adfgvx_encrypt("ATTACKAT1200", square_keyword="SECRET", transposition_key="CARGO")
    assert modules["adfgvx"].adfgvx_decrypt(adf, square_keyword="SECRET", transposition_key="CARGO") == "ATTACKAT1200"
    adfgx = modules["adfgx"].adfgx_encrypt("ATTACKATDAWN", square_keyword="SECRET", transposition_key="CARGO")
    assert modules["adfgx"].adfgx_decrypt(adfgx, square_keyword="SECRET", transposition_key="CARGO") == "ATTACKATDAWN"

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
    fs = modules["four_square"].four_square_encrypt("DEFENDTHEEAST", key1="EXAMPLE", key2="KEYWORD")
    assert modules["four_square"].four_square_decrypt(fs, key1="EXAMPLE", key2="KEYWORD").startswith("DEFENDTHEEAST")
    ts = modules["two_square"].two_square_encrypt("HELPMEOBIWAN", key1="ALPHA", key2="OMEGA")
    assert modules["two_square"].two_square_decrypt(ts, key1="ALPHA", key2="OMEGA").startswith("HELPMEOBIWAN")

    ve = modules["vernam"].vernam_encrypt("HELLO", "XMCKL")
    assert modules["vernam"].vernam_decrypt(ve, "XMCKL") == "HELLO"

    sp = modules["spiral_route"].spiral_route_encrypt("WEAREDISCOVERED", 5)
    assert modules["spiral_route"].spiral_route_decrypt(sp, 5) == "WEAREDISCOVERED"

    pc = modules["paired_caesar"].paired_caesar_encrypt("Attack at dawn!", 1, 3)
    assert modules["paired_caesar"].paired_caesar_decrypt(pc, 1, 3) == "Attack at dawn!"

    prog = modules["caesar_progressive"].caesar_progressive_encrypt("Attack at dawn!", start_shift=1, step=2)
    assert modules["caesar_progressive"].caesar_progressive_decrypt(prog, start_shift=1, step=2) == "Attack at dawn!"
    auto = modules["caesar_autoshift"].caesar_autoshift_encrypt("Attack at dawn!", start_shift=2)
    assert modules["caesar_autoshift"].caesar_autoshift_decrypt(auto, start_shift=2) == "Attack at dawn!"

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
    rca = modules["reverse_caesar"].reverse_caesar_encrypt("Attack at dawn", shift=4)
    assert modules["reverse_caesar"].reverse_caesar_decrypt(rca, shift=4) == "Attack at dawn"

    leet = modules["leetspeak"].leetspeak_encrypt("state")
    assert modules["leetspeak"].leetspeak_decrypt(leet) == "STATE"
    pigp = modules["pigpen"].pigpen_encrypt("HELLO")
    assert modules["pigpen"].pigpen_decrypt(pigp) == "HELLO"
    nato = modules["nato_phonetic"].nato_phonetic_encrypt("HELLO WORLD")
    assert modules["nato_phonetic"].nato_phonetic_decrypt(nato) == "HELLO WORLD"
    bra = modules["braille_unicode"].braille_unicode_encrypt("HELLO")
    assert modules["braille_unicode"].braille_unicode_decrypt(bra) == "HELLO"
    kbd = modules["keyboard_shift"].keyboard_shift_encrypt("Attack at Dawn", right=True)
    assert modules["keyboard_shift"].keyboard_shift_decrypt(kbd, right=True) == "Attack at Dawn"

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

    sub = modules["substitution_monoalpha"].substitution_encrypt("Attack At Dawn")
    assert modules["substitution_monoalpha"].substitution_decrypt(sub) == "Attack At Dawn"

    pac = modules["polyalpha_cycle"].polyalpha_cycle_encrypt("Attack at dawn!", shifts=(1, 2, 3))
    assert modules["polyalpha_cycle"].polyalpha_cycle_decrypt(pac, shifts=(1, 2, 3)) == "Attack at dawn!"

    pb = modules["permutation_blocks"].permutation_blocks_encrypt("ABCDEFGHIJKL", perm=(2, 0, 3, 1))
    assert modules["permutation_blocks"].permutation_blocks_decrypt(pb, perm=(2, 0, 3, 1)) == "ABCDEFGHIJKL"

    fib = modules["fibonacci_shift"].fibonacci_shift_encrypt("Attack at dawn", seed_shift=2)
    assert modules["fibonacci_shift"].fibonacci_shift_decrypt(fib, seed_shift=2) == "Attack at dawn"

    tri = modules["trinary_cipher"].trinary_encrypt("abc")
    assert modules["trinary_cipher"].trinary_decrypt(tri) == "abc"
    tfd = modules["trifid"].trifid_encrypt("DEFEND THE EAST WALL", key="CIPHER")
    assert modules["trifid"].trifid_decrypt(tfd, key="CIPHER") == "DEFEND.THE.EAST.WALL"

    zig = modules["zigzag_words"].zigzag_words_encrypt("one two three four five")
    assert modules["zigzag_words"].zigzag_words_decrypt(zig) == "one two three four five"

    cp = modules["caesar_prime"].caesar_prime_encrypt("Attack at dawn", base_shift=1)
    assert modules["caesar_prime"].caesar_prime_decrypt(cp, base_shift=1) == "Attack at dawn"

    b32 = modules["base32_cipher"].base32_encrypt("hello")
    assert modules["base32_cipher"].base32_decrypt(b32) == "hello"

    kc = modules["keyword_caesar"].keyword_caesar_encrypt("Attack", keyword="alpha")
    assert modules["keyword_caesar"].keyword_caesar_decrypt(kc, keyword="alpha") == "Attack"
    xb = modules["xor_base64"].xor_base64_encrypt("hello 🌍", key="secret")
    assert modules["xor_base64"].xor_base64_decrypt(xb, key="secret") == "hello 🌍"

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


def test_cli_list_json_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "list", "--json"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "\"caesar\"" in out


def test_cli_list_json_command_with_cache():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "--cache", "list", "--json"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "\"caesar\"" in out


def test_cli_version_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "version"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert out == "2.6.2"


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


def test_cli_inspect_command():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "inspect",
        "--module",
        "caesar",
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "caesar_encrypt" in out


def test_cli_invoke_batch_command():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "invoke-batch",
        "--calls",
        '[{"module":"caesar","function":"caesar_encrypt","kwargs":{"plaintext":"ABC","shift":3}}]',
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "\"ok\": true" in out
    assert "DEF" in out


def test_cli_transform_command():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "transform",
        "--module",
        "caesar",
        "--mode",
        "encrypt",
        "--text",
        "ABC",
        "--params",
        "{\"shift\":3}",
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert out == "DEF"


def test_cli_benchmark_command():
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(ONLINE_DIR),
        "--cache",
        "benchmark",
        "--iterations",
        "2",
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "avg_ms" in out


def test_cli_setup_command(tmp_path):
    cmd = [
        sys.executable,
        "-m",
        "extirpation.cli",
        "--online-dir",
        str(tmp_path / "cli_online"),
        "setup",
    ]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "loaded_modules" in out


def test_cli_doctor_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "--online-dir", str(ONLINE_DIR), "doctor"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env())
    assert "module_count" in out
    assert "load_error_count" in out


def test_cli_clear_cache_command():
    cmd = [sys.executable, "-m", "extirpation.cli", "clear-cache"]
    out = subprocess.check_output(cmd, text=True, env=_cli_env()).strip()
    assert out == "cache cleared"


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
