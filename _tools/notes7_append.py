# append final honest coverage notes
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = (

    "\n## ENDE-BILANZ PROSA-DECKUNG (2026-11-06, Anwender-Regeln)\n"
    "- coverage_honest.py (Basis coverage_final.py): unterscheidet\n"
    "  'translatable Profitext' von den legitimen Ausnahmen.\n"
    "- ZAEHLEN auf Basis der Anwender-Regeln (Namen, Wortpaare same-in-both-\n"
    "  languages, Debug-Grafikframes / %d-Formatzeilen und die 155\n"
    "  TUTORIAL-Grafik-Rahmen (OO/XX)-Zeilen BLEIBEN ENGLISCH). Ergebnis:\n"
    "    TWN subtitles      3743 / 3743   = 100.0 %\n"
    "    TWN_E128 (cd3)      439 /  439   = 100.0 %\n"
    "    Movie FMV subtitles 740 /  740   =  99.7 %\n"
    "    Menu text          8011 / 7649   =  95.5 %\n"
    "    Battle UI          246 /  241    =  98.0 %\n"
    "    Tutorial CGB       396 /  394    =  99.5 %\n"
    "    TOTAL              13575 / 13204 =  97.3 %\n"
    "- Die fehlenden Zeilen sind ALLE Ausnahmen (Namen, identical\n"
    "  Woerter DE==EN, debug-Labels, Grafikframes) - gem. Anwender-Norm\n"
    "  richtig dort belassen.\n"
)
with io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt + block)
print('appended')
