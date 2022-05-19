import sys
import pygame
from PyQt5 import QtWidgets, QtCore, QtGui
from game import Game
from game_model import GameModel
from level import Level
from menu import Menu


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("resources/Icon.png"))
        self.setWindowTitle("Zuma THE GAME")
        self.setFixedSize(1200, 800)

        self.central_widget = QtWidgets.QWidget(self)
        self.stacked_widget = QtWidgets.QStackedWidget(self.central_widget)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.setCentralWidget(self.central_widget)

        size = (1200, 800)
        levels = list()
        levels.append(Level.parse("level1.txt", size))
        levels.append(Level.parse("level2.txt", size))
        levels.append(Level.parse("level3.txt", size))
        levels.append(Level.parse("level4.txt", size))
        levels.append(Level.parse("level5.txt", size))
        levels.append(Level.parse("level6.txt", size))
        levels.append(Level.parse("level7.txt", size))
        levels.append(Level.parse("level8.txt", size))
        levels.append(Level.parse("level9.txt", size))

        self.model = GameModel(levels, 0)
        game = Game(self, self.model)
        self.stacked_widget.addWidget(Menu(self, self.model))
        self.stacked_widget.addWidget(game)
        pygame.init()

    def change_window(self, number):
        try:
            self.stacked_widget.setCurrentIndex(number)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
