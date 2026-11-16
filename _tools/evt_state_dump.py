# dump current disc German text for MOVIE.DAT groups (given EN from evt_offsets_discN.json)
import json
import sys
sys.stdout.reconfigure(encoding='latin1')

dnum = int(sys.argv[1]) if len(sys.argv) > 1 else 1
gfilter = sys.argv[2] if len(sys.argv) > 2 else None

BIN = '_work/patched_disc%d.bin' % dnum

j = json.load(open('_work/evt_offsets_disc%d.json' % dnum, encoding='utf-8'))
jp = json.load(open('_work/evt_offsets_patched_disc%d.json' % dnum, encoding='utf-8'))
ents = j['entries']

# group by src
groups = {}
for e in only_ent if False else ents:
    groups.setdefault(e['src'], []).append(e)

f = open(BIN, 'rb')


def read_at(abs_off, n):
    f.seek(abs_off)
    return f.read(n)


def read_str(abs_off):
    # read up to 120 bytes, cut at first NUL
    b = read_at(abs_off, 160)
    end = b.find(b'\x00')
    if end < 0:
        end = len(b)
    return b[:end].decode('latin1', 'replace')


sel = [k for k in groups if (gfilter is None or gfilter in k)]
for src in sorted(sel, key=lambda s: int(s.split('g')[1]) if 'g' in s else 0):
    print('=====', src)
    prev_en = ''
    for e in groups[src]:
        if e['src'] != src:
            continue
        cur = read_str(e['off'])
        print('%8d EN=%r' % (e['foff'], e['text']))
        print('           DE=%r' % cur)
