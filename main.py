import sys
import pickle

from PyQt5 import QtWidgets

from registration import RegistrationWindow

if __name__ == "__main__":
    try:
        try:
            users = pickle.load(open('users.pkl', 'rb'))
        except:
            users = {}
        app = QtWidgets.QApplication(sys.argv)
        w = RegistrationWindow(users)
        w.show()
        sys.exit(app.exec_())
    finally:
        pickle.dump(users, open('users.pkl', 'wb'))
