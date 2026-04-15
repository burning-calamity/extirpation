# Wordlists

This folder stores language wordlists for cipher exercises.

## Layout
- `latin/`: languages that use the Latin alphabet.
- `cyrillic/`: languages that use Cyrillic scripts.
- `greek/`: languages that use Greek script.
- `arabic/`: languages that use Arabic script.
- `devanagari/`: languages that use Devanagari script.
- `hebrew/`: languages that use Hebrew script.
- `armenian/`: languages that use Armenian script.
- `georgian/`: languages that use Georgian script.
- `hangul/`: languages that use Hangul script.
- `bengali/`: languages that use Bengali script.
- `thai/`: languages that use Thai script.
- `ethiopic/`: languages that use Ethiopic (Geʽez) script.
- `tamil/`: languages that use Tamil script.
- `kana/`: languages that use Japanese kana.
- `han/`: languages that use Han characters (CJK).

Each language may include:
- a flat `<language>.txt` seed list for simple lookups, and/or
- a `<language>/` directory split by part of speech:
  - `nouns.txt`
  - `verbs.txt`
  - `adjectives.txt`
  - `names.txt` (optional)
- optional extras such as transliteration/frequency companion files.
- optional thematic packs in a `themes/` folder.

All files contain one entry per line, UTF-8 encoded.
