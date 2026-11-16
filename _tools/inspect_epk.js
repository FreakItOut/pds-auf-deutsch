// Inspect E011.EPK structure.
const fs = require('fs');
const p = '_work/E011.EPK';
if (!fs.existsSync(p)) { console.log('extracting...'); }
// extract if missing
if (!fs.existsSync(p)) {
  const { execSync } = require('child_process');
}
const b = fs.readFileSync(p);
console.log('len', b.length);
console.log('head:', b.slice(0, 64).toString('hex'));
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x88 && ch <= 0x8f) || ch === 0x0a || ch === 0x0d;
let best = 0, bs = 0, cur = 0, cs = 0;
for (let i = 0; i < b.length; i++) { if (isP(b[i])) { if (cur === 0) cs = i; cur++; if (cur > best) { best = cur; bs = cs; } } else cur = 0; }
console.log('longest printable run', best, 'at 0x' + bs.toString(16));
let i = 0, runs = 0;
while (i < b.length) {
  if (isP(b[i])) { const st = i; while (i < b.length && isP(b[i])) i++; const len = i - st; if (len >= 4 && i < b.length && b[i] === 0) { runs++; i++; } else if (len >= 4 && i >= b.length) { runs++; break; } else if (i < b.length && !isP(b[i]) && b[i] !== 0) break; } else if (b[i] === 0) i++; else break;
}
console.log('NUL-runs>=4:', runs);
for (const w of ['Edge', 'Azel', 'Craymen', 'Zoah', 'the ']) { let idx = 0, c = 0; while ((idx = b.indexOf(w, idx)) !== -1) { c++; idx++; } console.log(w, 'hits', c); }
