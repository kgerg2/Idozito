import subprocess

# IP közzététele - Google Drive

feladatok = [["powershell", r"((netsh interface ip show address 'Wi-Fi' | where {$_ -match 'IP Address'}) -split ' ')[-1] | Out-File 'C:\Users\kgerg\Google Drive\Automate\ip.txt'"]]

def osszes():
    for f in feladatok:
        subprocess.run(f)