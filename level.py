import math
import random

from balls import Ball
from segment import Segment


def _generate_ball(colors: list, x: int, y: int, prev_colors=None):
    allowed_colors = list(filter(lambda x: not prev_colors or x not in prev_colors, colors))
    return Ball(allowed_colors[random.randint(0, len(allowed_colors) - 1)], (x, y))


class Level():
    def __init__(self, number: int, segments: list, colors: list):
        self.number = number
        self.segments = segments  # мб + самый первый отрезок
        self.colors = colors
        self.balls = [_generate_ball(colors, *segments[0].start)]
        self.balls_amount = 1
        self.max_balls = 5
        self.game_end = False

    def add_ball(self):
        used_colors = []
        col1 = self.balls[-1].color
        if (len(self.balls) >= 2):
            col2 = self.balls[-2].color

            if col1 == col2:
                used_colors.append(col1)
        self.balls_amount += 1
        self.balls.append(_generate_ball(self.colors, *self.segments[0].start, used_colors))

    def move_ball(self, ball: Ball, distance: float):
        pos = ball.position
        segment_number = ball.segment_number
        new_point, new_seg_num = self.get_coordinates(pos, distance, segment_number)
        ball.position = new_point
        ball.segment_number = new_seg_num

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

    @staticmethod
    def parse(file: str):
        with open(file) as f:
            number = int(f.readline())
            points = list(map(lambda x: tuple(map(int, x[1:-1].split(','))), f.readline().split()))
            segments = list(map(lambda x: Segment(*x), zip(points, points[1:])))
            colors = f.readline().split()

        return Level(number, segments, colors)
