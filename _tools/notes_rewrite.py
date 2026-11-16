# replace the (mojibake-afflicted) appendix of NOTES.md with a clean ASCII version
import io
txt = io.open('_project/NOTES.md', encoding='utf-8', errors='replace').read()
marker = '## ABSCHLUSS-QUALITAETSPASS (2026-11-06)'
i = txt.find(marker)
if i < 0:
    raise SystemExit('marker not found')
clean = '''## ABSCHLUSS-QUALITAETSPASS (2026-11-06)

### 1) TWN-Reconcile (E022/JIRI/CAMP/RUIN, alle 4 Discs)
- patch_shift_fixes.py ist VERALTET; idempotent-prefix ist jetzt reconcile2.py
  (FORCE-Liste + Disc-autoritatives CSV-Sync).
- WICHTIG (Bug-Historie): nach jedem write_file_regions MUSS der im RAM
  gehaltene Datei-Cache neu gelesen werden, sonst ueberschreiben Folge-Patches
  desselben Blocks fruehere Writes (Bug 1 in reconcile_pass2 reproziert:
  uid99 wurde zimmlich auf d2-d4 doppelt geschrieben).
- Endstand verify_twn4.py: ok=8372, len violations=0, mismatch=0.
  Die NO-CLOSE-Hinweise sind legitime Satzuebertraege (keine Fehler).
- Alle 4 TWN-CSVs sind jetzt byte-genau synchron zu den Discs.

### 2) BTL_* FNT (B5/C2/C52/T0/X0, alle 4 Discs)
- BTL_REST_map.csv komplett repariert: 94 Ersetzungen (Budget pflichtig),
  Mojibake behoben (gel??hmt -> gelaehmt, ??berhitzt -> ueberhitzt; Grundeinheit
  Literal-\\n-Sequenzen), Doppel-Felder kollabiert, "SHOT  Power" nachgetragen,
  6 Erklaerbloecke mit Zeilenbreite <= EN-Breite neu umbrochen (btl_line_fix.py).
- Endstand: 0 Zeilen ueber Budget, 0 Nicht-ASCII-Broken.
- Alle 5 BTL_*_FNT_map.csv sind Copies von BTL_REST_map (Konsistenz).
- Patches: applied gesamt 472, readback-mismatch=0 auf allen 4 Discs.
- Bewusst EN bleiben: CAUTION/COMBO/P-%s/time/EXP tier Debug-Zeilen, HP Max,
  Laser (identisch).

### 3) CHILDMP_MCB (alle 4 Discs)
- 12 Fixes (DRAGON * WING -> DRACH* GR., Aronak/Lindstrum Einheit, RUN->FLI,
  Golia-Schwanz, Not Use -> Unben.) via childmp_fix.py; validate 0;
  applied 229-235 je Disc, readback 0.
- Rest-EN = Debug/Unit/Scene-Labels (D Unit 01..12, camp1..9, event024..090,
  !Hp/!hp/!mp, TAM PRO (normal), (HIT), HP Max) - bewusst.

### 4) FLD_* (A5/A3/B6/C4_6 MCB + A7/B2/B5/C2/C4/D2/D3/D5 FNT, alle 4 Discs)
- FLD_A5_MCB: Rallye-Slide-Frames ('Rolling Start!'-Stufen -> 'Los gehts!'
  und 'Auf den Rekord!!'-Suffixe) sind BY DESIGN der Animations-Frames
  (Typewriter-Reveal), KEINE zu kurzen Uebersetzungen. Zusatz-Fixes:
  'ALL LOAD !' -> 'ALLE LADEN', 'X: dragon camera' -> 'X: Drachenkamera';
  gepatcht (applied 19/Disc, readback 0).
- FLD_A7_FNT_map (FNT-Union): 12 Fixes (PAL-WECHS., WART, ALLE LADEN,
  A:LADEN B:NICHT C:ALLES, SPEICH., FREI, REKORDE LOESCHEN, ZUG, KEINE!!,
  LEER, SPIEL NEUSTART, X: Drachenkamera). 'MAP'->'KARTE' scheiterte am
  Budget (3 < 5) und bleibt EN. Applied 5-17 je Dateinamen, readback 0.
- FLD_C4_6_MCB: 'So...' -> 'Also' (4-byte), '  No Entry' -> '  Verboten'
  (10-byte); "Tja..." passt nicht (6 Bytes); applied 37/Disc.
- FLD B6/C4_6/A3: light/light  :/ambient/air/ccp/scr/WHO/FREE CAM/SHADE VEC/
  FLD ERROR !/no/yes = Kamera-Debug-UI - absichtlich EN.

### 5) TWN-Kleinmaps (Shop/Rest + Quiz-Antworten)
- Grenz-Ergebnis: '(This lamp looks valuable.' -> '(Die Lampe wirkt wertvoll.'
  (26 = 26); 'back' -> 'Heck' (Quiz), plus neue Lathum-Quiz-Optionen im
  TWN_SEEK.PRG: front->vorn (off 181079), back->Heck (181085),
  sides->Seit. (181090) - auf Disc 1-4 byte-verifiziert
  ('Gegen Baldor, wo ist es sicher?' + vorn/Heck/Seit.).
- TWN_SEEK_PRG d4-map: 18 ueberkurzte Zeilen lesbar neu formuliert
  (seek_d4_short_fix.py, expand + validate + patch, alle sauber).
- Konvention: expand_menu_map.py TWN_SEEK_PRG _work/menu_de/TWN_SEEK_PRG_d4_map.csv
  = macht BEIDE Ausgaben (_de.csv und _de_d4.csv) aus derselben (grossen)
  Map; die kleine TWN_SEEK_PRG_map.csv (3 Disc-1-Autofixe) NICHT mehr
  verwenden (ausgeschrieben in Doku). Die d4-Map (811 ez-Zeilen) ist die
  Master-Quelle; die 3 off-1810xx-Optionen sind dort prasent.

### 6) TWN_E128 (Zoah-Bezirke, nur CD3)
- Befund:-_work/subtitles/TWN_E128_cd3_en.csv (108 Rows) ist UNBRAUCHBAR:
  die 3xxx-Offsets sind E022-Kopien und existieren in TWN_E128.PRG NICHT
  (die Region ist dort binary); die echten Strings stehen in der
  451-Row-Tabelle _work/subtitles/TWN_E128_cd3_de.csv (uid;len;off;copies;en;de).
- _tools/e128_build2.py: Fuellt leeres de aus der verify-en-valide EN-Pool
  (alle TWN_*_de.csv + TWN_*_map.csv) + FIX-Overrides
  (Town of Zoah->Stadt Zoah, Holy District->Heil. Bezirk, Leave Town->Raus hier,
  It is dark...->(Dunkel dort oben...), Enter->Rein, Stay->Wart,
  Stay Out->Draussen, Leave->Raus, Wait/Until Nightfall->Warte bis zum Abend,
  Wait Until Morning->Warte bis Morgen, Exit->Ende, Buy Item->Kaufen,
  Sell Item->Verkauf, FREE->FREI, front->vorn, back->Heck, sides->Seit.,
  Don't Exit->Bleib hier, ruins.->Ruinen, Ragdam->Radgam);
  Vaiman... bleibt Name. Binaries/Debug significants bleiben.
- Output: _work/menu_de/TWN_E128_de.csv (696 Rows inkl. copies) + _en.csv;
  validate 0 problems; Patch applied=692, skip=4 (2 Rows 'Go to the Liberalen
  Bezirk' auf Disc besser als 'Geh zum Liberalen Bezirk' -> bleibt), readback 0.
- Disc-Verifikation: 694/696 Rows am offset == de; keine EN-Reste
  (Town of Zoah / Holy District / Wait Until Nightfall = 0 Treffer in der Datei).

### 7) TUTORIAL.CGB (alle 4 Discs) - DATENRETTUNG!
- expand_menu_map.py TUTORIAL_CGB UEBERSCHRIEB die 612-Row-_de.csv auf 1 Row
  (die _en.csv enthielt nur 1 Row). RETTUNG ueber das Patch-Muster:
  extract_menu_full.py liest TUTORIAL.CGB aus Original_CD1 (sauber EN,
  keine TODO-Filterlung -> 838 Rows, 595 unique) und tutorial_rebuild.py
  liest pro offset den DEUTSCHEN Text vom GEPATCHTEN DISC1 (Disc = Backup!)
  und baut die _de.csv vollstaendig neu.
- 838 Rows, validate 0, alles auf allen 4 Discs idempotent gepatcht
  (applied 136-230, readback 0 in allen Runden).
- Danach Qualitaetspass (tutorial_de_pass.py + final2): 85+ echte Dialog-
  Fragmente (bislang EN-Duplikate der Extraktion, 207/222 REVIEW-Flags)
  ueber bislang ungeputzte EN-Uebersetzungen getauscht. Beispiele:
  %a1 erholt sich... / Rueber kommst du nie allein /
  Danke! Loehne dir... / Nimm. Verdient hast du es. /
  Lichtjemmirte Meldungen (Wurmgaenge, unterirdische / Wasserweg...
  / Wie dem sei: suchen wir / einen Untergrundweg.) /
  So manche / Man glaubt, / gottgleiche Macht hatten. /
  auf uns warteten. / auch Kriege, / Tja, / ...Tod? / zu schuetzen. /
  Ich kam nicht an Uru. / Siegel? / Gute Nachricht! / Entsch. /
  Zerstoert man Mel-Kava, / irgendwo in Zoah. / Das ist ein Schatz, oder? /
  (Wirkt zufrieden.) / (Azel ist bewusstlos.) / (Da ist etwas nahe Azel.) /
  (Azel ist noch bewusstlos.) / Ihm vertrauen. / Ja, ich weiss... /
  zu Craymen... / Du bist anders. / Du bist wie ein Anderer. /
  wirktest manchmal leblos. / Schon klar. Du verstehst / Meine Denkmuster /
  Ich fuehlte fremd. / Sogar mit Gewalt. / vor Stunden. / Halt /
  Zur Sucher-Festung / (Erzeugt es Hologramme?) / (Gestolpert... /
  er geht kaum, oder?) / (Wie ein mutierter Coolia...) /
  (Er hasst mich wohl...) / Beruh./Ignor./Tadel/Blick/Lach/Sauer/Str /
  (Muede? / Muessen beim Kaempfen aufholen.) /
  (Ich mache ihn wohl nervoes.) / (Heute wirkt er gesund.) /
  (Huch? Verletzt ihn?) / Hab ich Unrecht gesagt? etc.
- 3 Kettenebene-Retone (force=1): 'Verdammt, was sag ich' + 'denn ihm?',
  '(Wollte er wirklich' + 'sich den Drachen ansehn?)',
  'Wenn ich synchron bin, kann' + 'ich sagen, was der Turm tut.'
- Bewusst EN (Namen/Interjektionen identisch + Grafik): Gash... / Edge! /
  Mel-Kava? / (Paet! / Oh... / Hmm... (2x), plus O/X-Balkengrafik-Frames
  (off 86144..) und %cN!SEGASEGA!%c0-Frames sowie die kompletten Debug-
  Labels ab 126496 (5LE, Cnfdns, cfd/exp, fff, DDD, Lcs:, Res:, pos:, ang:,
  DRAM:%6x, DIV:, VRAM:%6x, ONE/TWO/THR/FOU/LOW/STD/LNG/SKY/DRV/LCS, PAUSE,
  Disp Collision, Clip Mdl, Shade, ShadeVec, PointLight, Camera1-3, NpcPos,
  STOCK).

### 8) Finale Backlog-Bilanz (collect_backlog.py)
- de-Level: 0 Ueber-Budget, 0 Nicht-ASCII. Rest-EN nur mit Begruendung:
  * MENUEN_FNT: 'Laser' (identisches Wort), 'Items' (Gaengiger Begriff),
    'Light Wing' (Name, 12 > 10) - bewusst.
  * TUTORIAL: 22 (siehe 7).
  * CHILDMP/FLD: Debug/Kamera-UI (siehe 3/4).
  * BTL_REST: 'HP Max', 'Laser' identisch; 'Schusskraft' ist factor-Correct.
- Das map-Level shows grosse UNTR-Zahlen (FLD_*_FNT_map 39 je, BTL-Maps...):
  Rausch-Filter - Ketten von map-Duplikaten und Reveal-Debug-Formaten ohne
  Disc-Konsumenten, und die 'SHORT/UNTR'-Def in collect_backlog zaehlen
  die bewusst-EN-Label mit.
- review_full.py Endstand: allein heuristische Flags (NO_END_PUNCT,
  NEG_LOST, VERB_START etc.) bei Satzuebertraegen, Interjektionen und
  Debug-Strings - sorgfaeltig als FALSE POSITIVES dokumentiert; echte
  TRUNC_DOUBLE-Faelle sind 0 (alle repariert in vorherigen Sessions oder
  in diesem Pass).

### 9) PC-Exe neu
- pds-recompile-builder --disc _work/patched_disc1..4.cue --out _build/pds-recompile-de
  (Build 53 s; bpasad). Erstellt pds-recompile.exe neu mit den Patches von
  diesem PASS; Kostet: NICHT weitergeben (enthaelt uebersetzten Spielcode).

### Kern-Lektionen (fuer zukuenftige Sessions)
1) Disc-Text ist autoritativ & die Disc ist die BESTE Sicherung der alten
   _de.csv-Zustaede: wenn expand ein *_de.csv verkleinert, erst rebuild aus
   dem gepatchten Disc (tutorial_rebuild.py als Pattern) - NICHT ohne
   weiteres expandierer die 451-Row-*_en.csv mit 'irgendeiner' Map
   ueberschreiben (TWN_SEEK-Praxis, TUTORIAL-Praxis).
2) menu_text_tool --patch matched EN@off und skipt bei bereits-DE; force=1
   nur fuer echte Retone; Budget-Checks laufen beim Patch trotzdem strak.
3) PowerShell `>` schreibt UTF-16 fuer Python-Einlesenaus; wenn Scan-Datei
   fuer Python benoetigt: per Python mit encoding='latin1' + newline='\n'
   schreiben.
4) el PDF-Namen nicht weitergeben; Alle Workes duegend (Notes/Scripts) sind
   eine Session-fertige Werkzeugkette.
'''
out = txt[:i] + clean
io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n').write(out)
print('rewritten, new length', len(out))
