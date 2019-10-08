from utemezo import listaz, letrehoz, torol

futo_feladatok = listaz()
if "figyelmezteto" in {nev for nev, _ in futo_feladatok}:
    torol("figyelmezteto")