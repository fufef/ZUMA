import unittest
from balls import Ball
from level import Level
from game_model import GameModel
from PyQt5 import QtGui
import copy

from userBall import userBall


def get_model():
    levels = list()
    levels.append(Level.parse("level1.txt", (1000, 1000)))
    levels.append(Level.parse("level2.txt", (1000, 1000)))
    levels.append(Level.parse("level3.txt", (1000, 1000)))
    return GameModel(levels)


class pause_tests(unittest.TestCase):
    def test_pauses(self):
        model = get_model()
        model.pause()
        self.assertEqual(model.paused, True)

    def test_unpauses(self):
        model = get_model()
        model.paused = True
        model.pause()
        self.assertEqual(model.paused, False)


class restart_tests(unittest.TestCase):
    def test_starts_the_same_level(self):
        model = get_model()
        index = model.levelIndex
        model.restart()
        self.assertEqual(index, model.levelIndex)

    def test_resets_level(self):
        model = get_model()
        segments = copy.copy(model.level.segments)
        balls = copy.copy(model.level.balls)
        model.update_game()
        model.restart()
        self.assertEqual(model.level.segments, segments)
        self.assertNotEqual(model.level.balls, balls)


class shoot_tests(unittest.TestCase):
    def test_adds_new_moving_ball(self):
        model = get_model()
        count = len(model.level.user_balls.moving)
        model.shoot((0, 0))
        self.assertEqual(len(model.level.user_balls.moving), count + 1)

    def test_adds_new_static_ball(self):
        model = get_model()
        static = model.level.user_balls.static
        model.shoot((0, 0))
        self.assertNotEqual(model.level.user_balls.static, static)

    def test_moving_to_correct_direction_x(self):
        model = get_model()
        model.shoot((492, 500))
        self.assertAlmostEqual(model.level.user_balls.moving[len(model.level.user_balls.moving) - 1].moveSpeed[0], -8)
        self.assertAlmostEqual(model.level.user_balls.moving[len(model.level.user_balls.moving) - 1].moveSpeed[1], 0)

    def test_moving_to_correct_direction_y(self):
        model = get_model()
        model.shoot((500, 492))
        self.assertAlmostEqual(model.level.user_balls.moving[len(model.level.user_balls.moving) - 1].moveSpeed[0], 0)
        self.assertAlmostEqual(model.level.user_balls.moving[len(model.level.user_balls.moving) - 1].moveSpeed[1], -8)


class collapse_tests(unittest.TestCase):
    def test_removes_balls_of_the_same_colors(self):
        model = get_model()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 4 * d), 1))
        model.collapse()
        self.assertEqual(balls, model.level.balls)

    def test_removes_balls_of_the_same_colors_more_than_three(self):
        model = get_model()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 4 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 6 * d), 1))
        model.collapse()
        self.assertEqual(balls, model.level.balls)

    def test_not_removes_balls_of_the_same_colors_less_than_three(self):
        model = get_model()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.collapse()
        self.assertNotEqual(balls, model.level.balls)

    def test_not_removes_balls_of_different_colors(self):
        model = get_model()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.black, (900, 650 - 4 * d), 1))
        model.collapse()
        self.assertNotEqual(balls, model.level.balls)


class intersect_balls_tests(unittest.TestCase):
    def test_removes_moving_ball(self):
        model = get_model()
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        b = userBall(QtGui.QColor.blue, (900, 499))
        model.level.user_balls.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.user_balls.moving), 0)

    def test_adds_new_ball_to_the_right_side(self):
        model = get_model()
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        b = userBall(QtGui.QColor.blue, (900, 499))
        k = len(copy.copy(model.level.balls))
        model.level.user_balls.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.balls), k + 1)

    def test_adds_new_ball_to_the_lef_at_side(self):
        model = get_model()
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        b = userBall(QtGui.QColor.blue, (900, 501))
        k = len(copy.copy(model.level.balls))
        model.level.user_balls.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.balls), k + 1)

    def test_adds_new_ball_between_other_balls(self):
        model = get_model()
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500 + 2 * d), 1))
        b = userBall(QtGui.QColor.blue, (900, 500 + d))
        k = len(copy.copy(model.level.balls))
        model.level.user_balls.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.balls), k + 1)


class updateGame(unittest.TestCase):
    def test_do_nothing_when_paused(self):
        model = get_model()
        model.paused = True
        m = copy.copy(model)
        model.update_game()
        self.assertEqual(m.level, model.level)

    def test_starts_next_level_when_no_balls(self):
        model = get_model()
        model.level.balls = list()
        model.update_game()
        self.assertEqual(model.levelIndex, 1)

    def test_restarts_when_loss(self):
        model = get_model()
        model.level.balls.append(Ball(QtGui.QColor.blue, (300, 300), 3))
        model.update_game()
        self.assertEqual(model.levelIndex, 0)

    def test_moves_balls(self):
        model = get_model()
        p = copy.copy(model.level.balls[0])
        model.update_game()
        self.assertNotEqual(p, model.level.balls[0])

    def test_moves_user_balls(self):
        model = get_model()
        model.shoot((0, 0))
        p = copy.copy(model.level.user_balls.moving[0].position)
        model.update_game()
        self.assertNotEqual(p, model.level.user_balls.moving[0].position)


if __name__ == '__main__':
    unittest.main()
