import time
from win10toast import ToastNotifier

toaster = ToastNotifier()

cim = "Figyelmezteto"
uzenet = """A számítógépet már 50 perce használod folyamatosan.
Kattints ide, hogy alvó állapotba rakd!"""
ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
hossz = 5

def keszenlet():
    import subprocess
    subprocess.run("C:\\Users\\kgerg\\Documents\\Programok\\nircmd.exe standby")
    exit()

while True:
    toaster.show_toast(cim, uzenet, icon_path=ikon, duration=5,
                       threaded=False, callback_on_click=keszenlet)
    time.sleep(5*60)
