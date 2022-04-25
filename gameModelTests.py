import unittest
from balls import Ball
from level import Level
from gameModel import GameModel
from PyQt5 import QtGui
import copy

from userBall import userBall

def getModel():
    levels = list()
    levels.append(Level.parse("level1.txt", (1000, 1000)))
    levels.append(Level.parse("level2.txt", (1000, 1000)))
    levels.append(Level.parse("level3.txt", (1000, 1000)))
    return GameModel(levels)

class pause_tests(unittest.TestCase):
    def test_pauses(self):
        model = getModel()
        model.pause()
        self.assertEqual(model.paused, True)
    
    def test_unpauses(self):
        model = getModel()
        model.paused = True
        model.pause()
        self.assertEqual(model.paused, False)

class restart_tests(unittest.TestCase):
    def test_startsTheSameLevel(self):
        model = getModel()
        index = model.levelIndex
        model.restart()
        self.assertEqual(index, model.levelIndex)

    def test_resetsLevel(self):
        model = getModel()
        segments = copy.copy(model.level.segments)
        balls = copy.copy(model.level.balls)
        model.updateGame()
        model.restart()
        self.assertEqual(model.level.segments, segments)
        self.assertNotEqual(model.level.balls, balls)

class shoot_tests(unittest.TestCase):
    def test_addsNewMovingBall(self):
        model = getModel()
        count = len(model.level.userBallS.moving)
        model.shoot((0, 0))
        self.assertEqual(len(model.level.userBallS.moving), count + 1)
    
    def test_addsNewStaticBall(self):
        model = getModel()
        static = model.level.userBallS.static
        model.shoot((0, 0))
        self.assertNotEqual(model.level.userBallS.static, static)    

    def test_movingToCorrectDirection_x(self):
        model = getModel()
        model.shoot((492, 500))
        self.assertAlmostEqual(model.level.userBallS.moving[len(model.level.userBallS.moving) - 1].moveSpeed[0], -8)
        self.assertAlmostEqual(model.level.userBallS.moving[len(model.level.userBallS.moving) - 1].moveSpeed[1], 0)

    def test_movingToCorrectDirection_y(self):
        model = getModel()
        model.shoot((500, 492))
        self.assertAlmostEqual(model.level.userBallS.moving[len(model.level.userBallS.moving) - 1].moveSpeed[0], 0)
        self.assertAlmostEqual(model.level.userBallS.moving[len(model.level.userBallS.moving) - 1].moveSpeed[1], -8)

class collapse_tests(unittest.TestCase):
    def test_removesBallsOfTheSameColors(self):
        model = getModel()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 4 * d), 1))
        model.collapse()
        self.assertEqual(balls, model.level.balls)
    
    def test_removesBallsOfTheSameColors_moreThanThree(self):
        model = getModel()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 4 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 6 * d), 1))
        model.collapse()
        self.assertEqual(balls, model.level.balls)
    
    def test_notRemovesBallsOfTheSameColors_lessThanThree(self):
        model = getModel()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.collapse()
        self.assertNotEqual(balls, model.level.balls)
    
    def test_notRemovesBallsOfDifferentColors(self):
        model = getModel()
        balls = copy.copy(model.level.balls)
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 650 - 2 * d), 1))
        model.level.balls.append(Ball(QtGui.QColor.black, (900, 650 - 4 * d), 1))
        model.collapse()
        self.assertNotEqual(balls, model.level.balls)

class intersect_balls_tests(unittest.TestCase):
    def test_removesMovingBall(self):
        model = getModel()
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        b = userBall(QtGui.QColor.blue, (900, 499))
        model.level.userBallS.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.userBallS.moving), 0)

    def test_addsNewBallToTheRightSide(self):
        model = getModel()
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        b = userBall(QtGui.QColor.blue, (900, 499))
        k = len(copy.copy(model.level.balls))
        model.level.userBallS.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.balls), k + 1)
    
    def test_addsNewBallToTheLeftSide(self):
        model = getModel()
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        b = userBall(QtGui.QColor.blue, (900, 501))
        k = len(copy.copy(model.level.balls))
        model.level.userBallS.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.balls), k + 1)
    
    def test_addsNewBallBetweenOtherBalls(self):
        model = getModel()
        d = 15
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500), 1))
        model.level.balls.append(Ball(QtGui.QColor.blue, (900, 500 + 2 * d), 1))
        b = userBall(QtGui.QColor.blue, (900, 500 + d))
        k = len(copy.copy(model.level.balls))
        model.level.userBallS.moving.append(b)
        model.intersect_balls(b)
        self.assertEqual(len(model.level.balls), k + 1)

class updateGame(unittest.TestCase):
    def test_doNothing_whenPaused(self):
        model = getModel()
        model.paused = True
        m = copy.copy(model)
        model.updateGame()
        self.assertEqual(m.level, model.level)
    
    def test_startsNextLevel_whenNoBalls(self):
        model = getModel()
        model.level.balls = list()
        model.updateGame()
        self.assertEqual(model.levelIndex, 1)
    
    def test_restarts_whenLoss(self):
        model = getModel()
        model.level.balls.append(Ball(QtGui.QColor.blue, (300, 300), 3))
        model.updateGame()
        self.assertEqual(model.levelIndex, 0)
    
    def test_movesBalls(self):
        model = getModel()
        p = copy.copy(model.level.balls[0])
        model.updateGame()
        self.assertNotEqual(p, model.level.balls[0])
    
    def test_movesUserBalls(self):
        model = getModel()
        model.shoot((0, 0))
        p = copy.copy(model.level.userBallS.moving[0].position)
        model.updateGame()
        self.assertNotEqual(p, model.level.userBallS.moving[0].position)
    
if __name__ == '__main__':
    unittest.main()