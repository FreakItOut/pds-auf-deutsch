# -*- coding: utf-8 -*-
# Schreibt alle Movie-Untertitel in Filmreihenfolge nach
# _work/review_fixes/evt_all_review.txt (latin1).
import io
import json

j = json.load(open('_work/evt_offsets_disc1.json', encoding='utf-8'))
de = {}
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    q = ln.rstrip('\r\n')
    if ';' in q and not q.startswith('#'):
        a, b = q.split(';', 1)
        de[a] = b
ents = [e for e in j['entries'] if e['src'].startswith('MOVIE.DAT')]
groups = {}
for e in ents:
    g = e['src'].split('g')[-1]
    groups.setdefault(int(g), []).append(e)
out = io.open('_work/review_fixes/evt_all_review.txt', 'w',
              encoding='latin1', newline='\n')
i = 0
for g in sorted(groups):
    items = groups[g]
    out.write('=== FILM g%d (%d Zeilen) ===\n' % (g, len(items)))
    for e in items:
        en = e['text']
        out.write('%4d | EN(%2d) %-50r | DE %r\n' % (
            i, len(en), en, de.get(en, '???')))
        i += 1
    out.write('\n')
out.close()
print('written', i)
