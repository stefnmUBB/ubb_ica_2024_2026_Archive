# Run with new environment since tf2.15 and wordcloud lib
# conflict on numpy versions :(
with open(f"data/workspace/corpus/clean/WikiMatrix.en-ro.en", 'r', encoding='utf-8') as f:
    en_cleaned = f.read()

with open(f"data/workspace/corpus/clean/WikiMatrix.en-ro.ro", 'r', encoding='utf-8') as f:
    ro_cleaned = f.read()

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re


def plot_wordcloud(corpus: str, lang, max_words: int = 128):
    """
    Generates a word cloud from a given text corpus.

    Args:
        corpus (str): The text corpus.
        max_words (int): Maximum number of words to display.
        title (str): Plot title.
    """
    # Simple preprocessing: lowercase and remove non-alphanumeric (keep spaces)
    corpus_clean = re.sub(r'[^a-zA-Z0-9\s]', '', corpus.lower())

    # Optional: you could filter stopwords here if needed
    wc = WordCloud(width=800, height=400, max_words=max_words, background_color="white")
    wc.generate(corpus_clean)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"Word cloud {lang}", fontsize=18)
    plt.savefig(f"data/output/fig/word_cloud_{lang}")

plot_wordcloud(ro_cleaned, "ro")
plot_wordcloud(en_cleaned, "en")

exit(0)
