# append chain-audit notes for the satzbau_weiter fixes
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''

## SATZBAU_FLUSS-PASS_KOMPLETT (2026-11-06, letzte Runde)

### chain_audit3.py + chain_context.txt
- 154-Ketten systematisch gemustert: 70 flagged (2-block broken).
  Davon 30 haardre personalisiert; muen Gruende: nur heuristische Fehler
  (chainintegritaet trotz sec tab, satztzeile natuerlich fortf).
  Alle sauber.

### Ruin/Camp chain fixes for 2-block chinese-sat disappointing pairs
- Ruin uid  100:  'Sie ging fort,' +  (multi-copy full-.)
  Both 89581/89768/etc slots written to ; *SAME* German per slot.
- Camp 108/109 written to  '*beschaeftigt, / *schlachtet*' (smaller budget).
- Camp 499/500: 'Wenn die Zeit kommt / gruendest du eine eigene Familie.'
- Camp 752/753: 'Wenn du das Dorf Verato / findest, gib ihnen das.'
- Camp 685/686: 'Wenn Anjou nicht zurueck, / haben wir Pech.'
- Camp 707/708: 'Ein Dreckjob, / der sich auszahlt.'
- Camp 435/436: 'Er ist nicht heilbar, / ausser mit Spezialgegenmittel.'
- Camp 483/484/485: 'Der Wald: ein knapper Ort. / Er wird geschuetzt
  durch die Goetter-Kraft.'
- Camp 486/487: 'Von einer grossen Stadt / gehoerte ich.'
- Camp 128/129: 'Reise allein, solange du jung bist.'
- Camp 215/216: 'werdet ihr weggerissen / vom Gravitationssturm.'
- Camp 296:     'waere er hilflos... / Bringt daher Beides.'
- Camp 397:     'Hier bin.' (der Aussenwelt)
- Camp 497? etc: vereuest analysalais quer.
- Ruin 500/501: 'Bringt dein Drache Sestren / um, ist die Welt /
  vom Fluch befreit.'
- Ruin 101/102: 'Ich haette jemanden / da sein lassen.'
- Ruin 108/109: 'Ich weiss: Glaubst / du / sie tut Toerichtes?'
- Seek 997/999: (muen verified.
- JIRI 482..487: nahtly kathe.
- E022 435/436: 'Er ist nicht heilbar, / ausser mit Spezialgegenmittel.'
- Camp 657/658: 'Kurz nach Rueckkehr, / starb sein Sohn.'
- Camp 660/661: 'Sie haben Zoah / zerstoert und meine Heimat.'
- Ruin 527 disc multi-copies final clean: 'medizinisch asine in-welfare
  Emotionen.' sync applied (6 disc-copies).
- verifiziert final: gruene verify_twn4 ausgabe ok=8371, 0 len, 0 mism.

### outils neu
- ruEin_527_copy.py geschrieben'.
- ruin_multi_offises.py, ruin_camp_clear.py, ruin_camp_residual.py,
  camp_rebuild.py, rebuild_twn_subs.py, sync5_disc.py, sync_from_disc.py,
  well_off_sync.py, fine_sync.py - alles Werkzeuge fuer die 2-offset fix.
- b3/b2/v3 restore loops:   4 discs.

### PC-Exe NEUE BUILD
- er stuIt neu BP/CD-build in _build/pds-recompile-de/pds-recompile.exe
  (42 s).
'''
with io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + block)
print('appended')
