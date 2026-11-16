import sys, glob, csv
sys.stdout.reconfigure(encoding='latin1')
pool = {}
for fn in glob.glob('_work/subtitles/*_de.csv'):
    if 'E128' in fn:
        continue
    for ln in open(fn, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[5].strip():
            pool.setdefault(q[4], (q[5], fn.split(chr(92))[-1]))
for fn in glob.glob('_work/menu_de/*_map.csv'):
    for ln in open(fn, encoding='latin1'):
        ln = ln.rstrip('\r\n')
        if ';' not in ln or ln.startswith('#'):
            continue
        en, de = ln.split(';', 1)
        if de.strip() and not en.startswith('#'):
            pool.setdefault(en, (de, fn.split(chr(92))[-1]))
try:
    rd = csv.reader(open('_work/evt_de_map.csv', encoding='latin1'), delimiter=';')
    header = next(rd, None)
    print('evt_de_map header:', header)
    for r in rd:
        if len(r) >= 2 and r[1].strip():
            pool.setdefault(r[0], (r[1], 'evt_de_map.csv'))
except Exception as ex:
    print('evt_de_map err:', ex)
test = ['Thanks! In return...', 'tell him?', "Take it. You've earned it.", 'Gash...',
        'Heh heh heh...', 'Worm tunnels, subterranean', 'Well,', 'Edge!', 'Mel-Kava?',
        'If we destroy Mel-Kava,', '(%a1 is recovering...)']
for t in test:
    hit = pool.get(t)
    print(('HIT %r -> %r' % hit) if hit else 'MISS %r' % t)
# how many of the 207 kept-en keys exist in pool?
n = hit_n = 0
for l in open('_work/menu_de/TUTORIAL_CGB_de.csv', encoding='latin1'):
    q = l.rstrip('\r\n').split(';')
    if len(q) < 6:
        continue
    if q[5].strip() == q[4].strip() and len(q[4].strip()) >= 4:
        n += 1
        if q[4].strip() in pool:
            hit_n += 1
print('kept-en rows %d, pool-hit %d' % (n, hit_n))
