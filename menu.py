from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFontDatabase

from settings import SettingsWindow
from game import Game


class Menu(QtWidgets.QFrame):
    def __init__(self, main_window, model, user, name):
        super().__init__()
        self.users = user
        self.name = name
        self.main_window = main_window
        self.settingsWindow = SettingsWindow(model)
        self.setObjectName("MenuWindow")
        self.setStyleSheet("#MenuWindow{border-image:url(resources/background_menu.png)}")

        QFontDatabase.addApplicationFont("resources/BNKGOTHM.TTF")
        font = QtGui.QFont("BankGothic Md BT", 32)
        style = "background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);"

        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setGeometry(QtCore.QRect(450, 350, 300, 100))
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(lambda: self.main_window.change_window(1))
        self.start_btn.setStyleSheet(style)

        self.config_btn = QtWidgets.QPushButton(self)
        self.config_btn.setGeometry(QtCore.QRect(450, 450, 300, 100))
        self.config_btn.setFont(font)
        self.config_btn.setObjectName("config_btn")
        self.config_btn.clicked.connect(self.settingsWindow.open_settings)
        self.config_btn.setStyleSheet(style)
        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.start_btn.setText(_translate("Menu", "play"))
        self.config_btn.setText(_translate("Menu", "settings"))

    def start_game(self):
        self.main_window.change_window(1, Game(self, self.model, self.users, self.name))

