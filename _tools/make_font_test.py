# -*- coding: utf-8 -*-
# Baut einen Font-Test-Discsatz: Namensbildschirm zeigt eine Schriftprobe.
import csv
import os
import shutil

SECT, DATA = 2352, 2048
OUT = '_work/font_test'
os.makedirs(OUT, exist_ok=True)
src = '_work/patched_disc1.bin'
dst = os.path.join(OUT, 'disc1.bin')
if not os.path.isfile(dst):
    shutil.copyfile(src, dst)
    print('kopiert', dst)

# CUE mit absoluten Pfaden fuer die Audio-Tracks
root = os.path.abspath('.')
cue = (
    'FILE "disc1.bin" BINARY\n'
    '  TRACK 01 MODE1/2352\n'
    '    INDEX 01 00:00:00\n'
    'FILE "%s" BINARY\n'
    '  TRACK 02 AUDIO\n'
    '    INDEX 00 00:00:00\n'
    '    INDEX 01 00:02:00\n'
    'FILE "%s" BINARY\n'
    '  TRACK 03 AUDIO\n'
    '    INDEX 00 00:00:00\n'
    '    INDEX 01 00:02:00\n'
) % (
    os.path.join(root, 'Original_CD1',
                 'Panzer Dragoon Saga (Europe) (Disc 1) (Track 2).bin'),
    os.path.join(root, 'Original_CD1',
                 'Panzer Dragoon Saga (Europe) (Disc 1) (Track 3).bin'),
)
open(os.path.join(OUT, 'disc1.cue'), 'w', encoding='latin1',
     newline='\r\n').write(cue)

idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0}
lba, size = idx['FLD_D5.FNT']
need, s = size, lba
data = bytearray()
with open(dst, 'rb') as f:
    while need > 0:
        f.seek(s * SECT + 16)
        c = f.read(min(DATA, need))
        if not c:
            break
        data += c
        need -= len(c)
        s += 1

line1 = b'Schriftprobe: ^ | ~ {'
line2 = b'wie ist dein Name?'
region = line1 + b'\x00' + line2 + b'\x00'
region = region + b'\xff' * (46 - len(region))
assert len(region) == 46
data[11456:11456 + 46] = region

with open(dst, 'r+b') as f:
    for k in range((len(data) + DATA - 1) // DATA):
        f.seek((lba + k) * SECT + 16)
        f.write(data[k * DATA:(k + 1) * DATA])
print('Schriftprobe eingesetzt:', region)
print('cue:', os.path.join(OUT, 'disc1.cue'))
