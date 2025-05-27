import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from graf.auth_graf import Ui_AuthForm
from graf.reg_graf import Ui_RegForm
from graf.admin_graf import Ui_admin_wind  # Импортируем класс из первого файла


class Main:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        # Основные окна
        self.auth_wind = AuthWind(self)
        self.reg_wind = RegWind(self)
        self.adm_wind = None

        self.showAuth()

    def showAuth(self):
        """Показать окно авторизации"""
        if hasattr(self, 'reg_wind') and self.reg_wind:
            self.reg_wind.hide()
        if hasattr(self, 'adm_wind') and self.adm_wind:
            self.adm_wind.hide()
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


class AuthWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Auth = Ui_AuthForm()
        self.Auth.setupUi(self)

        self.Auth.pushButton_reg_in_auth.clicked.connect(self.main.showReg)
        self.Auth.pushButton_auth_in.clicked.connect(self.check_auth)

    def check_auth(self):
        """Проверка авторизации"""
        login = self.Auth.lineEdit_auth_login.text()
        password = self.Auth.lineEdit_aut_pass.text()

        if login == "admin" and password == "admin":
            self.main.showAdm()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


class RegWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Reg = Ui_RegForm()
        self.Reg.setupUi(self)

        self.Reg.pushButton_reg_in_auth.clicked.connect(self.main.showAuth)
        self.Reg.pushButton_reg_in.clicked.connect(self.register_user)

    def register_user(self):
        """Регистрация нового пользователя"""
        # Здесь должна быть логика регистрации
        QMessageBox.information(self, "Успех", "Пользователь зарегистрирован")
        self.main.showAuth()


if __name__ == "__main__":
    app = Main()
    sys.exit(app.app.exec())