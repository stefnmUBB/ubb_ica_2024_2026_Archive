from rdflib import Graph, Namespace, RDFS, RDF, Literal, URIRef
from difflib import SequenceMatcher

from source import fileutils

# === Load ontologies ===
foodon = Graph()
amaltheia = Graph()

foodon.parse(fileutils.INPUT_ONTOLOGY_FOODON)
amaltheia.parse(fileutils.INPUT_ONTOLOGY_AMA)

# === Namespaces ===
FOODON = Namespace("http://purl.obolibrary.org/obo/FOODON_")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# === Step 1: FoodOn subset (food product classes) ===
query = """
SELECT ?cls ?label
WHERE {
  ?cls rdfs:subClassOf* <http://purl.obolibrary.org/obo/FOODON_00001002> .
  ?cls rdfs:label ?label .
}
LIMIT 200
"""
foodon_subset = [(str(r["cls"]), str(r["label"])) for r in foodon.query(query)]
print(f"Loaded {len(foodon_subset)} FoodOn classes")

# Build a lookup for FoodOn labels -> URIRef
foodon_label_to_uri = {label.lower(): URIRef(uri) for uri, label in foodon_subset}

# === Step 2: Extract Amaltheia SKOS concepts and multilingual labels ===
amal_labels = {}
for s, p, o in amaltheia.triples((None, SKOS.prefLabel, None)):
    if hasattr(o, "language") and o.language:
        amal_labels.setdefault(str(s), {})[o.language] = str(o)
for s, p, o in amaltheia.triples((None, SKOS.altLabel, None)):
    if hasattr(o, "language") and o.language:
        amal_labels.setdefault(str(s), {})[f"{o.language}_alt"] = str(o)

print(f"Extracted {len(amal_labels)} Amaltheia SKOS concepts with multilingual labels")

# Build English lookup including alt labels
amal_en_all = {}
for concept_uri, labels in amal_labels.items():
    for lang, text in labels.items():
        if lang == "en" or lang.endswith("_alt"):
            amal_en_all[text.lower()] = concept_uri

# === Step 3: Fuzzy matching helper ===
def best_match(label, candidates):
    best = None
    best_score = 0
    for cand in candidates:
        score = SequenceMatcher(None, label.lower(), cand.lower()).ratio()
        if score > best_score:
            best, best_score = cand, score
    return (best, best_score) if best_score > 0.65 else (None, 0)  # lower threshold

# === Step 4: Match Amaltheia concepts to FoodOn classes ===
matched = {}
for concept_uri, labels in amal_labels.items():
    # Prefer English prefLabel first
    candidate_labels = [labels.get("en")] if "en" in labels else []
    # Include alt labels
    candidate_labels += [labels[lang] for lang in labels if lang.endswith("_alt")]
    candidate_labels = [l for l in candidate_labels if l]

    best_class = None
    for label in candidate_labels:
        match, score = best_match(label, foodon_label_to_uri.keys())
        if match:
            best_class = foodon_label_to_uri[match]
            break

    # Fallback to top-level "Food product"
    if best_class is None:
        best_class = URIRef("http://purl.obolibrary.org/obo/FOODON_00001002")

    matched[concept_uri] = best_class

print(f"Matched {len(matched)} Amaltheia concepts to FoodOn classes (including fallback)")

# === Step 5: Create merged ontology ===
merged_graph = Graph()

# Add all FoodOn classes with readable labels
for cls_uri, cls_label in foodon_subset:
    cls_ref = URIRef(cls_uri)
    merged_graph.add((cls_ref, RDFS.label, Literal(cls_label)))

# Add Amaltheia concepts as instances with SKOS labels
for amal_uri, food_class_ref in matched.items():
    amal_ref = URIRef(amal_uri)
    labels = amal_labels[amal_uri]

    for lang, text in labels.items():
        if lang.endswith("_alt"):
            merged_graph.add((amal_ref, SKOS.altLabel, Literal(text, lang=lang.split("_")[0])))
        else:
            merged_graph.add((amal_ref, SKOS.prefLabel, Literal(text, lang=lang)))

    merged_graph.add((amal_ref, RDF.type, food_class_ref))

# Preserve FoodOn hierarchy (only between FoodOn classes)
for s, p, o in foodon.triples((None, RDFS.subClassOf, None)):
    if str(s).startswith(str(FOODON)) and str(o).startswith(str(FOODON)):
        merged_graph.add((URIRef(s), RDFS.subClassOf, URIRef(o)))

# === Step 6: Save merged ontology ===
out = fileutils.MINI_FOOD_ONTOLOGY
merged_graph.serialize(out, format="turtle")
print(f"Saved merged ontology with {len(matched)} individuals to {out}")
