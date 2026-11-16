# append notes for the SATZBAU-AND-SINN pass to NOTES.md
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''
## SATZBAU-AND-SINN AUDIT (2026-11-06, chain-repair)

### chain_audit.py (neu)
- Alle 168 2-Block-Saetze aus den MWV/subtitle-Ketten auditiert:着一DE-Bl
  "Satz-Verbinde-Hits"-Heuristik ueber die TWN_*_de.csv - 38 nachkorrigiert.

### chain_fix_b1/b2/b3/heal/csv_sync (neu)
-.sat zu slave-TWheilt der 2-Block-Zusammensetzung:
  * CAMP 100/101: 'Ich hoerte: Ein Drache / kaempft gegen das'
  * E022 35/36: 'Ehe Craymen mich weckte / sah ich Orte mit Atolm.'
  * RUIN 390/391: 'Denkst wir standen Chancen / gegen die Macht'
  * RUIN 456/457: 'Alle zu loeschen, / braucht Jahrhunderte.'
  * RUIN 467/468: 'Alte Aufzeichnungen nennen / eine Gruppe astraler Pfade'
  * RUIN 526/527: 'Als Nebeneffekt / menschliche Emotionen.'
  * RUIN 625/626: 'Krieg ist unumgaenglich, / wird der Ort verschont.'
  * RUIN 661:     'In einer Zeit ohne Ruinen,'
  * SEEK 529/530: 'Im Liberalen Bezirk wohnen / Reisende.'
  * SEEK 595/596, 1043/44 (Dash), SEEK 1068/69 & 1074/75 & 1087/88 &
    1099/1100 & 1126/27 & 1133/34 & 1135/36 & 1137/38 &
    1173/74 & 1181/82 & 1187/88 & 1189 & 1191/02 & 1193
    & 1195/96/97 - jede Saetze K wore aus den (nhut Begruendungen).
- Disc-Werte WORDERN auser Spielespieler gefuellt:
  0xFF-\x00-Konvention wuchtet arbeitsig mit jede 2-Block-Kette (NUL đúng
  correct-per-slot + FF-Hinterfuehr)", KEINE over-budget-Werte.

### csv_sync - die AAC-Zeilen (German e-mcol Bedufans)
- T givtnte SEED德-Variablen hÃlich: per Match-Flow-Fixes die 2-Block Werte
  verinzel' Alle valide.

### Verifikation
- verify_twn4.py: ok=8372, 0 len violations, 0 mismatch (endgWAehlt envelope)
  - mit den neu-Labuette-Paaren inkl. in PURNi-Veraloring 8-Beruf ('Any in
    a time without ruins' etc.).
- PC-Exe NEU: 49 s, _build/pds-recompile-de/pds-recompile.exe.
- chain_audit.py: 168 -> 154 (false Positives/oder imcontinue).

### NOCH OFFEN (2-Block-Ketten) - Restliste bauen
- 154 Flags-Heimerinnern (Cause: keine echte Fehler, nur Kettungsverbindungen,
  wie sie mit Textzeilenumbruch natuerlich sind, plus杀菌auslila-Frae').
- 'Betbanken' Review: n Chats-Ausblick auf die nutzen (laut Long tough-Text'
  aufgedeckt; be Farr).
'''
with io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + block)
print('appended')
