from source.text_processing import compute_wordpieces
from source import fileutils

compute_wordpieces([fileutils.ANNOT_CORPUS_RO, fileutils.ANNOT_CORPUS_EN],
                   fileutils.OUTPUT_CONCEPTS,
                   fileutils.OUTPUT_WORDPIECES)

# after wordpieces.txt compute, manually replace "1  " with "1 \s"