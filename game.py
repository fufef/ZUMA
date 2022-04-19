import math

from PyQt5 import QtWidgets, QtCore, QtGui

import level
from balls import Ball
from level import Level
from userBall import userBall


def is_intersect(ball1: Ball, ball2: Ball):
    return math.dist(ball1.position, ball2.position) <= ball1.radius + ball2.radius + 1


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        return -1, -1

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


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

        self.levels = list()
        self.levelIndex = 0
        self.levels.append(Level.parse("level1.txt", self.screen_size))
        self.levels.append(Level.parse("level2.txt", self.screen_size))
        self.levels.append(Level.parse("level3.txt", self.screen_size))
        self.level = self.levels[self.levelIndex]
        self.counter = 0
        self.paused = False

        self.setObjectName("GameWindow")
        self.setStyleSheet("#GameWindow{border-image:url(resources/background.png)}")

    def back_menu_action(self):
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
            draw_ball(painter, i)

        draw_ball(painter, self.level.userBallS.static)
        for i in self.level.userBallS.moving:
            draw_ball(painter, i)

        painter.end()

    def paintEvent(self, event):
        if self.paused:
            pass
        elif len(self.level.balls) == 0:
            self.level = self.levels[self.levelIndex + 1]
            self.counter = 0
        elif self.level.game_end:
            self.level = Level(self.level.number, self.level.segments, self.level.colors, self.level.max_balls,
                               self.level.screen_size)
            self.counter = 0
        else:
            pairs = zip(reversed(self.level.balls[:-1]), reversed(self.level.balls))

            self.level.move_ball(self.level.balls[-1], self.level.speed)
            for i, j in pairs:
                if math.dist(i.position, j.position) <= i.radius + j.radius:
                    self.level.move_ball(i, self.level.speed)

            self.counter += 1

            diameter_over_speed = self.level.balls[0].radius * 2 / self.level.speed

            if self.counter >= diameter_over_speed and self.level.balls_amount < self.level.max_balls:
                self.counter -= diameter_over_speed
                self.level.add_ball()

            del_balls = set()
            for i in self.level.userBallS.moving:
                i.position = (i.position[0] + i.moveSpeed[0], i.position[1] + i.moveSpeed[1])

                if not i.is_on_screen((1200, 800)):
                    del_balls.add(i)

            self.level.userBallS.moving = list(filter(lambda x: x not in del_balls, self.level.userBallS.moving))

            for i in self.level.userBallS.moving:
                self.tmp(i)

        self.collapse()
        self.draw()
        self.update()

    def tmp(self, i):
        epsilon = 1
        for j1, segment in enumerate(self.level.segments):
            d1 = math.dist(segment.start, i.position)
            d2 = math.dist(segment.end, i.position)
            d3 = math.dist(segment.end, segment.start)

            if abs(d1 + d2 - d3) < epsilon:
                p = line_intersection((segment.start, segment.end), (self.level.userBallS.static.position, i.position))
                indices, nearest_index1, min_dist1, nearest_index2, min_dist2, r = \
                    self._get_balls_intersection_data(p, epsilon)

                if len(indices) > 0:
                    if indices == [0]:
                        self._insert_in_begin_position()
                    else:
                        self._insert_standard(nearest_index1, nearest_index2, min_dist2, r, j1)

                    self.level.userBallS.moving.remove(i)

    def _get_balls_intersection_data(self, p, epsilon):
        indices = []
        nearest_index1, nearest_index2 = None, None
        min_dist1, min_dist2 = None, None
        r = None

        for k, b in enumerate(self.level.balls):
            if not r:
                r = b.radius

            dist = math.dist(b.position, p)

            if not min_dist1 or dist < min_dist1:
                min_dist2, nearest_index2 = min_dist1, nearest_index1
                min_dist1 = dist
                nearest_index1 = k
            elif not min_dist2 or dist < min_dist2:
                min_dist2 = dist
                nearest_index2 = k

            if dist < 2 * b.radius + epsilon:
                indices.append(k)

        return indices, nearest_index1, min_dist1, nearest_index2, min_dist2, r

    def _insert_in_begin_position(self):
        prev_ball = self.level.balls[0]
        prev_pos = prev_ball.position
        prev_seg_num = prev_ball.segment_number
        self.level.move_ball(prev_ball, prev_ball.radius * 2)
        new_ball = Ball(self.level.userBallS.moving[0].color, prev_ball.position,
                        prev_ball.segment_number)
        prev_ball.position = prev_pos
        prev_ball.segment_number = prev_seg_num
        self.level.balls.insert(0, new_ball)

    def _insert_standard(self, nearest_index1, nearest_index2, min_dist2, r, seg_num):
        if not nearest_index2:
            nearest_index2 = nearest_index1

        if min_dist2 and min_dist2 >= 2 * r:
            nearest_index2 = nearest_index1

        nearest_index = min(nearest_index1, nearest_index2)
        prev_ball = self.level.balls[nearest_index]
        new_ball = Ball(self.level.userBallS.moving[0].color, prev_ball.position, seg_num)
        self.level.balls.insert(nearest_index + 1, new_ball)

        for k in range(nearest_index + 1):
            self.level.move_ball(self.level.balls[k], self.level.balls[k].radius * 2)

    def collapse(self):
        r = set()
        for i in range(len(self.level.balls)):
            ball = self.level.balls[i]
            collided = [j for j in range(i - 1, i + 2, 2)
                        if -1 < j < len(self.level.balls) and is_intersect(ball, self.level.balls[j])]

            collided_balls = map(lambda x: self.level.balls[x], collided)
            same_clr_collided = set(filter(lambda x: x.color == ball.color,
                                           collided_balls))

            if len(same_clr_collided) > 1:
                r.add(ball)
                r.update(same_clr_collided)
        self.level.balls = list(filter(lambda x: x not in r, self.level.balls))

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if not self.paused:
            staticBall = self.level.userBallS.static
            deltaX = e.windowPos().x() - staticBall.position[0]
            deltaY = e.windowPos().y() - staticBall.position[1]

            speed = 8
            angle = math.atan2(deltaY, deltaX)
            staticBall.moveSpeed = (speed * math.cos(angle), speed * math.sin(angle))
            self.level.userBallS.moving.append(staticBall)
            self.level.userBallS.static = userBall(level.generate_color(self.level.colors, []), staticBall.position)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.nativeScanCode() == 25:
            self.paused = not self.paused
        if not self.paused:
            if e.nativeScanCode() == 19:
                self.level = Level(self.level.number, self.level.segments, self.level.colors, self.level.max_balls,
                                   self.level.screen_size)
                self.counter = 0

    def end_game(self):
        pass
