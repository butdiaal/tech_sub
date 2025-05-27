from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
import database.db as db
import main  # Импортируем ваш основной модуль


class AuthController:
    def __init__(self, auth_window, main_app):
        self.auth_window = auth_window
        self.main_app = main_app

    def auth(self):
        """Метод авторизации пользователя"""
        login = self.auth_window.Auth.lineEdit_auth_login.text().strip()
        password = self.auth_window.Auth.lineEdit_aut_pass.text().strip()

        user = db.get_user(login, password)

        if user is None:
            QMessageBox.critical(
                self.auth_window,
                "Ошибка авторизации",
                "Неверный логин или пароль.",
                QMessageBox.StandardButton.Ok
            )
        else:
            main.global_user_id = user[0]

            if user[3] == 'admin':
                self.main_app.showAdm()
            else:
                QMessageBox.information(
                    self.auth_window,
                    "Успешная авторизация",
                    f"Добро пожаловать, {login}!",
                    QMessageBox.StandardButton.Ok
                )


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
            user_id = db.get_user_id(login)

            if user_id is not None:
                QMessageBox.critical(
                    self.reg_window,
                    "Ошибка создания пользователя",
                    f"Пользователь с именем {login} уже существует.\n"
                    f"Выполните вход под ним или измените имя пользователя",
                    QMessageBox.StandardButton.Ok
                )
            else:
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