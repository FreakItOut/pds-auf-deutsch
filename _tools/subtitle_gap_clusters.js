// subtitle_gaps2.js — Analyze the unassigned sentence hits using fs_cd1_full.csv.
// For each gap cluster: report sector range, previous/next FS file, and whether
// the hits sit shortly AFTER a file's end (data beyond declared size) or in
// true void. Prints structure info only, no game text.
const fs = require('fs');
const files = fs.readFileSync('_work/fs_cd1_full.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[0], lba: +p[1], size: +p[2], lb: +p[3] }; });
files.sort((a, b) => a.lba - b.lba);

const offsets = files.map(f => ({ n: f.name, s: f.lba * 2352, e: f.lba * 2352 + Math.ceil(f.size / 2048) * 2352 }));

const hits = fs.readFileSync('_work/subtitle_hits.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => +l.split(';')[0])
  .filter(h => !offsets.some(r => h >= r.s && h < r.e))
  .sort((a, b) => a - b);
console.log('unassigned hits:', hits.length);

// cluster with 64 KB window
const clusters = [];
let cs = hits[0], ce = hits[0];
for (let k = 1; k < hits.length; k++) {
  if (hits[k] - ce < 0x10000) ce = hits[k];
  else { clusters.push([cs, ce]); cs = hits[k]; ce = hits[k]; }
}
clusters.push([cs, ce]);
console.log('clusters:', clusters.length);

// classify each cluster by neighbor context
const rows = [];
for (const [s0, e0] of clusters) {
  // previous file that ended before cluster, next file starting after cluster
  let prev = null, next = null;
  for (const r of offsets) {
    if (r.e <= s0 && (!prev || r.e > prev.e)) prev = r;
    if (r.s > e0 && (!next || r.s < next.s)) next = r;
  }
  const byteGap = prev && next ? next.s - prev.e : -1;
  const cls = [];
  if (prev) {
    const after = (s0 - prev.e) / 2352; // sectors beyond prev end
    if (after <= 10) cls.push('right-after ' + prev.n + ' (+' + after.toFixed(0) + ' sec)');
  }
  if (next) {
    const before = (next.s - e0) / 2352;
    if (before <= 10) cls.push('right-before ' + next.n + ' (-' + before.toFixed(0) + ' sec)');
  }
  const hitCount = hits.filter(h => h >= s0 && h <= e0).length;
  rows.push({ s0, e0, prev: prev && prev.n, next: next && next.n, byteGap, hitCount, cls: cls.join(' ') });
}

// summary classes
const classCount = {};
for (const r of rows) {
  const key = r.cls || 'VOID';
  classCount[key] = (classCount[key] || 0) + r.hitCount;
}
console.log('\nhit count by class:');
for (const [k, v] of Object.entries(classCount).sort((a, b) => b[1] - a[1]).slice(0, 20))
  console.log('  ', (k || 'VOID').padEnd(50), v);

fs.writeFileSync('_work/subtitle_gap_clusters.csv',
  'start;end;hits;prev;next;gapBytes;class\n' +
  rows.map(r => [r.s0, r.e0, r.hitCount, r.prev || '', r.next || '', r.byteGap, r.cls || 'VOID'].join(';')).join('\n') + '\n');
console.log('\nwritten _work/subtitle_gap_clusters.csv');
