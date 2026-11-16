# -*- coding: utf-8 -*-
# Findet englische Textkandidaten in allen Disc-Dateien (ausser Grafik/Audio).
import csv
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

de_corpus = ''
for p in (glob.glob('_work/subtitles/*_de.csv') +
          glob.glob('_work/menu_de/*_de.csv')):
    try:
        de_corpus += io.open(p, encoding='latin1', errors='ignore').read()
    except Exception:
        pass

EN = re.compile(r"\b(the|you|your|yours|and|that|with|have|has|had|this|"
                r"what|are|is|was|were|will|would|from|they|there|their|"
                r"them|then|than|into|can|cannot|not|for|but|all|his|her|"
                r"she|him|one|out|about|could|should|when|where|which|"
                r"who|why|how|any|some|just|only|very|more|most|now|"
                r"again|still|also|back|down|up|off|over|after|before|"
                r"because|if|so|no|yes|do|does|did|done|been|being|"
                r"get|got|make|made|take|took|come|came|know|think|"
                r"see|look|say|said|tell|told|give|gave|find|found|"
                r"want|need|must|may|might|shall|us|we|me|my|your|our|"
                r"its|it's|i'm|i've|don't|can't|won't|let's|there's)\b",
                re.I)
DE = re.compile(r"\b(ich|nicht|und|der|die|das|ein|eine|einen|einem|"
                r"einer|mit|von|auf|ist|sind|war|waren|den|dem|des|zu|"
                r"sich|wir|sie|ihr|ihre|ihren|er|es|hat|habe|haben|"
                r"wird|werden|kann|kannst|koennen|muss|muessen|ueber|"
                r"fuer|oder|aber|wenn|auch|nur|noch|schon|mehr|sehr|"
                r"hier|dort|jetzt|dann|doch|weil|dass|gross|klein|gut|"
                r"mein|meine|dein|deine|dieser|diese|dieses|zum|zur|"
                r"beim|vom|am|im|in|als|wie|was|wer|wo|warum|kein|"
                r"keine|mir|mich|dir|dich|uns|euch|bin|bist|seid|hab)\b",
                re.I)

SKIP_EXT = ('.PNB', '.CGB', '.SND', '.PCM', '.WAV', '.MOV', '.CPK',
            '.ADX', '.DAT')

recs = list(csv.DictReader(open('_work/fs_records_all.csv',
                                encoding='latin1'), delimiter=';'))
out = io.open('_work/review_fixes/english_candidates.txt', 'w',
              encoding='latin1', newline='\n')
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
            for m in re.finditer(rb'[ -~]{6,}', d):
                t = m.group().decode('latin1')
                letters = sum(ch.isalpha() for ch in t)
                if letters < 6 or letters < len(t) * 0.55:
                    continue
                if t in de_corpus:
                    continue
                if DE.search(t) and not EN.search(t):
                    continue
                if not (EN.search(t) or t.startswith('<') or
                        (t[:1].isupper() and t.rstrip().endswith(('.', '?', '!')))):
                    continue
                out.write('d%d;%s;%06x;%s\n' % (disc, name, m.start(), t))
out.close()
print('written')
