// es_dir_parse.js v2 — generic parser: find 62 01 1d 01, nameLen at +14,
// name; then scan for TWO consecutive mirrored u32 pairs (LE,BE) within 8 bytes
// after name-plus-terminator.
const fs = require('fs');
const m0 = fs.readFileSync('_work/cd1_0.bin');
const SIG = Buffer.from([0x62, 0x01, 0x1d, 0x01]);
const NAME_OK = /^[\w\-.]+;1$/i;

function tryParseAt(off) {
  const nl = m0[off + 14];
  if (nl < 2 || nl > 40) return null;
  const name = m0.slice(off + 15, off + 15 + nl).toString('latin1');
  if (!NAME_OK.test(name)) return null;
  // scan for mirrored pairs starting after name
  const base = off + 15 + nl;
  for (let skip = 1; skip <= 6; skip++) {
    const pairs = [];
    let q = base + skip;
    for (let k = 0; k < 4; k++) {
      if (q + 8 > m0.length) break;
      const le = m0.readUInt32LE(q), be = m0.readUInt32BE(q + 4);
      if (le === be) { pairs.push(le); q += 8; } else break;
    }
    if (pairs.length >= 2) return { name, pairs, end: q, skip };
  }
  return null;
}

const entries = [];
let p = 0;
while (p < m0.length - 60) {
  const i = m0.indexOf(SIG, p);
  if (i < 0) break;
  const rec = tryParseAt(i);
  if (rec) { entries.push({ off: i, ...rec }); p = rec.end; }
  else p = i + 1;
  if (entries.length > 3000) break;
}
console.log('entries parsed:', entries.length);
for (const e of entries.slice(0, 4))
  console.log(' ', e.name.padEnd(22), 'pairs:', e.pairs.map(x => x.toString()).join(', '),
    '(skip', e.skip, ')');

fs.writeFileSync('_work/es_dir_entries.csv',
  'name;dirOff;pair0;pair1;extra\n' +
  entries.map(e => [e.name, e.off, e.pairs[0] ?? '', e.pairs[1] ?? '', e.pairs[2] ?? ''].join(';')).join('\n') + '\n', 'latin1');
console.log('written _work/es_dir_entries.csv');

const hits = entries.filter(e => /BTL_|CAMPSCR|CARASCR|EVT\d\d\d/i.test(e.name));
console.log('script-file entries:', hits.length);
for (const e of hits.slice(0, 40))
  console.log(' ', e.name.padEnd(22), 'pairs:', e.pairs.map(x => x + '(0x' + (x >>> 0).toString(16) + ')').join('  '));
