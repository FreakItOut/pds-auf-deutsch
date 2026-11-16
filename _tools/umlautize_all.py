# -*- coding: utf-8 -*-
"""Setzt ae/oe/ue/ss in allen null-terminierten ASCII-Texten der Discs
auf Font-Slots um (nur wenn der Text deutsch aussieht)."""
import csv as _csv
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'

import umlaut_conv as U  # noqa: E402  (Konverter wiederverwenden)

SKIP_EXT = ('.PNB', '.CGB', '.SND', '.PCM', '.WAV', '.MOV', '.CPK',
            '.ADX', '.SEQ', '.EXB', '.BDB')
U_PRINT = re.compile(rb'[\x20-\x7e\x0a]{4,}')
WHITELIST = {
    'MENU.SCB', 'CHILDMP.MCB', 'FLD_C4_6.MCB',
    'FLD_D2.FNT', 'FLD_A5.MCB', 'BTL_A53.FNT', 'FLD_A7.FNT',
}
EN = re.compile(r"\b(the|you|your|and|that|with|have|this|what|are|is|"
                r"was|were|will|would|from|they|there|their|them|then|"
                r"than|into|can|not|for|but|all|his|her|she|him|one|out|"
                r"about|could|should|when|where|which|who|why|how|any|"
                r"some|just|only|very|more|most|now|again|still|also|"
                r"back|down|off|over|after|before|because|if|so|no|yes|"
                r"do|does|did|been|get|got|make|made|take|come|came|"
                r"know|think|see|look|say|said|tell|told|give|find|found|"
                r"want|need|must|may|might|shall|us|we|me|my|our|its)\b",
                re.I)

recs = list(_csv.DictReader(open('_work/fs_records_all.csv',
                                 encoding='latin1'), delimiter=';'))
changes = 0
files = {}
for disc in (1, 2, 3, 4):
    with open('_work/patched_disc%d.bin' % disc, 'rb') as f:
        for r in recs:
            name = r['name']
            if name.upper().endswith(SKIP_EXT):
                continue
            if WHITELIST and name not in WHITELIST:
                continue
            if not (r['lba'].isdigit() and r['size'].isdigit()):
                continue
            lba, size = int(r['lba']), int(r['size'])
            if lba == 0 or size == 0 or size > 4 * 1024 * 1024:
                continue
            key = (disc, name)
            if key not in files:
                out = bytearray()
                need, s = size, lba
                while need > 0:
                    f.seek(s * SECT + 16)
                    c = f.read(min(DATA, need))
                    if not c:
                        break
                    out += c
                    need -= len(c)
                    s += 1
                files[key] = [lba, bytearray(out[:size])]
            data = files[key][1]
            # zusammenhaengende druckbare Bereiche
            for m in U_PRINT.finditer(data):
                pos, e = m.start(), m.end()
                seg = data[pos:e]
                if 4 <= len(seg) <= 600:
                    try:
                        t = seg.decode('latin1')
                    except Exception:
                        t = ''
                    if (t and all(c == '\n' or 32 <= ord(c) < 127 for c in t)
                            and sum(c.isalpha() for c in t) >= 4
                            and len([m for m in EN.findall(t)
                                     if m == m.lower()]) < 2):
                        new = U.convert_text(t)
                        if new != t:
                            nb = new.encode('latin1')
                            if len(nb) <= len(seg):
                                changes += 1
                                if MODE == 'apply':
                                    data[pos:pos + len(nb)] = nb
                                    fill = pos + len(nb)
                                    for k in range(fill, e):
                                        data[k] = 0x00 if k == fill else 0xFF
if MODE == 'apply':
    for (disc, name), (lba, data) in files.items():
        with open('_work/patched_disc%d.bin' % disc, 'r+b') as f:
            for k in range((len(data) + DATA - 1) // DATA):
                f.seek((lba + k) * SECT + 16)
                f.write(data[k * DATA:(k + 1) * DATA])
print('changes=%d files=%d mode=%s' % (changes, len(files), MODE))
