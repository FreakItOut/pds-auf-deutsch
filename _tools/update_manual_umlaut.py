# -*- coding: utf-8 -*-
import io

p = '_dist/ANLEITUNG.txt'
s = io.open(p, encoding='cp1252').read()
start = s.find('Zusätzlich: Die Spieldaten auf der Disc')
end = s.find('zur Verfügung steht.', start)
if start < 0 or end < 0:
    raise SystemExit('Absatz nicht gefunden')
end += len('zur Verfügung steht.')
new = """e) UMLAUTE IM SPIEL
   Diese Fassung enthält echte Umlaut-Glyphen (ä, ö, ü) und ein
   scharfes ß direkt im Spiel-Font. Innerhalb von Wörtern sehen
   die Texte dadurch sauber aus (z. B. "Tür", "für", "schön",
   "Straße"). Großbuchstaben mit Umlaut (Ä, Ö, Ü) werden weiterhin
   als "Ae", "Oe", "Ue" geschrieben, weil der Originalsatz dafür
   keine eigenen Groß-Glyphen besitzt; am Wortanfang bleibt es
   daher bei dieser Schreibweise."""
s = s[:start] + new + s[end:]
io.open(p, 'w', encoding='cp1252', newline='').write(s)
print('ersetzt; Laenge', len(s))
