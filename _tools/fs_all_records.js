// fs_all_records.js — parse ALL 62 01 1d records in sector 14..60 (full window),
// list name+lba+size for every record, point out duplicates and
// any record whose LBA is in 235700..235730 (blob start candidates).
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const RECORD_SECTORS = 0, RECORD_SPAN = 70; // scan sectors 0..70
const buf = Buffer.alloc(RECORD_SPAN * 2352);
fs.readSync(fd, buf, 0, buf.length, RECORD_SECTORS * 2352);
const NAME_OK = /^[A-Za-z0-9_.;1\-]+$/;

const recs = [];
for (let i = 0; i < buf.length - 60; i++) {
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
        const pairs = [];
        let z = q;
        while (z + 8 <= buf.length) {
          const a = buf.readUInt32LE(z), b2 = buf.readUInt32BE(z + 4);
          if (a === b2) { pairs.push(a); z += 8; } else break;
        }
        if (pairs.length >= 2) {
          recs.push({ name: nm, lba: pairs[0], size: pairs[1], dump: i, nPairs: pairs.length });
          break;
        }
      }
    }
    break;
  }
}
console.log('records:', recs.length, 'unique names:', new Set(recs.map(r => r.name)).size);
// sorted by lba
const near = recs.filter(r => r.lba >= 235600 && r.lba <= 235730);
console.log('records with lba 235600..235730:', near.length);
for (const r of near) console.log('  ', r.name.padEnd(18), 'lba', r.lba, 'size', r.size);
(blob => {})(); // noop
// also: biggest records by size
const big = [...recs].sort((a, b) => b.size - a.size).slice(0, 12);
console.log('largest records by size:');
for (const r of big) console.log('  ', r.name.padEnd(18), 'lba', r.lba, 'size', r.size);
// bucket records near the megablob peaks:
const nearBig = recs.filter(r => (r.lba >= 236000 && r.lba <= 247200));
console.log('records inside 236000..247200:', nearBig.length);
for (const r of nearBig.slice(0, 30)) console.log('  ', r.name.padEnd(18), 'lba', r.lba, 'size', r.size);
fs.writeFileSync('_work/fs_records_all.csv',
  'name;lba;size;dump;iPairs\n' + recs.map(r => [r.name, r.lba, r.size, r.dump, r.nPairs].join(';')).join('\n') + '\n');
console.log('written _work/fs_records_all.csv');
