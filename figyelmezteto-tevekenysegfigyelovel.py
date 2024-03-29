from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
import logging
import subprocess
import sys
import random
import time
import tkinter
from tkinter import ttk

import screeninfo

from utemezo import letrehoz, listaz, torol

cim = "Figyelmeztető"
uzenet = """A számítógépet már 50 perce használod folyamatosan.
Kattints ide, hogy alvó állapotba rakd!"""
ora_ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
nyil_ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\nyíl-ikon.png"
tev_adatok = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\tevekenyseg-adatok.csv"
hossz = 5
halaszt_ertekek = ("2 perc", "5 perc", "10 perc", "20 perc", "30 perc", "1 óra", "2 óra")
nircmd = "nircmd.exe"
bef = False

logging.basicConfig(format="%(asctime)s|%(levelname)s|%(filename)s:%(funcName)s(%(lineno)d)|%(message)s",
                    filename="C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\logs.txt", level=logging.WARNING)

max_ism_szam = 10
ism_szam = 0
if len(sys.argv) > 1:
    try:
        ism_szam = int(sys.argv[1])
    except:
        print("Nem egész argumentum")

def keszenlet():
    subprocess.run(f"{nircmd} standby", check=False)

def kepernyo():
    subprocess.run(["cmd", "/c", "powercfg /change standby-timeout-ac 0"], check=True)
    subprocess.run(f"{nircmd} monitor async_off", check=False)

def kikapcs():
    subprocess.run(f"{nircmd} exitwin poweroff", check=False)

def befejez(destroy=True):
    global bef
    bef = True
    try:
        ablak.after_cancel(idolimit_id)
    except:
        pass
    if destroy:
        ablak.destroy()


bef_lehetosegek = [("Képernyő kikapcsolása", kepernyo),
                   ("Készenlét", keszenlet),
                   ("Kikapcsolás", kikapcs)]


def ido_ertelmezo(szoveg):
    szoveg = szoveg.strip()
    if not szoveg:
        return 0
    try:
        return int(szoveg)
    except ValueError:
        pass

    if ":" in szoveg:
        poz = szoveg.index(":")
        if ":" in szoveg[poz+1:]:
            return 60*ido_ertelmezo(szoveg[:poz]) + ido_ertelmezo(szoveg[poz+1:])/60
        else:
            return 60*ido_ertelmezo(szoveg[:poz]) + ido_ertelmezo(szoveg[poz+1:])
    elif "óra" in szoveg:
        szoveg = szoveg.split("óra")
        return 60*int(szoveg[0]) + ido_ertelmezo(szoveg[1])
    elif "ó" in szoveg:
        szoveg = szoveg.split("ó")
        return 60*int(szoveg[0]) + ido_ertelmezo(szoveg[1])
    elif "perc" in szoveg:
        szoveg = szoveg.split("perc")
        return int(szoveg[0]) + ido_ertelmezo(szoveg[1])/60
    elif "p" in szoveg:
        szoveg = szoveg.split("p")
        return int(szoveg[0]) + ido_ertelmezo(szoveg[1])/60

    raise ValueError(f"{szoveg} nem alakítható idővé.")

def halaszt(halaszt_lista):
    global ism_szam
    ido = halaszt_lista.get().lower()
    try:
        ido = ido_ertelmezo(ido)*60 or 30
    except ValueError:
        ido = 30
    try:
        ablak.after_cancel(idolimit_id)
    except:
        pass
    ablak.destroy()

    if ido < 1200:
        ism_szam = min(max_ism_szam, ism_szam + 1)
    else:
        ism_szam = 0

    print(f"halaszt: {ism_szam=}")
    if ido <= 120:
        time.sleep(ido)
    else:
        utemezett = [nev for nev, _ in listaz()]
        if "figyelmezteto" in utemezett:
            torol("figyelmezteto")
        ido = tuple(time.localtime(time.time() + ido))[3:5]
        eredm = letrehoz("figyelmezteto", r"C:\Users\kgerg\Documents\GitHub\Idozito\figyelmezteto-tevekenysegfigyelovel",
                 "{:02}:{:02}".format(*ido), argumentumok=[ism_szam])
        logging.info(eredm)
        befejez(destroy=False)

def ablakmeret_kiszamolasa(min_szel, min_mag, max_szel, max_mag, max_x, max_y, arany):
    szel = min_szel + (max_szel - min_szel) * arany
    mag = min_mag + (max_mag - min_mag) * arany
    x = max_x * (1 - arany)
    y = max_y * (1 - arany)
    return map(round, (szel, mag, x, y))

def szin_kiszamolasa(kezd, bef, arany):
    listava = lambda x: (x // 0x10000, x // 0x100 % 0x100, x % 0x100)
    r, g, b = (round(x + (y - x) * arany) for x, y in zip(listava(kezd), listava(bef)))
    return r * 0x10000 + g * 0x100 + b

def figyelmezteto(monitor: screeninfo.Monitor, ismetles_szam):
    global ablak, halaszt_lista, idolimit_id, ism_szam
    ism_szam = ismetles_szam
    ablak = tkinter.Tk(monitor.name)
    ablak.overrideredirect(True)
    ablak.wm_attributes("-topmost", True)
    kepernyo_szel = ablak.winfo_screenwidth() if monitor.is_primary else monitor.width
    kepernyo_mag = ablak.winfo_screenheight() if monitor.is_primary else monitor.height
    ablak_szel = 380
    ablak_mag = 100
    hely_x = 420
    hely_y = 190
    x = kepernyo_szel - hely_x
    y = kepernyo_mag - hely_y
    print(f"1: {ablak_szel}x{ablak_mag}+{x}+{y} ({monitor})")

    szel, mag, x, y = ablakmeret_kiszamolasa(ablak_szel, ablak_mag, kepernyo_szel, kepernyo_mag, x, y, ism_szam / max_ism_szam)

    x += monitor.x
    y += monitor.y

    print(f"2: {szel}x{mag}+{x}+{y}")
    # ablak.geometry("380x100+880+540")
    # ablak.geometry(f"{ablak_szel}x{ablak_mag}+{kepernyo_szel-hely_x}+{kepernyo_mag-hely_y}")
    ablak.geometry(f"{szel}x{mag}+{x}+{y}")
    ablak.wm_attributes("-alpha", 0.95)

    # hatterszin = round(0xF0F0F0 - (0xF0F0F0 - 0xA21414) * (ism_szam / max_ism_szam))
    hatterszin = szin_kiszamolasa(0xF0F0F0, 0xA21414, ism_szam / max_ism_szam)
    ablak.configure({"background": f"#{hatterszin:x}"})

    cimsor = tkinter.Frame(ablak)
    cimsor.columnconfigure(index=0, minsize=szel - 40)

    cim_szoveg = ttk.Label(cimsor, text=cim, font=(None, 10, 'bold'))
    cim_szoveg.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    nyil_kep = tkinter.PhotoImage(file=nyil_ikon)
    halaszt_lista = ttk.Combobox(ablak, values=tuple(halaszt_ertekek))
    nyil_gomb = tkinter.Button(cimsor, image=nyil_kep, borderwidth=0, command=lambda *_: halaszt(halaszt_lista))
    nyil_gomb.grid(row=0, column=1, sticky="e")

    cimsor.pack(anchor="n", fill="x")

    keszenlet_gomb = ttk.Button(ablak, text="Befejezés", command=befejez)
    keszenlet_gomb.pack(side=tkinter.LEFT, padx=10)

    halaszt_lista.pack(side=tkinter.RIGHT, padx=10)
    halaszt_lista.bind("<Key-Return>", lambda *_: halaszt(halaszt_lista))
    halaszt_lista.bind("<<ComboboxSelected>>", lambda *_: halaszt(halaszt_lista))

    halaszt_szoveg = ttk.Label(ablak, text="Halasztás:")
    halaszt_szoveg.configure({"background": f"#{hatterszin:x}"})
    halaszt_szoveg.pack(side=tkinter.RIGHT)

    if ism_szam != max_ism_szam:
        idolimit_id = ablak.after(10000, lambda *_: halaszt(halaszt_lista))
    if monitor.is_primary:
        ablak.bell()

    ablak.mainloop()

    print(f"figyelmezteto: {ism_szam=}")

    return ism_szam, bef

if __name__ == "__main__":
    while not bef:
        # ThreadPoolExecutor().map(figyelmezteto, screeninfo.get_monitors())
        # processes = [Process(target=figyelmezteto, args=[monitor]) for monitor in screeninfo.get_monitors()]
        # for process in processes:
        #     process.start()

        # for process in processes:
        #     process.join()
        executor = ProcessPoolExecutor()
        ism_szamok, bef_ek = zip(*executor.map(figyelmezteto, *zip(*zip(screeninfo.get_monitors(), repeat(ism_szam)))))
        ism_szam = max(ism_szamok)
        bef = any(bef_ek)
        print(f"main: {ism_szam=}")
        executor.shutdown(wait=True)
    sys.exit()

###################################################################################################
####################################### Tevékenységfigyelő ########################################
###################################################################################################

korabbi_tev = {}
kezd_ido = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 3600))

def tev_beolvas():
    global korabbi_tev, kezd_ido
    with open(tev_adatok, encoding="utf-8") as be:
        l = map(lambda x: tuple(x.split(";")[1:4:2]), be.readlines())
    for kezd_ido, nev in l:
        nev = nev[:-1]
        if nev in korabbi_tev:
            korabbi_tev[nev] += 1
        else:
            korabbi_tev[nev] = 1

def tev_rogzit():
    idok = kezd_ido.get(), bef_ido.get()
    idotartam = int(time.mktime(time.strptime(idok[1], "%Y-%m-%d %H:%M:%S"))) - \
                int(time.mktime(time.strptime(idok[0], "%Y-%m-%d %H:%M:%S")))
    l = [(lambda x: (x[1].get(), x[2].value))(abl.winfo_children()) for abl in tev_lista]

    with open(tev_adatok, "a", encoding="utf-8") as ki:
        for nev, szazalek in l:
            if nev and szazalek:
                ki.write(";".join([*idok, str(idotartam*szazalek//100), nev]))
                ki.write("\n")

    ablak.quit()

def kiegeszit(es):
    if not es.char:
        return
    mezo = es.widget
    szoveg = mezo.get()
    lehets = filter(lambda x: x[0].startswith(szoveg), korabbi_tev.items())
    kieg = max(lehets, default=("",), key=lambda x: x[1])[0]
    if not kieg:
        return
    h = len(szoveg)
    mezo.insert(h, kieg[h:])
    mezo.selection_range(h, len(kieg))
    mezo.icursor(h)

def osszeg_100(index, es):
    ertekek = [tev.winfo_children()[2].value for tev in tev_lista]
    ertekek[index] = 0
    jo_osszeg = int(100 - es.widget.get())
    jel_osszeg = sum(ertekek)

    for i in random.choices(range(len(ertekek)), ertekek, k=abs(jel_osszeg-jo_osszeg)):
        if jel_osszeg > jo_osszeg:
            ertekek[i] -= 1
        elif jel_osszeg < jo_osszeg:
            ertekek[i] += 1

    for tev, ert in zip(tev_lista, ertekek):
        if tev != tev_lista[index]:
            tev.winfo_children()[2].value = ert

def uj_tev(*_):
    global tev_lista

    tev_ablak = tkinter.Frame(ablak)

    megn_szoveg = ttk.Label(tev_ablak, text="Megnevezés:")
    megn_szoveg.pack(side=tkinter.LEFT, padx=10, pady=20)

    megn_mezo = ttk.Entry(tev_ablak)
    megn_mezo.pack(side=tkinter.LEFT, padx=10, pady=20)
    megn_mezo.bind("<FocusIn>", uj_tev)
    megn_mezo.bind("<KeyRelease>", kiegeszit)

    i = len(tev_lista)
    csuszka = ttk.LabeledScale(tev_ablak, to=100)
    csuszka.pack(padx=10)
    csuszka.scale.bind("<ButtonRelease>", lambda x: osszeg_100(i, x))

    if tev_lista:
        tev_lista[-1].winfo_children()[1].unbind("<FocusIn>")
        tev_lista[-1].winfo_children()[0].unbind("<ButtonRelease>")
    tev_lista.append(tev_ablak)
    tev_ablak.pack()

if __name__ == "__main__":
    tev_beolvas()
    ablak = tkinter.Tk("Tevékenységfigyelő")

    tev_lista = []

    ido_ablak = tkinter.Frame(ablak)

    kezd_szoveg = ttk.Label(ido_ablak, text="Kezdő időpont: ")
    kezd_szoveg.grid(row=0, column=0)

    kezd_ido = tkinter.StringVar(value=kezd_ido)
    kezd_bev = ttk.Entry(ido_ablak, textvariable=kezd_ido)
    kezd_bev.grid(row=0, column=1)

    bef_szoveg = ttk.Label(ido_ablak, text="Befejező időpont: ")
    bef_szoveg.grid(row=1, column=0)

    bef_ido = tkinter.StringVar(value=time.strftime("%Y-%m-%d %H:%M:%S"))
    bef_bev = ttk.Entry(ido_ablak, text=bef_ido)
    bef_bev.grid(row=1, column=1)

    ido_ablak.pack()

    uj_tev()

    bef_ablak = tkinter.Frame(ablak)

    bef_gombok = []

    for i, (felirat, fv) in enumerate(bef_lehetosegek):
        bef_gombok.append(ttk.Button(bef_ablak, text=felirat, command=lambda f=fv: tev_rogzit() or f()))
        bef_gombok[i].grid(row=0, column=i, padx=10)

    bef_ablak.pack(side=tkinter.BOTTOM, pady=10)

    ablak.mainloop()
