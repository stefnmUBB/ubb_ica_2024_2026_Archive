import re
import math
from collections import Counter
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from rdflib import Graph, SKOS, RDF

# -------------------------------
# Tokenization
# -------------------------------
TOKEN_RE = re.compile(r'(\s+|[A-Za-zăâîșțĂÂÎȘȚ]+|\d+|[^\s])', flags=re.UNICODE)
def tokenize_with_ws(text):
    return TOKEN_RE.findall(text)

# -------------------------------
# Trigram vectors (cached)
# -------------------------------
def trigrams(word):
    w = f" {word.lower()} "
    return [w[i:i+3] for i in range(len(w)-2)]

@lru_cache(maxsize=200_000)
def trigram_vector_cached(word):
    return Counter(trigrams(word))

@lru_cache(maxsize=200_000)
def cosine_cached(a_frozenset, b_frozenset):
    a = dict(a_frozenset)
    b = dict(b_frozenset)
    dot = sum(a[k] * b.get(k, 0) for k in a)
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    if not na or not nb:
        return 0.0
    return dot/(na*nb)

def ordered_alignment_score_cached(window_vecs, concept_vecs):
    wi = 0
    last = -1
    score = 0.0
    gap_penalty = 0.0
    for cv in concept_vecs:
        best_s = 0.0
        best_pos = -1
        for i in range(wi, len(window_vecs)):
            s = cosine_cached(cv, window_vecs[i])
            if s > best_s:
                best_s = s
                best_pos = i
        if best_pos < 0:
            return 0.0
        if last != -1:
            gap_penalty += max(0, best_pos - last - 1) * 0.05
        score += best_s
        last = best_pos
        wi = best_pos + 1
    score /= len(concept_vecs)
    score -= gap_penalty
    return max(score, 0.0)

# -------------------------------
# Preprocess ontology
# -------------------------------
def preprocess_ontology(ontology):
    pre = {}
    for cid, variants in ontology.items():
        all_variants = []
        for label in variants:
            tokens = label.split()
            vecs = [frozenset(trigram_vector_cached(t).items()) for t in tokens]
            all_variants.append((tokens, vecs))
        pre[cid] = all_variants
    return pre

# -------------------------------
# Annotate text with stricter fuzzy matching
# -------------------------------
def annotate_text_preserve_ws(text, ontology_vec, base_threshold=0.55, max_window_words=8):
    tokens = tokenize_with_ws(text)
    word_indices = [i for i, tok in enumerate(tokens) if not tok.isspace()]
    out_tokens = []
    idx = 0
    wi_ptr = 0
    while idx < len(tokens):
        if tokens[idx].isspace():
            out_tokens.append(tokens[idx])
            idx += 1
            continue
        while wi_ptr < len(word_indices) and word_indices[wi_ptr] < idx:
            wi_ptr += 1
        if wi_ptr >= len(word_indices) or word_indices[wi_ptr] != idx:
            out_tokens.append(tokens[idx])
            idx += 1
            continue
        best_label = None
        best_score = 0.0
        best_span = 1
        remaining_positions = word_indices[wi_ptr:]
        for span in range(1, min(max_window_words, len(remaining_positions)) + 1):
            window_tokens = [tokens[pos] for pos in remaining_positions[:span]]
            # Skip very short single-word tokens
            if span == 1 and len(window_tokens[0]) < 4:
                continue
            window_vecs = [frozenset(trigram_vector_cached(t).items()) for t in window_tokens]
            for cid, variants in ontology_vec.items():
                for var_tokens, var_vecs in variants:
                    if len(var_tokens) != span:
                        continue
                    # Length-dependent threshold
                    threshold = base_threshold
                    if span == 1:
                        threshold = max(0.75, base_threshold)  # stricter for single-word
                    s = ordered_alignment_score_cached(window_vecs, var_vecs)
                    if s > best_score and s >= threshold:
                        best_score = s
                        best_label = cid
                        best_span = span
        if best_label:
            span_start = word_indices[wi_ptr]
            span_end = word_indices[wi_ptr + best_span - 1]
            out_tokens.append(f"[{best_label}]")
            for j in range(span_start, span_end + 1):
                out_tokens.append(tokens[j])
            idx = span_end + 1
            wi_ptr += best_span
        else:
            out_tokens.append(tokens[idx])
            idx += 1
            wi_ptr += 1
    return "".join(out_tokens)

# -------------------------------
# TTL Ontology Loader
# -------------------------------
def load_ontology_ttl(filename):
    g = Graph()
    g.parse(filename, format="ttl")
    ontology_en, ontology_ro = {}, {}
    for subj in g.subjects(RDF.type, None):
        node_id = str(subj).split("/")[-1]
        en_labels = [str(label) for label in g.objects(subj, SKOS.prefLabel) if label.language and label.language.lower() == "en"]
        ro_labels = [str(label) for label in g.objects(subj, SKOS.prefLabel) if label.language and label.language.lower() == "ro"]
        for label in g.objects(subj, SKOS.altLabel):
            if label.language and label.language.lower() == "en":
                en_labels.append(str(label))
            elif label.language and label.language.lower() == "ro":
                ro_labels.append(str(label))
        if en_labels: ontology_en[f"FOODON_{node_id}"] = en_labels
        if ro_labels: ontology_ro[f"FOODON_{node_id}"] = ro_labels
    return ontology_en, ontology_ro

# -------------------------------
# Parallel annotation with sample print
# -------------------------------
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def parallel_annotate(input_file, output_file, ontology_vec, max_workers=4, sample_interval=200):
    with open(input_file, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    results = [""] * len(lines)
    counter = 0

    # Submit tasks
    futures_to_idx = {}
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i, line in enumerate(lines):
            # Submit each line for annotation
            future = executor.submit(annotate_text_preserve_ws, line, ontology_vec)
            futures_to_idx[future] = i

        # Process completed tasks as they finish
        for fut in tqdm(as_completed(futures_to_idx), total=len(futures_to_idx), desc=output_file, unit="line"):
            idx = futures_to_idx[fut]
            results[idx] = fut.result()
            counter += 1

            if counter % sample_interval == 0:
                print(f"\n--- Sample annotated line at {counter} ---")
                print(results[idx].strip())
                print("-----------------------------------------\n")

    with open(output_file, "w", encoding="utf-8") as fout:
        fout.writelines(results)


from tqdm import tqdm

def serial_annotate(input_file, output_file, ontology_vec, sample_interval=200):
    with open(input_file, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    results = []
    counter = 0

    for line in tqdm(lines, desc=output_file, unit="line"):
        annotated_line = annotate_text_preserve_ws(line, ontology_vec)
        results.append(annotated_line)
        counter += 1

        if counter % sample_interval == 0:
            print(f"\n--- Sample annotated line at {counter} ---")
            print(annotated_line.strip())
            print("-----------------------------------------\n")

    with open(output_file, "w", encoding="utf-8") as fout:
        fout.writelines(results)


print("[text_processing.annotate] Intializing")
from ..fileutils import MINI_FOOD_ONTOLOGY_RO
ontology_en, ontology_ro = load_ontology_ttl(MINI_FOOD_ONTOLOGY_RO)
ontology_en_vec = preprocess_ontology(ontology_en)
ontology_ro_vec = preprocess_ontology(ontology_ro)
print("[text_processing.annotate] Intialized")

def annotate_text(text, lang='en'):
    return annotate_text_preserve_ws(text, ontology_en_vec if lang=='en' else ontology_ro_vec)

def parallel_annotate_corpus(input_file, output_file, lang, max_workers=4, sample_interval=200):
    ontology_vec = ontology_en_vec if lang=='en' else ontology_ro_vec
    parallel_annotate(input_file, output_file, ontology_vec, max_workers, sample_interval)

def serial_annotate_corpus(input_file, output_file, lang, sample_interval=200):
    ontology_vec = ontology_en_vec if lang=='en' else ontology_ro_vec
    serial_annotate(input_file, output_file, ontology_vec, sample_interval)

