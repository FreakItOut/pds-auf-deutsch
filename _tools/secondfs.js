// secondfs.js — scan the WHOLE disc for Sega-FS record signatures 62 01 1d XX
// with parseable names; bucket by sector to see if there are other directories.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SECTORS = 274450;
const NAME_OK = /^[A-Za-z0-9_.;1\-]+$/;
const buf = Buffer.alloc(1000 * 2352);
const hits = [];
for (let s0 = 0; s0 < SECTORS; s0 += 1000) {
  const n = Math.min(1000, SECTORS - s0);
  fs.readSync(fd, buf, 0, n * 2352, s0 * 2352);
  for (let i = 0; i < (n - 1) * 2352; i++) {
    if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
      for (let hdr = 13; hdr <= 17; hdr++) {
        const nl = buf[i + hdr];
        if (nl < 2 || nl > 40) continue;
        const nm = buf.slice(i + hdr + 1, i + hdr + 1 + nl).toString('latin1');
        if (!NAME_OK.test(nm)) continue;
        hits.push({ sec: s0 + Math.floor(i / 2352), iSec: i % 2352, name: nm });
        break;
      }
    }
  }
}
console.log('named record hits on disc:', hits.length);
const bySec = {};
for (const h of hits) bySec[h.sec] = (bySec[h.sec] || 0) + 1;
const ks = Object.keys(bySec).map(Number).sort((a, b) => a - b);
console.log('sectors with records:', ks.length);
// print clusters
let prev = -10, cs = -1, cc = 0;
const clusters = [];
for (const k of ks) {
  if (k - prev <= 3) { cc += bySec[k]; }
  else { if (cs >= 0) clusters.push([cs, prev, cc]); cs = k; cc = bySec[k]; }
  prev = k;
}
if (cs >= 0) clusters.push([cs, prev, cc]);
console.log('record-sector clusters:', clusters.length);
for (const [a, b, c] of clusters) console.log('  sec ' + a + '..' + b, 'records', c);
