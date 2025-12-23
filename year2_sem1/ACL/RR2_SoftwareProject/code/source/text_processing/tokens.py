import re

def read_wordpieces(path):
    wp2id = {}
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                continue
            idx_str, wp = parts
            if wp == '\\s':
                wp = ' '
            wp2id[wp] = int(idx_str)

    sorted_wordpieces = sorted(wp2id.keys(), key=len, reverse=True)
    return wp2id, sorted_wordpieces

class Tokenizer:
    def __init__(self, wordpiece_file):
        self.wp2id, self.sorted_wordpieces = read_wordpieces(wordpiece_file)

        self.concept_pattern = re.compile(r"\[(FOODON_(\d+))\]")

    def greedy_wordpiece_tokenize(self, text):
        # Greedy longest-match wordpiece tokenizer
        i = 0
        n = len(text)
        pieces = []

        while i < n:
            matched = False

            # No whitespace skipping here — allow matching " "
            for wp in self.sorted_wordpieces:
                L = len(wp)
                if i + L <= n and text[i:i + L] == wp:
                    pieces.append(wp)
                    i += L
                    matched = True
                    break

            if matched:
                continue

            print(f"WARNING: Unmatchable text at position {i}: '{text[i]}'")
            i += 1

        return pieces

    def convert_sentence(self, line):
        result_ids = []
        idx = 0
        n = len(line)

        while idx < n:
            m = self.concept_pattern.match(line, idx)
            if m:
                cid = m.group(2)
                result_ids.append(f"c:{cid}")
                idx = m.end()
                continue

            next_concept = line.find("[FOODON_", idx)
            if next_concept == -1:
                next_concept = n

            segment = line[idx:next_concept]
            idx = next_concept

            pieces = self.greedy_wordpiece_tokenize(segment)
            for wp in pieces:
                if wp in self.wp2id:
                    result_ids.append(f"w:{self.wp2id[wp]}")
                else:
                    print(f"WARNING: wordpiece '{wp}' not in vocabulary")

        return " ".join(result_ids)

    def convert_corpus(self, infile, outfile):
        print(f"Processing {infile} → {outfile}")

        with open(infile, "r", encoding="utf8") as fin, \
                open(outfile, "w", encoding="utf8") as fout:

            for line in fin:
                line = line.strip()
                if not line:
                    fout.write("\n")
                    continue

                ids = self.convert_sentence(line)
                fout.write(ids + "\n")

