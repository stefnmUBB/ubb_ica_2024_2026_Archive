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

model = tf.keras.models.load_model(fileutils.OUTPUT_MODEL("lstm_nmt_model"), custom_objects={
    'Perplexity': Perplexity,
    "MaskedCategoricalAccuracy": SpecificMaskedAccuracy,
    "SimpleSelfAttention": SimpleSelfAttention,
    'loss_fn': loss_fn
})


def translate(text):
    text = normalize_line(text)
    text = annotate_text(text)
    tokens = tokenizer.convert_sentence(text)
    tokens = tokens.split(' ')
    embeddings = vec.vectorize_seq(tokens)
    embeddings = np.expand_dims(embeddings, 0)
    #print(tokens)
    #print(embeddings.shape)
    result = model(embeddings).numpy().argmax(axis=-1)[0]
    decoded = vec.decode(result)
    print("en = ", text)
    #print("en = ", tokens)
    print("ro = ", "".join(decoded))
    print("")



translate("I am eating a delicious ice cream.")
translate("The cake contains strawberries.")
translate("It is distinct from the mustard plants which belong to the genus Brassica.")
translate("Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter.")
translate("It is used in its dried form for Japanese soups, tempura, and material for manufacturing dried nori and tsukudani and rice.")



x=""
while x!="exit":
    x = input("[EN] >> ")
    if x=="": continue
    if(x=="exit"): break
    translate(x)
