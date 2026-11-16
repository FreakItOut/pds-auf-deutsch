# -*- coding: utf-8 -*-
"""Konvertiert ANLEITUNG.txt nach UTF-8 mit BOM + CRLF und prueft Inhalte."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
p = '_dist/ANLEITUNG.txt'
s = io.open(p, encoding='utf-8').read()
s = s.replace('\r\n', '\n').replace('\n', '\r\n')
io.open(p, 'w', encoding='utf-8-sig', newline='').write(s)

b = open(p, 'rb').read()
print('BOM:', b[:3] == b'\xef\xbb\xbf', '| Bytes:', len(b))
s = io.open(p, encoding='utf-8-sig').read()
for line in s.splitlines()[:6]:
    print(line)
for key in ('ä, ö, ü, Ä, Ö, Ü und ß', 'GEPATCHT UND GEPRUEFT',
            '1.100–1.300', 'ca. 2,5 GB', 'eingebaut in dieser EXE'):
    print('%-32s %s' % (key, key in s))
