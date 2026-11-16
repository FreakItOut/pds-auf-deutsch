# Consolidated EVT subtitle quality pass.
# - applies curated EN->DE fixes
# - applies mechanical normalization (double commas, trailing comma/ellipsis mismatches, " ," )
# - rewrites _work/evt_batch*_norm.csv in place and rebuilds _work/evt_de_map.csv
# - validates: EN key exists on disc, len(de) <= len(en), ASCII-only
# Run BEFORE check_evt_all.py and patch_evt_subtitles.py --disc all.
import glob
import json
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------- disc keys
disc = set()
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    disc |= {e['text'] for e in j['entries']}

# ---------------------------------------------------------------- curated fixes
FIX = {
    # --- grammar / wrong subject / wrong meaning
    'Why?': 'Wozu',
    'Why did you attack me?': 'Warum attackierst du?',
    "Why don't you come along?": 'Warum kommst du nicht?',
    'What... they\'re taking her?': 'Was... man nimmt sie?',
    'You plan to use me as a weapon?': 'Willst mich als Waffe nutzen?',
    'You survived... I saw you fall...': 'Du hast ueberlebt... du fielst.',
    'You\'re tougher than you look.': 'Staerker als du aussiehst!',
    'You... I know you from the site...': 'Ich kenne dich von der Staette...',
    'You... are our only hope.': 'Du bist unsere Hoffnung.',
    'Your men?': 'Deine?',
    'But I\'m sick of being kept alive': 'Aber ich bin das Leben leid.',
    'Damn! Come back... here...': 'Halte an... komm zurueck...',
    'Craymen will pay...': 'Craymen zahlt.',
    'Crush him before...': 'Zerdrueckt ihn...',
    'Divine Visitor?': 'Goettlicher?',
    "'%a0'... You are the Divine Visitor.": "'%a0'... Goettlicher Besucher.",
    "Don't shoot!!": 'Schiess nicht',
    'Eliminate it once more...': 'Noch einmal vernichten...',
    'No one would suspect a man like me to': 'Niemand glaubt, dass ich',
    'lead anything.': 'fuehren kann.',
    'Food for the monsters you awakened.': 'Nahrung der Monster, die du weckst.',
    'in the ancient records anyway.': 'in alten Schriften steht.',
    'in your own way.': 'auf deine Art.',
    'is gearing up to finish this war.': 'ruestet auf, den Krieg zu enden.',
    'it all belongs in the Ancient Age.': 'All das gehoert in die Vorzeit.',
    'left the Ancient Age in ruins.': 'zerstoerte die Vorzeit.',
    'to destroy the world with the': 'die Welt mit ihm zu enden',
    'I see... A dream...': 'Ach, ein Traum...',
    'mankind from extinction.': 'Menschheit vorm Verfall.',
    'or what we call the Tower.': 'oder auch Turm genannt.',
    'the less you know about the': 'Je weniger kennst du das',
    'the seekers are an organization,': 'Die Sucher sind ein Verband,',
    'structured, but secretive group.': 'organisierte Geheimgesellschaft.',
    'then I\'ll decide whether to': 'dann entscheide, ob ich',
    'to the creatures we\'ve': 'den Kreaturen, die',
    'but internally, I am closer': 'doch innerlich bin ich nah,',
    'been fighting.': 'wir bekriegen.',
    'to destroy the world with the': 'die Welt mit ihm zu enden',
    'to guard this excavation site.': 'diese Fundstaette zu bewachen.',
    'to loathe the monsters.': 'Monster verabscheuen.',
    'to travel into the frontier...': 'in die Frontier zu reisen...',
    'too discovered the ancient weapons.': 'entdeckte auch die alten Waffen.',
    'we visited, shortly after we met?': 'das wir kurz kennenlernten?',
    'we will... have to kill you.': 'muessen wir dich toeten.',
    "we're a band of tomb raiders.": 'Wir sind Grabraeuber.',
    'we were betrayed.': 'Man verriet uns.',
    'where I awoke.': 'erwachte.',
    'It was inscribed on the bed': 'Es steht dort, wo ich',
    'wield such power...': 'solche Gewalt...',
    'with the technology of the lost': 'mit der Technik der Verlorenen,',
    'with the Empire,': 'mit dem Reich',
    'I am sorry.': 'Verzeih.',
    'Zastava, leave them be.': 'Zastava, lass sie los.',
    'all wrong.': 'falsch.',
    'among the ancient ones.': 'unter den Alten.',
    'an endless waste...': 'endloses Elend...',
    'an eye on you.': 'Augen auf dich',
    'by our own fleet...': 'durch die eigene...',
    'caretakers of the ecosystem.': 'Hueter dieses Oekosystems.',
    'civilization on their side.': 'Zivilisation an ihrer Seite',
    'destroy this Tower.': 'Zerstoert den Turm!',
    'destructive force of the Tower.': 'Zerstoerungskraft des Turms.',
    'I hope you\'re right': 'Hoffe du hast recht',
    'biological technology...': 'Bio-Technologie...',
    'of the Ancient Age.': 'der Vorzeit.',
    'the Ancient Age': 'die Vorzeit',
    'Again, I am in your debt.': 'Schulde dir wieder was.',
    'but when we get out of here,': 'wenn wir hier draussen,',
    'but what is your purpose?': 'was ist dein Auftrag?',
    'but we\'ll have another chance.': 'doch es gibt eine 2. Chance.',
    'But this just doesn\'t seem right.': 'Doch das kommt mir falsch vor.',
    'But we\'re not really living.': 'Doch echt leben wir nicht.',
    'Craymen lead the monsters': 'Craymen rief die Monster',
    'If we\'re lucky.': 'Wenn\'s laeuft.',
    'Impurity detected...': 'Unreinheit hier...',
    'message in his own blood.': 'Botschaft, im Eigenblut.',
    'I may look human like you,': 'Ich seh aus wie du,',
    'I never asked your name.': 'Ich frag nie nach Name.',
    'I was taught...': 'Gelernt hab ich',
    "Isn't that why you kept me here?": 'Haeltst du mich deswegen hier?',
    'It made my job easier.': 'Erleichtert mir das.',
    'It appears that he has gathered': 'Er hat wohl mehr Infos,',
    'more information than we thought.': 'mehr als wir dachten.',
    # --- glossary: Empire -> Reich
    'by the Empire as well...': 'auch vom Reich...',
    'The Capital of the Empire.': 'Hauptstadt des Reiches.',
    'Special Force of the Empire...': 'Elitekraft des Reiches...',
    # --- glossary: Captain -> Chef
    'he killed my Captain and my friends!': 'Er toetete Chef und Freunde!',
    'Captain, what is this?': 'Chef, was ist das?',
    'I\'ve got to find my Captain. ': 'Ich muss meinen Chef finden.',
    # --- misc repairs
    'When we find the truth about Sestren.': 'Wenn wir Sestrens Wahrheit kennen.',
    'When you leave for Sestren,': 'Wenn du Sestren suchst,',
    'Without any fire power,': 'Ohne jede Feuerkraft,',
    'forever.': 'ewig.',
    'for his highness.': 'fuer seine Hoheit',
    'The operation at the Imperial Capital': 'Operation an der Reichshauptstadt',
    # --- second-pass fixes, lines ~561-815
    'It\'s a full-blooded one.': 'Ein Vollblut!',
    'It\'s out of control': 'Ausser Kontrolle.',
    'It\'s you!': 'Du bist\'s',
    'It\'s so hard to know who or': 'Wer oder was sie sind,',
    'Just who... what are you people?': 'Wer... was seid ihr?',
    'Justice may not be with us.': 'Gerechtigkeit ist nicht da.',
    'Meanwhile...': 'Derweil...',
    'Of course, oracles have foretold': 'Orakel haben das vorhergesagt',
    'Please, try to be on time.': 'Sei bitte puenktlich!',
    'Pull the trigger and': 'Drueck ab, und',
    'Pursue at once...': 'Verfolgt sofort',
    'She will finish you.': 'Sie vernichtet dich.',
    'That\'s all you have to say?': 'Ist das dein letztes Wort?',
    'That\'s not fair...': 'Das ist unfair...',
    'They\'ll never be able to': 'Nie werden sie das,',
    'This is bad... ': 'Das wird uebel.',
    'Those bastards...': 'Dieses Pack...',
    'Those fools...': 'Ihr Narren...',
    'To be honest,': 'Ehrlich,',
    'To gain control of the Tower,': 'Um des Turms Herr zu werden,',
    'To maintain superiority,': 'Zur Vorherrschaft,',
    'To shut down the Tower,': 'Den Turm ausschalten,',
    'We are always one step': 'Immer einen Schritt',
    'We cannot let a man with a dragon': 'Ein Mann mit Drachen darf nicht,',
    "We've got to abandon this base,": 'Basis muessen wir aufgeben,',
    'We\'ve lost this time,': 'Diesmal verloren,',
    'We, the seekers are...': 'Wir Sucher sind...',
    'Were you having a nightmare?': 'Hattest du einen Albtraum?',
    'What Craymen believed,': 'Woran Craymen glaubte,',
    'Now I control mankind\'s future!': 'Nun kontrollier ich die Zukunft',
    'Shall we send him to the flagship?': 'Schicken wir ihn zum Flaggschiff?',
    'The dragons ended the Ancient Age': 'Die Drachen beendeten die Vorzeit',
    'The Empire declared war on its': 'Das Reich erklaerte den Krieg,',
    'Keep quiet, and they will go away.': 'Still bleiben, dann ziehen sie ab.',
    "...I hope you're right": '...Hoffe du hast recht',
    'Crush him before he reaches the Tower.': 'Zerquetscht ihn vor dem Turm.',
    'Damn!  Come back... here...': 'Halt! Komm zurueck! Sofort!',
    'an endless waste of resources,': 'ein endloser Rohstoffraub,',
}

# ---------------------------------------------------------------- batches load
files = sorted(glob.glob('_work/evt_batch*_norm.csv'),
               key=lambda p: int(re.search(r'(?<=batch)\d+', p).group(0)))
batches = []
for f in files:
    data = []
    heads = []
    for ln in open(f, encoding='latin1').read().splitlines():
        if ln.strip():
            (heads if ln.startswith('#') else data).append(ln)
    batches.append((f, heads, [ln.split(';', 1) for ln in data]))

total = sum(len(p) for _, _, p in batches)
uniq = {en for _, _, pairs in batches for en, _ in pairs}
print('batch entries: %d total, %d unique EN keys' % (total, len(uniq)))

missing_disc = sorted(en for en in uniq if en not in disc)
if missing_disc:
    print('WARN %d EN keys not found on discs:' % len(missing_disc))
    for en in missing_disc:
        print('  DISC-MISSING:', repr(en))

unknown_fix = sorted(en for en in FIX if en not in uniq)
if unknown_fix:
    print('WARN %d FIX keys not present in batches:' % len(unknown_fix))
    for en in unknown_fix:
        print('  FIX-NOT-IN-BATCHES:', repr(en))

# ---------------------------------------------------------------- normalization
def norm(en, de):
    de = de.rstrip()
    while ',,' in de:
        de = de.replace(',,', ',')
    de = de.replace(' ,', ',')
    if de.endswith(','):
        if not en.endswith(','):
            de = de[:-1]
            if en.endswith('...') and not de.endswith('.'):
                de += '...'
            elif en.endswith('?') and not de.endswith(('?', '!')):
                de += '?'
            elif en.endswith('!') and not de.endswith(('!', '?')):
                de += '!'
            elif en.endswith('.') and not de.endswith('.'):
                de += '.'
    else:
        if en.endswith(',') and not de.endswith(('!', '?', ':')):
            if len(de) + 1 <= len(en):
                de += ','
    return de

changed = 0
problems = []
for f, heads, pairs in batches:
    out = list(heads)
    for idx, (en, de) in enumerate(pairs):
        new = norm(en, FIX.get(en, de))
        if new != de:
            changed += 1
        ok_len = len(new) <= len(en)
        ok_ascii = all(ord(c) < 128 for c in new)
        if not ok_len or not ok_ascii:
            problems.append((f, en, de, new, ok_len, ok_ascii))
            new = de  # revert on failure
        out.append(f'{en};{new}')
    with open(f, 'w', encoding='latin1', newline='') as fh:
        fh.write('\n'.join(out) + '\n')

print('changed DE strings:', changed)
print('problems (reverted):', len(problems))
for f, en, old, new, ok_len, ok_ascii in problems:
    print('  PROBLEM', os.path.basename(f), repr(en))
    print('     old:', repr(old), ' len %d + new:' % len(en), repr(new), 'len(en)=%d' % len(en),
          'ascii-ok=%s' % ok_ascii)

# ---------------------------------------------------------------- rebuild map
seen = {}
for f, heads, pairs in batches:
    data = [ln for ln in open(f, encoding='latin1').read().splitlines() if ln.strip() and not ln.startswith('#')]
    for ln in data:
        en, de = ln.split(';', 1)
        seen[en] = de
with open('_work/evt_de_map.csv', 'w', encoding='latin1', newline='') as fh:
    fh.write('\n'.join(f'{en};{seen[en]}' for en in sorted(seen)) + '\n')
print('rebuilt _work/evt_de_map.csv with', len(seen), 'entries')
