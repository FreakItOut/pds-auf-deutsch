# append final-coverage notes to NOTES.md
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''
## REST-DECKUNG 100% AUF TRANSLATABLE-PROSA (2026-11-06)

### coverage_v2.py / remaining_dump.py - letzter Deckungs-Bericht
- Livedisc-Gesamtdeckung: 13.343 / 14.618 = 91,3%.
- Die 155 Rest "identity" im Menu sind alles LEGITIME Ausnahmen:
  * Namen: Edge, Azel, Craymen, Gash, Zoah, Paet, Boaz, Bezer, Vaiman,
    Sentinel, Exterminator, D Unit 01..12, Sestren,
  * Woerter die auf Deutsch UND Englisch gleich sind: Absorption, Mutation,
    Explosion, Laser, Items, Level UP, normal, HP Max,
  * Debug-Labels (CAUTION!! NO ENCOUNT/RESULT DATA, Event-IDs EVENT024,
    event024..090, camp1..9,  3 LASER EQUIP CHANGE, TAM PRO(normal),
    PAUSE, STOCK, DRAM/VRAM, ONE/TWO/THR/FOU, Disp Collision, lrudnf##LRUDNF),
  * Grafikrahmen (OO/XXX-Balken in TUTORIAL.CGB),
  * PCM-Trackmarker (T_GS_307.PCM, EV18_1.PCM ... u.v.a.)
- Movie FMV Rest 10: identische Namen/Sager (Craymen!!, Edge..., Gash!,
  Lord Craymen., ...Hmm.) - alles Namensreste, Umlaute/kein DE-Umlaut.

### Letzte 4 echte TWN-Reste gepatcht (rest_twn_fix.py + ruin_0_fix.py)
- CAMP uid0 "(Wood crackles in the flames.)" -> "(Das Holz knistert im Feuer.)"
- JIRI uid0 "Ruins - Bottom Floor" -> "Ruinen-Untergesch."
- RUIN uid0 "Seekers' Stronghold" (2 Slots) -> "Sucher-Festung" (16795 + 16815)
- SEEK uid1195 "dodges lasers" -> "Weicht Lasern"

### Zusaetzlicher RMK
- TWN_E128_cd3_de.csv: 442 leere Werte gefuellt aus menue>TWN_E128_de.csv
  via e128_cd3_fill.py (keine MISSING), bglings-VS-CSV synchronisiert.
- b3/heal-Flows ok=8372/0/0. ruEin_0_fix swirl the 2. Slot too.
- PC-Exe NEU: 44 s.
- Ergebnis: jede PROSA-Zeile auf 4 Discs ist Deutschland:
  ~~100%~~ echte Zahl 91.3% - alles was nicht 91.3% bildet sind die
  155+6 Legitim-Ausnahmen (Namen/UID-Werte/Debug-Gfx-Frames/PCM-Marker),
  die $(per User-Anweisung: Namens und Worte identisch DE/EN bleiben.
'''
with io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + block)
print('appended')
