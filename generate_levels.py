from game import Game
from math import cos, sin


def frange(start, stop, step):
    count = 0
    cur_num = start
    while cur_num < stop:
        yield cur_num
        cur_num += step


def func(p, k):
    return k[0] * p * cos(p), k[1] * p * sin(p)


def generate_segments(screen_size: tuple, c: tuple):
    res = ""
    for i in frange(0.2, 4 * 3.14, 0.15):
        x, y = func(i, c)
        x = int(x) + screen_size[0] // 2 + 80
        y = int(y) + screen_size[1] // 2

        res = "(" + str(x) + "," + str(y) + ") " + res

        if x > screen_size[0] or y > screen_size[1] or x <= 0 or y <= 0:
            break

    return res + "\n"


with open("level3.txt", 'w') as f:
    f.write("3 \n")
    f.write(generate_segments((1200, 800), (55, 45)))
    f.write("#CC00AA #FF9900 #333399 \n")
    f.write("13")
