# End-to-end verification: re-parse MOVIE.DAT from the PATCHED disc images
# using the same FS/record/pointer logic as the original dump, then compare
# every string against the DE map. This proves the subtitle system is
# structurally intact and fully German after in-place patching.
import json
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PY = sys.executable

# 1) fresh dumps of the patched discs
for d in (1, 2, 3, 4):
    out = '_work/evt_offsets_patched_disc%d.json' % d
    r = subprocess.run([PY, '_tools/dump_evt_string_offsets.py',
                        '--iso', '_work/patched_disc%d.bin' % d,
                        '--out', out, '--disc', str(d)],
                       capture_output=True, text=True)
    tail = '\n'.join(r.stdout.strip().splitlines()[-3:])
    print('disc %d dump rc=%d: %s' % (d, r.returncode, tail.replace('\n', ' | ')))
    if r.returncode != 0:
        print(r.stderr[-2000:])
        sys.exit(1)

# 2) load the DE map
de_map = {}
for line in open('_work/evt_de_map.csv', encoding='latin1'):
    line = line.rstrip('\r\n')
    if not line or line.startswith('#'):
        continue
    en, de = line.split(';', 1)
    de_map[en] = de

# 3) round-trip: pair ORIGINAL dump records (EN) with PATCHED dump records
#    (same offsets, in order) and verify each patched string equals the
#    mapped DE value for the original EN key.
total_bad = 0
for d in (1, 2, 3, 4):
    jorig = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    jpat = json.load(open('_work/evt_offsets_patched_disc%d.json' % d, encoding='utf-8'))
    o = [e for e in jorig['entries'] if e['src'].startswith('MOVIE.DAT')]
    p = [e for e in jpat['entries'] if e['src'].startswith('MOVIE.DAT')]
    prg = len(jpat['entries']) - len(p)
    if len(o) != len(p):
        print('disc %d: RECORD COUNT MISMATCH orig=%d patched=%d' % (d, len(o), len(p)))
        total_bad += abs(len(o) - len(p))
    bad_off = bad_txt = no_key = same = 0
    for oe, pe in zip(o, p):
        if oe['foff'] != pe['foff']:
            bad_off += 1
            if bad_off <= 3:
                print('  d%d OFFSET DRIFT: orig foff=%d patched foff=%d'
                      % (d, oe['foff'], pe['foff']))
            continue
        en, dtxt = oe['text'], pe['text']
        if en not in de_map:
            no_key += 1
            if no_key <= 3:
                print('  d%d ORIGINAL KEY NOT IN MAP: %r' % (d, en))
            continue
        if dtxt != de_map[en]:
            bad_txt += 1
            if bad_txt <= 5:
                print('  d%d TEXT MISMATCH @foff=%d: expected %r got %r'
                      % (d, oe['foff'], de_map[en], dtxt))
        if dtxt == en:
            same += 1  # legit: proper nouns / punctuation-only strings
    print('disc %d: MOVIE records=%d, PRG strings=%d, offset-drift=%d, '
          'text-mismatch=%d, no-key=%d, DE==EN(proper nouns)=%d'
          % (d, len(p), prg, bad_off, bad_txt, no_key, same))
    total_bad += bad_off + bad_txt + no_key

print('TOTAL PROBLEMS:', total_bad)
