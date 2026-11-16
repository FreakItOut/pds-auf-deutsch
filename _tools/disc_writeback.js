// disc_writeback.js — Apply patched files into a COPY of the EU CD1 raw disc.
// For each name in _work/patched/ that exists in fs_records_all.csv, write its
// bytes back at the FS record's LBA (2048-byte user data per sector).
// Never touches the original disc; writes _work/patched_disc1.bin.
// Validates sizes before/after and prints a technical report only.
const fs = require('fs');
const src = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const dst = '_work/patched_disc1.bin';
const patchedDir = '_work/patched';

const recs = fs.readFileSync('_work/fs_records_all.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[0], lba: +p[1], size: +p[2] }; });

const patchedFiles = fs.readdirSync(patchedDir);
let written = 0, skipped = 0, mismatch = 0, missingRec = 0;
const applied = [];

// copy whole disc first
const buf = fs.readFileSync(src);
fs.writeFileSync(dst, buf);
console.log('disc copy written:', dst, buf.length, 'bytes');

for (const fname of patchedFiles) {
  const rec = recs.find(r => r.name === fname);
  if (!rec) { console.log('NO FS RECORD for', fname, '— skipped'); missingRec++; continue; }
  const data = fs.readFileSync(patchedDir + '/' + fname);
  if (data.length !== rec.size) {
    console.error('SIZE MISMATCH', fname, 'patched', data.length, 'vs record', rec.size);
    mismatch++;
    continue;
  }
  // write 2048-byte user area per sector
  const fd = fs.openSync(dst, 'r+');
  for (let i = 0; i < rec.size; i += 2048) {
    const take = Math.min(2048, rec.size - i);
    fs.writeSync(fd, data, i, take, rec.lba * 2352 + 16 + (i / 2048) * 2352);
  }
  fs.closeSync(fd);
  applied.push({ name: fname, lba: rec.lba, size: rec.size });
  written++;
}
console.log('applied:', written, '| size-mismatch:', mismatch, '| no-record:', missingRec, '| skipped:', skipped);
console.log('files written back:');
for (const a of applied) console.log('  ', a.name.padEnd(16), 'LBA', a.lba, 'size', a.size);
// verify readback for one file
if (applied.length) {
  const a = applied[0];
  const data = fs.readFileSync(patchedDir + '/' + a.name);
  const rd = Buffer.alloc(a.size);
  const fd = fs.openSync(dst, 'r');
  for (let i = 0; i < a.size; i += 2048) {
    const take = Math.min(2048, a.size - i);
    fs.readSync(fd, rd, i, take, a.lba * 2352 + 16 + (i / 2048) * 2352);
  }
  fs.closeSync(fd);
  console.log('readback verify ' + a.name + ':', rd.equals(data) ? 'OK' : 'FAIL');
}
