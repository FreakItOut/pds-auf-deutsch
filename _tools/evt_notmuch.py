import sys, io
sys.stdout.reconfigure(encoding='latin1')
path = '_work/evt_de_map.csv'
lines = io.open(path, encoding='latin1').read().split('\n')
out = []
for line in lines:
    if line.rstrip().startswith('Not much... at all.;') and not line.startswith('#'):
        en = 'Not much... at all.'
        line = en + ';Nicht viel.'
    out.append(line)
io.open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out) + '\n')
print('done')
