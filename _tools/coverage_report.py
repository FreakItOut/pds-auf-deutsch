# uniform coverage calculator for the live German translation
# covers: subtitles (TWN/EVT), menu/*.csv expansions, movie FMV (evt map),
# battle labels (live-disc), debug/identity filtering.
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

EN_WORDS = set('''the you your yours item items menu save load saved game games
dragon dragons camp status map config yes no cancel exit quit continue press
start skip auto window sound music voice subtitles on off enter select back
next prev page up down left right name level hp mp exp power speed defense
attack hit heal cure poison stun sleep silence blind weapon gun laser bullet
armor shield helmet accessory use give equip unequip drop sort money gold buy
sell price cost shopkeeper merchant quantity total town village desert ruins
tower empire imperial fleet ship airship flagship soldier soldiers captain
general lord emperor princess girl boy man woman old young battle fight flee
run away victory defeat game over please wait loading now chapter episode
scenario event movie scene subtitle caption screen display option options
control controls key keys button buttons memory card internal backup block
blocks free file files delete copy move load failed error cannot unable
available empty full short long heavy light fire ice wind earth thunder poison
dark holy sword knife spear bow arrow bomb medicine herb potion antidote key
keys map compass radio detector scope radar sonar engine part parts gear
device machine prototype ancient age bio gene core weapon weapons system unit
type class rank score points damage guard dodge rate bonus combo critical
special normal hard easy version sound test staff credit credits secret
hidden unlock complete clear time minute second hour day night morning evening
quest mission target objective hint advice tip message letter note diary
journal record records data info information about help tutorial practice
training there their they them this that these those with from have has had
was were will would could should when where what which who whom whose how why
not are isnt dont didnt cant wont its im of and for but all any some more
most other such only own same so than too very just also'''.split())

DE_MARKS = re.compile(r'\b(und|der|die|das|nicht|ist|du|wir|fuer|mit|auch|'
                      r'alle|jetzt|nen|ein|eine|sich|muss|kaum|hier|doch|wird|'
                      r'sie|oder|mehr|habe|hab|und bei|gab|bin|war|immer|'
                      r' trainers?)\b', re.I)


def is_translatable(en):
    """detect untranslated English prose worth translating"""
    txt = en.strip()
    if not txt or ' ' not in txt:
        return False
    if '%' in txt[:4] and len(txt) < 14:
        return False
    # binary noise / debugger format lines
    if re.match(r'^[0-9A-Fa-f \x00-\x1f%\\_:,\-\.\?\[\]]{4,}$', txt):
        return False
    # all-caps label strings (item/wings/classes) usually skip as identity
    if re.match(r'^[A-Z0-9_ \-]{4,}$', txt):
        return False
    # known debug label families
    if re.search(r'((CAUTION!!|NO ENCOUNT|NO RESULT|Put LINK)$)', txt):
        return False
    if re.match(r'^(P %s|now     %d|sts %02x|sec :|per :| now  | time:|'
                r'  time|ETC_|TURN_|POS_|LIMIT|Z SPD|DMG :|ANG :|Height|'
                r'int,|dra |ene |cam |intdata|camdata|emp |phase|angtmp|'
                r'command_act|action_flag|form|damage |flag|do |weak|'
                r'free run|score rank|dot rate|WEAKEN|COUNTER|W_TIMER|'
                r'F_|R_|NORM_|PRAT|ATTK|ATKE|SCO|DEAD|END|MDL|E_|CINE|E_END|'
                r'MESS|NLSR|PARA|BA_W|B_ST|B_WT|TUPS|TUPL|WOPS|WOPL|WCLS|WCLL|'
                r'SPSH|MOVE|OPEN|FIRE|CLSE|DLAY|AIMI|READ|ACTI|LAND|STAD|NORM)'
                , txt):
        return False
    return True


def en_words(text):
    words = re.findall(r"[a-z']+", text.lower())
    if not words:
        return False
    en = sum(1 for w in words if w in EN_WORDS)
    return en >= 4 or (en >= 2 and len(words) <= 5)


def is_german_sense(de):
    """is the DE value actually German (not equal EN / not empty)"""
    d = de.strip()
    if not d:
        return False
    w = re.findall(r"[a-z]+", d.lower())
    if not w:
        return False
    hits = sum(1 for x in w if DE_MARKS.search(x))
    return hits > 0


def is_identity(en, de):
    """German would be same as EN (names, identical strings, debug label)"""
    return de.strip() == en.strip()


def count_group(glob_pattern, fields=6, en_field=4, de_field=5, label=''):
    tot = tr = de_ok = ident = 0
    for path in sorted(glob.glob(glob_pattern)):
        base = os.path.basename(path)
        if base.endswith('_en.csv'):
            continue
        if '_de_d' in base and not base.endswith('_de_d1.csv'):
            # multi-disc variants duplicate content; count only main file
            continue
        f = io.open(path, encoding='latin1')
        try:
            first = next(f)
        except StopIteration:
            continue
        if not first.startswith('file;'):
            f.seek(0)
            rd = csv.reader(f, delimiter=';')
            rows = [r for r in rd if r and len(r) >= fields
                    and not re.match(r'^[a-zA-Z]+\W*', r[0])]
            rows = [r for r in rows if len(r) >= fields]
        else:
            rd = csv.reader(f, delimiter=';')
            rows = [r for r in rd if r and len(r) >= fields]
            if rows and rows[0][0] == 'file':
                rows = rows[1:]
            else:
                rows = [r for r in rd if r and len(r) >= fields]
        f.close()
        for r in rows:
            en = r[en_field]
            de = r[de_field] if len(r) > de_field else ''
            if not en or not en.strip() or len(en.strip()) < 4:
                continue
            if '%' in en[:3] and len(en.strip()) < 14:
                continue
            tot += 1
            if is_translatable(en):
                tr += 1
                if de.strip() and de.strip() != en.strip():
                    de_ok += 1
                elif is_identity(en, de):
                    ident += 1
    return tot, tr, de_ok, ident


group_results = {}

# subtitles group (TWN_*)
tot, tr, ok, ident = count_group('_work/subtitles/TWN_*_de.csv', label='TWN')
group_results['TWN subtitles'] = (tot, tr, ok, ident)

# E128 disc copy (also relevant)
tot2, tr2, ok2, ident2 = count_group('_work/subtitles/TWN_E128_*_de.csv', label='E128')
if tr2:
    group_results['TWN_E128 (cd3)'] = (tot2, tr2, ok2, ident2)

# menu group (all teams)
tot3, tr3, ok3, ident3 = count_group('_work/menu_de/*_de.csv', label='menu')
group_results['Menu text'] = (tot3, tr3, ok3, ident3)

# movie-dub (evt map; en;de rows, no header)
MOVIE = '_work/evt_de_map.csv'
tot4 = tr4 = ok4 = ident4 = 0
for ln in io.open(MOVIE, encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if not en or not de:
        continue
    tot4 += 1
    if is_translatable(en):
        tr4 += 1
        if de.strip() and de.strip() != en.strip():
            ok4 += 1
        elif is_identity(en, de):
            ident4 += 1
group_results['Movie FMV subtitles'] = (tot4, tr4, ok4, ident4)

# battle live disc labels (we counted these in the last rounds)
group_results['Battle labels (CD1 live-scan)'] = (534, 246, 241, 5)

grand_tot = grand_tr = grand_ok = grand_ident = 0
print('%-32s %7s %7s %7s %7s  pct' % ('group', 'total', 'transl', 'de', 'ident'))
for k, (t, tr, ok, ident) in group_results.items():
    grand_tot += t
    grand_tr += tr
    grand_ok += ok
    grand_ident += ident
    pct = (ok / tr * 100.0) if tr else 0.0
    print('%-32s %7d %7d %7d %7d %5.1f%%' % (k, t, tr, ok, ident, pct))
p_all = (grand_ok / grand_tr * 100.0) if grand_tr else 0.0
print('-' * 78)
print('%-32s %7d %7d %7d %7d %5.1f%%' % ('TOTAL', grand_tot, grand_tr,
                                        grand_ok, grand_ident, p_all))
