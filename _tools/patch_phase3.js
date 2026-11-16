// patch_phase3.js — Patch FLD/EVT/MENU strings in-place.
// Reads _work/phase3_strings.csv (en;de pairs) and patches all occurrences
// in the specified files. NUL-pads to original length. Keeps file sizes.
const fs = require('fs');

const files = process.argv.slice(2);
if (!files.length) {
  console.error('usage: node patch_phase3.js <file1> [file2...]');
  process.exit(1);
}

// Load translation map from CSV
const csvPath = '_work/phase3_strings.csv';
if (!fs.existsSync(csvPath)) {
  console.error('Translation file not found:', csvPath);
  process.exit(1);
}
const T = {};
const lines = fs.readFileSync(csvPath, 'latin1').split(/\r?\n/).filter(Boolean);
for (const l of lines.slice(1)) {
  const p = l.split(';');
  if (p.length >= 3 && p[1] && p[2]) {
    T[p[1]] = p[2];
  }
}
console.log('Loaded', Object.keys(T).length, 'translations');

const outDir = '_work/patched';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

let totalPatched = 0, totalTruncated = 0, totalSkipped = 0;
for (const fname of files) {
  const srcPath = '_work/' + fname;
  if (!fs.existsSync(srcPath)) { console.log('MISSING', fname); continue; }
  const data = fs.readFileSync(srcPath);
  const buf = Buffer.from(data);
  let patched = 0, truncated = 0, skipped = 0;
  for (const [en, de] of Object.entries(T)) {
    if (!en || !de) continue;
    const needle = Buffer.from(en + '\0', 'latin1');
    let pos = 0;
    while (true) {
      const idx = buf.indexOf(needle, pos);
      if (idx < 0) break;
      const origLen = en.length + 1;
      let toWrite = de;
      if (toWrite.length + 1 > origLen) {
        toWrite = toWrite.slice(0, origLen - 1);
        truncated++;
      }
      buf.write(toWrite, idx, 'latin1');
      buf[idx + toWrite.length] = 0x00;
      for (let k = idx + toWrite.length + 1; k < idx + origLen; k++) buf[k] = 0x00;
      pos = idx + origLen;
      patched++;
    }
  }
  fs.writeFileSync(outDir + '/' + fname, buf);
  const size = fs.statSync(srcPath).size;
  const newSize = fs.statSync(outDir + '/' + fname).size;
  totalPatched += patched;
  totalTruncated += truncated;
  console.log(fname.padEnd(16), 'patched=' + patched, 'truncated=' + truncated, 'size', size === newSize ? 'OK' : 'SIZE-CHANGED !!!');
}
console.log('--- total patched:', totalPatched, 'truncated:', totalTruncated);