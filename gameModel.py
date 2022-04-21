import math
from level import Level
from balls import Ball
from geometryExtensions import GeometryExtensions
from userBall import userBall
from level import generate_color

class GameModel:
    def __init__(self, levels: list):
        self.levelIndex = 0
        self.levels = levels
        self.level = self.levels[self.levelIndex]
        self.counter = 0
        self.paused = False

    def updateGame(self):
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
                
    def tmp(self, i):
        epsilon = 1
        for j1, segment in enumerate(self.level.segments):
            d1 = math.dist(segment.start, i.position)
            d2 = math.dist(segment.end, i.position)
            d3 = math.dist(segment.end, segment.start)

            if abs(d1 + d2 - d3) < epsilon:
                p = GeometryExtensions.line_intersection((segment.start, segment.end), (self.level.userBallS.static.position, i.position))
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
                        if -1 < j < len(self.level.balls) and GeometryExtensions.is_intersect(ball, self.level.balls[j], 1)]
            collided_balls = map(lambda x: self.level.balls[x], collided)
            same_clr_collided = set(filter(lambda x: x.color == ball.color,
                                           collided_balls))

            if len(same_clr_collided) > 1:
                r.add(ball)
                r.update(same_clr_collided)
        self.level.balls = list(filter(lambda x: x not in r, self.level.balls))

    def shoot(self, p):
        staticBall = self.level.userBallS.static
        deltaX = p[0] - staticBall.position[0]
        deltaY = p[1] - staticBall.position[1]
        speed = 8
        angle = math.atan2(deltaY, deltaX)
        staticBall.moveSpeed = (speed * math.cos(angle), speed * math.sin(angle))
        self.level.userBallS.moving.append(staticBall)
        self.level.userBallS.static = userBall(generate_color(self.level.colors, []), staticBall.position)
    
    def pause(self):
        self.paused = not self.paused

    def restart(self):
        self.level = Level(self.level.number, self.level.segments, self.level.colors, self.level.max_balls, self.level.screen_size)
        self.counter = 0

