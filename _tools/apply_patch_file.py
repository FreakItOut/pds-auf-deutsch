#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
PANZER DRAGOON SAGA - DEUTSCHE FASSUNG (FAN-UEBERSETZUNG)
Patcher fuer selbsterstellte Abbilder (CUE/BIN) der eigenen Discs.

                      *** NUR PRIVATER GEBRAUCH ***
  Bitte nicht: gepatchte Images weitergeben, hochladen oder verkaufen.
  Du brauchst eine eigene Kopie des Originalspiels (PAL-EU, 4 Discs).

Die Patch-Datei enthaelt nur Offsets, Laengen, CRC-Pruefsummen und die
deutschen Textbytes.  Keine Original-Spieldaten.

Beispiele (Windows-Konsole):
  python pds_deutsch_patcher.py --auto "C:\\Spiele\\PDS"
  python pds_deutsch_patcher.py --auto "C:\\Spiele\\PDS" --check-only
  python pds_deutsch_patcher.py --disc1 "C:\\PDS\\PDS (Disc 1) (Track 1).bin"
  python pds_deutsch_patcher.py --disc1 X --disc2 Y --disc3 Z --disc4 W
  python pds_deutsch_patcher.py --auto . --mode copy --cue --out-dir "..\\Deutsch"
"""
import argparse
import hashlib
import os
import shutil
import struct
import sys
import zlib
from binascii import crc32

MAGIC = b'PDS_DE01'
FMTVER = 1
SUFFIX = ' (Deutsch)'
PATCH_NAME = 'pds_deutsch_patch.pzp'


def out(s):
    so = getattr(sys, 'stdout', None)
    if so:
        so.write(s + '\n')


def err(s):
    se = getattr(sys, 'stderr', None)
    if se:
        se.write(s + '\n')


def find_patch(explicit):
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    cands = []
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        # Eingebauter Patch in der EXE (PyInstaller onefile)
        cands.append(os.path.join(meipass, PATCH_NAME))
    here = os.path.dirname(os.path.abspath(__file__))
    cands.append(os.path.join(here, PATCH_NAME))
    cands.append(os.path.join(os.getcwd(), PATCH_NAME))
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


def load_patch(path):
    raw = open(path, 'rb').read()
    if raw[:8] != MAGIC:
        raise SystemExit('FEHLER: %r ist keine gueltige Patch-Datei.'
                         % path)
    ulen = struct.unpack('<I', raw[8:12])[0]
    payload = zlib.decompress(raw[12:])
    if len(payload) != ulen:
        raise SystemExit('FEHLER: Patch-Datei unvollstaendig (%d von %d '
                         'Bytes).' % (len(payload), ulen))
    if payload[:8] != MAGIC or \
            struct.unpack('<I', payload[8:12])[0] != FMTVER:
        raise SystemExit('FEHLER: falsches Patch-Format.')
    pos = 12
    (ndisc,) = struct.unpack_from('<I', payload, pos)
    pos += 4
    discs = {}
    for _ in range(ndisc):
        disc, size = struct.unpack_from('<IQ', payload, pos)
        pos += 12
        sha_o = payload[pos:pos + 20].hex()
        sha_n = payload[pos + 20:pos + 40].hex()
        pos += 40
        (nh,) = struct.unpack_from('<I', payload, pos)
        pos += 4
        hunks = []
        for _ in range(nh):
            off, ln, c = struct.unpack_from('<QII', payload, pos)
            pos += 16
            hunks.append((off, ln, c))
        (bl,) = struct.unpack_from('<I', payload, pos)
        pos += 4
        blob = payload[pos:pos + bl]
        pos += bl
        data, i = [], 0
        for off, ln, c in hunks:
            data.append(blob[i:i + ln])
            i += ln
        discs[disc] = {'size': size, 'sha_o': sha_o, 'sha_n': sha_n,
                       'hunks': hunks, 'data': data}
    if pos != len(payload):
        raise SystemExit('FEHLER: Patch-Datei hat %d unbenutzte Bytes '
                         'am Ende.' % (len(payload) - pos))
    return discs


def sha1_file(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def disc_names(folder):
    good = []
    for s in os.listdir(folder):
        low = s.lower()
        if not low.endswith(('.bin', '.iso', '.img')):
            continue
        if 'track 1' in low or 'track1' in low:
            good.append(s)
    if not good:
        good = [s for s in os.listdir(folder)
                if s.lower().endswith(('.bin', '.iso', '.img'))]
    return good


def auto_map(folder):
    """Findet die Disc-1..4-Track-1-Dateien im Ordner (Disk-Nr. aus dem
    Dateinamen).  Ohne "Track 1" im Namen wird pro Disc die groesste
    .bin/.iso/.img gewaehlt (die Datenspur ist immer die groesste;
    die kleineren nebenbei sind Musik-Tracks).
    Gibt {disc: pfad} zurueck."""
    got = {}
    cands = [(s, os.path.getsize(os.path.join(folder, s)))
             for s in disc_names(folder)]
    have_track1 = any(('track 1' in s.lower() or 'track1' in s.lower())
                      for s, _ in cands)
    if have_track1:
        cands = [(s, ln) for s, ln in cands
                 if 'track 1' in s.lower() or 'track1' in s.lower()]
    for s, ln in cands:
        low = s.lower()
        for d in (1, 2, 3, 4):
            if ('disc %d' % d) in low or ('disc%d' % d) in low:
                if d not in got:
                    got[d] = os.path.join(folder, s)
                else:
                    cur = os.path.join(folder,
                                       os.path.basename(got[d]))
                    if ln > os.path.getsize(cur):
                        got[d] = os.path.join(folder, s)
                break
    return got


def out_name(binp, suffix):
    stem = os.path.splitext(os.path.basename(binp))[0]
    return stem + suffix + '.bin'


def process(disc, binp, m, args):
    out('--- Disc %d: %s' % (disc, binp))
    if not os.path.isfile(binp):
        err('    FEHLER: Datei nicht gefunden.')
        return False
    if binp.lower().endswith('.cue'):
        err('    FEHLER: Bitte die .BIN (Track 1) angeben, nicht die '
            '.cue.')
        return False
    size = os.path.getsize(binp)
    if size != m['size']:
        err('    FEHLER: Groesse passt nicht: Ist %d Bytes, erwartet %d '
            'Bytes.' % (size, m['size']))
        err('    Verbreiteste Ursachen: kein rohes 2352-Byte-Abbild '
            '(z.B. ISO/2048-Rip) oder ueberhaupt die falsche Disc.')
        return False
    data = bytearray(open(binp, 'rb').read())
    view = memoryview(data)
    sha_o = hashlib.sha1(data).hexdigest()
    if sha_o == m['sha_o']:
        out('    Gesamt-Pruefsumme: OK (erwartetes PAL-EU Original).')
    else:
        out('    Gesamt-Pruefsumme: ABWEICHEND (%s...)' % sha_o[:16])
        if not args.force:
            err('    Abbruch.  Wenn du sicher bist, dass dein Abbild in '
                'Ordnung ist (andere Ripper offen fuehrt manchmal zu')
            err('    einer etwas anderen Gesamtsumme), starte erneut mit '
                '--force: verlaesslich ist dann nur der Block-CRC.')
            return False
    bad = [off for off, ln, c in m['hunks']
           if crc32(view[off:off + ln]) != c]
    if bad:
        err('    FEHLER: %d von %d Textbloecken passen nicht (CRC).'
            % (len(bad), len(m['hunks'])))
        err('    Beispiel-Offsets: %s' % str(bad[:8]))
        err('    GESCHRIEBEN WURDE NICHTS.  Vermutlich gehoert das Abbild '
            'zu einer anderen Revision/Version.')
        return False
    if args.check_only:
        out('    Testlauf: alle %d Textbloecke passen.  Nichts '
            'geaendert.' % len(m['hunks']))
        return True
    for (off, ln, c), new in zip(m['hunks'], m['data']):
        data[off:off + ln] = new
    del view
    if args.mode == 'copy':
        od = args.out_dir or os.path.dirname(binp)
        os.makedirs(od, exist_ok=True)
        outp = os.path.join(od, out_name(binp, args.suffix))
        with open(outp, 'wb') as f:
            f.write(data)
        del data
        out('    neu geschrieben: %s' % outp)
    else:
        outp = binp
        bak = binp + '.original.bak'
        if not os.path.exists(bak):
            os.replace(binp, bak)
            out('    Sicherungsdatei: %s' % os.path.basename(bak))
        elif not args.overwrite_bak:
            err('    FEHLER: %s existiert bereits.  Bitte diese Datei '
                'zuerst loeschen oder umbenennen (oder --overwrite-bak '
                'verwenden, wenn du sicher bist).' %
                os.path.basename(bak))
            return False
        else:
            os.remove(bak)
        with open(binp, 'wb') as f:
            f.write(data)
        del data
    if args.mode == 'copy' and args.cue:
        if not patched_cue(binp, outp, args.suffix, args.out_dir):
            return False
    sha_n = sha1_file(outp)
    if sha_n == m['sha_n']:
        out('    GEPATCHT UND GEPRUEFT: OK   (sha1 %s...)' % sha_n[:16])
        return True
    err('    FEHLER: Nachpruefung fehlgeschlagen.')
    err('       ist:      %s' % sha_n)
    err('       erwartet: %s' % m['sha_n'])
    err('    Bitte diese Datei NICHT benutzen, sie ist defekt.')
    return False


def patched_cue(binp, outp, suffix, outdir=None):
    d = os.path.dirname(binp)
    base = os.path.basename(binp)
    newbase = os.path.basename(outp)
    stem = os.path.splitext(base)[0]
    prefix = stem.replace('(Track 1)', '').strip()
    cuep = os.path.join(d, prefix + '.cue')
    if not os.path.isfile(cuep):
        err('    Keine passende .cue gefunden (%s.cue)' % prefix)
        return False
    text = open(cuep, 'r', encoding='latin1').read()
    if '"%s"' % base not in text:
        err('    .cue nennt die Track-1-Datei anders (erwartet: %s).'
            % base)
        err('    Bitte die .cue von Hand anpassen.')
        return False
    newcue = text.replace('"%s"' % base, '"%s"' % newbase, 1)
    outdir = outdir or d
    outcue = os.path.join(outdir, os.path.splitext(newbase)[0] + '.cue')
    with open(outcue, 'w', encoding='latin1', newline='') as f:
        f.write(newcue)
    out('    .cue geschrieben: %s' % os.path.basename(outcue))
    same_dir = os.path.abspath(outdir) == os.path.abspath(d)
    if not same_dir:
        for line in text.splitlines():
            ls = line.strip()
            if not ls.upper().startswith('FILE'):
                continue
            name = ls.split('"')[1]
            if name.lower() == base.lower():
                continue
            src = os.path.join(d, name)
            dst = os.path.join(outdir, name)
            if os.path.isfile(src) and not os.path.exists(dst):
                shutil.copyfile(src, dst)
                out('    mitkopiert: %s' % name)
    return True


def show_info(discs):
    out('Patch-Datei Inhalt:')
    for d, m in discs.items():
        n = len(m['hunks'])
        tot = sum(l for _, l, _ in m['hunks'])
        out('  Disc %d: %d Regionen, %d veraenderte Bytes, Bildgroesse '
            '%d Bytes' % (d, n, tot, m['size']))


def main():
    ap = argparse.ArgumentParser(
        description='Panzer Dragoon Saga - deutsche Fassung: '
                    'Uebersetzung auf eigene Discs anwenden.')
    ap.add_argument('--patch', help='Pfad zur Patch-Datei '
                    '(%s).  Standard: neben diesem Tool bzw. im '
                    'Arbeitsverzeichnis.' % PATCH_NAME)
    for d in (1, 2, 3, 4):
        ap.add_argument('--disc%d' % d, metavar='TRACK1.BIN',
                        help='Track-1-Abbild deiner Disc %d (BIN, roh '
                        '2352 Bytes/Sektor).' % d)
    ap.add_argument('--auto', metavar='ORDNER',
                    help='Ordner, in dem alle vier Track-1-Dateien '
                    '(Disc-Nr. im Namen) automatisch erkannt werden.')
    ap.add_argument('--check-only', action='store_true',
                    help='Nur pruefen, ohne etwas zu aendern.')
    ap.add_argument('--force', action='store_true',
                    help='Abweichende Gesamt-Pruefsumme des Abbilds '
                    'akzeptieren; geprueft wird dann nur noch pro '
                    'Textblock (CRC).')
    ap.add_argument('--mode', choices=('inplace', 'copy'),
                    default='inplace',
                    help='inplace: Datei direkt ersetzen (Sicherung '
                    '*.original.bak) [Standard].  copy: neue Datei '
                    'schreiben und Original lassen.')
    ap.add_argument('--out-dir', metavar='ORDNER',
                    help='Zielordner fuer --mode copy.')
    ap.add_argument('--suffix', default=SUFFIX,
                    help='Anhang fuer neue Dateinamen bei --mode copy '
                    '(Standard: %r).' % SUFFIX)
    ap.add_argument('--overwrite-bak', action='store_true',
                    help='Vorhandene *.original.bak ersetzen (Vorsicht).')
    ap.add_argument('--cue', action='store_true',
                    help='Nur mit --mode copy: passende .cue erzeugen '
                    'und die Musik-Tracks mitkopieren.')
    ap.add_argument('--info', action='store_true',
                    help='Nur Informationen ueber die Patch-Datei '
                    'anzeigen und beenden.')
    args = ap.parse_args()

    pp = find_patch(args.patch)
    if not pp:
        err('Patch-Datei nicht gefunden: Bitte --patch PFAD angeben, '
            'oder %s in denselben Ordner wie dieses Tool legen.'
            % PATCH_NAME)
        return 2
    out('Patch-Datei: %s' % pp)
    discs = load_patch(pp)
    if args.info:
        show_info(discs)
        return 0
    sel = {}
    if args.auto:
        am = auto_map(args.auto)
        for d, p in am.items():
            if d in discs:
                sel[d] = p
        for d in sorted(am):
            if d not in discs:
                err('Hinweis: %s sieht aus wie Disc %d, es gibt dafuer '
                    'aber keinen Patch.' % (am[d], d))
    for d in (1, 2, 3, 4):
        p = getattr(args, 'disc%d' % d)
        if p:
            sel[d] = p
    if not sel:
        ap.print_help()
        err('')
        err('FEHLENDE ANGABE: Bitte --disc1 .. --disc4 oder --auto '
            '(mit ORDNER) verwenden.')
        return 2
    missing = [d for d in (1, 2, 3, 4) if d not in sel]
    if missing:
        out('Hinweis: verarbeitet werden nur Discs %s. Nicht angegeben '
            'bzw. uebersprungen: Disc %s.'
            % (sorted(sel), sorted(missing)))
    ok, fails = [], []
    for d in sorted(sel):
        (ok if process(d, sel[d], discs[d], args) else fails).append(d)
    out('')
    if args.check_only:
        out('TESTLAUF: %d von %d Disc(s) geprueft, keinerlei '
            'Aenderungen.' % (len(ok), len(sel)))
    else:
        out('ERGEBNIS: %d von %d Disc(s) erfolgreich gepatcht.' % (
            len(ok), len(sel)))
        if fails:
            out('Nicht gepatcht: %s' % fails)
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
