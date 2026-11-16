// twn_profile.js — Profile text-line layout inside the already-extracted
// TWN_*.PRG town script files. Print zone boundaries, line counts, structure.
// Output: _work/twn_lines_<name>.csv with lineIdx;off;len (no text).
const fs = require('fs');
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);

function profile(name) {
  const b = fs.readFileSync('_work/' + name);
  const lines = [];
  let i = 0;
  while (i < b.length) {
    if (isP(b[i])) {
      const st = i;
      while (i < b.length && isP(b[i])) i++;
      if (i < b.length && b[i] === 0 && i - st >= 3) lines.push({ st, len: i - st });
    } else i++;
  }
  // plausible dialogue filter: len>=11, letters>=6, has lowercase
  const dial = [];
  for (const l of lines) {
    let letters = 0, lower = 0, other = 0;
    for (let k = l.st; k < l.st + l.len; k++) {
      const x = b[k];
      if (x >= 0x41 && x <= 0x7a) { letters++; if (x >= 0x61) lower++; }
      else if (x !== 0x20 && x !== 0x2e && x !== 0x2c && x !== 0x27) other++;
    }
    if (l.len >= 11 && letters >= 6 && lower >= 2 && other <= l.len * 0.3) dial.push(l);
  }
  // zones by 16 KB buckets
  const buck = {};
  for (const l of dial) { const k = l.st >> 14; buck[k] = (buck[k] || 0) + 1; }
  console.log('===', name, 'len', b.length);
  console.log('  raw lines>=3:', lines.length, '| dialogue-like:', dial.length,
    '| 16KB buckets with >=50 dialogue lines:',
    Object.entries(buck).filter(([k, v]) => v >= 50).map(([k, v]) => k + ':' + v).join(' '));
  // contiguous zone detection with 4-bucket max gap
  const ks = Object.keys(buck).map(Number).sort((a, b) => a - b);
  let zones = [], cur = null;
  for (const k of ks) {
    if (buck[k] >= 20) {
      if (cur && k - cur.end <= 4) cur.end = k;
      else { if (cur) zones.push(cur); cur = { start: k, end: k }; }
    }
  }
  if (cur) zones.push(cur);
  for (const z of zones) {
    const inZone = dial.filter(l => l.st >= z.start * 16384 && l.st < (z.end + 1) * 16384);
    console.log('  zone 0x' + (z.start * 16384).toString(16) + '..0x' + ((z.end + 1) * 16384).toString(16),
      'lines', inZone.length);
  }
  fs.writeFileSync('_work/twn_lines_' + name.replace(/\.PRG$/i, '').toLowerCase() + '.csv',
    'lineIdx;off;len\n' + dial.map((l, n) => n + ';' + l.st + ';' + l.len).join('\n') + '\n');
  return dial.length;
}
for (const n of ['TWN_SEEK.PRG', 'TWN_CAMP.PRG', 'TWN_RUIN.PRG']) profile(n);
