import tkinter
from idozito_fv import feladatok, visszaszamlalo

ora_ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
hataridok = feladatok()

ablak = tkinter.Tk("Időzítő")

ablak.iconbitmap(ora_ikon)

szoveg = tkinter.Label(ablak, text=hataridok[0][2])
szoveg.pack()

visszaszamlalo(ablak, hataridok[0][1]).pack()

print(hataridok)

ablak.mainloop()
