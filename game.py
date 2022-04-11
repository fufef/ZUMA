import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPointF

import level
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
        self.backMenu_btn.clicked.connect(self.backMenu_action)

        self.levels = list()
        self.levelIndex = 0
        self.levels.append(Level.parse("level1.txt"))
        self.levels.append(Level.parse("level2.txt"))
        self.level = self.levels[self.levelIndex]
        self.counter = 0
        self.paused = False

        self.setObjectName("GameWindow")
        self.setStyleSheet("#GameWindow{border-image:url(resources/Icon.png)}")

    def backMenu_action(self):
        self.level.game_end = True
        self.paused = False
        self.main_window.change_window(0)

    def draw(self):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 10))

        for i in self.level.segments:
            painter.drawLine(*i.start, *i.end)

        painter.setPen(QtCore.Qt.NoPen)

        for i in self.level.balls:
            painter.setBrush(QtGui.QBrush(i.color))
            painter.drawEllipse(int(i.position[0] - i.radius), int(i.position[1] - i.radius), i.radius * 2,
                                i.radius * 2)

        self.drawBall(painter, self.level.userBallS.static)
        for i in self.level.userBallS.moving:
            self.drawBall(painter, i)

        painter.end()

    def drawBall(self, painter, ball: userBall):
        painter.setBrush(QtGui.QBrush(ball.color))
        painter.drawEllipse(int(ball.position[0] - ball.radius), int(ball.position[1] - ball.radius), ball.radius * 2,
                            ball.radius * 2)

    def paintEvent(self, event):
        if(self.paused):
            pass
        elif(len(self.level.balls) == 0):
            self.level = self.levels[self.levelIndex + 1]
            self.counter = 0
        elif self.level.game_end:
            self.level = Level(self.level.number, self.level.segments, self.level.colors, self.level.max_balls)
            self.counter = 0
        else:
            for i in self.level.balls:
                self.level.move_ball(i, self.level.speed)
            self.counter += 1

            diameter_over_speed = self.level.balls[0].radius * 2 / self.level.speed

            if (self.counter >= diameter_over_speed and self.level.balls_amount < self.level.max_balls):
                self.counter -= diameter_over_speed
                self.level.add_ball()

            for i in self.level.userBallS.moving:
                i.position = (i.position[0] + i.moveSpeed[0], i.position[1] + i.moveSpeed[1])

            epsilon = 1
            for i in self.level.userBallS.moving:
                for j1, segment in enumerate(self.level.segments):
                    d1 = math.dist(segment.start, i.position)
                    d2 = math.dist(segment.end, i.position)
                    d3 = math.dist(segment.end, segment.start)

                    if (abs(d1 + d2 - d3) < epsilon):
                        p = self.line_intersection((segment.start, segment.end), ((200, 200), i.position))
                        indices = []

                        nearest_index = None
                        min_dist = None

                        for k, b in enumerate(self.level.balls):
                            dist = math.dist(b.position, p)

                            if not min_dist or dist < min_dist:
                                min_dist = dist
                                nearest_index = k

                            if (dist < 2 * b.radius + epsilon):
                                indices.append(k)

                        if (len(indices) > 0):
                            moving_dist = self.level.balls[0].radius * 2 - min_dist
                            new_ball = Ball(self.level.userBallS.moving[0].color, p, j1)
                            self.level.balls.insert(nearest_index + 1, new_ball)

                            for k in range(nearest_index + 1):
                                self.level.move_ball(self.level.balls[k], moving_dist)

                            self.collapse()
                            self.level.userBallS.moving.remove(i)
        self.draw()
        self.update()

    def collapse(self):
        r = set()
        for i in range(len(self.level.balls)):
            ball = self.level.balls[i]
            collided = [j for j in range(i - 1, i + 2, 2)
                        if -1 < j < len(self.level.balls) and self.is_intersect(ball, self.level.balls[j])]

            collided_balls = map(lambda x: self.level.balls[x], collided)
            same_clr_collided = set(filter(lambda x: x.color == ball.color,
                                           collided_balls))

            if len(same_clr_collided) > 1:
                r.add(ball)
                r.update(same_clr_collided)
        self.level.balls = list(filter(lambda x: x not in r, self.level.balls))

    def is_intersect(self, ball1: Ball, ball2: Ball):
        return math.dist(ball1.position, ball2.position) <= ball1.radius + ball2.radius + 0.01

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

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if(self.paused):
            pass
        else:
            staticBall = self.level.userBallS.static
            deltaX = e.windowPos().x() - staticBall.position[0]
            deltaY = e.windowPos().y() - staticBall.position[1]

            speed = 10
            angle = math.atan2(deltaY, deltaX)
            staticBall.moveSpeed = (speed * math.cos(angle), speed * math.sin(angle))
            self.level.userBallS.moving.append(staticBall)
            self.level.userBallS.static = userBall(level.generate_color(self.level.colors, []), (200, 200))
        # self.draw()
        # self.update()
    
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if(e.key() == 80):#P
                self.paused = not self.paused
        if(self.paused):
            pass
        else:
            if(e.key() == 82):#R
                self.level = Level(self.level.number, self.level.segments, self.level.colors, self.level.max_balls)
                self.counter = 0
        
    

    def end_game(self):
        pass
