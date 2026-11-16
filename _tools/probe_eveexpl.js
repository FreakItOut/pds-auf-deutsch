// probe_eveexpl.js — Structural probe of EVEEXPL.FNT
const fs = require('fs');
const b = fs.readFileSync('_work/EVEEXPL.FNT');
console.log('len', b.length);

const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);

// NUL-terminated printable runs with NUL-skip, sentences filter
const sent = [], junk = [], all = [];
let i = 0;
while (i < b.length) {
  if (isP(b[i])) {
    const st = i;
    while (i < b.length && isP(b[i])) i++;
    const len = i - st;
    if (len >= 4 && i < b.length && b[i] === 0) {
      all.push(st);
      let t = '';
      for (let j = st; j < i; j++) t += String.fromCharCode(b[j]);
      const sp = (t.match(/ /g) || []).length, low = (t.match(/[a-z]{2,}/g) || []).length;
      if (sp >= 2 && low >= 3) { sent.push({ off: st, len, sp, low }); junkPush(st, len); }
      else junk.push(st);
    }
    i++;
  } else i++;
}
function junkPush(){/*noop*/}
console.log('runs >=4:', all.length, 'sentences:', sent.length, 'junk:', junk.length);

// cluster the sentences
sent.sort((a, b) => a.off - b.off);
const clusters = [];
let cs = sent[0]?.off ?? 0, ce = cs;
for (let k = 1; k < sent.length; k++) {
  if (sent[k].off - ce < 0x8000) ce = sent[k].off;
  else { clusters.push([cs, ce]); cs = sent[k].off; ce = cs; }
}
if (sent.length) clusters.push([cs, ce]);
console.log('sentence clusters:', clusters.length);
for (const [s, e] of clusters.slice(0, 25))
  console.log('  0x' + s.toString(16) + ' .. 0x' + e.toString(16),
    '(' + Math.round((e - s) / 1024) + ' KB span)');

// sentence-length histogram
const lh = {};
for (const s of sent) { const k = s.len < 32 ? 'a<32' : s.len < 64 ? 'b32-63' : s.len < 128 ? 'c64-127' : 'd>=128'; lh[k] = (lh[k] || 0) + 1; }
console.log('sentence length histogram:', JSON.stringify(lh));
fs.writeFileSync('_work/eveexpl_sentences.csv',
  'off;len\n' + sent.map(s => s.off + ';' + s.len).join('\n') + '\n');
console.log('written _work/eveexpl_sentences.csv');
