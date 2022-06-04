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
    u = users.copy()
    for i in u:
        if u[i].finished:
            u[i] = get_default()
    users = u
    pickle.dump(users, open('users.pkl', 'wb'))
    users = pickle.load(open('users.pkl', 'rb'))
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = RegistrationWindow(users)
        w.show()
        sys.exit(app.exec_())
    finally:
        w.close()
        print(users)
        pickle.dump(users, open('users.pkl', 'wb'))
