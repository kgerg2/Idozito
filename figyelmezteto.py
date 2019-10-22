import time
import subprocess

cim = "Figyelmezteto"
uzenet = """A számítógépet már 50 perce használod folyamatosan.
Kattints ide, hogy alvó állapotba rakd!"""
ikon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
hossz = 5

szkript = f"""[void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
$balloon = New-Object System.Windows.Forms.NotifyIcon -Property @{{
    Icon = "{ikon}"
    BalloonTipTitle = "{cim}"
    BalloonTipText = "{uzenet}"
    Visible = $True
}}
$balloon.ShowBalloonTip(1)
Register-ObjectEvent $balloon BalloonTipClicked -SourceIdentifier event_BalloonTipClicked
Register-ObjectEvent $balloon BalloonTipClosed -SourceIdentifier event_BalloonTipClosed
$retEvent = Wait-Event event_BalloonTip* -TimeOut {hossz}
$retSourceIdentifier = $retEvent.SourceIdentifier
If ($retSourceIdentifier -eq "event_BalloonTipClicked"){{ echo klikk }}
$balloon.Dispose()
"""

while True:
    if subprocess.run(["powershell", szkript], stdout=subprocess.PIPE).stdout.decode("utf-8").strip() == "klikk":
        subprocess.run("C:\\Users\\kgerg\\Documents\\Programok\\nircmd.exe standby")
        break
    time.sleep(5)
