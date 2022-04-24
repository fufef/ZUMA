import math
import random

from PyQt5 import QtGui
from userBall import userBalls
from balls import Ball
from segment import Segment


'''генерация нового шарика'''
def _generate_ball(colors: list, x: int, y: int, prev_colors: list):
    return Ball(generate_color(colors, prev_colors), (x, y))


'''генерация возможного цвета для шарика'''
def generate_color(colors: list, prev_colors: list):
    allowed_colors = list(filter(lambda x: not prev_colors or x not in prev_colors, colors))
    return allowed_colors[random.randint(0, len(allowed_colors) - 1)]


class Level():
    def __init__(self, number: int, segments: list, colors: list, max_balls: int, screen_size: (int, int)):
        self.number = number
        self.segments = segments
        self.colors = colors
        self.balls = [_generate_ball(colors, *segments[0].start, [])]
        self.balls_amount = 1
        self.max_balls = max_balls
        self.game_end = False
        self.userBallS = userBalls(generate_color(colors, []), screen_size)
        self.screen_size = screen_size

        self.speed = 0.06

    '''добавляет шарик в список шаров уровня'''
    def add_ball(self):
        used_colors = []
        col1 = self.balls[-1].color
        if (len(self.balls) >= 2):
            col2 = self.balls[-2].color

            if col1 == col2:
                used_colors.append(col1)
        self.balls_amount += 1
        self.balls.append(_generate_ball(self.colors, *self.segments[0].start, used_colors))

    '''движение шаров'''
    def move_ball(self, ball: Ball, distance: float):
        pos = ball.position
        segment_number = ball.segment_number
        new_point, new_seg_num = self.get_coordinates(pos, distance, segment_number)
        ball.position = new_point
        ball.segment_number = new_seg_num

    '''новые координаты объекта'''
    def get_coordinates(self, pos: (int, int), distance: float, segment_number: int):
        cur_seg = self.segments[segment_number]
        new_x = pos[0] + distance * math.cos(cur_seg.angle)
        new_y = pos[1] + distance * math.sin(cur_seg.angle)
        if (math.dist((new_x, new_y), cur_seg.start) > cur_seg.length):
            if segment_number + 1 >= len(self.segments):
                self.game_end = True
            return cur_seg.end, segment_number + 1
        np = (new_x, new_y)
        return np, segment_number

    '''извлекает информацию об уровне из файла'''
    @staticmethod
    def parse(file: str, screen_size: (int, int)):
        with open(file) as f:
            number = int(f.readline())
            points = list(map(lambda x: tuple(map(int, x[1:-1].split(','))), f.readline().split()))
            segments = list(map(lambda x: Segment(*x), zip(points, points[1:])))
            colors = list(map(lambda x: QtGui.QColor(x), f.readline().split()))
            max_balls = int(f.readline())

        return Level(number, segments, colors, max_balls, screen_size)
