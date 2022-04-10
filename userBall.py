from PyQt5 import QtGui


class userBall():
    def __init__(self, color: QtGui.QColor, position: (int, int)):
        self.color = color
        self.position = position
        self.radius = 15
        self.moveSpeed = (0, 0)

    def __eq__(self, other):
        return True


class userBalls():
    def __init__(self, color: QtGui.QColor):
        self.moving = list()
        self.static = userBall(color, (200, 200))
