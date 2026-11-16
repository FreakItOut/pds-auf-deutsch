// cluster_sublines.js — Group letter-heavy subline census rows into spatial
// clusters and attribute to FS files (fs_cd1_full.csv). Structure only.
const fs = require('fs');
const rows = fs.readFileSync('_work/subline_census.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { off: +p[0], len: +p[1], sec: +p[2], os: +p[3] }; });

const files = fs.readFileSync('_work/fs_cd1_full.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean)
  .map(l => { const p = l.split(';'); return { name: p[0], lba: +p[1], size: +p[2] }; });
files.sort((a, b) => a.lba - b.lba);

// cluster rows by sector with gap threshold of 150 sectors
const G = 150;
const clusters = [];
let cur = [rows[0]];
for (let k = 1; k < rows.length; k++) {
  if (rows[k].sec - cur[cur.length - 1].sec <= G) cur.push(rows[k]);
  else { clusters.push(cur); cur = [rows[k]]; }
}
clusters.push(cur);
console.log('letter-heavy line clusters (gap<=150 sec):', clusters.length);

const out = [];
for (const c of clusters) {
  const s0 = c[0].sec, s1 = c[c.length - 1].sec;
  const range = [s0 * 2352 + 16, s1 * 2352 + 2351];
  // owner: FS file overlapping the cluster's midpoint sector span
  let owner = null;
  const midS0 = s0, midS1 = s1;
  for (const f of files) {
    if (f.lba === 0 && f.size === 0) continue;
    const fs0 = f.lba, fs1 = f.lba + Math.ceil(f.size / 2048) - 1;
    if (midS0 <= fs1 && midS1 >= fs0) { owner = f.name; break; }
  }
  let prev = null;
  for (const f of files) { if (f.lba <= s0 && f.size > 0 && (!prev || f.lba > prev.lba)) prev = f; }
  let next = null;
  for (const f of files) { if (f.lba >= s1 && f.size > 0 && (!next || f.lba < next.lba)) next = f; }
  const c2 = c.map(r => r.len);
  c2.sort((a, b) => a - b);
  const med = c2[Math.floor(c2.length / 2)];
  out.push({ s0, s1, count: c.length, med, owner, prev: prev && prev.name, next: next && next.name });
}
out.sort((a, b) => b.count - a.count);
console.log('\ntop 45 clusters by line count:');
for (const o of out.slice(0, 45))
  console.log('  sec ' + o.s0 + '..' + o.s1, 'lines', String(o.count).padStart(4),
    'medlen', String(o.med).padStart(3),
    '| owner:', (o.owner || '-').padEnd(16),
    '| between', o.prev, '..', o.next);

fs.writeFileSync('_work/subline_clusters.csv',
  's0;s1;lines;medlen;owner;prev;next\n' +
  out.map(o => [o.s0, o.s1, o.count, o.med, o.owner || '', o.prev || '', o.next || ''].join(';')).join('\n') + '\n');
console.log('written _work/subline_clusters.csv');
