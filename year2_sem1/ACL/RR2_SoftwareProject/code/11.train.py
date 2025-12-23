import itertools

import tensorflow as tf
from source.embeddings import Vectorizer
from source import fileutils
from source.ml import *

vec = Vectorizer(fileutils.OUTPUT_WORDPIECE_EMBEDDINGS,
                 fileutils.OUTPUT_CONCEPT_EMBEDDINGS, fileutils.OUTPUT_WORDPIECES,
                 fileutils.TOKENIZED_CORPUS_EN, fileutils.TOKENIZED_CORPUS_RO)

data = vec.read_tokenized_paired_corpora(fileutils.TOKENIZED_CORPUS_EN, fileutils.TOKENIZED_CORPUS_RO)

val_split = 0.9

val_index = int(val_split*len(data))

train_data = vec.make_dataset(data[:val_index])
val_data = vec.make_dataset(data[val_index:])

def build_lstm_model(
    max_seq_len,
    embedding_size,
    vocab_size,
    lstm_units=256,
):
    inputs = tf.keras.Input(
        shape=(max_seq_len, embedding_size),
        name="input_embeddings"
    )

    # --- BiLSTM outputs 1024 ---
    x = tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(lstm_units, return_sequences=True)
    )(inputs)

    x = tf.keras.layers.LayerNormalization()(x)

    # --- Project 1024 → 512 so residual works ---
    x_proj = tf.keras.layers.Dense(lstm_units)(x)

    # --- 512-dim LSTM ---
    x2 = tf.keras.layers.LSTM(lstm_units, return_sequences=True)(x_proj)

    # --- Residual add (now both are 512) ---
    x = tf.keras.layers.Add()([x_proj, x2])
    x = tf.keras.layers.LayerNormalization()(x)

    # --- Multi-head Attention (512-dim) ---
    att = tf.keras.layers.MultiHeadAttention(
        num_heads=8,
        key_dim=lstm_units // 8
    )(x, x)

    x = tf.keras.layers.Dropout(0.1)(x)

    x = tf.keras.layers.Add()([x, att])
    x = tf.keras.layers.LayerNormalization()(x)

    # --- FFN block ---
    ffn = tf.keras.Sequential([
        tf.keras.layers.Dense(lstm_units * 4, activation="relu"),
        tf.keras.layers.Dense(lstm_units),
    ])
    ffn_out = ffn(x)

    x = tf.keras.layers.Add()([x, ffn_out])
    x = tf.keras.layers.LayerNormalization()(x)

    # --- Output softmax ---
    outputs = tf.keras.layers.TimeDistributed(
        tf.keras.layers.Dense(vocab_size, activation="softmax")
    )(x)

    return tf.keras.Model(inputs=inputs, outputs=outputs)



model = build_lstm_model(vec.max_seq_len, vec.embedding_size, vec.cat_count, lstm_units=512)
model.summary()

def focal_loss(gamma=2.0):
    def loss_fn(y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0)
        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = tf.pow(1 - y_pred, gamma)
        return tf.reduce_mean(weight * cross_entropy)
    return loss_fn

import tensorflow as tf

def combined_loss(alpha=1.0, beta=1.0, gamma=2.0, token_weights=None):
    ce = tf.keras.losses.CategoricalCrossentropy(from_logits=False, label_smoothing=0.1)

    def loss_fn(y_true, y_pred):
        # --- Categorical Crossentropy ---
        ce_loss = ce(y_true, y_pred)

        # --- Focal loss ---
        y_pred_clipped = tf.clip_by_value(y_pred, 1e-7, 1.0)
        focal_weight = tf.pow(1 - y_pred_clipped, gamma)
        focal_loss = -y_true * tf.math.log(y_pred_clipped) * focal_weight
        focal_loss = tf.reduce_mean(focal_loss)

        # --- Optional token weighting ---
        if token_weights is not None:
            weights = tf.reduce_sum(y_true * token_weights, axis=-1)
            ce_loss *= weights
            focal_loss *= weights

        return alpha * ce_loss + beta * focal_loss

    return loss_fn


# Loss & optimizer
loss_fn = combined_loss(1, 5)
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

perplexity = Perplexity()

pad_index = vec.cn_count + 0  # corresponds to 'w:0'
masked_acc = MaskedCategoricalAccuracy(pad_index=pad_index)

model.compile(
    optimizer=optimizer,
    loss=loss_fn,
    metrics=[masked_acc, perplexity]
)

checkpoint_path = fileutils.OUTPUT_MODEL("lstm_nmt_model_chp_ls_lr1e-4")

checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    save_weights_only=False,
    save_best_only=False,       # save every N epochs
    save_freq='epoch',  # every epoch
    verbose=1
)


history = model.fit(
    train_data.batch(32),
    validation_data=val_data.batch(32),
    epochs=100,
    callbacks=[checkpoint_cb]
)



model.save(fileutils.OUTPUT_MODEL("lstm_nmt_model"))

def create_fig(history):
    import matplotlib.pyplot as plt

    # metrics to plot (must exist in history.history)
    keys = [
        ("loss", "Loss"),
        ("val_loss", "Validation Loss"),
        ("masked_accuracy", "Masked Accuracy"),
        ("val_masked_accuracy", "Validation Masked Accuracy"),
        ("perplexity", "Perplexity"),
        ("val_perplexity", "Validation Perplexity"),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()

    for ax, (key, title) in zip(axes, keys):
        if key in history.history:
            ax.plot(history.history[key])
            ax.set_title(title)
            ax.set_xlabel("Epoch")
            ax.set_ylabel(title)
            ax.grid(True)
        else:
            ax.set_title(f"{title} (missing)")
            ax.axis("off")

    plt.tight_layout()
    plt.savefig( fileutils.OUTPUT_FIG("training_history"), dpi=200)
    plt.close()

create_fig(history)