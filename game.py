from PyQt5 import QtWidgets, QtCore, QtGui
from balls import Ball
from level import Level
from segment import Segment
from userBall import userBall
import math

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

        self.drawBall(painter, self.level.userBallS.static)
        for i in self.level.userBallS.moving:
            self.drawBall(painter, i)

        painter.end()

    def drawBall(self, painter, ball : userBall):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 10))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        painter.drawEllipse(int(ball.position[0]-ball.radius), int(ball.position[1]-ball.radius), ball.radius*2, ball.radius*2)

    def paintEvent(self, event):
        if not(self.level.game_end):
            for i in self.level.balls:
                self.level.move_ball(i, 1)
            for i in self.level.userBallS.moving:
                i.position = (i.position[0] + i.moveSpeed[0], i.position[1] + i.moveSpeed[1])
            epsilon = 1
            for i in self.level.userBallS.moving:
                for j in self.level.segments:
                    #print("YEP")
                    d1 = self.getDistance(j.start, i.position)
                    d2 = self.getDistance(j.end, i.position)
                    d3 = self.getDistance(j.end, j.start)
                    if(abs(d1 + d2 - d3) < epsilon):
                        p = self.line_intersection((j.start, j.end), ((200, 200), (i.position)))
                        count = 0
                        for k in self.level.balls:
                            if(abs(self.getDistance(k.position, p)) < 2 * k.radius + epsilon):
                                count += 1

                        if(count >= 2):
                            self.level.balls.append(Ball("", p, self.level.segments.index(j)))
                            self.level.userBallS.moving.remove(i)
        self.draw()
        self.update()

    def det(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 


        div = self.det(xdiff, ydiff)
        if div == 0:
            return (-1, -1)

        d = (self.det(*line1), self.det(*line2))
        x = self.det(d, xdiff) / div
        y = self.det(d, ydiff) / div
        return x, y


    def getDistance(self, p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    
    def mousePressEvent(self, e: QtGui.QMouseEvent):
        d1 = 1
        d2 = 1
        staticBall = self.level.userBallS.static
        deltaX = e.windowPos().x() - staticBall.position[0]
        deltaY = e.windowPos().y() - staticBall.position[1]
        if(deltaX < 0):
            d1 = -1
        if(deltaY < 0):
            d2 = -1
        deltaX = abs(deltaX)
        deltaY = abs(deltaY)
        angle = math.atan(deltaY / deltaX)
        staticBall.moveSpeed = (d1 * math.cos(angle), d2 * math.sin(angle))
        self.level.userBallS.moving.append(staticBall)
        self.level.userBallS.static = userBall("", (200, 200))
        #self.draw()
        #self.update()

    def end_game(self):
        pass
