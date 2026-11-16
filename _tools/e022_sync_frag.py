import sys
sys.stdout.reconfigure(encoding='latin1')
lines = open('_work/subtitles/TWN_E022_PRG_de.csv', encoding='latin1').read().split('\n')
out = []
for l in lines:
    if l.startswith('24;25;4763;'):
        out.append("24;25;4763;4763;I'd love to explore these;Gerne wuerde ich die")
    else:
        out.append(l)
idx = [i for i, l in enumerate(out) if l.startswith('24;25;4763;')][0]
mx = max(int(l.split(';')[0]) for l in out if l and l[0].isdigit())
newrow = '%d;6;4789;4789;ruins.;Ruinen' % (mx + 1)
out.insert(idx + 1, newrow)
open('_work/subtitles/TWN_E022_PRG_de.csv', 'w', encoding='latin1', newline='\n').write('\n'.join(out) + '\n')
print('inserted', newrow)
