// extract_story_files.js — Extract key EU CD1 Story files from the EU disc.
const fs = require('fs');
const { execSync } = require('child_process');
const NAMES = [
  'C_DRA6.MCB', 'E128SE.BIN', 'EVT029.CPK', 'BENITATE.MCB',
  'CHARCMP0.MCB', 'EV30_3.PCM', 'AZEL_ABS.TXT',
  'E014.EPK', 'E006.EPK', 'EVT000_1.FNT',
];
for (const n of NAMES) {
  if (fs.existsSync('_work/' + n)) { console.log('skip (exists):', n); continue; }
  try {
    execSync('node _tools\\extract_eu_file.js ' + n, { stdio: 'inherit' });
  } catch (e) { console.log('FAILED:', n); }
}
console.log('done');
