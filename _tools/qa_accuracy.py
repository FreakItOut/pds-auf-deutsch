# -*- coding: utf-8 -*-
# Gesamtpruefung: Genauigkeit (EN vs DE), Grammatik, Platzhalter,
# Doppelblock-Komposition.  Schreibt _work/review_fixes/qa_accuracy_report.txt
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')

TERMINAL = ('.', '!', '?', ')', '"', "'")
EN_STOP = set('''the you your and with from this that these those have
has had what when where which why how would could should does did
are not but for his its our their they them there she we me my
of to be been being can do don't doesn't
i'm you're we're they're isn't aren't wasn't weren't can't won't
something someone anything everything nothing'''.split())


def unesc(s):
    return s.replace('\\n', '\n').replace('\\t', '\t')


def load_twn():
    out = []
    for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
        stem = os.path.basename(path)[:-7]
        for line in io.open(path, encoding='latin1'):
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                off = 0
                try:
                    off = int(p[2].split('|')[0])
                except Exception:
                    pass
                out.append({'src': 'TWN', 'stem': stem, 'uid': p[0],
                            'off': off, 'en': p[4], 'de': p[5]})
    return out


def load_menu():
    out = []
    for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
        stem = os.path.basename(path)[:-7]
        for i, line in enumerate(io.open(path, encoding='latin1')):
            if i == 0 and line.startswith('file;'):
                continue
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6:
                out.append({'src': 'MENU', 'stem': stem, 'uid': p[1],
                            'off': int(p[1]) if p[1].isdigit() else 0,
                            'en': p[4], 'de': p[5]})
    return out


def load_evt():
    out = []
    path = '_work/evt_de_map.csv'
    if not os.path.isfile(path):
        return out
    for i, line in enumerate(io.open(path, encoding='latin1')):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 2:
            out.append({'src': 'EVT', 'stem': 'evt', 'uid': str(i),
                        'off': i, 'en': p[0], 'de': p[1]})
    return out


PLACE = re.compile(r'%[0-9.\-+]*[sdfxX]')
CTRL = re.compile(r'\{[0-9a-fA-F]{2}\}')


def check(s):
    en, de = s['en'], s['de']
    eno, deo = unesc(en), unesc(de)
    f = []
    if not de.strip() and en.strip():
        f.append('DE-LEER')
    if de == en and len(re.findall(r'[A-Za-z]{3,}', en)) >= 2 \
            and not en.isupper() and not re.search(r'[#%{}]', en):
        words = [w.lower() for w in re.findall(r"[A-Za-z']+", en)]
        if len(words) >= 2 and not all(
                w in ('laser', 'radar', 'combo', 'item', 'get', 'hp', 'exp',
                      'max', 'level', 'up', 'normal', 'start', 'parameter',
                      'time', 'rate', 'disp', 'collision', 'buy', 'sell',
                      'switch', 'gun', 'part', 'who', 'error', 'fld',
                      'open', 'close', 'yes', 'no', 'on', 'off')
                for w in words):
            f.append('DE==EN')
    # englische Funktionswoerter im DE
    eng = [w for w in re.findall(r"[A-Za-z][A-Za-z']*", deo)
           if len(w) > 2 and w.lower() in EN_STOP]
    if eng:
        f.append('EN-REST:' + ','.join(sorted(set(eng)))[:40])
    # Platzhalter / Steuercodes / Zeilenumbrueche
    if sorted(PLACE.findall(eno)) != sorted(PLACE.findall(deo)):
        f.append('PLATZHALTER')
    if sorted(re.findall(r'\d+', eno)) != sorted(re.findall(r'\d+', deo)):
        f.append('ZAHLEN')
    if len(CTRL.findall(eno)) != len(CTRL.findall(deo)):
        f.append('CTRL-CODES')
    if en.count('\\n') != de.count('\\n'):
        f.append('ZEILENUMBRUCH')
    # Interpunktion / Spacing
    if re.search(r'(?<!\.)\s[,;:!?]', deo):
        f.append('SPACE-VOR-SATZZEICHEN')
    if re.search(r'[.,;:!?][A-Za-zÄÖÜäöü]', deo) and not re.search(
            r'\b[A-Za-zÄÖÜäöü]\.(?=[A-Za-zÄÖÜäöü]\.)', deo):
        f.append('KEIN-SPACE-NACH-SATZZEICHEN')
    bare = deo.replace('...', '')
    if '..' in bare or ',,' in bare:
        f.append('DOPPELPUNKT')
    for a, b in (('[', ']'),):
        if deo.count(a) != deo.count(b):
            f.append('KLAMMER-%s' % a)
    # Grossschreibung nach Punkt + Satzende-Parität
    if re.search(r'[.!?]\s+[a-zäöü]', deo) and '...' not in deo:
        f.append('KLEIN-NACH-PUNKT')
    if eno.rstrip().endswith('?') and not deo.rstrip().endswith('?'):
        f.append('FRAGEZEICHEN-FEHLT')
    if not eno.rstrip().endswith('?') and deo.rstrip().endswith('?') \
            and len(eno) > 12:
        f.append('FRAGEZEICHEN-ZUVIEL')
    # doppelte Woerter (nur sinnvolle Laenge, keine Debug-Labels)
    ws = re.findall(r'[A-Za-zÄÖÜäöüß]{2,}', deo.lower())
    for i in range(1, len(ws)):
        if ws[i] == ws[i - 1] and ws[i] not in (
                'sehr', 'nein', 'lrudnf', 'heh', 'haha'):
            f.append('WORT-DOPPELT:' + ws[i])
            break
    return f


rows = load_twn() + load_menu() + load_evt()
print('strings=', len(rows))
cats = {}
detail = []
for s in rows:
    f = check(s)
    if not f:
        continue
    for tag in f:
        cats[tag] = cats.get(tag, 0) + 1
    detail.append((s, f))

# Doppelblock-Komposition (nur TWN, nach Offset)
chains = {}
for s in rows:
    if s['src'] == 'TWN':
        chains.setdefault(s['stem'], []).append(s)
chain_flags = []
CHAIN_STOP = set('''der die das den dem des ein eine einen einem einer
und oder aber mit für von vom zu zum zur im in an auf als wie dass
ob wenn weil'''.split())
for stem, items in chains.items():
    items.sort(key=lambda r: r['off'])
    i = 0
    while i < len(items):
        grp = [items[i]]
        while i + 1 < len(items) and not unesc(
                items[i]['en']).rstrip().endswith(TERMINAL):
            i += 1
            grp.append(items[i])
        i += 1
        if len(grp) < 2:
            continue
        de_join = ' '.join(unesc(m['de']).strip() for m in grp)
        en_join = ' '.join(unesc(m['en']).strip() for m in grp)
        d1 = unesc(grp[0]['de']).rstrip()
        d2 = unesc(grp[1]['de']).lstrip()
        w1 = re.findall(r'[A-Za-zÄÖÜäöüß]+', d1.lower())
        cf = []
        if w1 and w1[-1] in CHAIN_STOP and d2[:1].isupper():
            cf.append('SATZBRUCH:%s|%s' % (w1[-1], d2[:14]))
        if en_join.rstrip().endswith('?') and not de_join.rstrip(
                ).endswith('?'):
            cf.append('KETTE-FRAGEZEICHEN')
        if d1.endswith(',') and d2[:1].islower():
            cf.append('KOMMA-KLEIN')
        if re.search(r'[.!?]\s*$', d1) and d2[:1].islower() \
                and not d1.endswith('.'):
            cf.append('SATZ-DANN-KLEIN')
        if de_join.count('(') != de_join.count(')'):
            cf.append('KETTE-KLAMMER')
        if de_join.count('"') % 2 or de_join.count("'") % 2:
            cf.append('KETTE-ANFUEHRUNG')
        if cf:
            chain_flags.append((stem, grp, cf))

out = io.open('_work/review_fixes/qa_accuracy_report.txt', 'w',
              encoding='latin1', newline='\n')
out.write('=== STRING-EBENE (%d Träger, %d mit Befund) ===\n' % (
    len(rows), len(detail)))
for tag, n in sorted(cats.items(), key=lambda kv: -kv[1]):
    out.write('%6d  %s\n' % (n, tag))
out.write('\n')
for s, f in detail:
    out.write('[%s] %s uid=%s\n  EN %r\n  DE %r\n  -> %s\n' % (
        s['src'], s['stem'], s['uid'], unesc(s['en']), unesc(s['de']),
        '; '.join(f)))
out.write('\n=== KETTEN (%d) ===\n' % len(chain_flags))
for stem, grp, cf in chain_flags:
    out.write('# %s uids=%s FLAGS %s\n' % (
        stem, ','.join(m['uid'] for m in grp), ';'.join(cf)))
    for m in grp:
        out.write('  %6s EN %r\n         DE %r\n' % (
            m['uid'], unesc(m['en']), unesc(m['de'])))
    out.write('\n')
out.close()
print('bericht: _work/review_fixes/qa_accuracy_report.txt')
