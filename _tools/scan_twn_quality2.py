# Corrected quality scan for TWN_CAMP / TWN_RUIN.
# Format: uid;len;offset;offsets;en;de  (6 fields, en = field 4, de = field 5)
# EN and DE are the LAST two fields (handles variable offset count).
import csv
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EN_WORDS = set('the you your yours item items menu save load saved game games dragon dragons camp status map config yes no cancel exit quit continue press start skip auto window sound music voice subtitles on off enter select back next prev page up down left right name level hp mp exp power speed defense attack hit heal cure poison stun sleep silence blind weapon gun laser bullet armor shield helmet accessory use give equip unequip drop sort money gold buy sell price cost shopkeeper merchant quantity total town village desert ruins tower empire imperial fleet ship airship flagship soldier soldiers captain general lord emperor princess girl boy man woman old young battle fight flee run away victory defeat game over please wait loading now chapter episode scenario event movie scene subtitle caption screen display option options control controls key keys button buttons vibration memory card internal backup block blocks free file files delete copy move load failed error cannot unable available empty full short long heavy light fire ice wind earth thunder poison dark holy sword knife spear bow arrow bomb medicine herb potion antidote key keys map compass radio detector scope radar sonar engine part parts gear device machine prototype ancient age bio gene core weapon weapons system unit type class rank score points damage guard dodge rate bonus combo critical special normal hard easy version sound test staff credit credits secret hidden unlock complete clear time minute second hour day night morning evening quest mission target objective hint advice tip message letter note diary journal record records data info information about help tutorial practice training there their they them this that these those with from have has had was were will would could should when where what which who whom whose how why not are isnt dont didnt cant wont its im were theyre hes shes of and for but all any some more most other such only own same so than too very just also'.split())

DE_WORDS = set('der die das und nicht ein eine einen einem einer eines ich du er sie es wir ihr mir dich mich dir ihm ihnen uns euch fuer gegen ueber unter mit ohne auf aus bei nach vom zum zur ja nein weiter zurueck oben unten links rechts seite name wert staerke verteidigung geschwindigkeit glueck level erfahrung punkte schaden waffe waffen panzer helm schild gegenstand gegenstaende ausruestung benutzen geben anlegen ablegen wegwerfen sortieren geld kaufen verkaufen preis kosten haendler anzahl gesamt dorf wueste ruinen turm reich kaiser prinzessin maedchen junge mann frau alt jung kampf kaempfen fliehen lauf weg sieg niederlage spielstand laden speichern disc wechsel bitte warten jetzt kapitel szene untertitel bildschirm anzeige option steuerung taste tasten knopf memoria frei datei dateien loeschen kopieren verschieben fehlgeschlagen fehler kann nicht verfuegbar leer voll kurz lang leicht feuer eis wind erde donner gift dunkel heilig schwert messer speer bogen pfeil bombe medizin kraeuter trank gegenmittel schluessel kompass radio detektor radar sonar motor teil teile zahnrad geraet maschine prototyp vorzeit urzeit bio gen kern system einheit typ klasse rang wertung bonus spezial normal schwer leicht version ton test mitarbeiter abspann geheim versteckt freischalten komplett zeit minute sekunde stunde tag nacht morgen abend auftrag ziel hinweis ratschlag tipp botschaft brief notiz tagebuch journal daten info information ueber hilfe uebung training angriff abwehr ausweichen rate kritisch kaempfer reiter drache rettung hoffnung wahrheit luege freund feind bruder schwester vater mutter sohn tochter ist bin sind war waren habe hast hat hatte werde wirst wird wurden nicht kein keine keinen einem unsere unsere eurer alle alles man nur auch noch schon sehr immer nie wieder dort hier diese dieser dieses jener was wie wo wann warum weil doch mal gar ganz selbst'.split())

for fn in ('TWN_CAMP_PRG_de.csv', 'TWN_RUIN_PRG_de.csv'):
    src = '_work/subtitles/' + fn
    out = '_work/review_fixes/' + fn.replace('_de.csv', '_candidates2.csv')
    with open(src, encoding='latin1') as f, open(out, 'w', encoding='latin1', newline='') as o:
        rd = csv.reader(f, delimiter=';')
        o.write('uid;en;old_de;reason\n')
        n = 0
        for r in rd:
            if len(r) < 6:
                continue
            uid, length, offsets, off2, en, de = r[0], r[1], r[2], r[3], r[4], r[5]
            reasons = []
            if de.strip() in ('de', ''):
                reasons.append('placeholder de')
            if de == en:
                reasons.append('DE==EN (untranslated?)')
            # hard-cut: DE not ending in punctuation
            de_stripped = de.strip()
            if de_stripped and de_stripped[-1] not in '.!?...,:;)' and not de_stripped.endswith('...'):
                reasons.append('hard-cut (no terminal punct)')
            low = de.lower()
            if 'imperium' in low:
                reasons.append('Glossar: Imperium->Reich')
            if 'altertum' in low:
                reasons.append('Glossar: Altertum->Vorzeit')
            if 'kapit' in low:
                reasons.append('Glossar: Kapitaen->Chef')
            # glossary: Reich/Empire consistency — check if EN has "Empire" but DE has "Imperium"
            if 'empire' in en.lower() and 'imperium' in low:
                reasons.append('Glossar: Empire->Reich')
            if 'ancient age' in en.lower() and 'altertum' in low:
                reasons.append('Glossar: Ancient Age->Vorzeit')
            # mixed language: English words left in DE
            words = re.findall(r"[a-z']+", low)
            enleft = [w for w in words if w in EN_WORDS and w not in DE_WORDS]
            if len(enleft) >= 2:
                reasons.append('EN words left: ' + ','.join(sorted(set(enleft))[:3]))
            # negation check
            en_low = en.lower()
            en_neg = any(neg in en_low for neg in ('not ', "n't", 'never ', 'no ', "don't", "doesn't", "can't", "won't", 'without', 'never'))
            de_neg = any(neg in low for neg in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner'))
            if en_neg and not de_neg:
                reasons.append('NEGATION LOST?')
            # shifted: DE much shorter than EN (possible shift)
            if len(de) < 0.4 * len(en) and len(en) > 10:
                reasons.append('possibly shifted/empty')
            if reasons:
                o.write('%s;%s;%s;%s\n' % (
                    uid, en.replace(';', ','), de.replace(';', ','),
                    ' | '.join(reasons)))
                n += 1
        print(fn, 'candidates:', n, '->', out)
print('done')
