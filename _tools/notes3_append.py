# append cd234 fix notes to NOTES.md
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''
## CD2-4 LAUFDURCHLAUF (2026-11-06)

### Livedisc-Scan disc2-4 (live_scan_disc.py)
- Keine BTL/FLD-English-Reste mehr auf CD2-4 (vom 1. Batch hatte die
  A5-D2-'A:LOAD...'-Labels und 'NO USE' auf 4 Discs EINDEUTIG einzig CD2-4
  zurueck).
- Die 2-Block-Intro-Zeilen (FMV) sind identisch ueber alle 4 Discs und
  deshalb schriftgeheldselgedeutscht schon seit dem 1. Lauf.

### Disk2-4 NOTES (Matches via live_scan_disc.py hergeleitet und gepatcht)
- MERU == CD1 (nur False-Positives).
- CARA-4 (TWN_CARA.PRG, disc 4) 3-4 Labels in Deutsch:
  '(...Ein Objekt aus der Vorzeit.', '(...)Die Bruecke zerstoert.',
  'Verlasse Ausgrabungsort', 'Bleib hier' (statt 'Don't Endo').
- Zwischen CDs 2-4 gleiche TWN_heiss (E057 disc 2, E120/E121 disc 3,
  CARA disc 4) Shop-Labels:
    'Buy Gun Part' -> 'Teil kaufen',
    'Buy Item' -> 'Kaufen',
    'Sell Gun Part' -> 'Verkauf Teil');
  'Switch Sell/Buy' -> 'Kauf/Verkauf'.
- CD2-4 MODES: CHILDMP.MCB '3 LASER EQUIP CHANGE' -> '3-Laser-Tausch';
  'Not Use' -> 'Unben.' (2 Slots je Disc).
- FLD_A5+FLD_D2 'A:LOAD, B:NOT LOAD, C:ALL LOAD' -> 'A:LADEN, B:NICHT, C:ALLES'
- FLD_A3/A5/B6/C4_6 'NO USE' -> 'LEER.' (mismatch=4 in Toolreport -
  der Tool triggert alte _de.csv-Zeilen mit de==en, Disc enthaelt aber LEER.).
- TWN_CAMP 'Quit Game' (2 Slots je Disc) -> 'Beenden'
  + TWN_CAMP Esle: 'Quit' -> 'Ende' war schon Deutsch (vom kleinen SEEK-Map).
- TWN_RUIN 'How long?' -> 'Wie lang?' (alle 4 Discs, Kern-Slot 101327);
  'Will Training beenden' -> 'Training beenden!' (57668, 4 Discs).
- TWN_SEEK (disc 4): 'for the power of Goettern.' -> 'Kraft der Goetter.'
  (Slot 121663).

### Neue Tools
- cd234_probe.py / cd4_cara_probe.py  - live_disc Binary-Offset-Checker;
- live_scan_disc.py <d>  - EDISC-live-scan per disc (hat eigene EN_WORDS).
- cd234_fixes.py / 2/3 - rows-basierter In-Disc-Patches (alle 4 Discs,
  skip absent).  de2e.csv/de2f.csv/de2g.csv folgen dem selben Namensschema.

### Endcheck
- Disc-Byte-Verify prueft JEDE Zeile: CHILDMP 3-Laser-Tausch, A5 A:LADEN,
  NO USE -> LEER., Quit Game -> Beenden, How long? -> Wie lang?, CARA-4
  3 Labels in German, Seek-Kraft der Goetter. - alles 4 Discs gruen.
- btl_live_ratio: EN-like 5 CD1, auf CD2-4 0 (nur Debug-Artefakte).
- PC-Exe NEU: 47 s, _build/pds-recompile-de/pds-recompile.exe.
'''
out = txt + block
io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n').write(out)
print('notes appended; new len', len(out))
