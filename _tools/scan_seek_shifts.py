import os, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Scan TWN_SEEK subtitles for shifted/truncated entries
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) < 6:
            continue
        uid, en, de = parts[0], parts[4], parts[5]
        # Check for obvious shifts: DE is very short compared to EN
        if len(en) > 30 and len(de) < 0.3 * len(en):
            print('uid=%s EN=%r DE=%r' % (uid, en[:60], de[:60]))
        # Check for DE that doesn't share any words with EN (rough heuristic)
        en_words = set(re.findall(r"[a-zA-Z']+", en.lower()))
        de_words = set(re.findall(r"[a-zA-Z']+", de.lower()))
        # Remove common German words
        common_de = {'der', 'die', 'das', 'und', 'ist', 'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr', 'nicht', 'ein', 'eine', 'mit', 'von', 'zu', 'auf', 'in', 'an', 'fuer', 'ueber', 'nach', 'bei', 'aus', 'um', 'am', 'im', 'zum', 'zur'}
        de_specific = de_words - common_de
        en_specific = en_words - {'the', 'a', 'an', 'and', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may', 'might', 'shall', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'about', 'up', 'down', 'left', 'right', 'back', 'front', 'top', 'bottom', 'side', 'inside', 'outside', 'near', 'far', 'away', 'home', 'now', 'then', 'today', 'tomorrow', 'yesterday', 'always', 'never', 'often', 'sometimes', 'usually', 'again', 'once', 'twice', 'first', 'last', 'next', 'previous', 'new', 'old', 'good', 'bad', 'big', 'small', 'large', 'little', 'great', 'long', 'short', 'high', 'low', 'right', 'wrong', 'true', 'false', 'yes', 'no', 'maybe', 'please', 'thank', 'thanks', 'sorry', 'hello', 'hi', 'hey', 'bye', 'goodbye', 'ok', 'okay'}
        if len(en_specific) >= 3 and len(de_specific & en_specific) == 0:
            print('SHIFT: uid=%s EN=%r DE=%r' % (uid, en[:50], de[:50]))