from PyQt5 import QtGui


'''мяч, которым стреляет пользователь'''
class userBall():
    def __init__(self, color: QtGui.QColor, position: (int, int)):
        self.color = color
        self.position = position
        self.radius = 15
        self.moveSpeed = (0, 0)

    def __eq__(self, other):
        return isinstance(other, userBall) and self.color == other.color and self.position == other.position and \
               self.moveSpeed == other.moveSpeed

    def __hash__(self):
        p = 53
        return (hash(self.color.Rgb) * p + hash(self.position)) * p * hash(self.moveSpeed)

    def is_on_screen(self, screen_size: (int, int)):
        return 0 <= self.position[0] <= screen_size[0] and 0 <= self.position[1] <= screen_size[1]


class userBalls():
    def __init__(self, color: QtGui.QColor, screen_size: (int, int)):
        self.moving = list()
        self.static = userBall(color, (screen_size[0] / 2, screen_size[1] / 2))
