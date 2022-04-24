import pygame
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *


class SettingsWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle('Settings')
        self.window.setFixedSize(300, 400)
        self.window.setWindowIcon(QtGui.QIcon("resources/Icon.png"))

        font = QtGui.QFont()
        font.setPointSize(20)

        '''кнопка в настройках'''
        self.sound_btn = QRadioButton(self.window)
        self.sound_btn.setObjectName(u"sound_btn")
        self.sound_btn.setGeometry(QtCore.QRect(50, 20, 150, 60))
        self.sound_btn.setFont(font)

        self._retranslate_ui()
        

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.sound_btn.setText(_translate("Settings", "Sound"))


    def open_settings(self):
        self.window.show()
