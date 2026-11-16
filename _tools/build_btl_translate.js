// Build a clean translation CSV for the BTL battle-UI strings.
// Filters out binary artifacts, keeps meaningful strings.
const fs = require('fs');
const lines = fs.readFileSync('_work/strings_eu_btl_tables.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean);

const seen = new Set();
const clean = [];
for (const l of lines) {
  const parts = l.split(';');
  const text = parts.slice(2).join(';');
  if (seen.has(text)) continue;
  seen.add(text);
  // filter artifacts
  if (text.length < 3) continue;
  if (/[\r\n\t]/.test(text)) continue;          // control chars
  if (/[^A-Za-z0-9 .,!?'"%\-:/()&+]/.test(text)) continue; // non-printable
  if (/NOMAL/.test(text) && text !== 'NOMAL') continue; // binary artifact with NOMAL
  if (text === 'LV') continue; // too short/ambiguous
  clean.push(text);
}

// write unique strings CSV (for translation)
fs.writeFileSync('_work/btl_unique_strings.csv',
  'id;text_en;text_de\n' + clean.map((t, i) => (i + 1) + ';' + t.replace(/;/g, '\\;') + ';').join('\n') + '\n', 'utf8');

// write per-file mapping (file;slot;text_en;text_de)
const perFile = [];
for (const l of lines) {
  const parts = l.split(';');
  const file = parts[0], slot = parts[1];
  const text = parts.slice(2).join(';');
  if (clean.includes(text)) {
    perFile.push([file, slot, text.replace(/;/g, '\\;'), ''].join(';'));
  }
}
fs.writeFileSync('_work/strings_eu_btl_translate.csv',
  'file;slot;text_en;text_de\n' + perFile.join('\n') + '\n', 'utf8');

console.log('unique clean strings:', clean.length);
console.log('per-file rows:', perFile.length);
console.log('written: _work/btl_unique_strings.csv, _work/strings_eu_btl_translate.csv');
