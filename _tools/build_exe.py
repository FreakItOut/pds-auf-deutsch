# Baut die eigenstaendige EXE: GUI + Patch-Datei in EIN Programm.
#
#   python build_exe.py
#
# Ausgabe: _dist/PDS_Deutsch_Patcher.exe (onefile, --noconsole).
# Die EXE braucht kein installiertes Python (PyInstaller bundle).
# Eingebettet werden: pds_deutsch_patch.pzp und ANLEITUNG.txt.
# Danach wird ein Selbsttest des EXE ausgefuehrt (Returncode 0 = ok).
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, '_dist')
BUILD = os.path.join(ROOT, '_build')
EXE_NAME = 'PDS_Deutsch_Patcher'


def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    pzp = os.path.join(DIST, 'pds_deutsch_patch.pzp')
    gui = os.path.join(HERE, 'pds_deutsch_patcher_gui.py')
    guide = os.path.join(DIST, 'ANLEITUNG.txt')
    icon = os.path.join(HERE, 'assets', 'pds_logo.ico')
    logo64 = os.path.join(HERE, 'assets', 'pds_logo_64.png')
    for need in (pzp, gui, guide, icon, logo64):
        if not os.path.isfile(need):
            print('FEHLER: fehlt:', need)
            return 2
    try:
        import PyInstaller  # noqa: F401
        have = True
    except ImportError:
        have = False
    # Die .py-Variante im Verteilungsordner aktuell halten
    for src, dst in (
            (os.path.join(HERE, 'pds_deutsch_patcher_gui.py'),
             os.path.join(DIST, 'pds_deutsch_patcher_gui.py')),
            (os.path.join(HERE, 'apply_patch_file.py'),
             os.path.join(DIST, 'pds_deutsch_patcher.py'))):
        if os.path.isfile(src):
            shutil.copyfile(src, dst)
            print('aktualisiert: %s' % os.path.basename(dst))
    if not have:
        print('PyInstaller fehlt - wird installiert ...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                               '--disable-pip-version-check',
                               'pyinstaller'])
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile', '--noconsole', '--clean',
        '--name', EXE_NAME,
        '--workpath', os.path.join(BUILD, 'pyi_work'),
        '--distpath', os.path.join(BUILD, 'pyi_dist'),
        '--specpath', BUILD,
        '--icon', icon,
        '--add-data', pzp + os.pathsep + '.',
        '--add-data', guide + os.pathsep + '.',
        '--add-data', icon + os.pathsep + '.',
        '--add-data', logo64 + os.pathsep + '.',
        gui,
    ]
    print('baue EXE ...')
    subprocess.check_call(cmd)
    built = os.path.join(BUILD, 'pyi_dist', EXE_NAME + '.exe')
    if not os.path.isfile(built):
        print('FEHLER: EXE nicht erzeugt.')
        return 2
    final = os.path.join(DIST, EXE_NAME + '.exe')
    shutil.copyfile(built, final)
    # Selbsttest: Exitcode 0 erwartet (Fenster werden nicht gezeigt).
    print('EXE-Selbsttest ...')
    r = subprocess.run([final, '--selftest'], timeout=120)
    if r.returncode != 0:
        print('FEHLER: EXE-Selbsttest %d.' % r.returncode)
        return 2
    print('EXE-ok: %s' % final)
    print('Groesse: %d Bytes   sha1: %s' % (
        os.path.getsize(final), sha1(final)[:16]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
