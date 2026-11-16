# Full EN extraction from ORIGINAL disc (no TODO filtering).
# Same heuristics as extract_menu_strings.py but PATCH_BIN = ORIG_BIN so
# nothing is skipped. Usage: python extract_menu_full.py <NAME...
import csv
import os
import re
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048

ORIG_BIN = ('Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) '
            '(Track 1).bin')

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

DE_WORDS = set('''start ueberspringen auto fenster ton musik stimme untertitel
an aus waehlen zurueck waehlen weiter vor zurueck Seite vor zurueck rauf runter
punkt vor zurueck Datei Blocken kopieren verschieben laden Scheitern Fehler
koennen Datei Datei loschen Kopieren Verschieben laden gescheitert Fehler
kontn Sind nicht verfuegbar leer voll kurz lang schwer leicht Feuer Eis Wind
Erde Donner Gift dunkel heilig Schwert Messer Speer Bogen Pfeil Bombe Medizin
Kraeuter Trank Gegenmittel Schluessel Kompass Radio Detektor Radar Sonar
Motor Teil Teile Zahnrad Geraet Maschine Prototyp Vorzeit Urzeit Bio Gen Kern
System Einheit Typ Klasse Rang Wertung Bonus Spezial Normal Schwer Leicht
Version Ton Test Mitarbeiter Abspann Geheim Versteckt Freischalten Komplett
Zeit Minute Sekunde Stunde Tag Nacht Morgen Abend Auftrag Ziel Hinweis
Ratschlag Tip Botschaft Brief Notiz Tagebuch Journal Daten Info Information
ueber Hilfe Uebung Training Angriff Abwehr Ausweichen Rate Kritisch
Kaempfer Reiter Drache Rettung Hoffnung Wahrheit Luege Freund Feind Bruder
Schwester Vater Mutter Sohn Tochter ist bin sind war waren habe hast hat
hatte werde wirst wird wurden nicht kein keine keinen einer einer unsere
Eure alle alles man nur auch noch schon sehr immer nie wieder dort hier
diese dieser dieses jener was wie wo wann warum weil doch mal gar ganz
selbst'''.split())

TARGETS = sys.argv[1:] or ['MENU.SCB', 'MENUEN.FNT', 'TUTORIAL.CGB',
                           'CHILDMP.MCB', 'FLD_A5.MCB', 'FLD_A7.FNT',
                           'FLD_A3.MCB', 'FLD_B6.MCB', 'FLD_C4_6.MCB',
                           'FLD_B5.FNT', 'FLD_C2.FNT', 'FLD_C4.FNT',
                           'FLD_B2.FNT', 'FLD_D2.FNT', 'FLD_D3.FNT',
                           'FLD_D5.FNT', 'TWN_SEEK.PRG', 'TWN_CARA.PRG',
                           'TWN_E006.PRG', 'TWN_E011.PRG', 'TWN_E014.PRG',
                           'TWN_E021.PRG', 'TWN_EXCA.PRG', 'TWN_ZOAH.PRG']

ASCII_OK = re.compile(rb'^[A-Za-z0-9 ,.!?\x27":;()&%$/+_#\-\n]+$')
FILENAME_RE = re.compile(r'^[A-Za-z0-9_]+\.(PCM|PRG|CGB|MCB|BIN|SE|SEQ|FNT|'
                         r'SCB|PNB|EXB|TXT|DAT)$', re.I)


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


def split_chunks(data):
    off = 0
    for part in data.split(b'\x00'):
        if part:
            yield off, part
        off += len(part) + 1


def ascii_tail(chunk):
    i = 0
    while i < len(chunk) and chunk[i] >= 0x80:
        i += 1
    return chunk[:i], chunk[i:]


def is_english(t):
    words = re.findall(r"[a-z']+", t.lower())
    if not words:
        return False
    en = sum(1 for w in words if w in EN_WORDS)
    de = sum(1 for w in words if w in DE_WORDS)
    return en > 0 and (de == 0 or en / len(words) > 0.12) and (
        en / len(words) >= 0.10 or en >= 2)


idx = {}
for r in csv.DictReader(open('_work/fs_records_all.csv', encoding='latin1'),
                        delimiter=';'):
    if int(r['lba']) > 0 and int(r['size']) > 0:
        idx[r['name']] = (int(r['lba']), int(r['size']))

os.makedirs('_work/menu_de', exist_ok=True)
for name in TARGETS:
    if name not in idx:
        print('%-14s NOT ON DISC 1' % name)
        continue
    lba, size = idx[name]
    orig = read_file(ORIG_BIN, lba, size)
    rows = []
    for off, chunk in split_chunks(orig):
        if len(chunk) < 3 or len(chunk) > 400:
            continue
        prefix, text = ascii_tail(chunk)
        if len(text) < 3 or not ASCII_OK.match(text):
            continue
        if not re.search(rb'[A-Za-z]{2}', text):
            continue
        t = text.decode('ascii')
        if FILENAME_RE.match(t.strip()):
            continue
        if re.search(r'(MODE|DISP|DEBUG|CAM |BTL DATA| map[0-9]|x[0-9])', t):
            continue
        rows.append((off, prefix.hex(), len(text), t))
    uniq = len({r[3] for r in rows})
    out = f'_work/menu_de/{name.replace(".", "_")}_en.csv'
    with open(out, 'w', encoding='latin1', newline='') as fh:
        fh.write('file;off;prefix;len;en\n')
        for off, pre, ln, t in rows:
            fh.write('%s;%d;%s;%d;%s\n' % (
                name, off, pre, ln, t.replace('\n', '\\n').replace(';', ',')))
    print('%-14s rows=%4d unique=%4d -> %s' % (name, len(rows), uniq, out))
