// zone_profile.js — segment subblob_cd1.bin into zones by mean line length.
// Print zone ranges in *disc sector* terms (sector = S0 + off/2048).
const fs = require('fs');
const S0 = 235717;
const b = fs.readFileSync('_work/subblob_cd1.bin');
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);

// line census once
const lines = [];
let i = 0;
while (i < b.length) {
  if (isP(b[i])) {
    const st = i;
    while (i < b.length && isP(b[i])) i++;
    if (i < b.length && b[i] === 0 && i - st >= 3) lines.push({ st, len: i - st });
  } else i++;
}
console.log('lines:', lines.length);

// window = 128 sectors (256 KB); compute mean len + count
const W = 256 * 1024;
const rows = [];
for (let w = 0; w < b.length; w += W) {
  const inWin = lines.filter(l => l.st >= w && l.st < w + W);
  if (inWin.length === 0) { rows.push(null); continue; }
  const mean = inWin.reduce((a, l) => a + l.len, 0) / inWin.length;
  rows.push({ off: w, count: inWin.length, mean, sec: S0 + w / 2048, secEnd: S0 + (w + W) / 2048 });
}
// classify: subtitle-ish if mean>=15 && count>=200
const zones = [];
let cur = null;
for (let k = 0; k < rows.length; k++) {
  const r = rows[k];
  const hot = r && r.mean >= 15 && r.count >= 150;
  if (hot && !cur) cur = { start: k, end: k };
  else if (hot && cur) cur.end = k;
  else if (!hot && cur) { zones.push(cur); cur = null; }
}
if (cur) zones.push(cur);
console.log('subtitle-like zones (mean>=15, lines>=150/window):');
for (const z of zones) {
  const rs = rows.slice(z.start, z.end + 1).filter(Boolean);
  const count = rs.reduce((a, r) => a + r.count, 0);
  const mean = rs.reduce((a, r) => a + r.count * r.mean, 0) / count;
  console.log('  sectors', (S0 + z.start * 128) + '..' + (S0 + z.end * 128 + 128),
    'lines', count, 'meanLen', mean.toFixed(1),
    'byteRange 0x' + (z.start * W).toString(16) + '..0x' + ((z.end + 1) * W).toString(16));
}
fs.writeFileSync('_work/subblob_zones.txt',
  zones.map(z => (S0 + z.start * 128) + '</>' + (S0 + z.end * 128 + 128) + '</>' + z.start * W).join('\n') + '\n');
console.log('written _work/subblob_zones.txt');
