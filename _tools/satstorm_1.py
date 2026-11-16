# final SATZBAU fixes: a curated list of the broken 2-block chain pairs
# (CAMP / E022 / RUIN / JIRI / SEEK), each with German that fits its EN
# budget and reads naturally. Also fixes DE2's trailing fragment.
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

FIX = {
    # (stem, uidA) -> de1 ; uidB = uidA+1 -> de2
    # CAMP
    ('TWN_CAMP_PRG', 108): ('Er wirkt beschaeftigt,', 'schlachtet Monster.)'),
    ('TWN_CAMP_PRG', 128): ('Reise allein, solange du', 'jung bist.'),
    ('TWN_CAMP_PRG', 215): ('werdet ihr weggerissen', 'vom Gravitationssturm.'),
    ('TWN_CAMP_PRG', 296): ('waere er hilflos...', 'Bringt ihm Beides.'),
    ('TWN_CAMP_PRG', 397): ('der Aussenwelt.', 'Ich bin hier zurecht.'),
    ('TWN_CAMP_PRG', 452): ('Nicht viel fuettern,',' aber'),
    ('TWN_CAMP_PRG', 453): ('wir tun unser Bestes...', ''),
    ('TWN_CAMP_PRG', 456): ('Muede von der Reise,','und'),
    ('TWN_CAMP_PRG', 457): ('er auch wahrscheinlich...', ''),
    ('TWN_CAMP_PRG', 475): ('Wenn sie Nahrung nehmen,','verhungern'),
    ('TWN_CAMP_PRG', 476): ('wir voellig.', ''),
    ('TWN_CAMP_PRG', 490): ('Du solltest es schaffen,','wenn du ostwaerts gehst.'),
    ('TWN_CAMP_PRG', 499): ('Wenn die Zeit kommt,','wirst du'),
    ('TWN_CAMP_PRG', 500): ('eine Familie gruenden.', ''),
    ('TWN_CAMP_PRG', 535): ('Keine Sorge. Eines Tages,','finden wir'),
    ('TWN_CAMP_PRG', 536): ('ein Zuhause.', ''),
    ('TWN_CAMP_PRG', 649): ('Ich zeige selten Gefuehle,','aber'),
    ('TWN_CAMP_PRG', 650): ('der Junge war mir wer.', ''),
    ('TWN_CAMP_PRG', 657): ('Kurz nach Rueckkehr,', 'starb'),
    ('TWN_CAMP_PRG', 658): ('sein Sohn.', ''),
    ('TWN_CAMP_PRG', 660): ('Sie haben Zoah', 'zerstoert'),
    ('TWN_CAMP_PRG', 661): ('und auch meine Heimat.', ''),
    ('TWN_CAMP_PRG', 685): ('Wenn Anjou nicht zurueck,', 'haben'),
    ('TWN_CAMP_PRG', 686): ('wir ein Problem.', ''),
    ('TWN_CAMP_PRG', 707): ('Ein Dreckjob,', 'der'),
    ('TWN_CAMP_PRG', 708): ('sich ausgezahlt hat.', ''),
    ('TWN_CAMP_PRG', 752): ('Wenn du das Dorf Verato', 'findest,'),
    ('TWN_CAMP_PRG', 753): ('gib ihnen das hier.', ''),
    # SEEK
    ('TWN_SEEK_PRG', 529): ('Der Liberale Bezirk ist', 'von Reisenden bewohnt'),
    ('TWN_SEEK_PRG', 997): ('Wenn du es aushalten', 'kannst,'),
    ('TWN_SEEK_PRG', 998): ('bist du ein echter Mann.', ''),
    # RUIN
    ('TWN_RUIN_PRG', 390): ('Denkst wir stehen Chancen', 'gegen die Macht'),
    ('TWN_RUIN_PRG', 390): ('Denkst wir haben eine Chance', 'gegen die Macht'),
    ('TWN_RUIN_PRG', 500): ('Bringt dein Drache Sestren um,', 'ist die Welt'),
    ('TWN_RUIN_PRG', 501): ('vom Fluch befreit.', ''),
    ('TWN_SEEK_PRG', 595): ('Denkst du, weil wir nie', 'etwas Gutes fanden'),
    ('TWN_SEEK_PRG', 596): ('etwas Gutes fanden', ''),
    # RUIN
    ('TWN_RUIN_PRG', 100): ('Sie ging, als ich fort war.', ''),
    ('TWN_RUIN_PRG', 101): ('Ich haette jemanden da', 'bleiben'),
    ('TWN_RUIN_PRG', 102): ('muessen.'),  # du for missing empty block
    ('TWN_RUIN_PRG', 108): ('Ich weiss. Glaubst du,', ''),
    ('TWN_RUIN_PRG', 109): ('sie tut etwas Toerichtes?', ''),
    # JIRI
    ('TWN_JIRI_PRG', 482): ('Kennst du die Legende?', ''),
    ('TWN_JIRI_PRG', 483): ('Der Wald ist ein besonderer Ort.', ''),
    ('TWN_JIRI_PRG', 484): ('Er ist von Goettern', 'geschaetzt'),
    ('TWN_JIRI_PRG', 485): ('durch ihre Macht.', ''),
    ('TWN_JIRI_PRG', 486): ('Ich hoerte von einer grossen', ''),
    ('TWN_JIRI_PRG', 487): ('Stadt. Gibt es diese?', ''),
    # E022
    ('TWN_E022_PRG', 435): ('Er kann nicht geheilt werden,', ''),
    ('TWN_E022_PRG', 436): ('ausser mit Spezialgegenmittel', ''),
    # CAMP 435/436
    ('TWN_CAMP_PRG', 435): ('Er kann nicht geheilt werden,', ''),
    ('TWN_CAMP_PRG', 436): ('ausser mit Spezialgegenmittel', ''),
}
