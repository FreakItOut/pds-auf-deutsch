// Find longest common run of IDENTICAL strings between EU and ES BTL_A5 tables.
const fs = require('fs');
const isP = ch => (ch >= 0x20 && ch <= 0x7e) || ch === 0x85 || (ch >= 0x8a && ch <= 0x8f) || ch === 0x91 || ch === 0x0a || ch === 0x0d;
const ACCENT = { 0x85: 'Á', 0x8a: 'á', 0x8b: 'é', 0x8c: 'í', 0x8d: 'ó', 0x8e: 'ú', 0x8f: 'ñ', 0x91: '¡' };
function extractRuns(buf, start) {
  const runs = []; let i = start;
  while (i < buf.length) {
    if (isP(buf[i])) {
      const st = i; while (i < buf.length && isP(buf[i])) i++;
      const len = i - st;
      if (len >= 2 && i < buf.length && buf[i] === 0x00) { let t=''; for(let j=st;j<i;j++) t += (buf[j]>=0x85&&buf[j]<=0x91&&ACCENT[buf[j]])?ACCENT[buf[j]]:String.fromCharCode(buf[j]); runs.push(t); i++; }
      else if (len >= 2 && i >= buf.length) { let t=''; for(let j=st;j<i;j++) t += (buf[j]>=0x85&&buf[j]<=0x91&&ACCENT[buf[j]])?ACCENT[buf[j]]:String.fromCharCode(buf[j]); runs.push(t); break; }
      else break;
    } else if (buf[i] === 0x00) i++;
    else break;
  }
  return runs;
}
const eu = extractRuns(fs.readFileSync('_work/BTL_A5.FNT'), 0x5f5e4);
const es = extractRuns(fs.readFileSync('_work/cd1_0.bin'), 0x1d81af);
console.log('EU', eu.length, 'ES', es.length);
let bestI=-1,bestJ=-1,bestL=0;
for (let i=0;i<eu.length;i++){
  for(let j=0;j<es.length;j++){
    let L=0;
    while(i+L<eu.length && j+L<es.length && eu[i+L]===es[j+L]) L++;
    if(L>bestL){bestL=L;bestI=i;bestJ=j;}
  }
}
console.log('longest identical run:',bestL,'EU idx',bestI,'ES idx',bestJ);
if (bestL>0){ console.log('EU run starts:', eu.slice(bestI,bestI+bestL).map((t,k)=>bestI+k+':'+t.length).join(' | ')); }
// Print the identical matched strings (short UI labels — safe metadata)
if (bestL>0){ for(let L=0;L<bestL;L++) console.log('  match', bestI+L, JSON.stringify(eu[bestI+L])); }
