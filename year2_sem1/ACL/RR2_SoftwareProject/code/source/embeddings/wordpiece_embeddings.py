import numpy as np, csv

def compute_wordpiece_embeddings(wordpieces_path, embeddings_path, embedding_size = 127):
    np.random.seed(42)

    # Read wordpieces
    wordpieces = []
    with open(wordpieces_path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=1)
            if len(parts) == 0:
                continue
            idx = int(parts[0])
            wordpieces.append(idx)

    # Create embeddings (uniform random)
    embeddings = np.random.uniform(
        low=-0.1, high=0.1, size=(max(wordpieces) + 1, embedding_size)
    )

    # Write CSV
    with open(embeddings_path, "w", newline="", encoding="utf8") as csvfile:
        writer = csv.writer(csvfile)
        header = ["id"] + [f"e{i}" for i in range(embedding_size)]
        writer.writerow(header)

        for idx in sorted(wordpieces):
            row = [idx] + embeddings[idx].tolist()
            writer.writerow(row)

    print("Done. Saved:", embeddings_path)
