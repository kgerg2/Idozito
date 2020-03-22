import os
import re
import time
from tkinter import ttk
import gspread
from oauth2client.service_account import ServiceAccountCredentials

json_fajl = "C:\\Users\\kgerg\\Documents\\Programok\\Idobeosztas\\Idobeosztas-50eecbd4afa8.json"
hataridok_fajl = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\hataridok.txt"
nap_orava_formaz = lambda t: time.strftime('%Y. %m. %d. %H:%M:%S', time.localtime(t))
orava_formaz = lambda t: time.strftime('%H:%M:%S', time.gmtime(t))
tablazat = None

def folamatjelzo(master, ido, bef_fv=None, **kwargs):
    """Vízszintes folamatjelzőt állít be, ami a megadott idő alatt megtelik.

    `master`: a szülő elem\n
    `ido`: a befejezésig eltelő idő (másodperc)\n
    `bef_fv`: az idő letelte után meghívásra kerülő függvény"""

    sav = ttk.Progressbar(master, **kwargs)
    sav.start(10*ido)
    def bef():
        sav.stop()
        sav["value"] = 100
        if bef_fv:
            bef_fv()
    sav.after(1000*ido, bef)
    sav.bind()
    return sav

def visszaszamlalo(master, ido, bef_fv=None):
    """Visszaszámlál a megadott időmennyiséget.

    `master`: a szülő elem\n
    `ido`: a befejezésig eltelő idő (másodperc)\n
    `bef_fv`: az idő letelte után meghívásra kerülő függvény"""

    bef_ido = time.time() + ido
    if ido >= 3600:
        forma = "%H:%M:%S"
    else:
        forma = "%M:%S"

    szoveg = ttk.Label(master, text=time.strftime(forma, time.gmtime(ido)))

    def frissit():
        ido = bef_ido - time.time()
        if ido > 0:
            szoveg["text"] = time.strftime(forma, time.gmtime(ido))
            szoveg.after(30, frissit)
        else:
            szoveg["text"] = ("00:"*3)[:len(forma)]
            if bef_fv:
                bef_fv()

    szoveg.after(30, frissit)
    return szoveg

def letolt():
    """Kapcsolatot létesít a Google-táblázattal.

    A globális `tablazat` változóban tárolja és kiíratja a
    `hataridok_fájl` által meghatározott fájlba."""
    global tablazat

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_fajl, scope)
    client = gspread.authorize(creds)
    tablazat = client.open("Idobeosztas").sheet1

    fajlba_ir()

def befejezetlenek():
    """Megadja a befejezetlen feladatok listáját
    `(<határidő (s)>, <időtartam (s)>, <leírás>)` hármasokkal.

    Amennyiben még nem történt meg, a táblázat eléréséhez meghívja a `letolt` függvényt."""
    if not tablazat:
        letolt()
    return [sor["Snippet"].split(";") for sor in tablazat.get_all_records()
            if sor["Subject"] == "Idozito" and not sor["Finished"]]

def fajlba_ir():
    """A befejezetlen feladatok listáját a `hataridok_fajl` által meghatározozz fájlban rögzíti."""
    with open(hataridok_fajl, "w", encoding="utf-8") as ki:
        ki.writelines([f"{nap_orava_formaz(int(nap))};{orava_formaz(int(ido))};{megn};0\n"
                       for nap, ido, megn in befejezetlenek()])

def befejez(hatarido, feladat):
    """Egy adott feladatot befejezettnek minősít. Ezt rögzíti a Google-táblázatban
    és a `hataridok_fajl` által mutatott fájlban is.

    `hatarido`: az elvégzett feladat határideje (int)\n
    `feladat`: az elvégzett feladat leírása"""
    tal = tablazat.findall(re.compile(f"{hatarido};.*;{feladat}"))
    tal = [(t.row, t.col+1) for t in tal if not tablazat.cell(t.row, t.col+1).numeric_value]

    if not tal:
        raise LookupError("Nem található ilyen rekord.")

    tablazat.update_cell(*tal[0], 1)

    with open(hataridok_fajl, "r", encoding="utf-8") as be:
        with open(f"{hataridok_fajl}.temp", "w", encoding="utf-8") as ki:
            sor = ""
            while sor := be.readline():
                if re.match(f"{nap_orava_formaz(hatarido)};[0-9:]*;{feladat};0", sor):
                    ki.write(f"{sor[:-2]}1\n")
                    break
                else:
                    ki.write(sor)
            ki.write(be.read())

    os.replace(f"{hataridok_fajl}.temp", hataridok_fajl)

def feladatok():
    """A befejezetlen feladatok listája (határidő szerint rendezett).\n
    `(int <határidő (s)>, int <időtartam (s)>, string <leírás>)` hármasokkból áll."""
    return sorted([(int(nap), int(ido), megn) for nap, ido, megn in befejezetlenek()])
