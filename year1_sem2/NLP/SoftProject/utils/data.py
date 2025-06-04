import numpy as np
import string

from .helpers import to_categorical

class Dataset:
    labels = ['<PAD>', 'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM',
                       'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'VERB', 'X']
    label2id = {label: i for i, label in enumerate(labels)}

    ascii_chars = set([chr(i) for i in range(33, 128)])
    ro_chars = set('îăâțșÎĂÂȚȘ')
    valid_chars = ascii_chars.union(ro_chars)


    def __init__(self):
        self.max_word_len = 0
        self.max_sent_len = 0
        self.word2id = {'<PAD>': 0, '#': 1}
        self.char2id = {'<NULL>': 0, '#': 1}
        self.fitted = False

    def fit(self, sentences:list, mode: str, categorical_y=True):
        sentences = self.__clean(sentences)
        self.max_sent_len = max([len(s) for s in sentences])
        self.max_word_len = max([len(word) for s in sentences for word, upos in s])
        self.mode = mode
        self.categorical_y = categorical_y

        if mode=="chars":
            for s in sentences:
                for word, upos in s:
                    for ch in word:
                        if not ch in self.char2id:
                            self.char2id[ch] = len(self.char2id)
        if mode=="word_id":
            for s in sentences:
                for word, upos in s:
                    if not word in self.word2id:
                        self.word2id[word] = len(self.word2id)

        return self.encode_x(sentences), self.encode_y(sentences)

    def encode_x(self, sentences:list):
        if self.mode=="chars": 
            X = np.zeros((len(sentences), self.max_sent_len, self.max_word_len))
            for i, s in enumerate(sentences):
                for j, (word, upos) in enumerate(s):
                    for k, ch in enumerate(word):
                        X[i,j,k] = self.char2id.get(ch, self.char2id['#'])
            return X
        if self.mode=="word_id":
            X = np.zeros((len(sentences), self.max_sent_len))
            for i, s in enumerate(sentences):
                for j, (word, upos) in enumerate(s):
                    X[i,j] = self.word2id.get(word, self.word2id['#'])
            return X

    def encode_y(self, sentences:list):
        y = np.zeros((len(sentences), self.max_sent_len, len(self.labels)))
        for i, s in enumerate(sentences):
            for j, (word, upos) in enumerate(s):
                y[i,j, self.label2id[upos]] = 1
            for j in range(len(s), self.max_sent_len):
                    y[i,j,0]=1
        if not self.categorical_y:
            y = np.argmax(y, axis=-1)
        return y


    def __clean(self, sentences):
        new_sentences = []
        for s in sentences:
            new_sentences.append([(self._clean_word(word), upos) for word, upos in s])
        return new_sentences


    def _clean_word(self, word):
        return ''.join([ch if ch in self.valid_chars else '#' for ch in word])
            
    def encode(self, sentences:list):
        sentences = self.__clean(sentences)
        return self.encode_x(sentences), self.encode_y(sentences)
