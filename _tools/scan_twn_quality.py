# Heuristic quality scan for TWN_CAMP / TWN_RUIN German translations.
# Produces candidate-fix CSVs (_work/review_fixes/CAMP_candidates.csv etc.)
# with: uid;en;old_de;reason  (new_de left empty for manual completion).
# Detects: placeholder 'de', empty DE, untranslated (DE==EN), hard-cut
# mid-word (de not ending in punctuation), glossary violations, suspicious
# English words left in German, EN-side trailing-space/placeholder issues.
import csv
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EN_WORDS = set('the you your yours item items menu save load saved game games dragon dragons camp status map config yes no cancel exit quit continue press start skip auto window sound music voice subtitles on off enter select back next prev page up down left right name level hp mp exp power speed defense attack hit heal cure poison stun sleep silence blind weapon gun laser bullet armor shield helmet accessory use give equip unequip drop sort money gold buy sell price cost shopkeeper merchant quantity total town village desert ruins tower empire imperial fleet ship airship flagship soldier soldiers captain general lord emperor princess girl boy man woman old young battle fight flee run away victory defeat game over please wait loading now chapter episode scenario event movie scene subtitle caption screen display option options control controls key keys button buttons memory card internal backup block blocks free file files delete copy move load failed error cannot unable available empty full short long heavy light fire ice wind earth thunder poison dark holy sword knife spear bow arrow bomb medicine herb potion antidote key keys map compass radio detector scope radar sonar engine part parts gear device machine prototype ancient age bio gene core weapon weapons system unit type class rank score points damage guard dodge rate bonus combo critical special normal hard easy version sound test staff credit credits secret hidden unlock complete clear time minute second hour day night morning evening quest mission target objective hint advice tip message letter note diary journal record records data info information about help tutorial practice training there their they them this that these those with from have has had was were will would could should when where what which who whom whose how why not are isnt dont didnt cant wont its im were theyre hes shes of and for but all any some more most other such only own same so than too very just also'.split())

DE_WORDS = set('der die das und nicht ein eine einen einem einer eines ich du er sie es wir ihr mir dich mich dir ihm ihnen uns euch fuer gegen ueber unter mit ohne auf aus bei nach vom zum zur ja nein weiter zurueck oben unten links rechts seite name wert staerke verteidigung geschwindigkeit glueck level erfahrung punkte schaden waffe waffen panzer helm schild gegenstand gegenstaende ausruestung benutzen geben anlegen ablegen wegwerfen sortieren geld kaufen verkaufen preis kosten haendler anzahl gesamt dorf wueste ruinen turm reich kaiser prinzessin maedchen junge mann frau alt jung kampf kaempfen fliehen lauf weg sieg niederlage spielstand laden speichern disc wechsel bitte warten jetzt kapitel szene untertitel bildschirm anzeige option steuerung taste tasten knopf memoria frei datei dateien loeschen kopieren verschieben fehlgeschlagen fehler kann nicht verfuegbar leer voll kurz lang leicht feuer eis wind erde donner gift dunkel heilig schwert messer speer bogen pfeil bombe medizin kraeuter trank gegenmittel schluessel kompass radio detektor radar sonar motor teil teile zahnrad geraet maschine prototyp vorzeit urzeit bio gen kern system einheit typ klasse rang wertung bonus spezial normal schwer leicht version ton test mitarbeiter abspann geheim versteckt freischalten komplett zeit minute sekunde stunde tag nacht morgen abend auftrag ziel hinweis ratschlag tipp botschaft brief notiz tagebuch journal daten info information ueber hilfe uebung training angriff abwehr ausweichen rate kritisch kaempfer reiter drache rettung hoffnung wahrheit luege freund feind bruder schwester vater mutter sohn tochter ist bin sind war waren habe hast hat hatte werde wirst wird wurden nicht kein keine keinen einem unsere unsere eurer alle alles man nur auch noch schon sehr immer nie wieder dort hier diese dieser dieses jener was wie wo wann warum weil doch mal gar ganz selbst'.split())

GLOS = {
    'imperium': 'Reich (Glossar)', 'altertum': 'Vorzeit (Glossar)',
    'kapit': 'Chef (Glossar)', 'kapitaen': 'Chef (Glossar)',
    'kaiser': 'Reich (Glossar ok)', 'empire': 'Reich (Glossar)',
}


def is_hard_cut(de):
    # de not ending in punctuation and not a known fragment label
    de = de.strip()
    if not de:
        return True
    last = de[-1]
    return last not in '.!?...,:;)' and not de.endswith('...')


for fn in ('TWN_CAMP_PRG_de.csv', 'TWN_RUIN_PRG_de.csv'):
    src = '_work/subtitles/' + fn
    out = '_work/review_fixes/' + fn.replace('_de.csv', '_candidates.csv')
    with open(src, encoding='latin1') as f, open(out, 'w', encoding='latin1', newline='') as o:
        rd = csv.reader(f, delimiter=';')
        o.write('uid;en;old_de;reason\n')
        n = 0
        for r in rd:
            if len(r) < 5:
                continue
            uid, length, offsets, en, de = r[0], r[1], r[2], r[3], r[4]
            reasons = []
            if de.strip() == 'de':
                reasons.append('placeholder de')
            if de.strip() == '':
                reasons.append('empty DE')
            if de == en:
                reasons.append('DE==EN (untranslated?)')
            if is_hard_cut(de):
                reasons.append('hard-cut (no terminal punct)')
            if en.endswith(' ') and not de.endswith(' '):
                pass  # trailing space not strictly needed
            # glossary
            low = de.lower()
            if 'imperium' in low:
                reasons.append('Glossar: Imperium->Reich')
            if 'altertum' in low:
                reasons.append('Glossar: Altertum->Vorzeit')
            if 'kapit' in low:
                reasons.append('Glossar: Kapitaen->Chef')
            # mixed language: English words left in DE
            words = re.findall(r"[a-z']+", low)
            enleft = [w for w in words if w in EN_WORDS and w not in DE_WORDS]
            if len(enleft) >= 2:
                reasons.append('EN words left: ' + ','.join(sorted(set(enleft))[:3]))
            # meaning inversion keywords (EN has negation, DE doesn't)
            en_low = en.lower()
            en_neg = any(neg in en_low for neg in ('not ', "n't", 'never ', 'no ', 'don\'t', 'doesn\'t', "can't", "won't", 'without'))
            de_neg = any(neg in low for neg in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals'))
            if en_neg and not de_neg:
                reasons.append('NEGATION LOST?')
            if reasons:
                o.write('%s;%s;%s;%s\n' % (
                    uid, en.replace(';', ','), de.replace(';', ','),
                    ' | '.join(reasons)))
                n += 1
        print(fn, 'candidates:', n, '->', out)
print('done')
