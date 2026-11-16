# append note about kuerzungs-need to NOTES.md
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''

## KUERZUNGS-WOHL FrAGER (2026-11-06,				
bald(Method):	p.new)

### slack_classify.py:  kuerzen- length need
  Disc-Message:  alle 1250 TWN subtitle-slots sind PACKED between other
  engine code (model reference, pointer tables, PCM path markers).  
  Measured total slack:  732,315 bytes alive in tight row's gap  -> 
  NO freely-0x00/0xFF region to allow longer German.  Coming from live
  code, cannot be repurposed inline.
- so: je Slot=German must fit in the EN slot budget  - cuts are STRUCTURAL
  (game-engine-embedded), not a German model choice.

### Wenn Du wirklich laengere deutsche Saetze willst:
  1. Disc-rebuild:  move whole subtitle region to a NEW sector zone
     (needs pointer re-link + table relinking per TWN) - overhaul.
  2. Reallocate an "annex" area in a spare disc sector - same overhaul.
  3. Continue tightening the EN-constrained German (the current
     approach; ~1072 slots already fit within 95..100% budget; 511
     are at the exact budget and ~560 in the 1..3 byte room they have).
- My recommendation:  option (3)  - the current German fits the box,
  reads naturally per sentence, and the user has already seen them in
  context.  Option (1)+(2) is only for a major disc-rebuild rewrite;
  not necessary for this patch.

### Ressources (my inclination)
- slack_probe2.py      - slack per file
- slack_classify.py    - safe vs LIVE-region classification
- tight_check.py       - list of all tight budget rows
'''
with io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + block)
print('appended')
