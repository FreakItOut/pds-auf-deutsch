// Dump the complete Spanish member0 FS table (dir @0x63e..) to CSV:
// id;name;recOff;lba;size_kib
const fs = require('fs');
const s = fs.readFileSync('_work/cd1_0.bin');
let o = 0x63e;
const rows = [];
let i = 0;
while (o < 0x17800 && s[o] === 0x62 && s[o + 1] === 0x01 && s[o + 2] === 0x1d && s[o + 3] === 0x01) {
  const nl = s[o + 14];
  if (nl < 4 || nl > 40) break;
  const name = s.slice(o + 15, o + 15 + nl).toString('latin1');
  // find first mirrored u32 pair after name
  let p = o + 15 + nl, found = -1;
  for (let k = 0; k < 24; k++) {
    if (s[p + k] === s[p + k + 7] && s[p + k + 1] === s[p + k + 6] &&
        s[p + k + 2] === s[p + k + 5] && s[p + k + 3] === s[p + k + 4]) { found = k; break; }
  }
  let lba = 0, size = 0;
  if (found >= 0) {
    const q = p + found;
    lba = s[q] | (s[q + 1] << 8) | (s[q + 2] << 16) | (s[q + 3] << 24);
    size = s[q + 8] | (s[q + 9] << 8) | (s[q + 10] << 16) | (s[q + 11] << 24);
  }
  rows.push([i, name, '0x' + o.toString(16), '0x' + lba.toString(16), (size / 1024 | 0)]);
  o += 33 + nl; i++;
}
console.log('records parsed:', rows.length, 'chain end at 0x' + o.toString(16));
fs.writeFileSync('_work/fs_es_member0.csv', 'id;name;recOff;lba;size_kib\n' + rows.map(r => r.join(';')).join('\n') + '\n');
// which record covers byte region 0x1d8261?
const targetOff = 0x1d8261;
const covers = rows.filter(r => {
  const lba = parseInt(r[3], 16);
  const size = parseInt(r[4], 16) * 1024;
  return lba * 2048 <= targetOff && targetOff < lba * 2048 + size;
});
console.log('records whose LBA*2048 covers 0x1d8261:');
covers.forEach(r => console.log(' ', r.join('  ')));
// records around the same offset by lba sum
const sorted = rows.slice().sort((a, b) => parseInt(a[3], 16) - parseInt(b[3], 16));
const around = sorted.filter(r => {
  const L = parseInt(r[3], 16) * 2048;
  return L > 0x1c0000 && L < 0x200000;
});
console.log('\nrecords with member0 offset 0x1c0000..0x200000 (sorted by LBA):');
around.forEach(r => console.log(' ', r.join('  ')));
