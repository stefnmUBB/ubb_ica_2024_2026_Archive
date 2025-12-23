from source.embeddings import Vectorizer
from source import fileutils, annotate_text
from source.ml import *
import tensorflow as tf, numpy as np
from source.text_processing import normalize_line, Tokenizer

tokenizer = Tokenizer(fileutils.OUTPUT_WORDPIECES)

vec = Vectorizer(fileutils.OUTPUT_WORDPIECE_EMBEDDINGS,
                 fileutils.OUTPUT_CONCEPT_EMBEDDINGS, fileutils.OUTPUT_WORDPIECES,
                 fileutils.TOKENIZED_CORPUS_EN, fileutils.TOKENIZED_CORPUS_RO)

class SpecificMaskedAccuracy(MaskedCategoricalAccuracy):
    def __init__(self, name='masked_accuracy', **kwargs):
        super().__init__(name=name, pad_index=vec.cn_count, **kwargs)

def loss_fn(y_true, y_pred): return 0

data = vec.read_tokenized_paired_corpora(fileutils.TOKENIZED_CORPUS_EN, fileutils.TOKENIZED_CORPUS_RO)

val_split = 0.9

val_index = int(val_split*len(data))

val_data = data[val_index:]

model = tf.keras.models.load_model(fileutils.OUTPUT_MODEL("lstm_nmt_model"), custom_objects={
    'Perplexity': Perplexity,
    "MaskedCategoricalAccuracy": SpecificMaskedAccuracy,
    "SimpleSelfAttention": SimpleSelfAttention,
    'loss_fn': loss_fn
})


def translate(tokens):
    embeddings = vec.vectorize_seq(tokens)
    embeddings = np.expand_dims(embeddings, 0)
    #print(tokens)
    #print(embeddings.shape)
    result = model(embeddings).numpy().argmax(axis=-1)[0]
    result = vec.decode(result, map_wordpieces=False)
    print("PR = ", result)
    return result

from collections import Counter
import math

def ngram_counts(seq, n):
    return Counter(tuple(seq[i:i+n]) for i in range(len(seq)-n+1))

def bleu(y_true, y_pred, max_n=4):
    """
    Compute BLEU score between two sequences of tokens.
    y_true: list of reference tokens (GT)
    y_pred: list of predicted tokens (PR)
    max_n: maximum n-gram length
    """
    precisions = []
    for n in range(1, max_n+1):
        pred_ngrams = ngram_counts(y_pred, n)
        true_ngrams = ngram_counts(y_true, n)

        # Count overlapping ngrams
        overlap = sum(min(pred_ngrams[ng], true_ngrams.get(ng, 0)) for ng in pred_ngrams)
        total = sum(pred_ngrams.values())

        if total == 0:
            precisions.append(0)
        else:
            precisions.append(overlap / total)

    # Geometric mean of precisions
    if min(precisions) == 0:
        geo_mean = 0
    else:
        geo_mean = math.exp(sum(math.log(p) for p in precisions) / max_n)

    # Brevity penalty
    ref_len = len(y_true)
    pred_len = len(y_pred)
    if pred_len > ref_len:
        bp = 1
    elif pred_len == 0:
        bp = 0
    else:
        bp = math.exp(1 - ref_len / pred_len)

    return bp * geo_mean


def rouge_n(y_true, y_pred, n=2):
    """
    Compute ROUGE-N (recall) between reference and predicted sequences.
    """
    true_ngrams = ngram_counts(y_true, n)
    pred_ngrams = ngram_counts(y_pred, n)

    overlap = sum(min(pred_ngrams.get(ng, 0), count) for ng, count in true_ngrams.items())
    total = sum(true_ngrams.values())

    return overlap / total if total > 0 else 0.0


def lcs_length(x, y):
    """
    Compute length of Longest Common Subsequence (LCS) between sequences x and y.
    """
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            if x[i] == y[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
    return dp[m][n]


def rouge_l(y_true, y_pred):
    """
    Compute ROUGE-L (F1) between reference and prediction.
    """
    lcs = lcs_length(y_true, y_pred)
    if lcs == 0:
        return 0.0
    precision = lcs / len(y_pred)
    recall = lcs / len(y_true)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)

B = []
R = []
RL = []

for x,y in val_data:
    z = translate(x)
    print("GT", y)
    b = bleu(y, z)
    r = rouge_n(y,z)
    rl = rouge_l(y,z)
    print("B=", b)
    print("R=", r)
    print("RL=", rl)
    B.append(b)
    R.append(r)
    RL.append(rl)

B = np.array(B)
R = np.array(R)
RL = np.array(RL)
print("val mean BLEU-4 =", np.mean(B))
print("val mean ROUGE-2 =", np.mean(R))
print("val mean ROUGE-L =", np.mean(RL))
