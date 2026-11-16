// apply_batch.js — Merge a batch of DE translations into a *_de.csv.
// Batch CSV format: uid;de  (no header) placed in _work/subtitles/<batchfile>.csv
// Validates len(de) <= len(en) and ASCII-only; skips invalid entries and
// prints out a technical report. Never prints the text itself.
// Usage: node apply_batch.js TWN_CAMP_PRG 01
//   reads _work/subtitles/TWN_CAMP_PRG_de_batch01.csv
const fs = require('fs');
const name = process.argv[2];
const batchFile = process.argv[3];
if (!name || !batchFile) {
  console.error('usage: node apply_batch.js <NAME like TWN_CAMP_PRG> <batchNr>');
  process.exit(1);
}
const dePath = '_work/subtitles/' + name + '_de.csv';
const batch = '_work/subtitles/' + name + '_de_batch' + batchFile + '.csv';

const rows = fs.readFileSync(dePath, 'latin1').split(/\r?\n/).filter(Boolean);
const head = rows[0].split(';');
const deIdx = head.length - 1; // header: uid;len;firstOff;copies;en;de
const data = rows.slice(1).map(r => r.split(';'));

const batchRows = fs.readFileSync(batch, 'latin1').split(/\r?\n/).filter(Boolean);
let ok = 0, tooLong = 0, missing = 0, nonAscii = 0, suspicious = 0;
for (const b of batchRows) {
  const p = b.split(';');
  const uid = +p[0], de = p[1] || '';
  const row = data.find(r => +r[0] === uid);
  if (!row) { missing++; continue; }
  const enLen = +row[1], en = row[4].split('%2C').join(';');
  if (de.length > enLen) { console.error('TOOLONG uid', uid, 'slot', enLen, 'de.len', de.length); tooLong++; continue; }
  if (/[^\x20-\x7e]/.test(de)) { console.error('NON-ASCII uid', uid); nonAscii++; continue; }
  if (de && !en && de) { /* probably fine */ }
  if (de.includes('%') && !en.includes('%')) {
    console.error('WARNING suspicious %% in uid', uid, '(kept, may be intentional)');
    suspicious++;
  }
  row[deIdx] = de;
  ok++;
}
fs.writeFileSync(dePath, head.join(';') + '\r\n' + data.map(r => r.join(';')).join('\r\n') + '\r\n', 'latin1');
console.log('batch applied: ok', ok, '| tooLong', tooLong, '| missing', missing,
  '| nonAscii', nonAscii, '| suspicious', suspicious);
const filled = data.filter(r => r[deIdx]).length;
console.log(name + '_de.csv: ' + filled + ' of ' + data.length + ' rows have DE text');
