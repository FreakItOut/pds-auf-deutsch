// subtitles_patch.js — Tier-2: apply DE translations to the extracted TWN
// files, writing to _work/patched/<NAME>. Validates len(de) <= len(en),
// replaces ALL copies of every translated line, NUL-pads the rest of the
// slot. Keeps file size identical. Reads <NAME>_de.csv.
// Usage: node subtitles_patch.js [NAME...]   (default: all three TWN)
const fs = require('fs');
const outDir = '_work/patched';
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const names = process.argv.slice(2).length ? process.argv.slice(2)
  : ['TWN_CAMP.PRG', 'TWN_RUIN.PRG', 'TWN_SEEK.PRG'];

let totalApplied = 0, totalSkipped = 0, totalErr = 0;
for (const name of names) {
  const csv = '_work/subtitles/' + name.replace(/\./g, '_') + '_de.csv';
  if (!fs.existsSync(csv)) { console.log('no DE file for', name); continue; }
  const buf = Buffer.from(fs.readFileSync('_work/' + name));
  const rows = fs.readFileSync(csv, 'latin1').split(/\r?\n/).filter(Boolean);
  const header = rows[0].split(';');
  const deIdx = header.length - 1;
  let applied = 0, skipped = 0, err = 0;
  for (const r of rows.slice(1)) {
    const p = r.split(';');
    const len = +p[1], first = +p[2], copies = p[3] ? p[3].split('|').map(Number) : [];
    const en = p[4].split('%2C').join(';');
    const de = p[deIdx] || '';
    if (!de) { skipped++; continue; }
    if (de.length > len) {
      console.error('  TOOLONG uid', p[0], 'len', len, 'de.len', de.length);
      err++;
      continue;
    }
    if (de.includes('%') && !en.includes('%')) {
      // warn about suspicious control codes
      console.error('  WARNING uid', p[0], 'de contains % but EN does not');
    }
    if (/[^\x20-\x7e]/.test(de)) {
      console.error('  NON-ASCII uid', p[0]);
      err++;
      continue;
    }
    for (const off of copies) {
      const slot = buf.slice(off, off + len).toString('latin1');
      if (slot !== en) {
        console.error('  MISMATCH at off', off, 'uid', p[0], '— EN text differs, skipping');
        err++;
        continue;
      }
      buf.write(de, off, 'latin1');
      for (let k = off + de.length; k < off + len + 1; k++) buf[k] = 0;
      applied++;
    }
  }
  fs.writeFileSync(outDir + '/' + name, buf);
  const size = fs.statSync('_work/' + name).size;
  const newSize = fs.statSync(outDir + '/' + name).size;
  totalApplied += applied; totalSkipped += skipped; totalErr += err;
  console.log(name.padEnd(14), 'applied', applied, 'skipped(undone)', skipped, 'errors', err,
    'size', size, newSize === size ? 'OK' : 'SIZE-CHANGED !!!');
}
console.log('--- total applied', totalApplied, 'skipped', totalSkipped, 'errors', totalErr);
