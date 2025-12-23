from source.text_processing import Tokenizer
from source import fileutils

tokenizer = Tokenizer(fileutils.OUTPUT_WORDPIECES)

tokenizer.convert_corpus(fileutils.ANNOT_CORPUS_EN, fileutils.TOKENIZED_CORPUS_EN)
tokenizer.convert_corpus(fileutils.ANNOT_CORPUS_RO, fileutils.TOKENIZED_CORPUS_RO)