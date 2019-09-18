import subprocess
import ast

def cmd(parancs):
    a = subprocess.run(parancs.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("unicode_escape", errors="replace")
    print(a)
    return a

# a = cmd("SCHTASKS /Query /NH /FO CSV")
# a = "[[" + a[:-2].replace("\r\n", "], [").replace('"', '\"') + "]]"
# a = ast.literal_eval(a)
# a = list(filter(lambda x: x[0][:6] == "\\kgerg", a))
# print (a)
parancs = "schtasks /CREATE /SC ONCE /TN kgerg\\Teszt2 /TR \"C:\\Windows\\System32\\notepad.exe\" /ST 20:37"
a = subprocess.run(parancs.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(a)
a = a.stdout.decode("unicode_escape", errors="replace")
print("="*20)
print(a)