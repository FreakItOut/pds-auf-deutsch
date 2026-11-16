// subtitle_gaps.js — Cluster unassigned hits into ranges and correlate with FS
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);

const files = [];
for (let i = 0; i < SCAN_LEN - 40; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    const nl = buf[i + 14];
    if (nl < 1 || nl > 40) continue;
    const nm = buf.slice(i + 15, i + 15 + nl).toString('latin1');
    if (!/^[A-Za-z0-9_\-.]+$/.test(nm)) continue;
    let p = i + 15 + nl;
    if (buf[p] !== 0) continue;
    p++;
    const recLen = buf.readUInt16LE(p); p += 2;
    const pairs = [];
    for (let k = 0; k + 8 <= 40; k += 8) {
      const a = buf.readUInt32LE(p + k), b2 = buf.readUInt32BE(p + k + 4);
      if (a === b2) pairs.push(a); else break;
    }
    if (pairs.length >= 2 && pairs[0] < 600000 && pairs[1] < 470000000) {
      files.push({ name: nm, lba: pairs[0], size: pairs[1] });
    }
  }
}
files.sort((a, b) => a.lba - b.lba);
const ranges = files.map(f => ({ n: f.name, s: f.lba * 2352, e: f.lba * 2352 + Math.ceil(f.size / 2048) * 2352 }));

const hits = fs.readFileSync('_work/subtitle_hits.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return +p[0]; });

const assigned = hits.filter(h => ranges.some(r => h >= r.s && h < r.e));
const un = hits.filter(h => !assigned.includes(h));
un.sort((a, b) => a - b);

// cluster
const clusters = [];
let cs = un[0], ce = un[0];
for (let k = 1; k < un.length; k++) {
  if (un[k] - ce < 0x10000) ce = un[k];
  else { clusters.push([cs, ce]); cs = un[k]; ce = un[k]; }
}
clusters.push([cs, ce]);
console.log('unassigned hits:', un.length, 'in', clusters.length, 'clusters');

for (const [s, e] of clusters.slice(0, 40)) {
  // which FS ranges overlap?
  const near = ranges.filter(r => e + 0x100000 > r.s && s - 0x100000 < r.e)
    .map(r => r.n).slice(0, 6);
  const covered = ranges.some(r => s >= r.s - 0x100000 && e <= r.e + 0x100000);
  console.log('  0x' + s.toString(16) + ' .. 0x' + e.toString(16),
    '(sectors', Math.floor(s / 2352), '..', Math.floor(e / 2352) + ')',
    covered ? 'NEAR-FS' : 'GAP', near.join(','));
}
fs.closeSync(fd);
