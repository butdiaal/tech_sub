from PyQt6.QtWidgets import QMessageBox
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from graf.auth_graf import Ui_AuthForm
from graf.reg_graf import Ui_RegForm
from graf.admin_graf import Ui_admin_wind
import database.db as db
import main  # Импортируем ваш основной модуль


class RegController:
    def __init__(self, reg_window, main_app):
        self.reg_window = reg_window
        self.main_app = main_app

    def create_and_auth(self):
        """Метод регистрации и авторизации нового пользователя"""
        login = self.reg_window.Reg.lineEdit_reg_login.text().strip()
        password = self.reg_window.Reg.lineEdit_reg_pass.text().strip()
        phone = self.reg_window.Reg.lineEdit_reg_number.text().strip()

        if not all([login, password, phone]):
            QMessageBox.critical(
                self.reg_window,
                "Некорректные данные",
                "Все поля должны быть заполнены",
                QMessageBox.StandardButton.Ok
            )
            return

        try:
            # Пытаемся создать пользователя
            if not db.create_user(login, password, phone):
                raise Exception("Не удалось создать пользователя")

            user_id = db.get_user_id(login)
            if not user_id:
                raise Exception("Пользователь не найден после создания")

            main.global_user_id = user_id
            QMessageBox.information(
                self.reg_window,
                "Успешная регистрация",
                f"Пользователь {login} успешно зарегистрирован",
                QMessageBox.StandardButton.Ok
            )
            self.main_app.showUser()

        except Exception as e:
            QMessageBox.critical(
                self.reg_window,
                "Ошибка регистрации",
                f"Ошибка: {str(e)}",
                QMessageBox.StandardButton.Ok
            )


class AuthWind(QtWidgets.QWidget):
    def __init__(self, mainApp):
        super().__init__()
        self.main = mainApp
        self.Auth = Ui_AuthForm()
        self.Auth.setupUi(self)

        self.Auth.pushButton_reg_in_auth.clicked.connect(self.main.showReg)
        self.Auth.pushButton_auth_in.clicked.connect(self.check_auth)

    def check_auth(self):
        """Проверка авторизации для users и employees"""
        login = self.Auth.lineEdit_auth_login.text().strip()
        password = self.Auth.lineEdit_aut_pass.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми")
            return

        employee_id = db.get_employees_id(login)
        if employee_id:
            employee = db.get_employee(login, password)
            if employee:
                main.global_user_id = employee[0]
                if employee[6]:
                    self.main.showAdm()
                else:
                    self.main.showEmp()
                return

        user_id = db.get_user_id(login)
        if user_id:
            user = db.get_user(login, password)
            if user:
                main.global_user_id = user[0]
                self.main.showUser()
                return

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
        """Регистрация нового обычного пользователя"""
        controller = RegController(self, self.main)
        controller.create_and_auth()
