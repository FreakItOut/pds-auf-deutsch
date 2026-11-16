// analyze_evt_blob.js — structural analysis of the dialog blob in EVT000_1.FNT
// region 0xc9f200..0xca0500. Prints structure metadata only (lengths, control
// bytes, spacing), NOT the text itself.
const fs = require('fs');
const b = fs.readFileSync('_work/EVT000_1.FNT');

const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);
const START = 0xc9f200, END = 0xca0500;

// 1) enumerate sentences precisely
const sent = [];
let i = START;
while (i < END) {
  if (isP(b[i])) {
    const st = i;
    while (i < END && isP(b[i])) i++;
    if (i - st >= 4) sent.push({ off: st, len: i - st });
  } else i++;
}
console.log('sentence runs in window:', sent.length);
console.log('offsets:', sent.map(s => '0x' + s.off.toString(16)).join(' '));
console.log('lengths:', sent.map(s => s.len).join(' '));

// 2) gaps between runs (control codes between strings?)
for (let k = 0; k < sent.length - 1 && k < 6; k++) {
  const g0 = sent[k].off + sent[k].len, g1 = sent[k + 1].off;
  const gap = b.slice(g0, g1);
  console.log('gap', k, 'len', g1 - g0, 'hex:', gap.toString('hex'));
}

// 3) before first run / after last
console.log('pre-blob (0x' + (START - 0x40).toString(16) + '):', b.slice(START - 0x40, START).toString('hex'));
console.log('post-blob:', b.slice(sent[sent.length - 1].off + sent[sent.length - 1].len,
  Math.min(END, sent[sent.length - 1].off + sent[sent.length - 1].len + 0x40)).toString('hex'));

// 4) byte histogram of the whole window (non-string bytes)
const counts = {};
for (let j = START; j < END; j++) {
  const x = b[j];
  if (!isP(x)) counts[x] = (counts[x] || 0) + 1;
}
console.log('non-printable byte histogram (top 15):',
  Object.entries(counts).sort((a, c) => c[1] - a[1]).slice(0, 15)
    .map(e => '0x' + Number(e[0]).toString(16) + ':' + e[1]).join(' '));

// 5) printable-run census for the whole rest of EVT000_1 (junk runs — are they
//    somewhere structured?) quick length histogram
const runs = [];
i = 0;
while (i < b.length) {
  if (isP(b[i])) {
    const st = i;
    while (i < b.length && isP(b[i])) i++;
    if (i - st >= 6 && i < b.length && b[i] === 0) runs.push(i - st);
    i++;
  } else i++;
}
const lh = {};
for (const l of runs) { const k = l < 16 ? 'a<16' : l < 32 ? 'b16-31' : l < 64 ? 'c32-63' : l < 128 ? 'd64-127' : 'e>=128'; lh[k] = (lh[k] || 0) + 1; }
console.log('all-run length histogram:', JSON.stringify(lh));
