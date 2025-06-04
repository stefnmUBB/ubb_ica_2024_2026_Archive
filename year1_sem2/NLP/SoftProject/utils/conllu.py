def read_conllu_dataset(path):
    """
    Reads a CoNLL-U formatted dataset and returns a list of sentences.
    Each sentence is a list of (word, UPOS) tuples.
    
    Args:
        path (str): Path to the .conllu file.
    
    Returns:
        List[List[Tuple[str, str]]]: List of sentences.
    """
    sentences = []
    current_sentence = []

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line:
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []
                continue
            if line.startswith("#"):
                continue

            parts = line.split('\t')
            if len(parts) != 10:
                continue  # malformed line

            token_id, word, _, upos, *_ = parts

            # Skip multiword tokens or empty token IDs (e.g. 1-2 or empty lines)
            if "-" in token_id or "." in token_id:
                continue

            current_sentence.append((word, upos))

    # Append any remaining sentence
    if current_sentence:
        sentences.append(current_sentence)

    return sentences


def enumerate_word_upos_pairs(sentences):
    for sentence in sentences:
        for word, upos in sentence:
            yield word, upos

def enumerate_words(sentences):
    for sentence in sentences:
        for word, _ in sentence:
            yield word

def filtered_words(sentences, filter):
    for sentence in sentences:
        for word, upos in sentence:
            if filter(word, upos):
                yield word

def enumerate_tags(sentences):
    for sentence in sentences:
        for _, upos in sentence:
            yield upos