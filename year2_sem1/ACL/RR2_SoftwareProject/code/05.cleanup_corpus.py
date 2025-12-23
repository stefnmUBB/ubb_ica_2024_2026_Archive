from source.text_processing import preprocess_file
from source import fileutils

ro_lines = preprocess_file(fileutils.FILTERED_CORPUS_RO)
en_lines = preprocess_file(fileutils.FILTERED_CORPUS_EN)

# Ensure line count matches original
print(f"RO lines: {len(ro_lines)}")
print(f"EN lines: {len(en_lines)}")

with open(fileutils.CLEAN_CORPUS_RO, "w", encoding="utf-8") as f:
    for line in ro_lines:
        f.write(line + "\n")

with open(fileutils.CLEAN_CORPUS_EN, "w", encoding="utf-8") as f:
    for line in en_lines:
        f.write(line + "\n")

print("Preprocessing done. Line counts preserved.")