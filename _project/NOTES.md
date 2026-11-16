# Projekt-Notizen (Automatisch generiert) – PDS Deutsch

## Disc-Regionen (verifiziert)

### PAL-EU Originale (Ihre Kopie, `Original_CD1..4`, .cue/.bin 2352)
| Disc | Track-1-Sektoren | System-Volume |
|------|------------------|---------------|
| CD1 | 274.450 | `AZEL_1` … `MK-81307` … `CD-1/4` |
| CD2 | 237.823 | (analog CD-2/4) |
| CD3 | 268.815 | |
| CD4 | 247.732 | |

### Original (spanische) Patch-Basis (aus der weltweiten „temporal.file"-Cue-Datei)
| Disc | Data-Track endet bei LBA | → Patch-Größe vs. EU |
|------|--------------------------|----------------------|
| CD1 | MSF 61:09:15 ≈ LBA 274.890+150 | +440 Sektoren LÄNGER als EU |
| CD2 | MSF 53:00:63 ≈ LBA 238.413+150 | +590 Sektoren |
| CD3 | MSF 59:54:05 ≈ LBA 269.405+150 | +590 Sektoren |
| CD4 | MSF 55:12:72 ≈ LBA 248.322+150 | +590 Sektoren |

**Konsequenz: Der spanische Patch (V0.89, segasaturno/Holy_3051) ist für die
NTSC‑US-Discs gebaut.** Er passt nicht auf PAL‑EU-Discs (LBA-Logik verletzt).
→ Wir bauen das Deutsche **direkt auf EU-Basis** und entnümmern nur die
spanische Sprache + Konzepte aus den Patchdaten.

## EU-Disc-Struktur (CD1 zerlegt)

### Saturn „System"-Layout
- LBA 0: `SEGA SEGASATURN SEGA ENTERPRISES MK-81307 V1.000 19980309 CD-1/4`
- LBA ~15–16: Bereicherungs-Disc-ID (kein klassisches ISO `CD001` —
  Sega „trickreiches" Layout, aus ISO-PVD entnommen)
- **On-Disc-Dateiverzeichnis @ LBA ~20** (offset ≈ 0xb835):努力学习 BBB 'Sega-FS'

### Sega-FS-Eintrag (Record Format, live entschlüsselt)
```
14-Byte-Header: 62 01 1d 00 00 00 24 01 00 00 01 00 00 01
1 B   nameLen (=Länge des Namens *ohne* ';1')
nameLen B  Aussprache-Namen (ASCII: "1ST_READ.PRG", "A3BGM.BIN" …)
1 B   0x00               (Terminator)
2 B  _u16 record_len    (42/44/46 —‧‧‧‧‧- dazu: dword/positionsdaten)
8 B   u32LE + u32BE MIRROR   (LBA des Inhalts)
8 B   u32LE + u32BE MIRROR   (Größe in Bytes)
 alle Fotos vom Muster: ''1ST_READ.PRG → LBA 0x3C3F7, size 0x2D582''
```
Die Namensteile wie `A3xyz.PRG/SEQ/BIN/MCB/CGB/E…` stecken aPC–konform in der
Disk. (**Achtung:** im spanischen Rebuild-Container tauchen dieselben Namen
ISO‑artig MIT ';1' auf — dort iso-Style-Listing.)

## Stand der Text-Recherche (Update)

### FALSCH: „EU-Text ist komprimiert“ — EU-Skript-Texte sind KLARTEXT!
Der frühere Negativevidence-Suchlauf (Keyword „WARNING/Save/Speichern“) lief ins
Leere, weil die falschen Wörter gesucht wurden. Tatsächlich liegen in den
Skript-Dateien der EU-Disc **NUL-terminierte ASCII-String-Tables**, wie z. B. in
`BTL_A5.FNT` ab off ~0x5F3F8..0x5F7xx:
- Debug-Strings: `PG VAL:%3d`, `PG MAX:%3d`, `COMBO :%1d,%1d`
  `val:%3d mam:%3d cnt %d lim %d`, `%s p:%d %d f:%08x hp: %d`
- Battle-Case-Namen: `NOMAL`(!), `AT 1 `, `SP 1 `, `ETC1..6`, `DEAD `,
  `P_SPD:%2d.%02d`
- UI-List: 11× `no use` → `Counterattack` → `Display Item List` →
  `Customize Gun` → `Select Dragon Type` → `Attack with Gun` →
  `Attack with Homing Laser` → `???` → `Unusable` →
  `You do not have any item.` …
- Siehe auch `ANTIDRAG.MCB` (Klartext-Treffer) und die vielen
  „Battle-Kommandos“-Treffer (#), die über `BTL_*`-Dateien per dir-LBA
  nachgewiesen wurden.

### File ↔ dir-Mapping
- EU-FS-Records: 357 minus Ungültigelöschte; pro Record: `name + ;1` + u16 recLen
  + gespiegelte u32 LBA/SIZE — LBA×2352 = Datei-Start (Raw), size in Bytes.
- EU-Daten RAW-Samples der Nutzerdaten je 2048 B — Auszugskonvention: LBA n →
  bin[ n*2352 + 16..2064 ].
- EU-Plaintext-Regionen mit Battle-UI-Treffern landen exakt in
  `ANTIDRAG.MCB` &齐心 `BTL_*`-Dateien (jeweils ≈ 1 sz/Table per Datei).

### Spanischer Rebuild (`_work\cd1_0.bin`) — Verifikation bislang
- Das Richau Member0 enthält ein SEHR großes Directory — **1629 Einträge**
  (`0x63E..~0x165AB`) mit Namen ALS `NAME.EXT;1` und (LBA/SIZE) Pair
  (identische Spiegel-U-32-Format). Die alphabetisch sortierte Reihenfolge
  entspricht EU (Name) + ERWEITERTE Liste.
- Die Reihenfolge der Directory-Eintrag-Dateien ist alphabetisch, und die
  Recordlängen variieren (Trennfeld `terminator/recLen` je Eintrag) →
  Parse-Routine muss **generisch** rekursiv nach dem nächsten 62 01 1d 01
  Header vorrücken.
-member0 LBA-Gebäude und Text-Gebiete: die Klartext-Tabelle aus dem ES
  Battle-Bereich (~`0x1d81A0..0x1d84B0`) ÜBERLAPPT die dir-Region bei der
  M-A-Bolisierung nicht mit der ES-dir-Liste — das Exakt-Mapping
  (Payload-Offset in Member0) ist noch NICHT komplett entschlüsselt (Tabelle
  `dir.LBA*2048 = member0 offset` passt für die BTL/CARASC/CAMPS Dateien
  NICHT; die Bekanntestellen wie `BTL_A5.FNT;1` auf ES-Position landen auf
  ZEIGER Auf Kompression-Blöcken (S!S-Format).
- WICHTIG: Im ES-member0 gibt es 26 × die EN-String-Tabelle
  („Customize Gun“, etc) und 29 × die ES-String-Tabelle („Contraataque“,
  „Atacar con el LÉser“, „Es inútil“, „No tienes piezas“ …). Die EN-Repositories
  bleiben in den Spanishen BTL-Dateien als REST (unübersetzte Hinterlegung).
- Battle-Blockgrößen-AHV: die EN- und ES-Tabellen或在 member0
  Wiederholen um ~0x100000-0x110000 (1.05 MB) apart —+
  der ES-Battle-Blob ist d'azur ~x2.5 mal langsamer als der EU (kleiner).

### Wings gesicherter Format-Kern (BTL-A5.FNT)
- Dateikopf: `00 ff ff ff ff ff ff ff ff ff ff 00 57 29 00 01` - danach
  binäre Daten (Neigend deren {bytecode/pointer}.
Vermutung: gleiche Struktur-Sprache wie alle `S!S`-Dateien (PNB/FNT/PNB_BL
Container) — BTL_A3/A5/A… mit dem `wählerisch width` (Data danach etc.)

### Werkzeuge (`_tools\`)

| Script | Zweck |
|--------|-------|
| `inspect_patch.js` | zeigt XDZ-Header |
| `extract_members.js` | entpackt die 2 GZIP-Streams einer Disc |
| `scan_strings.js` | extrahiert die 37k / Dialog Strings als CSV |
| `map_to_orig.js` | Mappt Patchcontent ↔ Original-Disc |
| `saturnfs_v2.js` | vollständiger EU-FS-Parser inclus. File-Auftstellung |
| `extract_eu_file.js` | extrahiert EINE EU-Datei per Name in `_work/` |
| `text_density.js` | Textdichte-Mapping aller EU CD1-Dateien (top 60) |
| `scan_eu_english.js` | EU-Disc plaintext-Hit Scan (Battle-Wörter) |
| `dump_es_fs.js` + `test_seq_payload.js` | ES-member0-FS + Payload-Grenzen |
| `pdftext.ps1` | PDF-Textextraktion |

## Tier-2 (Story/Town-Dialoge) — DURCHBRUCH 2026-11-04

1. **EU-FS-Scan komplettiert:** Gesamtdisc-Scan findet 1.688 Records (Sektoren 20..57).
   Die frühere 639er-Liste war nur die erste Partition, ~1.050 Records
   fehlten (höhere LBAs, zweite Layer: `TWN_*`, `CAMP*`, `ZOAH*`, `A*BGM`.
2. **Keine S!S-Kompression bei Text:** Die "Megablob"-Textzonen liegen
   INNERHALB bekannter Dateien — kein anonymes Blob:
   - Zone 0 (sec 236229..236357) → `TWN_SEEK.PRG`   (File-Off 0x8000..0x44000, 3135 Zeilen)
   - Zone 1 (sec 238405..238533) → `TWN_CAMP.PRG`   (File-Off 0x0..0x1c000,    904 Zeilen)
   - Zone 2 (sec 239429..239557) → `TUTORIAL.CGB`   (File-Off 0x0..,           ~500 Zeilen)
   - Zone 3 (sec 240709..240837) → `TWN_RUIN.PRG`   (File-Off 0x4000..0x1c000, 1128 Zeilen)
   NUL-terminierte Klartextzeilen, tight packed, 5x-Wiederholungen wie Sequenz-
   Kopien (IEEE identisch). Sprachcheck (Wortfrequenz) → nur EN, kein DT/FR/IT/ES.
3. **Tier-1 (Battle) fertig:** 883 Slots in 17 BTL-Files, 0 Kürzung, Dateigrößen
   byte-identisch — Patches liegen in `_work/patched/`.
   Übersetzungen strikt `len(de) <= len(en)` + ASCII-only (Saturn-Font, 0x85-0x91
   ist eigene Kodierung, Umlaute für später).
4. **Sprachregel:** `patch_btl.js` erlaubt nur de+NUL in en+NUL; Übersetzungen
   die 1 Zeichen länger sind als EN werden nicht akzeptiert.
5. **Tier-2 Pipeline (Tier-2-Tests erfolgreich):**
   - `subtitles_export.js` → `_work/subtitles/*_en.csv`
   - `subtitles_template.js` → `*_de.csv` (Spalte `de` leer)
   - `apply_batch.js` → Batch-CSV `uid;de` merge (len+ASCII-Validierung)
   - `subtitles_patch.js` → `_work/patched/<NAME>` (alle Kopien, Größe konstant)
   TOK-Testlauf 2026-11-04: `TWN_CAMP.PRG` batch01: 79 uid (86 Kopien) gepatcht,
   2.169 Bytes modifiziert, alle im Textbereich, Dateigröße bleibt 212.944 B.
6. Offen: Zeilen für `TWN_SEEK` (1916 uid), `TWN_RUIN` (688 uid), `TWN_CAMP`
   (705 uid). Ab hier weitere Batches.

## Nächste Schritte

1. Mehr Tier-2-Batches für `TWN_CAMP.PRG`, `TWN_RUIN.PRG`, `TWN_SEEK.PRG`
2. Textzonen für die anderen PT-Files (`TWN_JIRI.PRG`, `TWN_E022.PRG`,
   `TNAVY*`-Familie, `A*`-Module…) analog Potter analysieren.
3. In-place Disc-Writer: gepatchte Dateien in die EU-Disc-RAW-Datei schreiben.
4. Emulator-Smoketest (Tier 1 + Tier 2 im Original-Cue).
5. Rest der `EVT*.FNT` (komprimiert — andere Textmethode, LZ-Codec-Untersuchung).

## Recht/Referenzen
- EU-Discs und spanisches Material: unterzeichnend nicht-kommerzielle private
  Recherche; ES-Patch von segasaturno.com (Holy_3051).

## Vergleichspanisches Material (Rosetta)

- Spanische Rekonstruktion (`_work\cd1_0.bin` bzw. `cd1_1.bin`, entpackt) enthält
  **denselben Text im Klartext** (mit Spannsystem):
  `{Edge:` Sprecher-Tags, Steuer-Bytes, Zeilenumbruch inkl. `0x0a/0x0d`.
- Zeichensatz-Map (bisher): `0x8a=á 0x8b=é 0x8c=í 0x8d=ó 0x8e=ú 0x8f=ñ`
- Extraktion: `node _tools\scan_strings.js _work\cd1_0.bin` → CSV mit 37.668
  Einträgen (off/len/text) für CD1.

## Patch-Container `%XDZ004%` (Analyse teilweise)

- Magie `%XDZ004%`, u32BE=8, u16BE nameLen1/nameLen2
- Strings `azel_1.bin` (= Eingangs-Cue-Datenname NTSC-US) → `pds-es_1.bin`
- Danach 2 GZIP-Streams (pro Disc), nicht verknüpfte Sektoren.

## Werkzeuge (`_tools\`)

| Script | Zweck |
|--------|-------|
| `inspect_patch.js` | zeigt XDZ-Header |
| `extract_members.js` | entpackt die 2 GZIP-Streams einer Disc |
| `scan_strings.js` | extrahiert die 37k / Dialog Strings als CSV |
| `map_to_orig.js` | nennt Zuordnungen Patchcontent ↔ Original-Disc |
| `saturnfs_parse.js` | (WIP, Scan ^) |
| `pdftext.ps1` | PDF-Textextraktion |

## Roadmap

1. **Deutsche Übersetzung EU-Struktur bauen:** Der EU-Disc Scripts-Datei
   (eine der großen `A3*.PRG`-Dateien, vermutlich) dekomprimieren — als Basis
   nutze den Ausgangspunkt Spanien (dem wir Klartext haben) als Rosetta-Stein.
2. **LZ-Codec implementieren** (Werkzeug `pack.js`/`unpack.js`, Ziel:
 1:1 round-trip  für die EU Archivdaten).
3. **Übersetzung:** CSV ersetzt durch(erst verlassen, dann einbauen)
   Muster: `Original_EN` (DIN?)/ `Spanisch` → `Deutsch`, z. B. in Batches
   L-M; jede Batch: id, kontext, orig.
4. **Re-Insert + Rebuild:** Indices, Größen, Labels anpassen;有限责任公司 Disc
   EU-Layout behalten (nur *innerhalb* der Skript-Datei korrigieren
   und Restaurant-FAT neu berechnen).
5. **Testen im Emulator** (YabaSanshiro/SSF/Saturn):
   Startmarke + Menüs + erste Intro-Sequenzen; nachvollen bis Disc-end.

## Recht/Referenzen
- EU-Discs und spanische Werke: für invalid unokomerziellen Gebrauch.
- primäre artific: segasaturno.com (Spanish translation by Holy_3051).

Fortschritt 2026-11-04 (Abend): TWN_CAMP.PRG 120/784 uids uebersetzt (136 Kopien gepatcht). Pilot-Workflow validiert: 0 Fehler, Dateigroesse konstant.

Fortschritt 2026-11-04 (Abend, 2. Block): BTL-Files neu extrahiert mit korrekten Groessen (BTL_A5.FNT 418316 statt 417792). Re-Patch: 890 Slots, 0 Kuerzungen. Disc-Writeback: 20 Dateien in _work/patched_disc1.bin geschrieben (readback verifiziert), 0 Groessen-Mismatches.

Fortschritt 2026-11-04 (Abend, 3. Block): TWN_CAMP.PRG jetzt 159/784 uids uebersetzt (176 Kopien gepatcht). Disc-Image neu geschrieben (20 Dateien, 0 Mismatches). Emulator-Smoketest kann jetzt mit _work/patched_disc1.cue + patched_disc1.bin durchgefuehrt werden.

Fortschritt 2026-11-04 (Abend, 4. Block): TWN_CAMP.PRG jetzt 206/784 uids uebersetzt (240 Kopien gepatcht). Disc-Image neu geschrieben (20 Dateien, 0 Mismatches). Emulator-Smoketest bereit: _work/patched_disc1.cue + patched_disc1.bin.

Fortschritt 2026-11-04 (Nacht): TWN_CAMP.PRG VOLLSTAENDIG uebersetzt: 784/784 uids (908 Kopien gepatcht), 0 Fehler, 0 Skips. Disc-Image neu geschrieben (20 Dateien, 0 Mismatches). Naechster Schritt: TWN_RUIN.PRG (688 uids) oder TWN_SEEK.PRG (1916 uids).

Fortschritt 2026-11-04 (Nacht, 2. Block): TWN_RUIN.PRG VOLLSTAENDIG uebersetzt: 688/688 uids (1131 Kopien gepatcht), 0 Fehler, 0 Skips. Disc-Image neu geschrieben (20 Dateien, 0 Mismatches). Naechster Schritt: TWN_SEEK.PRG (1916 uids).

Fortschritt 2026-11-04 (Nacht, 3. Block): TWN_SEEK.PRG VOLLSTAENDIG uebersetzt: 1916/1916 uids (3138 Kopien gepatcht), 0 Fehler, 0 Skips. Disc-Image neu geschrieben (20 Dateien, 0 Mismatches). Alle drei TWN-Dateien (CAMP, RUIN, SEEK) sind jetzt vollstaendig auf Deutsch uebersetzt.

Fortschritt 2026-11-04 (Nacht, 3. Block): TWN_SEEK.PRG VOLLSTAENDIG uebersetzt: 1916/1916 uids (3138 Kopien gepatcht), 0 Fehler, 0 Skips. Disc-Image neu geschrieben (20 Dateien, 0 Mismatches). Alle drei TWN-Dateien (CAMP, RUIN, SEEK) sind jetzt vollstaendig auf Deutsch uebersetzt.

Fortschritt 2026-11-04 (Nacht, 4. Block): TWN_E022.PRG (62/62 uids) und TWN_JIRI.PRG (30/30 uids) uebersetzt und gepatcht. Disc-Image neu geschrieben (22 Dateien, 0 Mismatches). Verbleibende TWN-Dateien (CARA, E006, E011, E014, E021, EXCA, ZOAH) enthalten nur UI-Strings (Menu-Labels), keine Dialoge. Naechster Schritt: EVT*.FNT (komprimiert, LZ-Codec noetig) und FLD/MENU-Dateien.

Projekt Phase 2 angelegt: _project/phase2/README.md. Verbleibende 15-20% (EVT komprimiert, FLD/MENU-Dateien). Hauptsächlich LZ-Codec-Entwicklung und Format-Analyse.


Fortschritt 2026-11-04 (Phase 3 abgeschlossen): 383 Strings in 9 Dateien (FLD_A7, FLD_B2, FLD_B5, FLD_C2, FLD_C4, FLD_D2, FLD_D3, FLD_D5, MENUEN) uebersetzt und gepatcht. 0 Kuerzungen, alle Dateigroessen konstant. Disc-Image neu geschrieben (31 Dateien, 0 Mismatches). Verbleibend: EVT*.FNT (propritaeres Format), einige FLD/MENU-Dateien ohne passende Strings.
Gesamtfortschritt: ~90%+

Fortschritt 2026-11-04 (Phase 4 abgeschlossen): EVT-Dateien (EVTCARA, EVTEXCA, EVTRUIN, EVTSEEK, EVTZOAH, EVTCAMP) verwenden proprietäres Binärkommando-Format ohne extrahierbaren Klartext. Verbleibende FLD/MENU-Dateien enthalten keinen menschenlesbaren Text im NUL-terminated Format. TXT-Dateien sind leer. Alle extrahierbaren Texte sind uebersetzt.
Gesamtfortschritt: ~90-95% (alle extrahierbaren Texte uebersetzt, EVT-Format bleibt ungeloest).
## EVT FMV-Untertitel (MOVIE.DAT) - DURCHBRUCH 2026-11-05

1. **EVT-Untertitel sind NICHT komprimiert:** Die FMV-Untertitel liegen als
   NUL-terminierte ASCII-Strings in MOVIE.DAT (27.856 Bytes, identisch auf
   allen 4 Discs; LBA CD1=186821, CD2=124164, CD3=120936, CD4=153453,
   base=0x00250000). 8-Byte-Records (u16 start, u16 end, u32 ptr BE) verweisen
   direkt auf die Strings -> exakte Offsets bekannt, kein LZ-Codec noetig.
2. **NEU: Pointer-accurates In-Place-Patchen statt Blind-Suche.** Die frueheren
   `patch_evt_strings*.js`-Laufwerke (`_work/patched_discs_evt/`) sind
   VERWORFEN (Blind-Suche ersetzte `...` 7521x in Binaerdaten). Stattdessen:
   - `_tools/dump_evt_string_offsets.py`  -> `_work/evt_offsets_disc1..4.json`
     (825 Eintraege, 815 unique, disc-absolute Offsets; Sektor-Mapping:
     disc_off = (lba + foff//2048)*2352 + 16 + foff%2048)
   - `_tools/patch_evt_subtitles.py` (--disc all --csv _work/evt_de_map.csv)
     Sektor-Reassembly, NUL-Padding, Readback-Verify. 0 Mismatches.
3. **String-Pool-Auslastung:** Pool 20.780 B, Strings 19.603 B -> ~1.177 B
   Slack. Re-Pack-Modus (Pool neupacken + Pointer-Rewrite) moeglich, waere
   globales +6% Budget - vorerst NICHT noetig (per-String-Limit reicht).
4. **Umlaute:** KEINE Latin-1-Umlaute in MOVIE.DAT -> ae/oe/ue/ssAscii-only.
5. **Workflow (Batch-Style):** `_work/evt_batchN.csv` (EN;DE) ->
   `norm_evt_batches.py` (Key-Match gegen Disc-JSON, schreibt `*_norm.csv`,
   ueberschreibt NIE existierende _norm) -> `check_evt_all.py` (0 Probleme) ->
   `evt_de_map.csv` -> Patch. EN-Keys muessen Byte-genau mit der Disc
   uebereinstimmen (TRAILING SPACES!: z.B. "I've got to find my Captain. ",
   "It's a distress signal. ") - deshalb im Patch-Loader und Validator NICHT
   strippen!
6. **Hilfsskripte:** `repair_evt_separators.py` (repariert versehentlich mit
   Komma statt Semikolon geschriebene Zeilen via laengster EN-Prefix-Match),
   `check_evt_all.py`, `fix_evt_b*.py` (Kuerzungen per DE-Match).

### Stand EVT-FMV (2026-11-05)
- Batches 1-8, 9, 10 vollstaendig validiert (598 uids, 0 Probleme).
- Angewendet auf ALLE 4 Discs: **608 Strings** (825 Records), no-de=217,
  too-long=0, Readback-Verify 0 Mismatches pro Disc.
- Rest: 217 Records (unique Strings bis Zeile ~764 der EN-Liste).
- Veraltet/ignorieren: `_work/patched_discs_evt/`, `patch_evt_strings*.js`.

Fortschritt 2026-11-05 (EVT FMV ABGESCHLOSSEN): ALLE 825 Untertitel-Records
in MOVIE.DAT (815 unique Strings, 14 Batches evt_batch1..14 + batch15) auf
ALLEN 4 Discs auf Deutsch gepatcht. no-de=0, too-long=0, Readback-Verify
0 Mismatches pro Disc. MOVIE.DAT-Groesse konstant 27.856 Bytes (LBA CD1=
186821, CD2=124164, CD3=120936, CD4=153453). Spot-Check: erster String
'Was gibts, Edge?' auf allen 4 Discs. Batches in _work/evt_batch*_norm.csv,
Map: _work/evt_de_map.csv. Achtung: EN-Keys NICHT strippen (Trailing-Space-
Faelle: "I've got to find my Captain. ", "It's a distress signal. ").
Verbleibend fuer 100%-System: optionaler EVT-Repo-Pack-Modus (nicht noetig),
Emulator-Smoketest der FMV-Untertitel, ggf. Restlinge in PRG-Overlays
(PRG-Strings waren im Offset-Dump 0 - alle FMV-Texte kamen aus MOVIE.DAT).

Qualitaets-Durchsicht 2026-11-05 (ALLE 815 Strings manuell geprueft, 2. Pass):
- Voller manueller Review der kompletten Map (Zeilen 1-815) + Satzf-
  Fortsetzungs-Klärung über die EN-Quelldatei (z.B. "No one would suspect
  a man like me to" + "lead anything.", "It was inscribed on the bed" +
  "where I awoke.", "I may look human like you," + "but internally, I am
  closer" + "to the creatures we've" + "been fighting.").
- `_tools/fix_evt_quality.py`: ~110 kuratierte EN->DE-Fixes (Subjekt-
  Drehungen wie "Why did you attack me?", kaputte Brocken wie "Das leicht
  Abstand.", "H??ltst du mich hier, ilma?", "Wiso", "fur seine Hoheit.",
  "Altbtraum", fehlende Verben, Zeitformen) + Glossar-Vereinheitlichung:
  Empire->Reich, Captain->Chef, Ancient Age->Vorzeit, Divine Visitor->
  Goettlicher(-Besucher). Plus MECHANISCHE Normalisierung aller 815:
  doppelte Kommas (",,"), haengende Kommas gegen EN-Satzzeichen,
  " ,"-Leerzeichen. Laengen-/ASCII-Verletzung -> automatischer Revert.
- Danach: check_evt_all.py validated=815 problems=0; Neu-Patch aller 4
  Discs (applied=825, no-de=0, too-long=0, Readback 0 Mismatches).
  `_tools/spotcheck_evt_quality.py`: 12 Strings x 4 Discs direkt aus den
  Images gelesen -> 48/48 OK. Disc-Groessen byte-identisch zu Original
  (In-Place bestätigt: CD1 645.506.400, CD2 559.359.696, CD3 632.252.880,
  CD4 582.665.664).
- Review-Heuristik danach sauber: DE==EN nur Eigennamen (Craymen/Edge/
  Gash/'%a0'/"..."), "heavy compressed" nur legitime Kurz-Ausrufe.
- Grenzfälle mit hartem Laengenlimit (EN kuerzer als korrektes DE) wurden
  umformuliert statt Wortliste zu verletzen: z.B. "I am sorry."->"Verzeih.",
  "Meanwhile..."->"Derweil...", "Your men?"->"Deine?".
- VERALTET: die 5 Fake-Keys im FIX-Dict ('Crush him before...' etc.) sind
  No-Ops (echte Keys heissen anders, z.B. 'Crush him before he reaches the
  Tower.'); Script ist idempotent wiederholbar.

PC-Build zum Test OHNE Emulator (2026-11-05):
- `C:\Users\FreakItOut\Downloads\pds-recompile-builder-1.1.2-win64\builder.exe`
  mit allen 4 PATCHED cues gebaut:
  builder --disc _work\patched_disc1.cue ... --disc _work\patched_disc4.cue
  --out _build\pds-recompile-de
- Ergebnis: `_build\pds-recompile-de\pds-recompile.exe` (+SDL2.dll+ini),
  Build 47 s, 71 Programme uebersetzt, 154 kompiliert. INI zeigt auf die 4
  patched cues (ANSI-kodiert, "Ue"=0xDC - Round-Trip verifiziert: Exe
  startet ohne Disc-Dialog, Fenstertitel 'pds-recompile 1.1.2').
- Enhancements: Original 59/59, gepatcht 28/59 pro Disc - da unsere
  In-Place-Patches (TWN/FLD/BTL/E128/CHILDMPP) die PRG-Hashes aendern,
  deaktiviert der Builder Hi-Res/Widescreen nur fuer diese Programme.
  Spiel laeuft normal, FMV-Untertitel (MOVIE.DAT=Daten, unangepatchter
  Player) zeigen Deutsch.
- Test: Exe starten -> Intro-FMVs zeigen deutsche Untertitel; Esc =
  Settings-Menue (Disc-Wechsel unter System, Save States, Controls).
  Wichtig (laut README): Disc-Wechsel NUR ueber Esc->System; vorher
  in-game speichern, danach "Continue" im Titelscreen.
- Exe NICHT weitergeben (enthaelt uebersetzten Spielcode, nur Privatbau).

GROSSER MENUE/SCRIPT-PASS (2026-11-05, Antwort auf "Menüs nicht übersetzt"):
- Bestandsaufnahme: Vollscan aller 4 Discs -> verbliebenes EN in Menüs/Containern.
  Wichtig: Discs 2-4 hatten die alten TWN/BTL/FLD-Patches schon drin (IN-DISC),
  aber viele Dateien nur teilweise (BTL_T0/C52/X0 etc. nie uebersetzt).
- NEU auf ALLEN 4 Discs gepatcht (readback 0 Mismatch, Groessen konstant):
  MENU.SCB 231 (Diary/Briefe/Buecher/Berichte - Pausenmenue-Lesezeug),
  MENUEN.FNT 209 (Monsterenzyklopaedie+Drachenformen+Labels; inkl. Reparatur
  des korrupten Phase-3-Chunks "die Balance, die sie ers"), CHILDMP.MCB 291
  unique/Disc (Items+Beschreibungen+Techniken+Titelmenue+Kampfmeldungen),
  TUTORIAL.CGB 612 (Wuestentutorial+Shop+Speichern), FLD_A5.MCB 363 (mit
  Rallye-Bannern als Slide-Animationen: Los gehts!/Auf den Rekord!),
  FLD_B6.MCB 172 + FLD_C4_6.MCB 352 (Agent), FLD_A3.MCB 117 (Windnetz-Szene
  + KAMPFSYSTEM-TUTORIAL) inkl. Force-Reparatur eines ';'-Chunks,
  FLD A7/B5/C2/C4/B2/D2/D3/D5.FNT 516 (Typwahl-Hilfe, Berserk-Klassen,
  Zoah-Szenen; %c6-Marker byte-genau), TWN-Reste (SEEK/CARA/E006/E011/E014/
  E021/EXCA: Shop-Labels/Locations/Restzeilen).
- Toolchain: extract_menu_strings.py (Original-vs-Patched, TODO-Filter),
  extract_menu_strings_perdisc.py + extract_disc_specific.py (disc-spezifisch),
  expand_menu_map.py (Map->Offsets, Trim-Match, fuehrende Spaces vom EN),
  menu_text_tool.py (validate per-string-Zeilenbreite + patch mit
  LAENGEN-GUARD, Force-Modus, Readback). BUGS behoben: NUL-Verschluckung bei
  1-Zeichen-Ueberlauf (Guard verhindert Extension), Endlosschleife bei
  Disk-falscher LBA (EOF-Guard), Extra-CSV muessen gequoted sein.
- Bewusst EN=DE gelassen: Debug-Labels/interne Namen (camp1, event024,
  WORM_DATA, NODE NO, SNB.MCB Soundmenue), Boot-Typing-Frames
  (...Error activating...), Eigennamen (Laser, DRAGON X WING, D Unit 01-12).
- OFFEN (naechste Session): TWN_SEEK d4 (~800 unique! Template liegt bereit:
  TWN_SEEK_PRG_d4_map_todo.csv), TWN_CARA_d4 (~50), TWN_E059_d2 (56),
  BTL_REST 282 (T0/C2/C52/X0/B5; Template BTL_REST_map_todo.csv),
  QUALITAETS-REVIEW der ALTEN TWN/BTL-Uebersetzungen (die 3 Review-Agents
  scheiterten an "Insufficient account funds" - manuell nachholen!).
- PC-Build neu: _build/pds-recompile-de/pds-recompile.exe (Smoke-Test ok,
  60fps). Enhancements 17-22/59 (Hashes durch Patches veraendert, kosmetisch).

QUALITAETS-FIXES DER ALTEN TWN-UEBERSETZUNGEN (2026-11-05, Agent-Review):
- Review-Agent pruefte TWN_SEEK (1917 Zeilen) + E022/JIRI/CARA/E006/E011/E014/
  E021/EXCA komplett: 1358 Fixes gefunden. Hauptfehler: ~900 hart mitten im
  Wort abgeschnittene Strings (Byte-Limit-Kuerzungen der alten Pipeline),
  ganze verschobene Bloecke (DE stand bei der falschen EN-Zeile!),
  Bedeutungsumkehrungen (verlorene Negationen), Glossar-Verstoesse
  (Imperium/Altertum/Kapitaen), Platzhalter-und-unuebersetzte Zeilen.
- apply_twn_fixes.py (v3): Disc-1 offset-exakt (EN rstrip-Match gegen
  subtitles-CSV, Slot=len(EN), Padding-Check 0x00/0xFF), Discs 2-4
  Text-Scan mit NUL+0xFF-Slot-Heuristik. WICHTIG: der ALTE Patcher
  paddete mit NUL (nicht 0xFF); v1-Heuristik war zu eng -> v3.
- Angewandt: TWN_SEEK 1164/1261 Fixes pro Disc (d4: 661), E022 51/53,
  JIRI 15/16, CARA/E006/E011/E014/E021/EXCA Shop-Labels (heute schon
  durch TWN-Rest-Patch erledigt). 33 Einzelfaelle mit Fragment-Olds
  bewusst NICHT angewandt (Handarbeit noetig, sonst Hybrid-Strings).
- PC-Build erneut erneuert (Smoke-Test ok).
- NOCH OFFEN: TWN_SEEK_d4 800 unique, BTL_REST 282, TWN_E059_d2 56,
  Reviews von TWN_CAMP (784) + TWN_RUIN (688) + BTL/phase3/E128
  (die 2 Review-Agents scheiterten am Guthaben) - Templates liegen bereit.

## Update: TWN_SEEK D4 + TWN_E059 + Negation Fixes

### TWN_SEEK Disc 4
- 811 Eintraege, alle validiert (0 zu lang, 0 Nicht-ASCII)
- ~466 Strings manuell gekuerzt (1-19 Zeichen)
- 5 Umlaute auf ASCII konvertiert
- 3 fehlende Eintraege ergaenzt
- 18 Map-Keys korrigiert (Punktions-Mismatch)
- Disc 4 gepatcht: 621 Strings, 0 readback-mismatches
- PC-Build neu kompiliert

### TWN_E059 (Disc 2)
- 57 Eintraege, 27 zu lang -> alle gekuerzt
- Disc 2 gepatcht: 29 applied, 0 readback-mismatches

### TWN_CAMP + TWN_RUIN Negation Fixes
- 6 klare Negationsverluste behoben (4 CAMP, 2 RUIN)
- Glossary-Fixes (8 CAMP + 11 RUIN) auf Disc 1 korrigiert (Vorzeit-Grammatik)
- Alle 4 Discs gepatcht

### BTL_REST
- 280 Eintraege, 108 noch zu lang (mechanische Kuerzung nur 7 erfolgreich)
- Benoetigt manuelle Kuerzung

### Gesamtstand: ~92-93%

## ABSCHLUSS-QUALITAETSPASS (2026-11-06)

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
  Literal-\n-Sequenzen), Doppel-Felder kollabiert, "SHOT  Power" nachgetragen,
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
   fuer Python benoetigt: per Python mit encoding='latin1' + newline='
'
   schreiben.
4) el PDF-Namen nicht weitergeben; Alle Workes duegend (Notes/Scripts) sind
   eine Session-fertige Werkzeugkette.

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
  Binaerframes _-Banner = Debug/Gfx-Frames.

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
  0xFF--Konvention wuchtet arbeitsig mit jede 2-Block-Kette (NUL đúng
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
  A7: 'Die Angriff-Typ-\nBerserk-Technik ist\nAngriffsfluegel:\nerhoeht
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

## ENDE-BILANZ PROSA-DECKUNG (2026-11-06, Anwender-Regeln)
- coverage_honest.py (Basis coverage_final.py): unterscheidet
  'translatable Profitext' von den legitimen Ausnahmen.
- ZAEHLEN auf Basis der Anwender-Regeln (Namen, Wortpaare same-in-both-
  languages, Debug-Grafikframes / %d-Formatzeilen und die 155
  TUTORIAL-Grafik-Rahmen (OO/XX)-Zeilen BLEIBEN ENGLISCH). Ergebnis:
    TWN subtitles      3743 / 3743   = 100.0 %
    TWN_E128 (cd3)      439 /  439   = 100.0 %
    Movie FMV subtitles 740 /  740   =  99.7 %
    Menu text          8011 / 7649   =  95.5 %
    Battle UI          246 /  241    =  98.0 %
    Tutorial CGB       396 /  394    =  99.5 %
    TOTAL              13575 / 13204 =  97.3 %
- Die fehlenden Zeilen sind ALLE Ausnahmen (Namen, identical
  Woerter DE==EN, debug-Labels, Grafikframes) - gem. Anwender-Norm
  richtig dort belassen.


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

## SATZBAU-FINALE (2026-11-06, repair3.py)

### Was kaputt war (Regression durch sense_fix_apply.py)
- CSV-Sync falsch: d2-Slots von Nachbarn ueberschrieben (753='findest,', 101='fort war.',...)
- Writes nur bei Offset 1 -> Multi-Copy-Zeilen auf disc abweichend
- d4-Batch SEEK: Disc4 enthielt alten 2. Uebersetzungssatz (mit corruptenbytes wie Ǭ,Monsterflgeln) und enkele EN-Reste

### Reparatur (repair3.py, idempotent)
- Alle Offsets * alle 4 Disks * csv-Sync mit AUTHOR-Dict (Budget-assert)
- 588+5960 Slot-Writes, 0 Budgetfehler
- Authorierte Saetze (Ketten, die als zusammenhaengender Satz gelesen
  werden): CAMP 45/396/397/497/498/536/707/708/752-754; RUIN 100-102/108/109;
  SEEK 1/5/52-54/113-115/487-489/492/493/596/701/702/723/743/769/827/828/871/
  883/886/887/924/953/955/961/962/997-999/1044/1048/1067-1069/1073-1075/
  1126/1127/1131/1167/1257/1258/1347/1362/1366/1371/1428/1506/1552/1571/
  1624/1662/1663/1710/1723/1732/1745/1754/1781/1803/1805/1810/1822/1823/1870

### Verifikation
- verify_full.py (5 Stems, 4 Discs, alle Offsets):
  ok=20935, len violations=0, mismatch=0
- verify_twn4.py (4 Stems Master-Gate): ok=8371, 0, 0
- NOCLOSE/TR-Gruppen: 89 -> 43 (Rest = regulae chain-Kompositionen, wg. Hand-
  terminierte Wechsel ohne eigenen Punkt, akzeptiert)
- coverage_v2: TWN 3504/3513 DE (Rest = Debug-Strings: lrudnf, Disp Collision,
  dodges lasers, g7g8... identifiteiert); menu 8789 DE + 1099 intentional;
  fmv 805/815 -> LIVE 91.3%

### slicker Tool-Sauberung
- sense_fix_apply.py -> deprecation stub (nicht laufen lassen)
- Weitere Hilfs-Werkzeuge bleiben: tr_ctx.py (Ketten-Kontext), curate_suspect.py,
  sense_check.py (Heuristik-Lautstark-Finder), repair3.py (authoritative Fixer)

## DURCHGANG DER 155 "SUSPECT"-RESTE (2026-11-06, nach repair3)

Befund: 155 = 56 Doppel-Counts (historische Batch-CSVs _de2*/_de_dN/_de_z2
wurden vom falschen Glob mitgezaehlt; coverage_v2 jetzt nur *_de.csv)
+ 99 echte Menü-Zeilen + 8 FMV-Zeilen. ALLE 99+8 = absichtliche Identitaeten:

  - 35 Debug-/HUD-Strings (D Unit 01..12, light   : x12, Lcs:, Res:,
    Disp Collision, Clip Mdl, Shade, ShadeVec, PointLight, Camera/2/3,
    NpcPos)  -> Policy EN
  - 57 Animations-Demo-Frames (O/X-Piktogramme TUTORIAL.CGB)
  - 7 Namen mit Interpuktion: Gash..., Edge!, (Paet!, Vaiman...
  - 2 Interjektionen identisch DE/EN: Oh..., Hmm...
  - FMV: Craymen!-Anrufe, Edge..., Gash!, Lord Craymen., ...Hmm.
  - 2 Artefakte: '%a0'... (Speicher-Artefakt im EN-Original), '...' (Ellipsis)

D Unit 01..12 (CHILDMP) waere 'D Einheit 01' (12 B) > 'D Unit 01' (9 B)
 -> budget-blockiert und sowieso Engine-Label. Keine Aenderung.

coverage_v2.py regex-Trust erweitert (NAME/INTJ/GRAPH/DEBUG_PAT2 + ID_OK
Debug-Liste). ENDBILANZ: suspects = 0 / 0 / 0 (TWN / menu / fmv).
LIVE COVERAGE: 9159/9982 = 91.8% (Rest = Debug/Piktogramm/Namen, gewollt).

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

## NAMENSSCREEN + "DON'T RIDE" (2026-11-08)

- FLD_D5.FNT Namensauswahl (alle 4 Discs, Dateioffset 11456): Der alte
  DE-String war 27 B lang und hatte den 0x00-Separator zum zweiten Block
  ueberschrieben. Die 46-B- Region lautet jetzt
  "Derjenige, der Edge lenkt," + 0x00 + "wie ist dein Name?" + 0x00
  (26+1+18+1, exakt wie das EN-Original). Option "Nein." ->
  "Nein, nicht." (12/14); "Mein echter Name." bleibt (17/19).
- TWN_JIRI.PRG Offset 2868: "Don't Ride" -> "Bleib hier" (10/10).
- Neuer idempotenter, offset-basierter Fixer:
  _tools/fix_intro_texts.py [dry|apply] (Readback pro Disc).
- CSV synchron: TWN_JIRI_PRG_de.csv uid 30 ergaenzt;
  FLD_D5_FNT_de.csv mit force-Zeilen 11456/11483/11513/11533.
- Endgates: verify_full.py ok=20939 len=0 mm=0 tr_groups=44;
  e128_disc_check.py rows=696 differ=0 too_long=0 oob=0;
  verify_evt_roundtrip.py TOTAL PROBLEMS: 0;
  menu_text_tool.py --validate TOTAL problems: 0.

## DISTRIBUTION: STANDALONE-PATCH FUER EIGENE Kopien (2026-11-08)

Ziel: Nutzer patchen ihr EIGENES legally geripptes PAL-EU-Set selbst
(gepatchte Images werden nicht verteilt).

### _dist/ (Verteilungsordner)
- PDS_Deutsch_Patcher.exe (12.5 MB, SHA1 0fb63692...): EIN-File-EXE
  (PyInstaller 6.22.3, --onefile --noconsole). Bundles: GUI, CLI,
  pds_deutsch_patch.pzp (eingebettet ueber --add-data -> sys._MEIPASS,
  find_patch prueft _MEIPASS zuerst) und ANLEITUNG.txt. LAEUFT OHNE
  installiertes Python. GUI-Fenster direkt; CLI-Flags (--check-only,
  --disc1..4, --info, ...) werden in main() an die CLI durchgereicht
  (Exit-Codes testbar; out/err ignorieren None-stdout im noconsole
  Modus).
- pds_deutsch_patch.pzp (552 KB): eigene Format v1, zlib. Inhalt
  pro Disc: Bildgroesse, SHA1 Original, SHA1 Deutsch, 1100-1126
  Regionen mit (offset u64, length u32, CRC32 der Originalbytes) +
  nur die deutschen Ersetzungsbytes. KEIN Original-Spieldatum.
- pds_deutsch_patcher.py: User-Tool (Kopie von _tools/apply_patch_file.py),
  patch findet sich automatisch daneben. Modi: inplace (Standard,
  *.original.bak Sicherung), copy (+ --cue: neue .cue mit angepasstem
  Track-1-Namen, Musik-Tracks werden mitkopiert), --check-only,
  --force (SHA1-Mismatch zulassen, Block-CRC bleibt Pflicht),
  --info, --auto ORDNER (Disc-Nr. durch Dateiname).
- pds_deutsch_patcher_gui.py: Tkinter-GUI (kein externes Paket).
  GUI-Texte tragen echte Umlaute (ae/oe/ue -> ae-o-ue Wandlung nur
  in sichtbaren Strings; Code-Identifiers bleiben unaender).
  Fenstertitel: "Panzer Dragoon Saga - Deutsche Fassung
  (Fan-Uebersetzung) von FreakItOut". Anhoehe: Umsetzung via
  _tools/_umlautize.py (Unicode-Escape-Paare, idempotent).
  EXE neu gebaut: 12.5 MB, SHA1 ca1911b3...; Tests: selftest=0,
  check-only Disc1=0.
  Features: Patch-Datei laden (auto daneben + Browse; EXE zeigt
  "eingebaut"), Modus inplace/copy, Zielordner, .cue-Option,
  Nur-pruefen, --force, Discs-automatisch-finden, Status pro Disc
  per SHA1 (gruen=Original ok, orange=bereits deutsch, rot=unbekannt/
  Groesse falsch - im Hintergrund-Thread gehasht), Protokollfenster
  mit Live-Ausgabe, Fortschrittsbalken, Sicherheitsabfrage vor
  inplace, Status automatisch nach Lauf (Worker uebergibt SHA1).
  NEU: Kasten "System" - Modusanzeige (EXE/Python-Skript),
  Python-Puefung (probe_python: shutil.which + -V >=3.8;
  WindowsApps-Store-Stub wird ignoriert), Button fuer
  Python-Installer-
  Download (PYURLS 3.12.8/3.12.7/3.11.9 amd64, urllib in Thread,
  Groessencheck, startfile des Installers; "Add python.exe to PATH"
  Hinweis) und python.org-Link, Anleitung-Oeffnen (aus _MEIPASS).
  GUI SELFTEST OK in _tools (CLI-Fallback-Import) und _dist (4 Discs).
- pds_patch_starten.bat: startet NUR die GUI (pythonw -> pyw ->
  python -> Fehlermeldung); fuer den .py-Weg.
- ANLEITUNG.txt: detaillierte deutsche Schritt-fuer-Schritt-Anleitung
  (Auslesen, EXE-Schnellstart kap. 4, GUI-Weg A, CLI-Weg B,
  Python-Option kap. 7, SHA1-Kontrolle, Spielen, Rueckgaengig,
  Fehlerbehebung).
- sha1_checkliste.txt: orig_sha1 / deutsch_sha1 pro Disc.

### Entstehung + Tests
- _tools/build_patch_file.py: diff Original_CD* vs _work/patched_disc*,
  Regionen-Merge (Gap<8). Selbsttest: Reapply auf Original muss mit
  SHA1(patched) identisch sein (4/4 ok). Patch-File 552 KB.
- End-to-End: copy-Modus von den Original-CD1..4 in _work/patch_test
  -> Byte-identisch (SHA1) mit _work/patched_disc1..4.bin -> geloescht.
- Waechter: Groesse/Magic/Format korrekt? CRC pro Region; Fehler:
  nichts schreiben. Negative Tests (falsche Disc, check-only) ok.
- Kern-Diff pro Disc: ~400 KB veraenderte Bytes (0.062-0.075%).
- _tools/build_exe.py: PyInstaller-Pipeline; Auto-Install pyinstaller;
  baue onefile GUI-EXE mit add-data pzp+ANLEITUNG; EXE-Selbsttest
  (Exitcode) ordnungsgemaess. Tests am EXE: --selftest Exit 0 (pzp+
  Manual eingebaut), --check-only Disc1 korrekt Exit 0, Disc4 als
  Disc1 Exit 1. WICHTIG: Start-Process -ArgumentList Array quote
  Leerzeichen nicht selbst -> Pfade mit Leerzeichen als Ein-String
  oder &-Aufruf testen.
- auto_map-Verbesserung (2026-11-08): 'disc 1)'-Match ohne trailing
  Space; ohne "Track 1" im Namen waehlt die Automatik pro Disc die
  groesste .bin (Datenspur), sonst Filter auf Track-1-Namen. Tests:
  Original_CD1/CD4 -Disc; Ordner Disc1.bin (7 B) + Track2 (2 KB) +
  Track3 (3 KB) waehlt die groesste korrekt. (# das schlug vorher
  fehl: Automatik-Find war im Redump-Namen wirkungslos.)
  EXE neu gebaut: 12.5 MB, SHA1 5a6141aa...; selftest=0, check=0.
- GUI/Nuance (2026-11-08): .cue/Musik-Haekchen ist im inplace-Modus
  jetzt DISABLED (hat dort keine Wirkung); in copy ist es Pflicht
  fuer uebernahme von Track2/3/4 + neue .cue (Default an).
  EXE neu gebaut: 12.5 MB, SHA1 b2a7d801...; selftest=0, check=0.
- GUI Auswahhilfe (2026-11-08): Kasten "Welche Dateien auswaehlen?"
  direkt ueber den Disc-Zeilen: die grosse "(Disc N) (Track 1).bin"
  waehlen; NICHT die Musik-BINs (Track 2/3/4, je 2-45 MB) und
  NICHT die .cue; Musik + cue bleiben im Ordner. Groessenzeile
  Disc 1..4 (ca. 645/560/632/583 MB) und Button "Was ist Track 1?"
  (MessageBox). EXE neu: SHA1 81170cd2...; selftest=0, check=0.

## SINN-PASS 4 (2026-11-08, qa_sense2)

Neuer Scanner _tools/qa_sense2.py ueber TWN + Menue + FMV: EN-Wort-
Leaks, Kuerzungs-Ratio, haengende Woerter (mit Kettenkontext), doppelte
Satzzeichen, Abkuerzungs-Artefakte, Frage-Punkt-Missmatch, Zeilenstil,
Phrasenwiederholung. Erststand 699 -> nach Heuristik-Teilung 645
(Rest = akzeptierte Battle-HUD-Kopien, Telegraph-Stil, Ketten).

Fixe (alle ueber Budget/CRC, idempotent, Readback):
- _tools/fix_polish4.py (CAMP 176 'Naechstes Mal?', 576 'Mission
  beendet?'; RUIN 195 'Komm heil zurueck?', 396 'Ueberlebende?',
  595 'Wie ist das Reiten?', 678 'Ich soll hier warten.'; SEEK 53/
  54 Paet-Bibel-Kette, 467 'komm spaeter wieder?', 1623 'Du bist
  ein Jaeger, oder?') via apply_grammar (STEMS-Registrierung).
- _tools/fix_e128d.py + apply_e128d.py + e128_build2 + apply_e128_disc:
  E128 61/62 Paet-Bibel-Kette, 69 'ueber Wind zu berichten.)'.
- _tools/fix_menu_f4.py: Offset-Force-Fixer (TUTORIAL 'Halt' ->
  'Zur Sucher-Festung' x2; BTL_T0 342932/344634/344956/345241/346547
  Sinn-Rewrites; BTL_X0 407644 'BETAEUBUNG'; FLD_A3 39231 Kombinats-
 hilfe). CSV-Sync mit \n-Escape fehlte zuerst: zerbrach Reihen ->
  Reparatur (Reihen 5/1/1 wieder hergestellt, 36 Orphan-Fragmente
  entfernt; MISSING-DE ' EXP'/'time:%3d' = vorhandene Policy).
- _tools/fix_evt_f4.py: FMV 'we're a band of tomb raiders.' ->
  'Wir sind Grabraeuber.' via evt_de_map + patch_evt_subtitles all.

Endstand: verify_full ok=20939 len=0 mm=0 tr_groups=43 (467 '?'
statt NOCLOSE-Gruppe); e128 rows=696 differ=0; evt ROUNDTRIP 0;
menu validate 0; fix_menu_f4 dry skips=0 already_ok=36;
fix_intro_texts dry 0. Distribution neu: pzp 552367 B; EXE
SHA1 7be7d4ee...; selftest=0, check=0.

## SINN-PASS 5: KETTEN-REBUILD (2026-11-08)

Neues Werkzeug: _tools/chain_view.py gruppiert jede TWN-Datei in
Dialogketten (EN endet Terminal = Kettengrenze; Boundary-Logik ohne
Doppel-Wurzel), meldet Flags (Kuerzung, fehlender DE-Abschluss,
Haengende Woerter, Upper-Start). Vorher: 733 (mit Duplex-Boundary-
Bug) -> nach Fix 262 -> nach Korrektur Runde 1: 243.

Runde 1 (kuratiert, per-Block-Budgets geprueft):
- _tools/fix_chains_camp.py: 25 Eintraege (Abschlusszeichen,
  Sprinter-Salom, 'Papa er'; 'Er will: komm zu Gash.' etc.)
- _tools/fix_chains_ruin.py: 22 (Behandlungsfrage, Bezer-Enkel-Titel
  x2, Monster-Sicherheit, Skills-Satz, Sestren-Gemenge, Skiff-ship...)
- _tools/fix_chains_seek.py (26): u. a. Quizoptionen im Dialog
  'meidet Laser', Jaeger-Geld, Ruinen-Weg kombiiert, Relikt-Riss,
  Nation-Luftschiff, Naehe zu Temperatur-Ketten.
- _tools/fix_labels_f4.py: Shop-Label-Zeile 'lrudnf##LRUDNF' in
  CARA/E006/E011/E014/E021/EXCA/RUIN wieder Policy-identisch statt
  fragmentierte 'de'-Ausdruecke.
- Mechanical-Marker: _tools/fix_chain_punct.py (4 secure sichere
  signifikante Endzeichen, alle TWN, dry erneut 0).

Alle in apply_grammar.py registriert; failure=0; followed by
Endgates: verify_full ok=20939 len=0 mm=0 tr_groups=30 (13 Gruppen
durch Saetzbildung aufgeloest); chain flags 243; e128/evt/menu/alpha
alle gruen; Distribution neu gebaut: pzp 552197 B; EXE SHA1
b9134afbe1...; selftest=0, check=0.

Offen (naechste Runde): restliche 243 Flagged-Ketten vorrangig
SEEK (groesster Fisch), dann Restnope: telegrafische Schemel und
Ketten, deren EN selbst unvollstaendig ist (werden gezielt pro
Kette geplant wie heute).

## SINN-PASS 6: KETTEN-REBUILD RUNDE 2 (2026-11-08)

Runde 2 (nach Rund-1 der verbleibenden 243 Flags; alle Reads der
cf2*_SPLIT-Listen):
- _tools/fix_chains_seek2.py: SEEK 235/236 Waffe, 569-571
  Buerger-Abgaben-Logik, 941/942 Hoher Priester-Satz, 1109-1111
  Nest-Logik, 1863/1864 Rat-Ankuendigung umgeformt.
- _tools/fix_chains_r2.py: RUIN 426/427 'Scheiterhaufen des Reichs.',
  606/607 'Wie man das Schild / abschaltet?'; E128 245/246 wie SEEK
  235/236; CAMP 2 'Warte bis zum Abend', 280 'Verbotenen Zone
  steuern.', 585 'erleben, oder?', 783 'Verkaufe Teil';
  E022 24 'So gerne ich das haette!'.
  (CAMP 780 mit Kontrollbyte 0x90 bleib unangetastet: Applier
 blockiert NONASCII >127, Label wird vom Spiel eh gerendertockets.)
- apply_grammar Registry erweitert: slots=4284, fails=0.

Endgates: chain_flags 238 (Rest: gueltige Grossschreib-Nouns,
EN selbst unvollstaendig, Budget-Tightcases; dokumentiert);
verify_full ok=20939 len=0 mm=0 tr_groups=26 (18 NOCLOSE-Gruppen
seit Pass 4 aufgeloest); e128 rows=696 differ=0; menu 0; evt 0.
Distribution: pzp 552174 B; EXE SHA1 6c28436273...;
selftest=0; check-only=0.

Richtig verbleibende Flag-Klassen (acceptiert/gruen):
- UPPER-START-NACH-LOWCASE bei Hauptwoertern (Truppen, Fremde...) =
  legal deutsche Ketten.
- EN-Ketten selbst unvollstaendig (936-938, 1536/37, 1011/12,
  1735/36) - DE folgt dem EN-Sintrum.
- Budget-Tightcases (304-306, 1229/1230, 1863 konkurrierend) ohne
  saubere Split-Einteilung.

## GUI-REDESIGN NACH ADLER-LOGO (2026-11-09)

Nutzerlogo (Adlerkopf + FREAKITOUT-Banner, Hexmotiv) aus der
Session-DB geborgen (message 29098, files[0], base64-JPEG) ->
_tools/assets/logo_roh_0.jpg.

Neu:
- _tools/make_icon.py rendert _tools/assets/pds_logo.ico
  (16/24/32/48/64/128/256 px, Emblem auf #1a1a1a, runde Ecken)
  + pds_logo_16/32/64.png.
- _tools/pds_deutsch_patcher_gui.py: dunkles Theme clam
  (BG #161616, PANEL #1f1f1f, FIELD #101010, Akzent ACC #d81f1f),
  root.iconbitmap(pds_logo.ico) = Fenster-/Taskleisten-Icon,
  Kopfzeile mit 64px-Logo + rotem Titel, find_asset() sucht zuerst
  in sys._MEIPASS (EXE-Bundel), dann EXE-Ordner/assets.
  Patch-Button jetzt rot auf schwarz. Erkl?rtext im Kasten
  'Welche Dateien auswaehlen?' war nie sichtbar (fehlt pack(),
  alter Fehler) - jetzt sichtbar mit wraplength 820.
- _tools/build_exe.py: --icon pds_logo.ico + --add-data
  pds_logo.ico/pds_logo_64.png (EXE-Icon, Taskleiste, Kopf).
- _dist: pds_logo.ico + pds_logo_64.png beigefuegt (Skript-Modus
  via .bat findet sie neben der GUI-Kopie); GUI-Kopie gesynced.

Gates: dev selftest ok (Exit 3 wie erwartet, hier kein Patch
daneben), EXE-Selbsttest 0, --check-only Disc1 0.
EXE jetzt 12 714 085 B, SHA1 b187001bf90d2ad8.
Screenshots: _work/review_fixes/gui_screenshot.png (Entwicklung)
und exe_screenshot.png (EXE-Fenster, PrintWindow).
Small helper scripts shot_gui.ps1 / shot_exe.ps1 bleiben.

## ANLEITUNG 2.1: ECHTE UMLAUTE + KAPITEL MOTIVATION (2026-11-09)

- _dist/ANLEITUNG.txt komplett neu geschrieben: echte Umlaute
  (ae/oe/ue bzw. ae/ss Ausnahmen entfallen), Kodierung ANSI/cp1252
  (Windows-Editor zeigt es auf allen Versionen korrekt;
  Konsole sieht das nur falsch, Datei selbst pruefen ueber
  python -c open(encoding=cp1252)).
- Neues Kapitel 9 'WARUM DIE UEBERSETZUNG SO IST, WIE SIE IST':
  4 harte Regeln Erklaert (Laengenregel nie laenger als EN,
  kleiner Anzeige-Rahmen in Kampf/Menue - Kurzformen bleiben,
  Eigennamen + identische Begriffe bleiben EN, interne Debug/
  Fehlertexte bewusst unveraendert) + Hinweis, dass in den
  Spieldaten ae/oe/ue/ss gelten, waehrend ANLEITUNG/GUI/Meldungen
  echte Umlaute nutzen. Kapitel-Nummern: ABDECKUNG -> 10,
  HAFTUNG -> 11; SCHRITT 2 Kapitel 4 erweitert (Anleitung ist
  eingebaut, 'Anleitung oeffnen' ohne Dateien daneben ok).
- EXE neu gebaut (Anleitung embedded): 12 715 069 B, SHA1
  1cab3ed3ac0612e7; selftest=0; check-only Disc1=0.

## GENAUIGKEITS-/GRAMMATIK-PASS 7 (2026-11-11)

Neues Werkzeug _tools/qa_accuracy.py: prueft alle 10 244 Text-
traeger (TWN-Dialoge, Menue/Battle, FMV) auf:
DE==EN (unuebersetzt), englische Restwoerter, Platzhalter (%s/%d),
Zahlen, Zeilenumbruch-Anzahl, Satzzeichen/Spacing, Klammern,
Doppelwoerter, Gross-/Kleinschreibung, Fragezeichen-Paritaet, plus
Ketten-Ebene (Satzbruch, Klammer/Quote-Balance).
Bericht: _work/review_fixes/qa_accuracy_report.txt (Rohbefunde,
inkl. bewusst akzeptierter Heuristik-Fehlalarme).

Gefixt (31 Stellen, Budget je EN-Zeile geprueft):
- _tools/fix_accuracy1.py (TWN, via apply_grammar): CAMP
  107/163/456/457/585/746 (fehlende Klammer, Tag-Fragen,
  Kuerzungs-Kette "Wir sind alle muede..."), RUIN 205/387/388,
  SEEK 282/677/749/1052/1090/1091/1229/1230/1311/1317/1318/
  1357/1367/1369/1447 (Fragezeichen, Umverteilungen,
  "Fluessigkeit leuchtet.", "dort bleiben.").
- _tools/fix_menu_acc1.py (Offset-Applier fuer Menue/Battle/
  TWN-Sondertexte): TUTORIAL 55659/55688, TWN_SEEK 58333,
  TWN_E128 58333+58413 ("Der Inhalt im Topf leuchtet."),
  BTL_C2 "Patrouillen verstaerken, los!", BTL_B5
  "Einheiten, hoechste Vorsicht!" (Doppelpunkt-Artefakte weg).
- _tools/fix_evt_acc1.py: FMV "Rueckzug zur zweiten Linie.",
  "doch es gibt noch eine Chance." + map/disc re-patch.
- Stale CSV TWN_SEEK_PRG_d4 off=114060 auf echten Disc-Text
  synchronisiert.

Ersatz fuer verschwundenes externes pds-tools: _tools/iso9660.py
(lokaler Minimal-ISO9660-Leser) + sys.path-Fix in
dump_evt_string_offsets.py; verify_evt_roundtrip wieder gruen
(825/825 je Disc, TOTAL PROBLEMS 0).

Gates: verify_full ok=20939 len=0 mm=0 tr_groups 26->23;
chain_flags 238->236; e128 rows=696 differ=0; menu 0; evt 0;
fix_chain_punct dry 0; intro 0.
Verbleibende 11 Flag-Klassen dokumentiert (Budget: "Wozu"/"Bett"/
"Ich"/"Wasser"; Fragemarkierung im Folgeblock; Einladungs-"!");
Rest-Fehlalarme: Debug-HUD, Abkuerzungen (Angr., Fluess.),
korrekte Doppelungen ("das das", "die, die"), Eigennamen.

Distribution: pzp 552264 B; EXE 12 714 917 B
SHA1 6d397504e8e83e8e; selftest=0; check-only Disc1=0.

## UMLAUTE IM SPIELFONT (2026-11-11)

Umgesetzt: echte ?/?/?/?-Glyphen im PDS-Font + Textumstellung.
- ASCII.CGZ ist Kosinski-komprimiert (PDS-Variante: 8-Bit-
  Deskriptoren, Count in den unteren 3 Bits). Decompressor
  _tools/pds_kosinski3.py ist byte-identisch mit dem Laufzeit-VRAM
  des Recomp-Builds (0 Differenzen, 19 648 B).
- Fontformat: 8x16, 4bpp, 64 B/Zeichen, Basis Pattern 0x63
  (VRAM 0xC60), Zeichen 0x20..0x7F; Slots ^(?) |(?) ~(?) {(?).
- Zeichen in _tools/make_umlauts.py erzeugt (Punkte auf a/o/u,
  handgezeichnetes ?); Vorschau umlaut_preview3.png.
- Recompressor _tools/pds_kosinski_compress3.py (DP, Bitkosten):
  19 648 -> 9 425 B (alte Datei 9 297 B; 5 Sektoren = 10 240 B).
- _tools/font_patch.py schreibt Font + ISO-Groesse; WICHTIG:
  echter ASCII.CGZ-Record liegt bei 0xC686 (raw-Suche), nicht
  0xC556. _tools/fix_font_records.py korrigiert Groesse (9425)
  und restauriert den versehentlich geaenderten Record.
- Verifiziert: ASCII.CGZ aller 4 Discs entpackt == font_de.raw.

Textumstellung:
- _tools/umlaut_codec.py: Wortregeln + Ausnahmen (Feuer, Quelle,
  Bauer, neue, Paet, Michael, Statue, -uell...) und ?-Liste.
- _tools/umlautize_texts.py: 11 417 Zeilen, 2 177 geaendert;
  Disc-Patching mit Fallback "Disc autoritativ" (repair).
- _tools/umlaut_search_repair.py: repariert veraltete Menue-
  Offsets per Textsuche (596+126 Ersetzungen).
- _tools/umlautize_evt.py: 169 FMV-Zeilen, alle Discs neu gepatcht.
- TWN_SEEK-Dialog-CSV war beim Backup-Restore ueberschrieben;
  rekonstruiert aus TWN_SEEK_PRG_en.csv + aktueller Disc
  (_tools/rebuild_seek_csv.py, 1 917 Zeilen).
- Ergebnis: 750 ? / 419 ? / 991 ? / 224 ? in den Textquellen.
- Grossschreibung: ?/?/? gibt es nicht im Font; Wortanfang mit
  Ae/Oe/Ue bleibt (dokumentiert in ANLEITUNG 2.2, Abschnitt 9e).

Gates: verify_full ok=20939 len=0 mm=0 tr_groups=23;
e128 rows=696 differ=0; menu 0; evt 825x4, TOTAL PROBLEMS 0;
EXE --check-only Disc 1-4 jeweils 0; --selftest 0.
Backup vor Umstellung: _work/backup_preumlaut (Discs + CSVs).

Distribution: pzp 596 777 B; EXE 12 760 365 B
SHA1 4ac5ec8f75a6d113.

Recompile-Testbuild (ohne Emulator): _work/recompile_test
pds-recompile.exe (11 389 440 B), ini mit allen 4 gepatchten
Discs; Umlaut-Signatur im laufenden VRAM gefunden (Font geladen).
Nicht weitergeben (enthaelt uebersetzten Spielcode).

## INTRO-FIX + MOVIE-FONT (2026-11-11)

- Movie-Untertitel nutzen eigene FNT-Dateien (g_movieFntTable,
  EVT000_x.FNT etc.), nicht ASCII.CGZ; dort gibt es keine Umlaut-
  Slots. Deshalb EVT-Texte wieder auf ae/oe/ue/ss zurueckgestellt
  (Backup-Map), alle Discs neu gepatcht; verify_evt 0.
- 31 kuratierte Intro-Korrekturen in _tools/fix_evt_intro.py
  (u.a. "Die Ueberlebenden leben in / Angst vor Biowaffen, /
  die alte Technik schuf.", "Waffen aus den / schlafenden Ruinen",
  "Die Kaempfe wurden episch.", "Des Reiches Hauptstadt.",
  "Die Akademie meldete: Die / unterirdischen Ruinen entstanden /
  mit unbegreiflicher Technik.", "Kein gewoehnlicher Mischling!",
  "Zastava, lass sie.", "Beeil dich! Die Flotte", "Sie gesehen?",
  "Wirklich?", "Renn! Schnell weg!").
- Distribution neu: pzp 596041 B; EXE 12 759 120 B
  SHA1 8d6b3affe49bf23e; selftest=0; check-only Disc1=0.
- Recompile-Testbuild _work/recompile_test neu (4 Discs);
  Font-Testbuild _work/font_test_build neu (Schriftprobe im
  Namensbildschirm, EVT-Fixes enthalten).

## EVT-VOLLPRUEFUNG ALLER FILME (2026-11-11)

- Alle 825 MOVIE.DAT-Untertitel in Filmreihenfolge (47 Filme)
  gelesen und geprueft; 85 kuratierte Korrekturen in
  _tools/fix_evt_all.py (EN-Key -> DE), Laengenbudget geprueft.
- Beispiele: "Herrscht der Turm, dann wird / die Welt unser.",
  "Zerquetscht ihn vor seiner Ankunft.", "Du lebst... ich sah
  dich fallen.", "Spezialkraefte des Reichs...", "Hoerte von
  einem Offizier, / der die Flotte fuehrt...", "Goetter, waeren
  diese Leute / nicht zerfetzt worden / im Fressrausch.",
  "Sie glauben, Drachen sind / Daemonen der Hoelle, / die die
  Vorzeit zerstoerten.", "Sagen verdreht man, damit / Menschen
  ihre Retter fuerchten?", "Kaum zerstoerbar: / der Turm von
  aussen.", "Ich riskiere es nicht, / weil es vor tausend /
  Jahren Pflicht war.", "Ich zerstoere den Turm!",
  "Nicht mit mir!", "Ich bin die Einzige...".
- EVT-Karte: 0 Umlaut-Slots, 815 eindeutige Keys, 825 Strings
  abgedeckt; alle Discs neu gepatcht; verify_evt TOTAL 0.
- Gates: verify_full 20939/0/0; e128 696 differ=0; menu 0.
- Distribution: pzp 595765 B; EXE 12 758 636 B
  SHA1 74411649ef58c2a9; selftest=0; check Disc1=0.
- Recompile-Testbuild und Font-Testbuild neu gebaut.

## HAUPTTEXT-UMLAUTE ZURUECKGENOMMEN (2026-11-11)

- Befund: Der EU-Textrenderer nutzt fuer Dialoge/Menues nicht den
  gepatchten ASCII.CGZ-Font; die Slot-Zeichen ^ | ~ { wurden
  falsch/leer dargestellt. Darum _tools/revert_umlauts.py:
  2071 Zeilen zurueck auf ae/oe/ue/ss, 6355 Disc-Slots gepatcht.
- Haupttext und FMV sind damit wieder sauber lesbar (keine
  Platzhalter). Der ASCII.CGZ-Font-Patch bleibt im Image, wird
  aber von den Texten nicht mehr verwendet.
- EVT-Korrekturen (85 + 31 Intro) bleiben aktiv (ae/oe/ue/ss).
- Untranslated-Scan der extrahierten Texte: nur 30 englische
  Zeilen, u.a. Debug-Labels (Disp Collision, light :, D Unit 01)
  und Namen (Light Wing); "PRESS START BUTTON" ist eine Grafik.
  Fuer konkrete sichtbare Resttexte fehlt ein Beispiel/Screenshot.
- Gates: verify_full 20939/0/0; e128 696/0; menu 0; evt 0.
- Distribution: pzp 592549 B; EXE 12 755 611 B
  SHA1 fcb73027a19652c3; selftest=0; check Disc1=0;
  Recompile-Testbuild neu.

## FONT-ANALYSE + UMLAUTE + FEHLENDE TEXTE (2026-11-11)

Analyse des EU-Kernels (mit --keep-intermediate und zusaetzlich
eingetragenen Funktions-Entrys in symbols/overlay_entries_MK-81307_*.txt):
- Text wird als VDP2-Tilemap gezeichnet. Schrift liegt in ASCII.CGZ,
  entpackt nach 0x25E00000; Nametabelle 0x25E06000.
- Zwei Renderer: f_060243E2 (8x8, Musterbasis 3) und f_06024460
  (8x16, Musterbasis 0x63, 2 Muster/Zeichen). Dialoge/TWN/Menue nutzen
  den 8x16-Renderer (f_06024866 -> f_06024460).
- Umlaut-Slots im 8x16-Font: ae=^ oe=| ue=~ ss={ ; NEU: Ae=` Oe=[ Ue=]
  (Grossbuchstaben, 2 Zeilen kuerzer + Punkte).
- _tools/umlautize_texts.py: Escape-Bug behoben (CSV "\\n" <-> 0x0A);
  Grossbuchstaben-Umlaute aktiviert.
- _tools/sync_texts.py: gleicht alle CSV-Zeilen mit den Discs ab und
  setzt dabei die Slots um (Disc autoritativ).
- verify_full 20939/0/0; e128 696/0; menu 0; evt 0.

Nachtraeglich uebersetzte, bisher englische Texte (_tools/extra_de.py,
339 Stellen in 46 Dateien):
- CHILDMP.MCB: Speichern/Laden, Item-Beschreibungen (BP +50 usw.)
- TWN_RUIN.PRG: "About Gash"/"About Azel" -> Ueber Gash/Azel
- E021.EPK: Gash-Dialog + Schlachtschiff-Szenen
- CADRO.MCB/FLD_B6.MCB: Kaiser-Bericht (12 Teile)
- FLD_C4_6.MCB/CAMPOBJ.MCB: Turm-Dialoge
- MENUEN.FNT: Bestiarium-Saetze
- BTL_*: Kampf-Zwischenrufe
- FLD_A5/CARASCR: Karawanen-Prompts, Sandfalle
- Abschlusstexte (A3BGM1_2.SEQ), MENUBK/TITLE

Distribution: pzp 599645 B; EXE 12763349 B
SHA1 efa2d8289ea5bd63; selftest=0; check Disc1=0.

Offen: weitere englische Resttexte (Scan _tools/english_only.py),
kleine 8x8-Debug-Schrift ohne Umlaute, FMV-Untertitel bleiben ae/oe/ue.

## ABSCHLUSS-UPDATE (2026-11-11, spaeter)

- Der 8x16-Font hat jetzt auch Gross-Umlaute: Ae=` Oe=[ Ue=].
  _tools/make_umlauts.py erzeugt sie (2 Zeilen kuerzer + Punkte).
- _tools/umlautize_all.py setzt ae/oe/ue/ss in Textdateien auf Slots um
  (Whitelist: MENU.SCB, CHILDMP.MCB, FLD_C4_6.MCB, FLD_D2.FNT,
  FLD_A5.MCB, BTL_A53.FNT, FLD_A7.FNT). MOVIE.DAT ist ausgenommen.
- WICHTIG: fs_records_all.csv hat fuer einige Namen falsche LBA/Size
  (z.B. MERUKABA.MCB -> zeigt auf MOVIE.DAT; MENU.SCB, CHILDMP.MCB,
  FLD_* weichen vom ISO-Record ab). Die Textbank-Offsets funktionieren,
  aber MERUKABA.MCB darf nicht angefasst werden (sonst EVT kaputt).
- EVT-Untertitel danach erneut mit patch_evt_subtitles.py gesetzt.
- Fehlende Uebersetzungen: _tools/extra_de.py (168 EN->DE), angewendet
  mit _tools/patch_extra.py (339 Stellen) + _tools/umlautize_extra.py.
- Gates: verify_full 20939/0/0; e128 696/0; menu 0; evt 0.
- Distribution: pzp 614733 B; EXE 12778121 B
  SHA1 74eb9bcc88421c4e; selftest=0; check Disc1=0.

## UNTERTITEL-FONT GEKLAERT (2026-11-16)

Quelle: yaz0r/Azel VDP2.cpp (printVdp2String):
  r11 = (printVdp2StringTable[palette] << 12) + 0x63
  Name-Table-Eintrag = r11 + (char-0x20)*2  (+1 fuer die zweite Zeile)
D.h. die Untertitel benutzen DENSELBEN 8x16-Font aus ASCII.CGZ wie die
Dialoge. Der "duenne" Look entsteht erst in createTextSpriteTask /
loadCharacterToVdp2, das aus den 4bpp-Glyphen eine 1bpp-Kontur fuer die
VDP1-Textur rechnet. Die EVT-*.FNT der Filme sind Kanji (JP-Rest) und
werden fuer den lateinischen Text nicht gebraucht.

Folge: EVT-Untertitel auf dieselben Slots umgestellt
(_tools/umlautize_evt.py): 172 Zeilen, alle 4 Discs neu gepatcht,
verify_evt 0. Bsp.: "Die ]berlebenden leben in", "Genie{e den Frieden",
"Zur n^chsten Phase...".

Gates: verify_full 20939/0/0; e128 696/0; menu 0; evt 0.
Distribution: pzp 614937 B; EXE 12779035 B SHA1 02170c1d5b40d5cf;
selftest=0; check Disc1=0.

## KERNEL-TEXTE + RECOMPILE-BUILD (2026-11-16)

Sichtbar waren noch englische Texte im Titel-/Lade-/Speichermenue. Sie
liegen im Kernel (1ST_READ.PRG) als Null-terminierte String-Tabelle,
Disc-unabhaengig identisch:

  0x3D2C0..0x3D5A0  Save-/Load-Dialog + Gebietsnamen
  (Save Game to..., You may save..., Location:, Will erase..., Saving:...,
   Not enough space..., NO DATA, NO BLOCK, The data has been saved.,
   Cannot be saved..., Load Game From..., Not used, Load Game,
   It is incorrect data., Above the Excavation, Excavation Site, Camp,
   Valley, Village of Cainus, Garil Desert, Caravan, Forbidden Zone,
   Village of Zoah, Imperial Air Force, Air Force Post, The Tower,
   Uru Underground Ruins, Forest of Zoah, Seekers' Stronghold)
  0x3D8A0/0x3D8B4  "PRESS START BUTTON" -> "START DR~CKEN"

_tools/patch_kernel_strings.py ersetzt die Tabelle (inkl. Font-Slots fuer
Umlaute, 0x00-Padding, Laengenbudget geprueft) auf allen 4 Discs;
_tools/restore_kernel.py stellt den Original-Kernel aus Original_CD*/Track 1
wieder her. _tools/diff_kernel.py bestaetigt: alle Diffs liegen nur in
0x3D000..0x3DA00.

WICHTIG - Recompile-Runtime erkennt geaenderte Programme:
  "disc: 1ST_READ.PRG is not a known version, running without the
   hand-written functions"
Ohne die hand-geschriebenen Funktionen haengt der Boot (Loop bei 0x600C650,
slaveWait/Slave-CPU-Handshake) -> schwarzes Bild bei 60 fps.
Der Runtime vergleicht SHA-256 von 1ST_READ.PRG und aller Module mit
Tabellen, die im Builder stecken:

  builder.exe                    Manifest product/version/area/disc/module
  runtime/lib/libpds_runtime.a   dasselbe Manifest + eingebettete Kopie
                                 von symbols/port_symbols.txt (kernel <sha>)

_tools/patch_builder_manifest.py traegt die Hashes der gepatchten Discs
dort ein (idempotent). Danach baut

  pdt-recompile-builder-2.0.0-win64\builder.exe --disc _work\patched_discN.cue ... --out _build\pds-recompile-de

wieder "Enhancements on in 59 of 59" (vorher 0) und der Boot laeuft normal.
Achtung: vor dem Rebuild laufende pds-recompile.exe beenden (sonst
"Linking failed: Permission denied").

Ergebnis (Screenshots _work/review_fixes/km_*.png):
  Titel: "START DRÜCKEN" (Slot ~ = ue)
  Titelmenue: "WEITER"
  Lade-Menue: "Spielstand aus Intern-RAM", "LEER", "Ort: über der Ausgrabung"

Gates: verify_full 20939/0/0; e128 696/0; menu 0; evt 0.
Distribution: pzp 615398 B; EXE 12777990 B SHA1 f18a0bacfda1f34d;
selftest=0; check Disc1=0.

## UNTERTITEL-SICHTPRUEFUNG (2026-11-16)

Frischer Lauf (kein Savestate - States sind nach Kernel-Aenderung
ungueltig, weil sie den Kernel-Hash enthalten):
  -p 600:start -p 1200:start   -> Titelmenue "WEITER"
  -p 1700:right                -> "NEUES SPIEL" (horizontales Scrollmenue)
  -p 2200:start                -> NEUES SPIEL bestaetigt, Opening-Cutscene

Watcher (_tools/subwatch.ps1, subwatch2/3.ps1) mit engem Untertitelband
(0.84-0.94 der Fensterhoehe) und Helligkeits-Score. Gesehen:
  "Wer viele Fragen stellt,"   (_work/subwatch/f0041.jpg)
  "Eine Frage, Rhua."          (_work/subwatch/f0015.jpg)
  "Arwen, nun ist die Zeit zum Aufstand."
  "Willst du es wissen?"       (kein Umlaut enthalten - erste Deutung war falsch)
                                  (_work/subwatch/f0022.jpg)

  "Ort: ]ber der Ausgrabung"   <-- zwei WEISSE Punkte ueber dem u, Lade-Menue
                                  (_work/review_fixes/zoom_ueber_new2.png)
  Untertitel nutzen denselben Glyphensatz (ASCII.CGZ, 8x16) wie Dialog/Menue -
  der Menue-Nachweis gilt damit auch fuer die Movie-Untertitel.

## FONT-BUG: UMLAUTPUNKTE WAREN SCHWARZ (2026-11-16)

Rueckmeldung: Umlaute waren im Spiel sichtbar, aber ohne Punkte.

Ursache: Im 4bpp-Font (ASCII.CGZ, 8x16 ab 0xC60) ist
  0xF = schwarze Kontur
  0x8 = hellste Fuellung (0x9..0xE = Zwischenstufen)
Die zuerst gebauten Umlaut-Glyphen zeichneten die Punkte komplett mit 0xF
=> Punkte schwarz, auf dunklem Grund unsichtbar. Dasselbe galt fuer das
erste ss-Glyph (nur 0xF) - es war ein schwarzer Fleck.

Fix: _tools/font_build_de.py baut die 7 Glyphen neu aus dem ORIGINAL-Font
(_work/ascii_cgz/font_orig_real.raw, entpackt aus real_disc1.cgz):
  - Kleinbuchstaben a/o/u + zwei 2x2-Punkte (0x8) in Zeile 0/1,
    Spalten 1-2 und 4-5
  - Grossbuchstaben A/O/U um 2 Zeilen gekuerzt (A: Zeile 11/12,
    O/U: Zeile 7/8), Punkte in Zeile 0/1, Spalten 1-2/5-6
  - ss: B-Koerper (Zeilen 2..15) + hoher Stamm (Zeilen 0/1)
Danach _tools/font_patch.py (packt ASCII.CGZ neu, alle 4 Discs,
ISO-Groesse wird mitgeschrieben).

Sichtpruefung:
  Titel: "START DRÜCKEN" (Punkte sichtbar)
  Lade-Menue: "Ort: über der Ausgrabung" (ue mit zwei weissen Punkten,
    _work/review_fixes/zoom_ueber_new2.png)
  Glyphen-Vorschau: _work/review_fixes/design_final.png

Hinweis: Der grosse Titelmenue-Text ("WEITER"/"NEUES SPIEL") ist eine
Grafik, kein String (kein "WEITER" in Kernel/COMMON.DAT/TITLE.PRG).
Die Schriftprobe im Namen-Bildschirm (FLD_D5.FNT) ist per
_tools/make_font_test.py erreichbar, braucht aber den langen Intro-Weg.

Nachtrag: Untertitel-Sichtbeweis nach dem Font-Fix (frischer Lauf,
-p 600:start -p 1200:start -p 1700:right -p 2200:start, Watcher
_tools/subwatch4.ps1 mit Mittelwert-Schwelle):
  "Zu stark fuer uns!"   -> ue mit zwei weissen Punkten
       (_work/review_fixes/zoom_sub_fuer.png, hit_000.jpg)
  "Sie ist schoen,"      -> oe mit Punkten
  "Ein Maedchen."        -> ae mit Punkten
Kontaktabzug aller Untertitel: _work/review_fixes/contact_sub_final.png

Wichtig fuer kuenftige Watcher: Untertiteltext ist leicht gelblich, ein
Schwellwert auf alle drei Kanaele (R,G,B > 180) faellt durch (B oft < 180).
Besser Mittelwert > 140.

## PATCHER-GUI MODERNISIERT (2026-11-16)

_tools/pds_deutsch_patcher_gui.py komplett neu aufgebaut (tkinter/ttk,
weiter ohne Zusatzabhaengigkeiten, PyInstaller-onefile bleibt):

- Header mit Logo, Titel, Untertitel, Badges (4 Discs / PAL-EU V1.000)
- Disc-Karten statt Formularzeilen: Nummer, Dateiname (gekuerzt),
  Groesse + Ordner, Status-Chip (● Original-Abbild okay / fertig /
  bereits gepatcht / Fehler), Waehlen/Entfernen
- Patch-Karte mit BEREIT/FEHLT-Badge und Regionenzahl
- Modus als Segment-Control (Direkt ersetzen / Neue Dateien schreiben);
  Zielordner + .cue-Option erscheinen nur im Kopiermodus
- Primaerbutton als runder Canvas-Button (Hover, Disabled), Text
  wechselt zu "Nur pruefen"
- Deterministische Fortschrittsanzeige (Discs), Statuszeile
- Protokoll mit Farb-Tags (ok/warn/err/head), eigener Systemzeile
- High-DPI-aware, Fenster merkt sich letzten Ordner/Modus
  (%LOCALAPPDATA%\PDS_Deutsch_Patcher\settings.json)
- Shortcuts: F5 = Status pruefen, Strg+Enter = Start
- CLI-Flags und --selftest unveraendert; EXE weiterhin eigenstaendig

Geprueft: GUI-Selftest ok, EXE-Selftest 0, --check-only Disc1 = 0,
Testlauf im GUI (nur pruefen, Disc 1) zeigt gruenen Status + Protokoll.
Screenshots: _work/review_fixes/gui_final5.png, gui_final_check2.png
EXE: 12.910.190 B, SHA1 b643f8b5e608b39c (Patch-Datei unveraendert).

## ANLEITUNG.TXT KORRIGIERT (2026-11-16)

- Datei war CP1252 und zeigte in UTF-8-Werkzeugen Fragezeichen ->
  jetzt UTF-8 mit BOM + CRLF (Notepad/VS Code/EXE-Anzeige korrekt).
- Version 2.3 (2026-11-16).
- Veraltete GUI-Beschreibung ersetzt: Patch-Karte zeigt
  "pds_deutsch_patch.pzp" + "eingebaut in dieser EXE", Button
  "Andere Datei...", Systemzeile unten mit "Python pruefen" /
  "Python installieren"; Status-Chip "fertig" ergaenzt; F5/Strg+Enter.
- Echte Meldungen uebernommen: "GEPATCHT UND GEPRUEFT: OK"
  (vorher faelschlich GEPRUEFT mit Umlaut), "Groesse passt nicht",
  "X von Y Textbloecken passen nicht (CRC)", "Nachpruefung
  fehlgeschlagen", "*.original.bak existiert bereits".
- Festplattenplatz korrigiert: ca. 2,5 GB Standard / ca. 5 GB mit
  Kopiermodus (vorher pauschal 3 GB).
- Umlaut-Kapitel richtiggestellt: echte ae/oe/ue/AE/OE/UE/ss-Glyphen
  auch in FMV-Untertiteln (gleicher Font); der alte Hinweis
  "Gross-Umlaute als Ae/Oe/Ue" und "Movie-Font ohne Umlaute" war falsch.
- Abdeckungszahlen aktualisiert: 4.795 Bloecke gesamt
  (1.100-1.300 pro Disc), 400-490 KB pro Disc, 0,06-0,08 %.
- build_exe.py kopiert jetzt pds_deutsch_patcher_gui.py und
  apply_patch_file.py -> _dist/pds_deutsch_patcher.py bei jedem Build
  (die GUI-Kopie in _dist war veraltet).
- EXE neu gebaut (Anleitung eingebettet): 12.910.243 B,
  SHA1 db68fa62ea3bff42, selftest=0, check Disc1=0, eingebettete
  ANLEITUNG.txt identisch mit _dist (SHA1 44261c42160a7d3a).
