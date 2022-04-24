import math
from math import *


'''отрезки, из которых складывается путь шаров'''
class Segment():
    def __init__(self, start: (int, int), end: (int, int)):
        self.start = start
        self.end = end
        self.angle = atan2(end[1] - start[1], end[0] - start[0])
        self.length = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
