import time
import subprocess
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


def keszenlet():
    subprocess.run("C:\\Users\\kgerg\\Documents\\Programok\\nircmd.exe standby", check=False)
    exit()

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
    ablak.destroy()
    if ido <= 120:
        time.sleep(ido)
    else:
        utemezett = [nev for nev, _ in listaz()]
        if "figyelmezteto" in utemezett:
            torol("figyelmezteto")
        ido = tuple(time.localtime(time.time() + ido))[3:5]
        letrehoz("figyelmezteto", "figyelmezteto", "{:02}:{:02}".format(*ido))
        exit()

while True:
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


    keszenlet_gomb = ttk.Button(ablak, text="Készenlét", command=keszenlet)
    keszenlet_gomb.pack(side=tkinter.LEFT, padx=10)

    halaszt_lista = ttk.Combobox(ablak, values=tuple(halaszt_ertekek))
    halaszt_lista.pack(side=tkinter.RIGHT, padx=10)
    halaszt_lista.bind("<Key-Return>", halaszt)
    halaszt_lista.bind("<<ComboboxSelected>>", halaszt)

    halaszt_szoveg = ttk.Label(ablak, text="Halasztás:")
    halaszt_szoveg.pack(side=tkinter.RIGHT)


    ablak.after(10000, halaszt)
    ablak.bell()

    ablak.mainloop()
