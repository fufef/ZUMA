import math
from balls import Ball


class GeometryExtensions:
    @classmethod
    def is_intersect(cls, ball1: Ball, ball2: Ball, d: int):
        """Checks balls for intersection

        :param ball1: first ball
        :type ball1: Ball
        :param ball2: second ball
        :type ball2: Ball
        :param d: small delta to determine intersection
        :type d: int

        :rtype: bool
        """
        return math.dist(ball1.position, ball2.position) <= ball1.radius + ball2.radius + d

    @classmethod
    def __det__(cls, a, b):
        return a[0] * b[1] - a[1] * b[0]

    @classmethod
    def line_intersection(cls, line1, line2):
        """Finds intersection of two lines of returns (-1, -1) if no intersection

        :param line1: first line
        :type line1: ((int, int), (int, int))
        :param line2: second line
        :type line2: ((int, int), (int, int))

        :rtype: (int, int)
        """
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        div = GeometryExtensions.__det__(xdiff, ydiff)
        if div == 0:
            return -1, -1

        d = (GeometryExtensions.__det__(*line1), GeometryExtensions.__det__(*line2))
        x = GeometryExtensions.__det__(d, xdiff) / div
        y = GeometryExtensions.__det__(d, ydiff) / div
        return x, y
