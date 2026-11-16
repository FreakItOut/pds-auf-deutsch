# -*- coding: utf-8 -*-
"""Extrahiert null-terminierte ASCII-Strings (Textbereiche) aus allen
Disc-Dateien und filtert englische Kandidaten."""
import csv
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
SKIP_EXT = ('.PNB', '.CGB', '.SND', '.PCM', '.WAV', '.MOV', '.CPK',
            '.ADX', '.SEQ', '.EXB', '.BDB')

de_corpus = ''
for p in (glob.glob('_work/subtitles/*_de.csv') +
          glob.glob('_work/menu_de/*_de.csv')):
    try:
        de_corpus += io.open(p, encoding='latin1', errors='ignore').read()
    except Exception:
        pass

EN = re.compile(r"\b(the|you|your|and|that|with|have|has|this|what|are|"
                r"is|was|were|will|would|from|they|there|their|them|"
                r"then|than|into|can|not|for|but|all|his|her|she|him|"
                r"one|out|about|could|should|when|where|which|who|why|"
                r"how|any|some|just|only|very|more|most|now|again|still|"
                r"also|back|down|off|over|after|before|because|if|so|no|"
                r"yes|do|does|did|been|get|got|make|made|take|come|came|"
                r"know|think|see|look|say|said|tell|told|give|find|found|"
                r"want|need|must|may|might|shall|us|we|me|my|our|its|"
                r"it's|i'm|i've|don't|can't|won't|let's|there's)\b", re.I)
DE = re.compile(r"\b(ich|nicht|und|der|die|das|ein|eine|mit|von|auf|"
                r"ist|sind|war|den|dem|des|zu|sich|wir|sie|ihr|er|es|"
                r"hat|habe|haben|wird|werden|kann|muss|ueber|fuer|oder|"
                r"aber|wenn|auch|nur|noch|schon|mehr|sehr|hier|dort|"
                r"jetzt|dann|doch|weil|dass|mein|deine|diese|zum|zur|"
                r"beim|vom|als|wie|was|wer|wo|warum|kein|keine|mir|"
                r"mich|dir|dich|uns|euch|bin|bist|seid)\b", re.I)
NAME = re.compile(r'^[<(]?[A-Za-z0-9_#]+\.(MCB|PRG|FNT|EPK|PCM|SCB|CGB|'
                  r'PNB|BIN|SND|SEQ|EXB|BDB|DAT|CGZ)', re.I)

recs = list(csv.DictReader(open('_work/fs_records_all.csv',
                                encoding='latin1'), delimiter=';'))
out = io.open('_work/review_fixes/english_texts.txt', 'w',
              encoding='latin1', newline='\n')
seen = set()
for disc in (1, 2, 3, 4):
    with open('_work/patched_disc%d.bin' % disc, 'rb') as f:
        for r in recs:
            name = r['name']
            if name.upper().endswith(SKIP_EXT):
                continue
            if not (r['lba'].isdigit() and r['size'].isdigit()):
                continue
            lba, size = int(r['lba']), int(r['size'])
            if lba == 0 or size == 0 or size > 4 * 1024 * 1024:
                continue
            buf = bytearray()
            need, s = size, lba
            while need > 0:
                f.seek(s * SECT + 16)
                c = f.read(min(DATA, need))
                if not c:
                    break
                buf += c
                need -= len(c)
                s += 1
            d = bytes(buf[:size])
            for m in re.finditer(rb'[\x20-\x7e\x0a]{4,}', d):
                t = m.group().decode('latin1').replace('\n', '\\n')
                if t in de_corpus or NAME.match(t):
                    continue
                if len(t) < 6 or len(t) > 90:
                    continue
                letters = sum(c.isalpha() for c in t)
                if letters < 6 or letters < len(t) * 0.6:
                    continue
                if DE.search(t):
                    continue
                if not (EN.search(t) or t.startswith('<') or
                        (t[:1].isupper() and t.rstrip().endswith(('.', '?', '!')))):
                    continue
                key = t
                if key in seen:
                    continue
                seen.add(key)
                out.write('d%d;%s;%06x;%s\n' % (disc, name, m.start(), t))
out.close()
print('unique', len(seen))
