// void_probe.js — Analyze the big "void" cluster (sectors ~236235..236345)
// between E128SE.BIN and CHARCMP1.CGB. Print per-sector run statistics and
// charclass histograms — NO game text.
const fs = require('fs');
const track = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const fd = fs.openSync(track, 'r');

const S0 = 236200, S1 = 236360;
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);
const cls = x => {
  if (x >= 0x61 && x <= 0x7a) return 'l'; // lowercase
  if (x >= 0x41 && x <= 0x5a) return 'u'; // uppercase
  if (x >= 0x30 && x <= 0x39) return 'd'; // digit
  if (x === 0x20 || x === 0x2e || x === 0x2c || x > 0x27 && x < 0x40) return 'p'; // punct/space
  if (isP(x)) return 'o'; // other printable
  return 'c'; // control
};

const buf = Buffer.alloc(2352);
const rows = [];
for (let s = S0; s <= S1; s++) {
  fs.readSync(fd, buf, 0, 2352, s * 2352);
  // runs of printable bytes terminated by NUL
  const runs = [];
  let j = 16;
  while (j < 2352) {
    if (isP(buf[j])) {
      const st = j;
      while (j < 2352 && isP(buf[j])) j++;
      // count a run only if followed by NUL
      if (j < 2352 && buf[j] === 0) runs.push([st, j - st]);
    } else j++;
  }
  if (runs.length === 0) continue;
  // per-run charclass breakdown
  let lowerRun = 0, mixed = 0;
  const lens = [], sigs = [];
  for (const [st, len] of runs) {
    const hist = { l: 0, u: 0, d: 0, p: 0, o: 0, c: 0 };
    for (let k = st; k < st + len; k++) hist[cls(buf[k])]++;
    lens.push(len);
    if (hist.l >= 5) lowerRun++;
    // class signature like "lulp" (letters almost everywhere)
    sigs.push(Array.from(new Set(['l','u','d','p','o'].filter(k => hist[k] > 0))).join(''));
  }
  rows.push({ s, runs: runs.length, lowerRun, lens: lens.slice(0, 8), sigs: sigs.slice(0, 8) });
}
console.log('sectors with NUL-terminated printable runs:', rows.length, 'of', S1 - S0 + 1);
for (const r of rows.slice(0, 30))
  console.log('sector', r.s, '| runs', r.runs, '| lower-heavy', r.lowerRun,
    '| lens', r.lens.join(','), '| sigs', r.sigs.join('|'));
if (rows.length > 30) console.log('...', (rows.length - 30), 'more sectors');

// how many lowercase-heavy runs total?
let allLow = 0, allRuns = 0;
for (const r of rows) { allLow += r.lowerRun; allRuns += r.runs; }
console.log('runs total:', allRuns, 'lower-heavy:', allLow);
