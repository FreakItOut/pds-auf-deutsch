// Extract ALL plausible dialogue strings from a PDS game-data member file.
//Charset observed in Spanish patch data:
//  0x8a=á 0x8b=é 0x8c=í 0x8d=ó 0x8e=ú 0x8f=ñ  (verify & extend)
// strings are NUL-terminated runs of printable ASCII + accents + CR/LF + control bytes.
// Output: CSV (id, offset_hex, length, decoded_utf8) — for local translation work.
const fs = require('fs');
const path = require('path');

const ACCENTS = { 0x8a: 'á', 0x8b: 'é', 0x8c: 'í', 0x8d: 'ó', 0x8e: 'ú', 0x8f: 'ñ' };

function decodeByte(x) {
  if (x >= 0x20 && x <= 0x7e) return String.fromCharCode(x);
  if (ACCENTS[x]) return ACCENTS[x];
  if (x === 0x0a) return '\\n';
  if (x === 0x0d) return '\\r';
  return null;
}

const file = process.argv[2];
const tag = process.argv[3] || path.basename(file, '.bin');
const b = fs.readFileSync(file);

const entries = [];
let start = -1;
for (let i = 0; i < b.length; i++) {
  const isAllowed = decodeByte(b[i]) !== null;
  if (isAllowed) {
    if (start < 0) start = i;
  } else {
    if (start >= 0 && b[i] === 0x00) {
      const len = i - start;
      if (len >= 4) {
        let txt = '';
        let ok = true;
        for (let j = start; j < i; j++) {
          const d = decodeByte(b[j]);
          if (d === null) { ok = false; break; }
          txt += d;
        }
        if (ok) entries.push({ off: start, len, txt });
      }
    }
    start = -1;
  }
}

// CSV schreiben
let csv = 'id;off_hex;len;text\n';
entries.forEach((e, i) => {
  csv += `${i};0x${e.off.toString(16)};${e.len};"${e.txt.replace(/"/g, '""')}"\n`;
});
const out = path.join(path.dirname(file), `strings_${path.basename(file, '.bin')}.csv`);
fs.writeFileSync(out, csv);

console.log(`extracted ${entries.length} strings -> ${out}`);
// Kurze Qualitätsprobe (nur die ersten 8, kurze Ausgaben)
entries.slice(0, 12).forEach(e => console.log(`#0x${e.off.toString(16)} [${e.len}] ${e.txt.slice(0, 60)}`));
console.log('... total bytes covered: %d', entries.reduce((s, e) => s + e.len, 0));
