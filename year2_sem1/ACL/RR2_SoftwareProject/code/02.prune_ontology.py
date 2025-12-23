from rdflib import Graph, RDFS, RDF, SKOS
from source import fileutils

# === Load merged ontology ===
infile = fileutils.MINI_FOOD_ONTOLOGY
merged_graph = Graph()
merged_graph.parse(infile, format="turtle")
print(f"Loaded ontology with {len(merged_graph)} triples from {infile}")

# === Step 0: Filter individual labels ===
individuals_to_check = set()
for s, p, o in merged_graph.triples((None, RDF.type, None)):
    # consider as individual if object is not a known FoodOn class
    if str(o).startswith("http://purl.obolibrary.org/obo/FOODON_"):
        individuals_to_check.add(s)

for ind in individuals_to_check:
    labels = {}
    # collect existing prefLabels
    for s, p, o in merged_graph.triples((ind, SKOS.prefLabel, None)):
        if hasattr(o, "language") and o.language in ("en", "ru"):
            labels[o.language] = o
    if not labels:
        # remove individual completely
        for s, p, o in merged_graph.triples((ind, None, None)):
            merged_graph.remove((s, p, o))
        for s, p, o in merged_graph.triples((None, None, ind)):
            merged_graph.remove((s, p, o))
    else:
        # remove other language labels
        for s, p, o in merged_graph.triples((ind, SKOS.prefLabel, None)):
            if hasattr(o, "language") and o.language not in ("en", "ru"):
                merged_graph.remove((s, p, o))

print("Filtered individuals to keep only those with English or Russian labels.")

# === Step 1: Build class -> subclasses mapping ===
subclasses = {}
for s, p, o in merged_graph.triples((None, RDFS.subClassOf, None)):
    subclasses.setdefault(o, set()).add(s)

# === Step 2: Build class -> instances mapping ===
class_instances = {}
for s, p, o in merged_graph.triples((None, RDF.type, None)):
    class_instances.setdefault(o, set()).add(s)

# === Step 3: Bottom-up pruning function ===
def prune_class(cls, visited=None):
    if visited is None:
        visited = set()
    if cls in visited:
        return False  # already checked
    visited.add(cls)

    # Check instances
    if cls in class_instances and class_instances[cls]:
        return True

    # Check subclasses recursively
    keep = False
    for sub in subclasses.get(cls, set()).copy():
        if prune_class(sub, visited):
            keep = True
        else:
            # Remove empty subclass
            merged_graph.remove((sub, None, None))
            merged_graph.remove((None, None, sub))
            subclasses[cls].remove(sub)

    return keep

# === Step 4: Prune all top-level FoodOn classes ===
top_classes = [cls for cls in subclasses.keys() if not any(cls in sset for sset in subclasses.values())]
for cls in top_classes:
    prune_class(cls)

# === Step 5: Save pruned ontology ===
outfile = fileutils.MINI_FOOD_ONTOLOGY_EN_RU
merged_graph.serialize(outfile, format="turtle")
print(f"Saved pruned ontology with {len(merged_graph)} triples to {outfile}")
