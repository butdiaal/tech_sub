from PyQt6.QtWidgets import QMessageBox
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from graf.auth_graf import Ui_AuthForm
from graf.reg_graf import Ui_RegForm
from graf.admin_graf import Ui_admin_wind
import database.db as db
import main  # Импортируем ваш основной модуль


# class AuthController:
#     def __init__(self, auth_window, main_app):
#         self.auth_window = auth_window
#         self.main_app = main_app
#
#     def auth(self):
#         """Метод авторизации пользователя"""
#         login = self.auth_window.Auth.lineEdit_auth_login.text().strip()
#         password = self.auth_window.Auth.lineEdit_aut_pass.text().strip()
#
#         user = db.get_user(login, password)
#         main.global_user_id = user[0]
#
#         if user[3] == 'admin':
#             self.main_app.showAdm()
#         # Сначала проверяем таблицу employees (сотрудники и админы)
#         employee = db.get_employee(login, password)
#         main.global_employee_id = employee[0]
#         if employee and employee['password'] == password:
#             main.global_user_id = employee['id']
#
#             if employee['is_admin']:
#                 self.main_app.showAdm()  # Открываем админ-панель
#             else:
#                 self.main_app.showEmployeeWindow()  # Открываем рабочее окно сотрудника
#             return
#
#         # Если не сотрудник, проверяем таблицу users (обычные пользователи)
#         user = db.get_user(login, password)
#         if user:
#             main.global_user_id = user['id']
#             self.main_app.showUserWindow()  # Открываем пользовательское окно
#             return
#
#         # Если не нашли нигде
#         QMessageBox.critical(
#             self.auth_window,
#             "Ошибка авторизации",
#             "Неверный логин или пароль.",
#             QMessageBox.StandardButton.Ok
#         )

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

        emp_id = db.get_employees_id(login)

        if emp_id:
            is_admin = emp_id[0]
            if is_admin:
                self.main.showAdm()
            else:
                self.main.showEmployeeWindow()
        else:
            user= db.get_user_id(login)
            if user:
                self.main.showUserWindow()
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