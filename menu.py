from PyQt5 import QtWidgets, QtCore, QtGui

from settings import SettingsWindow


class Menu(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.settingsWindow = SettingsWindow()

        font = QtGui.QFont()
        font.setPointSize(28)

        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setGeometry(QtCore.QRect(450, 350, 300, 100))
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(lambda: self.main_window.change_window(1))

        self.config_btn = QtWidgets.QPushButton(self)
        self.config_btn.setGeometry(QtCore.QRect(450, 500, 300, 100))
        self.config_btn.setFont(font)
        self.config_btn.setObjectName("config_btn")
        self.config_btn.clicked.connect(self.settingsWindow.open_settings)

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.start_btn.setText(_translate("Menu", "Играть"))
        self.config_btn.setText(_translate("Menu", "Настройки"))
