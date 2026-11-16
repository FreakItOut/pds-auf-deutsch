// rosetta_align.js  (v4 – battle-UI tables aligned by shared prefix)
const fs = require('fs');

const isP = ch => (ch >= 0x20 && ch <= 0x7e) || ch === 0x85 || (ch >= 0x8a && ch <= 0x8f) || ch === 0x91 || ch === 0x0a || ch === 0x0d;
const ACCENT = { 0x85: 'Á', 0x8a: 'á', 0x8b: 'é', 0x8c: 'í', 0x8d: 'ó', 0x8e: 'ú', 0x8f: 'ñ', 0x91: '¡' };
function extractRuns(buf, start) {
  const runs = []; let i = start;
  while (i < buf.length) {
    if (isP(buf[i])) {
      const st = i; while (i < buf.length && isP(buf[i])) i++;
      const len = i - st;
      if (len >= 2 && i < buf.length && buf[i] === 0x00) {
        let t = ''; for (let j = st; j < i; j++) t += (buf[j] >= 0x85 && buf[j] <= 0x91 && ACCENT[buf[j]]) ? ACCENT[buf[j]] : String.fromCharCode(buf[j]);
        runs.push(t); i++;
      } else if (len >= 2 && i >= buf.length) {
        let t = ''; for (let j = st; j < i; j++) t += (buf[j] >= 0x85 && buf[j] <= 0x91 && ACCENT[buf[j]]) ? ACCENT[buf[j]] : String.fromCharCode(buf[j]);
        runs.push(t); break;
      } else break;
    } else if (buf[i] === 0x00) i++;
    else break;
  }
  return runs;
}
function csvEsc(s) { return s.replace(/\\/g, '\\\\').replace(/\r/g, '\\r').replace(/\n/g, '\\n').replace(/;/g, '\\;'); }

const eu = fs.readFileSync('_work/BTL_A5.FNT');
const euStart = eu.indexOf('Counterattack');
const euRuns = extractRuns(eu, euStart);
console.log('EU BTL_A5 battle-UI table: start 0x' + euStart.toString(16), 'strings', euRuns.length);

const es = fs.readFileSync('_work/cd1_0.bin');
const esStart = es.indexOf('Contraataque', 0x1d81af);
const esRuns = extractRuns(es, esStart);
console.log('ES battle-UI table: start 0x' + esStart.toString(16), 'strings', esRuns.length);

// Shared prefix: first min count that aligns by position.
// EU and ES share strings 0..13 (14 strings), then diverge.
const sharedN = Math.min(euRuns.length, esRuns.length);
// find the longest prefix where both have the same count of leading strings
// (we know empirically sharedN=14; verify by printing lengths)
// Align by position for the shared prefix (14 strings)
const SHARED = 14;
const rows = [];
for (let k = 0; k < SHARED; k++) rows.push(['SHARED_' + k, csvEsc(euRuns[k]), csvEsc(esRuns[k])].join(';'));
for (let k = SHARED; k < euRuns.length; k++) rows.push(['EUONLY_' + k, csvEsc(euRuns[k]), ''].join(';'));
for (let k = SHARED; k < esRuns.length; k++) rows.push(['ESONLY_' + k, '', csvEsc(esRuns[k])].join(';'));

fs.writeFileSync('_work/rosetta_battle.csv', 'slot;EU_EN;ES_ES\n' + rows.join('\n') + '\n', 'utf8');
console.log('shared pairs:', SHARED, 'EU-only:', euRuns.length - SHARED, 'ES-only:', esRuns.length - SHARED);
console.log('written _work/rosetta_battle.csv (', rows.length, 'rows )');
