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
        login_data_is_correct = True

        if not login:
            login_data_is_correct = False
            QMessageBox.critical(
                self.reg_window,
                "Некорректные данные авторизации",
                "Укажите имя пользователя",
                QMessageBox.StandardButton.Ok
            )
        elif not password:
            login_data_is_correct = False
            QMessageBox.critical(
                self.reg_window,
                "Некорректные данные авторизации",
                "Укажите пароль пользователя",
                QMessageBox.StandardButton.Ok
            )

        if login_data_is_correct:
            # Используем функцию из main.py для проверки существования пользователя
            user_id = main.get_user_id(login)

            if user_id is not None:
                QMessageBox.critical(
                    self.reg_window,
                    "Ошибка создания пользователя",
                    f"Пользователь с именем {login} уже существует.\n"
                    f"Выполните вход под ним или измените имя пользователя",
                    QMessageBox.StandardButton.Ok
                )
            else:
                # Создаем пользователя с ролью 'user' по умолчанию
                db.create_user(login, password, 'user')
                user = db.get_user(login, password)
                main.global_user_id = user[0]

                QMessageBox.information(
                    self.reg_window,
                    "Создание пользователя",
                    f"Пользователь {login} успешно создан",
                    QMessageBox.StandardButton.Ok
                )

                self.main_app.showAuth()


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
        login = self.Auth.lineEdit_auth_login.text().strip()
        password = self.Auth.lineEdit_aut_pass.text().strip()

        # Проверка на пустые поля
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми")
            return

        # Сначала проверяем в таблице users
        user = db.get_user(login, password)
        if user:
            main.global_user_id = user[0]  # user_id
            if user[3] == 'admin':  # role
                self.main.showAdm()
            else:
                self.main.showUser()
            return

        # Если не нашли в users, проверяем в таблице employees
        employee_id = main.get_employees_id(login)
        if employee_id:
            # Здесь можно добавить дополнительную логику для сотрудников
            QMessageBox.information(self, "Вход", "Вы вошли как сотрудник")
            main.global_user_id = employee_id
            self.main.showEmployee()
            return

        # Если не нашли нигде
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
        login = self.Reg.lineEdit_reg_login.text().strip()
        password = self.Reg.lineEdit_reg_pass.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми")
            return

        # Используем функцию из main.py для проверки существования пользователя
        if main.get_user_id(login) is not None:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
            return

        # Создаем нового пользователя
        db.create_user(login, password, 'user')
        QMessageBox.information(self, "Успех", "Пользователь зарегистрирован")
        self.main.showAuth()