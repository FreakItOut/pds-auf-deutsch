// subtitles_export.js — Export unique EN dialogue lines (with all copy offsets)
// per TWN file to _work/subtitles/<NAME>_en.csv. Columns:
//   uid;len;firstOff;copies;en
// TEXT lives in the CSV only — never printed to console.
const fs = require('fs');
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);

function collect(name) {
  const b = fs.readFileSync('_work/' + name);
  const lines = [];
  let i = 0;
  while (i < b.length) {
    if (isP(b[i])) {
      const st = i;
      while (i < b.length && isP(b[i])) i++;
      if (i < b.length && b[i] === 0 && i - st >= 3) lines.push({ st, len: i - st });
    } else i++;
  }
  // dialogue filter
  const dial = [];
  for (const l of lines) {
    let letters = 0, lower = 0, other = 0;
    for (let k = l.st; k < l.st + l.len; k++) {
      const x = b[k];
      if (x >= 0x41 && x <= 0x7a) { letters++; if (x >= 0x61) lower++; }
      else if (x !== 0x20 && x !== 0x2e && x !== 0x2c && x !== 0x27) other++;
    }
    if (l.len >= 11 && letters >= 6 && lower >= 2 && other <= l.len * 0.3) dial.push(l);
  }
  // unique grouping: escape ; and newline in the CSV value
  const esc = s => s.replace(/;/g, '%2C').replace(/%2C/g, '%252C') // simple: ; -> %2C ; % -> %25 first
  const esc2 = s => s.split(';').join('%2C');
  const map = new Map();
  for (const l of dial) {
    const s = b.slice(l.st, l.st + l.len).toString('latin1');
    const u = map.get(s) || { len: l.len, copies: [], first: l.st };
    u.copies.push(l.st);
    map.set(s, u);
  }
  const out = [];
  let uid = 0;
  for (const [s, u] of map) {
    out.push({ uid: uid++, len: u.len, first: u.first, copies: u.copies, en: s });
  }
  out.sort((a, b) => a.first - b.first);
  const dir = '_work/subtitles';
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const csv = out.map(o =>
    [o.uid, o.len, o.first, o.copies.join('|'), o.en.split(';').join('%2C')].join(';')).join('\r\n');
  fs.writeFileSync(dir + '/' + name.replace(/\./g, '_') + '_en.csv', csv, 'latin1');
  console.log(name + ': copies', dial.length, 'unique', out.length,
    '-> _work/subtitles/' + name.replace(/\./g, '_') + '_en.csv');
}
for (const n of ['TWN_CAMP.PRG', 'TWN_RUIN.PRG', 'TWN_SEEK.PRG']) collect(n);
