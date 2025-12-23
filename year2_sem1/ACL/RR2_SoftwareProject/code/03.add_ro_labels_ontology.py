from rdflib import Graph, SKOS, Literal
from googletrans import Translator
from source import fileutils

# === Load ontology ===
infile = fileutils.MINI_FOOD_ONTOLOGY_EN_RU
g = Graph()
g.parse(infile, format="turtle")
print(f"Loaded {len(g)} triples")

translator = Translator()

# === Step 1: Collect English prefLabels ===
to_translate = []
for s, p, o in g.triples((None, SKOS.prefLabel, None)):
    if hasattr(o, "language") and o.language == "en":
        to_translate.append((s, o))

print(f"Found {len(to_translate)} English labels to translate into Romanian")

# === Step 2: Translate and add Romanian labels ===
for subj, lit in to_translate:
    for i in range(3):
        try:
            print(f"Translating {lit.value}", end="")
            result = translator.translate(lit.value, src="en", dest="ro")
            ro_label = Literal(result.text, lang="ro")
            g.add((subj, SKOS.prefLabel, ro_label))
            print(f"\rTranslating {lit.value} > {ro_label}", )
            break
        except Exception as e:
            print(f"Translation failed for {lit.value}: {e}")

# === Step 3: Save enriched ontology ===
outfile = fileutils.MINI_FOOD_ONTOLOGY_RO
g.serialize(outfile, format="turtle")
print(f"Saved ontology with Romanian translations to {outfile}")
