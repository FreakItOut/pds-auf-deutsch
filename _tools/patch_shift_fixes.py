# uid-exact patcher for sheared/misaligned German rows in TWN_*_PRG files.
# spec: (file_stem, uid_or_en, new_de). uid>0 = patch only that row;
# uid=0 = patch every row in the csv whose EN matches.
import os, sys, csv

SECT, DATA = 2352, 2048

SPEC = [
    # ---------------- TWN_E022 ----------------
    ('TWN_E022_PRG', 0, 'Ausgrabungsort'),
    ('TWN_E022_PRG', 1, '(Mein Chef!!!'),
    ('TWN_E022_PRG', 2, '(Da ist %a1...'),
    ('TWN_E022_PRG', 3, 'Er wartet wohl auf mich...)'),
    ('TWN_E022_PRG', 4, 'Ausgrabung verlassen'),
    ('TWN_E022_PRG', 6, 'Motor eines Kampfschiffs.'),
    ('TWN_E022_PRG', 7, '(Daten-Speicherkapsel.)'),
    ('TWN_E022_PRG', 8, '(...Wertvolle Sachen sind weg.'),
    ('TWN_E022_PRG', 11, '(Es ist nutzlos. Nichts mehr da.)'),
    ('TWN_E022_PRG', 12, '(Die Bruecke ist zerstoert.'),
    ('TWN_E022_PRG', 13, 'Kein Weg zur anderen Seite.)'),
    ('TWN_E022_PRG', 14, '(Jetzt weiss ich:'),
    ('TWN_E022_PRG', 15, 'Vom Verrueckten abgeschossen.'),
    ('TWN_E022_PRG', 16, '...Wie ueberlebte ich nur?)'),
    ('TWN_E022_PRG', 17, '(Alter Behaelter.)'),
    ('TWN_E022_PRG', 20, '(Nutzlos. Nichts drin.)'),
    ('TWN_E022_PRG', 21, '(Es ist ein Relikt der Vorzeit.'),
    ('TWN_E022_PRG', 22, '(Eingang zu den Ruinen.)'),
    ('TWN_E022_PRG', 23, '(Eingang durch Schutt verstopft.)'),
    ('TWN_E022_PRG', 24, 'Ruinen erforschen?'),
    ('TWN_E022_PRG', 25, 'Verdammt: wer war vor mir?'),
    ('TWN_E022_PRG', 26, 'und nahm hier alles.'),
    ('TWN_E022_PRG', 27, 'Wenn ich doch frueher hier!'),
    ('TWN_E022_PRG', 28, 'Schwarze Flotte war da.'),
    ('TWN_E022_PRG', 29, 'Sie haben sich diesmal'),
    ('TWN_E022_PRG', 30, 'uebertroffen.'),
    ('TWN_E022_PRG', 31, 'Was planen sie?'),
    ('TWN_E022_PRG', 32, 'Schon gut...'),
    ('TWN_E022_PRG', 33, 'Ich bleib jetzt hier.'),
    ('TWN_E022_PRG', 34, '(Azel starrt aufs Relikt.)'),
    ('TWN_E022_PRG', 35, 'Bevor Craymen kam,'),
    ('TWN_E022_PRG', 36, 'sah ich Orte mit Atolm.'),
    ('TWN_E022_PRG', 37, 'Bin nie zu Fuss gelaufen.'),
    ('TWN_E022_PRG', 38, 'Ich fuerchte den Turm,'),
    ('TWN_E022_PRG', 39, 'aber nicht fuer immer.'),
    ('TWN_E022_PRG', 40, 'Ich muss wissen, was war.'),
    ('TWN_E022_PRG', 41, '(Ich beende das...'),
    ('TWN_E022_PRG', 42, 'fuer sie und fuer mich!)'),
    ('TWN_E022_PRG', 43, 'Radgams Leib liegt tot'),
    ('TWN_E022_PRG', 44, 'als Geruemmel da.'),
    ('TWN_E022_PRG', 45, 'Ruecken gebrochen'),
    ('TWN_E022_PRG', 46, 'und sein Blut entleert.)'),
    ('TWN_E022_PRG', 47, 'Ein Jaeger haette'),
    ('TWN_E022_PRG', 48, 'dieses gewollt.)'),
    ('TWN_E022_PRG', 49, 'Abgetrennte Hand haelt Gewehr.'),
    ('TWN_E022_PRG', 50, 'Wenigstens kaempfend.)'),
    ('TWN_E022_PRG', 51, '(...Da hat jemand gefressen.)'),
    ('TWN_E022_PRG', 52, '(Radgam, der Jaeger.'),
    ('TWN_E022_PRG', 53, 'Er starb als Jaeger.)'),
    ('TWN_E022_PRG', 54, '(Zerfetzte Leiche...)'),
    ('TWN_E022_PRG', 55, '(...Verrottet.)'),
    ('TWN_E022_PRG', 56, '(Leere Augenhoehlen starren...)'),
    ('TWN_E022_PRG', 57, 'O8lrudnf##LRUDNF'),
    ('TWN_E022_PRG', 58, 'Disp Kollision'),
    ('TWN_E022_PRG', 59, 'Teil kaufen'),
    ('TWN_E022_PRG', 60, 'Verk. Teil'),

    # ---------------- TWN_JIRI ----------------
    ('TWN_JIRI_PRG', 3, '(Der Aufzug ist verriegelt.)'),
    ('TWN_JIRI_PRG', 4, 'Der Schluessel...'),
    ('TWN_JIRI_PRG', 5, '(Schloss zu weit weg.)'),
    ('TWN_JIRI_PRG', 7, 'Zu weit, um zu aktivieren...)'),
    ('TWN_JIRI_PRG', 9, 'Verschlossen, bewegt nicht...'),
    ('TWN_JIRI_PRG', 12, 'Naeher, um ihn zu nutzen.)'),
    ('TWN_JIRI_PRG', 16, 'Von hier nicht erkennbar.)'),
    ('TWN_JIRI_PRG', 18, 'Vielleicht genauer ansehen...)'),
    ('TWN_JIRI_PRG', 21, '(Es ist leer.)'),
    ('TWN_JIRI_PRG', 23, 'Verschlossen, bewegt nicht.'),
    ('TWN_JIRI_PRG', 24, 'Ich muss entsperren.)'),

    # ---------------- TWN_CAMP ----------------
    ('TWN_CAMP_PRG', 52, '(Eingeweide in Antiseptikum'),
    ('TWN_CAMP_PRG', 53, 'verwahrt. Nuetzt noch.)'),
    ('TWN_CAMP_PRG', 55, '(Uralte Fundstuecke, Werkzeug'),
    ('TWN_CAMP_PRG', 56, 'handgemacht. Vielleicht was drin.)'),
    ('TWN_CAMP_PRG', 111, 'Baicah erzaehlte es mir.'),
    ('TWN_CAMP_PRG', 161, 'Hast Rauls Geschichte gehoert?'),
    ('TWN_CAMP_PRG', 162, 'Tu mir einen Gefallen:'),
    ('TWN_CAMP_PRG', 171, 'eine arme Familie, koennen'),
    ('TWN_CAMP_PRG', 346, 'Oh, sag Papa nichts.'),
    ('TWN_CAMP_PRG', 378, 'Das Schiff! Ist das nicht gross?'),
    ('TWN_CAMP_PRG', 379, 'Papa fand es!'),
    ('TWN_CAMP_PRG', 380, 'Das Essen hier ist gut!'),
    ('TWN_CAMP_PRG', 381, 'Wie weit gehen wir?'),
    ('TWN_CAMP_PRG', 382, 'Papa sagt es nicht.'),
    ('TWN_CAMP_PRG', 501, 'Schau, da kommt der Jaeger.'),
    ('TWN_CAMP_PRG', 502, 'Was? Nichts aendert, wenn du'),
    ('TWN_CAMP_PRG', 549, 'ihn, er bleibt im'),
    ('TWN_CAMP_PRG', 550, 'Herzen weiter.'),
    ('TWN_CAMP_PRG', 551, 'Reist du alleine?'),
    ('TWN_CAMP_PRG', 552, 'In deinem Alter muss es'),
    ('TWN_CAMP_PRG', 553, 'schwer sein...'),
    ('TWN_CAMP_PRG', 554, 'Seltene Gegenstaende?'),
    ('TWN_CAMP_PRG', 555, 'Wenn ja: zeig sie meinem Mann.'),
    ('TWN_CAMP_PRG', 556, 'Wenn Gash dich schickte,'),
    ('TWN_CAMP_PRG', 557, 'versteckst du was, oder?'),
    ('TWN_CAMP_PRG', 558, 'Graebst du die Ruinen aus,'),
    ('TWN_CAMP_PRG', 559, 'wie die Sucher?'),
    ('TWN_CAMP_PRG', 560, 'Sie ist so schuechtern...'),
    ('TWN_CAMP_PRG', 561, 'Aber sehr fleissig.'),
    ('TWN_CAMP_PRG', 562, 'Musstest du was Seltsames'),
    ('TWN_CAMP_PRG', 563, 'kaufen?'),
    ('TWN_CAMP_PRG', 564, 'Fordere Dein Geld ein, wenn'),
    ('TWN_CAMP_PRG', 565, 'du magst.'),
    ('TWN_CAMP_PRG', 566, 'Nur Mut, ok?'),
    ('TWN_CAMP_PRG', 567, 'Kou, Baicahs Frau.'),
    ('TWN_CAMP_PRG', 568, 'Freut mich.'),
    ('TWN_CAMP_PRG', 569, 'Wie grausam ist das Reich?'),
    ('TWN_CAMP_PRG', 570, 'So weit kamen wir, und das?'),
    ('TWN_CAMP_PRG', 571, 'Wir duerfen wohl noch warten,'),
    ('TWN_CAMP_PRG', 572, 'eh wir uns niederlassen.'),
    ('TWN_CAMP_PRG', 573, "Zumindest durfte An'jou"),
    ('TWN_CAMP_PRG', 574, 'bei Sohn letztes Mal.'),
    ('TWN_CAMP_PRG', 575, 'Ein kleiner Trost fuer ihn...'),
    ('TWN_CAMP_PRG', 576, 'Quest beendet?'),
    ('TWN_CAMP_PRG', 577, 'Es gibt viel Essen hier.'),
    ('TWN_CAMP_PRG', 578, 'Das hilft sehr.'),
    ('TWN_CAMP_PRG', 579, 'Schoener Ort, oder?'),
    ('TWN_CAMP_PRG', 582, 'haette es sehen.'),
    ('TWN_CAMP_PRG', 583, 'Werde sesshaft.'),
    ('TWN_CAMP_PRG', 584, 'Nicht immer auf Abenteuern'),
    ('TWN_CAMP_PRG', 585, 'gehn, oder?'),
    ('TWN_CAMP_PRG', 745, 'Ich glaube, du'),
    ('TWN_CAMP_PRG', 746, 'sagst niemandem was.'),

    # ---------------- TWN_RUIN ----------------
    ('TWN_RUIN_PRG', 220, 'Geht es um deinen Drachen?'),    ('TWN_RUIN_PRG', 265, 'aus Naehe.'),
    ('TWN_RUIN_PRG', 267, 'Wohin gehst du?'),
    ('TWN_RUIN_PRG', 268, 'Ich war nie'),
    ('TWN_RUIN_PRG', 269, 'ausserhalb von Zoah.'),
    ('TWN_RUIN_PRG', 270, 'Warum nicht Sucher werden?'),
    ('TWN_RUIN_PRG', 271, 'Hat Gash dich geschickt?'),
    ('TWN_RUIN_PRG', 272, 'Nein, nur dass...'),
    ('TWN_RUIN_PRG', 275, 'zu dir, wegen Drachen.'),
    ('TWN_RUIN_PRG', 276, 'Ich bin nur ein Typ.'),
    ('TWN_RUIN_PRG', 277, 'Du denkst nicht, ich haette'),
    ('TWN_RUIN_PRG', 278, 'gegen die antike Technologie!?'),
    ('TWN_RUIN_PRG', 279, 'Alle kaempfen gegen die'),
    ('TWN_RUIN_PRG', 280, 'antiken Uebel.'),
    ('TWN_RUIN_PRG', 281, 'Die Uebel von Sestren.'),
    ('TWN_RUIN_PRG', 282, 'Du und Sucher gleich.'),
    ('TWN_RUIN_PRG', 283, 'Alle vertrieben'),
    ('TWN_RUIN_PRG', 284, 'aus ihrer Heimat...'),
    ('TWN_RUIN_PRG', 285, 'Bin ich ehrlich nuetzlich?'),
    ('TWN_RUIN_PRG', 286, 'Red nicht so. Mit deinen'),
    ('TWN_RUIN_PRG', 287, 'Faehigkeiten hilft man.'),
    ('TWN_RUIN_PRG', 288, 'Sucher wissen wohl,'),
    ('TWN_RUIN_PRG', 289, 'was du drauf hast.'),
    ('TWN_RUIN_PRG', 290, 'Du hast wohl recht.'),
    ('TWN_RUIN_PRG', 291, 'Dein Luftschiff?'),
    ('TWN_RUIN_PRG', 292, 'Berzer auch tot.'),
    ('TWN_RUIN_PRG', 293, 'Wusste nie, dass die echte Welt'),
    ('TWN_RUIN_PRG', 294, 'so gefaehrlich ist.'),
    ('TWN_RUIN_PRG', 295, 'Vermiss wirklich alles'),
    ('TWN_RUIN_PRG', 296, '(Verwirrt...)'),
    ('TWN_RUIN_PRG', 297, '(Paet sicher.)'),
    ('TWN_RUIN_PRG', 298, 'Sucher verlassen wohl'),
    ('TWN_RUIN_PRG', 299, 'diesen Ort.'),
    ('TWN_RUIN_PRG', 300, 'Ich hab viel nachgedacht...'),
    ('TWN_RUIN_PRG', 301, 'und begleite sie.'),
    ('TWN_RUIN_PRG', 302, 'Wird dauerhaft sicherer und'),
    ('TWN_RUIN_PRG', 303, 'Arbeit geht dann weiter.'),
    ('TWN_RUIN_PRG', 304, 'Niemand weiss, wann oder wie'),
    ('TWN_RUIN_PRG', 305, 'Leben endet,'),
    ('TWN_RUIN_PRG', 306, 'nur das Ende.'),
    ('TWN_RUIN_PRG', 307, 'Wenn Sucher forschen,'),
    ('TWN_RUIN_PRG', 308, 'geht Lebenswerk weiter,'),
    ('TWN_RUIN_PRG', 309, 'und die Welt besser machen.'),
    ('TWN_RUIN_PRG', 310, 'Genau.'),
    ('TWN_RUIN_PRG', 311, 'Chance gut, wir sehen uns'),
    ('TWN_RUIN_PRG', 312, 'als Sucher wieder.'),
    ('TWN_RUIN_PRG', 314, 'Ich muss mit Azel zum Turm.'),
    ('TWN_RUIN_PRG', 315, 'Bin gleich wieder hier.'),
    ('TWN_RUIN_PRG', 316, 'Du schaffst das schon.'),
    ('TWN_RUIN_PRG', 317, 'Tu, was du musst und'),
    ('TWN_RUIN_PRG', 318, 'komm zurueck.'),
    ('TWN_RUIN_PRG', 319, '(Hoffe wir ueberleben...)'),
    ('TWN_RUIN_PRG', 320, 'Schau diese Relikte...'),
    ('TWN_RUIN_PRG', 321, 'Viel zu tun...'),
    ('TWN_RUIN_PRG', 322, 'Beneide dich...'),
    ('TWN_RUIN_PRG', 323, 'Kannst vielen Leuten helfen.'),
    ('TWN_RUIN_PRG', 324, 'Paet! Du lebst!'),
    ('TWN_RUIN_PRG', 325, 'Entkam im Luftschiff, aber'),
    ('TWN_RUIN_PRG', 326, 'es stuerzte kurz ab.'),
    ('TWN_RUIN_PRG', 327, 'Sucher fanden mich lebend.'),
    ('TWN_RUIN_PRG', 328, 'Jetzt ist Zoah Ruine.'),
    ('TWN_RUIN_PRG', 329, 'Von Goettern bewacht? Pff.'),
    ('TWN_RUIN_PRG', 330, 'Es tut mir leid...'),
    ('TWN_RUIN_PRG', 331, 'Keine Sorge.'),
    ('TWN_RUIN_PRG', 333, 'Ich bin Reuben, Lehrling.'),
    ('TWN_RUIN_PRG', 334, 'Freut mich.'),
    ('TWN_RUIN_PRG', 335, 'Also ist er freundlich?'),
    ('TWN_RUIN_PRG', 336, 'Ausbildung laeuft.'),
    ('TWN_RUIN_PRG', 337, 'Will Training beenden'),
    ('TWN_RUIN_PRG', 338, 'damit ich sie im Kampf nutze.'),
    ('TWN_RUIN_PRG', 374, 'Es tut mir leid.'),
    ('TWN_RUIN_PRG', 415, 'Kam lebend zurueck.)'),
    ('TWN_RUIN_PRG', 416, 'Fuer Drachenreiter siehst du nicht'),
    ('TWN_RUIN_PRG', 419, 'in die Schlacht fuehren?'),
    ('TWN_RUIN_PRG', 420, 'Schau dich um.'),
    ('TWN_RUIN_PRG', 421, 'Das ging hart rein.'),
    ('TWN_RUIN_PRG', 422, 'Azel fand wohl heraus,'),
    ('TWN_RUIN_PRG', 423, 'warum wir sie schuetzten.'),
    ('TWN_RUIN_PRG', 424, 'Der Wald brennt, bis sich der'),
    ('TWN_RUIN_PRG', 425, 'Mond wandelt.'),
    ('TWN_RUIN_PRG', 500, 'Bringt dein Drache Sestren um,'),
    ('TWN_RUIN_PRG', 501, 'wird die Welt von den'),
    ('TWN_RUIN_PRG', 502, 'Uebeln der Vorzeit.'),
    ('TWN_RUIN_PRG', 503, 'Wir wussten, dass etwas kommt,'),
    ('TWN_RUIN_PRG', 504, 'um uns vom Turm zu befreien.'),
    ('TWN_RUIN_PRG', 505, 'Erst kuerzlich haben wir'),
    ('TWN_RUIN_PRG', 507, 'Dein Drache rettet uns.'),
    ('TWN_RUIN_PRG', 508, 'Drachen sollten die'),
    ('TWN_RUIN_PRG', 510, 'Doch deiner ist anders berufen.'),
    ('TWN_RUIN_PRG', 512, 'Azel verschwand im Kampf.'),
]

def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1 else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
            if int(r['lba']) > 0 and int(r['size']) > 0}

def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])

def write_file_regions(binp, lba, filedata):
    with open(binp, 'r+b') as f:
        for k in range((len(filedata) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(filedata[k * DATA:(k + 1) * DATA])

csvs = {}
for stem in ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG'):
    rows = {}
    with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
        for line in f:
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6:
                uid = int(p[0])
                offs = [int(x) for x in p[3].split('|') if x]
                rows.setdefault(uid, []).append({'uid': uid, 'off0': int(p[2]), 'offs': offs,
                                                 'len': int(p[1]), 'en': p[4], 'de': p[5]})
    csvs[stem] = rows

errors, applied, skipped, changed_states = [], 0, 0, []

# group by stem+disc so each file is read/written once
by_sd = {}
for stem, uid, new in SPEC:
    for d in (1, 2, 3, 4):
        by_sd.setdefault((stem, d), []).append((uid, new))

def actual_str(data, o):
    end = o
    while end < len(data) and data[end] not in (0x00, 0xFF):
        end += 1
    return bytes(data[o:end]).decode('latin1'), end

for (stem, d) in sorted(by_sd):
    name = stem.replace('_PRG', '.PRG')
    idx = fs_index(d)
    if name not in idx:
        continue
    lba, size = idx[name]
    binp = '_work/patched_disc%d.bin' % d
    data = bytearray(read_file(binp, lba, size))
    changed = False
    for uid, new in by_sd[(stem, d)]:
        entries = csvs.get(stem, {}).get(uid)
        if not entries:
            errors.append('%s uid=%d: NOT FOUND in csv' % (stem, uid))
            continue
        for e in entries:
            targets = e['offs'] or [e['off0']]
            for o in targets:
                if o < 0 or o >= len(data):
                    errors.append('%s uid=%d off=%d: OOB (file size %d)' % (stem, uid, o, len(data)))
                    continue
                actual, nend = actual_str(data, o)
                old = e['de'].rstrip()
                if actual == new:
                    skipped += 1
                    continue
                if actual != old:
                    errors.append('%s uid=%d off=%d DISC=%r CSV=%r EN=%r'
                                  % (stem, uid, o, actual, old, e['en'][:60]))
                    continue
                new_b = new.encode('latin1')
                en_b = e['en'].encode('latin1')
                if len(new_b) > len(en_b):
                    errors.append('%s uid=%d off=%d TOO LONG (%d > %d)' % (stem, uid, o, len(new_b), len(en_b)))
                    continue
                slot_end = nend + 1
                while slot_end < len(data) and data[slot_end] == 0xFF:
                    slot_end += 1
                data[o:o + len(new_b)] = new_b
                for k in range(o + len(new_b), slot_end):
                    data[k] = 0x00 if k == o + len(new_b) else 0xFF
                changed_states.append((stem, d, o, new))
                applied += 1
                changed = True
    if changed:
        write_file_regions(binp, lba, bytes(data))
        chk = read_file(binp, lba, size)
        for s2, d2, o, new in changed_states:
            if s2 == stem and d2 == d:
                nb = new.encode('latin1')
                a2, _ = actual_str(chk, o)
                if a2 != new:
                    errors.append('%s disc=%d off=%d READBACK %r != %r' % (stem, d, o, a2, new))

# sync subtitle CSVs with new values so future text-scan patches stay valid
sync_n = 0
for stem in set(s for s, _, _, _ in changed_states):
    path = '_work/subtitles/%s_de.csv' % stem
    upd = {}
    for s2, d2, o, new in changed_states:
        if s2 == stem:
            upd[str(o)] = new
    lines = open(path, encoding='latin1').read().split('\n')
    result = []
    for line in lines:
        p = line.rstrip('\r').split(';')
        if line.strip() and len(p) >= 6:
            headers = p[3].split('|')
            hit = None
            if p[2] in upd:
                hit = upd[p[2]]
            else:
                cand = [(i, upd[h]) for i, h in enumerate(headers) if h in upd]
                if len(set(v for i, v in cand)) == 1:
                    hit = cand[0][1]
                elif cand:
                    result.append(line)
                    errors.append('%s: ambiguous offset keys %r' % (path, cand))
                    continue
            if hit is not None and hit != p[5]:
                p[5] = hit
                sync_n += 1
            result.append(';'.join(p))
        else:
            result.append(line)
    with open(path, 'w', encoding='latin1', newline='\n') as fh:
        fh.write('\n'.join(result))

print('applied=%d skipped=%d csv_synced=%d' % (applied, skipped, sync_n))
errfile = open('_work/review_fixes/shift_errors.txt', 'w', encoding='latin1', newline='\n')
errfile.write('\n'.join(errors))
errfile.close()
if errors:
    print('ERRORS (%d):' % len(errors))
    for x in errors[:60]:
        print('  ' + x)
else:
    print('ERRORS: none')
