import subprocess
import random
import time
import tkinter
from tkinter import ttk

from utemezo import letrehoz, listaz, torol

cim = "Figyelmeztető"
uzenet = """A számítógépet már 50 perce használod folyamatosan.
Kattints ide, hogy alvó állapotba rakd!"""
ora_ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
nyil_ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\nyíl-ikon.png"
hossz = 5
halaszt_ertekek = ("1 perc", "2 perc", "5 perc", "10 perc", "30 perc", "1 óra", "2 óra")
nircmd = "C:\\Users\\kgerg\\Documents\\Programok\\nircmd.exe"


def keszenlet():
    subprocess.run(f"{nircmd} standby", check=False)

def kepernyo():
    subprocess.run(["cmd", "/c", "powercfg /change standby-timeout-ac 0"], check=True)
    subprocess.run(f"{nircmd} monitor async_off", check=False)

def kikapcs():
    subprocess.run(f"{nircmd} exitwin poweroff", check=False)

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

def halaszt(*_):
    ido = halaszt_lista.get().lower()
    try:
        ido = ido_ertelmezo(ido)*60 or 30
    except ValueError:
        ido = 30
    ablak.after_cancel(idolimit_id)
    ablak.destroy()
    if ido <= 120:
        time.sleep(ido)
    else:
        utemezett = [nev for nev, _ in listaz()]
        if "figyelmezteto" in utemezett:
            torol("figyelmezteto")
        ido = tuple(time.localtime(time.time() + ido))[3:5]
        letrehoz("figyelmezteto", "figyelmezteto-tevekenysegfigyelovel", "{:02}:{:02}".format(*ido))
        exit()

def figyelmezteto():
    global ablak, halaszt_lista, idolimit_id
    ablak = tkinter.Tk()
    ablak.overrideredirect(True)
    ablak.wm_attributes("-topmost", True)
    ablak.geometry("380x100+880+540")
    ablak.wm_attributes("-alpha", 0.95)


    cimsor = tkinter.Frame(ablak)
    cimsor.columnconfigure(index=0, minsize=340)

    cim_szoveg = ttk.Label(cimsor, text=cim, font=(None, 10, 'bold'))
    cim_szoveg.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    nyil_kep = tkinter.PhotoImage(file=nyil_ikon)
    nyil_gomb = tkinter.Button(cimsor, image=nyil_kep, borderwidth=0, command=halaszt)
    nyil_gomb.grid(row=0, column=1, sticky="e")

    cimsor.pack(anchor="n", fill="x")


    keszenlet_gomb = ttk.Button(ablak, text="Befejezés", command=exit)
    keszenlet_gomb.pack(side=tkinter.LEFT, padx=10)

    halaszt_lista = ttk.Combobox(ablak, values=tuple(halaszt_ertekek))
    halaszt_lista.pack(side=tkinter.RIGHT, padx=10)
    halaszt_lista.bind("<Key-Return>", halaszt)
    halaszt_lista.bind("<<ComboboxSelected>>", halaszt)

    halaszt_szoveg = ttk.Label(ablak, text="Halasztás:")
    halaszt_szoveg.pack(side=tkinter.RIGHT)


    idolimit_id = ablak.after(10000, halaszt)
    ablak.bell()

    ablak.mainloop()

while True:
    try:
        figyelmezteto()
    except SystemExit:
        break

ablak.after_cancel(idolimit_id)
ablak.destroy()

###################################################################################################
####################################### Tevékenységfigyelő ########################################
###################################################################################################

korabbi_tev = {}
kezd_ido = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 3600))

def tev_beolvas():
    global korabbi_tev, kezd_ido
    with open("tevekenyseg-adatok.csv", encoding="utf-8") as be:
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

    with open("tevekenyseg-adatok.csv", "a", encoding="utf-8") as ki:
        for nev, szazalek in l:
            if nev and szazalek:
                ki.write(";".join([*idok, str(idotartam*szazalek//100), nev]))
                ki.write("\n")

    ablak.quit()

tev_beolvas()

ablak = tkinter.Tk("Tevékenységfigyelő")

tev_lista = []

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
    tev_lista.append(tev_ablak)
    tev_ablak.pack()

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

bef_lehetosegek = [("Képernyő kikapcsolása", kepernyo),
                   ("Készenlét", keszenlet),
                   ("Kikapcsolás", kikapcs)]
bef_gombok = []

for i, (felirat, fv) in enumerate(bef_lehetosegek):
    bef_gombok.append(ttk.Button(bef_ablak, text=felirat, command=lambda f=fv: tev_rogzit() or f()))
    bef_gombok[i].grid(row=0, column=i, padx=10)

# kesz_gomb = ttk.Button(bef_ablak, text="Készenlét", command=lambda: tev_rogzit() or keszenlet())
# kesz_gomb.grid(row=0, column=1, padx=10)

# leall_gomb = ttk.Button(bef_ablak, text="Leállítás", command=lambda: tev_rogzit() or kikapcs())
# leall_gomb.grid(row=0, column=2, padx=10)

bef_ablak.pack(side=tkinter.BOTTOM, pady=10)

ablak.mainloop()
