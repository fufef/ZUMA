import unittest
from geometryExtensions import GeometryExtensions
from balls import Ball


class is_intersect_tests(unittest.TestCase):
    def test_not_intersected(self):
        result = GeometryExtensions.is_intersect(Ball(None, (0, 0)), Ball(None, (0, 100)), 1)
        self.assertEqual(result, False)

    def test_intersected(self):
        result = GeometryExtensions.is_intersect(Ball(None, (0, 0)), Ball(None, (0, 10)), 1)
        self.assertEqual(result, True)

    def test_oneBallInsideAnother(self):
        result = GeometryExtensions.is_intersect(Ball(None, (0, 0)), Ball(None, (0, 0)), 1)
        self.assertEqual(result, True)


class det_tests(unittest.TestCase):
    def test_countsCorrectly_WithZeroes(self):
        result = GeometryExtensions.__det__((0, 0), (0, 0))
        self.assertEqual(result, 0)

    def test_countsCorrectly_WithNonZeroes(self):
        result = GeometryExtensions.__det__((1, 2), (3, 4))
        self.assertEqual(result, -2)


class line_intersection_tests(unittest.TestCase):
    def test_returns_whenNoIntersection(self):
        result = GeometryExtensions.line_intersection(((0, 0), (0, 1)), ((1, 0), (1, 1)))
        self.assertEqual(result, (-1, -1))

    def test_returns_whenTheSameLine(self):
        result = GeometryExtensions.line_intersection(((0, 0), (0, 1)), ((0, 0), (0, 1)))
        self.assertEqual(result, (-1, -1))

    def test_returnsCorrectIntersection_whenLinesIntersects(self):
        result = GeometryExtensions.line_intersection(((0, 0), (0, 1)), ((0, 1), (2, 2)))
        self.assertEqual(result, (0, 1))


if __name__ == '__main__':
    unittest.main()
