// patch_btl.js — Tier 1: overwrite BTL English strings with German in-place.
// Strings are NUL-terminated; we overwrite each occurrence and NUL-pad/truncate
// to the original byte-length (so file sizes and pointers stay valid).
const fs = require('fs');

// load translation map
const lines = fs.readFileSync('_work/btl_unique_strings.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean);
const T = {};
for (const l of lines) {
  const p = l.split(';');
  T[p[1]] = p[2] || '';
}

const files = [...new Set(fs.readFileSync('_work/strings_eu_btl_tables.csv', 'latin1')
  .split(/\r?\n/).slice(1).filter(Boolean).map(l => l.split(';')[0]))];

const outDir = '_work/patched';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

let totalPatched = 0, totalTruncated = 0, totalSkipped = 0;
for (const fname of files) {
  const srcPath = '_work/' + fname;
  if (!fs.existsSync(srcPath)) { console.log('MISSING', fname); continue; }
  const data = fs.readFileSync(srcPath);
  const buf = Buffer.from(data);
  let patched = 0, truncated = 0;
  // For each English string, find all occurrences and replace
  for (const [en, de] of Object.entries(T)) {
    if (!en || !de) continue;
    // EN must be NUL-terminated in the file; search for en + '\0'
    const needle = Buffer.from(en + '\0', 'latin1');
    let pos = 0;
    while (true) {
      const idx = buf.indexOf(needle, pos);
      if (idx < 0) break;
      // slot size = distance to next NUL after the original string's NUL
      // We overwrite in-place: write de + '\0' + NUL padding to original length
      const origLen = en.length + 1; // including NUL
      let toWrite = de;
      if (toWrite.length + 1 > origLen) {
        toWrite = toWrite.slice(0, origLen - 1);
        truncated++;
      }
      // write
      buf.write(toWrite, idx, 'latin1');
      buf[idx + toWrite.length] = 0x00;
      for (let k = idx + toWrite.length + 1; k < idx + origLen; k++) buf[k] = 0x00;
      pos = idx + origLen;
      patched++;
    }
  }
  fs.writeFileSync(outDir + '/' + fname, buf);
  totalPatched += patched;
  totalTruncated += truncated;
  console.log(fname.padEnd(16), 'patched=' + patched, 'truncated=' + truncated);
}
console.log('---');
console.log('total patched:', totalPatched, 'truncated:', totalTruncated);
console.log('patched files in:', outDir);
