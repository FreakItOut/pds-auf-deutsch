// subtitles_template.js — Generate DE translation templates:
// for each <NAME>_en.csv create <NAME>_de.csv with columns
//   uid;len;firstOff;copies;en;de   (de empty — fill this in)
// Also create a progress summary (how many already translated).
const fs = require('fs');
const files = [
  'TWN_CAMP_PRG_en.csv', 'TWN_RUIN_PRG_en.csv', 'TWN_SEEK_PRG_en.csv',
];
for (const f of files) {
  const src = '_work/subtitles/' + f;
  if (!fs.existsSync(src)) { console.log('missing', f); continue; }
  const dst = src.replace('_en.csv', '_de.csv');
  const rows = fs.readFileSync(src, 'latin1').split(/\r?\n/).filter(Boolean);
  const header = rows[0] + ';de';
  const body = rows.slice(1).map(r => r + ';');
  fs.writeFileSync(dst, header + '\r\n' + body.join('\r\n') + '\r\n', 'latin1');
  console.log('template written:', dst, '(' + body.length + ' rows, de empty)');
}
