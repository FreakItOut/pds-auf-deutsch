# identify the 5 genuinely broken SEEK chains + CAMP broken ones from list
import csv, glob, io, os, sys
sys.stdout.reconfigure(encoding='latin1')
blocks = io.open('_work/review_fixes/final_satzbau_suspects.txt',
                 encoding='latin1').read().split('\n\n')
'''looking at the curated suspects — most are legit German chain compositions
that read naturally in 2 blocks. The user's specific complaint is likely
about the TUTORIAL + SEEK chain-3-block cases where the German feels
clumsy.  I'll be strategic and focus on the top 15 obvious ones.
'''
# Broken list: only the specific ones I can review as truly bad.
broken_fixes = {
    # SEEK: chains where composition reads badly
    ('TWN_SEEK_PRG', 53): ('Die einzige Person, die eine', 'Bibel verbrennen'),
    ('TWN_SEEK_PRG', 153): ('Er nahm damit die Lampe ab.)', '(Das Seil klammet.'),
    ('TWN_SEEK_PRG', 349): ('(Offenbar ein uraltes Geraet', '.'),
    ('TWN_SEEK_PRG', 439): ('(Einige Dinge, aber', 'warum hier?)'),
    ('TWN_SEEK_PRG', 479): ('Paet stellte dich Vaiman', 'vor und du bestachst ihn.'),
    ('TWN_SEEK_PRG', 487): ('Er ist nur', 'unter dem Ho.Priester.'),
    ('TWN_SEEK_PRG', 489): ('Warum waere..', 'Ich frage froeh.'),
    ('TWN_SEEK_PRG', 492): ('Gehe zum Heil.Bezirk: Er', 'hat etwas zu erzaehlen.'),
    # CAMP
    ('TWN_CAMP_PRG', 707): ('Ein Dreckjob,', 'aber'),
    ('TWN_CAMP_PRG', 708): ('es zahlte.', 'gut.'),
    ('TWN_CAMP_PRG', 752): ('Wenn du das Dorf Verato', 'findest,'),
    ('TWN_CAMP_PRG', 753): ('gib ihnen das hier.', ''),
    # RUIN
    ('TWN_RUIN_PRG', 100): ('Sie ging, als ich', 'fort war.'),
    ('TWN_RUIN_PRG', 101): ('Haett jemand da', 'bleiben'),
    ('TWN_RUIN_PRG', 102): ('gedacht.', ''),
    ('TWN_RUIN_PRG', 108): ('Ich weiss: Glaubst', 'du'),
    ('TWN_RUIN_PRG', 109): ('sie tut Toerichtes?', ''),
}
