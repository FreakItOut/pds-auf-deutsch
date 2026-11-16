// Debug: print EU and ES table run lengths only (no text).
const fs = require('fs');
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || ch === 0x85 || (ch >= 0x8a && ch <= 0x8f) || ch === 0x91 || ch === 0x0a || ch === 0x0d;
function extractRuns(buf, start) {
  const runs = []; let i = start;
  while (i < buf.length) {
    if (isP(buf[i])) {
      const st = i; while (i < buf.length && isP(buf[i])) i++;
      const len = i - st;
      if (len >= 2 && i < buf.length && buf[i] === 0x00) { runs.push(len); i++; }
      else if (len >= 2 && i >= buf.length) { runs.push(len); break; }
      else break;
    } else if (buf[i] === 0x00) i++;
    else break;
  }
  return runs;
}
const eu = fs.readFileSync('_work/BTL_A5.FNT');
const es = fs.readFileSync('_work/cd1_0.bin');
const euRuns = extractRuns(eu, 0x5f5e4);
const esRuns = extractRuns(es, 0x1d81af);
console.log('EU runs', euRuns.length);
console.log('EU lens', euRuns.join(' '));
console.log('ES runs', esRuns.length);
console.log('ES lens', esRuns.join(' '));
