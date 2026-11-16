# -*- coding: utf-8 -*-
"""Wandelt ae/oe/ue (und ausgewaehlte ss) in die Font-Slots um.

Slots: ä=^  ö=|  ü=~  ß={
Ausnahmen verhindern falsche Umwandlungen (Bauer, Feuer, Quelle,
dass, Schloss, Namen ...). Modus: dry | apply
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
SLOT = {'ä': '^', 'ö': '|', 'ü': '~', 'ß': '{'}

# Woerter, in denen "ue" KEIN ü ist
UE_EXCEPT = {
    'bauer', 'bauern', 'bauernhof', 'feuer', 'feuern', 'feuerholz',
    'feuerkraft', 'feuerbereit', 'feuernd', 'waechterfeuer',
    'waechterfeuers', 'saettigungsfeuer', 'zufallsfeuer',
    'steuer', 'steuern', 'steuerst', 'steuert', 'steuerkreuz',
    'teuer', 'teure', 'teurer', 'teures', 'teuren',
    'treu', 'treue', 'treuen', 'treuer', 'treues',
    'neu', 'neue', 'neuen', 'neuer', 'neues', 'neuem', 'neueste',
    'neuerdings', 'abenteuer', 'abenteuern', 'abenteuerlich',
    'schauen', 'nachschauen', 'schauer', 'sauer', 'sauerei',
    'trauen', 'traue', 'vertrauen', 'vertraue', 'trauern',
    'statue', 'statuen', 'queen', 'quelle', 'quellen', 'queren',
    'bequem', 'durchqueren', 'konsequenzen', 'lichtquelle',
    'kraftquelle', 'angeheuerter', 'euer', 'greuel', 'steuere',
    'steuerst', 'tue', 'tuest', 'blue', 'clue',
    'eventuell', 'aktuell', 'manuell', 'sexuell', 'intellektuell',
    'punktuell', 'konzeptuell', 'visuell', 'graduell', 'individuell',
    'duell', 'duelle', 'duellen', 'duells',
}
UE_SUFFIX_KEEP = ()
AE_EXCEPT = {'michael', 'rafael', 'israel', 'paet', 'paets', "paet's",
             'jael', 'aaron', 'aerobic', 'mael', 'cael'}
OE_EXCEPT = {'soeben', 'poesie'}

# Woerter mit ß (kuratierte, sichere Liste)
SS_SET = {
    'gross', 'grosse', 'grosser', 'grosses', 'grossen', 'grossem',
    'groesser', 'groessere', 'groesserer', 'groesseres', 'groesseren',
    'groesserem', 'groesste', 'groessten', 'groesster', 'groesse',
    'grossteil', 'grossartig', 'weiss', 'weisse', 'weisser', 'weisses',
    'weissen', 'weisst', 'weissglut', 'heiss', 'heisse', 'heisser',
    'heisses', 'heissen', 'heisst', 'fuss', 'fuesse', 'fuessen',
    'draussen', 'strasse', 'strassen', 'spass', 'schliessen',
    'schliesse', 'schliesst', 'schliesslich', 'schiessen', 'schiesse',
    'schiesst', 'schiess', 'fliessen', 'fliesse', 'fliesst',
    'fliessendem', 'giessen', 'giesse', 'giesst', 'geniessen',
    'geniesse', 'geniesst', 'beissen', 'beisse', 'beisst', 'reissen',
    'reisse', 'reisst', 'zerreisse', 'zerreissen', 'liess', 'liessen',
    'verliess', 'verliessen', 'entliessen', 'verliessest', 'suess',
    'suesse', 'suesser', 'suesses', 'suessen', 'bloss', 'aussen',
    'ausser', 'ausserhalb', 'aussergewoehnlich', 'aussenwelt',
    'aussenstehende', 'aussenstehenden', 'aussenstehender',
    'aussenst', 'erfahrungsgemaess', 'gemaess', 'gewaesser',
}

WORD_RE = re.compile(r"[A-Za-z]+")
UPPER_SLOT = {'^': '`', '|': '[', '~': ']'}


def convert_word(w):
    if w.isupper():
        return w
    low = w.lower()
    if 'statu' in low:
        # Statue/Statuen/Holzstatuen: "ue" ist kein ü
        return w
    chars = list(w)
    for a, b, rep in (('a', 'e', '^'), ('o', 'e', '|'), ('u', 'e', '~')):
        i = 0
        while i < len(chars) - 1:
            if chars[i].lower() == a and chars[i + 1].lower() == b:
                if i == 0 and chars[0].isupper():
                    if a == 'a' and low in AE_EXCEPT:
                        i += 1
                        continue
                    if a == 'o' and low in OE_EXCEPT:
                        i += 1
                        continue
                    if a == 'u' and low in UE_EXCEPT:
                        i += 1
                        continue
                    chars[i] = UPPER_SLOT[rep]
                    del chars[i + 1]
                    continue
                if a == 'u':
                    if low in UE_EXCEPT or low.endswith(UE_SUFFIX_KEEP):
                        i += 1
                        continue
                    if i > 0 and chars[i - 1].lower() in 'aeiouq':
                        i += 1
                        continue
                if a == 'a' and low in AE_EXCEPT:
                    i += 1
                    continue
                if a == 'o' and low in OE_EXCEPT:
                    i += 1
                    continue
                chars[i] = rep
                del chars[i + 1]
            else:
                i += 1
    out = ''.join(chars)
    if low in SS_SET:
        out = out.replace('ss', '{').replace('SS', '{')
    return out


def convert_text(t):
    return WORD_RE.sub(lambda m: convert_word(m.group(0)), t)


def unescape(s):
    """CSV-Schreibweise (\\n) -> echte Disc-Bytes (0x0A)."""
    return s.replace('\\n', '\n')


def escape(s):
    """Echte Disc-Bytes (0x0A) -> CSV-Schreibweise (\\n)."""
    return s.replace('\n', '\\n')


def stem_to_file(stem):
    base = stem
    for suf in ('_d2', '_d3', '_d4'):
        if base.endswith(suf):
            base = base[:-3]
    if base == 'TWN_E128_cd3':
        return 'TWN_E128.PRG'
    return base.replace('_PRG', '.PRG')


def load_rows():
    rows = []
    for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
        stem = os.path.basename(path)[:-7]
        for i, ln in enumerate(io.open(path, encoding='latin1')):
            p = ln.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                offs = [int(x) for x in p[3].split('|') if x]
                if not offs:
                    try:
                        offs = [int(p[2].split('|')[0])]
                    except Exception:
                        offs = []
                rows.append({'csv': path, 'line': i, 'uid': p[0],
                             'file': stem_to_file(stem), 'offs': offs,
                             'en': p[4], 'de': p[5]})
    for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
        for i, ln in enumerate(io.open(path, encoding='latin1')):
            p = ln.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[1].isdigit() and p[0]:
                rows.append({'csv': path, 'line': i, 'uid': p[1],
                             'file': p[0], 'offs': [int(p[1])],
                             'en': p[4], 'de': p[5]})
    return rows


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv_rows(fs) if int(r['lba']) > 0}


def csv_rows(path):
    import csv as _csv
    return list(_csv.DictReader(open(path, encoding='latin1'),
                               delimiter=';'))


def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def write_file(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'
rows = load_rows()
changes = []
words = {}
for r in rows:
    new = convert_text(r['de'])
    if new != r['de']:
        changes.append((r, new))
        for m in WORD_RE.finditer(r['de']):
            w = m.group(0)
            nw = convert_word(w)
            if nw != w:
                words[w] = nw
print('rows=%d changed=%d unique_words=%d mode=%s' % (
    len(rows), len(changes), len(words), MODE))
for w in sorted(words)[:400]:
    print('  %s -> %s' % (w, words[w]))
if DRY:
    sys.exit(0)

# CSV-Schreibpuffer (nur erfolgreich geschriebene Zeilen!)
csv_lines = {}


def mark_csv(r, new):
    if r['csv'] not in csv_lines:
        csv_lines[r['csv']] = io.open(r['csv'], encoding='latin1'
                                      ).read().split('\n')
    ln = csv_lines[r['csv']][r['line']].rstrip('\r\n').split(';')
    ln[5] = new
    csv_lines[r['csv']][r['line']] = ';'.join(ln)

# Discs patchen: pro (disc, file) einmal laden
def actual(data, o):
    e = o
    while e < len(data) and data[e] not in (0x00, 0xFF):
        e += 1
    return data[o:e].decode('latin1')


apply = {}
stats = {'written': 0, 'skip': 0, 'budget': 0, 'repair': 0}
fails = []
for r, new in changes:
    old = r['de']
    if not r['offs']:
        fails.append((r, 'no-offsets'))
        continue
    ob = unescape(old).encode('latin1')
    nb = unescape(new).encode('latin1')
    if len(nb) > len(ob):
        stats['budget'] += 1
        fails.append((r, 'budget %d>%d' % (len(nb), len(ob))))
        continue
    ok = False
    csv_new = new
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if r['file'] not in idx:
            continue
        key = (d, r['file'])
        if key not in apply:
            lba, size = idx[r['file']]
            apply[key] = [lba, bytearray(read_file(
                '_work/patched_disc%d.bin' % d, lba, size))]
        data = apply[key][1]
        for off in r['offs']:
            if off + len(ob) > len(data):
                stats['skip'] += 1
                continue
            if bytes(data[off:off + len(ob)]) == ob:
                end = off + max(len(ob), len(nb))
                data[off:off + len(nb)] = nb
                fill = off + len(nb)
                for k in range(fill, min(end, len(data))):
                    data[k] = 0x00 if k == fill else 0xFF
                stats['written'] += 1
                ok = True
            elif bytes(data[off:off + len(nb)]) == nb:
                ok = True
            else:
                # Disc ist autoritativ: tatsaechlichen Text konvertieren
                act = actual(data, off)
                if act and all(c == '\n' or 32 <= ord(c) < 127 for c in act):
                    na = convert_text(act)
                    nab = na.encode('latin1')
                    if len(nab) <= len(act.encode('latin1')):
                        end = off + max(len(act.encode('latin1')),
                                        len(nab))
                        data[off:off + len(nab)] = nab
                        fill = off + len(nab)
                        for k in range(fill, min(end, len(data))):
                            data[k] = 0x00 if k == fill else 0xFF
                        stats['repair'] += 1
                        ok = True
                        csv_new = escape(na)
                    else:
                        stats['budget'] += 1
                else:
                    stats['skip'] += 1
    if ok:
        mark_csv(r, csv_new)
    else:
        fails.append((r, 'bytes-mismatch'))
for (d, name), (lba, data) in apply.items():
    write_file('_work/patched_disc%d.bin' % d, lba, bytes(data))
for path, lines in csv_lines.items():
    io.open(path, 'w', encoding='latin1', newline='').write(
        '\n'.join(lines))
with io.open('_work/review_fixes/umlaut_apply_fails.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for r, why in fails:
        f.write('%s | %s | offs=%s | %s | %s -> %s\n' % (
            r['csv'], r['file'], r['offs'][:4], why,
            r['de'], convert_text(r['de'])))
print('discs: written=%d repair=%d skip=%d budget=%d fails=%d files=%d' % (
    stats['written'], stats['repair'], stats['skip'],
    stats['budget'], len(fails), len(apply)))
