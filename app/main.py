import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from graf.auth_graf import Ui_AuthForm
from graf.reg_graf import Ui_RegForm


class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.auth_wind = AuthWind(self)
        self.reg_wind = RegWind(self)

        self.showAuth()

    def showAuth(self):
        self.reg_wind.hide()
        self.auth_wind.show()

    def showReg(self):
        self.auth_wind.hide()
        self.reg_wind.show()


class AuthWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Auth = Ui_AuthForm()
        self.Auth.setupUi(self)

        self.Auth.pushButton_reg_in_auth.clicked.connect(self.main.showReg)


class RegWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Auth = Ui_RegForm()
        self.Auth.setupUi(self)

        self.Auth.pushButton_reg_in_auth.clicked.connect(self.main.showAuth)


if __name__ == "__main__":
    app = Main()
    sys.exit(app.app.exec())