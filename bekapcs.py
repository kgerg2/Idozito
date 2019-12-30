import time
from utemezo import letrehoz, listaz, torol

utemezett = [nev for nev, _ in listaz()]

if "figyelmezteto" in utemezett:
    print(torol("figyelmezteto"))

ido = tuple(time.localtime(time.time() + 50*60))[3:5] # 50 perc múlva
print(letrehoz("figyelmezteto", "figyelmezteto", "{:02}:{:02}".format(*ido)))


# if "szunet" in utemezett:
#     torol("szunet")
# print(letrehoz("szunet", "szunet", kezdes="ONIDLE", kesleltetes=10))
