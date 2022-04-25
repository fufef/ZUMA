import math
from geometryExtensions import GeometryExtensions
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit
from gameModel import GameModel
from PyQt5.QtCore import QRect, Qt
import level
from balls import Ball
from level import Level
from userBall import userBall


'''отображает шар'''
def draw_ball(painter, ball: [userBall | Ball]):
    painter.setBrush(QtGui.QBrush(ball.color))
    painter.drawEllipse(int(ball.position[0] - ball.radius), int(ball.position[1] - ball.radius), ball.radius * 2,
                        ball.radius * 2)


class Game(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.screen_size = (main_window.size().width(), main_window.size().height())
        self.main_window = main_window

        self.backMenu_btn = QtWidgets.QPushButton(self)
        self.backMenu_btn.setGeometry(QtCore.QRect(25, 25, 40, 30))
        self.backMenu_btn.setObjectName("backMenu_btn")
        self.backMenu_btn.clicked.connect(self.back_menu_action)

        levels = list()
        levels.append(Level.parse("level1.txt", self.screen_size))
        levels.append(Level.parse("level2.txt", self.screen_size))
        levels.append(Level.parse("level3.txt", self.screen_size))

        self.model = GameModel(levels)

        self.setObjectName("GameWindow")
        self.setStyleSheet("#GameWindow{border-image:url(resources/background.png)}")

    def back_menu_action(self):
        self.model.level.game_end = True
        self.model.paused = False
        self.main_window.change_window(0)

    def draw(self):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 10))
        if(self.model.finished):
            rect = QRect(0, 0, 1200, 800)
            painter.drawText(rect, Qt.AlignCenter, "Поздравляем! Ты прошел игру")
        else:

            for i in self.model.level.segments:
                painter.drawLine(*i.start, *i.end)

            painter.setPen(QtCore.Qt.NoPen)

            for i in self.model.level.balls:
                draw_ball(painter, i)

            draw_ball(painter, self.model.level.userBallS.static)
            for i in self.model.level.userBallS.moving:
                draw_ball(painter, i)

            painter.end()

    def paintEvent(self, event):
        self.model.updateGame()
        self.model.collapse()
        self.draw()
        self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if not self.model.paused:
            self.model.shoot((e.windowPos().x(), e.windowPos().y()))

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.nativeScanCode() == 25:
            self.model.pause()
        if not self.model.paused:
            if e.nativeScanCode() == 19:
                self.model.restart()

    def end_game(self):
        pass
