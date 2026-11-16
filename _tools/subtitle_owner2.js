// subtitle_owner2.js — Redo owner attribution with the FULL FS parse (639 records).
// Uses fs_cd1_full.csv (sorted by LBA) and subtitle_hits.csv.
const fs = require('fs');
const files = fs.readFileSync('_work/fs_cd1_full.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[0], lba: +p[1], size: +p[2], lb: +p[3] }; });
files.sort((a, b) => a.lba - b.lba);

const hits = fs.readFileSync('_work/subtitle_hits.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { off: +p[0], len: +p[1] }; });

const perFile = {};
const assigned = [];
for (const h of hits) {
  // binary search
  let lo = 0, hi = files.length - 1, found = -1;
  const pos = h.off;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const f = files[mid];
    if (pos < f.lba * 2352) hi = mid - 1;
    else if (pos >= f.lba * 2352 + Math.ceil(f.size / 2048) * 2352) lo = mid + 1;
    else { found = mid; break; }
  }
  if (found >= 0) {
    const f = files[found];
    perFile[f.name] = (perFile[f.name] || 0) + 1;
    assigned.push({ ...h, file: f.name });
  }
}
console.log('assigned hits:', assigned.length, 'of', hits.length, 'files touched:', Object.keys(perFile).length);
const top = Object.entries(perFile).sort((a, b) => b[1] - a[1]);
for (const [n, c] of top.slice(0, 24)) console.log('  ', n.padEnd(18), c);

fs.writeFileSync('_work/subtitle_owner.csv', 'off;len;file\n' +
  assigned.map(a => [a.off, a.len, a.file].join(';')).join('\n') + '\n');
console.log('written _work/subtitle_owner.csv');
