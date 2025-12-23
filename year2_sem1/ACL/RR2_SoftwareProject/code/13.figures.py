from source.embeddings import Vectorizer
from source import fileutils, OUTPUT_FIG
from source.ml import *
import numpy as np, tensorflow as tf
from tensorflow.keras.utils import plot_model


vec = Vectorizer(fileutils.OUTPUT_WORDPIECE_EMBEDDINGS,
                 fileutils.OUTPUT_CONCEPT_EMBEDDINGS, fileutils.OUTPUT_WORDPIECES,
                 fileutils.TOKENIZED_CORPUS_EN, fileutils.TOKENIZED_CORPUS_RO)

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

wordpiece_embeddings = np.array(list(vec.wp_vecs.values()))

# Assuming concept_embeddings is your (127, 128) array
pca = PCA(n_components=2)
wp_2d = pca.fit_transform(wordpiece_embeddings)

# Simple scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(wp_2d[:, 0], wp_2d[:, 1], c='blue', alpha=0.7)

# Optional: annotate points with indices
for i, (x, y) in enumerate(wp_2d):
    plt.text(x, y, str(i), fontsize=8, alpha=0.7)

plt.title("PCA of Wordpiece Embeddings")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.savefig(fileutils.OUTPUT_FIG("pca_wordpiece_embeddings"))


exit(0)

class SpecificMaskedAccuracy(MaskedCategoricalAccuracy):
    def __init__(self, name='masked_accuracy', **kwargs):
        super().__init__(name=name, pad_index=vec.cn_count, **kwargs)

def loss_fn(y_true, y_pred): return 0

model = tf.keras.models.load_model(fileutils.OUTPUT_MODEL("lstm_nmt_model"), custom_objects={
    'Perplexity': Perplexity,
    "MaskedCategoricalAccuracy": SpecificMaskedAccuracy,
    "SimpleSelfAttention": SimpleSelfAttention,
    'loss_fn': loss_fn
})

plot_model(model, to_file=OUTPUT_FIG("model"),
           show_shapes=True, show_layer_names=True, rankdir='TB', expand_nested=True
)

exit(0)

concept_embeddings = np.array(list(vec.cn_vecs.values()))

print(concept_embeddings.shape) # (127, 128)

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

# Assuming concept_embeddings is your (127, 128) array
pca = PCA(n_components=2)
concepts_2d = pca.fit_transform(concept_embeddings)

# Simple scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(concepts_2d[:, 0], concepts_2d[:, 1], c='blue', alpha=0.7)

# Optional: annotate points with indices
for i, (x, y) in enumerate(concepts_2d):
    plt.text(x, y, str(i), fontsize=8, alpha=0.7)

plt.title("PCA of Concept Embeddings")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.savefig(fileutils.OUTPUT_FIG("pca_concept_embeddings"))

############################################################################

import matplotlib.pyplot as plt
from collections import Counter

# vec.data is a list of tuples (x_list, y_list)
x_list_all = [item for x, _ in vec.data for item in x]
y_list_all = [item for _, y in vec.data for item in y]

# Separate wordpieces and concepts
x_wp = [int(i.split(':')[1]) for i in x_list_all if i.startswith('w:')]
x_c = [int(i.split(':')[1]) for i in x_list_all if i.startswith('c:')]

y_wp = [int(i.split(':')[1]) for i in y_list_all if i.startswith('w:')]
y_c = [int(i.split(':')[1]) for i in y_list_all if i.startswith('c:')]

# Plot histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].hist(x_wp, bins=50, color='skyblue')
axes[0, 0].set_title('Wordpiece IDs in x')
axes[0, 0].set_xlabel('ID')
axes[0, 0].set_ylabel('Frequency')

axes[0, 1].hist(y_wp, bins=50, color='lightgreen')
axes[0, 1].set_title('Wordpiece IDs in y')
axes[0, 1].set_xlabel('ID')
axes[0, 1].set_ylabel('Frequency')

axes[1, 0].hist(x_c, bins=50, color='salmon')
axes[1, 0].set_title('Concept IDs in x')
axes[1, 0].set_xlabel('ID')
axes[1, 0].set_ylabel('Frequency')

axes[1, 1].hist(y_c, bins=50, color='orange')
axes[1, 1].set_title('Concept IDs in y')
axes[1, 1].set_xlabel('ID')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig(fileutils.OUTPUT_FIG("total_frequencies"))
