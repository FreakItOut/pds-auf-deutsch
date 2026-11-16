// Extract all BTL_* files from EU CD1 disc.
const fs = require('fs');
const { execSync } = require('child_process');
const names = fs.readFileSync('_work/strings_eu_btl_files.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean).map(l => l.split(';')[0]);
for (const name of names) {
  if (fs.existsSync('_work/' + name)) { console.log('skip (exists):', name); continue; }
  try {
    execSync('node _tools\\extract_eu_file.js ' + name, { stdio: 'inherit', cwd: process.cwd() });
  } catch (e) {
    console.log('FAILED:', name);
  }
}
console.log('done');
