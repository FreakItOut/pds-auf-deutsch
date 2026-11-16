import os, glob, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
issues = []
for pattern in ['_work/subtitles/*_de.csv', '_work/menu_de/*_de*.csv']:
    for fpath in glob.glob(pattern):
        with open(fpath, encoding='latin1') as f:
            for line in f:
                line = line.rstrip('\r\n')
                if not line: continue
                parts = line.split(';')
                if len(parts) < 2: continue
                de = parts[-1]
                en_words = ['the', 'and', 'you', 'your', 'with', 'for', 'not', 'are', 'is', 'have', 'has', 'this', 'that', 'from', 'but', 'can', 'will', 'don', 'just', 'all', 'more', 'some', 'there', 'what', 'when', 'where', 'who', 'how', 'why', 'which', 'their', 'them', 'they', 'been', 'were', 'was', 'had']
                words = re.findall(r"[a-zA-Z']+", de.lower())
                en_found = [w for w in words if w in en_words]
                if len(en_found) >= 2:
                    issues.append((os.path.basename(fpath), 'EN-WORDS', de[:60], en_found[:3]))
                if len(parts) >= 6:
                    en = parts[-2]
                    if de == en and len(de) > 3:
                        issues.append((os.path.basename(fpath), 'UNTRANSLATED', de[:60], []))
print('Total issues found:', len(issues))
from collections import Counter
types = Counter(i[1] for i in issues)
print('By type:', dict(types))
for fpath, typ, text, extra in issues[:30]:
    print('  %s | %s | %s | %s' % (fpath, typ, text, extra))