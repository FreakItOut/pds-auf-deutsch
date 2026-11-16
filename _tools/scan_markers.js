// scan_markers.js — find structural markers inside subblob_cd1.bin:
// uppercase-letter runs (>=4) which likely are scene/file/section IDs.
// Also short 'name-like' runs of the form UPP or UPCas. Print counts only.
const fs = require('fs');
const b = fs.readFileSync('_work/subblob_cd1.bin');
const isUp = x => x >= 0x41 && x <= 0x5a;
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);

const upRuns = [];
let i = 0;
while (i < b.length) {
  if (isUp(b[i])) {
    const st = i;
    while (i < b.length && isUp(b[i])) i++;
    if (i - st >= 4) upRuns.push([st, i - st]);
  } else i++;
}
console.log('uppercase runs >=4:', upRuns.length);
// bucket by 256 KB window
const buck = {};
for (const [o, l] of upRuns) { const k = o >> 18; buck[k] = (buck[k] || 0) + 1; }
const ks = Object.keys(buck).map(Number).sort((a, c) => a - c);
console.log('upruns per 256KB (k:count, showing >20):',
  ks.filter(k => buck[k] > 20).map(k => k + ':' + buck[k]).join(' '));
console.log('empty 256KB windows:', ks.filter(k => buck[k] <= 20).length, 'of', ks.length);

// the shape of an uppercase run should be continued by lowercase? Check the
// run *followed* by lowercase (case-sensitive: names like EVT029)
let upThenLow = 0;
for (const [o, l] of upRuns.slice(0, 200)) {
  const after = o + l;
  if (after < b.length && b[after] >= 0x61 && b[after] <= 0x7a) upThenLow++;
}
console.log('upper-runs with lowercase following (first 200):', upThenLow);

// how many upFullyAlpha runs look like evt-name pattern: 4-10 chars with digits?
const upWithDigit = upRuns.filter(([o, l]) => [...Array(l)].some((_, k) => {
  const x = b[o + k]; return x >= 0x30 && x <= 0x39;
}));
console.log('upruns containing digits:', upWithDigit.length, '(first 15):',
  upWithDigit.slice(0, 15).map(([o, l]) => o).join(' '));
const upNoDigit = upRuns.filter(([o, l]) => ![...Array(l)].some((_, k) => (b[o + k] >= 0x30 && b[o + k] <= 0x39)));
console.log('upruns no digits:', upNoDigit.length, '(first 10 offsets):', upNoDigit.slice(0, 10).map(([o, l]) => o).join(' '));
