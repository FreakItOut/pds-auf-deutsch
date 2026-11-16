# Inventory of REMAINING ENGLISH text on the patched discs.
# For every file in the Sega FS of each patched disc, extract the file
# (2048-byte user data reassembly) and collect printable ASCII runs that
# look like English UI/dialog text. German-looking strings are counted
# separately so we can see per file what is done vs. missing.
import csv
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048

EN_WORDS = set('''the you your yours item items menu save load saved game games
dragon dragons camp status map config yes no cancel exit quit continue press
start skip auto window sound music voice subtitles on off enter select back
next prev page up down left right name level hp mp exp power speed defense
attack hit heal cure poison stun sleep silence blind weapon gun laser bullet
armor shield helmet accessory use give equip unequip drop sort money gold
buy sell price cost shopkeeper merchant quantity total town village desert
ruins tower empire imperial fleet ship airship flagship soldier soldiers
captain general lord emperor princess girl boy man woman old young battle
fight flee run away victory defeat game over disc change insert please wait
loading now chapter episode scenario event movie scene subtitle caption
screen display option options control controls key keys button buttons
vibration memory card internal backup block blocks free file files delete
copy move load failed error cannot unable available empty full short long
heavy light fire ice wind earth thunder poison dark holy sword knife spear
bow arrow bomb medicine herb potion antidote key keys map compass radio
detector scope radar sonar engine part parts gear device machine prototype
ancient age bio gene core weapon weapons system unit type class rank score
points damage guard dodge rate bonus combo critical special normal hard easy
version sound test staff credit credits secret hidden unlock complete clear
time minute second hour day night morning evening quest mission target
objective hint advice tip message letter note diary journal record records
data info information about help tutorial practice training'''.split())

DE_WORDS = set('''der die das und nicht ein eine einen einem einer eines ich
du er sie es wir ihr mir dich mich dir ihm ihnen uns euch fuer gegen ueber
unter mit ohne auf aus bei nach vom zum zur ja nein weiter zurueck oben unten
links rechts seite name wert staerke verteidigung geschwindigkeit glueck
level erfahrung punkte schaden waffe waffen panzer helm schild gegenstand
gegenstaende ausruestung benutzen geben anlegen ablegen wegwerfen sortieren
geld kaufen verkaufen preis kosten haendler anzahl gesamt dorf wueste ruinen
turm reich kaiser prinzessin maedchen junge mann frau alt jung kampf kaempfen
fliehen lauf weg sieg niederlage spielstand laden speichern disc wechsel
bitte warten jetzt kapitel szene untertitel bildschirm anzeige option
steuerung taste tasten knopf memoria frei datei dateien loeschen kopieren
verschieben fehlgeschlagen fehler kann nicht verfuegbar leer voll kurz lang
leicht feuer eis wind erde donner gift dunkel heilig schwert messer speer
bogen pfeil bombe medizin kraeuter trank gegenmittel schluessel kompass radio
detektor radar sonar motor teil teile zahnrad geraet maschine prototyp
vorzeit urzeit bio gen kern system einheit typ klasse rang wertung bonus
spezial normal schwer leicht version ton test mitarbeiter abspann geheim
versteckt freischalten komplett zeit minute sekunde stunde tag nacht morgen
abend auftrag ziel hinweis ratschlag tipp botschaft brief notiz tagebuch
journal daten info information ueber hilfe uebung training angriff abwehr
ausweichen rate kritisch kombinieren kaempfer reiter drache rettung hoffnung
wahrheit luege freund feind bruder schwester vater mutter sohn tochter'''.split())

STR_RE = re.compile(rb'[A-Za-z][A-Za-z0-9 .,!?\'`:;\-()&%$/+_#\x20]{4,}')


def read_file_regions(binpath, lba, size):
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


def classify(text):
    lo = text.lower()
    words = re.findall(r"[a-z']+", lo)
    if not words:
        return 0.0
    en = sum(1 for w in words if w in EN_WORDS)
    de = sum(1 for w in words if w in DE_WORDS)
    return (en - de) / len(words)


def is_germanish(text):
    lo = text.lower()
    words = re.findall(r"[a-z']+", lo)
    if not words:
        return False
    de = sum(1 for w in words if w in DE_WORDS)
    return de / len(words) > 0.24


summary = {}
for d in (1, 2, 3, 4):
    fs = ('_work/fs_records_all.csv' if d == 1
          else f'_work/fs_records_cd{d}.csv')
    binp = f'_work/patched_disc{d}.bin'
    rows = [r for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
            if int(r['lba']) > 0 and int(r['size']) > 0]
    out = open(f'_work/english_remaining_disc{d}.csv', 'w',
               encoding='latin1', newline='')
    out.write('file;score;len;text\n')
    per_file = {}
    for r in rows:
        data = read_file_regions(binp, int(r['lba']), int(r['size']))
        hits = []
        for m in STR_RE.finditer(data):
            t = m.group().decode('ascii', 'replace').strip()
            if len(t) < 5:
                continue
            sc = classify(t)
            if sc >= 0.25 and not is_germanish(t):
                hits.append((sc, m.start(), t))
        if hits:
            per_file[r['name']] = hits
            for sc, off, t in hits:
                out.write('%s;%.2f;%d;%s\n' % (r['name'], sc, off, t.replace(';', ',')))
    out.close()
    total = sum(len(h) for h in per_file.values())
    print('disc %d: %d/%d files with English, %d English strings total'
          % (d, len(per_file), len(rows), total))
    summary[d] = per_file

# combined per-file-name overview (all discs)
names = {}
for d, per_file in summary.items():
    for n, hits in per_file.items():
        names.setdefault(n, [0, 0.0, ''])[0] += len(hits)
        if not names[n][2]:
            names[n][2] = hits[0][2][:60]
print()
print('=== files with most remaining English (across discs) ===')
for n, (cnt, _, sample) in sorted(names.items(), key=lambda kv: -kv[1][0])[:40]:
    print('%-18s %5d  e.g. %r' % (n, cnt, sample))
