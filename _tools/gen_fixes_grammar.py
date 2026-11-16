# Generate curated grammar/shift fixes for TWN_*_PRG subtitle files.
# Format: source_file;en;old_de;new_de;reason
FIX = [
    # ---------- TWN_E022 ----------
    ('TWN_E022_PRG', "(It's my Captain!!!)", '(Es ist mein Kapitae', '(Mein Chef!!!'),
    ('TWN_E022_PRG', "(There's my %a1...", '(Da ist mein %a1..', '(Da ist %a1...'),
    ('TWN_E022_PRG', "Looks like he's waiting for me...)", 'Sieht aus, als ob er auf mich wart', 'Er wartet wohl auf mich...)'),
    ('TWN_E022_PRG', 'Exit the Excavation Site', 'Verlasse die Ausgrabungs', 'Ausgrabung verlassen'),
    ('TWN_E022_PRG', "It's a battleship's engine.)", 'Es ist der Motor eines Schla', 'Motor eines Kampfschiffs.'),
    ('TWN_E022_PRG', '(A Data Storage Capsule.)', '(Eine Daten-Speicherkapse', '(Daten-Speicherkapsel.)'),
    ('TWN_E022_PRG', '(...All the valuable items are gone.', '(...Alle wertvollen Gegenstaende sin', '(...Wertvolle Sachen sind weg.'),
    ('TWN_E022_PRG', "(It's no use. There's nothing left.)", '(Es ist nutzlos. Es ist nichts mehr ', '(Es ist nutzlos. Nichts mehr da.)'),
    ('TWN_E022_PRG', '(The bridge was destroyed...', '(Die Bruecke wurde zerstoert', '(Die Bruecke ist zerstoert.'),
    ('TWN_E022_PRG', "There's no way to the other side...)", 'Es gibt keinen Weg zur anderen Seite', 'Kein Weg zur anderen Seite.)'),
    ('TWN_E022_PRG', '(I remember now...', '(Ich erinnere mich', '(Jetzt weiss ich:'),
    ('TWN_E022_PRG', 'That madman shot me off the bridge.', 'Dieser Verrueckte schoss mich von d', 'Vom Verrueckten abgeschossen.'),
    ('TWN_E022_PRG', '...How did I survive the fall?)', '...Wie habe ich den Sturz ueber', '...Wie ueberlebte ich nur?)'),
    ('TWN_E022_PRG', '(An old Container.)', '(Ein alter Containe', '(Alter Behaelter.)'),
    ('TWN_E022_PRG', "(No use. There's nothing inside.)", '(Nutzlos. Es ist nichts drin.)', '(Nutzlos. Nichts drin.)'),
    ('TWN_E022_PRG', "(It's a relic from the Ancient Age.", '(Es ist ein Relikt aus dem Altertum', '(Es ist ein Relikt der Vorzeit.'),
    ('TWN_E022_PRG', '(The entrance to the ruins.)', '(Der Eingang zu den Ruinen.)', '(Eingang zu den Ruinen.)'),
    ('TWN_E022_PRG', '(The entrance is blocked by rubble.)', '(Der Eingang ist durch Schutt blocki', '(Eingang durch Schutt verstopft.)'),
    ('TWN_E022_PRG', "I'd love to explore these", 'Ich wuerde gerne diese', 'Ruinen erforschen?'),
    ('TWN_E022_PRG', 'Damn, someone got here before', 'ruinen erforschen, aber...', 'Verdammt: wer war vor mir?'),
    ('TWN_E022_PRG', 'me and took everything...', 'Verdammt, jemand war vor ', 'und nahm hier alles.'),
    ('TWN_E022_PRG', "If only I'd gotten here sooner.", 'und nahm alles mit...', 'Wenn ich doch frueher hier!'),
    ('TWN_E022_PRG', 'The Black Fleet was here.', 'Wenn ich nur frueher hier', 'Schwarze Flotte war da.'),
    ('TWN_E022_PRG', "I wonder what they're up to.", 'uebertroffen.', 'Was planen sie?'),
    ('TWN_E022_PRG', 'They have really outdone', 'Die Schwarze Flotte war ', 'Sie haben sich diesmal'),
    ('TWN_E022_PRG', 'themselves this time.', 'Sie haben sich diesma', 'uebertroffen.'),
    ('TWN_E022_PRG', "It's all right...", 'Ich frage mich, w', 'Schon gut...'),
    ('TWN_E022_PRG', "I won't leave you again.", 'Es ist in Ordnung...', 'Ich bleib jetzt hier.'),
    ('TWN_E022_PRG', '(Azel keeps staring at the relic.)', 'Ich werde dich nicht wieder verlas', '(Azel starrt aufs Relikt.)'),
    ('TWN_E022_PRG', 'Before Craymen woke me,', '(Azel starrt weiter auf', 'Bevor Craymen kam,'),
    ('TWN_E022_PRG', 'I saw many places with Atolm.', 'Bevor Craymen mich weckte,', 'sah ich Orte mit Atolm.'),
    ('TWN_E022_PRG', 'But I never walked the land.', 'sah ich viele Orte mit Atolm', 'Bin nie zu Fuss gelaufen.'),
    ('TWN_E022_PRG', "I'm still afraid of the Tower,", 'Aber ich ging nie zu Fuss.', 'Ich fuerchte den Turm,'),
    ('TWN_E022_PRG', "but I can't be afraid forever.", 'Ich fuerchte den Turm immer no', 'aber nicht fuer immer.'),
    ('TWN_E022_PRG', 'I need to know what happened.', 'aber ich kann nicht fuer imme', 'Ich muss wissen, was war.'),
    ('TWN_E022_PRG', '(I must end this...', 'Ich muss wissen, wa', '(Ich beende das...'),
    ('TWN_E022_PRG', 'for her sake as well as mine!)', '(Ich muss dies beenden...', 'fuer sie und fuer mich!)'),
    ('TWN_E022_PRG', "(Radgam's lifeless body lies", 'fuer ihre sake sowie fuer me', 'Radgams Leib liegt tot'),
    ('TWN_E022_PRG', 'in a crumpled heap.', '(Radgams lebloser K', 'als Geruemmel da.'),
    ('TWN_E022_PRG', 'His back has been broken and', 'in einem Haufen zusammen.', 'Ruecken gebrochen'),
    ('TWN_E022_PRG', 'his blood has been drained.)', 'Sein Ruecken wurde gebrochen', 'und sein Blut entleert.)'),
    ('TWN_E022_PRG', '(He would have wanted a', 'sein Blut wurde ausgesa', 'Ein Jaeger haette'),
    ('TWN_E022_PRG', 'hunter to have this.)', '(Er haette gewollt, d', 'dieses gewollt.)'),
    ('TWN_E022_PRG', 'His severed hand still grips a gun.', 'Seine abgetrennte Hand haelt ', 'Abgetrennte Hand haelt Gewehr.'),
    ('TWN_E022_PRG', 'At least he died fighting...)', 'Jaeger dies hat.)', 'Wenigstens kaempfend.)'),
    ('TWN_E022_PRG', "(...A body something's fed on.)", 'Zumindest starb er kaempfend...', '(...Da hat jemand gefressen.)'),
    ('TWN_E022_PRG', "(It's Radgam, the hunter.", '(...Ein Koerper, von dem ', '(Radgam, der Jaeger.'),
    ('TWN_E022_PRG', "He died a hunter's death.)", '(Es ist Radgam, der Jaeger', 'Er starb als Jaeger.)'),
    ('TWN_E022_PRG', "(It's a mangled corpse...)", 'Er starb einen Jaegertod.)', '(Zerfetzte Leiche...)'),
    ('TWN_E022_PRG', '(A rotting corpse...)', '(Es ist eine verstuem', '(...Verrottet.)'),
    ('TWN_E022_PRG', '(Empty eye sockets stare at you...)', '(Eine verrottende Leiche...)', '(Leere Augenhoehlen starren...)'),
    ('TWN_E022_PRG', 'O8lrudnf##LRUDNF', '(Leere Augenhoeh', 'O8lrudnf##LRUDNF'),
    ('TWN_E022_PRG', 'Disp Collision', 'O8lrudnf##LRUD', 'Disp Collision'),
    ('TWN_E022_PRG', 'Buy Gun Part', 'Disp Collisi', 'Teil kaufen'),
    ('TWN_E022_PRG', 'Sell Gun Part', 'Buy Gun Part', 'Verk. Teil'),

    # ---------- TWN_JIRI ----------
    ('TWN_JIRI_PRG', "(The elevator's security lock.", '(Der Sicherheitsschloss des Au', '(Der Aufzug ist verriegelt.)'),
    ('TWN_JIRI_PRG', 'I need the key...)', 'Ich brauche den Sc', 'Der Schluessel...'),
    ('TWN_JIRI_PRG', '(The lock is out of reach...)', '(Das Schloss ist ausser Reich', '(Schloss zu weit weg.)'),
    ('TWN_JIRI_PRG', "It's too far away to activate...)", 'Es ist zu weit weg, um zu aktivie', 'Zu weit, um zu aktivieren...)'),
    ('TWN_JIRI_PRG', "It's locked, and it won't move...", 'Er ist verschlossen und bewegt si', 'Verschlossen, bewegt nicht...'),
    ('TWN_JIRI_PRG', "I'll need to get closer to use it.)", 'Ich muss naeher kommen, um ihn zu b', 'Naeher, um ihn zu nutzen.)'),
    ('TWN_JIRI_PRG', "I can't tell from this angle.)", 'Ich kann es aus diesem Winkel ', 'Von hier nicht erkennbar.)'),
    ('TWN_JIRI_PRG', 'Maybe I should take a closer look...)', 'Vielleicht sollte ich genauer hinsehe', 'Vielleicht genauer ansehen...)'),
    ('TWN_JIRI_PRG', "(It's empty...)", '(Es ist leer...', '(Es ist leer...)'),
    ('TWN_JIRI_PRG', "It's locked, and it won't move.", 'Er ist verschlossen und bewegt ', 'Verschlossen, bewegt nicht.'),
    ('TWN_JIRI_PRG', 'I need to unlock it.)', 'Ich muss ihn entsperr', 'Ich muss entsperren.)'),

    # ---------- TWN_CAMP ----------
    ('TWN_CAMP_PRG', 'Baicah told me what you did.', 'Baicah erzaehlte, was du tat', 'Baicah erzaehlte es mir.'),
    ('TWN_CAMP_PRG', "You've heard Raul's story, right?", 'Rauls Geschichte gehoert?', 'Hast Rauls Geschichte gehoert?'),
    ('TWN_CAMP_PRG', "Do me a favor, and don't tell", 'Tu mir einen Gefallen', 'Tu mir einen Gefallen:'),
    ('TWN_CAMP_PRG', "a poor family and we can't", 'eine arme Familie und', 'eine arme Familie, koennen'),
    ('TWN_CAMP_PRG', '(Intestines stored in an antiseptic.', '(Eingeweide in Behaeltern', '(Eingeweide in Antiseptikum'),
    ('TWN_CAMP_PRG', 'These could be useful.)', 'Das nutzt was.)', 'verwahrt. Nuetzt noch.)'),
    ('TWN_CAMP_PRG', '(Ancient finds, hand-crafted tools...', '(Uralte Fundstuecke,', '(Uralte Fundstuecke, Werkzeug'),
    ('TWN_CAMP_PRG', 'There may be something useful here.)', 'Vielleicht was Brauchbares drin.)', 'handgemacht. Vielleicht was drin.)'),
    ('TWN_CAMP_PRG', "Oh, don't tell my daddy.", 'Oh, Papa nichts sagen.', 'Oh, sag Papa nichts.'),
    ('TWN_CAMP_PRG', 'My daddy found it!', 'Papa hat gefunden!', 'Papa fand es!'),
    ('TWN_CAMP_PRG', 'The food here is good, you know!', 'Essen hier gut!', 'Das Essen hier ist gut!'),
    ('TWN_CAMP_PRG', 'How far are we gonna go?', 'Wie weit gehen?', 'Wie weit gehen wir?'),
    ('TWN_CAMP_PRG', "My daddy won't tell us.", 'Papa sagt nicht.', 'Papa sagt es nicht.'),
    ('TWN_CAMP_PRG', 'Look, here comes that hunter.', 'Schau, da kommt Jaeger.', 'Schau, da kommt der Jaeger.'),
    ('TWN_CAMP_PRG', 'What? Nothing changes, if you ', 'Was? Nichts aendert, wenn', 'Was? Nichts aendert, wenn du'),
    # order matters: 555 before 554 (duplicate old 'Zeige meinem Mann.')
    ('TWN_CAMP_PRG', 'If you do, show them to my husband.', 'Zeige meinem Mann.', 'Wenn ja: zeig sie meinem Mann.'),
    ('TWN_CAMP_PRG', 'Do you have any rare items?', 'Zeige meinem Mann.', 'Seltene Gegenstaende?'),
    # order matters: 579 before 578 (duplicate old 'Schoener Ort?')
    ('TWN_CAMP_PRG', "Nice place, isn't it?", 'Schoener Ort?', 'Schoener Ort, oder?'),
    ('TWN_CAMP_PRG', 'It helps us a lot.', 'Schoener Ort?', 'Das hilft sehr.'),
    # shifted block 548-585
    ('TWN_CAMP_PRG', "him and he'll live", 'in Herz leben.', 'ihn, er bleibt im'),
    ('TWN_CAMP_PRG', 'in your heart forever.', 'Reist du alleine?', 'Herzen weiter.'),
    ('TWN_CAMP_PRG', 'Are you traveling alone?', 'In Alter muss es', 'Reist du alleine?'),
    ('TWN_CAMP_PRG', 'At your age, it must be', 'schwer sein...', 'In deinem Alter muss es'),
    ('TWN_CAMP_PRG', 'tough for you...', 'Seltene?', 'schwer sein...'),
    ('TWN_CAMP_PRG', 'Hmm... if Gash sent you here,', 'versteckst du etwas, oder?', 'Wenn Gash dich schickte,'),
    ('TWN_CAMP_PRG', 'you must be hiding something, eh?', 'Graebst du die Ruinen aus,', 'versteckst du was, oder?'),
    ('TWN_CAMP_PRG', 'Are you digging up the ruins,', 'wie die Sucher?', 'Graebst du die Ruinen aus,'),
    ('TWN_CAMP_PRG', 'like the seekers?', 'Schuechtern...', 'wie die Sucher?'),
    ('TWN_CAMP_PRG', 'She is such a shy girl...', 'Aber arbeitet hart.', 'Sie ist so schuechtern...'),
    ('TWN_CAMP_PRG', 'But she works very hard.', 'Hat dich zum Kaufen', 'Aber sehr fleissig.'),
    ('TWN_CAMP_PRG', 'Did he make you buy another', 'gezwungen?', 'Musstest du was Seltsames'),
    ('TWN_CAMP_PRG', 'strange item?', 'Fordere.', 'kaufen?'),
    ('TWN_CAMP_PRG', 'Ask for your money back, if you', 'nicht willst.', 'Fordere Dein Geld ein, wenn'),
    ('TWN_CAMP_PRG', "don't want it.", 'Will es nicht.', 'du magst.'),
    ('TWN_CAMP_PRG', 'Feel free, okay?', 'Ich bin Kou.', 'Nur Mut, ok?'),
    ('TWN_CAMP_PRG', "I am Kou, Baicah's wife.", 'Schoen, dich zu treffen.', 'Kou, Baicahs Frau.'),
    ('TWN_CAMP_PRG', 'Nice to meet you.', 'Ruecksichtslos?', 'Freut mich.'),
    ('TWN_CAMP_PRG', 'How ruthless is the Empire?', 'Wir kamen weit.', 'Wie grausam ist das Reich?'),
    ('TWN_CAMP_PRG', 'We came this far and they do this.', 'Sieht aus, als muessten wir noch', 'So weit kamen wir, und das?'),
    ('TWN_CAMP_PRG', 'Looks like we have to wait a little', 'laenger warten...', 'Wir duerfen wohl noch warten,'),
    ('TWN_CAMP_PRG', 'longer before we can settle down...', "Wenigstens durfte An'jou bei", 'eh wir uns niederlassen.'),
    ('TWN_CAMP_PRG', "At least An'jou got to be with", 'Sohn letztes Mal sein.', "Zumindest durfte An'jou"),
    ('TWN_CAMP_PRG', 'his son one last time.', 'Kleiner Trost...', 'bei Sohn letztes Mal.'),
    ('TWN_CAMP_PRG', 'A small consolation for him...', 'Quest fertig?', 'Ein kleiner Trost fuer ihn...'),
    ('TWN_CAMP_PRG', 'Are you finished with your quest?', 'Es gibt viel Essen hier.', 'Quest beendet?'),
    ('TWN_CAMP_PRG', "There's lots of food around.", 'Hilft uns sehr.', 'Es gibt viel Essen hier.'),
    ('TWN_CAMP_PRG', 'could have seen it.', 'haette sehen.', 'haette es sehen.'),
    ('TWN_CAMP_PRG', 'You should settle down.', 'Du niederlassen.', 'Werde sesshaft.'),
    ('TWN_CAMP_PRG', "You can't keep adventuring", 'Nicht weiter abenteuern', 'Nicht immer auf Abenteuern'),
    ('TWN_CAMP_PRG', 'all your life, can you?', 'ganzes Leben, oder?', 'gehn, oder?'),
    ('TWN_CAMP_PRG', "I'm sure you won't", 'Ich sicher, du...', 'Ich glaube, du'),
    ('TWN_CAMP_PRG', 'tell anyone about them, right?', 'niemandem davon...', 'sagst niemandem was.'),
    ('TWN_CAMP_PRG', "I'm sure you won't", 'Ich sicher, du...#', 'X_unused'),

    # ---------- TWN_RUIN ----------
    ('TWN_RUIN_PRG', "Aren't they after your dragon?", 'Hinter deinem Drachen?', 'Geht es um deinen Drachen?'),
    ('TWN_RUIN_PRG', 'Where will you go?', 'Wohin gehen?', 'Wohin gehst du?'),
    ('TWN_RUIN_PRG', "I've never been", 'Wohin gehen?', 'Ich war nie'),
    ('TWN_RUIN_PRG', 'outside of Zoah before.', 'Ich war nie', 'ausserhalb von Zoah.'),
    ('TWN_RUIN_PRG', "Why don't you join the seekers?", 'Schliesst dich nicht an?', 'Warum nicht Sucher werden?'),
    ('TWN_RUIN_PRG', 'Did Gash put you up to this?', 'Warum nicht Sucher?', 'Hat Gash dich geschickt?'),
    ('TWN_RUIN_PRG', "No. It's just that...", 'Gash gebracht?', 'Nein, nur dass...'),
    ('TWN_RUIN_PRG', 'because you have that dragon.', 'weil du diesen Drachen hast.', 'zu dir, wegen Drachen.'),
    ('TWN_RUIN_PRG', "Me, I'm just an ordinary guy.", 'Ich bin gewoehnlicher Typ.', 'Ich bin nur ein Typ.'),
    ('TWN_RUIN_PRG', "You really don't think I'd have", 'Du denkst nicht, ich haette', 'Du denkst nicht, ich haette'),
    ('TWN_RUIN_PRG', 'Everyone is fighting against the', 'Alle kaempfen.', 'Alle kaempfen gegen die'),
    ('TWN_RUIN_PRG', 'ancient evils.', 'antiken Uebel.', 'antiken Uebel.'),
    ('TWN_RUIN_PRG', 'The evils spawned by Sestren.', 'Die Uebel, die Sestren gebar.', 'Uebel von Sestren.'),
    ('TWN_RUIN_PRG', 'You and the seekers are alike.', 'Du und Sucher.', 'Du und Sucher gleich.'),
    ('TWN_RUIN_PRG', 'They were all driven', 'Alle aus', 'Alle vertrieben'),
    ('TWN_RUIN_PRG', 'from their lands...', 'ihren Laendern vertrieben...', 'aus ihrer Heimat...'),
    ('TWN_RUIN_PRG', 'Honestly, am I useful to anybody?', 'Wie auch immer, nein.', 'Bin ich ehrlich nuetzlich?'),
    ('TWN_RUIN_PRG', "I'm sure the seekers are aware", 'Faehigkeiten helfen Leuten.', 'Sucher wissen wohl,'),
    ('TWN_RUIN_PRG', 'of your potential.', 'Sucher sind sich', 'was du drauf hast.'),
    ('TWN_RUIN_PRG', "I guess you're right.", 'Potenzials bewusst.', 'Du hast wohl recht.'),
    ('TWN_RUIN_PRG', 'Your airship crashed...', 'Ich denke, recht.', 'Dein Luftschiff?'),
    ('TWN_RUIN_PRG', 'Berzer must be dead too.', 'Luftschiff abgestuerzt.', 'Berzer auch tot.'),
    ('TWN_RUIN_PRG', 'I never knew that the real world', 'Wusste nicht, echte Welt', 'Wusste nie, dass die echte Welt'),
    ('TWN_RUIN_PRG', 'was such a dangerous place.', 'Wusste nie, echte Welt', 'so gefaehrlich ist.'),
    ('TWN_RUIN_PRG', "I'm really starting to miss", 'so gefaehrlich.', 'Vermiss wirklich alles'),
    ('TWN_RUIN_PRG', '(He looks baffled...)', 'Fange an zu vermissen', '(Verwirrt...)'),
    ('TWN_RUIN_PRG', '(Paet is safe.)', '(Verwirrt...)', '(Paet sicher.)'),
    ('TWN_RUIN_PRG', 'Looks like the seekers are', '(Paet ist sicher.)', 'Sucher verlassen wohl'),
    ('TWN_RUIN_PRG', 'abandoning this place.', 'Sieht aus, Sucher', 'diesen Ort.'),
    ('TWN_RUIN_PRG', "I've given it a lot of thought...", 'diesen Ort aufgeben.', 'Ich hab viel nachgedacht...'),
    ('TWN_RUIN_PRG', "and I've decided to go with them.", 'Ich habe viel nachgedacht...', 'und begleite sie.'),
    ('TWN_RUIN_PRG', "I'm sure it will be safer and", 'und entschieden mitzugehen.', 'Wird dauerhaft sicherer und'),
    ('TWN_RUIN_PRG', 'I want my work to continue.', 'Ich sicher, sicherer und', 'Arbeit geht dann weiter.'),
    ('TWN_RUIN_PRG', 'Nobody knows when or how their', 'meine Arbeit weitergeht.', 'Niemand weiss, wann oder wie'),
    ('TWN_RUIN_PRG', 'life will end,', 'Niemand...', 'Leben endet,'),
    ('TWN_RUIN_PRG', 'only that it will.', 'Leben enden,', 'nur das Ende.'),
    ('TWN_RUIN_PRG', 'If the seekers continue my', 'nur dass es wird.', 'Wenn Sucher forschen,'),
    ('TWN_RUIN_PRG', "research, my life's work will", 'Wenn Sucher Forschung', 'geht Lebenswerk weiter,'),
    ('TWN_RUIN_PRG', 'make this world a better place.', 'fortsetzen, Lebensarbeit', 'und die Welt besser machen.'),
    ('TWN_RUIN_PRG', "You're right.", 'Recht.', 'Genau.'),
    ('TWN_RUIN_PRG', "There's also a good chance that", 'Recht.', 'Chance gut, wir sehen uns'),
    ('TWN_RUIN_PRG', "we'll meet again if you're a seeker.", 'Gute Chance, dass', 'als Sucher wieder.'),
    ('TWN_RUIN_PRG', "You're not coming with us?", 'Nicht mit uns?', 'Kommst du nicht mit?'),
    ('TWN_RUIN_PRG', 'I must go to the Tower with Azel.', 'Du kommst nicht mit uns?', 'Ich muss mit Azel zum Turm.'),
    ('TWN_RUIN_PRG', "I'll return as soon as I'm done.", 'Zurueckkommen, sobald fertig.', 'Bin gleich wieder hier.'),
    ('TWN_RUIN_PRG', "I'm sure you'll be all right.", 'Ich sicher, in Ordnung.', 'Du schaffst das schon.'),
    ('TWN_RUIN_PRG', 'Do what you need to do and', 'Tu, was musst.', 'Tu, was du musst und'),
    ('TWN_RUIN_PRG', 'come back soon.', 'komm bald.', 'komm zurueck.'),
    ('TWN_RUIN_PRG', 'All this fighting for nothing.', 'All dieses Kaempfen...', 'All die Kaempfe umsonst.'),
    ('TWN_RUIN_PRG', "I'm sorry, I couldn't help more.", 'Leid, nicht mehr helfen.', 'Es tut mir leid.'),
    ('TWN_RUIN_PRG', "I'm sorry, I couldn't be of your", 'Leid, nicht helfen.', 'Tut mir leid, ich konnte'),
    ('TWN_RUIN_PRG', 'Look at all these relics...', 'Schau Relikte...', 'Schau diese Relikte...'),
    ('TWN_RUIN_PRG', 'So much work to be done.', 'Viel Arbeit.', 'Viel zu tun...'),
    ('TWN_RUIN_PRG', 'You can help so many people.', 'Kannst helfen.', 'Kannst vielen Leuten helfen.'),
    ('TWN_RUIN_PRG', 'I escaped in the airship, but', 'Entkam, aber', 'Entkam im Luftschiff, aber'),
    ('TWN_RUIN_PRG', 'it crashed shortly after.', 'stuerzte kurz ab.', 'es stuerzte kurz ab.'),
    ('TWN_RUIN_PRG', 'The seekers found me alive.', 'Sucher fanden lebend.', 'Sucher fanden mich lebend.'),
    ('TWN_RUIN_PRG', 'Zoah is now in ruins.', 'Zoah ist jetzt in Ruinen.', 'Jetzt ist Zoah Ruine.'),
    ('TWN_RUIN_PRG', 'Guarded by the Gods... My ass.', 'Bewacht von Goettern...', 'Von Goettern bewacht? Pff.'),
    ('TWN_RUIN_PRG', "I'm sorry about that...", 'Bewacht von Goettern...', 'Es tut mir leid...'),
    ('TWN_RUIN_PRG', "I'm Reuben. an apprentice quester.", 'Ich bin Reuben.', 'Ich bin Reuben, Lehrling.'),
    ('TWN_RUIN_PRG', "It's nice to meet you.", 'Schoen, dich.', 'Freut mich.'),
    ('TWN_RUIN_PRG', 'So, the dragon is friendly', 'Schoen, dich.', 'Also ist er freundlich?'),
    ('TWN_RUIN_PRG', "I'm still in training.", 'Noch in Ausbildung.', 'Ausbildung laeuft noch.'),
    ('TWN_RUIN_PRG', 'so I can use my skills in battle.', 'um Faehigkeiten einsetzen.', 'damit ich sie im Kampf nutze.'),
    ('TWN_RUIN_PRG', 'She returned alive.)', 'kehrte lebend.)', 'Kam lebend zurueck.)'),
    ('TWN_RUIN_PRG', "For a dragon rider, you don't look", 'Fuer Drachenreiter siehst nicht', 'Fuer Drachenreiter siehst du nicht'),
    ('TWN_RUIN_PRG', "into battle. Don't you think?", 'Schlacht. Findest du?', 'in die Schlacht fuehren?'),
    ('TWN_RUIN_PRG', 'Look around...', 'Schau um...', 'Schau dich um.'),
    ('TWN_RUIN_PRG', 'We took quite a beating.', 'Tracht Pruegel.', 'Das ging hart rein.'),
    ('TWN_RUIN_PRG', 'I guess Azel figured out', 'Ich denke, Azel fand', 'Azel fand wohl heraus,'),
    ('TWN_RUIN_PRG', 'why we were protecting her.', 'warum schuetzten.', 'warum wir sie schuetzten.'),
    ('TWN_RUIN_PRG', 'The forest will burn until the', 'Der Wald wird brennen, bis der', 'Der Wald brennt, bis sich der'),
    ('TWN_RUIN_PRG', 'moon changes.', 'Mond aendert.', 'Mond wandelt.'),
    ('TWN_RUIN_PRG', 'If your dragon can destroy Sestren,', 'Wenn Drache zerstoeren kann,', 'Bringt dein Drache Sestren um,'),
    ('TWN_RUIN_PRG', 'the world will be free from the', 'wird die Welt frei von den', 'wird die Welt von den'),
    ('TWN_RUIN_PRG', 'evils of the Ancient Age.', 'Uebeln des Vorzeits.', 'Uebeln der Vorzeit.'),
    ('TWN_RUIN_PRG', 'We knew that something would appear', 'Wir wussten, etwas erscheint.', 'Wir wussten, dass etwas kommt,'),
    ('TWN_RUIN_PRG', "to free us from the Tower's will.", 'um uns zu befreien.', 'um uns vom Turm zu befreien.'),
    ('TWN_RUIN_PRG', "It wasn't until recently that we", 'Erst kuerzlich wir', 'Erst kuerzlich haben wir'),
    ('TWN_RUIN_PRG', 'Your dragon is our salvation.', 'Dein Drache unsere Erloesung.', 'Dein Drache rettet uns.'),
    ('TWN_RUIN_PRG', 'Dragons were created to', 'Drachen geschaffen, um', 'Drachen sollten die'),
    ('TWN_RUIN_PRG', 'But yours has a different purpose.', 'Aber deiner anderen Zweck.', 'Doch deiner ist anders berufen.'),
    ('TWN_RUIN_PRG', 'Azel vanished during the battle.', 'Azel verschwand.', 'Azel verschwand im Kampf.'),
]

EN2 = {}
for src, en in [('TWN_CAMP_PRG', 'TWN_CAMP_PRG_de.csv'), ('TWN_RUIN_PRG', 'TWN_RUIN_PRG_de.csv'),
                ('TWN_E022_PRG', 'TWN_E022_PRG_de.csv'), ('TWN_JIRI_PRG', 'TWN_JIRI_PRG_de.csv')]:
    rows = {}
    for line in open('_work/subtitles/' + en, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            if p[4] not in rows:
                rows[p[4]] = p[5]
    EN2[src] = rows

bad_len = []
bad_old = []
dup_old = {}
out = open('_work/review_fixes/grammar_fixes.csv', 'w', encoding='latin1', newline='')
out.write('source_file;en;old_de;new_de;reason\n')
for src, en, old, new in FIX:
    if new in ('XXX_not_used', 'X_unused'):
        continue
    if len(new) > len(en):
        bad_len.append((src, en, new, len(new), len(en)))
        continue
    if ' ' in en or True:
        pass
    cur = EN2.get(src, {}).get(en)
    if cur is None:
        bad_old.append((src, en, 'EN NOT FOUND'))
        continue
    cur = cur.rstrip()
    if cur != old.rstrip() and not (cur == old or cur.rstrip() == old.rstrip()):
        # allow minor whitespace diffs
        if cur.lstrip() != old.lstrip():
            bad_old.append((src, en, 'OLD MISMATCH: csv=%r gen=%r' % (cur[:60], old[:60])))
            continue
    if old.rstrip() and old != cur and cur.rstrip() != old.rstrip():
        pass
    if src not in dup_old:
        dup_old[src] = {}
    key = old.rstrip()
    dup_old[src][key] = dup_old[src].get(key, 0) + 1
    out.write('%s;%s;%s;%s;grammar/shift fix\n' % (src, en, old, new))
out.close()
print('too long:', len(bad_len))
for b in bad_len:
    print('  %s | %r -> %r (%d > %d)' % (b[0], b[1][:45], b[2][:45], b[3], b[4]))
print('old problems:', len(bad_old))
for b in bad_old:
    print('  %s | %r | %s' % (b[0], b[1][:50], b[2]))
print('duplicate old values per file (info):')
for src, m in dup_old.items():
    for k, n in m.items():
        if n > 1:
            print('  %s %r x%d' % (src, k[:50], n))
