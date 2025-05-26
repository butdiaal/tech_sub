import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from graf.auth_graf import *
from graf.reg_graf import *
from graf.admin_graf import *


class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.auth_wind = AuthWind(self)
        self.reg_wind = RegWind(self)
        self.adm_wind = AdmWind(self)

        self.showAuth()

    def showAuth(self):
        self.reg_wind.hide()
        self.auth_wind.show()

    def showReg(self):
        self.auth_wind.hide()
        self.reg_wind.show()

    def showAdm(self):
        self.auth_wind.hide()
        self.adm_wind.show()


class AuthWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Auth = Ui_AuthForm()
        self.Auth.setupUi(self)

        self.Auth.pushButton_reg_in_auth.clicked.connect(self.main.showReg)
        self.Auth.pushButton_auth_in.clicked.connect(self.main.showAdm)


class AdmWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Adm = Ui_AdminWindow()
        self.Adm.setup_ui(self)


class RegWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Reg = Ui_RegForm()
        self.Reg.setupUi(self)

        self.Reg.pushButton_reg_in_auth.clicked.connect(self.main.showAuth)


if __name__ == "__main__":
    app = Main()
    sys.exit(app.app.exec())
