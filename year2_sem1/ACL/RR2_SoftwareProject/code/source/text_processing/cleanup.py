import re
import unicodedata
import sys

# Allowed characters
BASE_LATIN = "abcdefghijklmnopqrstuvwxyz"
ROMANIAN_DIACRITICS = "șțăîâ"
DIGITS = "0123456789"
ALLOWED_PUNCTUATION = '.,!?"`-&()\'/:;%'

SYMBOL_NORMALIZATION = {
    "–": "-",
    "—": "-",
    "“": '"',
    "”": '"',
    "„": '"',
    "‘": "'",
    "’": "'",
    "…": "...",
    "ß": "ss"
}

def progress_bar(current, total, width=40):
    filled = int(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    percent = (current / total) * 100
    sys.stdout.write(f"\r[{bar}] {percent:5.1f}%")
    sys.stdout.flush()

# Strip accents from a character except Romanian diacritics
def normalize_char(ch: str) -> str:
    ch_lower = ch.lower()
    if ch_lower in ROMANIAN_DIACRITICS:
        return ch_lower
    if ch_lower in BASE_LATIN:
        return ch_lower
    if unicodedata.category(ch).startswith('L'):
        base = unicodedata.normalize('NFKD', ch)[0].lower()
        if base in BASE_LATIN:
            return base
    return None

def normalize_line(line: str) -> str:
    # Map symbol variants inside the line only
    for k, v in SYMBOL_NORMALIZATION.items():
        line = line.replace(k, v)

    result = []
    for ch in line:
        if ch.isspace() or ch in DIGITS or ch in ALLOWED_PUNCTUATION:
            result.append(ch)
        else:
            normalized = normalize_char(ch)
            result.append(normalized if normalized is not None else "#")

    cleaned = "".join(result)

    # Fix casing but only PER LINE
    def fix_casing(s: str) -> str:
        if s.islower() or s.isupper():
            return s.lower()
        s_stripped = s.strip()
        if len(s_stripped) > 1 and s_stripped[0].isupper() and s_stripped[1:].islower():
            return s_stripped[0].upper() + s_stripped[1:].lower()
        return s.lower()

    return fix_casing(cleaned)

def preprocess_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    print(f"Processing {filename} ({total} lines)...")

    output_lines = []
    for i, line in enumerate(lines):
        output_lines.append(normalize_line(line.rstrip("\n")))
        progress_bar(i + 1, total)

    print()  # newline after bar
    return output_lines
