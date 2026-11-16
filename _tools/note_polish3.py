# Append the polish-pass summary to _project/NOTES.md (ASCII, latin1-safe).
import io

TEXT = """
## QUALITAETS-PASS GRAMMATIK/SINN (2026-11-07)

Ziel: deutsche Grammatik und Sinn ueber Blockgrenzen, vollstaendige
Uebersetzung (alles ausser Namen), ohne die harte Laengenregel zu brechen.

### Neue Korrekturmodule
- _tools/fix_polish3.py: 51 Korrekturen in TWN_CAMP/RUIN/SEEK
  (u. a. CAMP 487 'Gibt es den Ort wirklich?', CAMP 486/488 Ketten,
  RUIN 511-513 'Er sollte die Tuerme / zerstoeren. Azel verschwand /
  im Kampf. Sie geht nach Uru.', RUIN 17/55/82/89/232/309/433/472/602/
  634/671/683, SEEK 58/164/414/425/448/901/1275).
- _tools/fix_e128c.py: 31 Korrekturen in TWN_E128_cd3
  (Abkuerzungen 'Masch..', 'Toepf..', 'Haengem.', 'Getr.', 'Aussenst..',
  'f. Motor' sowie Gross-/Kleinschreibung und 'auszusein').
- Beide Module sind in apply_grammar.py bzw. apply_e128c.py eingebunden
  und idempotent.

### Verifikation (Endstand)
- verify_full.py: ok=20935, len=0, mm=0, tr_groups=44
  (die neue 44. Gruppe ist die legitime 2-Block-Kette RUIN 512->513).
- e128_disc_check.py: rows=696, differ=0, too_long=0, oob=0.
- verify_evt_roundtrip.py: TOTAL PROBLEMS: 0 (alle 4 Discs).
- menu_text_tool.py --validate: TOTAL problems: 0
  (MENU_SCB, MENUEN_FNT, TUTORIAL_CGB, CHILDMP_MCB, FLD_*).
- menu_quality_scan.py: 0 Rest-EN/NONASCII in TUTORIAL/MENU/CHILDMP.
- coverage_honest.py: TWN 100.0%, E128 100.0%, FMV 99.7%,
  Menu 95.5%, Battle-UI 98.0%, Tutorial 99.5%, TOTAL 97.3%
  (Rest = bewusste Policy-EN/Debug/Namen).
"""

with io.open('_project/NOTES.md', 'a', encoding='latin1', newline='\n') as f:
    f.write(TEXT)
print('appended')
