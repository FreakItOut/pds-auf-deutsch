# append found-and-patched notes to NOTES.md
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''
## "The one who controls Edge" (2026-11-06, geleakter Satz behoben)

### raw-disc-Scanner (find_edge_phrase.py / _probe_d5.py)
- 'The one who controls Edge,' lag in FLD_D5.FNT (nicht BTL_D5):
  Layout: Sestren-Dialog an Azel im D5-Feld. Auf ALLEN 4 Discs in deutscher
  Version oberhalb von 'wie ist dein Name?' - veraltet war nur die "one
  who controls"-Zeile. Der Single-Line-Slot hat nur 27 byte
  ("Wer dich steuert, Edge," = 23 bytes) - passt exakt.
- Gleiche Pass-NOTSCHLUSS: auch die aehnliche Zeile
  'The Attack Type specific / Berserk Technique is / Assault Wing ...' in
  FLD_A7.FNT (4-Disc, nicht "The" davor) und
  'Watch out for the ones with horns.' in BTL_A5.FNT und
  'This must be the one...' in E014.EPK (bzw Disc-1 only).
  Alle 4 Slots in gleicher Weise mit Budget-Zulauf gepatcht:
  A7: 'Die Angriff-Typ-\\nBerserk-Technik ist\\nAngriffsfluegel:\\nerhoeht
      die Laserkraft.'
  A5: 'Achte auf die mit Hoernern.'
  E14: 'Das muss es sein...'
- Includes E014.EPK (nur CD1) und BTL_A5 für alle 4 Discs (CD2-4 vorhanden).

### Tools
- find_edge_phrase.py, _probe_d5.py, fld_d5_phrase_fix.py,
  a5_e014_fix.py, fld_a7_type_fix.py.

### Endstand
- BTL_D5.FNT alle 4 Discs, alle Fld_A5, A7.fragment - verify_twn4: ok=8372
  0 len 0 mismatch.
- PC-Exe: _build/pds-recompile-de/pds-recompile.exe NEU (42 s).
'''
with io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + block)
print('appended')
