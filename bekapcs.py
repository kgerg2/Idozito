from utemezo import *
import time

ido = tuple(time.localtime(time.time() + 50*60))[3:5] # 50 perc múlva
letrehoz("figyelmezteto", "figyelmezteto", "{}:{}".format(*ido))

letrehoz("szunet", "szunet", kezdes="ONIDLE", kesleltetes="10")

