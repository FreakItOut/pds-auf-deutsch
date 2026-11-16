# list remaining over-budget rows in BTL_REST_map + scan non-ascii bytes
path = '_work/menu_de/BTL_REST_map.csv'
raw = open(path, 'rb').read()
bad = [b for b in raw if b > 0x7F]
print('non-ascii bytes:', len(bad))
for i, b in enumerate(raw):
    if b > 0x7F:
        print('  at %d: %02x ctx=%r' % (i, b, raw[max(0, i - 20):i + 20]))
        if i > 30:
            break
count = 0
for i, line in enumerate(open(path, encoding='latin1')):
    line = line.rstrip('\r\n')
    if not line or ';' not in line:
        continue
    if line.startswith('#'):
        continue
    p = line.split(';', 1)
    en, de = p[0], p[1]
    if len(de.encode('latin1')) > len(en.encode('latin1')):
        count += 1
        print('OVER  budget=%3d del=%3d EN=%r  DE=%r' % (len(en), len(de), en, de))
    elif de.strip() == en.strip() and len(en.strip()) >= 4:
        e = en.strip()
        import re
        if not re.match(r'^[A-Z0-9_% ,:.:!?-]*$', e) and '%' not in e:
            print('UNTR  EN=%r' % e)
print('over rows:', count)
