import subprocess
from math import floor, ceil

def letrehoz(nev, feladat, ido="", kezdes="ONCE", kesleltetes=0):
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
            parancs += ["/DELAY", "{}:{}".format(perc, mp)]

    # Időpont
    if ido:
        parancs += ["/ST", ido]

    # Feladat
    feladat = "python C:\\\\Users\\kgerg\\Documents\\GitHub\\Idozito\\" + feladat + ".py"
    parancs += ["/TR", feladat]

    eredmeny = subprocess.run(["schtasks"]+parancs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        eredmeny = eredmeny.stdout
        eredmeny = eredmeny.decode("unicode_escape", errors="replace")
    finally:
        if eredmeny[:7] == "SUCCESS":
            return 0
        else:
            return eredmeny
