import sys
import pickle

from PyQt5 import QtWidgets

from registration import RegistrationWindow
from game_model import get_default

if __name__ == "__main__":
    try:
        users = pickle.load(open('users.pkl', 'rb'))
    except:
        users = {}
    for i in users:
        if users[i].finished:
            users[i] = get_default()
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = RegistrationWindow(users)
        w.show()
        sys.exit(app.exec_())
    finally:
        w.close()
        print(users)
        pickle.dump(users, open('users.pkl', 'wb'))
