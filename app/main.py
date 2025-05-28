import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from graf.auth_graf import Ui_AuthForm
from graf.reg_graf import Ui_RegForm
from graf.admin_graf import Ui_admin_wind
import auth

class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        # Основные окна
        self.auth_wind = auth.AuthWind(self)
        self.reg_wind = auth.RegWind(self)
        self.adm_wind = None

        self.showAuth()

    def showAuth(self):
        """Показать окно авторизации"""
        self.auth_wind.show()

    def showReg(self):
        """Показать окно регистрации"""
        self.auth_wind.hide()
        self.reg_wind.show()

    def showAdm(self):
        """Показать админскую панель"""
        self.auth_wind.hide()
        self.adm_wind = QtWidgets.QWidget()
        self.ui_adm = Ui_admin_wind()
        self.ui_adm.setupUi(self.adm_wind)

        self.adm_wind.show()



if __name__ == "__main__":
    app = Main()
    sys.exit(app.app.exec())