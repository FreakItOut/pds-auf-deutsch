import os, csv
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# I need to find the old and new DE values. Since I already changed the CSV files,
# I need to reconstruct from the candidates or just apply the changes.
# The glossary changes were: Imperium->Reich, Altertum->Vorzeit, Kapitän->Chef
# Let me check if there's a record of the old values.

# Actually, the apply_review_fixes.py needs old_de and new_de. Since I already changed
# the CSV, I can't easily get old_de. But I can reconstruct: the old values had
# "Imperium", "Altertum", "Kapitän" and the new values have "Reich", "Vorzeit", "Chef".

# Let me just check the review_fixes directory for existing glossary fix files.
import glob
for p in glob.glob('_work/review_fixes/*camp*') + glob.glob('_work/review_fixes/*ruin*'):
    print(p)