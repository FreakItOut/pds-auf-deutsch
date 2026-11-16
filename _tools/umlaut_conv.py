# -*- coding: utf-8 -*-
"""Gemeinsamer ae/oe/ue/ss -> Font-Slot-Konverter."""
import re

UE_EXCEPT = {
    'bauer', 'bauern', 'bauernhof', 'feuer', 'feuern', 'feuerholz',
    'feuerkraft', 'feuerbereit', 'feuernd', 'waechterfeuer',
    'waechterfeuers', 'saettigungsfeuer', 'zufallsfeuer',
    'steuer', 'steuern', 'steuerst', 'steuert', 'steuerkreuz',
    'teuer', 'teure', 'teurer', 'teures', 'teuren',
    'treu', 'treue', 'treuen', 'treuer', 'treues',
    'neu', 'neue', 'neuen', 'neuer', 'neues', 'neuem', 'neueste',
    'neuerdings', 'abenteuer', 'abenteuern', 'abenteuerlich',
    'schauen', 'nachschauen', 'schauer', 'sauer', 'sauerei',
    'trauen', 'traue', 'vertrauen', 'vertraue', 'trauern',
    'statue', 'statuen', 'queen', 'quelle', 'quellen', 'queren',
    'bequem', 'durchqueren', 'konsequenzen', 'lichtquelle',
    'kraftquelle', 'angeheuerter', 'euer', 'greuel', 'steuere',
    'steuerst', 'tue', 'tuest', 'blue', 'clue',
    'eventuell', 'aktuell', 'manuell', 'sexuell', 'intellektuell',
    'punktuell', 'konzeptuell', 'visuell', 'graduell', 'individuell',
    'duell', 'duelle', 'duellen', 'duells', 'true', 'guest', 'guess',
}
AE_EXCEPT = {'michael', 'rafael', 'israel', 'paet', 'paets', "paet's",
             'jael', 'aaron', 'aerobic', 'mael', 'cael', 'caesar',
             'maestro', 'aerosol'}
OE_EXCEPT = {'soeben', 'poesie'}
SS_SET = {
    'gross', 'grosse', 'grosser', 'grosses', 'grossen', 'grossem',
    'groesser', 'groessere', 'groesserer', 'groesseres', 'groesseren',
    'groesserem', 'groesste', 'groessten', 'groesster', 'groesse',
    'grossteil', 'grossartig', 'weiss', 'weisse', 'weisser', 'weisses',
    'weissen', 'weisst', 'weissglut', 'heiss', 'heisse', 'heisser',
    'heisses', 'heissen', 'heisst', 'fuss', 'fuesse', 'fuessen',
    'draussen', 'strasse', 'strassen', 'spass', 'schliessen',
    'schliesse', 'schliesst', 'schliesslich', 'schiessen', 'schiesse',
    'schiesst', 'schiess', 'fliessen', 'fliesse', 'fliesst',
    'fliessendem', 'giessen', 'giesse', 'giesst', 'geniessen',
    'geniesse', 'geniesst', 'beissen', 'beisse', 'beisst', 'reissen',
    'reisse', 'reisst', 'zerreisse', 'zerreissen', 'liess', 'liessen',
    'verliess', 'verliessen', 'entliessen', 'verliessest', 'suess',
    'suesse', 'suesser', 'suesses', 'suessen', 'bloss', 'aussen',
    'ausser', 'ausserhalb', 'aussergewoehnlich', 'aussenwelt',
    'aussenstehende', 'aussenstehenden', 'aussenstehender',
    'aussenst', 'erfahrungsgemaess', 'gemaess', 'gewaesser',
}
WORD_RE = re.compile(r"[A-Za-z]+")
UPPER_SLOT = {'^': '`', '|': '[', '~': ']'}


def convert_word(w):
    if w.isupper():
        return w
    low = w.lower()
    if 'statu' in low:
        return w
    chars = list(w)
    for a, b, rep in (('a', 'e', '^'), ('o', 'e', '|'), ('u', 'e', '~')):
        i = 0
        while i < len(chars) - 1:
            if chars[i].lower() == a and chars[i + 1].lower() == b:
                if i == 0 and chars[0].isupper():
                    if a == 'a' and low in AE_EXCEPT:
                        i += 1
                        continue
                    if a == 'o' and low in OE_EXCEPT:
                        i += 1
                        continue
                    if a == 'u' and low in UE_EXCEPT:
                        i += 1
                        continue
                    chars[i] = UPPER_SLOT[rep]
                    del chars[i + 1]
                    continue
                if a == 'u':
                    if low in UE_EXCEPT:
                        i += 1
                        continue
                    if i > 0 and chars[i - 1].lower() in 'aeiouq':
                        i += 1
                        continue
                if a == 'a' and low in AE_EXCEPT:
                    i += 1
                    continue
                if a == 'o' and low in OE_EXCEPT:
                    i += 1
                    continue
                chars[i] = rep
                del chars[i + 1]
            else:
                i += 1
    out = ''.join(chars)
    if low in SS_SET:
        out = out.replace('ss', '{').replace('SS', '{')
    return out


def convert_text(t):
    return WORD_RE.sub(lambda m: convert_word(m.group(0)), t)
