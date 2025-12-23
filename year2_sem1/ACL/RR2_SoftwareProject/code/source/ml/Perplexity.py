import tensorflow as tf

# Custom perplexity metric
class Perplexity(tf.keras.metrics.Metric):
    def __init__(self, name='perplexity', **kwargs):
        super().__init__(name=name, **kwargs)
        self.cross_entropy = self.add_weight(name='ce', initializer='zeros')
        self.count = self.add_weight(name='count', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        # Categorical crossentropy per timestep
        ce = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
        ce_sum = tf.reduce_sum(ce)
        count = tf.cast(tf.size(ce), tf.float32)

        self.cross_entropy.assign_add(ce_sum)
        self.count.assign_add(count)

    def result(self):
        # Prevent division by zero
        avg_ce = tf.cond(
            self.count > 0,
            lambda: self.cross_entropy / self.count,
            lambda: 0.0
        )
        return tf.exp(avg_ce)

    def reset_state(self):
        self.cross_entropy.assign(0.0)
        self.count.assign(0.0)
