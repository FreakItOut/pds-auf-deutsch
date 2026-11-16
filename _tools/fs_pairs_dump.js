// fs_pairs_dump.js v2 — robust FS record dump: for each 62 01 1d record,
// find name, locate the first mirrored LE/BE u32 pair within 0..8 bytes after
// the name+NUL, then collect CONSECUTIVE mirrored pairs from there.
// Flags records whose pair list has more than 2 pairs (extent lists?).
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const buf = Buffer.alloc(20 * 2352);
fs.readSync(fd, buf, 0, 20 * 2352, 14 * 2352);
const NAME_OK = /^[A-Za-z0-9_.;1\-]+$/;

const all = [];
const byName = {};
for (let i = 0; i < 20 * 2352 - 60; i++) {
  if (buf[i] !== 0x62 || buf[i + 1] !== 0x01 || buf[i + 2] !== 0x1d) continue;
  for (let hdr = 13; hdr <= 17; hdr++) {
    const nl = buf[i + hdr];
    if (nl < 2 || nl > 40) continue;
    const nm = buf.slice(i + hdr + 1, i + hdr + 1 + nl).toString('latin1');
    if (!NAME_OK.test(nm)) continue;
    const base = i + hdr + 1 + nl;
    for (let k = 0; k <= 8; k++) {
      const q = base + k;
      if (q + 16 > buf.length) break;
      if (buf.readUInt32LE(q) === buf.readUInt32BE(q + 4)) {
        // collect consecutive mirrored pairs from q
        const pairs = [];
        let z = q;
        while (z + 8 <= buf.length) {
          const a = buf.readUInt32LE(z), b = buf.readUInt32BE(z + 4);
          if (a === b) { pairs.push(a); z += 8; } else break;
        }
        if (pairs.length >= 2) {
          const rec = { name: nm, pairs, dump: i, hdr };
          all.push(rec);
          (byName[nm] = byName[nm] || []).push(rec);
          break;
        }
      }
    }
    break;
  }
}
console.log('records parsed:', all.length, 'unique names:', Object.keys(byName).length);
let multi = 0;
for (const r of all) if (r.pairs.length > 2) {
  multi++;
  if (multi <= 30) console.log(' MULTI:', r.name.padEnd(16), r.pairs.join(' '));
}
console.log('records with >2 pairs:', multi);
// duplicate-name entries (same name listed twice — from multiple partitions?)
let dupNames = Object.keys(byName).filter(n => byName[n].length > 1);
console.log('names appearing multiple times:', dupNames.length, '(first 12):', dupNames.slice(0, 12).join(' '));

fs.writeFileSync('_work/fs_pairs.csv',
  'name;dump;hdr;pairs\n' + all.map(r => r.name + ';' + r.dump + ';' + r.hdr + ';' + r.pairs.join(',')).join('\n') + '\n');
console.log('written _work/fs_pairs.csv');
