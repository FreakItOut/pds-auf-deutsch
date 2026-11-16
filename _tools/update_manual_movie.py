# -*- coding: utf-8 -*-
import io

p = '_dist/ANLEITUNG.txt'
s = io.open(p, encoding='cp1252').read()
needle = ('   daher bei dieser Schreibweise.')
add = ('   In den FMV-Zwischensequenzen bleiben die Untertitel bei\n'
       '   "ae/oe/ue/ss", weil der dortige Movie-Font keine Umlaut-\n'
       '   Zeichen enthält.')
if 'Movie-Font keine Umlaut' not in s:
    s = s.replace(needle, needle + '\n' + add, 1)
io.open(p, 'w', encoding='cp1252', newline='').write(s)
print('ok', 'Movie-Font keine Umlaut' in s)
