# Comprehensive quality scan: spelling, grammar, untranslated, over-shortened
# (run from project root)
import os, re, glob

EN_GERMAN_SHARED = set('''der die das den dem des und ist ich du er sie es wir ihr
nicht ein eine einen einem einer eines mit von zu auf in an bei aus um am im zum
zurfuer oder aber als auch noch nur schon dann wenn wie was wer wo warum
habe hast hat haben hatte hatten bin bist sind seid war waren werde wirst wird
werden kann kannst koennen muss musst dich dir mir mich ihm ihm whilst'''.split())

EN_ONLY = set('''the a an and or but is are was were be been am have has had do
does did will would could should can may might shall not no yes of for on with
at by from as into through during before after above below between out off over
under again further then once here there when where why how all any each few
more most other some such than too very just about up down left right back it
its this that these those who whom which they them their their you your my me
we our us if while because'''.split())

def en_words_in_de(text):
    found = []
    for w in re.findall(r"[A-Za-z']+", text):
        wl = w.lower()
        if wl in EN_ONLY and wl not in EN_GERMAN_SHARED:
            found.append(w)
    return found

def check(en, de):
    flags = []
    if not de or not en:
        flags.append('EMPTY'); return flags
    enb = len(en.encode('latin1')); deb = len(de.encode('latin1'))
    if deb > enb:
        flags.append('TOO_LONG(%d>%d)' % (deb, enb))
    # untranslated
    if de.strip() == en.strip() and len(en.strip()) >= 4:
        flags.append('UNTRANSLATED')
    # over-short but translated
    elif deb < 0.45 * enb and enb >= 40:
        flags.append('OVERSHORT(%.0f%%)' % (100.0 * deb / enb))
    # negation lost
    enw = en.lower(); dew = de.lower()
    en_neg = ("n't" in enw) or re.search(r'\b(not|never|no|none|nothing|nobody|without|cannot)\b', enw)
    de_neg = re.search(r'\b(nicht|kein|keine|keinen|keiner|keinem|nie|niemals|ohne|niemand|nie)\b', dew)
    if en_neg and not de_neg:
        flags.append('NEG_LOST')
    # english words left in german
    ew = en_words_in_de(de)
    if ew:
        flags.append('EN_IN_DE(' + ','.join(sorted(set(ew))) + ')')
    # truncated trailing word
    base = de.rstrip()
    if base and base[-1].isalpha():
        tail = re.findall(r"([A-Za-zaeiou0-9]+)$", base)
        if tail and not en.rstrip()[-1].isalpha():
            flags.append('TRUNC_END')
    elif base and not base.endswith(('!','?','.',':',';',')')):
        flags.append('NO_END_PUNCT')
    # broken punctuation
    for pat, name in ((r'[,](?=\.)', 'COMMA_DOT'), (r'\.\.(?!\.)', 'DOUBLE_DOT'),
                      (r'\s,', 'COMMA_PRE'), (r'\(\s*\)', 'EMPTY_PAR'),
                      (r'\?\?', 'DOUBLE_Q'), (r'!!', 'DOUBLE_BANG'),
                      (r'\s{2,}', 'DOUBLE_SPACE')):
        if re.search(pat, de) and not re.search(pat, en):
            flags.append(name)
    # missing subject: starts with finite verb of "you" question without du
    if re.match(r'^(Kennst|Weisst|Hast|Bist|Kommst|Willst|Moechtest|Findest|Sprichst|Verstehst|Denkst|Glaubst|Sagst|Bleibst|Warte)s?\b', de) and len(de.split()) > 1:
        # crude: many of these ARE imperative-like; flag for review
        flags.append('VERB_START')
    # lowercase sentence start where en starts uppercase
    e0 = en.lstrip('(...\'"')[:1]
    d0 = de.lstrip('(...\'"')[:1]
    if e0 and e0.isupper() and d0 and d0.islower() and deb >= 10:
        flags.append('LC_SENT_START')
    return flags

def load_csv(path, mode):
    rows = []
    with open(path, encoding='latin1') as f:
        for i, line in enumerate(f):
            line = line.rstrip('\r\n')
            if not line:
                continue
            if i == 0 and mode in ('sub', 'menu') and not line.startswith(('(','"',)) and (';off;' in line or line.startswith('uid;') or line.startswith('file;')):
                continue
            if mode == 'map' and i == 0 and line == 'en;de':
                continue
            p = line.split(';')
            if mode == 'sub' and len(p) >= 6:
                rows.append((p[0], p[4], p[5], line))
            elif mode == 'menu' and len(p) >= 6:
                rows.append((p[1], p[4], p[5], line))
            elif mode == 'map' and len(p) >= 2:
                rows.append(('', p[0], p[1], line))
    return rows

def main():
    tasks = []
    for p in sorted(glob.glob('_work/subtitles/*_de.csv')):
        tasks.append((p, load_csv(p, 'sub')))
    for p in sorted(glob.glob('_work/menu_de/*_de*.csv')):
        if p.endswith('_de_p2.csv'):
            tasks.append((p, load_csv(p, 'menu')))
        else:
            tasks.append((p, load_csv(p, 'menu')))
    for p in ['_work/menu_de/BTL_REST_map.csv', '_work/menu_de/TWN_SEEK_PRG_d4_map.csv',
              '_work/menu_de/TWN_SEEK_PRG_map.csv', '_work/menu_de/TWN_E059_PRG_d2_map.csv',
              '_work/menu_de/BTL_B5_FNT_map.csv', '_work/menu_de/BTL_C2_FNT_map.csv',
              '_work/menu_de/BTL_C52_FNT_map.csv', '_work/menu_de/BTL_T0_FNT_map.csv',
              '_work/menu_de/BTL_X0_FNT_map.csv', '_work/menu_de/CHILDMP_MCB_map.csv',
              '_work/menu_de/TUTORIAL_CGB_map.csv', '_work/menu_de/MENUEN_FNT_map.csv']:
        if os.path.exists(p):
            tasks.append((p, load_csv(p, 'map')))

    out = open('_work/review_fixes/full_review_candidates.csv', 'w', encoding='latin1', newline='')
    out.write('file;id;flags;chars;en;de\n')
    n_flag = 0
    for path, rows in tasks:
        per_flag = {}
        rows_out = []
        for rid, en, de, line in rows:
            fl = check(en, de)
            if fl:
                for f in fl:
                    per_flag[f.split('(')[0]] = per_flag.get(f.split('(')[0], 0) + 1
                rows_out.append((rid, fl, en, de))
        if rows_out:
            print('== %s  (%d rows)' % (path, len(rows)))
            for k in sorted(per_flag):
                print('   %-14s %d' % (k, per_flag[k]))
            n_flag += len(rows_out)
            for rid, fl, en, de in rows_out:
                out.write('%s;%s;%s;%d;%s;%s\n' % (os.path.basename(path), rid,
                    '+'.join(f.split('(')[0] for f in fl), len(de), en, de))
    out.close()
    print()
    print('total flagged rows:', n_flag)

main()
