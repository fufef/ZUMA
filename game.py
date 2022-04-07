from PyQt5 import QtWidgets, QtCore, QtGui
from level import Level


class Game(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        # self.resize(800,800)
        self.main_window = main_window

        self.backMenu_btn = QtWidgets.QPushButton(self)
        self.backMenu_btn.setGeometry(QtCore.QRect(50, 50, 50, 50))
        self.backMenu_btn.setObjectName("backMenu_btn")
        self.backMenu_btn.clicked.connect(lambda: main_window.change_window(0))

        self.level = Level.parse("level1.txt")
        self.counter = 0

        self.setObjectName("GameWindow")
        self.setStyleSheet("#GameWindow{border-image:url(resources/Icon.png)}")

    def draw(self):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 10))

        for i in self.level.segments:
            painter.drawLine(*i.start, *i.end)
        self.counter += 1

        if (self.counter%50==0 and self.level.balls_amount < self.level.max_balls):
            self.level.add_ball()

        for i in self.level.balls:

            painter.setPen(QtGui.QPen(QtCore.Qt.red, 10))
            painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
            painter.drawEllipse(int(i.position[0]-i.radius), int(i.position[1]-i.radius), i.radius*2, i.radius*2)

        painter.end()

    def paintEvent(self, event):
        if not(self.level.game_end):
            for i in self.level.balls:
                self.level.move_ball(i, 1)
        self.draw()
        self.update()

    def end_game(self):
        pass
