#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PANZER DRAGOON SAGA - DEUTSCHE FASSUNG (FAN-ÜBERSETZUNG)
Grafische Oberfläche (GUI) für den Patch.

Du brauchst die selbsterstellten Abbilder (BIN/CUE) deiner eigenen
Discs sowie die Patch-Datei pds_deutsch_patch.pzp.

                        *** NUR PRIVATER GEBRAUCH ***
  Bitte keine gepatchten Images weitergeben oder veröffentlichen.

Selbsttest (ohne Fenster):
    python pds_deutsch_patcher_gui.py --selftest
"""
import argparse
import contextlib
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import traceback
import webbrowser

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    from tkinter import font as tkfont
except ImportError:
    print('tkinter ist in dieser Python-Installation nicht vorhanden.')
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    import pds_deutsch_patcher as cli
except ImportError:
    import apply_patch_file as cli  # noqa: F401  (Projektquellbaum)

# --------------------------------------------------------------- Farben
GREEN = '#4ade80'
ORANGE = '#fbbf24'
RED = '#f87171'
BLUE = '#60a5fa'
GRAY = '#8b8b95'

BG = '#111113'          # Fenster
CARD = '#1a1a1e'        # Karten
CARD_HI = '#212127'     # Karten hervorgehoben / Hover
FIELD = '#0c0c0e'       # Eingabefelder / Protokoll
FG = '#ececf1'          # normaler Text
MUT = '#9a9aa4'         # abgeschwaechter Text
BORDER = '#2c2c34'      # 1px-Rahmen
ACC = '#e02424'         # Logo-Rot
ACC_HI = '#ff4d4d'      # Akzent hell
ACC_DARK = '#8f1414'    # Akzent dunkel

TITLE = ('Panzer Dragoon Saga - Deutsche Fassung '
         '(Fan-Übersetzung) von FreakItOut')

FONT = 'Segoe UI'
FONT_DISPLAY = 'Segoe UI'

TAG = 'PDS-Deutsch-Patch'
FROZEN = bool(getattr(sys, 'frozen', False))
EXE_DIR = (os.path.dirname(os.path.abspath(sys.argv[0]))
           if FROZEN else HERE)

PYURLS = [
    'https://www.python.org/ftp/python/3.12.8/'
    'python-3.12.8-amd64.exe',
    'https://www.python.org/ftp/python/3.12.7/'
    'python-3.12.7-amd64.exe',
    'https://www.python.org/ftp/python/3.11.9/'
    'python-3.11.9-amd64.exe',
]

SETTINGS_DIR = os.path.join(
    os.environ.get('LOCALAPPDATA') or os.path.expanduser('~'),
    'PDS_Deutsch_Patcher')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'settings.json')


def load_settings():
    try:
        with open(SETTINGS_FILE, encoding='utf-8') as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def save_settings(d):
    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=2)
    except Exception:
        pass


def enable_dpi():
    """Scharfe Schrift auf Windows (High-DPI)."""
    if sys.platform != 'win32':
        return
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def pick_fonts(root):
    global FONT, FONT_DISPLAY
    try:
        fams = set(tkfont.families(root))
    except Exception:
        return
    for cand in ('Segoe UI Variable Text', 'Segoe UI'):
        if cand in fams:
            FONT = cand
            break
    for cand in ('Segoe UI Variable Display', 'Segoe UI Semibold',
                 'Segoe UI'):
        if cand in fams:
            FONT_DISPLAY = cand
            break


def find_asset(name):
    """Sucht pds_logo.* : EXE-Bundel, EXE-Ordner, Projektquellbaum."""
    cands = []
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        cands.append(os.path.join(meipass, name))
    cands.append(os.path.join(EXE_DIR, name))
    cands.append(os.path.join(HERE, 'assets', name))
    cands.append(os.path.join(HERE, name))
    cands.append(os.path.join(os.path.dirname(HERE), '_dist', name))
    for c in cands:
        try:
            if os.path.isfile(c):
                return c
        except Exception:
            pass
    return None


def setup_style(root):
    """Dunkles Theme im Logo-Stil (Schwarz + Rot)."""
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    style.configure('.', background=BG, foreground=FG,
                    fieldbackground=FIELD)
    style.configure('TFrame', background=BG)
    style.configure('Card.TFrame', background=CARD)
    style.configure('TLabel', background=BG, foreground=FG)
    style.configure('Muted.TLabel', background=BG, foreground=MUT)
    style.configure('Card.TLabel', background=CARD, foreground=FG)
    style.configure('CardMuted.TLabel', background=CARD, foreground=MUT)
    style.configure('Section.TLabel', background=BG, foreground=MUT,
                    font=(FONT, 9, 'bold'))
    style.configure('TButton', background='#26262c', foreground=FG,
                    bordercolor=BORDER, lightcolor='#2e2e35',
                    darkcolor='#1e1e23', padding=(10, 4),
                    focusthickness=0, relief='flat')
    style.map('TButton',
              background=[('active', '#33333b'), ('pressed', '#1e1e23')],
              foreground=[('disabled', '#6a6a72')])
    style.configure('Ghost.TButton', background=CARD, foreground=MUT,
                    bordercolor=CARD, lightcolor=CARD, darkcolor=CARD,
                    padding=(6, 2), relief='flat')
    style.map('Ghost.TButton',
              background=[('active', CARD_HI), ('pressed', CARD)],
              foreground=[('active', FG)])
    style.configure('TEntry', fieldbackground=FIELD, foreground=FG,
                    insertcolor=FG, bordercolor=BORDER,
                    lightcolor=BORDER, darkcolor=BORDER, padding=(6, 4))
    style.configure('TCheckbutton', background=BG, foreground=FG,
                    focuscolor=ACC)
    style.map('TCheckbutton',
              background=[('active', BG)],
              indicatorcolor=[('pressed', ACC), ('selected', ACC),
                              ('!selected', '#3a3a42')])
    style.configure('TRadiobutton', background=BG, foreground=FG,
                    focuscolor=ACC)
    style.map('TRadiobutton',
              background=[('active', BG)],
              indicatorcolor=[('pressed', ACC), ('selected', ACC),
                              ('!selected', '#3a3a42')])
    style.configure('Card.TRadiobutton', background=CARD,
                    foreground=FG)
    style.map('Card.TRadiobutton',
              background=[('active', CARD)],
              indicatorcolor=[('pressed', ACC), ('selected', ACC),
                              ('!selected', '#3a3a42')])
    style.configure('Modern.Horizontal.TProgressbar',
                    troughcolor=FIELD, background=ACC, bordercolor=FIELD,
                    lightcolor=ACC, darkcolor=ACC, thickness=6)
    style.configure('TScrollbar', background='#26262c',
                    troughcolor=FIELD, bordercolor=FIELD,
                    arrowcolor='#8b8b95', relief='flat')
    style.map('TScrollbar', background=[('active', '#35353d')])
    style.configure('TSeparator', background=BORDER)
    root.configure(bg=BG)


class RoundButton(tk.Canvas):
    """Moderner Primär-Button mit abgerundeten Ecken."""

    def __init__(self, parent, text, command, width=240, height=44,
                 radius=10, bg=ACC, hover=ACC_HI, fg='#ffffff',
                 font=None, parent_bg=BG):
        super().__init__(parent, width=width, height=height,
                         bg=parent_bg, highlightthickness=0, bd=0,
                         cursor='hand2')
        self._bw, self._bh, self._br = width, height, radius
        self._bg, self._hover, self._fg = bg, hover, fg
        self._font = font or (FONT, 10, 'bold')
        self._text = text
        self._state = 'normal'
        self._cmd = command
        self._hovering = False
        self._draw()
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<ButtonRelease-1>', self._on_release)

    def _rounded(self, x0, y0, x1, y1, r, **kw):
        pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r,
               x1, y1 - r, x1, y1, x1 - r, y1, x0 + r, y1,
               x0, y1, x0, y1 - r, x0, y0 + r, x0, y0]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self):
        self.delete('all')
        if self._state != 'normal':
            fill = '#2a2a30'
            color = '#6a6a72'
        else:
            fill = self._hover if self._hovering else self._bg
            color = self._fg
        self._rounded(1, 1, self._bw - 1, self._bh - 1, self._br,
                      fill=fill, outline='')
        self.create_text(self._bw / 2, self._bh / 2, text=self._text,
                         fill=color, font=self._font)

    def config(self, **kw):
        if 'text' in kw:
            self._text = kw['text']
        if 'state' in kw:
            self._state = kw['state']
            try:
                self.configure(cursor='hand2' if kw['state'] == 'normal'
                               else 'arrow')
            except Exception:
                pass
        self._draw()

    configure = config

    def _on_enter(self, _e):
        self._hovering = True
        if self._state == 'normal':
            self._draw()

    def _on_leave(self, _e):
        self._hovering = False
        if self._state == 'normal':
            self._draw()

    def _on_release(self, _e):
        if self._state == 'normal' and self._cmd:
            self._cmd()


def probe_python():
    """Sucht ein benutzbares Python (>= 3.8) im System.

    Gibt (pfad-oder-'', beschreibung) zurück.
    """
    for exe in ('python', 'python3', 'py'):
        p = shutil.which(exe)
        if not p:
            continue
        low = p.lower()
        if 'windowsapps' in low:
            continue  # Windows-Store-Strohhalm-Link
        try:
            r = subprocess.run([p, '-V'], capture_output=True,
                               text=True, timeout=8)
        except Exception:
            continue
        ver = (r.stdout.strip() or r.stderr.strip())
        if not ver.startswith('Python '):
            continue
        num = ver.split()[-1]
        parts = num.split('.')
        if len(parts) >= 2:
            try:
                if (int(parts[0]), int(parts[1])) >= (3, 8):
                    return p, 'Python %s (%s)' % (num, p)
            except ValueError:
                pass
    return '', 'kein benötigtes Python (ab 3.8) gefunden'


class QueueWriter:
    """Leitet stdout/stderr des Patchers zeilenweise in die Queue."""

    def __init__(self, q):
        self.q = q
        self._tail = ''

    def write(self, s):
        self._tail += s
        while '\n' in self._tail:
            line, self._tail = self._tail.split('\n', 1)
            self.q.put(line.rstrip('\r'))
        return len(s)

    def flush(self):
        if self._tail:
            self.q.put(self._tail)
            self._tail = ''


EXPECTED_MB = {1: 645, 2: 560, 3: 632, 4: 583}


class App:
    def __init__(self, root):
        self.root = root
        root.title(TITLE)
        root.minsize(980, 690)
        root.geometry('1060x770')
        pick_fonts(root)
        setup_style(root)
        self._set_icon(root)

        self.settings = load_settings()
        self.last_dir = self.settings.get('last_dir') or ''

        self.q = queue.Queue()
        self.patch = {}
        self.patch_source_path = cli.find_patch(None)
        self.patch_path = tk.StringVar(value='')
        self.mode_var = tk.StringVar(
            value=self.settings.get('mode') or 'inplace')
        self.out_dir_var = tk.StringVar(
            value=self.settings.get('out_dir') or '')
        self.cue_var = tk.BooleanVar(value=bool(self.settings.get('cue', True)))
        self.check_var = tk.BooleanVar(value=False)
        self.force_var = tk.BooleanVar(value=False)

        self.path_vars = {}
        self.status_lbls = {}
        self.disc_names = {}
        self.disc_subs = {}
        self.disc_clear = {}
        self.hashes = {}
        self.checking = set()
        self.worker = None
        self.done_count = 0

        display = self.patch_source_path or ''
        if FROZEN and self.patch_source_path:
            display = '%s (eingebaut in der EXE)' % (
                os.path.basename(self.patch_source_path))
        self.patch_path.set(display)

        self._load_patch_silent()
        self._build_ui()
        self._mode_changed()
        self._refresh_patch_info()
        self._probe_async()
        self.root.after(120, self._poll)

        self.root.bind('<F5>', lambda _e: self._check_all_async())
        self.root.bind('<Control-Return>', lambda _e: self._on_run())
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

    # ------------------------------------------------------------ UI
    def _set_icon(self, root):
        ico = find_asset('pds_logo.ico')
        if ico:
            try:
                root.iconbitmap(ico)
            except Exception:
                pass
        try:
            png = find_asset('pds_logo_64.png')
            if png:
                self._logo_img = tk.PhotoImage(file=png)
            else:
                self._logo_img = None
        except Exception:
            self._logo_img = None

    # ---------------------------------------------------------- Header
    def _build_header(self):
        head = tk.Frame(self.root, bg=BG)
        head.pack(fill='x', padx=18, pady=(16, 10))

        if self._logo_img is not None:
            tk.Label(head, image=self._logo_img, bg=BG).pack(
                side='left', padx=(0, 14))

        txt = tk.Frame(head, bg=BG)
        txt.pack(side='left', fill='x', expand=True)
        tk.Label(txt, bg=BG, fg=FG, font=(FONT_DISPLAY, 16, 'bold'),
                 anchor='w', text='Panzer Dragoon Saga'
                 ).pack(anchor='w')
        tk.Label(txt, bg=BG, fg=ACC, font=(FONT, 10, 'bold'), anchor='w',
                 text='Deutsche Fassung · Fan-Übersetzung'
                 ).pack(anchor='w', pady=(0, 2))
        tk.Label(txt, bg=BG, fg=MUT, font=(FONT, 9), anchor='w',
                 text='Patch-Werkzeug von FreakItOut  ·  nur privater '
                      'Gebrauch'
                 ).pack(anchor='w')

        right = tk.Frame(head, bg=BG)
        right.pack(side='right')
        self._pill(right, '4 Discs', ACC).pack(anchor='e')
        self._pill(right, 'PAL-EU · V1.000', MUT).pack(anchor='e',
                                                       pady=(6, 0))

        sep = tk.Frame(self.root, bg=BORDER, height=1)
        sep.pack(fill='x', padx=18)

    def _pill(self, parent, text, color):
        f = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                     highlightthickness=1)
        tk.Label(f, text=text, bg=CARD, fg=color, font=(FONT, 8, 'bold'),
                 padx=10, pady=3).pack()
        return f

    # ----------------------------------------------------------- Body
    def _build_ui(self):
        self._build_header()

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill='x', padx=18, pady=(12, 0))
        body.grid_columnconfigure(0, minsize=590, weight=0)
        body.grid_columnconfigure(1, weight=1)

        left = tk.Frame(body, bg=BG)
        left.grid(row=0, column=0, sticky='nsew')
        self._build_discs(left)

        right = tk.Frame(body, bg=BG)
        right.grid(row=0, column=1, sticky='nsew', padx=(16, 0))
        self._build_options(right)

        self._build_actionbar()
        self._build_sysrow()
        self._build_log()

    # ------------------------------------------------------------ Discs
    def _section(self, parent, text, hint=''):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill='x', pady=(0, 6))
        tk.Label(row, text=text, bg=BG, fg=MUT,
                 font=(FONT, 9, 'bold')).pack(side='left')
        if hint:
            tk.Label(row, text=hint, bg=BG, fg='#6f6f78',
                     font=(FONT, 8)).pack(side='left', padx=(8, 0))

    def _build_discs(self, parent):
        self._section(parent, 'DISC-ABBILDER',
                      'je Disc genau die große (Track 1)-BIN wählen')

        for d in (1, 2, 3, 4):
            card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                            highlightthickness=1)
            card.pack(fill='x', pady=3)

            num = tk.Label(card, text=str(d), bg=CARD, fg='#3a3a42',
                           font=(FONT_DISPLAY, 18, 'bold'), width=3)
            num.pack(side='left', padx=(8, 0))

            mid = tk.Frame(card, bg=CARD)
            mid.pack(side='left', fill='x', expand=True, pady=7)

            name = tk.Label(mid, text='Keine Datei gewählt', bg=CARD,
                            fg=MUT, font=(FONT, 10, 'bold'), anchor='w',
                            width=44)
            name.pack(fill='x')
            self.disc_names[d] = name

            sub = tk.Label(mid, text='Erwartet: ca. %d MB · Track 1'
                           % EXPECTED_MB[d], bg=CARD, fg='#6f6f78',
                           font=(FONT, 8), anchor='w', width=56)
            sub.pack(fill='x', pady=(1, 0))
            self.disc_subs[d] = sub

            st = tk.Label(card, text='● wählen', bg=CARD, fg=GRAY,
                          font=(FONT, 9), width=20, anchor='e')
            st.pack(side='right', padx=(6, 12))
            self.status_lbls[d] = st

            btns = tk.Frame(card, bg=CARD)
            btns.pack(side='right', padx=(0, 8))
            tk.Button(btns, text='Wählen…', bg='#26262c', fg=FG,
                      activebackground='#33333b', activeforeground=FG,
                      relief='flat', bd=0, padx=9, pady=2,
                      font=(FONT, 8), cursor='hand2',
                      command=lambda d=d: self._pick_disc(d)
                      ).pack(side='left')
            x = tk.Button(btns, text='✕', bg=CARD, fg='#5c5c64',
                          activebackground=CARD_HI, activeforeground=FG,
                          relief='flat', bd=0, padx=6, pady=2,
                          font=(FONT, 9), cursor='hand2',
                          state='disabled',
                          command=lambda d=d: self.path_vars[d].set(''))
            x.pack(side='left', padx=(4, 0))
            self.disc_clear[d] = x

            v = tk.StringVar(value='')
            self.path_vars[d] = v
            v.trace_add('write', lambda *_a, d=d: self._path_changed(d))

        tools = tk.Frame(parent, bg=BG)
        tools.pack(fill='x', pady=(8, 0))
        ttk.Button(tools, text='Discs automatisch finden…',
                   command=self._scan_folder).pack(side='left')
        ttk.Button(tools, text='Status prüfen (F5)',
                   command=self._check_all_async).pack(side='left',
                                                       padx=(8, 0))
        ttk.Button(tools, text='Was ist "Track 1"?',
                   command=self._what_is_track1).pack(side='right')

    # ---------------------------------------------------------- Options
    def _build_options(self, parent):
        self._section(parent, 'PATCH-DATEI')

        card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill='x')

        top = tk.Frame(card, bg=CARD)
        top.pack(fill='x', padx=12, pady=(10, 4))
        pv = self.patch_path.get()
        pname = ('pds_deutsch_patch.pzp' if 'eingebaut' in pv
                 else os.path.basename(pv) or 'pds_deutsch_patch.pzp')
        tk.Label(top, text=pname, bg=CARD, fg=FG,
                 font=(FONT, 10, 'bold')).pack(side='left')
        self.patch_badge = tk.Label(top, text='', bg=CARD, fg=MUT,
                                    font=(FONT, 8, 'bold'))
        self.patch_badge.pack(side='right')

        self.patch_status = tk.Label(card, text='', bg=CARD, fg=MUT,
                                     font=(FONT, 8), anchor='w',
                                     justify='left')
        self.patch_status.pack(fill='x', padx=12)

        prow = tk.Frame(card, bg=CARD)
        prow.pack(fill='x', padx=12, pady=(4, 10))
        self.patch_path_lbl = tk.Label(prow, text='', bg=CARD,
                                       fg='#6f6f78', font=(FONT, 8),
                                       anchor='w')
        self.patch_path_lbl.pack(side='left', fill='x', expand=True)
        tk.Button(prow, text='Andere Datei…', bg='#26262c', fg=FG,
                  activebackground='#33333b', activeforeground=FG,
                  relief='flat', bd=0, padx=10, pady=2,
                  font=(FONT, 8), cursor='hand2',
                  command=self._pick_patch).pack(side='left',
                                                 padx=(6, 0))

        self._section(parent, 'MODUS')
        mode = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                        highlightthickness=1)
        mode.pack(fill='x')

        seg = tk.Frame(mode, bg=CARD)
        seg.pack(fill='x', padx=10, pady=(10, 6))
        for val, txt in (('inplace', 'Direkt ersetzen'),
                         ('copy', 'Neue Dateien schreiben')):
            tk.Radiobutton(
                seg, text=txt, variable=self.mode_var, value=val,
                indicatoron=0, bg=CARD, fg=FG, selectcolor=ACC,
                activebackground=CARD_HI, activeforeground=FG,
                relief='flat', bd=0, padx=14, pady=6,
                font=(FONT, 9, 'bold'), cursor='hand2',
                command=self._mode_changed).pack(side='left',
                                                 padx=(0, 4))
        tk.Label(mode, text='Sicherung *.original.bak wird automatisch '
                 'angelegt.', bg=CARD, fg='#6f6f78',
                 font=(FONT, 8), anchor='w').pack(fill='x', padx=12)

        self.copy_box = tk.Frame(mode, bg=CARD)
        self.copy_box.pack(fill='x')

        orow = tk.Frame(self.copy_box, bg=CARD)
        orow.pack(fill='x', padx=12, pady=(8, 4))
        self.out_row = orow
        self.out_lbl = tk.Label(orow, text='Zielordner:', bg=CARD,
                                fg=MUT, font=(FONT, 8))
        self.out_lbl.pack(side='left')
        self.out_entry = tk.Entry(orow, textvariable=self.out_dir_var,
                                  bg=FIELD, fg=FG, insertbackground=FG,
                                  relief='flat', font=(FONT, 8),
                                  highlightthickness=1,
                                  highlightbackground=BORDER,
                                  highlightcolor=ACC_DARK)
        self.out_entry.pack(side='left', fill='x', expand=True,
                            padx=(6, 6), ipady=2)
        self.out_btn = tk.Button(orow, text='…', bg='#26262c', fg=FG,
                                 activebackground='#33333b',
                                 activeforeground=FG, relief='flat', bd=0,
                                 padx=8, pady=2, font=(FONT, 8),
                                 cursor='hand2',
                                 command=self._pick_outdir)
        self.out_btn.pack(side='left')
        self.cue_cb = ttk.Checkbutton(
            self.copy_box, text='Passende .cue schreiben und Musik-Tracks '
            'mitkopieren', variable=self.cue_var)
        self.cue_cb.pack(anchor='w', padx=12, pady=(0, 10))

        self._section(parent, 'OPTIONEN')
        opt = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                       highlightthickness=1)
        opt.pack(fill='x')
        ttk.Checkbutton(opt, text='Nur prüfen (nichts ändern)',
                        variable=self.check_var,
                        command=self._run_label).pack(anchor='w',
                                                      padx=12,
                                                      pady=(8, 2))
        ttk.Checkbutton(opt, text='Abweichende Gesamt-Prüfsumme '
                        'erlauben (--force)',
                        variable=self.force_var).pack(anchor='w',
                                                      padx=12,
                                                      pady=(0, 8))

    # ------------------------------------------------------- Systemzeile
    def _build_sysrow(self):
        row = tk.Frame(self.root, bg=BG)
        row.pack(fill='x', padx=18, pady=(8, 0))
        ttk.Button(row, text='Anleitung öffnen',
                   command=self._open_manual).pack(side='left')
        ttk.Button(row, text='Python prüfen',
                   command=self._probe_async).pack(side='left',
                                                   padx=(6, 0))
        self.py_dl_btn = ttk.Button(
            row, text='Python installieren',
            command=self._py_download)
        self.py_dl_btn.pack(side='left', padx=(6, 0))
        self.sys_status = tk.Label(row, text='Suche Python…', bg=BG,
                                   fg=MUT, font=(FONT, 8), anchor='e',
                                   justify='right', wraplength=520)
        self.sys_status.pack(side='right', fill='x', expand=True,
                             padx=(12, 0))

    # ------------------------------------------------------- Action bar
    def _build_actionbar(self):
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill='x', padx=18, pady=(14, 0))

        self.status_line = tk.Label(bar, text='Bereit.', bg=BG, fg=MUT,
                                    font=(FONT, 9), anchor='w')
        self.status_line.pack(side='left')

        self.run_btn = RoundButton(bar, text='Patch anwenden',
                                   command=self._on_run, width=230,
                                   height=42, parent_bg=BG)
        self.run_btn.pack(side='right')

        prow = tk.Frame(self.root, bg=BG)
        prow.pack(fill='x', padx=18, pady=(8, 0))
        self.pbar = ttk.Progressbar(prow, mode='determinate',
                                    style='Modern.Horizontal.TProgressbar')
        self.pbar.pack(fill='x')

    # -------------------------------------------------------------- Log
    def _build_log(self):
        wrap = tk.Frame(self.root, bg=BG)
        wrap.pack(fill='both', expand=True, padx=18, pady=(12, 14))

        self._section(wrap, 'PROTOKOLL')

        box = tk.Frame(wrap, bg=CARD, highlightbackground=BORDER,
                       highlightthickness=1)
        box.pack(fill='both', expand=True)

        self.txt = tk.Text(box, height=10, wrap='word', bg=FIELD,
                           fg=MUT, insertbackground=FG,
                           font=('Cascadia Mono', 9), borderwidth=0,
                           highlightthickness=0, padx=10, pady=8,
                           selectbackground='#33333b')
        sb = ttk.Scrollbar(box, command=self.txt.yview)
        self.txt.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self.txt.pack(side='left', fill='both', expand=True)

        self.txt.tag_configure('info', foreground=MUT)
        self.txt.tag_configure('ok', foreground=GREEN)
        self.txt.tag_configure('warn', foreground=ORANGE)
        self.txt.tag_configure('err', foreground=RED)
        self.txt.tag_configure('head', foreground=FG,
                               font=('Cascadia Mono', 9, 'bold'))
        self.txt.tag_configure('dim', foreground='#6f6f78')
        self.txt.configure(state='disabled')

        self._log_lines([
            ('head', 'So geht’s'),
            ('dim', '1. BIN/CUE-Abbild deiner eigenen Original-Discs '
                    'bereithalten (roh, 2352 Bytes/Sektor).'),
            ('dim', '2. „Discs automatisch finden…“ oder jede Disc '
                    'einzeln wählen.'),
            ('dim', '3. „Nur prüfen“ ankreuzen und starten (F5 prüft '
                    'nur den Status).'),
            ('dim', '4. Danach „Patch anwenden“ – Sicherung '
                    '*.original.bak wird automatisch angelegt.'),
            ('dim', ''),
            ('dim', 'Anleitung: ANLEITUNG.txt (Button „Anleitung '
                    'öffnen“).'),
        ])

    def _log_lines(self, items):
        self.txt.configure(state='normal')
        for tag, line in items:
            self.txt.insert('end', line + '\n', tag)
        self.txt.configure(state='disabled')
        self.txt.see('end')

    # --------------------------------------------------- System/Python
    def _what_is_track1(self):
        messagebox.showinfo(
            TITLE,
            '„Track 1“ ist die Spieledaten-Datei: die einzige, die '
            'den Spieltext enthält und gepatcht wird.\n\n'
            'Eine CD hat mehrere Dateien (eine pro „Track“):\n'
            ' - (Track 1).bin ..... Spieldaten, GROSS (ca. 550–650 MB)\n'
            ' - (Track 2/3/4).bin . Musik, klein (2–45 MB)\n'
            ' - .cue .............. Trackliste, kein Abbild\n\n'
            'Du wählst also pro Disc nur die große (Track 1)-Datei '
            'aus. Die Musik-Dateien und die .cue müssen trotzdem im '
            'selben Ordner bleiben (für Emulator oder Rohling).\n\n'
            'Tipp: Bei falscher Auswahl hält sofort der Status '
            '„Größe unpassend (erwartet …)“ an.')

    def _open_manual(self):
        cands = []
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            cands.append(os.path.join(meipass, 'ANLEITUNG.txt'))
        cands.append(os.path.join(EXE_DIR, 'ANLEITUNG.txt'))
        cands.append(os.path.join(HERE, 'ANLEITUNG.txt'))
        cands.append(os.path.join(os.getcwd(), 'ANLEITUNG.txt'))
        for c in cands:
            if os.path.isfile(c):
                os.startfile(c)
                return
        messagebox.showinfo(TITLE, 'ANLEITUNG.txt wurde neben der '
                            'EXE nicht gefunden.')

    def _probe_async(self):
        self.sys_status.config(text='Suche Python…', fg=MUT)

        def work():
            p, desc = probe_python()
            if FROZEN:
                mode = ('Laufmodus: EXE mit eingebautem Python '
                        '(kein Python nötig).')
            else:
                mode = 'Laufmodus: Python-Skript.'

            def up():
                if p:
                    self.sys_status.config(
                        text=mode + '  System-Python: ' + desc,
                        fg=GREEN)
                else:
                    self.sys_status.config(
                        text=mode + ' System-Python: nicht gefunden '
                        '(im EXE-Modus egal).',
                        fg=ORANGE)
            self.root.after(0, up)
        threading.Thread(target=work, daemon=True).start()

    def _py_download(self):
        target = os.path.join(
            os.environ.get('TEMP', EXE_DIR), 'pds_python_setup.exe')
        self.py_dl_btn.config(state='disabled')
        self.pbar.config(mode='indeterminate')
        self.pbar.start(20)
        self.log('--- Python-Installer herunterladen')

        def work():
            import urllib.request
            try:
                for url in PYURLS:
                    try:
                        self.log('   hole: %s' % url)
                        with urllib.request.urlopen(url, timeout=45) \
                                as r:
                            total = int(
                                r.headers.get('content-length',
                                              '0') or '0')
                            got = 0
                            with open(target, 'wb') as f:
                                while True:
                                    chunk = r.read(1 << 18)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                                    got += len(chunk)
                        size = os.path.getsize(target)
                        if total and (abs(size - total) > 4096):
                            raise IOError('unvollständig (%d/%d)'
                                          % (size, total))
                        self.log('    fertig: %s (%d Bytes)' % (
                            target, size))
                        self.log('    Installer wird gestartet – im '
                                 'Installer „Add python.exe to PATH“ '
                                 'ankreuzen!')
                        os.startfile(target)
                        return
                    except Exception as exc:
                        self.log('    Adresse fehlgeschlagen: %r'
                                 % (exc,))
                self.log('    Alle Download-Adressen fehlgeschlagen.')
                self.log('    Bitte „python.org öffnen“ verwenden.')
            finally:
                self.root.after(0, self._stop_indeterminate)
        threading.Thread(target=work, daemon=True).start()

    def _stop_indeterminate(self):
        self.pbar.stop()
        self.pbar.config(mode='determinate', value=0)
        self.py_dl_btn.config(state='normal')

    # --------------------------------------------------- Datei/Quellen
    def _load_patch_silent(self):
        p = self.patch_source_path
        if p:
            p = p.strip()
        if not (p and os.path.isfile(p)):
            return False, ''
        try:
            self.patch = cli.load_patch(p)
            return True, ''
        except Exception as exc:
            self.patch = {}
            return False, repr(exc)

    def _refresh_patch_info(self, error=''):
        p = self.patch_path.get()
        if getattr(self, 'patch_path_lbl', None) is not None:
            if 'eingebaut' in p:
                self.patch_path_lbl.config(text='eingebaut in dieser EXE')
            else:
                short = p if len(p) <= 64 else '…' + p[-62:]
                self.patch_path_lbl.config(text=short)
        if error:
            self.patch_status.config(
                text='Patch-Datei unbrauchbar: %s' % error, fg=RED)
            self.patch_badge.config(text='FEHLER', fg=RED)
            return
        if self.patch:
            hunks = sum(len(m['hunks']) for m in self.patch.values())
            self.patch_status.config(
                text='Geladen: %d Discs · %d Regionen · '
                'Größe/SHA1 geprüft' % (len(self.patch), hunks),
                fg=MUT)
            self.patch_badge.config(text='BEREIT', fg=GREEN)
        else:
            self.patch_status.config(
                text='Keine Patch-Datei gewählt – bitte auswählen.',
                fg=RED)
            self.patch_badge.config(text='FEHLT', fg=RED)

    def _pick_patch(self):
        cand = filedialog.askopenfilename(
            title='Patch-Datei pds_deutsch_patch.pzp wählen',
            initialdir=self.last_dir or HERE,
            filetypes=[('Patch-Dateien', '*.pzp'),
                       ('Alle Dateien', '*.*')])
        if not cand:
            return
        self.last_dir = os.path.dirname(cand)
        self._remember()
        self.patch_source_path = cand
        self.patch_path.set(cand)
        ok, err = self._load_patch_silent()
        if not ok:
            self.patch_status.config(
                text='Patch-Datei unbrauchbar: %s' % err, fg=RED)
            self.patch_badge.config(text='FEHLER', fg=RED)
            return
        self._refresh_patch_info()
        self._check_all_async()

    def _pick_disc(self, d):
        cand = filedialog.askopenfilename(
            title='Track-1-BIN der Disc %d wählen' % d,
            initialdir=self.last_dir or HERE,
            filetypes=[('Abbild', '*.bin;*.iso;*.img'),
                       ('Alle Dateien', '*.*')])
        if cand:
            self.last_dir = os.path.dirname(cand)
            self._remember()
            self.path_vars[d].set(cand)

    def _pick_outdir(self):
        cand = filedialog.askdirectory(
            title='Zielordner für die neuen Dateien wählen',
            initialdir=self.last_dir or HERE)
        if cand:
            self.last_dir = cand
            self.out_dir_var.set(cand)
            self._remember()

    def _remember(self):
        self.settings.update({
            'last_dir': self.last_dir,
            'mode': self.mode_var.get(),
            'out_dir': self.out_dir_var.get(),
            'cue': bool(self.cue_var.get()),
        })
        save_settings(self.settings)

    def _scan_folder(self):
        cand = filedialog.askdirectory(
            title='Ordner mit den vier Discs (BINs) wählen',
            initialdir=self.last_dir or HERE)
        if not cand:
            return
        self.last_dir = cand
        self._remember()
        found = cli.auto_map(cand)
        for d, p in sorted(found.items()):
            self.path_vars[d].set(p)
        missing = [d for d in self.path_vars if d not in found]
        if missing:
            self.log('Hinweis: für Disc(s) %s wurde nichts gefunden; '
                     'bitte von Hand wählen.' % sorted(missing))
        for d in found:
            self._check_disc_async(d)
        self.status_line.config(
            text='%d von 4 Discs gefunden.' % len(found), fg=MUT)

    # ------------------------------------------------- Status pro Disc
    def _chip(self, lbl, text, color):
        lbl.config(text='● ' + text, fg=color)

    def _path_changed(self, d):
        self.hashes.pop(d, None)
        self._refresh_disc_row(d)
        self._chip(self.status_lbls[d], 'neue Datei – noch nicht '
                   'geprüft', GRAY)

    def _refresh_disc_row(self, d):
        p = self.path_vars[d].get().strip()
        name = self.disc_names[d]
        sub = self.disc_subs[d]
        if not p:
            name.config(text='Keine Datei gewählt', fg=MUT)
            sub.config(text='Erwartet: ca. %d MB · Track 1'
                       % EXPECTED_MB[d], fg='#6f6f78')
            self.disc_clear[d].config(state='disabled', fg='#5c5c64')
            return
        base = os.path.basename(p)
        if len(base) > 46:
            base = base[:43] + '…'
        name.config(text=base, fg=FG)
        try:
            mb = os.path.getsize(p) / 1_000_000
            folder = os.path.dirname(p)
            if len(folder) > 58:
                folder = '…' + folder[-56:]
            sub.config(text='%.0f MB · %s' % (mb, folder),
                       fg='#6f6f78')
        except Exception:
            sub.config(text=os.path.dirname(p)[:58], fg='#6f6f78')
        self.disc_clear[d].config(state='normal', fg=MUT)

    def _check_disc_async(self, d):
        path = self.path_vars[d].get().strip()
        if not path:
            self._chip(self.status_lbls[d], 'keine Datei', GRAY)
            return
        if d in self.checking:
            return
        self.checking.add(d)
        self._chip(self.status_lbls[d], 'wird geprüft…', BLUE)

        def work():
            try:
                sha = cli.sha1_file(path)
                self.hashes[d] = self._hash(d, path, sha)
            except Exception:
                tb = traceback.format_exc().strip().splitlines()[-1]
                self._set_status(d, 'Fehler: %s' % tb, RED)
            finally:
                self.checking.discard(d)
        threading.Thread(target=work, daemon=True).start()

    def _check_all_async(self):
        for d in self.path_vars:
            self._check_disc_async(d)

    def _hash(self, d, path, sha):
        self.root.after(0, lambda: self._judge_from_sha(d, path, sha))
        return sha

    def _judge_from_sha(self, d, path, sha):
        m = self.patch.get(d)
        if m is None:
            self._set_status(d, 'kein Patch für Disc %d' % d, RED)
            return
        if not os.path.isfile(path) \
                or os.path.getsize(path) != m['size']:
            self._set_status(d, 'Größe unpassend (erwartet %d B)'
                             % m['size'], RED)
            return
        if sha == m['sha_o']:
            self._set_status(d, 'Original-Abbild okay', GREEN)
        elif sha == m['sha_n']:
            self._set_status(d, 'bereits deutsch gepatcht', ORANGE)
        else:
            self._set_status(
                d, 'SHA1 unbekannt (%s…) evtl. anderes '
                'Ausleseprogramm' % sha[:8], RED)

    def _set_status(self, d, text, color):
        self.root.after(0, lambda: self._chip(self.status_lbls[d],
                                              text, color))

    # -------------------------------------------------------------- Log
    def log(self, line):
        self.q.put(line)

    def _poll(self):
        lines = []
        while True:
            try:
                lines.append(self.q.get_nowait())
            except queue.Empty:
                break
            if len(lines) > 500:
                break
        if lines:
            self.txt.configure(state='normal')
            for line in lines:
                self.txt.insert('end', line + '\n', self._tag_for(line))
            self.txt.configure(state='disabled')
            self.txt.see('end')
        self.root.after(120, self._poll)

    @staticmethod
    def _tag_for(line):
        low = line.lower()
        if line.startswith('+++') or 'fehlgeschlagen' in low or \
                'interner fehler' in low or 'error' in low:
            return 'err'
        if 'achtung' in low or 'hinweis' in low or 'übersprungen' in low \
                or 'warn' in low:
            return 'warn'
        if line.startswith('ERGEBNIS') or line.startswith('TESTLAUF') \
                or line.startswith('---'):
            return 'head'
        if 'ok' in low or 'fertig' in low or 'gespeichert' in low:
            return 'ok'
        if line.strip() == '':
            return 'dim'
        return 'info'

    # ------------------------------------------------------------- Start
    def _mode_changed(self):
        copy_mode = self.mode_var.get() == 'copy'
        if copy_mode:
            self.copy_box.pack(fill='x')
        else:
            self.copy_box.pack_forget()
        state = 'normal' if copy_mode else 'disabled'
        self.out_entry.config(state=state)
        self.out_lbl.config(fg=FG if copy_mode else '#5c5c64')
        self.out_btn.config(state=state)
        self.cue_cb.config(state=state)
        self._remember()

    def _run_label(self):
        self.run_btn.config(text='Nur prüfen' if self.check_var.get()
                            else 'Patch anwenden')

    def _on_run(self):
        if self.worker and self.worker.is_alive():
            return
        if not self.patch:
            messagebox.showwarning(
                TITLE, 'Bitte zuerst die Patch-Datei wählen '
                '(pds_deutsch_patch.pzp), die zum Spiel passt.')
            return
        discs, bad = [], []
        for d, v in self.path_vars.items():
            p = v.get().strip()
            if not p:
                continue
            if os.path.isfile(p):
                discs.append(d)
            else:
                bad.append(d)
        if not discs:
            messagebox.showwarning(
                TITLE, 'Bitte mindestens eine Disc-Datei angeben.')
            return
        if bad:
            self.log('Achtung: für Disc(s) %s existiert die Datei '
                     'nicht; sie werden übersprungen.' % sorted(bad))
        if self.check_var.get() or self.mode_var.get() == 'copy':
            self._start(discs)
            return
        if not messagebox.askyesno(
                TITLE,
                'Es werden %d Datei(en) direkt ersetzt!\n'
                'Vorher wird von jeder Disc automatisch eine Kopie als\n'
                '*.original.bak angelegt.\n\nWirklich fortfahren?'
                % len(discs)):
            return
        self._start(discs)

    def _start(self, discs):
        args = argparse.Namespace(
            force=self.force_var.get(),
            check_only=self.check_var.get(),
            mode=self.mode_var.get(),
            out_dir=self.out_dir_var.get().strip() or None,
            suffix=cli.SUFFIX,
            cue=self.cue_var.get() and self.mode_var.get() == 'copy',
            overwrite_bak=False)
        self.run_btn.config(state='disabled')
        self.pbar.config(mode='determinate', maximum=len(discs), value=0)
        self.done_count = 0
        self.status_line.config(
            text='%s läuft …' % ('Prüfung' if args.check_only
                                 else 'Patch'), fg=BLUE)
        for d in discs:
            self.checking.discard(d)
            self._chip(self.status_lbls[d], 'Arbeit läuft…', BLUE)
        w = threading.Thread(target=self._worker, args=(discs, args),
                             daemon=True)
        self.worker = w
        w.start()

    def _worker(self, discs, args):
        writer = QueueWriter(self.q)
        new_hashes = {}
        ok, skip, fail = [], [], []

        def jsha(d, path, sha):
            new_hashes[d] = sha
            self.root.after(0, lambda: self._judge_from_sha(d, path,
                                                            sha))

        def steps():
            self.done_count += 1
            self.root.after(0, lambda: self.pbar.config(
                value=self.done_count))

        with contextlib.redirect_stdout(writer), \
                contextlib.redirect_stderr(writer):
            try:
                for d in sorted(discs):
                    p = self.path_vars[d].get().strip()
                    m = self.patch.get(d)
                    if m is None:
                        self.log('+++ Disc %d übersprungen: zu dieser '
                                 'Disc gibt es keinen Patch.' % d)
                        fail.append(d)
                        steps()
                        continue
                    sha = cli.sha1_file(p)
                    jsha(d, p, sha)
                    if sha == m['sha_n']:
                        self.log('+++ Disc %d ist bereits deutsch '
                                 'gepatcht – übersprungen.' % d)
                        skip.append(d)
                        steps()
                        continue
                    try:
                        res = cli.process(d, p, m, args)
                        (ok if res else fail).append(d)
                        self.root.after(
                            0, lambda d=d: self._set_status(
                                d, 'fertig' if res else 'fehler',
                                GREEN if res else RED))
                    except Exception:
                        self.log('+++ INTERNER FEHLER bei Disc %d:'
                                 % d)
                        for ln in traceback.format_exc().strip(
                                ).splitlines():
                            self.log('    ' + ln)
                        fail.append(d)
                    steps()
                self.log('')
                if args.check_only:
                    self.log('TESTLAUF ENDE: %d von %d Disc(s) in '
                             'Ordnung; nichts wurde verändert.'
                             % (len(ok), len(discs)))
                else:
                    self.log('ERGEBNIS: %d ok, %d übersprungen, %d '
                             'fehlgeschlagen.'
                             % (len(ok), len(skip), len(fail)))
                self.log('Details und Fehlerhilfe stehen in '
                         'ANLEITUNG.txt.')
            finally:
                writer.flush()
                self.root.after(0, self._finished, ok, skip, fail,
                                args.check_only)

    def _finished(self, ok, skip, fail, check_only):
        self.pbar.config(value=self.pbar['maximum'])
        self.run_btn.config(state='normal')
        total = len(ok) + len(skip) + len(fail)
        if check_only:
            self.status_line.config(
                text='Prüfung beendet: %d von %d in Ordnung.'
                % (len(ok), total), fg=MUT)
        else:
            self.status_line.config(
                text='Fertig: %d ok · %d übersprungen · %d fehlerhaft.'
                % (len(ok), len(skip), len(fail)),
                fg=(RED if fail else GREEN))
        if fail:
            body = '\n'.join(
                'Disc %d: %s' % (d, 'ok' if d in ok else
                                 ('übersprungen' if d in skip
                                  else 'fehler'))
                for d in sorted(set(ok + skip + fail)))
            messagebox.showwarning(
                'Achtung: %d Disc(s) nicht verarbeitet' % len(fail),
                'ok=%d   übersprungen=%d   fehlgeschlagen=%d\n\n%s'
                % (len(ok), len(skip), len(fail), body))
        else:
            messagebox.showinfo(
                'Fertig!',
                'Es wurden %d von %d Disc(s) erfolgreich '
                'verarbeitet.\n\nDetails stehen im Protokoll.'
                % (len(ok), len(ok) + len(skip)))
        self._remember()

    def _on_close(self):
        self._remember()
        self.root.destroy()


CLI_FLAGS = ('--check-only', '--disc1', '--disc2', '--disc3',
             '--disc4', '--auto', '--info', '--patch', '--mode',
             '--out-dir', '--force', '--overwrite-bak')


def main():
    if '--selftest' in sys.argv:
        enable_dpi()
        root = tk.Tk()
        root.withdraw()
        app = App(root)
        root.update_idletasks()
        has_patch = bool(cli.find_patch(None))
        manual = os.path.join(getattr(sys, '_MEIPASS', HERE),
                              'ANLEITUNG.txt')
        has_manual = os.path.isfile(manual)
        print('GUI SELFTEST OK  (patch=%s manual=%s discs=%d)' % (
            bool(has_patch), has_manual, len(app.patch)))
        root.destroy()
        if not has_patch:
            return 3
        if not has_manual:
            return 4
        return 0
    if any(a.startswith(f) for a in sys.argv[1:] for f in CLI_FLAGS):
        return cli.main()
    enable_dpi()
    root = tk.Tk()
    App(root)
    root.mainloop()
    return 0


if __name__ == '__main__':
    sys.exit(main())
