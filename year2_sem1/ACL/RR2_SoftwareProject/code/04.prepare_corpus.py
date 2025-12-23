import rdflib, random, re
from tqdm import tqdm
from source import fileutils

# --- Paths ---
ontology_path = fileutils.MINI_FOOD_ONTOLOGY_RO
en_path = fileutils.INPUT_CORPUS_EN
ro_path = fileutils.INPUT_CORPUS_RO
out_en = fileutils.FILTERED_CORPUS_EN
out_ro = fileutils.FILTERED_CORPUS_RO

# --- 1. Load ontology and extract en-ro label pairs ---
print("Loading ontology...")
g = rdflib.Graph()
g.parse(ontology_path, format="turtle")

pairs = []
for s, p, o in tqdm(
    g.triples((None, rdflib.term.URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"), None)),
    desc="Extracting labels"
):
    if isinstance(o, rdflib.Literal) and o.language in ("en", "ro"):
        pairs.append((s, o.language, str(o)))

concepts = {}
for subj, lang, label in pairs:
    concepts.setdefault(subj, {})[lang] = label.lower()

label_pairs = [(v["en"], v["ro"]) for v in concepts.values() if "en" in v and "ro" in v]

en_terms = [re.escape(en) for en, _ in label_pairs]
ro_terms = [re.escape(ro) for _, ro in label_pairs]
en_pattern = re.compile(r"\b(" + "|".join(en_terms) + r")\b", re.IGNORECASE)
ro_pattern = re.compile(r"\b(" + "|".join(ro_terms) + r")\b", re.IGNORECASE)

print(r"\b(" + "|".join(en_terms) + r")\b")
print(r"\b(" + "|".join(ro_terms) + r")\b")

print(f"Extracted {len(label_pairs)} English–Romanian concept pairs.\n")

# --- 2. Load corpus ---
print("Loading WikiMatrix corpus...")
with open(en_path, encoding="utf-8") as f_en, open(ro_path, encoding="utf-8") as f_ro:
    en_lines = f_en.readlines()
    ro_lines = f_ro.readlines()

assert len(en_lines) == len(ro_lines), "Parallel files must have the same number of lines."

# --- 3. Filter corpus with ontology terms ---
print("Filtering relevant sentence pairs...")
filtered_en, filtered_ro = [], []

for en_sent, ro_sent in tqdm(zip(en_lines, ro_lines), total=len(en_lines), desc="Scanning corpus"):
    en_match = en_pattern.search(en_sent.lower())
    ro_match = ro_pattern.search(ro_sent.lower())

    if en_match or ro_match:
        # Debug: show what matched and where
        if en_match:
            print(f"[EN MATCH] '{en_match.group(0)}' in: {en_sent.strip()}")
        if ro_match:
            print(f"[RO MATCH] '{ro_match.group(0)}' in: {ro_sent.strip()}")

        filtered_en.append(en_sent)
        filtered_ro.append(ro_sent)

print(f"Found {len(filtered_en)} ontology-related sentence pairs.\n")

# --- 4. Add random general examples ---
num_extra = int(0.2 * len(filtered_en))
indices = random.sample(range(len(en_lines)), num_extra)

#print(f"Adding {num_extra} random general sentence pairs...")
#for idx in tqdm(indices, desc="Sampling random pairs"):
#    filtered_en.append(en_lines[idx])
#    filtered_ro.append(ro_lines[idx])

# --- 5. Shuffle and save ---
combined = list(zip(filtered_en, filtered_ro))
random.shuffle(combined)
final_en, final_ro = zip(*combined)

print("Saving filtered data...")
with open(out_en, "w", encoding="utf-8") as f_en, open(out_ro, "w", encoding="utf-8") as f_ro:
    for e, r in tqdm(zip(final_en, final_ro), total=len(final_en), desc="Writing files"):
        f_en.write(e)
        f_ro.write(r)

print(f"\nSaved {len(final_en)} pairs to {out_en} and {out_ro}.")
