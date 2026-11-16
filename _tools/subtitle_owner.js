// subtitle_owner.js — Map subtitle_hits.csv sector offsets to owner EU files
// using the disc FS table (same parse as extract_eu_file.js).
// Per file: sentence-hit count. Also export hits CSV with owner names.
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
      const a = buf.readUInt32LE(p + k); const b2 = buf.readUInt32BE(p + k + 4);
      if (a === b2) pairs.push(a); else break;
    }
    if (pairs.length >= 2 && pairs[0] < 600000 && pairs[1] < 470000000) {
      files.push({ name: nm, lba: pairs[0], size: pairs[1] });
    }
  }
}
console.log('EU files on disc:', files.length);

const hits = fs.readFileSync('_work/subtitle_hits.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { off: +p[0], len: +p[1] }; });

// owner = file with lba*2352 <= off < (lba+size_sectors)*2352, size_sectors=ceil(size/2048)
const perFile = {};
const assigned = [];
for (const h of hits) {
  const found = files.find(f =>
    h.off >= f.lba * 2352 &&
    h.off < f.lba * 2352 + Math.ceil(f.size / 2048) * 2352);
  if (found) {
    perFile[found.name] = (perFile[found.name] || 0) + 1;
    assigned.push({ ...h, file: found.name });
  }
}
console.log('assigned hits:', assigned.length, 'of', hits.length);
const top = Object.entries(perFile).sort((a, b) => b[1] - a[1]);
console.log('\ntop owner files by sentence-hit count:');
for (const [n, c] of top.slice(0, 30)) console.log('  ', n.padEnd(16), c);

fs.writeFileSync('_work/subtitle_owner.csv', 'off;len;file\n' +
  assigned.map(a => [a.off, a.len, a.file].join(';')).join('\n') + '\n');
console.log('\nwritten _work/subtitle_owner.csv');
fs.closeSync(fd);
