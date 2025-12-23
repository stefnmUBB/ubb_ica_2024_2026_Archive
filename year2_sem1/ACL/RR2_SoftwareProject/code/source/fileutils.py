INPUT_CORPUS_EN = "data/input/corpus/WikiMatrix.en-ro.en"
INPUT_CORPUS_RO = "data/input/corpus/WikiMatrix.en-ro.ro"

INPUT_ONTOLOGY_AMA = "data/input/ontology/amaletheia.rdf"
INPUT_ONTOLOGY_FOODON = "data/input/ontology/foodon.owl"

OUTPUT_CONCEPT_EMBEDDINGS = "data/output/embeddings/concept_embeddings.csv"
OUTPUT_WORDPIECE_EMBEDDINGS = "data/output/embeddings/wordpiece_embeddings.csv"
OUTPUT_WORDPIECES = "data/output/wordpieces.txt"
OUTPUT_CONCEPTS = "data/output/concepts.txt"

def OUTPUT_MODEL(name): return f"data/output/model/{name}"

def OUTPUT_FIG(name): return f"data/output/fig/{name}.png"

def MODIFIED_CORPUS_PATH(original_path:str, modification_type:str)->str:
    components = original_path.split('/')
    data = components[0]
    name = components[-1]
    return f"{data}/workspace/corpus/{modification_type}/{name}"

def WORKING_ONTOLOGY(name):
    return f"data/workspace/ontology/{name}"

MINI_FOOD_ONTOLOGY = WORKING_ONTOLOGY("mini_food_ontology.ttl")
MINI_FOOD_ONTOLOGY_EN_RU = WORKING_ONTOLOGY("mini_food_ontology_en_ru.ttl")
MINI_FOOD_ONTOLOGY_RO = WORKING_ONTOLOGY("mini_food_ontology_ro.ttl")
MINI_FOOD_ONTOLOGY_EDGES = WORKING_ONTOLOGY("mini_food_ontology_edges.csv")

FILTERED_CORPUS_EN = MODIFIED_CORPUS_PATH(INPUT_CORPUS_EN, "filtered")
FILTERED_CORPUS_RO = MODIFIED_CORPUS_PATH(INPUT_CORPUS_RO, "filtered")

CLEAN_CORPUS_EN = MODIFIED_CORPUS_PATH(INPUT_CORPUS_EN, "clean")
CLEAN_CORPUS_RO = MODIFIED_CORPUS_PATH(INPUT_CORPUS_RO, "clean")

ANNOT_CORPUS_EN = MODIFIED_CORPUS_PATH(INPUT_CORPUS_EN, "annotated")
ANNOT_CORPUS_RO = MODIFIED_CORPUS_PATH(INPUT_CORPUS_RO, "annotated")

TOKENIZED_CORPUS_EN = MODIFIED_CORPUS_PATH(INPUT_CORPUS_EN, "tokenized")
TOKENIZED_CORPUS_RO = MODIFIED_CORPUS_PATH(INPUT_CORPUS_RO, "tokenized")

def open_read_utf8(path):
    return open(path, 'r', encoding='utf8')
