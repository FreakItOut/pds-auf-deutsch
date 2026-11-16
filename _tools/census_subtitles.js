// census_subtitles.js — Whole-disc census of NUL-terminated printable runs
// (len 8..200). Records per-run metadata: raw byte offset (bin), length,
// charclass histogram, and headline stats. NO text content in this summary.
// Output: _work/subline_census.csv (off;len;sector;offInSector;l;u;d;p;o;c)
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const SECTORS = 274450;

const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);
const buf = Buffer.alloc(2352);
const rows = [];
let carriedRun = []; // to handle runs spanning sector boundary: simple — treat per sector only (slack: subtitle lines mostly < 2K)
for (let s = 0; s < SECTORS; s++) {
  fs.readSync(fd, buf, 0, 2352, s * 2352);
  let j = 16;
  while (j < 2352) {
    if (isP(buf[j])) {
      const st = j;
      while (j < 2352 && isP(buf[j])) j++;
      if (j < 2352 && buf[j] === 0 && j - st >= 8 && j - st <= 200) {
        // charclass histogram
        let L = 0, U = 0, D = 0, P = 0, O = 0;
        for (let k = st; k < j; k++) {
          const x = buf[k];
          if (x >= 0x61 && x <= 0x7a) L++;
          else if (x >= 0x41 && x <= 0x5a) U++;
          else if (x >= 0x30 && x <= 0x39) D++;
          else if (x === 0x20 || (x > 0x27 && x < 0x40)) P++;
          else O++;
        }
        rows.push({ off: s * 2352 + st, len: j - st, sec: s, os: st, L, U, D, P, O });
      }
    } else j++;
  }
}
console.log('NUL-terminated printable runs (8..200):', rows.length);
// filter story-like: mostly letters
const st = rows.filter(r => (r.L + r.U) * 2 > r.len && r.L >= 5);
console.log('letter-heavy runs:', st.length);
// bucket by 1000 sectors
const b = {};
for (const r of st) { const k = Math.floor(r.sec / 1000); b[k] = (b[k] || 0) + 1; }
const ks = Object.keys(b).map(Number).sort((a, c) => a - c);
console.log('letter-heavy per 1000-sector bucket (k:count) — first 40:');
for (const k of ks.slice(0, 40)) if (b[k] > 20) console.log(' ', k * 1000, '..', k * 1000 + 999, b[k]);
fs.writeFileSync('_work/subline_census.csv',
  'off;len;sector;offInSector;L;U;D;P;O\n' +
  st.map(r => [r.off, r.len, r.sec, r.os, r.L, r.U, r.D, r.P, r.O].join(';')).join('\n') + '\n');
console.log('written _work/subline_census.csv (' + st.length + ' rows)');
