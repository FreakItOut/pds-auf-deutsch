# Kettenansicht: gruppiert jede TWN-Datei in Dialogketten (EN-Blocksatz)
# und meldet fuer jede Kette die heutige DE-Komposition + Flags.
# usage: python chain_view.py  ->  _work/review_fixes/chain_all.txt
import csv
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')

TERMINAL = ('.', '!', '?', ')')


def unesc(s):
    return s.replace('\\n', '\n').replace('\\t', '\t')


def en_chain_end(en):
    return en.strip().endswith(TERMINAL) or en.strip().endswith('..."')


def ratio_ok(de_total, en_total):
    return len(de_total) / max(len(en_total), 1)


def chain_flags(members):
    f = []
    en_t = unesc(' '.join(m['en'] for m in members))
    de_t = unesc('|'.join(m['de'] for m in members))
    r = ratio_ok(de_t, en_t)
    if r < 0.55 and len(en_t) >= 30:
        f.append('KUERZUNG %.2f' % r)
    # kein DE-Abschluss wo EN-Abschluss
    if en_chain_end(members[-1]['en']) and \
            not de_t.rstrip().endswith(TERMINAL):
        last = de_t.rstrip()[-8:]
        f.append('KEIN-DE-ABSCHLUSS [%s]' % last)
    # haengendes Wort am letzten DE-Block ohne Terminal
    last_words = unesc(members[-1]['de']).split()
    if last_words and last_words[-1].islower() and \
            not unesc(members[-1]['de']).rstrip().endswith(TERMINAL):
        f.append('HAENGT:%s' % last_words[-1][:12])
    # Gross-/Klein nach goes: EN1 ends mid-sentence but DE2 starts upper
    if len(members) >= 2:
        de1 = unesc(members[0]['de']).rstrip()
        de2 = unesc(members[1]['de'])
        if de1 and not de1.endswith(TERMINAL) and \
                de1.endswith('...') is False and de2[:1].isupper():
            f.append('UPPER-START-NACH-LOWCASE')
    # DE-Muster: block endet mit Artikel/waegwort + DE2 unterwaerts
    de1w = re.findall(r'\w+', unesc(members[0]['de']).lower())
    if de1w and de1w[-1] in ('der', 'die', 'das', 'den', 'dem', 'ein',
                             'eine', 'einem', 'einen', 'einer', 'und',
                             'oder', 'aber', 'mit', 'fuer', 'von',
                             'vom', 'zu', 'zum', 'zur', 'im', 'an',
                             'auf', 'als', 'wie', 'zu') and \
            len(members) >= 2 and not unesc(members[0]['de']).rstrip()\
            .endswith(TERMINAL):
        f.append('DE1-AENDER-FALLE-OK?')
    return f


out = io.open('_work/review_fixes/chain_all.txt', 'w',
              encoding='latin1', newline='\n')
stats = {'chains': 0, 'multi': 0, 'flagged': 0}
flagged_rows = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    stem = os.path.basename(path)[:-7]
    rows = []
    with io.open(path, encoding='latin1') as fh:
        for line in fh:
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                rows.append({'uid': int(p[0]),
                             'off': int(p[2].split('|')[0]) if p[2]
                             else 0,
                             'en': p[4], 'de': p[5]})
    rows.sort(key=lambda r: r['off'])
    chains = []
    cur = [rows[0]]
    for r in rows[1:]:
        if cur and en_chain_end(cur[-1]['en']):
            chains.append(cur)
            cur = []
        cur.append(r)
    chains.append(cur)
    for members in chains:
        stats['chains'] += 1
        if len(members) >= 2:
            stats['multi'] += 1
        fl = chain_flags(members) if len(members) >= 2 else []
        if fl:
            stats['flagged'] += 1
            flagged_rows.append((stem, members, fl))
        out.write('# %s KETTE uids=%s\n' % (
            stem, ','.join(str(m['uid']) for m in members)))
        for m in members:
            out.write('  %4d EN %-45r DE %r\n' % (
                m['uid'], unesc(m['en']), unesc(m['de'])))
        if fl:
            out.write('  FLAGS: %s\n' % '; '.join(fl))
        out.write('\n')
out.close()

print('ketten=%d mehrblockig=%d mit-flags=%d' % (
    stats['chains'], stats['multi'], stats['flagged']))
with io.open('_work/review_fixes/chain_flagged.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for stem, members, fl in flagged_rows:
        f.write('# %s uids=%s FLAGS %s\n' % (
            stem, ','.join(str(m['uid']) for m in members), ';'.join(fl)))
        for m in members:
            f.write('  %4d EN %-45r DE %r\n' % (
                m['uid'], unesc(m['en']), unesc(m['de'])))
        f.write('\n')
print('bericht: chain_all.txt / chain_flagged.txt')
