// extract_subblob.js — extract the subtitle megablob from EU CD1
// (sectors 235717..247000) and profile its line structure. No text output.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');
const S0 = 235717, S1 = 247001; // exclusive end
const out = Buffer.alloc((S1 - S0) * 2048);
for (let s = S0; s < S1; s++) {
  const b = Buffer.alloc(2048);
  fs.readSync(fd, b, 0, 2048, s * 2352 + 16);
  b.copy(out, (s - S0) * 2048);
}
fs.writeFileSync('_work/subblob_cd1.bin', out);
console.log('written _work/subblob_cd1.bin,', out.length, 'bytes');

const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);
// count lines (NUL-terminated printable runs)
let lines = 0, lens = [];
let i = 0;
const pos = [];
while (i < out.length) {
  if (isP(out[i])) {
    const st = i;
    while (i < out.length && isP(out[i])) i++;
    if (i < out.length && out[i] === 0 && i - st >= 3) { lines++; lens.push(i - st); pos.push(st); }
  } else i++;
}
console.log('lines:', lines);
// length histogram
const h = {};
for (const l of lens) { const k = l < 10 ? 5 : l < 20 ? 10 : l < 40 ? 20 : l < 80 ? 40 : 80; h[k] = (h[k] || 0) + 1; }
console.log('length histogram:', JSON.stringify(h));
// detect record cycles: check earlier pattern — line lengths
console.log('first 40 line lengths:', lens.slice(0, 40).join(','));
console.log('last 20 line lengths:', lens.slice(-20).join(','));

// where do the lines densify — 16KB bucket census
const buckets = {};
for (const p of pos) { const k = Math.floor(p / 16384); buckets[k] = (buckets[k] || 0) + 1; }
const ks = Object.keys(buckets).map(Number).sort((a, b) => a - b);
console.log('dense buckets (first 25):', ks.slice(0, 25).map(k => k + ':' + buckets[k]).join(' '));
