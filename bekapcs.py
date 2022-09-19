import time
from utemezo import letrehoz, listaz, torol
import feladatok

utemezett = [nev for nev, _ in listaz()]

if "figyelmezteto" in utemezett:
    print(torol("figyelmezteto"))

ido = tuple(time.localtime(time.time() + 20*60))[3:5] # 20 perc múlva
print(letrehoz("figyelmezteto", "figyelmezteto-tevekenysegfigyelovel", "{:02}:{:02}".format(*ido)))

feladatok.osszes()

# if "szunet" in utemezett:
#     torol("szunet")
# print(letrehoz("szunet", "szunet", kezdes="ONIDLE", kesleltetes=10))
