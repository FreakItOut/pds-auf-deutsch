# -*- coding: utf-8 -*-
"""Testet den GUI-Worker (nur pruefen) mit Disc 1, ohne Dialoge."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_tools'))
os.chdir(os.path.join(ROOT, '_dist'))

import pds_deutsch_patcher_gui as G  # noqa: E402

DISC = os.path.join(ROOT, 'Original_CD1',
                    'Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin')

root = G.tk.Tk()
app = G.App(root)
app.path_vars[1].set(DISC)
app.check_var.set(True)
app._run_label()
root.after(1200, app._on_run)
root.after(60000, root.destroy)
root.mainloop()
print('gui test done')
