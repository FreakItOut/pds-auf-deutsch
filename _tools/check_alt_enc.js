// Check a few extracts for plain-text markers of alternative encodings.
const fs = require('fs');
const files = [
  '_work/CAMPSCR4.PNB',
  '_work/CARASCR2.PNB',
  '_work/BTL_A5.FNT',
  '_work/AZEL_ABS.TXT'
];
for (const f of files) {
  if (!fs.existsSync(f)) { console.log(f, '-- missing'); continue; }
  const b = fs.readFileSync(f);
  const counts = {};
  for (const w of ['you', 'You', 'the ', 'THE ', ' Europe', 'Item', 'item ']) {
    let i = 0, c = 0;
    while ((i = b.indexOf(w, i)) !== -1) { c++; i++; }
    counts[w] = c;
  }
  const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x88 && ch <= 0x8f);
  let runs4 = 0, longestA = 0, cur = 0;
  for (const x of b) { if (isP(x)) { cur++; if (cur > longestA) longestA = cur; } else cur = 0; }
  console.log('==', f, 'len', b.length, 'longest printable run', longestA, JSON.stringify(counts));
}
