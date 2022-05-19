import pygame
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import *

from game_model import GameModel


class SettingsWindow(QtWidgets.QFrame):
    def __init__(self, model: GameModel):
        super().__init__()
        self.model = model
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle('Settings')
        self.window.setFixedSize(300, 400)
        self.window.setWindowIcon(QtGui.QIcon("resources/Icon.png"))
        self.window.setObjectName("SettingsWindow")
        self.window.setStyleSheet("#SettingsWindow{border-image:url(resources/background_settings.png)}")

        font = QtGui.QFont("BankGothic Md BT", 20)
        style = "background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);"

        self.sound_btn = QRadioButton(self.window)
        self.sound_btn.setObjectName(u"sound_btn")
        self.sound_btn.setGeometry(QtCore.QRect(50, 170, 150, 60))
        self.sound_btn.setFont(font)
        self.sound_btn.setStyleSheet(style)
        self.sound_btn.setChecked(False)
        self.sound_btn.clicked.connect(lambda: self.change_sound())

        self.level_box = QtWidgets.QComboBox(self.window)
        self.level_box.setObjectName(u"level_btn")
        self.level_box.setGeometry(QtCore.QRect(50, 220, 220, 50))
        self.level_box.setStyleSheet(style)
        self.level_box.addItem("select level...")
        self.level_box.setFont(QtGui.QFont("BankGothic Md BT", 15))
        self.level_box.addItem("level 1")
        self.level_box.addItem("level 2")
        self.level_box.addItem("level 3")
        self.level_box.addItem("level 4")
        self.level_box.addItem("level 5")
        self.level_box.addItem("level 6")
        self.level_box.addItem("level 7")
        self.level_box.addItem("level 8")
        self.level_box.addItem("level 9")
        self.level_box.activated.connect(lambda: self.change_start_level(self.level_box.currentIndex()))
        # ToDo смена уровней + новые уровни

        self._retranslate_ui()

    def change_start_level(self, n):
        self.model.levelIndex = n - 1
        self.model.level = self.model.levels[self.model.levelIndex]

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.sound_btn.setText(_translate("Settings", "sound"))

    def change_sound(self):
        if self.sound_btn.isChecked():
            musicname = "New Worlds.mp3"
            music = pygame.mixer.Sound("resources/" + musicname)
            pygame.mixer.Channel(1).play(music, -1)
        else:
            pygame.mixer.Channel(1).pause()


    def open_settings(self):
        self.window.show()
