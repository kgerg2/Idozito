import subprocess
from ast import literal_eval
from math import floor, ceil

def futtat(parancs):
    return subprocess.run(parancs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def letrehoz(nev, feladat, ido="", kezdes="ONCE", kesleltetes=0):
    """
    Új feladat létrehozása.
    nev: feladat neve,
    feladat: a futtatandó program neve,
    ido: a futtatás időpontja (óra:perc),
    kezdes: a kezdőesemény,
    kesleltetes: a kezdőesemény és a feladat elindítása között eltelt idő (perc)
    """

    parancs = ["/CREATE"]

    # Név
    parancs += ["/TN", "kgerg\\" + nev]

    # Kezdés
    parancs += ["/SC", kezdes]
    if kezdes == "ONIDLE":
        if kesleltetes > 0:
            kesleltetes = ceil(min(kesleltetes, 999))
            parancs += ["/I", str(kesleltetes)]
    else:
        if kesleltetes > 0:
            perc = floor(min(kesleltetes, 9999))
            mp = ceil((kesleltetes-floor(kesleltetes)) * 60)
            parancs += ["/DELAY", "{:02}:{:02}".format(perc, mp)]

    # Időpont
    if ido:
        parancs += ["/ST", ido]

    # Feladat
    feladat = "cmd /c python C:\\\\Users\\kgerg\\Documents\\GitHub\\Idozito\\" + feladat + ".py"
    parancs += ["/TR", feladat]

    eredmeny = futtat(["schtasks"]+parancs)
    try:
        eredmeny = eredmeny.stdout
        eredmeny = eredmeny.decode("unicode_escape", errors="replace")
    finally:
        if eredmeny[:7] == "SUCCESS":
            return 0
        else:
            return eredmeny

def idove_alakit(szoveg):
    if ":" not in szoveg:
        return None
    return tuple(map(int, szoveg.split(" ")[-1].split(":")))

def listaz():
    """
    Aktuálisan ütemezett feladatok listázása.
    Név, időpont párosokból álló listát ad vissza.
    Az időpont None, ha nem ismert.
    """

    parancs = "SCHTASKS /QUERY /NH /FO CSV".split()
    eredmeny = futtat(parancs)
    eredmeny = r"{}".format(eredmeny.stdout[:-2])[2:-1]
    eredmeny = "[[" + eredmeny.replace("\\r\\n", "], [") + "]]"
    eredmeny = literal_eval(eredmeny)
    eredmeny = filter(lambda x: x[0][:6] == "\\kgerg", eredmeny)
    eredmeny = [(es[0][7:], idove_alakit(es[1])) for es in eredmeny]
    return eredmeny

def torol(nev):
    """
    Adott nevű ütemezett feladat törlése.
    """

    parancs = "SCHTASKS /DELETE /F /TN kgerg\\" + nev
    parancs = parancs.split()
    eredmeny = futtat(parancs)
    try:
        eredmeny = eredmeny.stdout
        eredmeny = eredmeny.decode("unicode_escape", errors="replace")
    finally:
        if eredmeny[:7] == "SUCCESS":
            return 0
        else:
            return eredmeny