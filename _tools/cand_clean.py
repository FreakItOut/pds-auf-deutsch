# -*- coding: utf-8 -*-
import collections
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
rows = []
for ln in io.open('_work/review_fixes/english_candidates.txt',
                  encoding='latin1'):
    p = ln.rstrip('\n').split(';', 3)
    if len(p) == 4:
        rows.append(p)

OK = re.compile(r"^[A-Za-z0-9 %.,!?'\"()<>:/+&;_-]+$")
EN = re.compile(r"\b(the|you|your|and|that|with|have|this|what|are|will|"
                r"from|they|there|about|could|should|when|where|which|"
                r"their|them|then|than|into|can|not|for|but|all|his|her|"
                r"she|him|out|just|only|more|now|again|still|also|"
                r"get|got|make|take|come|know|think|see|look|say|tell|"
                r"give|find|want|need|must|may|us|we|me|my|our|its|"
                r"is|was|were|has|had|been|will|would|do|does|did)\b",
                re.I)
DE = re.compile(r"\b(ich|nicht|und|der|die|das|ein|eine|mit|von|auf|"
                r"ist|sind|war|den|dem|des|zu|sich|wir|sie|ihr|er|es|"
                r"hat|habe|haben|wird|werden|kann|muss|ueber|fuer|oder|"
                r"aber|wenn|auch|nur|noch|schon|mehr|sehr|hier|dort|"
                r"jetzt|dann|doch|weil|dass|mein|deine|diese|zum|zur|"
                r"beim|vom|als|wie|was|wer|wo|warum|kein|keine|mir|"
                r"mich|dir|dich|uns|euch|bin|bist|seid)\b", re.I)

by_text = collections.OrderedDict()
for d, name, off, t in rows:
    if not OK.match(t):
        continue
    letters = sum(c.isalpha() for c in t)
    if letters < 8 or len(t) < 8:
        continue
    if DE.search(t):
        continue
    if not (EN.search(t) or t.startswith('<') or
            re.search(r'[.!?]$', t)):
        continue
    if re.search(r'(.)\1\1', t):
        continue
    by_text.setdefault(t, []).append((d, name, off))

print('unique', len(by_text))
for t, locs in by_text.items():
    files = sorted(set(x[1] for x in locs))
    print('%-70s | %d | %s' % (t[:70], len(locs), ','.join(files)[:70]))
