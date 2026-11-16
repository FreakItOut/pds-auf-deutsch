import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Reconstruct old_de from new_de by reversing glossary replacements
# Old had: Reich->Imperium (no, old had Imperium, new has Reich)
# So old_de = new_de with Reich->Imperium, Vorzeit->Altertum, Chef->Kapitaen
# But this is imprecise. Instead, let me check the existing fix files.

# The existing TWN_CAMP_fixes.csv and TWN_RUIN_fixes.csv already had some glossary fixes.
# The new ones (8 CAMP, 11 RUIN) are additional. Let me create a new fixes CSV.

# I need old_de values. Since I changed the CSV, I need to find them.
# Let me search git or backup... there's no git. Let me just use the EN text as key
# and apply via text-scan (old = EN text won't work since old_de != EN).

# Actually, the apply_review_fixes.py text-scan searches for old_b + NUL in the binary.
# The old text (with Imperium/Altertum) is still on the discs (not yet patched).
# So I can search for the old German text on the discs.

# But I don't have the old_de values anymore. Let me reconstruct them by
# reversing the replacement in the current DE (which has Reich/Vorzeit/Chef).
# This is approximate but should work for text-scan.

import re

for src_fn, out_fn in [('TWN_CAMP_PRG_de.csv', 'TWN_CAMP_glossary2.csv'),
                       ('TWN_RUIN_PRG_de.csv', 'TWN_RUIN_glossary2.csv')]:
    # The current CSV has new (fixed) values. I need to find which entries changed.
    # I'll compare with the original candidates or just detect entries that
    # contain Reich/Vorzeit/Chef where the EN contains Empire/Ancient Age/Captain.
    
    # Actually, let me just create fixes by replacing back
    fixes = []
    with open('_work/subtitles/' + src_fn, encoding='latin1') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line: continue
            parts = line.split(';')
            if len(parts) < 6: continue
            en, de = parts[4], parts[5]
            # Check if de contains Reich/Vorzeit/Chef and en contains Empire/Ancient/Captain
            low_de = de.lower()
            low_en = en.lower()
            old_de = None
            if 'reich' in low_de and 'empire' in low_en:
                old_de = de.replace('Reich', 'Imperium').replace('reich', 'Imperium')
            if 'vorzeit' in low_de and 'ancient' in low_en:
                if old_de is None: old_de = de
                old_de = old_de.replace('Vorzeit', 'Altertum').replace('vorzeit', 'Altertum')
            if 'chef' in low_de and 'captain' in low_en:
                if old_de is None: old_de = de
                old_de = re.sub(r'Chef', 'Kapitaen', old_de, flags=re.IGNORECASE)
            if old_de is not None and old_de != de:
                fixes.append((src_fn, en, old_de, de))
    
    out_path = '_work/review_fixes/' + out_fn
    with open(out_path, 'w', encoding='latin1', newline='') as f:
        f.write('source_file;en;old_de;new_de;reason\n')
        for src, en, old, new in fixes:
            f.write('%s;%s;%s;%s;glossary2\n' % (src, en.replace(';', ','), old.replace(';', ','), new.replace(';', ',')))
    print(src_fn, 'reconstructed fixes:', len(fixes))