# Panzer Dragoon Saga – Deutsche Fassung (Fan-Übersetzung)

Deutsche Textfassung der **PAL-EU-Version** von *Panzer Dragoon Saga*
(Sega Saturn, Discs 1–4).

Der Patcher schreibt die Übersetzung direkt in **eigene BIN/CUE-Abbilder**
der Original-Discs. Es werden keine Spieldaten und keine gepatchten
Images veröffentlicht.

## Status

- Discs 1–4 vollständig übersetzt: Feld- und Stadtdialoge, Menüs, Shops,
  Tutorials, Kampf-Anzeigen, FMV-Untertitel und die Namensauswahl
- Echte Umlaute im Spiel-Font: **ä ö ü Ä Ö Ü ß** (auch in Untertiteln)
- Prüfungen: 20.939 Dialogstrings, 696 Menüzeilen, 825 Untertitel,
  alle Textblöcke per CRC und SHA-1 verifiziert
- Längenregel: jede deutsche Zeile ist höchstens so lang wie das englische
  Original (kein Überschreiben benachbarter Spieldaten)

## Voraussetzungen

- Eigene Original-Discs 1–4 (PAL/Europe), als **rohes BIN/CUE-Abbild**
  (2352 Bytes/Sektor, alle Tracks)
- Windows 10/11 – die EXE braucht kein installiertes Python
- optional: Python 3.8+ für den .py-Weg

## Benutzung

1. Eigene Discs als BIN/CUE auslesen.
2. `PDS_Deutsch_Patcher.exe` starten.
3. „Discs automatisch finden…“ → Status prüfen → „Patch anwenden“.

Die ausführliche Anleitung steht in [`_dist/ANLEITUNG.txt`](_dist/ANLEITUNG.txt).

## Aufbau dieses Repositories

| Ordner | Inhalt |
|---|---|
| `_tools/` | Python-Werkzeuge: Patcher-GUI, CLI, Patch-Bau, Prüfskripte |
| `_project/NOTES.md` | Technische Projektnotizen (Reverse Engineering, Formate) |
| `_dist/ANLEITUNG.txt` | Benutzeranleitung |
| `_dist/sha1_checkliste.txt` | Prüfsummen der Original- und Ziel-Abbilder |

**Nicht im Repository** (siehe `.gitignore`):

- Disc-Abbilder (Original oder gepatcht) und extrahierte Spieldaten
- Laufzeit-Build mit übersetztem Spielcode (`_build/`)
- Fremdwerkzeuge wie der `pdt-recompile-builder`
- die fertige `PDS_Deutsch_Patcher.exe` und `pds_deutsch_patch.pzp`
  (enthalten Spieltext; werden bei Bedarf als GitHub-Release bereitgestellt)

## Wie der Patch funktioniert

Die Patch-Datei enthält nur die deutschen Textbytes, ihre Offsets im
Abbild und je Block eine CRC32. Beim Patchen wird jeder Block geprüft;
danach wird das Ergebnis über die SHA-1 mit dem erwarteten Abbild
verglichen. Passt etwas nicht, wird nichts geschrieben.

## Rechtliches

Dies ist ein **privates Fan-Projekt** ohne Verbindung zu SEGA.

- Nur für den privaten Gebrauch mit der eigenen, legal erworbenen
  PAL-EU-Kopie.
- **Keine** Weitergabe von Original- oder gepatchten Disc-Images.
- *Panzer Dragoon Saga* und alle Marken gehören SEGA. Die Übersetzung
  ist Fan-Inhalt und kein offizielles Produkt.
- Für die frühe Analyse wurde die spanische Fan-Übersetzung
  (Holy_3051, segasaturno.com) untersucht – Danke dafür.

## Danksagung

- yaz0r / Azel-Projekt für die Dokumentation der Spiel-Engine
- pdt-recompile für die Test-Laufzeit (nicht Teil dieses Repos)
