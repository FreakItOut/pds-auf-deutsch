// subtitle_scan.js — Scan ALL EU CD1 files for sentence-like plaintext
// (>=2 spaces + >=3 lowercase words) and count per file. Output only counts.
const fs = require('fs');
const FD = fs.openSync('Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin', 'r');
const SECTORS = 274450, SEC = 2352;

// chunked read of the whole data area, in 2000-sector windows
const WIN = 2000;
const buf = Buffer.alloc(WIN * SEC);
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);

// gather global hits of sentences with offsets
let i = 0;
const hits = []; // start offset within disc (sector*2352+16)
let carried = 0; // unfinished long-run carried over to next window? handle simply
while (i < SECTORS) {
  const n = Math.min(WIN, SECTORS - i);
  const rd = n * SEC;
  const got = fs.readSync(FD, buf, 0, rd, i * SEC);
  const nn = Math.floor(got / SEC);
  let j = 0;
  while (j < nn * SEC) {
    if (isP(buf[j])) {
      const st = j;
      while (j < nn * SEC && isP(buf[j])) j++;
      const len = j - st;
      if (len >= 24) {
        let sp = 0, low = 0;
        for (let k = st; k < j; k++) {
          const x = buf[k];
          if (x === 0x20) sp++;
          else if (x >= 0x61 && x <= 0x7a) low++;
        }
        if (sp >= 4 && low >= 10) hits.push({ off: i * SEC + st + 16, len });
      }
    } else j++;
  }
  i += nn;
}
console.log('sentence-like plaintext hits (>=24B, 4+ spaces, 10+ lowercase):', hits.length);
// bucket by sector → file via fs table
const fsTab = fs.readFileSync('_work/fs_cd1_table.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[1], lba: p[2] === 'undefined' ? -1 : +p[2] }; });
// We lack sector sizes; approximate owner by nearest preceding lba from a second source:
// parse LBAs fresh from disc (records known)
const owners = fs.readFileSync('_work/fs_cd1_table.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[1], off: +p[0] }; });
// Instead: scan lbAs? skip here — print top clusters by 2048-sector bucket
const buckets = {};
for (const h of hits) { const k = Math.floor(h.off / (2048 * 2352)); buckets[k] = (buckets[k] || 0) + 1; }
const ks = Object.keys(buckets).map(Number).sort((a, b) => a - b);
console.log('clusters by 2048-sector bucket:');
for (const k of ks) console.log('  bucket', k, 'startSector', k * 2048, 'count', buckets[k]);
fs.writeFileSync('_work/subtitle_hits.csv', 'off;len\n' + hits.map(h => h.off + ';' + h.len).join('\n') + '\n');
console.log('written _work/subtitle_hits.csv');
fs.closeSync(FD);
