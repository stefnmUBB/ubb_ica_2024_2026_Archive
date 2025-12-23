import re
from collections import Counter
from tqdm import tqdm   # <-- added

# =========================
# CONFIGURATION
# =========================
WORD_PIECES_COUNT = 1024
BASE_PIECES = [
    '\n', ' ', '!', '"', '#', '%', '&', "'", '(', ')', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', '`',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'â', 'î', 'ă', 'ș', 'ț'
]

CONCEPT_PATTERN = re.compile(r'\[(FOODON_[0-9]+)\]')
SEPARATOR_PATTERN = re.compile(
    r'(\s+|[!"#%&\'(),\-./:;?`0-9]+|\[FOODON_[0-9]+\])'
)


def compute_wordpieces(corpora_paths, concepts_path, wordpieces_path):
    # =========================
    # LOAD AND MERGE TEXT
    # =========================
    merged = ""
    for path in corpora_paths:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            if len(merged)==0:
                merged = text
            else:
                merged += "\n"+text

    # =========================
    # EXTRACT CONCEPTS
    # =========================
    concepts = set(CONCEPT_PATTERN.findall(merged))
    with open(concepts_path, "w", encoding="utf-8") as f:
        for c in sorted(concepts):
            f.write(c + "\n")

    # =========================
    # SPLIT INTO WORD SEGMENTS
    # =========================
    segments = []
    for part in SEPARATOR_PATTERN.split(merged):
        if part and not SEPARATOR_PATTERN.fullmatch(part):
            segments.append(part)

    tokenized = [list(seg) for seg in segments if seg]


    # =========================
    # BPE TRAINING
    # =========================
    def get_pair_counts(sequences):
        counts = Counter()
        for seq in sequences:
            for i in range(len(seq) - 1):
                counts[(seq[i], seq[i+1])] += 1
        return counts

    def merge_pair(pair, sequences):
        a, b = pair
        merged_token = a + b
        new_sequences = []

        # tqdm to visualize sequence rewriting per iteration
        for seq in tqdm(sequences, desc="Merging sequences", leave=False):
            i = 0
            new_seq = []
            while i < len(seq):
                if i < len(seq) - 1 and seq[i] == a and seq[i+1] == b:
                    new_seq.append(merged_token)
                    i += 2
                else:
                    new_seq.append(seq[i])
                    i += 1
            new_sequences.append(new_seq)

        return merged_token, new_sequences


    vocab = list(BASE_PIECES)
    bpe_sequences = tokenized

    # tqdm over BPE iterations
    pbar = tqdm(total=WORD_PIECES_COUNT - len(vocab), desc="BPE merges")

    while len(vocab) < WORD_PIECES_COUNT:
        pair_counts = get_pair_counts(bpe_sequences)
        if not pair_counts:
            break

        best_pair, freq = pair_counts.most_common(1)[0]
        new_piece, bpe_sequences = merge_pair(best_pair, bpe_sequences)

        vocab.append(new_piece)
        pbar.update(1)

        if freq == 0:
            break

    pbar.close()

    # =========================
    # OUTPUT WORDPIECES
    # =========================
    with open(wordpieces_path, "w", encoding="utf-8") as f:
        for idx, piece in enumerate(vocab):
            text = "\\n" if piece == "\n" else piece
            f.write(f"{idx} {text}\n")
