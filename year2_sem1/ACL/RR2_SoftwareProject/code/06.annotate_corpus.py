from source.text_processing import parallel_annotate_corpus
from source import fileutils

if __name__=="__main__":
    print("Annotating Romanian...")
    parallel_annotate_corpus(fileutils.CLEAN_CORPUS_RO, fileutils.ANNOT_CORPUS_RO, 'ro', max_workers=10,
                           sample_interval=400)

    print("Annotating English...")
    parallel_annotate_corpus(fileutils.CLEAN_CORPUS_EN, fileutils.ANNOT_CORPUS_EN, 'en', max_workers=10,
                           sample_interval=400)

    print("Done.")