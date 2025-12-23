import tensorflow as tf

class MaskedCategoricalAccuracy(tf.keras.metrics.Metric):
    def __init__(self, pad_index, name='masked_accuracy', **kwargs):
        super().__init__(name=name, **kwargs)
        self.pad_index = pad_index
        self.correct = self.add_weight(name='correct', initializer='zeros')
        self.total = self.add_weight(name='total', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        # y_true: one-hot (batch, seq_len, cat_count)
        # y_pred: softmax probabilities
        true_ids = tf.argmax(y_true, axis=-1)
        pred_ids = tf.argmax(y_pred, axis=-1)

        # Mask positions where true_ids == pad_index
        mask = tf.not_equal(true_ids, self.pad_index)
        mask = tf.cast(mask, tf.float32)

        matches = tf.cast(tf.equal(true_ids, pred_ids), tf.float32)
        matches *= mask

        self.correct.assign_add(tf.reduce_sum(matches))
        self.total.assign_add(tf.reduce_sum(mask))

    def result(self):
        return tf.math.divide_no_nan(self.correct, self.total)

    def reset_state(self):
        self.correct.assign(0.0)
        self.total.assign(0.0)