# Vollstaendiger Sinn-QA-Scan ueber TWN + Menue + FMV-Texte.
# Findet: EN-Word-Leaks, Kuerzungen, haengende Woerter, doppelte
# Satzzeichen, Abkuerzungs-Artefakte, Frage-Punkt-Missmatch,
# Zeilenumbruch-Stil, Kettenfehler und Phrasen-Wiederholungen.
# usage: python qa_sense2.py   (schreibt _work/review_fixes/qa_sense2_report.txt)
import csv
import glob
import io
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='latin1')

EN_WORDS = {'the', 'and', 'you', 'your', "it's", 'its', "don't", 'don',
            'not', 'were', 'have', 'been', 'there', 'with', 'what',
            'why', 'how', 'who', 'which', 'they', 'them', 'just',
            'more', 'some', 'over'}
ALLOW = {'Edge', 'Gash', 'Azel', 'Paet', 'Bezer', 'Jared', 'Zadoc',
         'Vaiman', 'Ladha', 'Craymen', 'Kraymen', 'Sestren', 'Uru',
         'Panzer', 'Dome', 'Ancient'}
DANGLE = {'der', 'die', 'das', 'den', 'dem', 'ein', 'eine', 'einem',
          'einen', 'einer', 'und', 'oder', 'aber', 'im', 'in', 'an',
          'auf', 'fuer', 'mit', 'zu', 'zum', 'zur', 'als', 'wie',
          'von', 'vom', 'sich', 'bei', 'nach', 'so', 'dass', 'denn',
          'wird', 'wird', 'hab', 'hat', 'bin', 'ist', 'brauch',
          'brauche', 'brauchen', 'muss', 'musst', 'kann', 'kannst',
          'bleib', 'bleiben', 'gehe', 'gehst', 'gehen', 'nicht',
          'myself', 'hole', 'bin', 'aber', 'als', 'den', 'ist'}
STOP_SHARED = {'der', 'die', 'das', 'und', 'ist', 'ich', 'ein', 'zu',
               'im', 'in', 'mir', 'mich', 'hat', 'hab', 'sich', 'mit',
               'fuer', 'sie', 'er', 'wir', 'nicht', 'den', 'dem'}


def unesc(s):
    return s.replace('\\n', '\n').replace('\\t', '\t')


def flag_punct(de):
    f = []
    if re.search(r'[,;](?=[A-Za-z])', de):
        f.append('keine-Leerzeichen-nach-Komma')
    if re.search(r'[,;]\.', de):
        f.append('Komma-plus-Punkt')
    if ',,' in de:
        f.append('Doppelkomma')
    if re.search(r'\b[^\W\d_]{1,3}\.\.(?!\.)', de):
        f.append('Abkuerzungs-Artefakt')
    if re.search(r'\s{2,}\.', de):
        f.append('Leerzeichen-vor-Punkt')
    if re.search(r"'\B", de):
        pass
    return f


def flag_repeat(de):
    words = re.findall(r'\w+', de.lower())
    reps = [w for i, w in enumerate(words[:-2])
            if w == words[i + 1] == words[i + 2] and len(w) > 1]
    return ['Wort-x3'] if reps else []


def flag_end(de, lines_only=False):
    f = []
    parts = de.split('\n') if '\n' in de else [de]
    for j, line in enumerate(parts):
        if line.strip().endswith(('...',)) or line.strip() == '':
            continue
        toks = re.findall(r'\w+', line)
        if not toks:
            continue
        last = line.split()[-1].lower().strip('.,!?()')
        has_punct = line.strip().endswith(('.', '!', '?', ')'))
        if has_punct:
            continue
        if last in DANGLE or (len(last) <= 3 and last.isalpha()
                              and not last.encode('latin1', 'ignore')):
            f.append('haengendes-Woertchen-%r line%d' % (last, j + 1))
            continue
    # Frage-Punkt-Vergleiche testet man separat (braucht EN).
    return f


def flag_break_style(de):
    f = []
    lines = de.split('\n')
    if len(lines) > 1:
        for j in range(len(lines) - 1):
            a, b = lines[j], lines[j + 1]
            if a.strip().endswith(('.', '!', '?', ')')) or \
                    a.strip() == '' or b.strip() == '':
                continue
            toks = re.findall(r'\w+', a)
            if toks and toks[-1].islower() and len(toks[-1]) >= 3 and \
                    b and b[0].isupper():
                f.append('Zeile%d-endet-lowercase, Zeile%d-Grossstart'
                         % (j + 1, j + 2))
    return f


def flag_q(en, de):
    f = []
    en_end = en.strip()[-1:] if en.strip() else ''
    de_end = de.strip()[-1:] if de.strip() else ''
    if en_end == '?' and de_end and de_end in '.!,' and \
            '?' not in de.strip():
        f.append('EN-Frage-punkt-DE')
    if en_end == '!' and de_end == '.':
        f.append('EN-Ausruf-DE-Punkt')
    return f


def flag_short(en, de):
    en2 = en.strip()
    de2 = de.strip()
    if len(en2) < 25 or len(de2) < 4:
        return []
    # Ketten: EN mit Ellipse oder Klammern um Enden hinweg
    if en2.endswith('...') and de2.endswith('...'):
        return []
    ratio = len(de2) / max(len(en2), 1)
    if ratio < 0.60:
        return ['KUERZUNG-VERDACHT %.2f' % ratio]
    return []


def flag_dup_chain(triple):
    f = []
    (a, b, c) = triple
    wa = set(re.findall(r'\w+', b['de'].lower()))
    wc = set(re.findall(r'\w+', c['de'].lower()))
    shared = wa & wc - STOP_SHARED
    if len(shared) >= 5 and len(b['de']) > 10:
        f.append('phrasen-widerholung %s' % sorted(shared)[:5])
    return f


def scan_row(fam, row, next_de=None):
    de = unesc(row['de'])
    en = unesc(row['en'])
    f = []
    if de == en and len(de) > 4:
        en_s = en.strip()
        looks_sentence = (' ' in en_s and
                          any(c in en_s for c in ',.!?)(') and
                          not en_s.isupper())
        if looks_sentence and not re.search(r'\b(%s)\b' % '|'.join(
                ALLOW), en_s):
            f.append('unuebersetzt-Satz')
    words = [w for w in re.findall(r"[a-zA-Z']+", de.lower())
             if w in EN_WORDS]
    if len(words) >= 1 and not (de == en):
        f.append('EN-woerter:%s' % words[:3])
    f.extend(flag_punct(de))
    f.extend(flag_repeat(de))
    # haengende Woertchen nur als CRITICAL melden, wenn der Naechste
    # Abschnitt NICHT kleinschreibend weiterfuehrt.
    for x in list(flag_end(de)):
        cont = False
        if '\n' in de:
            pass
        elif next_de and next_de.strip()[:1].islower():
            cont = True
        if not cont:
            f.append(x)
    f.extend(flag_break_style(de))
    f.extend(flag_q(en, de))
    f.extend(flag_short(en, de))
    return f


rows_out = []
counts = Counter()


def add(fam, fid, en, de, flags, ctx):
    if not flags:
        return
    counts[tuple(sorted(set(x.split()[0] for x in flags)))] += 1
    rows_out.append((fam, fid, ','.join(sorted(set(flags))), en, de,
                     ctx))


def load_twn():
    for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
        base = os.path.basename(path)[:-7]
        rows = []
        with io.open(path, encoding='latin1') as fh:
            for line in fh:
                p = line.rstrip('\r\n').split(';')
                if len(p) >= 6 and p[0].isdigit():
                    rows.append({'uid': int(p[0]),
                                 'off': int(p[2].split('|')[0]) if p[2]
                                 else 0,
                                 'en': p[4], 'de': p[5]})
        rows.sort(key=lambda r: r['off'])
        for i, r in enumerate(rows):
            n_de = unesc(rows[i + 1]['de']) if i + 1 < len(rows) else None
            ctx = []
            for k in (i - 1, i + 1):
                if 0 <= k < len(rows):
                    ctx.append('uid%d en=%r de=%r' % (
                        rows[k]['uid'], unesc(rows[k]['en'])[:60],
                        unesc(rows[k]['de'])[:60]))
            fl = scan_row('TWN', r, next_de=n_de)
            if i >= 2:
                fl.extend(flag_dup_chain((None, rows[i - 1], rows[i])))
            add(base, 'uid%d' % r['uid'],
                unesc(r['en']), unesc(r['de']), fl, ' || '.join(ctx))


def load_menu():
    for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
        base = 'menu/' + os.path.basename(path)
        with io.open(path, encoding='latin1') as fh:
            rd = csv.reader(fh, delimiter=';')
            head = next(rd, None)
            for r in rd:
                if len(r) < 6 or r[0] != base.split('_de.csv')[0] \
                        and len(r) < 7:
                    if len(r) < 6 or not r[0].startswith('FLD') \
                            and not r[0].endswith(('.FNT', '.MCB',
                                                   '.SCB', '.CGB')):
                        if len(r) < 6:
                            break
                f, off, prefix, ln, en, de = r[:6]
                fl = scan_row('menu', {'en': en, 'de': de})
                add(base, 'off%s' % off, unesc(en), unesc(de), fl, '')


def load_evt():
    path = '_work/evt_ev_de_map.csv'
    path = '_work/evt_de_map.csv'
    if not os.path.isfile(path):
        return
    with io.open(path, encoding='latin1') as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip('\r\n')
            if not line or line.startswith('#') or ';' not in line:
                continue
            en, de = line.split(';', 1)
            fl = scan_row('fmv', {'en': en, 'de': de})
            add('fmv', 'line%d' % n, unesc(en), unesc(de), fl, '')


load_twn()
load_menu()
load_evt()

out = io.open('_work/review_fixes/qa_sense2_report.txt', 'w',
              encoding='latin1', newline='\n')
for fam, fid, flags, en, de, ctx in rows_out:
    out.write('=== %s %s [%s]\n' % (fam, fid, flags))
    out.write('  EN: %r\n' % (en,))
    out.write('  DE: %r\n' % (de,))
    if ctx:
        out.write('  CTX: %s\n' % ctx)
out.close()

print('Antraege geliefert: %d' % len(rows_out))
for k, v in counts.most_common(20):
    print('  %-32s %d' % ('+'.join(k), v))
print('bericht: _work/review_fixes/qa_sense2_report.txt')
