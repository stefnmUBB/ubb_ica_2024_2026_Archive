import tensorflow as tf
from tensorflow.keras import layers

class SimpleSelfAttention(layers.Layer):
    def __init__(self, hidden_size):
        super().__init__()
        self.Wq = layers.Dense(hidden_size)
        self.Wk = layers.Dense(hidden_size)
        self.Wv = layers.Dense(hidden_size)

    def call(self, x):
        # x: (B, T, H)
        Q = self.Wq(x)
        K = self.Wk(x)
        V = self.Wv(x)

        # attention weights
        scores = tf.matmul(Q, K, transpose_b=True)   # (B, T, T)
        scores /= tf.math.sqrt(tf.cast(Q.shape[-1], tf.float32))
        weights = tf.nn.softmax(scores, axis=-1)     # (B, T, T)

        # weighted sum
        return tf.matmul(weights, V)                 # (B, T, H)
