import csv
import numpy as np
import tensorflow as tf
import random
from collections import Counter

MAX_SEQ_LENGTH = 256

def read_vectors(filename, type_value=1.0):
    """
    Reads a CSV file with columns: id, e0, e1, ..., eN-1
    Returns a dictionary: {id: vector}, where each vector is a numpy array
    of shape (N+1,) with the first element set to type_value and the rest from the CSV.
    """
    vectors = {}
    with open(filename, "r", encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header

        for row in reader:
            if not row:
                continue
            key = row[0]  # first column is id
            # convert rest to float
            vec = np.array([float(x) for x in row[1:]], dtype=np.float32)
            # prepend type_value
            vec = np.insert(vec, 0, type_value)
            vectors[key] = vec

    return vectors

def read_wordpieces(path):
    wordpieces = {}
    with open(path,'r', encoding='utf8') as f:
        for line in f.read().splitlines():
            wid, wval = line.split(' ')
            if wval == '\\s': wval=' '
            if wval == '\\n': wval='\n'
            wordpieces[wid]=wval
    return wordpieces

class Vectorizer:
    def __init__(self, wordpiece_embeddings_path, concept_embeddings_path, wordpieces_path,
                 tokenized_corpus_en_path, tokenized_corpus_ro_path):
        # wordpiece vectors
        self.wp_vecs = read_vectors(wordpiece_embeddings_path, 1.0)
        # ontology concepts
        self.cn_vecs = read_vectors(concept_embeddings_path, -1.0)
        # remove non-terminal nodes (not used in annotation)
        self.cn_vecs = {k: v for k, v in self.cn_vecs.items() if not k.startswith('FOODON_')}

        self.data = self.read_tokenized_paired_corpora(tokenized_corpus_en_path, tokenized_corpus_ro_path)
        data_concepts = [
            t.split(':')[1]
            for x, y in self.data
            for t in (*x, *y)
            if t.startswith("c")
        ]

        top128 = [x for x, _ in Counter(data_concepts).most_common(128)]
        self.cn_vecs = {k: v for k, v in self.cn_vecs.items() if k in top128}
        # concepts count
        self.cn_count = len(self.cn_vecs)

        # mappings concept <-> category id
        self.concept2catid = {}
        self.catid2concept = {}

        for conceptId in sorted(self.cn_vecs.keys()):
            catId = len(self.catid2concept)
            self.concept2catid[conceptId] = catId
            self.catid2concept[catId] = conceptId
            catId += 1

        self.wordpieces = read_wordpieces(wordpieces_path)
        self.wp_count = len(self.wordpieces)
        # final categories count
        self.cat_count = self.cn_count + self.wp_count

        self.max_seq_len = MAX_SEQ_LENGTH
        self.embedding_size = self.wp_vecs["0"].shape[0]

    def normalize_seq(self, x):
        # Remove any leftover concepts that appear in corpus but not in embeddings
        x = [t for t in x if not (t.startswith('c:') and t.split(':', 1)[1] not in self.concept2catid)]
        # pad with null tokens till max length
        if len(x) < MAX_SEQ_LENGTH:
            x += ['w:0'] * (MAX_SEQ_LENGTH - len(x))
        return x

    def vectorize_seq(self, x):
        x = self.normalize_seq(x)
        return np.array([self.vectorize_token(t) for t in x])

    def categorize_seq(self, x, to_categorical=True):
        x = self.normalize_seq(x)
        x = np.array([self.categorize_token(t) for t in x])
        if not to_categorical:
            return x
        return np.eye(self.cat_count, dtype=float)[x]

    def vectorize_token(self, tk):
        tk_type, tk_id = tk.split(':')[:2]
        if tk_type == 'w':
            return self.wp_vecs[tk_id]
        if tk_type == 'c':
            return self.cn_vecs[tk_id]
        raise ValueError(f"Invalid type: '{tk_type}:{tk_id}'")

    def categorize_token(self, tk):
        tk_type, tk_id = tk.split(':')[:2]
        if tk_type == 'c':
            return self.concept2catid[tk_id]
        if tk_type == 'w':
            return self.cn_count + int(tk_id)
        raise ValueError(f"Invalid type: '{tk_type}:{tk_id}'")

    def make_dataset(self, paired_tokenized_sequences):
        paired_tokenized_sequences_sorted = list(sorted(paired_tokenized_sequences, key=lambda p:len(p[0])+len(p[1])))
        length_factor ={'value':10}

        L = len(paired_tokenized_sequences)

        def generator():
            i = 0
            while i<L:
                coll = paired_tokenized_sequences_sorted[:length_factor['value']*len(paired_tokenized_sequences_sorted)//100]
                random.shuffle(coll)
                for x, y in coll:
                    yield self.vectorize_seq(x), self.categorize_seq(y, to_categorical=True)
                    i+=1
                    if i>=L: break
                for _ in range(5):
                    p = random.randint(0, L)
                    x,y = paired_tokenized_sequences_sorted[p]
                    yield self.vectorize_seq(x), self.categorize_seq(y, to_categorical=True)
                    i += 1
                    if i >= L: break
            length_factor['value'] = min(length_factor['value']+1, 100)

        return tf.data.Dataset.from_generator(
            generator,
            output_signature=(
                tf.TensorSpec(shape=(MAX_SEQ_LENGTH, self.embedding_size), dtype=tf.float32),
                tf.TensorSpec(shape=(MAX_SEQ_LENGTH, self.cat_count), dtype=tf.float32)
            )
        ).shuffle(103)

    def read_tokenized_corpus(self, path):
        lines = []
        with open(path, 'r') as f:
            for line in f.read().splitlines():
                lines.append(line.split(' '))
        return lines

    def read_tokenized_paired_corpora(self, en_path, ro_path):
        en_lines = self.read_tokenized_corpus(en_path)
        ro_lines = self.read_tokenized_corpus(ro_path)
        data = list(zip(en_lines, ro_lines))
        # force max seq length
        data = [(x, y) for x, y in data if len(x) <= MAX_SEQ_LENGTH and len(y) <= MAX_SEQ_LENGTH]
        return data

    def decode(self, token_ids, map_wordpieces=True):
        result = [f"w:{tk-self.cn_count}" if tk>=self.cn_count else f"c:{tk}" for tk in token_ids]
        i = len(result)-1
        while result[i]=='w:0' and i>0:
            i-=1
        result = result[:i]

        if map_wordpieces:
            result = [self.wordpieces[tk.split(':')[1]] if tk.startswith('w') else tk for tk in result]

        return result

