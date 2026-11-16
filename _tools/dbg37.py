# debug uid37 CAMP: show csv row, offsets, disc actuals per disc, plus hexdump
import sys

sys.stdout.reconfigure(encoding='latin1')
csvline = [l for l in open('_work/subtitles/TWN_CAMP_PRG_de.csv',
                           encoding='latin1') if l.startswith('37;')]
print('csv:', repr(csvline))
if csvline:
    p = csvline[0].rstrip('\n').split(';')
    print('uid=%s off3=%r en=%r de=%r' % (p[0], p[3], p[4], p[5]))
    offs = [int(x) for x in p[3].split('|') if x] or [int(p[2])]
    print('offs:', offs)
    SECT, DATA = 2352, 2048
    for d in (1, 2, 3, 4):
        import csv as _c
        fs = ('_work/fs_records_all.csv' if d == 1
              else '_work/fs_records_cd%d.csv' % d)
        idx = {r['name']: (int(r['lba']), int(r['size']))
               for r in _c.DictReader(open(fs, encoding='latin1'),
                                      delimiter=';') if int(r['lba']) > 0}
        lba, size = idx['TWN_CAMP.PRG']
        with open('_work/patched_disc%d.bin' % d, 'rb') as f:
            need, s = size, lba
            out = bytearray()
            while need > 0:
                f.seek(s * SECT + 16)
                c = f.read(min(DATA, need))
                out += c
                need -= len(c)
                s += 1
        for o in offs:
            e = o
            while e < len(out) and out[e] not in (0x00, 0xFF):
                e += 1
            hexd = ' '.join('%02X' % b
                            for b in out[max(0, o - 12):o + 2])
            print('d%d off=%d val=%r hexbefore=%s' % (d, o,
                                                      out[o:e].decode('latin1'),
                                                      hexd))
