// extract_eu_file2.js — Extract any named file from EU CD1 using the FULL
// FS record list (_work/fs_records_all.csv). Usage: node extract_eu_file2.js NAME [out]
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';

const name = process.argv[2];
if (!name) { console.error('usage: node extract_eu_file2.js <FILE.EXT> [out]'); process.exit(1); }
const wanted = name.toUpperCase();
const rows = fs.readFileSync('_work/fs_records_all.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[0], lba: +p[1], size: +p[2] }; });
const rec = rows.filter(r => r.name.split(';')[0].toUpperCase() === wanted);
if (rec.length === 0) { console.error('file not found:', wanted); process.exit(1); }
if (rec.length > 1) console.error('WARNING multiple records (' + rec.length + '), using first');
const r = rec[0];
const fd = fs.openSync(track, 'r');
const out = process.argv[3] || ('_work/' + r.name);
const data = Buffer.alloc(r.size);
for (let i = 0; i < r.size; i += 2048) {
  const take = Math.min(2048, r.size - i);
  fs.readSync(fd, data, i, take, (r.lba * 2352) + 16 + (i / 2048) * 2352);
}
fs.writeFileSync(out, data);
console.log(r.name, 'LBA', r.lba, 'size', r.size, '(' + Math.round(r.size / 1024) + ' KiB)');
console.log('written', out);
