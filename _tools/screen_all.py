# full row dump for manual review + multi-signal screen
import csv
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')

STEMS = ['TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG',
         'TWN_SEEK_PRG']


def read_stem(stem):
    rows = []
    with io.open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
        for ln in f:
            q = ln.rstrip('\r\n').split(';')
            if len(q) >= 6 and q[0].isdigit():
                rows.append({'uid': int(q[0]), 'en': q[4], 'de': q[5],
                             'off': q[3]})
    return rows


EN_WORDS = re.compile(r"\b(the|you|your|with|what|that|this|have|from|"
                      r"there|they|will|would|should|could|about|"
                      r"please|because|before|after|something|nothing|"
                      r"anything|everything|again|still|just|only|"
                      r"really|maybe|never|always|people|place|thing)\b",
                      re.I)
TRUNC_END = re.compile(r"[A-Za-z]{1,3}$")
GER_STOP = set("""der die das den dem des ein eine einer eines einem einen
und oder aber doch sondern wenn weil dass ob als wie wo wer was warum
wieso weshalb ich du er sie es wir ihr mich dich sich uns euch mir dir
nicht kein keine keinen keinem keiner mit von zu zur zum auf an in im am
fuer fuer's durch gegen ohne um bei aus nach vor ueber unter zwischen
ist sind war waren bin bist sei seid wird werden wurde wurden hat haben
habe hast hatte hatten kann kannst koennen konnte konnte koenntest
muss musst muessen soll sollst sollen will willst wollen mag moechte
auch noch nur schon sehr so dann denn mal ja nein bitte danke""".split())
GER_VERBISH = re.compile(r"(en|st|te|test|et|t)$")


def screen(rows, stem):
    flags = []
    for i, r in enumerate(rows):
        en, de = r['en'], r['de']
        e, d = en.strip(), de.strip()
        if not e or not d:
            continue
        prev = rows[i - 1] if i else None
        nxt = rows[i + 1] if i + 1 < len(rows) else None
        # 1. english leftovers inside german
        m = EN_WORDS.findall(d)
        if m and len(d) > 8 and not re.search(r'\b(Item|Items|Laser|Level|'
                                              r'Max|HP|EXP|normal|Coolia|'
                                              r'Coolias|Hopper|Seeker|'
                                              r'Seekers|Edge|Azel)\b', d):
            flags.append((i, r, 'EN-LEFTOVER', ','.join(m[:3])))
        # 2. lowercase sentence start after a closed sentence
        if (prev and prev['de'].strip().rstrip().endswith(('.', '!', '?'))
                and d[:1].islower()):
            flags.append((i, r, 'LOWER-AFTER-DOT',
                          prev['de'].strip()[-15:]))
        # 3. German ends with comma but next starts uppercase
        if (d.rstrip().endswith(',') and nxt
                and nxt['de'].strip()[:1].isupper()):
            flags.append((i, r, 'COMMA-THEN-CAP', nxt['de'].strip()[:12]))
        # 4. DE much shorter than EN (possible meaning loss)
        if len(e) >= 22 and len(d) <= int(len(e) * 0.55):
            flags.append((i, r, 'SHORT', '%d/%d' % (len(d), len(e))))
        # 5. sentence-final word is a German stopword (dangling grammar)
        w = re.findall(r"[A-Za-z']+", d)
        if w and len(d) > 6 and w[-1].lower() in GER_STOP \
                and not d.rstrip().endswith(('.', '!', '?', ',')):
            flags.append((i, r, 'END-STOPWORD', w[-1]))
    return flags


out = io.open('_work/review_fixes/full_screen.txt', 'w', encoding='latin1',
              newline='\n')
allflags = 0
for stem in STEMS:
    rows = read_stem(stem)
    fl = screen(rows, stem)
    allflags += len(fl)
    out.write('===== %s rows=%d flags=%d =====\n' % (stem, len(rows), len(fl)))
    for i, r, kind, extra in fl:
        out.write('%s %5d [%s] %s\n' % (stem, r['uid'], kind, extra))
        out.write('   EN=%r\n   DE=%r\n' % (r['en'], r['de']))
    out.write('\n')

# fmv chains
fv = []
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if en.strip():
        fv.append({'uid': -1, 'en': en, 'de': de})
fl = screen(fv, 'FMV')
allflags += len(fl)
out.write('===== FMV rows=%d flags=%d =====\n' % (len(fv), len(fl)))
for i, r, kind, extra in fl:
    out.write('FMV %5d [%s] %s\n' % (i, kind, extra))
    out.write('   EN=%r\n   DE=%r\n' % (r['en'], r['de']))
out.close()
print('flags total:', allflags)
