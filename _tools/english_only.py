# -*- coding: utf-8 -*-
import collections
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
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

rows = []
for ln in io.open('_work/review_fixes/english_candidates.txt',
                  encoding='latin1'):
    p = ln.rstrip('\n').split(';', 3)
    if len(p) != 4:
        continue
    d, name, off, t = p
    letters = sum(c.isalpha() for c in t)
    if letters < 6 or len(t) < 6:
        continue
    if DE.search(t):
        continue
    if not EN.search(t):
        continue
    rows.append((t, name, off))

by = collections.OrderedDict()
for t, name, off in rows:
    by.setdefault(t, []).append((name, off))
print('unique english', len(by))
for t, locs in by.items():
    files = sorted(set(n for n, o in locs))
    print('%-66s|%2d|%s' % (t[:66], len(locs), ','.join(files)[:60]))
