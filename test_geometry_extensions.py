import unittest
from geometry_extensions import GeometryExtensions
from balls import Ball


class is_intersect_tests(unittest.TestCase):
    def test_not_intersected(self):
        result = GeometryExtensions.is_intersect(Ball(None, (0, 0)), Ball(None, (0, 100)), 1)
        self.assertEqual(result, False)

    def test_intersected(self):
        result = GeometryExtensions.is_intersect(Ball(None, (0, 0)), Ball(None, (0, 10)), 1)
        self.assertEqual(result, True)

    def test_one_ball_inside_another(self):
        result = GeometryExtensions.is_intersect(Ball(None, (0, 0)), Ball(None, (0, 0)), 1)
        self.assertEqual(result, True)


class det_tests(unittest.TestCase):
    def test_countsCorrectly_WithZeroes(self):
        result = GeometryExtensions.__det__((0, 0), (0, 0))
        self.assertEqual(result, 0)

    def test_counts_correctly_with_non_zeroes(self):
        result = GeometryExtensions.__det__((1, 2), (3, 4))
        self.assertEqual(result, -2)


class line_intersection_tests(unittest.TestCase):
    def test_returns_when_no_intersection(self):
        result = GeometryExtensions.line_intersection(((0, 0), (0, 1)), ((1, 0), (1, 1)))
        self.assertEqual(result, (-1, -1))

    def test_returns_when_the_same_line(self):
        result = GeometryExtensions.line_intersection(((0, 0), (0, 1)), ((0, 0), (0, 1)))
        self.assertEqual(result, (-1, -1))

    def test_returns_correct_intersection_when_lines_intersects(self):
        result = GeometryExtensions.line_intersection(((0, 0), (0, 1)), ((0, 1), (2, 2)))
        self.assertEqual(result, (0, 1))


if __name__ == '__main__':
    unittest.main()
