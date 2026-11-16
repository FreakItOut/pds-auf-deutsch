# coverage: fixed grand total summary
# combines: subtitles group (TWN), TWN_E128, movie FMV, menu group
# and battle live scan numbers.
import sys
sys.stdout.reconfigure(encoding='latin1')

GROUPS = [
    ('TWN subtitles (CD1-4 dialog)', 3963, 3935, 3491, 6),
    ('TWN_E128 (cd3-only)', 449, 444, 5, 20),
    ('Menu text (menu - BTL/FLD/CHILDMP/SCB/TUNE/etc)', 10043, 9147, 8234, 913),
    ('Movie FMV subtitles', 815, 771, 770, 1),
    ('Battle labels/disc', 534, 246, 241, 5),
    ('Tutorial CGB', 838, 118, 116, 2),
]
grand_tot = grand_tr = grand_ok = grand_ident = 0
print('%-48s %6s %6s %6s %6s  pct' % ('group', 'total', 'transl', 'de', 'ident'))
for name, t, tr, ok, ident in GROUPS:
    grand_tot += t
    grand_tr += tr
    grand_ok += ok
    grand_ident += ident
    pct = (ok / tr * 100.0) if tr else 0.0
    print('%-48s %6d %6d %6d %6d %5.1f%%' % (name, t, tr, ok, ident, pct))
print('-' * 82)
p_all = (grand_ok / grand_tr * 100.0) if grand_tr else 0.0
print('%-48s %6d %6d %6d %6d %5.1f%%' % ('TOTAL', grand_tot, grand_tr,
                                        grand_ok, grand_ident, p_all))

# write csv report
with open('_work/review_fixes/coverage_total.csv', 'w',
          encoding='latin1', newline='\n') as f:
    f.write('group;total;translatable;de_ok;identity;pct\n')
    for name, t, tr, ok, ident in GROUPS:
        pct = (ok / tr * 100.0) if tr else 0.0
        f.write('%s;%d;%d;%d;%d;%.1f\n' % (name, t, tr, ok, ident, pct))
    f.write('TOTAL;%d;%d;%d;%d;%.1f\n' % (grand_tot, grand_tr, grand_ok,
                                          grand_ident, p_all))
print('written _work/review_fixes/coverage_total.csv')
