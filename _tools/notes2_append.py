# append session notes for the CD1/intro pass to NOTES.md
import io
with io.open('_project/NOTES.md', encoding='utf-8', newline='\n') as f:
    txt = f.read()
block = '''
## CD1/INTRO-QUALITAETSPASS (2026-11-06, zweite Runde)

### FMV-Untertitel (MOVIE.DAT, alle 4 Discs)
- Beschwerde "Intro-Text stimmt nicht / Saetze in 2 Bloecken falsch" ->	Komplettpass:
  Alle 47 MOVIE.DAT-Gruppen g0..g46 auf CD1 reviewt, 2-Block-Ketten neu
  zusammengesetzt (je 4-6 Bloecke der Einleitungsschlagzeilen g1 inkl.
  "Erfahrungsgemaess, / je weniger du vom Reich / weisst, desto besser gehts.",
  "Wer zu viele Fragen stellt, / stirbt bald.", die Vorzeit-Narration
  'Das Reich stieg zur Macht / mit der Technik aus der / untergegangenen Zeit.'),
  6 vermeintlich korrupte Slots waren Dump-Artefakte (evt_offsets_json
  'off' != Sector-View des Patcher-Tools) - energy-Check via
  evt_state_dump2.py (lba-based) - Disc war in sich integer,
  trotzdem ~205 Zeilen stilistisch bessert.
- evt_de_map.csv: 815 unique EN keys, 825 Rows je Disc gepatcht (applied=825,
  readback 0). 12 bewusst-EN: Craymen/Gash/Edge/...Hmm/'%a0'-Namen + Ellipsen.
- Extremsprachprobleme im Intro gel oest:===== 'Not much... at all.'
  'Nach Erfahrung' / 'Zu viele Fragen, bringt nur den Tod.' /
  'Nein. Loomleber...' - jetzt durchgaengig deinen deutschen Kontext.

### FMV-Caption-Dateien (neu entdeckt: MERUKABA.MCB = intro-captions)
- MERUKABA.MCB (27856 bytes, = MOVIE.DAT-Clone im MCB-Container) haelt die
  Intro-Untertitel-Kopie: 'back now.' -> 'Sofort.' gepatcht (applied=1/Disc).
- Die kleinen EN-Fragmente ('e', 'rl.', 'd Fleet', 'rt!', ',er?') sind
  Nachbar-Slots bereits-gedeutscher Saetze - bewusst unveraendert.

### In-Game-UI-Labels (neu eingefuehrt)
- '  YES   NO' (CHILDMP.MCB-Kontextfenster) -> 'JA    NEIN' (applied=1/Disc).
- '(Imperial piece ofcrap.)' (FLD_A3) -> '(Kaiserlicher Mist!)'.
- 6 Passage-Strings aus FLD_B6 (Light-Wing-Report: Institute/regarding/
  mentioned/seal/continent/more-than) -> DT-Bloecke (<Das Institut, das
  ueberlegte> / <zu den Lichtfluegeln...> / ...).
- MENU.SCB Turm-Wegweiser 2 Texte (upper/outer 13F -> 12F -> oberer Hangar;
  middle 8F -> 6F -> unterer Hangar) in Deutsch umgebaut (ZEILENBRUCH-basiert,
  Kamera-Zeilenbreite = EN-Breite).

### BATTLE-UI (VOLLSTUENDIG!) - endlich die in-Kaempfe sichtbaren Texte:
- Batch 1: 246 Livedisc-Strings (live_english_scan/btl_live_en) reviews ->
  169 unique + Feedback; fix-batch (btl_ext_de2.py) + ~120 Monster-/Angriffs/
  Status-Labels (btl_ext_de3.py) + 5 Debug-Prefixed (btl_ext_de4.py):
  saemtliche BTL_*.FNT-Battle-Files u. BTL_*_2.PRG files (a-b-c-d-Reihe +
  'A5_2','B5_2','A5_FNT etc.) JETZT instrinsisch DEUTSCH:
  - ATTACK/DEFENSE/SPIRITUAL/AGILITY/FULL-GAUGE CLASS -> KAMPF/ABWEHR/
    GEISTER/WENDIG/VOLLLADE-KLASSE.
  - Attack with Gun/Homing Laser -> Angr. mit Waffe/Homing-Laser.
  - Level UP -> STUFE +1 (disk-wide, alle 25 BTL-Files).
  - Boss/debug-label Bomb regen/Charisma-Fusion 'Fus. Mel-Kava' u. Stretch-
    Formen (Wanderform/Abwehrform/Endform) inkl. 'Baldor-Queen'.
- Endstand Livedisc: EN-like 246 -> 5 (3 davon Binary/Debug-Artefakte,
  1 deutscher False-Positive 'Es will Rache.').
- Battle-Chatter C22 (Raketen-Launch), C5 (Flotte), C82 (Exterminator),
  C8 (Skiff), A72 (Homing-Mines) etc. komplett deutsch:
  Rails oben: Start klar. / Boosters gev beruht. / Stabilisator loesen /
  Zielflugphase / Gefechtskopf an! / Deton. / 5 Min. bis zur Detonation.

### Buy-/Sell-Item-Labels in TWN-PRGs
- TWN_E022/CAMP/JIRI/RUIN: 'Buy Item'->'Kaufen', 'Sell Item'->'Verkauf'
  (applied 2 je Disc; E022 only disc1).

### Rest-Bestand (freiwuest EN, dokumentiert)
- FLD_A5/D2 'PRESS ENTER ==> REC/PLAY' + 'A:LOAD...' = VMS-Recorder-Debug.
- FLD_C4_6 'OFF WAIT %3d' = Debug; FLD_C2 'free run %1d'/'score rank' = Debug.
- FLD_B5 '...Defense System'-Typewriter-Frames = unsichtbar/by design.
- BTL: CAUTION!! NO ENCOUNT/RESULT DATA!!, LASER TYPE=MULTI/SINGLE, die
  Binaerframes \x90_-Banner = Debug/Gfx-Frames.

### Tools (neu)
- evt_state_dump.py/dump2.py (Patcher-View-Kopie; dump1 mit JSON-'off' ist
  MISAUS-gefiltert, nicht verwenden.)
- evt_intro_fix.py/2/3/4/5 - der FMV-Intro-Ketten-Fixes (evt_de_map).
- live_english_scan.py/btl_live_ratio.py - Livedisc-EN-//Dir-Werkzeug mit
  EN-Wordlist-Treffer; moeglich fuer 'wie viel ist noch übrig'.
- slots_probe.py, live_en_rows.py, menu_scb_z2.py, merukaba_z2.py (MCB-EXE),
  extract_menu_full.py (alle Strings ohne TODO-FILTER, Original-Disc)
  + extract_menu_strings.py bleibt TODO-FILTER-Variante.
- btl_ext_de2/3/4.py - 362+280+28 Rows-Makierung (de2/de2b/de2c csv-Nomen-
  Konvention 'BTL_<X>_de.csv'');
- final_sweep.py - 'Level UP/Buy/Sell' Shared-Labels 26 Files (34 rows).
- Alle neuen Label-Zeilen landen in '*_de2.csv'-Typen (deploy-plain) -
  expand_menu_map UND PATCH-Flow koengineering kooperativ, rows[0] bestimmt fsname.

### Verifikation
- verify_twn4.py: ok=8372, 0 len violations, 0 mismatch (unveraendert OK).
- patch_evt_subtitles --disc all: applied=825, no-de=0, too-long=0, mism=0.
- Alle BTL/CHILDMP/FLD/TUTORIAL/MENUEN/MENU_SCB validates: 0 Budget-Problems.
- btl_live_ratio.py: EN-like 5 (vs 246 davor).
- PC-Exe NEU: 51 s, _build/pds-recompile-de/pds-recompile.exe (nicht weitergeben).
'''
out = txt + block
io.open('_project/NOTES.md', 'w', encoding='utf-8', newline='\n').write(out)
print('notes appended, new len', len(out))
