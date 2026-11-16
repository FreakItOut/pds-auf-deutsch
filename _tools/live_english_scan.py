# live scan: which disc1 menu/tutorial files still hold plausible English?
import csv
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT = 2352
DATA = 2048

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


def read_file(binpath, lba, size):
    with open(binpath, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


def is_english(t):
    words = re.findall(r"[a-z']+", t.lower())
    if not words:
        return False
    en = sum(1 for w in words if w in EN_WORDS)
    return en >= 4 or (en >= 2 and len(words) <= 4)


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv', encoding='latin1'),
                               delimiter=';') if int(r['lba']) > 0}
FILES = ['TUTORIAL.CGB', 'MENUEN.FNT', 'CHILDMP.MCB', 'FLD_A5.MCB',
         'FLD_A3.MCB', 'FLD_B6.MCB', 'FLD_C4_6.MCB', 'FLD_A7.FNT',
         'FLD_B5.FNT', 'FLD_C2.FNT', 'FLD_D2.FNT', 'BTL_T0.FNT',
         'BTL_B5.FNT', 'BTL_C2.FNT', 'BTL_X0.FNT', 'TWN_SEEK.PRG',
         'TWN_E022.PRG', 'MERUKABA.MCB', 'MENU.SCB']
for name in FILES:
    if name not in idx:
        print('%-14s not on disc1' % name)
        continue
    lba, size = idx[name]
    data = read_file('_work/patched_disc1.bin', lba, size)
    found = 0
    samples = []
    off = 0
    for part in data.split(b'\x00'):
        if len(part) >= 8:
            txt = part.decode('latin1', 'replace')
            if is_english(txt) and not re.match(r'^[\$\%@#\^0-9A-Z_\.\- ]+$', txt):
                found += 1
                if len(samples) < 6:
                    samples.append(txt[:60])
        off += len(part) + 1
    print('%-14s english-like=%4d  %s' % (name, found, samples))
