from source.embeddings import extract_edges, edges2embeddings

from source import fileutils

extract_edges(fileutils.MINI_FOOD_ONTOLOGY_RO, fileutils.MINI_FOOD_ONTOLOGY_EDGES)

edges2embeddings(fileutils.MINI_FOOD_ONTOLOGY_EDGES, fileutils.OUTPUT_CONCEPT_EMBEDDINGS)