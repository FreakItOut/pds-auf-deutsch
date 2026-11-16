// build_linedb.js — Build the subtitle line database:
// - Extract every plausible dialogue line from subblob_cd1.bin
// - Identify unique strings (byte-exact), first offset, all copy offsets
// - Output to _work/subblob_lines.csv (line index;off;len), and
//   _work/subblob_unique.csv (uid;len;copies;firstOff)
// Print structure stats only (no text).
const fs = require('fs');
const S0 = 235717;
const b = fs.readFileSync('_work/subblob_cd1.bin');
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);

// 1) all NUL-terminated printable runs (>=3)
const lines = [];
let i = 0;
while (i < b.length) {
  if (isP(b[i])) {
    const st = i;
    while (i < b.length && isP(b[i])) i++;
    if (i < b.length && b[i] === 0 && i - st >= 3) lines.push({ st, len: i - st });
  } else i++;
}
console.log('raw NUL-terminated runs (>=3):', lines.length);

// 2) filter plausible dialogue lines: length >= 11, letters >= 6, has lowercase
const dial = [];
for (const l of lines) {
  let letters = 0, lower = 0, upper = 0, other = 0;
  for (let k = l.st; k < l.st + l.len; k++) {
    const x = b[k];
    if ((x >= 0x61 && x <= 0x7a) || (x >= 0x41 && x <= 0x5a)) { letters++; if (x >= 0x61) lower++; else upper++; }
    else if (x !== 0x20 && x !== 0x2e && x !== 0x2c && x !== 0x27) other++;
  }
  if (l.len >= 11 && letters >= 6 && lower >= 2 && other <= l.len * 0.3) dial.push(l);
}
console.log('dialogue-like lines:', dial.length);

// 3) unique by bytes
const uniq = new Map(); // bytes -> {len, copies:[st..], first}
for (const l of dial) {
  const s = b.slice(l.st, l.st + l.len).toString('latin1');
  const u = uniq.get(s) || { len: l.len, copies: [], first: l.st };
  u.copies.push(l.st);
  uniq.set(s, u);
}
console.log('unique dialogue lines:', uniq.size);
const copiesHist = {};
for (const u of uniq.values()) copiesHist[u.copies.length] = (copiesHist[u.copies.length] || 0) + 1;
console.log('copies distribution:', Object.entries(copiesHist).sort((a, c) => +c[0] - +a[0]).slice(0, 10)
  .map(e => e[0] + 'x:' + e[1]).join(' '));
const totalCopies = [...uniq.values()].reduce((a, u) => a + u.copies.length, 0);
console.log('total dialogue copies:', totalCopies);

// 4) zone assignment
const zt = fs.readFileSync('_work/subblob_zones.txt', 'latin1').split(/\r?\n/).filter(Boolean).map(l => l.split('</>'));
const zones = zt.map(([s0, s1, off]) => ({ s0: +s0, s1: +s1, off: +off, size: 0x40000 }));
for (const [idx, z] of zones.entries()) {
  const zin = dial.filter(l => l.st >= z.off && l.st < z.off + z.size);
  const u = [...uniq.values()].filter(v => v.first >= z.off && v.first < z.off + z.size);
  console.log(' zone ' + idx, 'sec ' + z.s0 + '..' + z.s1, 'off 0x' + z.off.toString(16),
    'lines', zin.length, 'unique', u.length);
}

// write line DB (all dialogue copies)
fs.writeFileSync('_work/subblob_lines.csv',
  'lineIdx;off;len;offInSector;sector\n' +
  dial.map((l, n) => [n, l.st, l.len, (S0 * 2048 + l.st) % 2048, S0 + Math.floor(l.st / 2048)].join(';')).join('\n') + '\n');
// write unique DB
fs.writeFileSync('_work/subblob_unique.csv',
  'uid;len;copies;firstOff\n' +
  [...uniq.entries()].map(([s, u], n) => [n, u.len, u.copies.length, u.first].join(';')).join('\n') + '\n');
console.log('written _work/subblob_lines.csv, _work/subblob_unique.csv');
