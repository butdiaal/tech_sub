import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from graf.auth_graf import Ui_AuthForm
from graf.reg_graf import Ui_RegForm
from admin import AdminWindow
from user import User_Window
from employee import Employee_Window
from graf.employees_graf import Employee_Ui_Form
from graf.user_graf import User_Ui_Form
import database.db as db
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
        self.auth_wind.hide()
        self.auth_wind.show()

    def showReg(self):
        """Показать окно регистрации"""
        self.auth_wind.hide()
        self.reg_wind.show()

    def showAdm(self):
        """Показать админскую панель"""
        self.auth_wind.hide()
        self.adm_wind = AdminWindow()
        self.adm_wind.show()

    def showEmp(self, id):
        """Показать панель сотрудников"""
        self.auth_wind.hide()
        self.emp_wind = Employee_Window(employee_id=id)
        self.emp_wind.show()

    def showUser(self,  id):
        """Показать пользовательскую панель"""
        self.auth_wind.hide()
        self.user_wind = User_Window(user_id=id)
        self.user_wind.show()


if __name__ == "__main__":
    app = Main()
    sys.exit(app.app.exec())
