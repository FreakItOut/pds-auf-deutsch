// translate_btl.js v2 — German translations sized to fit each EN slot
// (len(de) <= len(en)+1), aiming for ZERO truncations.
const fs = require('fs');
const lines = fs.readFileSync('_work/btl_unique_strings.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean);

const T = {
  'AT 1 ': 'AGR1 ',
  'AT 2 ': 'AGR2 ',
  'SP 1 ': 'SPR1 ',
  'SP 2 ': 'SPR2 ',
  'ETC1 ': 'ETC1 ',
  'ETC2 ': 'ETC2 ',
  'ETC3 ': 'ETC3 ',
  'ETC4 ': 'ETC4 ',
  'ETC5 ': 'ETC5 ',
  'ETC6 ': 'ETC6 ',
  'DEAD ': 'TOT  ',
  'no use': 'keine',
  'Counterattack': 'Konterangriff',
  'Display Item List': 'Gegenstandsliste',
  'Display Berserk List': 'Berserkliste',
  'Customize Gun': 'Waffe aendern',
  'Select Dragon Type': 'Dragontyp waehle',
  'Attack with Gun': 'Waffenangriff',
  'Attack with Homing Laser': 'Zielsuchlaser',
  '???': '???',
  'Unusable': 'Nutzlos',
  'You do not have any item.': 'Keinen Gegenstand.',
  'You do not know how to berserk.': 'Keine Berserk-Kenntnis.',
  'You do not have any parts.': 'Du hast keine Teile.',
  'Your Dragon can only move.': 'Drache kann nur laufen.',
  'Not enough Action Gauge.': 'Aktionsleiste leer.',
  'Not enough Berserk Points.': 'Berserk-Punkte leer.',
  'Hit Point at maximum.': 'HP ist voll.',
  'Berserk Point at maximum.': 'BP ist voll.',
  'You have already done so.': 'Das hast du schon getan.',
  'There are no enemies to attack.': 'Keine Gegner zum Angreifen.',
  'NOMAL': 'NORM',
  'Drones': 'Drohne',
  'Reflect Vertical': 'Hoch-Reflexion',
  'Reflect Horizontal': 'Quer-Reflexion',
  'Change Light': 'Lichtwahl',
  'Photon Cannon': 'Photon-Kanone',
  'Photon Blast': 'Photon-Blast',
  "There's no way through that barrier...": 'Kein Weg durch die Barriere...',
  "It's no use! I must retreat.": 'Zwecklos! Rueckzug noetig.',
  'The barrier is down!': 'Barriere ist unten!',
  'Plasma Spider': 'Plasmaspinne',
  'Plasma Fusion %c620%% %c0': 'Plasmafusion %c620%% %c0',
  'Plasma Fusion %c650%% %c0': 'Plasmafusion %c650%% %c0',
  'Plasma Fusion %c690%% %c0': 'Plasmafusion %c690%% %c0',
  'Incandescent Light': 'Gluehendes Licht',
  'Auto Defense System': 'Auto-Verteidigung',
  'Activate Defense System 04': 'Vert.Syst. 04 aktivieren',
  'Activate Defense System 09': 'Vert.Syst. 09 aktivieren',
  'Activate Defense System 13': 'Vert.Syst. 13 aktivieren',
  'Light Particle Laser': 'Lichtpartikellaser',
  'Status Clear': 'Status aus',
  'Purifier 002': 'Reiniger 002',
  'Purifier 001': 'Reiniger 001',
  'Purifier 000': 'Reiniger 000',
  'Lazara': 'Lazara',
  'Intruder Removal System': 'Anti-Eindringling',
  'Laser': 'Laser',
  'Laser Storm': 'Lasersturm',
  'Activate Evasion System': 'Ausweichsystem an',
  'Evasion System Failure': 'Ausweich-Fehler',
  'Scavenger': 'Scavenger',
  'Provocation': 'Provokation',
  'Arangata': 'Arangata',
  'Tornado': 'Tornado',
  'Malfunction': 'Stoerung',
  'Protodrones': 'Protodrone',
  'Reflect': 'Reflekt',
  'Deflect': 'Ablenk',
  'Energy Stream': 'Energiestrahl',
  'Evasion System': 'Ausweichsystem',
  'Evasion Failure': 'Ausweichfehler',
  'Glide Dragon': 'Gleitdrache',
  'Bio Energy': 'Bioenergie',
  'Bio Plasma': 'Bioplasma',
  'Golia Hunter': 'Golia-Jaeger',
  'Light Wave': 'Lichtwelle',
  'Golia Tracker': 'Golia-Radar',
  'P_SPD:%2d.%02d': 'SPD:%2d.%02d',
};

// check fits: strict rule — de (+NUL) must fit into en (+NUL) slot
let fits = 0, too = [];
const out = [];
const nonAscii = [];
for (const l of lines) {
  const p = l.split(';');
  const id = p[0], en = p[1];
  const de = T[en];
  if (de === undefined) { console.error('MISSING TRANSLATION:', JSON.stringify(en)); out.push(id + ';' + en + ';'); continue; }
  if (/[^\x20-\x7e]/.test(de)) nonAscii.push({ en, de });
  if (de.length > en.length) too.push({ en, de, need: en.length, have: de.length });
  else fits++;
  out.push(id + ';' + en + ';' + de);
}
if (nonAscii.length) {
  console.error('NON-ASCII detected (Saturn font likely lacks latin1 umlauts):');
  for (const n of nonAscii) console.error('  ', JSON.stringify(n.en), '->', JSON.stringify(n.de));
  process.exit(1);
}
fs.writeFileSync('_work/btl_unique_strings.csv', 'id;text_en;text_de\n' + out.join('\n') + '\n', 'utf8');

// per-file CSV
const pf = fs.readFileSync('_work/strings_eu_btl_tables.csv', 'latin1').split(/\r?\n/).slice(1).filter(Boolean);
const pfOut = [];
for (const l of pf) {
  const parts = l.split(';');
  const text = parts.slice(2).join(';');
  const de = T[text];
  pfOut.push([parts[0], parts[1], text, de !== undefined ? de : ''].join(';'));
}
fs.writeFileSync('_work/strings_eu_btl_translate.csv',
  'file;slot;text_en;text_de\n' + pfOut.join('\n') + '\n', 'utf8');

console.log('translations applied:', out.length, '| fits:', fits, '| too long:', too.length);
for (const t of too)
  console.log('  TOOLONG:', JSON.stringify(t.en), '->', JSON.stringify(t.de),
    'slot', t.need, 'have', t.have, '(-' + (t.have - t.need) + ')');
console.log('written _work/btl_unique_strings.csv, _work/strings_eu_btl_translate.csv');
