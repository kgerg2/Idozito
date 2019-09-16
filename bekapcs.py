import subprocess
import json
import ast

a = subprocess.run("SCHTASKS /Query /NH /FO CSV".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("unicode_escape", errors="replace")
a = "[[" + a[:-2].replace("\r\n", "], [").replace('"', '\"') + "]]"
a = ast.literal_eval(a)
a = list(filter(lambda x: x[0][:6] == "\\kgerg", a))
print (a)