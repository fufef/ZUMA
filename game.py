from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from menu import Menu


class Game(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        #self.resize(800,800)
        self.main_window = main_window

        self.backMenu_btn = QtWidgets.QPushButton(self)
        self.backMenu_btn.setGeometry(QtCore.QRect(50, 50, 50, 50))
        self.backMenu_btn.setObjectName("backMenu_btn")
        self.backMenu_btn.clicked.connect(lambda: main_window.change_window(0))

        self.setObjectName("GameWindow")
        self.setStyleSheet("#GameWindow{border-image:url(resources/Icon.png)}")

        

    '''def paintEvent(self):
        if self.is_running:
            """шевеление картинок"""
            pass
        self.update()'''
