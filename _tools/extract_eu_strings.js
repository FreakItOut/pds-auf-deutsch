// extract_eu_strings.js  (v2 – word-filtered)
// For each EU CD1 file: reconstruct NUL-terminated printable string runs,
// keep only runs that contain common English function words (strong text-ish
// evidence) -> master CSV (no game text printed to stdout).
'use strict';
const fs = require('fs');

const TRACK = 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin';
const MIN_LEN = 3;

const fd = fs.openSync(TRACK, 'r');

// ---- FS table ----
const SCAN_FROM = 14 * 2352, SCAN_LEN = 20 * 2352;
const buf = Buffer.alloc(SCAN_LEN);
fs.readSync(fd, buf, 0, SCAN_LEN, SCAN_FROM);
const recs = [];
for (let i = 0; i < SCAN_LEN - 40; i++) {
  if (buf[i] === 0x62 && buf[i + 1] === 0x01 && buf[i + 2] === 0x1d) {
    const nl = buf[i + 14];
    if (nl < 1 || nl > 40) continue;
    const name = buf.slice(i + 15, i + 15 + nl).toString('latin1');
    if (!/^[A-Za-z0-9_\-.]+$/.test(name)) continue;
    let p = i + 15 + nl;
    if (buf[p] !== 0) continue;
    p++;
    buf.readUInt16LE(p); p += 2;
    const pairs = [];
    for (let k = 0; k + 8 <= 40; k += 8) {
      const a = buf.readUInt32LE(p + k), b2 = buf.readUInt32BE(p + k + 4);
      if (a === b2) pairs.push(a); else break;
    }
    if (pairs.length >= 2 && pairs[0] < 600000 && pairs[1] < 470000000) {
      recs.push({ name, lba: pairs[0], size: pairs[1] });
    }
  }
}
const seen = new Set();
const files = recs.filter(r => {
  const k = r.name.toUpperCase();
  if (seen.has(k)) return false;
  seen.add(k); return true;
});

// ---- string words filter set ----
const HITS = [
  'the', 'you', 'and', 'your', 'not', 'have', 'has', 'with', 'this', 'that',
  'item', 'items', 'use', 'no', 'yes', 'all', 'do', 'for', 'from', 'is',
  'it', 'was', 'are', 'will', 'can', 'one', 'new', 'out', 'but', 'if',
  'steel', 'talk', 'battle', 'dragon', 'world', 'save', 'load',
  'attack', 'defend', 'berserk', 'counter', 'gun', 'laser', 'wing',
  'vest', 'part', 'parts', 'level', 'gauge', 'point', 'points', 'weapon',
  'rally', 'moor', 'name', 'press', 'button', 'please', 'wait', 'data',
  'enemy', 'allies', 'heal', 'damage', 'guard', 'stop', 'start', 'free',
  'open', 'close', 'return', 'exit', 'cancel', 'select', 'change', 'menu'
];

const isP = ch =>
  (ch >= 0x20 && ch <= 0x7e) || (ch >= 0x88 && ch <= 0x8f) ||
  ch === 0x0a || ch === 0x0d;
const ACCENT = { 0x88: 'Á', 0x89: 'Ä', 0x8a: 'á', 0x8b: 'é', 0x8c: 'í', 0x8d: 'ó', 0x8e: 'ú', 0x8f: 'ñ' };

function csvEsc(s) {
  return s.replace(/\\/g, '\\\\')
    .replace(/\r/g, '\\r').replace(/\n/g, '\\n').replace(/;/g, '\\;');
}

function hasHit(txt) {
  const low = txt.toLowerCase();
  for (const w of HITS) {
    if (low.includes(w)) {
      // require the hit to be word-bounded
      const re = new RegExp('[^a-z\\u00c0-\\u017f]' + w + '[^a-z\\u00c0-\\u017f]|^' + w + '$|' +
        '^' + w + '[^a-z\\u00c0-\\u017f]|[^a-z\\u00c0-\\u017f]' + w + '$', 'i');
      if (re.test(low) || low === w) return true;
    }
  }
  return false;
}

const CH = Buffer.alloc(2352 * 128);
const master = [];
const stats = [];

for (const r of files) {
  const lbaByte = r.lba * 2352;
  let pos = lbaByte, userDone = 0, sectIdx = 0;
  const parts = [];
  while (userDone < r.size) {
    const n = fs.readSync(fd, CH, 0, CH.length, pos + sectIdx * 2352);
    if (n <= 0) break;
    const nSectors = Math.floor(n / 2352);
    for (let s = 0; s < nSectors && userDone < r.size; s++) {
      const take = Math.min(2048, r.size - userDone);
      parts.push(CH.slice(s * 2352 + 16, s * 2352 + 16 + take));
      userDone += take;
    }
    sectIdx += nSectors;
  }
  if (!parts.length) continue;
  const data = Buffer.concat(parts);
  const N = data.length;
  let i = 0, okCount = 0;
  while (i < N) {
    if (isP(data[i])) {
      const start = i;
      while (i < N && isP(data[i])) i++;
      const len = i - start;
      if (len >= MIN_LEN && i < N && data[i] === 0x00) {
        let txt = '';
        for (let j = start; j < i; j++) {
          const b = data[j];
          txt += (b >= 0x88 && b <= 0x8f) ? ACCENT[b] : String.fromCharCode(b);
        }
        // extra quality: printable ratio (excl. accents) + some letters
        let letters = 0;
        for (const c of txt) if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) letters++;
        if (letters >= 2 && hasHit(txt) && len >= 4) {
          master.push([r.name, r.lba, start, len, csvEsc(txt)].join(';'));
          okCount++;
        }
      }
    } else i++;
  }
  stats.push({ name: r.name, lba: r.lba, size: r.size, ok: okCount });
}

fs.writeFileSync('_work/strings_eu_cd1_master.csv',
  'file;base_lba;off;len;text\n' + master.join('\n') + '\n', 'utf8');
fs.writeFileSync('_work/strings_eu_cd1_files.csv',
  'file;base_lba;size_bytes;text_runs\n' +
  stats.filter(f => f.ok > 0).map(f => [f.name, f.lba, f.size, f.ok].join(';')).join('\n') + '\n', 'utf8');

const withText = stats.filter(f => f.ok > 0);
const total = {};
for (const f of withText) { total[f.name] = f.ok; }
const top = withText.slice().sort((a, b) => b.ok - a.ok).slice(0, 40);
console.log('files parsed:', files.length);
console.log('word-filtered text-runs:', master.length);
console.log('files with matches:', withText.length);
console.log('--- top 40 ---');
for (const f of top) console.log(f.name.padEnd(16), 'lba 0x' + f.lba.toString(16).padStart(6, '0'), 'strings=' + f.ok);
fs.closeSync(fd);
console.log('written: _work/strings_eu_cd1_master.csv, _work/strings_eu_cd1_files.csv');
