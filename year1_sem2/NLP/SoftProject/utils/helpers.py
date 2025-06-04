from collections import Counter
import numpy as np

def list_to_value_count_pairs(strings, as_counter=False):
    counter = Counter(strings)
    if as_counter: return counter
    return [[value, count] for value, count in counter.items()]

def to_categorical(y, num_classes):
    y = np.array(y)
    y_cat = np.zeros((*y.shape, num_classes), dtype=np.int32)
    for idx in np.ndindex(y.shape):
        label = y[idx]
        if label >= 0:
            y_cat[idx + (label,)] = 1
    return y_cat