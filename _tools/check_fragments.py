import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Check all negation-lost UIDs to see if they're multi-line fragments
neg_uids = {
    'TWN_CAMP_PRG_de.csv': [24, 91, 162, 164, 171, 198, 378, 422, 444, 482, 510, 548, 565, 579, 679, 699, 738, 745, 747],
    'TWN_RUIN_PRG_de.csv': [89, 220, 244, 264, 268, 270, 273, 277, 286, 293, 313, 331, 362, 374, 388, 398, 419, 505, 537, 629, 673],
}

for fn, uids in neg_uids.items():
    print('===', fn)
    with open('_work/subtitles/'+fn, encoding='latin1') as f:
        lines = f.readlines()
    for uid in uids:
        # Find the entry and its neighbors
        for i, line in enumerate(lines):
            parts = line.rstrip('\r\n').split(';')
            if len(parts) >= 6 and parts[0] == str(uid):
                # Check if prev/next entry is part of same sentence
                prev_uid = str(uid-1)
                next_uid = str(uid+1)
                prev_line = None
                next_line = None
                for j, l in enumerate(lines):
                    p = l.rstrip('\r\n').split(';')
                    if len(p) >= 6:
                        if p[0] == prev_uid: prev_line = p
                        if p[0] == next_uid: next_line = p
                # Check if EN continues on next line
                is_fragment = False
                if next_line and not parts[4].endswith(('.', '!', '?', ')')):
                    is_fragment = True
                if parts[4].startswith(('the ', 'a ', 'an ', 'and ', 'but ', 'or ', 'to ', 'of ', 'in ', 'for ', 'with ', 'on ', 'at ', 'by ', 'from ', 'as ', 'into ', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just')):
                    is_fragment = True
                status = 'FRAGMENT' if is_fragment else 'STANDALONE'
                print('  uid=%s %s EN=%r DE=%r' % (uid, status, parts[4][:40], parts[5][:40]))
                break