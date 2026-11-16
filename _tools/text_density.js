// Text density map: for every file in the EU CD1 Sega-FS table, count printable-
// ASCII density of its user data (2352-byte raw sectors, user = 16..2064).
// Output: files sorted by (density * size) descending.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);
const recs = [];
for (let i = 0; i < SCAN_LEN - 40; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    const nl = buf[i + 14];
    if (nl < 1 || nl > 40) continue;
    const name = buf.slice(i + 15, i + 15 + nl).toString('latin1');
    if (!/^[A-Za-z0-9_\-.]+$/.test(name)) continue;
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
      recs.push({ name, lba: pairs[0], size: pairs[1] });
    }
  }
}
console.log('files:', recs.length);

const CH = buf => { };
const out = [];
const SEC = Buffer.alloc(2352 * 64);
for (const r of recs) {
  let printable = 0, sampled = 0;
  let pos = r.lba * 2352;
  let left = r.size;
  while (left > 0) {
    const nSect = Math.min(64, left);
    const want = Math.min(nSect * 2352, SEC.length);
    const n = fs.readSync(fd, SEC, 0, want, pos);
    if (n <= 0) break;
    for (let i = 16; i < n; i += 1) { } // placeholder: user area only
    // count printable in user areas of each sector
    const nSectors = Math.floor(n / 2352);
    for (let s = 0; s < nSectors; s++) {
      const base = s * 2352 + 16;
      for (let i = 0; i < 2048; i++) {
        const ch = SEC[base + i];
        if ((ch >= 0x20 && ch <= 0x7e) || (ch >= 0x88 && ch <= 0x8f) || ch === 0x0a || ch === 0x0d) printable++;
      }
      sampled += 2048;
    }
    pos += nSectors * 2352;
    left -= nSectors * 2048;
  }
  const dens = sampled ? printable / sampled : 0;
  out.push({ name: r.name, lba: r.lba, size: r.size, dens, score: dens * r.size });
}
out.sort((a, b) => b.score - a.score);
console.log('=== top 60 by text density × file size ===');
out.slice(0, 60).forEach(r =>
  console.log(r.name.padEnd(16), 'LBA 0x' + r.lba.toString(16).padStart(6, '0'),
    ((r.size / 1024) | 0).toString().padStart(6), 'KiB',
    'dens=' + r.dens.toFixed(3)));
fs.closeSync(fd);
