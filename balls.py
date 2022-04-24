from PyQt5 import QtGui


'''шарики, которые нужно уничтожить'''
class Ball():
    def __init__(self, color: QtGui.QColor, position: (int, int), segment_number=0):
        self.color = color
        self.position = position
        self.segment_number = segment_number
        self.radius = 15
