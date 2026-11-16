# -*- coding: utf-8 -*-
"""Synchronisiert alle CSV-Textzeilen mit den Discs und setzt dabei
ae/oe/ue/ss in die Font-Slots um. Disc ist autoritativ."""
import glob
import io
import os
import re
import csv as _csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

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
AE_EXCEPT = {'michael', 'rafael', 'israel', 'paet', 'paets', "paet's",
             'jael', 'aaron', 'aerobic', 'mael', 'cael'}
OE_EXCEPT = {'soeben', 'poesie'}
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
                    if low in UE_EXCEPT:
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


def escape(s):
    return s.replace('\n', '\\n')


def load_rows():
    rows = []
    for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
        stem = os.path.basename(path)[:-7]
        base = stem
        for suf in ('_d2', '_d3', '_d4'):
            if base.endswith(suf):
                base = base[:-3]
        if base == 'TWN_E128_cd3':
            fname = 'TWN_E128.PRG'
        else:
            fname = base.replace('_PRG', '.PRG')
        for i, ln in enumerate(io.open(path, encoding='latin1')):
            p = ln.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                offs = [int(x) for x in p[3].split('|') if x]
                if not offs:
                    try:
                        offs = [int(p[2].split('|')[0])]
                    except Exception:
                        offs = []
                rows.append({'csv': path, 'line': i, 'file': fname,
                             'offs': offs, 'en': p[4], 'de': p[5]})
    for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
        for i, ln in enumerate(io.open(path, encoding='latin1')):
            p = ln.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[1].isdigit() and p[0]:
                rows.append({'csv': path, 'line': i, 'file': p[0],
                             'offs': [int(p[1])], 'en': p[4], 'de': p[5]})
    return rows


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in _csv.DictReader(open(fs, encoding='latin1'),
                                     delimiter=';') if int(r['lba']) > 0}


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


rows = load_rows()
cache = {}
written = 0
skip = 0
same = 0
csv_lines = {}
idx_cache = {}
for r in rows:
    if not r['offs']:
        skip += 1
        continue
    for d in (1, 2, 3, 4):
        if d not in idx_cache:
            idx_cache[d] = fs_index(d)
        idx = idx_cache[d]
        if r['file'] not in idx:
            continue
        key = (d, r['file'])
        if key not in cache:
            lba, size = idx[r['file']]
            cache[key] = [lba, bytearray(read_file(
                '_work/patched_disc%d.bin' % d, lba, size))]
        data = cache[key][1]
        for off in r['offs']:
            e = off
            while e < len(data) and data[e] not in (0x00, 0xFF):
                e += 1
            act = data[off:e].decode('latin1')
            if not act or not all(c == '\n' or 32 <= ord(c) < 127
                                  for c in act):
                skip += 1
                continue
            new = convert_text(act)
            if new != act:
                nb = new.encode('latin1')
                ob = act.encode('latin1')
                if len(nb) > len(ob):
                    skip += 1
                    continue
                end = off + max(len(ob), len(nb))
                data[off:off + len(nb)] = nb
                fill = off + len(nb)
                for k in range(fill, min(end, len(data))):
                    data[k] = 0x00 if k == fill else 0xFF
                written += 1
            else:
                same += 1
            if r['csv'] not in csv_lines:
                csv_lines[r['csv']] = io.open(
                    r['csv'], encoding='latin1').read().split('\n')
            ln = csv_lines[r['csv']][r['line']].rstrip('\r\n').split(';')
            ln[5] = escape(new)
            csv_lines[r['csv']][r['line']] = ';'.join(ln)
for (d, name), (lba, data) in cache.items():
    write_file('_work/patched_disc%d.bin' % d, lba, bytes(data))
for path, lines in csv_lines.items():
    io.open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines))
print('rows=%d written=%d same=%d skip=%d files=%d csvs=%d' % (
    len(rows), written, same, skip, len(cache), len(csv_lines)))
