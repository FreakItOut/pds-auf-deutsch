// analyze_sis.js — dump what follows each S!S header (00 ff ff ff ff ff ff ff ff ff ff 00)
// in several script files. No game text is printed; only byte/structure stats.
const fs = require('fs');

const SIG = Buffer.from([0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00]);
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);

function analyze(name) {
  const p = '_work/' + name;
  if (!fs.existsSync(p)) { console.log(name, 'NOT EXTRACTED'); return; }
  const b = fs.readFileSync(p);
  console.log('===', name, 'len', b.length);

  // locate all signature occurrences
  let idx = 0, hits = [];
  while ((idx = b.indexOf(SIG, idx)) !== -1) { hits.push(idx); idx += 12; }
  console.log('S!S headers:', hits.length);

  for (const h of hits.slice(0, 8)) {
    const label = b.slice(h + 12, h + 16);
    console.log('  @0x' + h.toString(16), 'label', label.toString('hex'),
      '("' + [...label].map(x => (x >= 0x20 && x <= 0x7e) ? String.fromCharCode(x) : '?').join('') + '")');
    // bytes 0x10..0x30 after header
    const d = b.slice(h + 0x10, h + 0x30);
    let printable = 0;
    for (const x of d) if (isP(x)) printable++;
    console.log('     +0x10..0x30 hex:', d.toString('hex'));
    console.log('     printable in that window:', printable + '/' + d.length);
  }

  // printable-run census across whole file (runs >=6, NUL-terminated)
  let runs = [], i = 0;
  while (i < b.length) {
    if (isP(b[i])) {
      const st = i;
      while (i < b.length && isP(b[i])) i++;
      if (i - st >= 6 && i < b.length && b[i] === 0) runs.push(st);
      i++;
    } else i++;
  }
  console.log('printable NUL-terminated runs (>=6):', runs.length,
    'first@0x' + (runs.length ? runs[0].toString(16) : '-'),
    'last@0x' + (runs.length ? runs[runs.length - 1].toString(16) : '-'));
  // where do runs cluster? bucket by 16KB
  const buckets = {};
  for (const s of runs) { const k = Math.floor(s / 16384); buckets[k] = (buckets[k] || 0) + 1; }
  const ks = Object.keys(buckets).map(Number).sort((a, b) => a - b);
  console.log('run clusters (16KB bucket:start-count...):', ks.slice(0, 12).map(k => k + ':' + buckets[k]).join(' '), ks.length > 12 ? '...' : '');
}

for (const n of ['CAMPSCR0.PNB', 'CAMPSCR4.PNB', 'CARASCR4.SCB', 'CARASCR2.PNB', 'BTL_A5.FNT', 'EVT000_1.FNT']) analyze(n);
