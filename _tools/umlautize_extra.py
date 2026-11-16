# -*- coding: utf-8 -*-
"""Setzt die in patch_extra.py geschriebenen Texte auf Font-Slots um."""
import collections
import csv as _csv
import io
import re
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


recs = {r['name']: (int(r['lba']), int(r['size']))
        for r in _csv.DictReader(open('_work/fs_records_all.csv',
                                      encoding='latin1'), delimiter=';')
        if r['lba'].isdigit() and int(r['lba']) > 0}

# Deutsche Texte aus extra_de uebernehmen
from extra_de import T

hits = collections.defaultdict(list)
for ln in io.open('_work/review_fixes/english_candidates.txt',
                  encoding='latin1'):
    p = ln.rstrip('\n').split(';', 3)
    if len(p) == 4 and p[3] in T:
        hits[(int(p[0][1:]), p[1])].append((int(p[2], 16), p[3]))

files = {}
done = 0
skip = 0
for (d, name), items in sorted(hits.items()):
    if name not in recs:
        continue
    lba, size = recs[name]
    key = (d, name)
    if key not in files:
        out = bytearray()
        need, s = size, lba
        with open('_work/patched_disc%d.bin' % d, 'rb') as f:
            while need > 0:
                f.seek(s * SECT + 16)
                c = f.read(min(DATA, need))
                if not c:
                    break
                out += c
                need -= len(c)
                s += 1
        files[key] = [lba, bytearray(out[:size])]
    data = files[key][1]
    for off, en in items:
        cur = T[en]
        new = convert_text(cur)
        if new == cur:
            continue
        cb = cur.encode('latin1')
        nb = new.encode('latin1')
        if len(nb) > len(cb):
            skip += 1
            continue
        if bytes(data[off:off + len(cb)]) != cb:
            skip += 1
            continue
        end = off + len(cb)
        data[off:off + len(nb)] = nb
        fill = off + len(nb)
        for k in range(fill, end):
            data[k] = 0x00 if k == fill else 0xFF
        done += 1
for (d, name), (lba, data) in files.items():
    with open('_work/patched_disc%d.bin' % d, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])
print('umlautized=%d skip=%d files=%d' % (done, skip, len(files)))
