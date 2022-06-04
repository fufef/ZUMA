import pygame
from PyQt5 import QtWidgets, QtCore, QtGui

from game import Game
from menu import Menu


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, users, name):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("resources/Icon.png"))
        self.setWindowTitle("Zuma THE GAME")
        self.setFixedSize(1200, 800)

        self.central_widget = QtWidgets.QWidget(self)
        self.stacked_widget = QtWidgets.QStackedWidget(self.central_widget)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.setCentralWidget(self.central_widget)

        self.model = model
        game = Game(self, self.model, users, name)
        self.stacked_widget.addWidget(Menu(self, self.model, users, name))
        self.stacked_widget.addWidget(game)
        pygame.init()

    def change_window(self, number):
        try:
            self.stacked_widget.setCurrentIndex(number)
        except Exception as e:
            print(e)
