from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QPushButton, QLineEdit

from game_model import get_default
from main_window import MainWindow


class RegistrationWindow(QtWidgets.QMainWindow):
    def __init__(self, users):
        super().__init__()
        self.users = users
        style = "background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255);"
        self.setWindowIcon(QtGui.QIcon("resources/Icon.png"))
        self.setWindowTitle("Registration")
        self.setFixedSize(400, 200)
        self.setStyleSheet("RegistrationWindow{border-image:url(resources/background3.png)}")
        self.btn = QPushButton('Go!', self)
        self.btn.clicked.connect(self.handle_button)
        self.btn.setGeometry(170, 120, 60, 40)
        self.btn.setFont(QtGui.QFont("BankGothic Md BT", 16))
        self.btn.setStyleSheet(style)
        self.textbox = QLineEdit(self)
        self.textbox.setFont(QtGui.QFont("BankGothic Md BT", 12))
        self.textbox.move(120, 70)
        self.textbox.resize(160, 40)
        self.textbox.setStyleSheet(style)

    def handle_button(self):
        if not self.textbox.text() in self.users.keys():
            self.users[self.textbox.text()] = get_default()
        self.close()
        w = MainWindow(self.users[self.textbox.text()], self.users, self.textbox.text())
        w.show()


