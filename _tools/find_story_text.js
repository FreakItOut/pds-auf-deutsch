// find_story_text.js — check whether EU story files contain real English sentences
// in plaintext (space-separated words). Print only stats/counts, no game text.
const fs = require('fs');

const isP = ch => (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x85 && ch <= 0x91);

function census(name) {
  const p = '_work/' + name;
  if (!fs.existsSync(p)) { console.log(name, 'NOT EXTRACTED'); return null; }
  const b = fs.readFileSync(p);

  // collect NUL-terminated printable runs
  const runs = [];
  let i = 0;
  while (i < b.length) {
    if (isP(b[i])) {
      const st = i;
      while (i < b.length && isP(b[i])) i++;
      const len = i - st;
      if (len >= 6 && i < b.length && b[i] === 0) runs.push({ off: st, len });
      i++;
    } else i++;
  }

  // count runs that look like sentences (contain a space AND 3+ lowercase letters)
  const sent = [], junk = [];
  for (const r of runs) {
    let text = '';
    for (let j = r.off; j < r.off + r.len; j++) text += String.fromCharCode(b[j]);
    const spaces = (text.match(/ /g) || []).length;
    const lower = (text.match(/[a-z]{2,}/g) || []).length;
    if (spaces >= 2 && lower >= 3) sent.push({ off: r.off, len: r.len, spaces });
    else junk.push(r.off);
  }
  console.log('===', name, 'len', b.length);
  console.log('  runs>=6:', runs.length, '| sentence-like:', sent.length, '| junk:', junk.length);
  if (sent.length) {
    const first = sent.slice(0, 500);
    // Cluster: are sentence runs contiguous (a blob) or scattered?
    let clusters = [], cs = sent[0].off, ce = cs;
    for (let k = 1; k < sent.length; k++) {
      if (sent[k].off - ce < 0x4000) ce = sent[k].off;
      else { clusters.push([cs, ce]); cs = sent[k].off; ce = cs; }
    }
    clusters.push([cs, ce]);
    console.log('  sentence-run clusters:', clusters.length);
    clusters.slice(0, 15).forEach(c =>
      console.log('    0x' + c[0].toString(16) + ' .. 0x' + c[1].toString(16),
        '(+len ' + (c[1] - c[0]) + ')'));
    console.log('  first sentence offsets lens:',
      first.slice(0, 10).map(x => '0x' + x.off.toString(16) + ':' + x.len).join(' '));
  }
  return { sent, junk, total: b.length };
}

for (const n of ['EVT000_1.FNT', 'E011.EPK', 'E014.EPK', 'E006.EPK', 'EVT029.CPK', 'CAMPSCR0.PNB', 'CARASCR4.SCB', 'E128SE.BIN']) census(n);
