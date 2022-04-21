import math
from balls import Ball

class GeometryExtensions:
    @classmethod
    def is_intersect(self, ball1: Ball, ball2: Ball, d: int):
        return math.dist(ball1.position, ball2.position) <= ball1.radius + ball2.radius + d

    @classmethod
    def det(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    @classmethod
    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        div = GeometryExtensions.det(xdiff, ydiff)
        if div == 0:
            return -1, -1

        d = (GeometryExtensions.det(*line1), GeometryExtensions.det(*line2))
        x = GeometryExtensions.det(d, xdiff) / div
        y = GeometryExtensions.det(d, ydiff) / div
        return x, y
