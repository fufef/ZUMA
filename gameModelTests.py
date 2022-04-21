import unittest
from level import Level
from gameModel import GameModel
import copy

levels = list()
levels.append(Level.parse("level1.txt", (1000, 1000)))
levels.append(Level.parse("level2.txt", (1000, 1000)))
levels.append(Level.parse("level3.txt", (1000, 1000)))
model = GameModel(levels)

class pause_tests(unittest.TestCase):
    def test_pauses(self):
        model.pause()
        self.assertEqual(model.paused, True)
    
    def test_unpauses(self):
        model.paused = True
        model.pause()
        self.assertEqual(model.paused, False)

class restart_tests(unittest.TestCase):
    def test_startsTheSameLevel(self):
        index = model.levelIndex
        model.restart()
        self.assertEqual(index, model.levelIndex)

    def test_resetsLevel(self): #Todo: override equals correctly
        level = copy.copy(model.level)
        model.updateGame()
        model.restart()
        self.assertEqual(model.level, level)

class shoot_tests(unittest.TestCase):
    def test_addsNewMovingBall(self):
        count = len(model.level.userBallS.moving)
        model.shoot((0, 0))
        self.assertEqual(len(model.level.userBallS.moving), count + 1)
    
    def test_addsNewStaticBall(self):
        static = model.level.userBallS.static
        model.shoot((0, 0))
        self.assertNotEqual(model.level.userBallS.static, static)    

if __name__ == '__main__':
    unittest.main()