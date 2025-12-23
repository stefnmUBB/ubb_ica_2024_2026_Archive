#!/usr/bin/env python3
import csv, rdflib, numpy as np
from tqdm import tqdm
from gensim.models.poincare import PoincareModel, PoincareRelations
from collections import defaultdict

def extract_edges(ontology_path, out_edges_path):
    # Load the RDF file
    g = rdflib.Graph()
    g.parse(ontology_path, format="turtle")

    # Namespaces
    RDFS = rdflib.RDFS

    # Build obo2conceptIds as a multimap (use set to remove duplicates)
    obo2conceptIds = defaultdict(set)
    for concept in g.subjects():
        if str(concept).startswith("http://gretaste.ilsp.gr/rdf/concept/"):
            concept_id = str(concept).rsplit("/", 1)[-1]
            for obo in g.objects(concept, rdflib.RDF.type):
                obo_id = str(obo).rsplit("/", 1)[-1]
                obo2conceptIds[obo_id].add(concept_id)

    # Convert sets to lists for easier iteration
    obo2conceptIds = {k: list(v) for k, v in obo2conceptIds.items()}

    # Extract all rdfs:subClassOf pairs
    edges = []
    for obo1, _, obo2 in g.triples((None, RDFS.subClassOf, None)):
        obo1_id = str(obo1).rsplit("/", 1)[-1]
        obo2_id = str(obo2).rsplit("/", 1)[-1]

        ids1 = obo2conceptIds.get(obo1_id, [obo1_id])
        ids2 = obo2conceptIds.get(obo2_id, [obo2_id])

        # Create all combinations
        for id1 in ids1:
            for id2 in ids2:
                edges.append((id1, id2))

    # Write edges to CSV
    with open(out_edges_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id1", "id2"])  # generic header
        writer.writerows(edges)

    print(f"Written {len(edges)} edges to {out_edges_path}")


# ==========================
# CONFIG
# ==========================
def edges2embeddings(EDGES_CSV, OUTPUT_CSV, EMBEDDING_SPACE_SIZE=127, EPOCHS=70, BURN_IN=10):

    # ==========================
    # LOAD EDGES
    # ==========================
    print("Loading edges from CSV...")
    edges = []
    nodes_set = set()
    with open(EDGES_CSV, "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row["id1"].strip()
            v = row["id2"].strip()
            edges.append((u, v))
            nodes_set.add(u)
            nodes_set.add(v)

    print(f"Total edges: {len(edges)}")
    print(f"Total unique nodes: {len(nodes_set)}")

    # ==========================
    # TRAIN POINCARÉ EMBEDDINGS
    # ==========================
    print("Writing temporary TSV for Poincaré training...")
    relations_file = "relations.tsv"
    with open(relations_file, "w", encoding="utf8") as f:
        for u, v in edges:
            f.write(f"{u}\t{v}\n")

    print("Training Poincaré embeddings...")
    relations_graph = PoincareRelations(
        file_path=relations_file,
        encoding="utf8",
        delimiter="\t"
    )
    model = PoincareModel(
        train_data=relations_graph,
        size=EMBEDDING_SPACE_SIZE,
        burn_in=BURN_IN
    )
    model.train(epochs=EPOCHS)

    # ==========================
    # COMPUTE CENTER OF MASS
    # ==========================
    print("Computing center of mass of raw embeddings...")
    raw_vectors = []
    node_order = []  # preserve order so we match means correctly

    for node in nodes_set:
        if node in model.kv:
            raw_vectors.append(np.array(model.kv[node]))
            node_order.append(node)

    raw_vectors = np.stack(raw_vectors, axis=0)
    center_of_mass = raw_vectors.mean(axis=0)
    print("Center of mass norm:", np.linalg.norm(center_of_mass))

    # ==========================
    # CENTERED DISPERSIVE PROJECTOR
    # ==========================
    def poincare_to_euclidean_centered(v, center, eps=1e-6, exponent=0.5):
        """
        Project vector to Euclidean space with spreading based on distance
        from the empirical center of mass rather than from origin.
        """
        v_rel = v - center  # shift so center is 0
        norm = np.linalg.norm(v_rel)

        if norm < eps:
            return v_rel + center  # stays at center

        # adaptive exponent: push closer points outward more
        local_exp = exponent
        if norm < 1.0:
            local_exp *= max(norm, 0.5)

        factor = (norm ** local_exp) / norm

        # Poincaré → Euclid blow-up
        v_rel = v_rel * factor / np.sqrt(1 - norm**2 + eps)

        return center + v_rel * np.exp(-1+min(norm*norm,5))

    # ==========================
    # PROJECT TO EUCLIDEAN SPACE
    # ==========================
    print("Projecting embeddings to Euclidean space...")
    embeddings = {}
    for node in tqdm(nodes_set):
        if node in model.kv:
            vec = np.array(model.kv[node])
            embeddings[node] = poincare_to_euclidean_centered(
                vec, center_of_mass, exponent=0.5
            )
        else:
            embeddings[node] = np.zeros(EMBEDDING_SPACE_SIZE)

    # ==========================
    # WRITE EMBEDDINGS CSV
    # ==========================
    print(f"Writing embeddings to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        header = ["concept_id"] + [f"e{i}" for i in range(EMBEDDING_SPACE_SIZE)]
        writer.writerow(header)

        for node in sorted(embeddings.keys(), key=lambda x: x):
            row = [node] + embeddings[node].tolist()
            writer.writerow(row)

    print("Done.")
