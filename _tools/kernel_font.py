# -*- coding: utf-8 -*-
import struct
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader

sys.stdout.reconfigure(encoding='latin1')
iso = ISO9660Reader('_work/patched_disc1.bin')
files = iso.list_files()
for f in files:
    if f['name'].upper().endswith('COMMON.DAT'):
        print(f)
        data = iso.extract_file(f['lba'], f['size'])
        open('_work/review_fixes/common_real.bin', 'wb').write(data)
        print('size', len(data), 'head', data[:16].hex(' '))
        off = 0x010E98
        if len(data) > off + 16:
            cnt = struct.unpack('>H', data[off:off + 2])[0]
            typ = struct.unpack('>H', data[off + 2:off + 4])[0]
            print('kernel font count', cnt, 'type', typ)
            from PIL import Image
            gsize = 32
            cols = 16
            rows = (cnt + cols - 1) // cols
            scale = 2
            cell = 16 * scale + 2
            img = Image.new('RGB', (cols * cell, rows * cell), (0, 0, 0))
            base = off + 16
            for g in range(cnt):
                for y in range(16):
                    o = base + g * gsize + y * 2
                    v = (data[o] << 8) | data[o + 1]
                    for x in range(16):
                        if v & (1 << (15 - x)):
                            cx = (g % cols) * cell
                            cy = (g // cols) * cell
                            for sy in range(scale):
                                for sx in range(scale):
                                    img.putpixel((cx + x * scale + sx,
                                                  cy + y * scale + sy),
                                                 (230, 230, 230))
            img.save('_work/review_fixes/kernel_font.png')
            print('sheet saved')
