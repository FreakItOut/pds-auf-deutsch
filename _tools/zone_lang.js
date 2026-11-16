// zone_lang.js — Detect language of each subblob zone via hint-word frequency.
// Only counts printed (no text). Zones from _work/subblob_zones.txt.
const fs = require('fs');
const S0 = 235717;
const b = fs.readFileSync('_work/subblob_cd1.bin');
const isP = x => (x >= 0x20 && x <= 0x7e) || (x >= 0x85 && x <= 0x91);
const zonesTxt = fs.readFileSync('_work/subblob_zones.txt', 'latin1').split(/\r?\n/).filter(Boolean)
  .map(l => l.split('</>'));

const HINTS = {
  en: [' the ', ' and ', ' of ', ' to ', ' is ', ' that ', ' you ', ' with ', ' was '],
  fr: [' et ', ' que ', ' des ', ' les ', ' une ', ' avec ', ' dans ', ' est ', ' pas '],
  de: [' und ', ' der ', ' die ', ' das ', ' nicht ', ' ist ', ' mit ', ' auch ', ' wurde '],
  it: [' che ', ' non ', ' del ', ' sono ', ' aveva ', ' con ', ' per ', ' una '],
  es: [' que ', ' con ', ' del ', ' las ', ' por ', ' una ', ' pero ', ' para '],
};

for (const [s0t, s1t, offT] of zonesTxt) {
  const off = +offT, size = 0x40000;
  const w = b.slice(off, off + size);
  const lines = [];
  let i = 0;
  while (i < w.length) {
    if (isP(w[i])) {
      const st = i;
      while (i < w.length && isP(w[i])) i++;
      if (i < w.length && w[i] === 0 && i - st >= 3) {
        let t = '';
        for (let j = st; j < i; j++) t += String.fromCharCode(w[j]);
        const low = t.toLowerCase();
        lines.push(' ' + low.replace(/[^a-zà-ÿ]/g, ' ').replace(/\s+/g, ' ') + ' ');
      }
    } else i++;
  }
  const counts = {};
  for (const lang of Object.keys(HINTS)) {
    for (const hh of HINTS[lang]) {
      counts[lang] = (counts[lang] || 0) + lines.reduce((a, t) => a + (t.includes(hh) ? 1 : 0), 0);
    }
  }
  const total = Object.values(counts).reduce((a, c) => a + c, 0);
  console.log('zone sec ' + s0t + '..' + s1t + ' lines ' + lines.length, 'hint scores:',
    Object.entries(counts).sort((a, c) => c[1] - a[1]).map(e => e[0] + ':' + e[1]).join(' '),
    'total-hits/lines ratio:', (total / lines.length).toFixed(2));
}
