import csv, os, re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

rows = []
with open('_work/subtitles/TWN_RUIN_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        line = line.rstrip('\r\n')
        if not line: continue
        parts = line.split(';')
        if len(parts) < 6: continue
        uid, length, offset, offsets, en, de = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
        rows.append((uid, en, de))

print('RUIN rows:', len(rows))

# glossary
gloss = 0
for uid, en, de in rows:
    low = de.lower()
    if 'imperium' in low or 'altertum' in low or 'kapit' in low:
        gloss += 1
        if gloss <= 10:
            print('  GLOSSARY:', uid, repr(en[:40]), '->', repr(de[:40]))
print('glossary issues:', gloss)

# placeholder
ph = [r for r in rows if r[2].strip() in ('de', '')]
print('placeholder:', len(ph))

# negation
neg = 0
for uid, en, de in rows:
    en_low = en.lower()
    de_low = de.lower()
    en_neg = any(n in en_low for n in ('not ', "n't", 'never ', 'no ', "don't", "doesn't", "can't", "won't", 'without', 'never'))
    de_neg = any(n in de_low for n in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner'))
    if en_neg and not de_neg:
        neg += 1
        if neg <= 10:
            print('  NEG-LOST:', uid, repr(en[:40]), '->', repr(de[:40]))
print('negation lost:', neg)

# EN words left
en_words = set('the you your yours item items menu save load saved game games dragon dragons camp status map config yes no cancel exit quit continue press start skip auto window sound music voice subtitles on off enter select back next prev page up down left right name level hp mp exp power speed defense attack hit heal cure poison stun sleep silence blind weapon gun laser bullet armor shield helmet accessory use give equip unequip drop sort money gold buy sell price cost shopkeeper merchant quantity total town village desert ruins tower empire imperial fleet ship airship flagship soldier soldiers captain general lord emperor princess girl boy man woman old young battle fight flee run away victory defeat game over please wait loading now chapter episode scenario event movie scene subtitle caption screen display option options control controls key keys button buttons vibration memory card internal backup block blocks free file files delete copy move load failed error cannot unable available empty full short long heavy light fire ice wind earth thunder poison dark holy sword knife spear bow arrow bomb medicine herb potion antidote key keys map compass radio detector scope radar sonar engine part parts gear device machine prototype ancient age bio gene core weapon weapons system unit type class rank score points damage guard dodge rate bonus combo critical special normal hard easy version sound test staff credit credits secret hidden unlock complete clear time minute second hour day night morning evening quest mission target objective hint advice tip message letter note diary journal record records data info information about help tutorial practice training there their they them this that these those with from have has had was were will would could should when where what which who whom whose how why not are isnt dont didnt cant wont its im were theyre hes shes of and for but all any some more most other such only own same so than too very just also'.split())
de_words = set('der die das und nicht ein eine einen einem einer eines ich du er sie es wir ihr mir dich mich dir ihm ihnen uns euch fuer gegen ueber unter mit ohne auf aus bei nach vom zum zur ja nein weiter zurueck oben unten links rechts seite name wert staerke verteidigung geschwindigkeit glueck level erfahrung punkte schaden waffe waffen panzer helm schild gegenstand gegenstaende ausruestung benutzen geben anlegen ablegen wegwerfen sortieren geld kaufen verkaufen preis kosten haendler anzahl gesamt dorf wueste ruinen turm reich kaiser prinzessin maedchen junge mann frau alt jung kampf kaempfen fliehen lauf weg sieg niederlage spielstand laden speichern disc wechsel bitte warten jetzt kapitel szene untertitel bildschirm anzeige option steuerung taste tasten knopf memoria frei datei dateien loeschen kopieren verschieben fehlgeschlagen fehler kann nicht verfuegbar leer voll kurz lang leicht feuer eis wind erde donner gift dunkel heilig schwert messer speer bogen pfeil bombe medizin kraeuter trank gegenmittel schluessel kompass radio detektor radar sonar motor teil teile zahnrad geraet maschine prototyp vorzeit urzeit bio gen kern system einheit typ klasse rang wertung bonus spezial normal schwer leicht version ton test mitarbeiter abspann geheim versteckt freischalten komplett zeit minute sekunde stunde tag nacht morgen abend auftrag ziel hinweis ratschlag tipp botschaft brief notiz tagebuch journal daten info information ueber hilfe uebung training angriff abwehr ausweichen rate kritisch kaempfer reiter drache rettung hoffnung wahrheit luege freund feind bruder schwester vater mutter sohn tochter ist bin sind war waren habe hast hat hatte werde wirst wird wurden nicht kein keine keinen einem unsere unsere eurer alle alles man nur auch noch schon sehr immer nie wieder dort hier diese dieser dieses jener was wie wo wann warum weil doch mal gar ganz selbst'.split())
enleft_count = 0
for uid, en, de in rows:
    words = re.findall(r"[a-z']+", de.lower())
    enleft = [w for w in words if w in en_words and w not in de_words]
    if len(enleft) >= 2:
        enleft_count += 1
        if enleft_count <= 5:
            print('  EN-LEFT:', uid, repr(en[:40]), '->', repr(de[:40]), enleft[:3])
print('EN words left (>=2):', enleft_count)
print('done')
